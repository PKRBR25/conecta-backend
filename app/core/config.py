"""Application configuration module."""
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Conecta"

    # Authentication
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str | None = None

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]  # Frontend URL

    # Email
    SMTP_TLS: bool = True
    SMTP_PORT: int | None = None
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "app/email-templates"
    SERVER_HOST: str = "http://localhost:3000"  # Frontend URL

    # Internationalization
    SUPPORTED_LANGUAGES: List[str] = ["en", "pt-br"]
    DEFAULT_LANGUAGE: str = "en"

    class Config:
        """Pydantic config class."""

        case_sensitive = True
        env_file = ".env"

    @property
    def database_url(self) -> str:
        """Get database URL."""
        if self.DATABASE_URL:
            return self.DATABASE_URL

        from urllib.parse import quote_plus

        password = quote_plus(self.POSTGRES_PASSWORD)
        return f"postgresql://{self.POSTGRES_USER}:{password}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"


settings = Settings()
