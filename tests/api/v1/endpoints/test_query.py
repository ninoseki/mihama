import pytest
from httpx import AsyncClient

from mihama import schemas


@pytest.mark.asyncio()
async def test_query(client: AsyncClient, vulns: list[schemas.Vulnerability]):
    for v in vulns:
        for affected in v.affected:
            if affected.package is None:
                continue

            for version in affected.versions or []:
                payload = {"version": version, "package": affected.package.model_dump()}
                res = await client.post("/v1/query", json=payload)
                assert res.status_code == 200

                vulns = res.json().get("vulns", [])
                assert len(vulns) > 0


@pytest.mark.asyncio()
async def test_querybatch(client: AsyncClient, vulns: list[schemas.Vulnerability]):
    queries = []
    for v in vulns:
        for affected in v.affected:
            if affected.package is None:
                continue

            for version in affected.versions or []:
                queries.append(
                    {"version": version, "package": affected.package.model_dump()}
                )

    res = await client.post("/v1/querybatch", json={"queries": queries})

    results = res.json().get("results", [])
    assert len(results) > 0

    for r in results:
        vulns = r.get("vulns", [])
        assert len(vulns) > 0
