import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.db import Base, get_db
import os


DATABASE_URL = os.getenv("DATABASE_URL")

test_engine = create_async_engine(
    DATABASE_URL,
    future=True,
    pool_pre_ping=True,
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# -------------------------
# DB初期化
# -------------------------
@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# -------------------------
# 重要修正：毎リクエストで新session
# -------------------------
@pytest.fixture
async def client():
    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session   # ←ここ重要（毎回新規）

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()