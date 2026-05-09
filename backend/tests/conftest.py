import asyncio
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.db.session import get_db, AsyncSessionLocal


# pytestのイベントループ固定（CIクラッシュ防止）
@pytest.fixture
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# DB override（これが超重要）
async def override_get_db():
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope="function", autouse=True)
def override_dependencies():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


# テスト用クライアント統一
@pytest.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac