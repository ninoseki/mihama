from fastapi import APIRouter

from app import schemas

from .utils import batch_query, cached_query

router = APIRouter()


@router.post(
    "/query",
    response_model=schemas.Vulnerabilities,
    response_model_exclude_none=True,
    description="Query vulnerabilities for a particular project at a given commit or version. ",
)
async def query(query: schemas.Query) -> schemas.Vulnerabilities:
    return await cached_query(query)


@router.post(
    "/querybatch",
    response_model=schemas.BatchResponse,
    response_model_exclude_none=True,
    description="Query vulnerabilities (batched) for given package versions and commits. This currently allows a maximum of 1000 package versions to be included in a single query.",
)
async def querybatch(queries: schemas.BatchQuery) -> schemas.BatchResponse:
    return await batch_query(queries)
