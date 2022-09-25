from fastapi import APIRouter, Query

from app import crud, schemas
from app.query import normalize_package

router = APIRouter()


@router.post(
    "/package",
    response_model=schemas.SearchResults,
    response_model_exclude_none=True,
    description="Search by package",
)
async def search_by_package(
    package: schemas.BasePackage,
    *,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
) -> schemas.SearchResults:
    normalized = normalize_package(package)

    count = await crud.vulnerability.count_by_package(normalized)
    vulns = await crud.vulnerability.search_by_package(
        normalized, limit=limit, offset=offset
    )

    return schemas.SearchResults(vulns=vulns, total=count)
