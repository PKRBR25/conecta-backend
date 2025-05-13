"""Authentication schemas."""

from pydantic import BaseModel, Field, field_validator


class PasswordReset(BaseModel):
    """Password reset schema."""

    token: str
    new_password: str = Field(min_length=8, max_length=14)

    @field_validator("new_password")
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
