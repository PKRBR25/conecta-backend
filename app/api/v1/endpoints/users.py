"""User endpoints."""
from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api import deps
from app.db.models.user import User
from app.schemas.user import UserResponse

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/me", response_model=UserResponse)
@limiter.limit("5/minute")
def read_user_me(
    request: Request,
    current_user: Annotated[User, Depends(deps.get_current_user)]
) -> Any:
    """Get current user."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
