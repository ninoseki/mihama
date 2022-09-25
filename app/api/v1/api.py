from fastapi import APIRouter

from .endpoints import cyclonedx, query, search, vulns

api_router = APIRouter()

api_router.include_router(query.router, tags=["Query"])
api_router.include_router(vulns.router, prefix="/vulns", tags=["Vuln"])
api_router.include_router(cyclonedx.router, prefix="/cyclonedx", tags=["CycloneDX"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
