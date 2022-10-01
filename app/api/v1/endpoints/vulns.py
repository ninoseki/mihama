from fastapi import APIRouter, HTTPException

from app import crud, schemas

router = APIRouter()


@router.get(
    "/{id}",
    response_model=schemas.Vulnerability,
    response_model_exclude_none=True,
    description="Return a `Vulnerability` object for a given OSV ID.",
)
async def get_by_id(id: str) -> schemas.Vulnerability:
    v = await crud.vulnerability.get_by_id(id)

    if v is None:
        raise HTTPException(status_code=404, detail="Vulnerability not found")

    return schemas.Vulnerability.parse_obj(v)
