import asyncio

import pytest
import pytest_asyncio

from app import crud, models
from app.factories.vulnerability import VulnerabilityFactory
from app.monkeypatch import monkeypatch_escaper
from app.redis import setup_redis_om


@pytest.fixture(scope="session")
def event_loop():
    """Force the pytest-asyncio loop to be the main one."""
    loop = asyncio.new_event_loop()
    yield loop


@pytest.fixture
def vulnerabilities():
    return VulnerabilityFactory.from_directory("tests/fixtures/advisories/")


@pytest_asyncio.fixture
async def setup_redis(vulnerabilities: list[models.Vulnerability]):
    monkeypatch_escaper()

    # setup migrations for using redis-om
    await setup_redis_om()

    # save OSV data for testing
    for v in vulnerabilities:
        v_ = await crud.vulnerability.get_by_id(v.id)

        if v_ is None:
            await crud.vulnerability.save(v)
