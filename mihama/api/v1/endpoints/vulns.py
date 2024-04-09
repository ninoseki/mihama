from elasticsearch import NotFoundError
from fastapi import APIRouter, HTTPException

from mihama import crud, deps, schemas

router = APIRouter()


@router.get(
    "/",
    response_model_exclude_none=True,
)
async def search(
    ecosystem: str | None = None,
    q: str | None = None,
    search_after: list[int] | None = None,
    *,
    es: deps.Elasticsearch,
) -> schemas.SearchResults:
    count = await crud.vulnerability.count(
        es, ecosystem=ecosystem, id_or_package_name=q
    )
    vulns = await crud.vulnerability.search(
        es, ecosystem=ecosystem, id_or_package_name=q, search_after=search_after
    )
    return schemas.SearchResults(vulns=vulns, total=count)


@router.get(
    "/{id}",
    response_model_exclude_none=True,
    description="Return a `Vulnerability` object for a given OSV ID.",
)
async def get_by_id(id: str, *, es: deps.Elasticsearch) -> schemas.Vulnerability:
    try:
        v = await crud.vulnerability.get(es, id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail="Vulnerability not found") from e

    return v
