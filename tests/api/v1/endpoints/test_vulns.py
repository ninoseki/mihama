import pytest
from httpx import AsyncClient

from mihama import schemas


@pytest.mark.asyncio()
@pytest.mark.usefixtures("_setup_vulns")
async def test_get_by_id(
    client: AsyncClient,
    vulns: list[schemas.Vulnerability],
):
    for v in vulns:
        res = await client.get(f"/v1/vulns/{v.id}")
        assert res.status_code == 200


@pytest.mark.asyncio()
async def test_search(client: AsyncClient, vulns: list[schemas.Vulnerability]):
    for v in vulns:
        for affected in v.affected:
            if affected.package is None:
                continue

            res = await client.post(
                "/v1/vulns/",
                json={
                    "ecosystem": affected.package.ecosystem,
                    "name": affected.package.name,
                },
            )
            vulns = res.json().get("vulns", [])
            assert len(vulns) > 0
