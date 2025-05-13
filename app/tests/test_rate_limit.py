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
    # Mock user query to always return None to simulate failed login attempts
    mock_db.exec.return_value.first.return_value = None

    data = {"username": "test@example.com", "password": "wrongpassword"}

    # Make 6 requests (limit is 5 per minute)
    responses = []
    for _ in range(6):
        response = client.post(f"{settings.API_V1_STR}/auth/login", data=data)
        responses.append(response)
        time.sleep(0.1)  # Add a small delay between requests

    # First 5 requests should return 401 (Unauthorized)
    for response in responses[:5]:
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect email or password" in response.json()["detail"]

    # 6th request should be rate limited
    assert responses[5].status_code == status.HTTP_429_TOO_MANY_REQUESTS
    error_response = responses[5].json()
    assert error_response["error"] == "Rate limit exceeded: 5 per 1 minute"


def test_register_rate_limit(client, mock_db):
    """Test rate limiting on register endpoint."""
    # Mock database query to always return a user (user already exists)
    mock_user = MagicMock()
    mock_user.email = "test@example.com"
    mock_db.exec.return_value.first.return_value = mock_user

    data = {
        "email": "test@example.com",
        "password": "StrongPass123!",  # Use strong password to test rate limit
        "full_name": "Test User",
    }

    # Make 6 requests (limit is 5 per minute)
    responses = []
    for _ in range(6):
        response = client.post(f"{settings.API_V1_STR}/auth/register", json=data)
        responses.append(response)
        time.sleep(0.1)  # Add a small delay between requests

    # First 5 requests should return 400 (Bad Request - user already exists)
    for response in responses[:5]:
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email already registered" in response.json()["detail"].lower()

    # 6th request should be rate limited
    assert responses[5].status_code == status.HTTP_429_TOO_MANY_REQUESTS
    error_response = responses[5].json()
    assert error_response["error"] == "Rate limit exceeded: 5 per 1 minute"


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

    # First 3 requests should return 404 (Not Found)
    for response in responses[:3]:
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "User not found" in response.json()["detail"]

    # 4th request should be rate limited
    assert responses[3].status_code == status.HTTP_429_TOO_MANY_REQUESTS
    error_response = responses[3].json()
    assert error_response["error"] == "Rate limit exceeded: 3 per 1 minute"
