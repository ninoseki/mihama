import pytest
from httpx import AsyncClient

from mihama import schemas


@pytest.fixture
def bom():
    return schemas.CycloneDX.parse_file("tests/fixtures/cyclonedx/example.json")


@pytest.mark.asyncio
async def test_cyclonedx(client: AsyncClient, bom: schemas.CycloneDX):
    res = await client.post("/v1/cyclonedx/querybatch", json=bom.dict())
    assert res.status_code == 200

    results = res.json().get("results", [])
    assert len(results) > 0
