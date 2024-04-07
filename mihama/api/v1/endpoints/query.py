from fastapi import APIRouter

from mihama import crud, deps, schemas

router = APIRouter()


@router.post(
    "/query",
    response_model_exclude_none=True,
    description="Query vulnerabilities for a particular project at a given commit or version.",
)
async def query(
    query: schemas.Query, *, es: deps.Elasticsearch
) -> schemas.Vulnerabilities:
    return await crud.vulnerability.query(es, query)


@router.post(
    "/querybatch",
    response_model_exclude_none=True,
    description="Query vulnerabilities (batched) for given package versions and commits. This currently allows a maximum of 1000 package versions to be included in a single query.",
)
async def querybatch(
    queries: schemas.BatchQuery, *, es: deps.Elasticsearch
) -> schemas.BatchResponse:
    return await crud.vulnerability.querybatch(es, queries)
