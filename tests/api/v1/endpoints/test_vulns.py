import pytest
from httpx import AsyncClient

from mihama import models


@pytest.mark.asyncio
async def test_get_by_id(
    client: AsyncClient, vulnerabilities: list[models.Vulnerability]
):
    for v in vulnerabilities:
        res = await client.get(f"/v1/vulns/{v.id}")
        assert res.status_code == 200
