from fastapi import APIRouter

from mihama import crud, deps, schemas

router = APIRouter()


@router.post(
    "/querybatch",
    response_model_exclude_none=True,
    description="Query vulnerabilities by SPDX SBOM. (Packages inside should have package URL to work)",
)
async def querybatch(
    bom: schemas.SPDX, *, es: deps.Elasticsearch
) -> schemas.BatchResponse:
    return await crud.vulnerability.querybatch(es, queries=bom.to_queries())
