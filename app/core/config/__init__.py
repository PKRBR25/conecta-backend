"""Configuration module."""

import os

from app.core.config.base import BaseConfig
from app.core.config.staging import StagingConfig
from app.core.config.production import ProductionConfig


def get_config() -> BaseConfig:
    """Get the appropriate configuration based on the environment."""
    env = os.getenv("ENVIRONMENT", "development")
    if env == "production":
        return ProductionConfig()
    elif env == "staging":
        return StagingConfig()
    return DevelopmentConfig()
    """Get the configuration based on the environment."""
    env = os.getenv("ENVIRONMENT", "staging")
    if env == "production":
        return ProductionConfig()
    return StagingConfig()


# Create a global instance of the configuration
settings = get_config()
