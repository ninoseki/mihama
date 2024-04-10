from pydantic import BaseModel, Field

from .osv import Vulnerability


class SearchResults(BaseModel):
    vulns: list[Vulnerability]
    total: int


class SearchQuery(BaseModel):
    ecosystem: str | None = Field(default=None)
    q: str | None = Field(default=None)
    search_after: list[int | str] | None = Field(default=None)
