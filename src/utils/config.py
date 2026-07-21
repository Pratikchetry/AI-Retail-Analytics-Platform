# src/utils/config.py

from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    # Renamed from DATABASE_URL to prevent Chainlit from hijacking it
    DATABASE_URL = os.getenv("WAREHOUSE_DB_URL")

    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    CHROMA_DB_PATH = os.getenv(
        "CHROMA_DB_PATH",
        "./chroma_store"
    )

    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )

settings = Settings()