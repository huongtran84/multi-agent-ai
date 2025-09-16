import os
from dotenv import load_dotenv

load_dotenv()
class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "127.0.0.1")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", 9999))
    ALLOWED_MODELS_NAMES = ["openai/gpt-oss-120b","qwen/qwen3-32b"]
    
settings = Settings()