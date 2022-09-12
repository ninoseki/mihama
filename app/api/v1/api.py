from fastapi import APIRouter

from .endpoints import query, vulns

api_router = APIRouter()

api_router.include_router(query.router)
api_router.include_router(vulns.router, prefix="/vulns")
