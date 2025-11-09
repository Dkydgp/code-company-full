# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Central configuration class for the Code Company Backend."""

    # 🔹 API Keys
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")

    # 🔹 Search API Settings
    SEARCH_MODE = os.getenv("SEARCH_MODE", "mock")   # 'mock' or 'http'
    SEARCH_API_URL = os.getenv("SEARCH_API_URL", "")
    SEARCH_API_KEY = os.getenv("SEARCH_API_KEY", "")
    SEARCH_TIMEOUT = int(os.getenv("SEARCH_TIMEOUT", 10))

    # 🔹 File Paths
    MEMORY_FILE = os.getenv("MEMORY_FILE", "app/data/memory.json")
    DATA_FILE = os.getenv("DATA_FILE", "app/data/data.json")

    # 🔹 Flask & General Settings
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_change_in_prod")

    # 🔹 Supabase (for later data sync)
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
