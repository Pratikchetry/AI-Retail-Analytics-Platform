import os
import time
from dotenv import load_dotenv
from src.utils.logger import get_logger

load_dotenv()
log = get_logger(__name__)

class LocalLLM:
    def __init__(self):
        self.has_gemini = bool(os.getenv("GEMINI_API_KEY"))
        self.has_groq = bool(os.getenv("GROQ_API_KEY"))
        
        self.gemini_client = None
        self.groq_client = None
        
        # Rate limit tracking
        self.gemini_disabled_until = 0
        
        if self.has_gemini:
            try:
                from src.llm.gemini_client import GeminiClient
                self.gemini_client = GeminiClient()
                log.info("LLM Router: Gemini client loaded.")
            except Exception as e:
                log.warning(f"LLM Router: Failed to load Gemini: {e}")
                self.has_gemini = False
                
        if self.has_groq:
            try:
                from src.llm.groq_client import GroqClient
                self.groq_client = GroqClient()
                log.info("LLM Router: Groq client loaded.")
            except Exception as e:
                log.warning(f"LLM Router: Failed to load Groq: {e}")
                self.has_groq = False

    def generate(self, prompt: str) -> str:
        """
        Tries Gemini first (better free limits), falls back to Groq.
        If Gemini hits a 429 rate limit, disables Gemini for 60 seconds.
        """
        # Check if Gemini is currently disabled due to rate limiting
        use_gemini = self.has_gemini and self.gemini_client and (time.time() > self.gemini_disabled_until)
        
        if use_gemini:
            try:
                return self.gemini_client.generate_response(prompt)
            except Exception as e:
                err_msg = str(e)
                # Print the FULL error message so we can see why it's failing
                log.warning(f"LLM Router: Gemini failed. FULL ERROR: {err_msg}")
                
                if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                    log.warning("LLM Router: Gemini rate limited. Disabling for 60 seconds and falling back to Groq.")
                    self.gemini_disabled_until = time.time() + 60
        
        # Try Groq
        if self.has_groq and self.groq_client:
            try:
                return self.groq_client.generate_response(prompt)
            except Exception as e:
                log.warning(f"LLM Router: Groq failed ({str(e)[:50]}...).")
                
        # If both failed or neither was configured
        raise RuntimeError("All LLM providers failed. Check your API keys in .env.")