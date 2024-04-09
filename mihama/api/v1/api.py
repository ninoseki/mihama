from fastapi import APIRouter

from .endpoints import cyclonedx, ecosystems, query, spdx, vulns

api_router = APIRouter()

api_router.include_router(cyclonedx.router, prefix="/cyclonedx", tags=["CycloneDX"])
api_router.include_router(query.router, tags=["Query"])
api_router.include_router(spdx.router, prefix="/spdx", tags=["SPDX"])
api_router.include_router(vulns.router, prefix="/vulns", tags=["Vuln"])
api_router.include_router(ecosystems.router, prefix="/ecosystems", tags=["Ecosystem"])
