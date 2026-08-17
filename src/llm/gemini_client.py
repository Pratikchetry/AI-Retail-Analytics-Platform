import os
import httpx
from dotenv import load_dotenv
from src.utils.logger import get_logger

load_dotenv()
log = get_logger(__name__)

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        # Using the latest stable flash model available in your account
        self.model = "gemini-flash-latest"
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        log.info("GeminiClient initialized using direct REST API.")
        
    def generate_response(self, prompt: str) -> str:
        try:
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            
            # Make direct REST call with 30s timeout
            response = httpx.post(self.api_url, json=payload, timeout=30.0)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract text from the JSON response
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "")
            
            return str(data)
            
        except Exception as e:
            raise RuntimeError(f"Gemini API Error: {str(e)}")