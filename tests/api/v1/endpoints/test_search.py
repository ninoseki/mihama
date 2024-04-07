import pytest
from httpx import AsyncClient

from mihama import schemas


@pytest.mark.asyncio()
async def test_search(client: AsyncClient, vulns: list[schemas.Vulnerability]):
    for v in vulns:
        for affected in v.affected:
            if affected.package is None:
                continue

            res = await client.post(
                "/v1/search/package",
                json={"package": affected.package.model_dump()},
            )
            vulns = res.json().get("vulns", [])
            assert len(vulns) > 0
