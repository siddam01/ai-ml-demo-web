from __future__ import annotations

import time
import uuid
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.db.session import AsyncSessionLocal
from app.models.app_log import AppLog


class DbLoggingMiddleware(BaseHTTPMiddleware):
    """
    Persists request logs to Postgres (app_logs).
    Designed to never break the request even if logging fails.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start = time.perf_counter()
        request_id = request.headers.get("x-request-id") or uuid.uuid4().hex

        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        except Exception:
            status_code = 500
            raise
        finally:
            duration_ms = int((time.perf_counter() - start) * 1000.0)
            try:
                async with AsyncSessionLocal() as session:
                    await _write_log(
                        session,
                        level="info" if status_code < 500 else "error",
                        message="http_request",
                        method=request.method,
                        path=str(request.url.path),
                        status_code=status_code,
                        duration_ms=duration_ms,
                        request_id=request_id,
                        extra={
                            "query": dict(request.query_params),
                            "client": request.client.host if request.client else None,
                        },
                    )
                    await session.commit()
            except Exception:
                # Never fail the request due to logging
                pass


async def _write_log(
    session: AsyncSession,
    *,
    level: str,
    message: str,
    method: str | None,
    path: str | None,
    status_code: int | None,
    duration_ms: int | None,
    request_id: str | None,
    owner_id=None,
    extra: dict | None,
) -> None:
    row = AppLog(
        level=level,
        message=message,
        method=method,
        path=path,
        status_code=status_code,
        duration_ms=duration_ms,
        request_id=request_id,
        owner_id=owner_id,
        extra=extra,
    )
    session.add(row)

