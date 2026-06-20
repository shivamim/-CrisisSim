"""
config.py — Application configuration
======================================
"""

import os
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str
    GROQ_API_KEY: str = ""
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    TWITTER_BEARER_TOKEN: str = ""
    REDDIT_CLIENT_ID: str = ""
    REDDIT_CLIENT_SECRET: str = ""
    FRONTEND_URL: str = "http://localhost:3000"
    DB_SSL: bool = True

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def ensure_async_driver(cls, v):
        """Auto-convert postgresql:// to postgresql+asyncpg://"""
        if isinstance(v, str) and v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v


settings = Settings()

# Set GROQ_API_KEY in OS environment so langchain-groq can find it
os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY or "gsk_placeholder_for_startup"

if not settings.GROQ_API_KEY:
    logger.warning("GROQ_API_KEY is not set. Simulations will fail until it's configured.")
