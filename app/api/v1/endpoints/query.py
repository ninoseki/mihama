import functools

import aiometer
from fastapi import APIRouter

from app import crud, schemas
from app.cache import cache

router = APIRouter()


@cache()
async def cached_query(query: schemas.Query) -> schemas.Vulnerabilities:
    vulns = await crud.vulnerability.search_by_query(query)
    return schemas.Vulnerabilities(vulns=vulns)


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
    jobs = [functools.partial(cached_query, q) for q in queries.queries]
    results = await aiometer.run_all(jobs, max_at_once=100)
    return schemas.BatchResponse(results=results)
