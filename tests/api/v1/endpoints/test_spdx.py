import pytest
from httpx import AsyncClient

from mihama import schemas


@pytest.fixture
def bom():
    with open("tests/fixtures/spdx/example.json") as f:
        return schemas.SPDX.model_validate_json(f.read())


@pytest.mark.asyncio
@pytest.mark.usefixtures("_setup_vulns")
async def test_spdx(client: AsyncClient, bom: schemas.SPDX):
    res = await client.post("/v1/spdx/querybatch", json=bom.model_dump())
    results = res.json().get("results", [])
    assert len(results) > 0
