"""Authentication endpoints."""

import logging
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.core.limiter import limiter
from app import schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.db.models.user import User, PasswordResetToken
from app.schemas.auth import PasswordReset
from app.schemas.token import Token
from app.schemas.user import UserCreate
from app.core.email import send_reset_password_email
from app.core.i18n import get_message

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register(
    request: Request, db: Annotated[Session, Depends(deps.get_db)], user_in: UserCreate,
) -> Any:
    """Register a new user."""
    try:
        logger.debug(f"Attempting to register user with email: {user_in.email}")

        # Check if user already exists
        user = db.exec(select(User).where(User.email == user_in.email)).first()

        if user:
            logger.debug(f"User with email {user_in.email} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=get_message(request.state.language, "email_exists", "auth"),
            )

        logger.debug("Creating new user")
        # Create new user
        user = User(
            email=user_in.email,
            hashed_password=security.get_password_hash(user_in.password),
            full_name=user_in.full_name,
            language="en",  # Default to English
            is_active=True,
            is_superuser=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        logger.debug("Adding user to database")
        db.add(user)
        db.commit()
        db.refresh(user)

        logger.debug("Generating access token")
        # Generate access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        token = {
            "access_token": security.create_access_token(
                user.id, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }

        logger.debug("Registration successful")
        return token
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        raise


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login_access_token(
    request: Request,
    db: Annotated[Session, Depends(deps.get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Any:
    """OAuth2 compatible token login, get an access token for future requests."""
    user = db.exec(select(User).where(User.email == form_data.username)).first()

    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=get_message(request.state.language, "invalid_credentials", "auth"),
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=get_message(request.state.language, "inactive_user", "auth"),
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/password-recovery/{email}", status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")
async def recover_password(
    request: Request, email: str, db: Annotated[Session, Depends(deps.get_db)],
) -> Any:
    """Password Recovery."""
    try:
        logger.debug(f"Attempting password recovery for email: {email}")
        user = db.exec(select(User).where(User.email == email)).first()

        if not user:
            logger.debug(f"User not found: {email}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=get_message(request.state.language, "user_not_found", "auth"),
            )

        logger.debug("Generating reset code")
        # Generate 6-digit code
        reset_code = str(random.randint(100000, 999999))
        token_expires = datetime.utcnow() + timedelta(hours=24)

        logger.debug("Creating reset token")
        # Save token to database
        reset_token = PasswordResetToken(
            user_id=user.id, token=reset_code, expires_at=token_expires,
        )
        db.add(reset_token)
        db.commit()
        logger.debug("Reset token saved to database")

        logger.debug("Sending email")
        try:
            await send_reset_password_email(
                email_to=email, token=reset_code,
            )
            logger.debug("Email sent successfully")
        except Exception as email_error:
            logger.error(f"Error sending email: {type(email_error).__name__}")
            logger.error(f"Error details: {str(email_error)}")
            logger.error(f"Error args: {email_error.args}")
            # Delete the token if email fails
            db.delete(reset_token)
            db.commit()
            raise HTTPException(
                status_code=500,
                detail=get_message(request.state.language, "email_send_error", "auth"),
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in password recovery: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=get_message(
                request.state.language, "password_recovery_error", "auth"
            ),
        )


@router.post("/reset-password", status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")
async def reset_password(
    request: Request,
    password_reset: PasswordReset,
    db: Annotated[Session, Depends(deps.get_db)],
) -> Any:
    """Reset password."""
    try:
        logger.debug(f"Attempting to reset password with token: {password_reset.token}")
        stmt = select(PasswordResetToken).where(
            PasswordResetToken.token == password_reset.token,
            PasswordResetToken.is_used == False,  # noqa: E712
            PasswordResetToken.expires_at > datetime.utcnow(),
        )
        logger.debug(f"SQL Query: {stmt}")
        reset_token = db.exec(stmt).first()

        if not reset_token:
            logger.debug("Token not found or expired")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=get_message(request.state.language, "invalid_token", "auth"),
            )

        logger.debug(f"Found valid token for user_id: {reset_token.user_id}")
        user = db.get(User, reset_token.user_id)
        if not user:
            logger.debug("User not found")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=get_message(request.state.language, "email_exists", "auth"),
            )

        logger.debug("Updating password...")
        # Update password
        user.hashed_password = security.get_password_hash(password_reset.new_password)
        reset_token.is_used = True
        db.add(user)
        db.add(reset_token)
        db.commit()
        logger.debug("Password updated successfully")

        return {"msg": "Password updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resetting password: {type(e).__name__}")
        logger.error(f"Error details: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error resetting password: {str(e)}"
        )

    return {"msg": "Password updated successfully"}
