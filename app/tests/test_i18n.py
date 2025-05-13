"""Test internationalization."""
import pytest
from unittest.mock import MagicMock, patch
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
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


def test_error_messages_en(client, mock_db):
    """Test error messages in English."""
    # Set Accept-Language header to English
    headers = {"Accept-Language": "en"}

    # Test invalid login
    mock_db.exec.return_value.first.return_value = None
    data = {"username": "nonexistent@example.com", "password": "wrongpassword"}

    response = client.post(
        f"{settings.API_V1_STR}/auth/login", data=data, headers=headers
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect email or password"

    # Test weak password registration
    data = {
        "email": "newuser@example.com",
        "password": "weak",
        "full_name": "New User",
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/register", json=data, headers=headers
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "Password must be at least" in response.json()["detail"]


def test_error_messages_pt_br(client, mock_db):
    """Test error messages in Portuguese."""
    # Set Accept-Language header to Portuguese
    headers = {"Accept-Language": "pt-br"}

    # Test invalid login
    mock_db.exec.return_value.first.return_value = None
    data = {"username": "nonexistent@example.com", "password": "wrongpassword"}

    response = client.post(
        f"{settings.API_V1_STR}/auth/login", data=data, headers=headers
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Email ou senha incorretos"

    # Test weak password registration
    data = {
        "email": "newuser@example.com",
        "password": "weak",
        "full_name": "New User",
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/register", json=data, headers=headers
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "A senha deve ter pelo menos" in response.json()["detail"]


def test_success_messages_en(client, mock_db):
    """Test success messages in English."""
    # Set Accept-Language header to English
    headers = {"Accept-Language": "en"}

    # Test password recovery
    # Mock user query
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.email = "test@example.com"
    mock_db.exec.return_value.first.return_value = mock_user

    # Mock token creation
    mock_token = MagicMock()
    mock_token.token = "123456"
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = mock_token

    with patch("app.core.email.send_reset_password_email") as mock_send_email:
        mock_send_email.return_value = None  # This is needed for async functions
        response = client.post(
            f"{settings.API_V1_STR}/auth/password-recovery/test@example.com",
            headers=headers,
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["msg"] == "Password recovery email sent"
        assert mock_send_email.call_count == 1


def test_success_messages_pt_br(client, mock_db):
    """Test success messages in Portuguese."""
    # Set Accept-Language header to Portuguese
    headers = {"Accept-Language": "pt-br"}

    # Test password recovery
    # Mock user query
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.email = "test@example.com"
    mock_db.exec.return_value.first.return_value = mock_user

    # Mock token creation
    mock_token = MagicMock()
    mock_token.token = "123456"
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = mock_token

    with patch("app.core.email.send_reset_password_email") as mock_send_email:
        mock_send_email.return_value = None  # This is needed for async functions
        response = client.post(
            f"{settings.API_V1_STR}/auth/password-recovery/test@example.com",
            headers=headers,
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["msg"] == "Email de recuperação de senha enviado"
        assert mock_send_email.call_count == 1
