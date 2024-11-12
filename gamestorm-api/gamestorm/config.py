import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Configuration settings for the GameStorm application."""
    API_KEY = os.getenv("ZEBEDEE_API_KEY")  # API key for ZEBEDEE
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./gamestorm.db")  # SQLite database

settings = Settings()

