"""Staging environment configuration."""

from pydantic import ConfigDict
from app.core.config.base import BaseConfig


class StagingConfig(BaseConfig):
    """Staging configuration."""

    model_config = ConfigDict(extra="allow")

    PROJECT_NAME: str = "Conecta API (Staging)"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://conecta_bhcn_user:1Ec9UPdFBrbuQF0Gw8KRdBmM8jcuRaIU@dpg-d0idhlu3jp1c73d1tb90-a.virginia-postgres.render.com/conecta_bhcn"

    # Email
    SMTP_TLS: bool = True
    SMTP_PORT: int = 465
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_USER: str = "${SMTP_USER}"  # Set by Railway
    SMTP_PASSWORD: str = "${SMTP_PASSWORD}"  # Set by Railway

    # Security
    SECRET_KEY: str = "${SECRET_KEY}"  # Set by Railway
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "https://conecta-staging.up.railway.app",
        "https://conecta-staging.vercel.app",
    ]

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60  # Higher limit for staging
