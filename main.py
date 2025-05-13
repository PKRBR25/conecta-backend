from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
import random
from typing import Optional

app = FastAPI(title="Conecta API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class VerifyCodeRequest(BaseModel):
    email: EmailStr
    code: str


class SetNewPasswordRequest(BaseModel):
    email: EmailStr
    code: str
    new_password: str


# Temporary storage for verification codes (should be replaced with proper database storage)
verification_codes = {}


@app.post("/api/auth/login")
async def login(request: LoginRequest):
    # TODO: Implement actual authentication logic
    return JSONResponse(status_code=200, content={"message": "Login successful"})


@app.post("/api/auth/request-reset")
async def request_password_reset(request: PasswordResetRequest):
    # Generate 6-digit code
    code = str(random.randint(100000, 999999))
    verification_codes[request.email] = code

    # TODO: Implement email sending logic
    return JSONResponse(
        status_code=200, content={"message": "Reset code sent to email"}
    )


@app.post("/api/auth/verify-code")
async def verify_code(request: VerifyCodeRequest):
    stored_code = verification_codes.get(request.email)
    if not stored_code or stored_code != request.code:
        return JSONResponse(status_code=400, content={"message": "Invalid code"})
    return JSONResponse(
        status_code=200, content={"message": "Code verified successfully"}
    )


@app.post("/api/auth/reset-password")
async def reset_password(request: SetNewPasswordRequest):
    stored_code = verification_codes.get(request.email)
    if not stored_code or stored_code != request.code:
        return JSONResponse(status_code=400, content={"message": "Invalid code"})

    # TODO: Implement password update logic
    verification_codes.pop(request.email, None)  # Clear the used code
    return JSONResponse(
        status_code=200, content={"message": "Password updated successfully"}
    )
