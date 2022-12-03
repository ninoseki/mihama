import pytest
from httpx import AsyncClient

from mihama import models


@pytest.mark.asyncio
async def test_search(client: AsyncClient, vulnerabilities: list[models.Vulnerability]):
    for v in vulnerabilities:
        for affected in v.affected:
            res = await client.post(
                "/v1/search/package", json={"package": affected.package.dict()}
            )
            assert res.status_code == 200

            vulns = res.json().get("vulns", [])
            assert len(vulns) > 0
