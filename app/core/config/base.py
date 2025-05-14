"""Base configuration for all environments."""

from typing import Any

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    """Base configuration."""

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Conecta API"
    DEFAULT_LANGUAGE: str = "en"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # Database
    DATABASE_URL: str = "postgresql://conecta_bhcn_user:1Ec9UPdFBrbuQF0Gw8KRdBmM8jcuRaIU@dpg-d0idhlu3jp1c73d1tb90-a.virginia-postgres.render.com/conecta_bhcn"

    # JWT
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # Email
    SMTP_TLS: bool = True
    SMTP_PORT: int
    SMTP_HOST: str
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAILS_FROM_EMAIL: str = "emailconectateste@gmail.com"
    EMAILS_FROM_NAME: str = "Conecta"

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 5

    model_config = ConfigDict(
        case_sensitive=True,
        env_file=".env",
    )
