"""Test configuration file."""

import asyncio
from datetime import datetime, timedelta
from typing import AsyncGenerator, Generator
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.core import security
from app.core.config import settings
from app.db.models.user import User, PasswordResetToken
from app.api.deps import get_db
from app.main import app


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_db_engine():
    """Create a test database engine."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def db(test_db_engine) -> Generator:
    """Create a test database session."""
    with Session(test_db_engine) as session:
        yield session


@pytest.fixture
def client(db: Session) -> Generator:
    """Create a test client with the test database."""
    app.dependency_overrides = {}

    def get_test_db():
        return db

    app.dependency_overrides[get_db] = get_test_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_user(db: Session) -> User:
    """Create a test user."""
    user = User(
        email="test@example.com",
        hashed_password=security.get_password_hash("test-password"),
        full_name="Test User",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_password_reset_token(db: Session, test_user: User) -> PasswordResetToken:
    """Create a test password reset token."""
    token = PasswordResetToken(
        user_id=test_user.id,
        token="123456",
        expires_at=datetime.utcnow() + timedelta(hours=24),
        is_used=False,
    )
    db.add(token)
    db.commit()
    db.refresh(token)
    return token


@pytest.fixture
def test_superuser(db: Session) -> User:
    """Create a test superuser."""
    user = User(
        email="admin@example.com",
        hashed_password=security.get_password_hash("admin-password"),
        full_name="Admin User",
        is_superuser=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
