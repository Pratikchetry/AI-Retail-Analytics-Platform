import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

class GeminiClient:
    def __init__(self):
        # Initialize the new Google GenAI Client
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        # Use the new Gemini 2.0 Flash model (super fast, massive free tier)
        self.model = "gemini-2.0-flash-001"

    def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text
        except Exception as e:
            raise RuntimeError(f"Gemini API Error: {str(e)}")
        