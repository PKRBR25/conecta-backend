"""User schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    """Shared properties."""

    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    language: Optional[str] = "en"


class UserCreate(UserBase):
    """Properties to receive via API on creation."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=14)
    full_name: str

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if len(v) > 14:
            raise ValueError("Password must not be longer than 14 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v):
            raise ValueError("Password must contain at least one special character")
        return v


class UserUpdate(UserBase):
    """Properties to receive via API on update."""

    password: Optional[str] = None


class UserInDBBase(UserBase):
    """Properties shared by models stored in DB."""

    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class UserResponse(UserInDBBase):
    """Properties to return via API."""

    class Config:
        """Pydantic config."""

        from_attributes = True


class User(UserInDBBase):
    """Additional properties to return via API."""


class UserInDB(UserInDBBase):
    """Additional properties stored in DB."""

    hashed_password: str
