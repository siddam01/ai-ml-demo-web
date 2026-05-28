from __future__ import annotations

import asyncio
import sys

# psycopg async requires SelectorEventLoop on Windows (not ProactorEventLoop).
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.errors import app_error_handler, validation_error_handler
from app.api.health import router as health_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.middleware.db_logging import DbLoggingMiddleware
from app.middleware.request_logging import RequestLoggingMiddleware
from app.routes.api_v1 import router as api_v1_router
from app.utils.exceptions import AppError
from app.db.session import AsyncSessionLocal
from app.services.logs import LogService


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.LOG_LEVEL)

    app = FastAPI(
        title=settings.APP_NAME,
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        docs_url=f"{settings.API_V1_PREFIX}/docs",
        redoc_url=f"{settings.API_V1_PREFIX}/redoc",
        default_response_class=ORJSONResponse,
    )

    if settings.cors_origin_list:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origin_list,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(DbLoggingMiddleware)

    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)

    app.include_router(health_router, prefix=settings.API_V1_PREFIX)
    app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)

    @app.on_event("startup")
    async def _cleanup_old_logs() -> None:
        # Simple built-in retention: keep last 2 days.
        async with AsyncSessionLocal() as session:
            await LogService(session).cleanup_older_than_days(days=2)

    return app


app = create_app()

