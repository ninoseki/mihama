import pytest

from mihama import schemas
from mihama.api.v1.query import batch_query


@pytest.fixture
def empty_batch_query():
    return schemas.BatchQuery(queries=[])


@pytest.mark.asyncio
async def test_batch_query_with_empty_queries(empty_batch_query: schemas.BatchQuery):
    res = await batch_query(queries=empty_batch_query)
    assert len(res.results) == 0
