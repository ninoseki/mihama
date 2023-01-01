from fastapi import APIRouter

from mihama import schemas
from mihama.query import batch_query

router = APIRouter()


@router.post(
    "/querybatch",
    response_model=schemas.BatchResponse,
    response_model_exclude_none=True,
    description="Query vulnerabilities by SPDX SBOM. (Packages inside should have package URL to work)",
)
async def querybatch(bom: schemas.SPDX) -> schemas.BatchResponse:
    queries = bom.to_batch_query()
    return await batch_query(queries=queries)
