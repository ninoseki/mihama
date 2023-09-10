import asyncio
import os

import ci
import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from pytest_docker.plugin import Services

from mihama import crud, models
from mihama.core import settings
from mihama.core.datastructures import DatabaseURL
from mihama.factories.vulnerability import VulnerabilityFactory
from mihama.main import create_app
from mihama.redis import setup_redis_om

from .utils import is_responsive


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(str(pytestconfig.rootdir), "test.docker-compose.yml")


if not ci.is_ci():

    @pytest.fixture(scope="session", autouse=True)
    def docker_compose(docker_ip: str, docker_services: Services):  # type: ignore
        port = docker_services.port_for("redis", 8001)
        url = f"http://{docker_ip}:{port}"
        docker_services.wait_until_responsive(
            timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
        )
        return url

else:

    @pytest.fixture
    def docker_compose():
        return


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def vulnerabilities():
    return VulnerabilityFactory.from_directory("tests/fixtures/advisories/")


def check_redis_host(redis_url: DatabaseURL = settings.REDIS_OM_URL):
    if redis_url.hostname in ["127.0.0.1", "localhost", "0.0.0.0"]:
        return True

    raise Exception("You should not run tests with non-local Redis!")


@pytest_asyncio.fixture
async def setup_redis(vulnerabilities: list[models.Vulnerability]):
    check_redis_host()
    # setup migrations for using redis-om
    await setup_redis_om()

    # save OSV data for testing
    for v in vulnerabilities:
        v_ = await crud.vulnerability.get_by_id(v.id)

        if v_ is None:
            await crud.vulnerability.save(v)


@pytest.fixture
def app(setup_redis):
    app = create_app(add_event_handlers=False)
    yield app


@pytest_asyncio.fixture
async def client(app: FastAPI):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
