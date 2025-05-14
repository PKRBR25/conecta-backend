"""Production environment configuration."""

from app.core.config.base import BaseConfig


class ProductionConfig(BaseConfig):
    """Production configuration."""

    PROJECT_NAME: str = "Conecta API"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "${DATABASE_URL}"  # Set by Railway

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
        "https://conecta.up.railway.app",
        "https://conecta.vercel.app",
    ]

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 30  # Stricter limit for production
