"""User schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Shared properties."""

    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    language: Optional[str] = "en"


class UserCreate(UserBase):
    """Properties to receive via API on creation."""

    email: EmailStr
    password: str


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


class User(UserInDBBase):
    """Additional properties to return via API."""

    pass


class UserInDB(UserInDBBase):
    """Additional properties stored in DB."""

    hashed_password: str
