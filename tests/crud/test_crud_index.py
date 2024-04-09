import pytest
from elasticsearch import AsyncElasticsearch

from mihama import crud


@pytest.mark.asyncio()
@pytest.mark.usefixtures("docker_compose")
async def test_exists(es: AsyncElasticsearch):
    got = await crud.index.exists(es, index="404_not_found")
    assert got is False
