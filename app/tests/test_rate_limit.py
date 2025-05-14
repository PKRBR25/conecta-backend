"""Test rate limiting."""

import pytest
import time
from unittest.mock import MagicMock, patch
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session
from unittest.mock import MagicMock

from app.core.config import settings
from app.main import app
from app.api import deps
from app.db.models.user import User


@pytest.fixture
def client():
    """Create a test client."""
    # Create test client
    return TestClient(app)


@pytest.fixture
def mock_db():
    """Create a mock database session."""
    mock = MagicMock(spec=Session)

    # Override get_db dependency
    def override_get_db():
        return mock

    app.dependency_overrides[deps.get_db] = override_get_db
    yield mock
    app.dependency_overrides.clear()


def test_login_rate_limit(client, mock_db):
    """Test rate limiting on login endpoint."""
    # Mock user query to always return None
    mock_db.exec.return_value.first.return_value = None

    # Make 6 requests (limit is 5 per minute)
    responses = []
    for _ in range(6):
        response = client.post(
            f"{settings.API_V1_STR}/auth/login",
            data={"username": "test@example.com", "password": "wrongpassword"},
        )
        responses.append(response)
        time.sleep(0.1)  # Add a small delay between requests

    # All requests should be rate limited
    for response in responses:
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        error_response = response.json()
        assert "Rate limit exceeded" in error_response["detail"]


def test_register_rate_limit(client, mock_db):
    """Test rate limiting on register endpoint."""
    # Mock user query to always return a user (simulating existing user)
    mock_user = User(
        id=1, email="test@example.com", hashed_password="hashedpass", is_active=True,
    )
    mock_db.exec.return_value.first.return_value = mock_user

    # Make 6 requests (limit is 5 per minute)
    responses = []
    for _ in range(6):
        response = client.post(
            f"{settings.API_V1_STR}/auth/register",
            json={
                "email": "test@example.com",
                "password": "testpassword123",
                "confirm_password": "testpassword123",
            },
        )
        responses.append(response)
        time.sleep(0.1)  # Add a small delay between requests

    # All requests should be rate limited
    for response in responses:
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        error_response = response.json()
        assert "Rate limit exceeded" in error_response["detail"]


def test_password_recovery_rate_limit(client, mock_db):
    """Test rate limiting on password recovery endpoint."""
    # Mock user query to always return None
    mock_db.exec.return_value.first.return_value = None

    # Make 4 requests (limit is 3 per minute)
    responses = []
    for _ in range(4):
        response = client.post(
            f"{settings.API_V1_STR}/auth/password-recovery/test@example.com"
        )
        responses.append(response)
        time.sleep(0.1)  # Add a small delay between requests

    # All requests should be rate limited
    for response in responses:
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        error_response = response.json()
        assert "Rate limit exceeded" in error_response["detail"]
