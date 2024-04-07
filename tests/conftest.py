import os
from contextlib import asynccontextmanager

import ci
import httpx
import pytest
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from pytest_docker.plugin import Services
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

from mihama import crud, deps, schemas
from mihama.factories.vulnerability import VulnerabilityFactory
from mihama.main import create_app

config = Config()

ES_HOSTS: CommaSeparatedStrings = config(
    "ES_HOSTS", cast=CommaSeparatedStrings, default="http://localhost:9200"
)
ES_PASSWORD: Secret = config("ES_PASSWORD", cast=Secret, default="changeme")


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(str(pytestconfig.rootdir), "test.docker-compose.yml")


if ci.is_ci():

    @pytest.fixture(scope="session")
    def docker_compose():  # type: ignore # noqa: PT004
        return
else:

    @pytest.fixture(scope="session")
    def docker_compose(  # type; ignore # noqa: PT004
        docker_services: Services,
    ):  # type: ignore
        def ping():
            try:
                httpx.get(ES_HOSTS[0])
                return True
            except Exception:
                return False

        docker_services.wait_until_responsive(
            timeout=30.0, pause=0.1, check=lambda: ping()
        )


@asynccontextmanager
async def get_es():
    es = AsyncElasticsearch(
        hosts=list(ES_HOSTS),
        basic_auth=("elastic", str(ES_PASSWORD)),
    )
    yield es
    await es.close()


@pytest.fixture()
async def es():
    async with get_es() as es:
        yield es


@pytest.fixture(scope="session")
def vulns():
    return VulnerabilityFactory.from_directory("tests/fixtures/advisories/")


@pytest.fixture(scope="session")
async def _setup_vulns(vulns: list[schemas.Vulnerability], docker_compose):
    async with get_es() as es:
        await crud.vulnerability.bulk_index(es, vulns, refresh=True)


@pytest.fixture()
def app(_setup_vulns, es: AsyncElasticsearch, docker_compose):
    app = create_app(set_lifespan=False)
    app.dependency_overrides[deps.get_es] = lambda: es
    return app


@pytest.fixture()
async def client(app: FastAPI):
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),  # type: ignore
        base_url="http://test",
    ) as client:
        yield client
