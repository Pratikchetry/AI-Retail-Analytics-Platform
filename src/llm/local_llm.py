import os
from dotenv import load_dotenv
from src.utils.logger import get_logger

load_dotenv()
log = get_logger(__name__)

class LocalLLM:
    def __init__(self, model_size: str = "70b"):
        """
        model_size: '8b' for fast routing/classification tasks
                    '70b' for deep reasoning, SQL generation, critic
        """
        self.has_groq = bool(os.getenv("GROQ_API_KEY"))
        self.groq_client = None

        if model_size == "8b":
            self.model_name = "openai/gpt-oss-20b"    # fastest free model
        else:
            self.model_name = "openai/gpt-oss-120b"   # most capable free model

        if self.has_groq:
            try:
                from src.llm.groq_client import GroqClient
                self.groq_client = GroqClient(model=self.model_name)
                log.info(f"LocalLLM ready: {self.model_name}")
            except Exception as e:
                log.warning(f"LocalLLM: Groq load failed: {e}")
                self.has_groq = False

    def generate(self, prompt: str) -> str:
        if self.has_groq and self.groq_client:
            try:
                return self.groq_client.generate_response(prompt)
            except Exception as e:
                log.warning(f"LocalLLM: Groq call failed: {str(e)[:80]}")

        raise RuntimeError(
            "LLM provider failed. Check GROQ_API_KEY in .env."
        )