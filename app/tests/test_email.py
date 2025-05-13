"""Test email functionality."""
import pytest
from unittest.mock import patch, AsyncMock
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.email import send_reset_password_email, send_email
from app.core.config import settings


@pytest.mark.asyncio
async def test_send_reset_password_email(mocker):
    """Test sending reset password email."""
    # Mock SMTP connection and sending
    mock_smtp = AsyncMock()
    mock_smtp.__aenter__.return_value = mock_smtp
    mock_smtp.send_message = AsyncMock()
    
    # Mock template reading
    mock_template = """<div>Your password reset code is: {{ code }}</div>"""
    mock_open = mocker.patch('builtins.open')
    mock_open.return_value.__enter__.return_value.read.return_value = mock_template
    
    with patch("aiosmtplib.SMTP", return_value=mock_smtp):
        await send_reset_password_email(
            email_to="test@example.com",
            token="123456",
        )
        
        # Check if send_message was called
        mock_smtp.send_message.assert_called_once()
        
        # Get the email message that was sent
        message = mock_smtp.send_message.call_args[0][0]
        
        # Check email content
        assert isinstance(message, MIMEMultipart)
        assert message["To"] == "test@example.com"
        assert message["From"] == f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        assert "Password recovery" in message["Subject"]
        
        # Check if token is in the HTML content
        html_part = None
        for part in message.walk():
            if part.get_content_type() == "text/html":
                html_part = part
                break
        
        assert html_part is not None
        assert "123456" in html_part.get_payload()


@pytest.mark.asyncio
async def test_send_reset_password_email_failure(mocker):
    """Test handling of email sending failure."""
    # Mock SMTP to raise an exception
    mock_smtp = AsyncMock()
    mock_smtp.__aenter__.return_value = mock_smtp
    mock_smtp.send_message = AsyncMock(side_effect=Exception("SMTP error"))
    
    # Mock template reading
    mock_template = """<div>Your password reset code is: {{ code }}</div>"""
    mock_open = mocker.patch('builtins.open')
    mock_open.return_value.__enter__.return_value.read.return_value = mock_template
    
    with patch("aiosmtplib.SMTP", return_value=mock_smtp):
        with pytest.raises(Exception) as exc_info:
            await send_reset_password_email(
                email_to="test@example.com",
                token="123456",
            )
        
        assert "SMTP error" in str(exc_info.value)
