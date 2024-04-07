import pytest
from httpx import AsyncClient

from mihama import schemas


@pytest.mark.asyncio()
async def test_get_by_id(
    client: AsyncClient,
    vulns: list[schemas.Vulnerability],
    _setup_vulns,  # noqa: PT019
):
    for v in vulns:
        res = await client.get(f"/v1/vulns/{v.id}")
        assert res.status_code == 200
