import httpx
import pytest_asyncio
from fastapi import FastAPI


@pytest_asyncio.fixture
async def app() -> FastAPI:
    from app.run import app
    return app


@pytest_asyncio.fixture
async def client(app):
    async with httpx.AsyncClient(
            app=app,
            base_url="http://testserver",
    ) as client:
        yield client
