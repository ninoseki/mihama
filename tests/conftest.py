import asyncio

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from httpx import AsyncClient

from app import crud, models
from app.factories.vulnerability import VulnerabilityFactory
from app.main import create_app
from app.redis import setup_redis_om


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def vulnerabilities():
    return VulnerabilityFactory.from_directory("tests/fixtures/advisories/")


@pytest_asyncio.fixture
async def setup_redis(vulnerabilities: list[models.Vulnerability]):
    # setup migrations for using redis-om
    await setup_redis_om()

    # save OSV data for testing
    for v in vulnerabilities:
        v_ = await crud.vulnerability.get_by_id(v.id)

        if v_ is None:
            await crud.vulnerability.save(v)


@pytest.fixture
def setup_fastapi_cache():
    FastAPICache.init(InMemoryBackend())


@pytest.fixture
def app(setup_redis, setup_fastapi_cache):
    app = create_app(add_event_handlers=False)
    yield app


@pytest_asyncio.fixture
async def client(app: FastAPI):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
