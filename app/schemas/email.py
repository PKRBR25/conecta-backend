"""Email schemas."""
from pydantic import BaseModel, EmailStr


class EmailTest(BaseModel):
    """Email test schema."""

    email: EmailStr
