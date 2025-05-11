"""Authentication endpoints."""
import random
from datetime import datetime, timedelta
from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.api import deps
from app.core import security
from app.core.config import settings
from app.db.models import User, PasswordResetToken
from app.schemas.token import Token
from app.services.email import send_email

router = APIRouter()


@router.post("/login/access-token", response_model=Token)
async def login_access_token(
    db: Annotated[Session, Depends(deps.get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Any:
    """OAuth2 compatible token login, get an access token for future requests."""
    user = db.exec(
        select(User).where(User.email == form_data.username)
    ).first()
    
    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/password-recovery/{email}")
async def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
    """Password Recovery."""
    user = db.exec(select(User).where(User.email == email)).first()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    
    # Generate 6-digit code
    reset_code = str(random.randint(100000, 999999))
    token_expires = datetime.utcnow() + timedelta(hours=24)
    
    # Save token to database
    reset_token = PasswordResetToken(
        user_id=user.id,
        token=reset_code,
        expires_at=token_expires,
    )
    db.add(reset_token)
    db.commit()
    
    # Send email with reset code
    await send_email(
        email_to=email,
        subject="Password Recovery",
        template_name="password_reset",
        template_data={
            "code": reset_code,
            "expires": token_expires.strftime("%Y-%m-%d %H:%M UTC"),
        },
        language=user.language,
    )
    
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/")
def reset_password(
    token: str, new_password: str, db: Session = Depends(deps.get_db)
) -> Any:
    """Reset password."""
    reset_token = db.exec(
        select(PasswordResetToken).where(
            PasswordResetToken.token == token,
            PasswordResetToken.used == False,  # noqa: E712
            PasswordResetToken.expires_at > datetime.utcnow(),
        )
    ).first()
    
    if not reset_token:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired password reset token",
        )
    
    user = db.get(User, reset_token.user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    
    # Update password
    user.hashed_password = security.get_password_hash(new_password)
    reset_token.used = True
    db.add(user)
    db.add(reset_token)
    db.commit()
    
    return {"msg": "Password updated successfully"}
