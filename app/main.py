"""Main application module."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from sqlmodel import SQLModel
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import engine

# Create database tables
SQLModel.metadata.create_all(engine)

from app.core.limiter import limiter

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=True
)

# Configure rate limiter
app.state.limiter = limiter
app.state.limiter_enabled = True

# Add middlewares
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Add exception handlers
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429, content={"detail": f"Rate limit exceeded: {exc.detail}"}
    )


# Add exception handlers
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": str(exc), "detail": f"Rate limit exceeded: {exc.detail}"},
    )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # Get language from header or use default
    language = request.headers.get("accept-language", settings.DEFAULT_LANGUAGE)
    request.state.language = language.lower()

    response = await call_next(request)
    return response


# Set CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)
