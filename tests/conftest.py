import pytest
from api.app import get_app, lifespan
from httpx import AsyncClient


@pytest.fixture(scope="session")
def anyio_backend():
    """This fixture sets up asyncio as the async backend."""
    return "asyncio"


@pytest.fixture(scope="function")
async def client():
    app = get_app()
    async with lifespan(app):
        async with AsyncClient(app=app, base_url="http://localhost") as client:
            yield client
