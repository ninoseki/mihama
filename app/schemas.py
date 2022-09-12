from datetime import datetime
from typing import Any

from packageurl import PackageURL
from pydantic import BaseModel, Field, root_validator, validator

from app import models


class Package(BaseModel):
    name: str | None
    ecosystem: str | None
    purl: str | None

    @root_validator
    def check_consistency(cls, values: dict[str, Any]):
        has_ecosystem = values.get("ecosystem") is not None
        has_name = values.get("name") is not None
        has_purl = values.get("purl") is not None

        has_name_or_purl = has_name or has_purl

        if has_ecosystem and not has_name_or_purl:
            raise ValueError("name or purl should be included")

        if all([not has_ecosystem, not has_name, not has_purl]):
            raise ValueError("One of name, ecosystem and purl should be included")

        return values

    @validator("purl")
    def purl_format(cls, v: str | None):
        if v is None:
            return v

        PackageURL.from_string(v)
        return v


class Query(BaseModel):
    commit: str | None
    version: str | None
    package: Package | None

    @root_validator
    def check_consistency(cls, values: dict[str, Any]):
        has_commit = values.get("commit") is not None
        has_version = values.get("version") is not None
        has_package = values.get("package") is not None

        if has_commit:
            raise ValueError("commit is not supported yet")

        if all([not has_commit, not has_package]):
            raise ValueError("commit or package should be included")

        if has_version and not has_package:
            raise ValueError("package should be included")

        return values


class Vulnerabilities(BaseModel):
    vulns: list[models.Vulnerability]


class SimplifiedVulnerability(BaseModel):
    id: str
    modified: datetime | None


class SimplifiedVulnerabilities(BaseModel):
    vulns: list[SimplifiedVulnerability]


class BatchQuery(BaseModel):
    queries: list[Query] = Field(max_items=1000)


class BatchResponse(BaseModel):
    results: list[SimplifiedVulnerabilities]
