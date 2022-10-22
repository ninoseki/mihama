import pytest
from httpx import AsyncClient

from app import schemas


@pytest.fixture
def bom():
    return schemas.SPDX.parse_file("tests/fixtures/spdx/example.json")


@pytest.mark.asyncio
async def test_spdx(client: AsyncClient, bom: schemas.SPDX):
    res = await client.post("/v1/spdx/querybatch", json=bom.dict())
    assert res.status_code == 200

    results = res.json().get("results", [])
    assert len(results) > 0
