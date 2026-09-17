import os
import time
from dotenv import load_dotenv
from src.utils.logger import get_logger

load_dotenv()
log = get_logger(__name__)

# ------------------------------------------------------------------
# Circuit breaker configuration
# ------------------------------------------------------------------
# After this many consecutive Groq failures, skip Groq entirely and go
# straight to Gemini for COOLDOWN_SECONDS, instead of waiting through
# Groq's own retry/backoff on every single call while it's down.
FAILURE_THRESHOLD = 3
COOLDOWN_SECONDS = 60


class LocalLLM:
    # Class-level (shared across all instances/nodes in this process)
    # circuit breaker state for Groq. This is intentionally simple and
    # in-memory: it resets on process restart and is not shared across
    # multiple server workers/replicas. That's a known limitation, not
    # an oversight — see README "Honest Limitations".
    _groq_consecutive_failures = 0
    _groq_breaker_opened_at = None

    def __init__(self, model_size: str = "70b"):
        """
        model_size: '8b' for fast routing/classification tasks
                    '70b' for deep reasoning, SQL generation, critic
        """
        self.has_groq = bool(os.getenv("GROQ_API_KEY"))
        self.has_gemini = bool(os.getenv("GEMINI_API_KEY"))
        self.groq_client = None
        self.gemini_client = None

        if model_size == "8b":
            self.model_name = "openai/gpt-oss-20b"    # fastest free model
        else:
            self.model_name = "openai/gpt-oss-120b"   # most capable free model

        if self.has_groq:
            try:
                from src.llm.groq_client import GroqClient
                self.groq_client = GroqClient(model=self.model_name)
                log.info(f"LocalLLM ready: {self.model_name} (Groq)")
            except Exception as e:
                log.warning(f"LocalLLM: Groq init failed: {e}")
                self.has_groq = False

        if self.has_gemini:
            try:
                from src.llm.gemini_client import GeminiClient
                self.gemini_client = GeminiClient()
                log.info("LocalLLM: Gemini fallback ready")
            except Exception as e:
                log.warning(f"LocalLLM: Gemini init failed: {e}")
                self.has_gemini = False

        if not self.has_groq and not self.has_gemini:
            log.error("LocalLLM: no working LLM provider configured (checked Groq, Gemini)")

    @classmethod
    def _groq_breaker_is_open(cls) -> bool:
        """True if the circuit breaker is currently OPEN (skip Groq)."""
        if cls._groq_breaker_opened_at is None:
            return False
        elapsed = time.monotonic() - cls._groq_breaker_opened_at
        if elapsed >= COOLDOWN_SECONDS:
            # Cooldown expired — close the breaker, allow Groq to be tried again
            log.info("LocalLLM: Groq circuit breaker cooldown elapsed, closing breaker")
            cls._groq_breaker_opened_at = None
            cls._groq_consecutive_failures = 0
            return False
        return True

    @classmethod
    def _record_groq_failure(cls):
        cls._groq_consecutive_failures += 1
        if cls._groq_consecutive_failures >= FAILURE_THRESHOLD and cls._groq_breaker_opened_at is None:
            cls._groq_breaker_opened_at = time.monotonic()
            log.warning(
                f"LocalLLM: Groq circuit breaker OPEN after "
                f"{cls._groq_consecutive_failures} consecutive failures "
                f"— skipping Groq for {COOLDOWN_SECONDS}s"
            )

    @classmethod
    def _record_groq_success(cls):
        cls._groq_consecutive_failures = 0
        cls._groq_breaker_opened_at = None

    def generate(self, prompt: str) -> str:
        groq_error = None
        gemini_error = None

        # --- Try Groq, unless the circuit breaker is open ---
        if self.has_groq and self.groq_client and not self._groq_breaker_is_open():
            try:
                result = self.groq_client.generate_response(prompt)
                self._record_groq_success()
                return result
            except Exception as e:
                groq_error = str(e)[:200]
                log.warning(f"LocalLLM: Groq call failed: {groq_error}")
                self._record_groq_failure()
        elif self.has_groq and self._groq_breaker_is_open():
            log.info("LocalLLM: Groq circuit breaker OPEN, skipping straight to Gemini")

        # --- Fall back to Gemini ---
        if self.has_gemini and self.gemini_client:
            try:
                result = self.gemini_client.generate_response(prompt)
                log.info("LocalLLM: served by Gemini fallback")
                return result
            except Exception as e:
                gemini_error = str(e)[:200]
                log.warning(f"LocalLLM: Gemini fallback also failed: {gemini_error}")

        raise RuntimeError(
            "LLM provider failed on both Groq and Gemini. "
            f"Groq error: {groq_error or 'not attempted (breaker open or not configured)'}. "
            f"Gemini error: {gemini_error or 'not attempted or not configured'}. "
            "Check GROQ_API_KEY and GEMINI_API_KEY in .env."
        )