import os
import asyncio

import pytest
import pytest_asyncio
import httpx
from httpx import ASGITransport


@pytest.fixture(scope="session", autouse=True)
def _set_test_env() -> None:
    # Ensure consistent test runtime config.
    os.environ.setdefault("ENV", "test")
    os.environ.setdefault("JWT_SECRET_KEY", "test-secret")
    # Use local postgres DB created earlier.
    os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/rentflow")


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _dispose_engine_at_end():
    yield
    from app.db.session import engine

    await engine.dispose()


@pytest_asyncio.fixture()
async def client() -> httpx.AsyncClient:
    # Import after env is set.
    from app.main import app

    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
