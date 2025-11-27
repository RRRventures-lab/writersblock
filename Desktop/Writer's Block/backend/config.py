from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./songs.db"

    # API
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    DEBUG: bool = True

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    ENABLE_AI_FEATURES: bool = True

    # Audio
    MAX_AUDIO_FILE_SIZE: int = 52428800  # 50MB
    SUPPORTED_AUDIO_FORMATS: List[str] = ["mp3", "wav", "ogg", "flac"]
    AUDIO_UPLOAD_DIR: str = "./uploads/audio"

    # Redis
    REDIS_URL: Optional[str] = None
    ENABLE_REDIS: bool = False

    # JWT
    JWT_SECRET_KEY: str = "your_super_secret_key_change_this_in_production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
