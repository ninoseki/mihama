import functools

import aiometer
from fastapi import APIRouter

from mihama import crud, schemas
from mihama.core import settings

router = APIRouter()


async def query(query: schemas.Query) -> schemas.Vulnerabilities:
    vulns = await crud.vulnerability.search_by_query(query)
    return schemas.Vulnerabilities(
        vulns=[schemas.Vulnerability.parse_obj(v) for v in vulns]
    )


async def batch_query(
    queries: schemas.BatchQuery,
    *,
    max_at_once: int = settings.OSV_QUERY_BATCH_MAX_AT_ONCE
) -> schemas.BatchResponse:
    if len(queries.queries) == 0:
        return schemas.BatchResponse(results=[])

    jobs = [functools.partial(query, q) for q in queries.queries]
    results = await aiometer.run_all(jobs, max_at_once=max_at_once)
    return schemas.BatchResponse(results=[r.simplify() for r in results])
