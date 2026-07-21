import time

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()


class GroqClient:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.model = "llama-3.3-70b-versatile"

    def generate_response(
        self,
        prompt: str
    ) -> str:
        # Retry with exponential backoff on rate limits (429).
        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
                return response.choices[0].message.content
            except Exception as e:
                msg = str(e).lower()
                if "429" in msg or "rate limit" in msg or "too many requests" in msg:
                    wait = min(2 ** attempt * 3, 60)  # 3, 6, 12, 24, 48s capped at 60
                    time.sleep(wait)
                    continue
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                raise
        raise RuntimeError("Groq rate limit: max retries exceeded")