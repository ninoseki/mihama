from pydantic import BaseModel

from .osv import Vulnerability


class SearchResults(BaseModel):
    vulns: list[Vulnerability]
    total: int
