import pytest
from httpx import AsyncClient

from mihama import schemas


@pytest.fixture
def bom():
    with open("tests/fixtures/cyclonedx/example.json") as f:
        return schemas.CycloneDX.model_validate_json(f.read())


@pytest.mark.asyncio
@pytest.mark.usefixtures("_setup_vulns")
async def test_cyclonedx(client: AsyncClient, bom: schemas.CycloneDX):
    res = await client.post("/v1/cyclonedx/querybatch", json=bom.model_dump())
    results = res.json().get("results", [])
    assert len(results) > 0
