import functools

import aiometer
from fastapi import APIRouter

from app import crud, schemas
from app.cache import cache
from app.core import settings

router = APIRouter()


@cache()
async def cached_query(query: schemas.Query) -> schemas.Vulnerabilities:
    vulns = await crud.vulnerability.search_by_query(query)
    return schemas.Vulnerabilities(vulns=vulns)


async def batch_query(
    queries: schemas.BatchQuery,
    *,
    max_at_once: int = settings.OSV_QUERY_BATCH_MAX_AT_ONCE
):
    if len(queries.queries) == 0:
        return schemas.BatchResponse(results=[])

    jobs = [functools.partial(cached_query, q) for q in queries.queries]
    results = await aiometer.run_all(jobs, max_at_once=max_at_once)
    return schemas.BatchResponse(results=results)
