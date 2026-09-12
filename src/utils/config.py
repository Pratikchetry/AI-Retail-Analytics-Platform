try:
    from dotenv import load_dotenv  # type: ignore[import-not-found]
except ImportError:
    def load_dotenv(*args, **kwargs):
        """Fallback when python-dotenv is not installed.

        This keeps the configuration module importable in minimal
        environments while leaving environment variable loading a no-op.
        """
        return False

import os

load_dotenv()

class Settings:
    # Standardized to DATABASE_URL (Chainlit is removed, so no more hijacking)
    DATABASE_URL = os.getenv("DATABASE_URL")

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