from pydantic import BaseModel

from app import models


class SearchResults(BaseModel):
    vulns: list[models.Vulnerability]
    total: int
