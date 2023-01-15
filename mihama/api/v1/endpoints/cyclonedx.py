from fastapi import APIRouter

from mihama import schemas
from mihama.api.v1.query import batch_query

router = APIRouter()


@router.post(
    "/querybatch",
    response_model=schemas.BatchResponse,
    response_model_exclude_none=True,
    description="Query vulnerabilities by CycloneDX SBOM. (Components inside should have package URL to work)",
)
async def querybatch(bom: schemas.CycloneDX) -> schemas.BatchResponse:
    queries = bom.to_batch_query()
    return await batch_query(queries=queries)
