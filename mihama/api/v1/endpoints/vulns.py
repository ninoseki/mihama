from elasticsearch import NotFoundError
from fastapi import APIRouter, HTTPException

from mihama import crud, deps, schemas

router = APIRouter()


@router.post(
    "/",
    response_model_exclude_none=True,
)
async def search(
    query: schemas.SearchQuery,
    *,
    es: deps.Elasticsearch,
) -> schemas.SearchResults:
    count = await crud.vulnerability.count(
        es, ecosystem=query.ecosystem, id_or_package_name=query.q
    )
    vulns = await crud.vulnerability.search(
        es,
        ecosystem=query.ecosystem,
        id_or_package_name=query.q,
        search_after=query.search_after,
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
