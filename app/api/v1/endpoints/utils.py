"""Utils endpoints."""
from typing import Any

from fastapi import APIRouter, HTTPException, Body
from pydantic import EmailStr

from app.core.email import send_test_email

router = APIRouter()


@router.post("/test-email/{email}")
async def test_email(email: EmailStr,) -> Any:
    """Test email."""
    try:
        await send_test_email(email_to=email)
        return {"msg": "Test email sent"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error sending test email: {str(e)}"
        )
