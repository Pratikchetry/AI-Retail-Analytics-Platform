from src.llm.groq_client import GroqClient

class LocalLLM:

    def __init__(self):
        self.client = GroqClient()

    def generate(
        self,
        prompt: str
    ):
        return self.client.generate_response(
            prompt
        )