import pytest
from elasticsearch import AsyncElasticsearch

from mihama import crud


@pytest.mark.asyncio()
async def test_exists(es: AsyncElasticsearch, docker_compose):
    got = await crud.index.exists(es, index="404_not_found")
    assert got is False
