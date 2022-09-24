from fastapi import APIRouter

from app import schemas

from .utils import batch_query

router = APIRouter()


@router.post(
    "/querybatch",
    response_model=schemas.BatchResponse,
    response_model_exclude_none=True,
    description="Query vulnerabilities by CycloneDX SBOM. (Components inside should have package URL to work) ",
)
async def querybatch(bom: schemas.BOM) -> schemas.BatchResponse:
    queries = bom.to_batch_query()
    return await batch_query(queries=queries)
