import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.db import Base, get_db


# -----------------------
# テスト専用DB
# -----------------------
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

test_engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=False,
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# -----------------------
# DB初期化
# -----------------------
@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# -----------------------
# DBセッション
# -----------------------
@pytest.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session


# -----------------------
# FastAPI client
# -----------------------
@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()