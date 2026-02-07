import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock

from src.main import app
from src.services.task import get_task_service


@pytest.fixture
def mock_task_service():
    return AsyncMock()


@pytest_asyncio.fixture
async def client(mock_task_service) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_task_service] = lambda: mock_task_service

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides = {}
