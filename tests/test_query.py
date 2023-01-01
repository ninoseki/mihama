import pytest

from mihama import schemas
from mihama.query import batch_query, normalize_query


@pytest.fixture
def query_with_package_with_purl_without_version():
    return schemas.Query(
        version=None, package=schemas.Package(purl="pkg:npm/jsrsasign")
    )


def test_normalize_query_with_purl_without_version(
    query_with_package_with_purl_without_version: schemas.Query,
):
    normalized = normalize_query(query_with_package_with_purl_without_version)
    assert normalized.version is None


@pytest.fixture
def query_with_package_with_purl_with_version():
    return schemas.Query(
        version=None, package=schemas.Package(purl="pkg:npm/jsrsasign@0.1.0")
    )


def test_normalize_query_with_purl_with_version(
    query_with_package_with_purl_with_version: schemas.Query,
):
    normalized = normalize_query(query_with_package_with_purl_with_version)
    assert normalized.version is not None


@pytest.fixture
def empty_batch_query():
    return schemas.BatchQuery(queries=[])


@pytest.mark.asyncio
async def test_batch_query_with_empty_queries(empty_batch_query: schemas.BatchQuery):
    res = await batch_query(queries=empty_batch_query)
    assert len(res.results) == 0
