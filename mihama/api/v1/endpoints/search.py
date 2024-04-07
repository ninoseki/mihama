from fastapi import APIRouter

from mihama import crud, deps, schemas
from mihama.query import normalize_package

router = APIRouter()


@router.post(
    "/package",
    response_model_exclude_none=True,
    description="Search by package",
)
async def search_by_package(
    query: schemas.SearchQuery,
    size: int = 1000,
    *,
    es: deps.Elasticsearch,
) -> schemas.SearchResults:
    normalized = normalize_package(query.package)

    count = await crud.vulnerability.count_by_package(es, normalized)
    vulns = await crud.vulnerability.search_by_package(es, normalized, size=size)
    return schemas.SearchResults(vulns=vulns, total=count)
