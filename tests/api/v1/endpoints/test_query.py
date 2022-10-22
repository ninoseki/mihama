import pytest
from httpx import AsyncClient

from app import models


@pytest.mark.asyncio
async def test_query(client: AsyncClient, vulnerabilities: list[models.Vulnerability]):
    for v in vulnerabilities:
        for affected in v.affected:
            for version in affected.versions or []:
                payload = {"version": version, "package": affected.package.dict()}
                res = await client.post("/v1/query", json=payload)
                assert res.status_code == 200

                vulns = res.json().get("vulns", [])
                assert len(vulns) > 0


@pytest.mark.asyncio
async def test_querybatch(
    client: AsyncClient, vulnerabilities: list[models.Vulnerability]
):
    queries = []
    for v in vulnerabilities:
        for affected in v.affected:
            for version in affected.versions or []:
                queries.append({"version": version, "package": affected.package.dict()})

    res = await client.post("/v1/querybatch", json={"queries": queries})
    assert res.status_code == 200

    results = res.json().get("results", [])
    assert len(results) > 0

    for r in results:
        vulns = r.get("vulns", [])
        assert len(vulns) > 0
