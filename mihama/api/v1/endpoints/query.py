from fastapi import APIRouter

from mihama import schemas
from mihama.api.v1.query import batch_query
from mihama.api.v1.query import query as _query

router = APIRouter()


@router.post(
    "/query",
    response_model=schemas.Vulnerabilities,
    response_model_exclude_none=True,
    description="Query vulnerabilities for a particular project at a given commit or version.",
)
async def query(query: schemas.Query) -> schemas.Vulnerabilities:
    return await _query(query)


@router.post(
    "/querybatch",
    response_model=schemas.BatchResponse,
    response_model_exclude_none=True,
    description="Query vulnerabilities (batched) for given package versions and commits. This currently allows a maximum of 1000 package versions to be included in a single query.",
)
async def querybatch(queries: schemas.BatchQuery) -> schemas.BatchResponse:
    return await batch_query(queries)
