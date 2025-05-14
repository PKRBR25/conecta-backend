"""Database session module."""

import logging
from sqlmodel import Session, create_engine

from app.core.config import settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Database URL: {settings.DATABASE_URL}")
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, echo=True)


def get_session():
    """Get database session."""
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
