"""User model module."""

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import DateTime


class User(SQLModel, table=True):
    """User model."""

    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    language: str = Field(default="en")
    created_at: datetime = Field(sa_type=DateTime, default_factory=datetime.utcnow)
    updated_at: datetime = Field(sa_type=DateTime, default_factory=datetime.utcnow)


class PasswordResetToken(SQLModel, table=True):
    """Password reset token model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    token: str = Field(unique=True, index=True)
    user_id: int = Field(foreign_key="users.id")
    expires_at: datetime = Field(sa_type=DateTime)
    is_used: bool = Field(default=False)
