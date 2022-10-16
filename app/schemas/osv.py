from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, root_validator

from app import models

from .package import BasePackage

# NOTE: define same schemas to exclude PKs from the output


class ExcludePkMixin(BaseModel):
    class Config:
        fields = {"pk": {"exclude": True}}


class Severity(models.Severity, ExcludePkMixin):
    pass


class AffectedPackage(models.Package, ExcludePkMixin):
    pass


class Event(models.Event, ExcludePkMixin):
    pass


class Range(BaseModel):
    type: str
    repo: str | None = None
    events: list[Event]
    database_specific: dict[str, Any] | None = None


class Affected(BaseModel):
    package: AffectedPackage
    ranges: list[Range] | None = None
    versions: list[str] | None = None
    ecosystem_specific: dict[str, Any] | None = None
    database_specific: dict[str, Any] | None = None


class Reference(models.Reference, ExcludePkMixin):
    pass


class Credit(models.Reference, ExcludePkMixin):
    pass


class Vulnerability(BaseModel):
    schema_version: str | None = None
    id: str
    modified: datetime
    published: datetime | None = None
    withdrawn: datetime | None = None
    aliases: list[str] | None = None
    related: list[str] | None = None
    summary: str | None = None
    details: str | None = None
    severity: list[Severity] | None = None
    affected: list[Affected] = Field(default_factory=list)
    references: list[Reference] | None = None
    credits: list[Credit] | None = None
    database_specific: dict[str, Any] | None = None


class Package(BasePackage):
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


class Query(BaseModel):
    commit: str | None = Field(
        default=None,
        description="The commit hash to query for. If specified, version should not be set.",
    )
    version: str | None = Field(
        default=None,
        description="The version string to query for. A fuzzy match is done against upstream versions. If specified, commit should not be set.",
    )
    package: Package | None = Field(
        default=None,
        description="The package to query against. When a commit hash is given, this is optional.",
    )

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
    vulns: list[Vulnerability]


class SimplifiedVulnerability(BaseModel):
    id: str
    modified: datetime | None


class SimplifiedVulnerabilities(BaseModel):
    vulns: list[SimplifiedVulnerability]


class BatchQuery(BaseModel):
    queries: list[Query] = Field(max_items=1000)


class BatchResponse(BaseModel):
    results: list[SimplifiedVulnerabilities]
