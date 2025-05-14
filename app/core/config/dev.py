"""Development environment configuration."""

from pydantic import ConfigDict
from app.core.config.base import BaseConfig


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    model_config = ConfigDict(extra="allow")

    PROJECT_NAME: str = "Conecta API (Development)"
    DEBUG: bool = True

    # Database - Local PostgreSQL
    DATABASE_URL: str = "postgresql://conecta_dev:conecta_dev@localhost:5432/conecta_dev"

    # Email settings for development (can use a service like Mailtrap)
    SMTP_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: str = "smtp.mailtrap.io"  # You can replace with your preferred email testing service
    SMTP_USER: str = ""  # Add your test SMTP credentials
    SMTP_PASSWORD: str = ""  # Add your test SMTP credentials
    EMAILS_FROM_EMAIL: str = "test@conecta.dev"
    EMAILS_FROM_NAME: str = "Conecta (Dev)"