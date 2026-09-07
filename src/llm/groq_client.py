import os
from dotenv import load_dotenv
from groq import Groq
from src.utils.logger import get_logger

load_dotenv()
log = get_logger(__name__)

class GroqClient:
    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = model
        log.info(f"GroqClient initialized with model: {self.model}")

    def generate_response(self, prompt: str) -> str:
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Groq API Error: {str(e)}")