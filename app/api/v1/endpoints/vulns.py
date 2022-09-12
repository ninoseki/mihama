from fastapi import APIRouter, HTTPException

from app import crud, models

router = APIRouter()


@router.get(
    "/{id}",
    response_model=models.Vulnerability,
    response_model_exclude_none=True,
    description="Return a `Vulnerability` object for a given OSV ID.",
)
async def get_by_id(id: str) -> models.Vulnerability:
    v = await crud.vulnerability.get_by_id(id)

    if v is None:
        raise HTTPException(status_code=404, detail="Vulnerability not found")

    return v
