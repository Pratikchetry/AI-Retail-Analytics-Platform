import os
from dotenv import load_dotenv
from src.utils.logger import get_logger

load_dotenv()
log = get_logger(__name__)

class LocalLLM:
    def __init__(self):
        # Force Groq as the sole provider to avoid Gemini timeout delays
        self.has_groq = bool(os.getenv("GROQ_API_KEY"))
        self.groq_client = None
        
        if self.has_groq:
            try:
                from src.llm.groq_client import GroqClient
                self.groq_client = GroqClient()
                log.info("LLM Router: Groq client loaded (Sole Provider).")
            except Exception as e:
                log.warning(f"LLM Router: Failed to load Groq: {e}")
                self.has_groq = False

    def generate(self, prompt: str) -> str:
        """Uses Groq exclusively to prevent gateway timeouts."""
        if self.has_groq and self.groq_client:
            try:
                return self.groq_client.generate_response(prompt)
            except Exception as e:
                log.warning(f"LLM Router: Groq failed ({str(e)[:50]}...).")
                
        raise RuntimeError("LLM provider failed. Check your GROQ_API_KEY in .env.")