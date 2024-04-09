from functools import partial

import aiometer
from fastapi import APIRouter

from mihama import crud, deps, schemas, settings

router = APIRouter()


@router.get(
    "/",
    response_model_exclude_none=True,
)
async def search(es: deps.Elasticsearch) -> schemas.Ecosystems:
    # TODO: use multi-search?
    tasks = [
        partial(crud.vulnerability.count, es, ecosystem=ecosystem)
        for ecosystem in settings.OSV_ECOSYSTEMS
    ]
    results = await aiometer.run_all(tasks)
    ecosystems_results = zip(settings.OSV_ECOSYSTEMS, results, strict=True)
    ecosystems = [
        schemas.Ecosystem(name=name, total=total) for name, total in ecosystems_results
    ]
    return schemas.Ecosystems(ecosystems=ecosystems, total=sum(results))
