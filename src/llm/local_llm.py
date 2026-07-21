import os
from dotenv import load_dotenv
from src.utils.logger import get_logger

load_dotenv()
log = get_logger(__name__)

class LocalLLM:
    def __init__(self):
        # Check which API keys are available
        self.has_gemini = bool(os.getenv("GEMINI_API_KEY"))
        self.has_groq = bool(os.getenv("GROQ_API_KEY"))
        
        # Initialize available clients
        self.gemini_client = None
        self.groq_client = None
        
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
        """
        # Try Gemini
        if self.has_gemini and self.gemini_client:
            try:
                return self.gemini_client.generate_response(prompt)
            except Exception as e:
                log.warning(f"LLM Router: Gemini failed ({str(e)[:50]}...). Falling back to Groq.")
        
        # Try Groq
        if self.has_groq and self.groq_client:
            try:
                return self.groq_client.generate_response(prompt)
            except Exception as e:
                log.warning(f"LLM Router: Groq failed ({str(e)[:50]}...).")
                
        # If both failed or neither was configured
        raise RuntimeError("All LLM providers failed. Check your API keys in .env.")