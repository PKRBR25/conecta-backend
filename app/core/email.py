"""Email configuration."""
import logging
from pathlib import Path
from typing import Any, Dict, Optional

import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from pydantic import EmailStr

from app.core.config import settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def send_email(
    email_to: EmailStr,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    """Send email."""
    try:
        logger.debug(f"Creating email message with subject: {subject_template}")
        logger.debug(f"Environment: {environment}")

        # Render templates
        logger.debug("Rendering subject template")
        subject = Template(subject_template).render(**environment)
        logger.debug(f"Subject after rendering: {subject}")

        logger.debug("Rendering HTML template")
        logger.debug(f"HTML template content: {html_template}")
        html_content = Template(html_template).render(**environment)
        logger.debug(f"HTML content after rendering: {html_content}")

        # Create message
        message = MIMEMultipart()
        message["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        message["To"] = email_to
        message["Subject"] = subject

        logger.debug(f"From: {message['From']}")
        logger.debug(f"To: {message['To']}")
        logger.debug(f"Subject: {message['Subject']}")

        # Add HTML content
        message.attach(MIMEText(html_content, "html"))

        logger.debug("Setting up SMTP connection")
        logger.debug(
            f"SMTP settings: host={settings.SMTP_HOST}, port={settings.SMTP_PORT}, tls={settings.SMTP_TLS}, user={settings.SMTP_USER}"
        )

        # Usar SSL
        try:
            import ssl

            logger.debug("Creating SMTP connection...")
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            smtp = aiosmtplib.SMTP(
                hostname=settings.SMTP_HOST,
                port=465,  # Porta SSL
                username=settings.SMTP_USER,
                password=settings.SMTP_PASSWORD,
                tls_context=context,
                use_tls=True,
            )
            logger.debug("SMTP object created, connecting...")
            await smtp.connect()
            logger.debug("SMTP connection established")
            logger.debug("Sending email...")
            await smtp.send_message(message)
            logger.debug("Email sent through SMTP")
        except Exception as smtp_error:
            logger.error(f"SMTP Error: {type(smtp_error).__name__}")
            logger.error(f"SMTP Error details: {str(smtp_error)}")
            raise
        finally:
            try:
                await smtp.quit()
            except Exception as quit_error:
                logger.error(f"Error during SMTP quit: {str(quit_error)}")
                # Don't raise this error as the email might have been sent successfully

        logger.info(f"Email sent successfully to {email_to}")
    except Exception as e:
        logger.error(f"Error sending email to {email_to}: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error details: {str(e)}")
        raise


async def send_test_email(email_to: EmailStr) -> None:
    """Send test email."""
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    await send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


async def send_reset_password_email(email_to: EmailStr, token: str) -> None:
    """Send reset password email."""
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    await send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email_to,
            "code": token,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
        },
    )
