import functools
from datetime import datetime

import aiometer
from fastapi import APIRouter

from app import crud, models, schemas
from app.cache import cache
from app.core import settings

router = APIRouter()


def sort_by_modified(vulns: list[models.Vulnerability]) -> list[models.Vulnerability]:
    def to_float(dt: datetime | None) -> float:
        if dt is None:
            return -1.0

        return dt.timestamp()

    vulns.sort(key=lambda v: to_float(v.modified), reverse=True)
    return vulns


@cache()
async def cached_query(query: schemas.Query) -> schemas.Vulnerabilities:
    vulns = await crud.vulnerability.search_by_query(query)

    # NOTE: redis-om v0.27.0 does not support sortable field yet
    #       so we have to sort vulns manually
    vulns = sort_by_modified(vulns)

    return schemas.Vulnerabilities(vulns=vulns)


async def batch_query(
    queries: schemas.BatchQuery,
    *,
    max_at_once: int = settings.OSV_QUERY_BATCH_MAX_AT_ONCE
):
    jobs = [functools.partial(cached_query, q) for q in queries.queries]
    results = await aiometer.run_all(jobs, max_at_once=max_at_once)
    return schemas.BatchResponse(results=results)
