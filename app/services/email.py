"""Email service module."""
import logging
from typing import Any, Dict

import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core.config import settings

logger = logging.getLogger(__name__)


async def send_email(
    email_to: str,
    subject: str,
    template_name: str,
    template_data: Dict[str, Any],
    language: str = "en",
) -> None:
    """Send an email."""
    if not settings.SMTP_HOST or not settings.SMTP_PORT:
        logger.warning("No SMTP host or port configured")
        return

    message = MIMEMultipart()
    message["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
    message["To"] = email_to
    message["Subject"] = subject

    # TODO: Implement template rendering with Jinja2
    # For now, we'll just use a simple text format
    body = f"Subject: {subject}\n\n"
    for key, value in template_data.items():
        body += f"{key}: {value}\n"

    message.attach(MIMEText(body, "plain"))

    try:
        async with aiosmtplib.SMTP(
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            use_tls=settings.SMTP_TLS,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
        ) as smtp:
            await smtp.send_message(message)
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise
