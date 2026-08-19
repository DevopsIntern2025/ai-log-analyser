from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.ai_exceptions import (
    AIConnectionError,
    AITimeoutError,
    AIRateLimitError,
    AIProviderError,
    AIResponseError,
)


async def ai_connection_error_handler(
    request: Request,
    exc: AIConnectionError,
):
    return JSONResponse(
        status_code=503,
        content={
            "error": "AI_SERVICE_UNAVAILABLE",
            "message": str(exc),
        },
    )


async def ai_timeout_error_handler(
    request: Request,
    exc: AITimeoutError,
):
    return JSONResponse(
        status_code=504,
        content={
            "error": "AI_SERVICE_TIMEOUT",
            "message": str(exc),
        },
    )


async def ai_rate_limit_error_handler(
    request: Request,
    exc: AIRateLimitError,
):
    return JSONResponse(
        status_code=429,
        content={
            "error": "AI_RATE_LIMITED",
            "message": str(exc),
        },
    )


async def ai_provider_error_handler(
    request: Request,
    exc: AIProviderError,
):
    return JSONResponse(
        status_code=502,
        content={
            "error": "AI_PROVIDER_ERROR",
            "message": str(exc),
        },
    )


async def ai_response_error_handler(
    request: Request,
    exc: AIResponseError,
):
    return JSONResponse(
        status_code=502,
        content={
            "error": "AI_INVALID_RESPONSE",
            "message": str(exc),
        },
    )