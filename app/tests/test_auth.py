"""Test authentication endpoints."""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlmodel import Session
from fastapi import status

from app.core import security
from app.core.config import settings
from app.db.models.user import User, PasswordResetToken
from app.main import app
from app.api import deps


@pytest.fixture
def client():
    """Create a test client."""
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


def test_register_user(client, mock_db):
    """Test user registration."""
    # Mock database query
    mock_db.exec.return_value.first.return_value = None

    # Mock user creation
    mock_user = User(
        email="newuser@example.com",
        hashed_password=security.get_password_hash("Test@123"),
        full_name="New User",
    )
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = mock_user

    data = {
        "email": "newuser@example.com",
        "password": "Test@123",
        "full_name": "New User",
    }

    with patch("app.api.deps.get_db", return_value=mock_db):
        response = client.post(f"{settings.API_V1_STR}/auth/register", json=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert "access_token" in response.json()
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


def test_password_recovery(client, mock_db):
    """Test password recovery request."""
    # Mock user query
    mock_user = User(
        email="test@example.com",
        hashed_password=security.get_password_hash("oldpassword"),
        full_name="Test User",
    )
    mock_db.exec.return_value.first.return_value = mock_user

    # Mock token creation
    mock_token = PasswordResetToken(
        user_id=1, token="123456", expires_at=datetime.utcnow() + timedelta(minutes=15)
    )
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = mock_token

    # Mock email sending
    with patch("app.core.email.send_reset_password_email") as mock_send_email:
        mock_send_email.return_value = None  # This is needed for async functions
        response = client.post(
            f"{settings.API_V1_STR}/auth/password-recovery/test@example.com"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["msg"] == "Password recovery email sent"
        assert mock_send_email.call_count == 1


def test_reset_password(client, mock_db):
    """Test password reset."""
    # Mock token query
    mock_token = PasswordResetToken(
        user_id=1, token="123456", expires_at=datetime.utcnow() + timedelta(minutes=15)
    )
    mock_db.exec.return_value.first.return_value = mock_token

    # Mock user query for the second call
    mock_user = User(
        id=1,
        email="test@example.com",
        hashed_password=security.get_password_hash("oldpassword"),
        full_name="Test User",
    )
    mock_db.get.return_value = mock_user

    data = {"token": "123456", "new_password": "Test@123"}

    response = client.post(f"{settings.API_V1_STR}/auth/reset-password", json=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["msg"] == "Password updated successfully"


def test_login_success(client, mock_db):
    """Test successful login."""
    # Mock user query
    mock_user = User(
        id=1,
        email="test@example.com",
        hashed_password=security.get_password_hash("password123"),
        full_name="Test User",
    )
    mock_db.exec.return_value.first.return_value = mock_user

    data = {"username": "test@example.com", "password": "password123"}

    response = client.post(f"{settings.API_V1_STR}/auth/login", data=data)

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_invalid_credentials(client, mock_db):
    """Test login with invalid credentials."""
    # Mock user query to return None (user not found)
    mock_db.exec.return_value.first.return_value = None

    data = {"username": "nonexistent@example.com", "password": "wrongpassword"}

    response = client.post(f"{settings.API_V1_STR}/auth/login", data=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()


def test_register_existing_user(client, mock_db):
    """Test registration with existing email."""
    # Mock existing user
    mock_user = User(
        id=1,
        email="existing@example.com",
        hashed_password=security.get_password_hash("password123"),
        full_name="Existing User",
    )
    mock_db.exec.return_value.first.return_value = mock_user

    data = {
        "email": "existing@example.com",
        "password": "Test@123",
        "full_name": "New User",
    }

    response = client.post(f"{settings.API_V1_STR}/auth/register", json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.json()


def test_register_weak_password(client, mock_db):
    """Test registration with weak password."""
    # Mock database query to return no existing user
    mock_db.exec.return_value.first.return_value = None

    # Test different weak password scenarios
    test_cases = [
        {
            "password": "weak",
            "expected_error": "Password must be at least 8 characters long",
        },
        {
            "password": "weakpassword",
            "expected_error": "Password must contain at least one uppercase letter",
        },
        {
            "password": "WEAKPASSWORD",
            "expected_error": "Password must contain at least one lowercase letter",
        },
        {
            "password": "WeakPassword",
            "expected_error": "Password must contain at least one number",
        },
        {
            "password": "WeakPassword1",
            "expected_error": "Password must contain at least one special character",
        },
    ]

    for test_case in test_cases:
        data = {
            "email": "newuser@example.com",
            "password": test_case["password"],
            "full_name": "New User",
        }

        response = client.post(f"{settings.API_V1_STR}/auth/register", json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert test_case["expected_error"] in response.json()["detail"]


def test_password_recovery_nonexistent_email(client, mock_db):
    """Test password recovery with nonexistent email."""
    # Mock user query to return None
    mock_db.exec.return_value.first.return_value = None

    response = client.post(
        f"{settings.API_V1_STR}/auth/password-recovery/nonexistent@example.com"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in response.json()


def test_reset_password_invalid_token(client, mock_db):
    """Test password reset with invalid token."""
    # Mock token query to return None
    mock_db.exec.return_value.first.return_value = None

    data = {"token": "invalid123", "new_password": "Test@123"}

    response = client.post(f"{settings.API_V1_STR}/auth/reset-password/", json=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in response.json()


def test_reset_password_expired_token(client, mock_db):
    """Test password reset with expired token."""
    # Mock token query with expired token
    mock_token = PasswordResetToken(
        user_id=1,
        token="123456",
        expires_at=datetime.utcnow()
        - timedelta(minutes=1),  # Token expired 1 minute ago
    )
    mock_db.exec.return_value.first.return_value = mock_token

    data = {"token": "123456", "new_password": "weak"}

    response = client.post(f"{settings.API_V1_STR}/auth/reset-password/", json=data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "Password must be at least 8 characters long" in response.json()["detail"]
