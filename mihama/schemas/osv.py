from datetime import datetime
from functools import cached_property
from typing import Any

from packageurl import PackageURL
from pydantic import (
    BaseModel,
    Field,
    model_validator,
)
from returns.maybe import Maybe
from returns.pipeline import flow
from returns.pointfree import bind
from returns.result import ResultE, safe
from semver.version import Version

from mihama.utils import safe_parse_version

from .types import OptionalPurl


class Severity(BaseModel):
    type: str
    score: str


class Package(BaseModel):
    ecosystem: str
    name: str
    purl: OptionalPurl = None


class QueryPackage(BaseModel):
    name: str | None = Field(
        default=None,
        description="Name of the package. Should match the name used in the package ecosystem (e.g. the npm package name). For C/C++ projects integrated in OSS-Fuzz, this is the name used for the integration.",
    )
    ecosystem: str | None = Field(
        default=None,
        description="The ecosystem for this package. For the complete list of valid ecosystem names.",
    )
    purl: OptionalPurl = Field(
        default=None,
        description="The package URL for this package.",
    )

    @model_validator(mode="after")
    def check_consistency(self):
        has_ecosystem = self.ecosystem is not None
        has_name = self.name is not None
        has_purl = self.purl is not None
        has_name_or_purl = has_name or has_purl

        if has_ecosystem and not has_name_or_purl:
            raise ValueError("name or purl should be included")

        if all([not has_ecosystem, not has_name, not has_purl]):
            raise ValueError("One of name, ecosystem and purl should be included")

        return self


class Event(BaseModel):
    introduced: str | None = None
    fixed: str | None = None
    last_affected: str | None = None
    limit: str | None = None


class Range(BaseModel):
    type: str
    repo: str | None = None
    events: list[Event]
    database_specific: dict[str, Any] | None = None

    @property
    def is_semver_type(self) -> bool:
        return self.type == "SEMVER"

    @property
    def introduced(self) -> str | None:
        for event in self.events:
            if event.introduced is not None:
                return event.introduced

        return None

    @property
    def fixed(self) -> str | None:
        for event in self.events:
            if event.fixed is not None:
                return event.fixed

        return None

    @property
    def last_affected(self) -> str | None:
        for event in self.events:
            if event.last_affected is not None:
                return event.last_affected

        return None

    def is_introduced(self, semver_version: Version) -> bool:
        @safe
        def _is_introduced(semver_introduced: Version):
            return semver_version >= semver_introduced

        result: ResultE[bool] = flow(
            self.introduced, safe_parse_version, bind(_is_introduced)
        )
        return result.value_or(False)

    def is_fixed(self, semver_version: Version):
        @safe
        def _is_fixed(semver_fixed: Version):
            return semver_version >= semver_fixed

        result: ResultE[bool] = flow(self.fixed, safe_parse_version, bind(_is_fixed))
        return result.value_or(False)

    def is_no_longer_affected(self, semver_version: Version):
        @safe
        def _is_no_longer_affected(semver_last_affected: Version):
            return semver_version > semver_last_affected

        result: ResultE[bool] = flow(
            self.last_affected, safe_parse_version, bind(_is_no_longer_affected)
        )
        return result.value_or(False)

    def is_affected_version(self, version: str) -> bool:
        if not self.is_semver_type:
            # NOTE: it is impossible to do semantics versioning based comparison
            #       if it is not a SEMVER type
            return False

        @safe
        def inner(semver_version: Version):
            if not self.is_introduced(semver_version):
                return False

            if self.is_fixed(semver_version):
                return False

            if self.is_no_longer_affected(semver_version):
                return False

            return True

        result: ResultE[bool] = flow(version, safe_parse_version, bind(inner))
        return result.value_or(False)


class Affected(BaseModel):
    package: Package | None = None
    ranges: list[Range] | None = None
    versions: list[str] | None = None
    ecosystem_specific: dict[str, Any] | None = None
    database_specific: dict[str, Any] | None = None
    severity: list[Severity] | None = None

    @cached_property
    def maybe_package(self):
        return Maybe.from_optional(self.package)

    @property
    def package_name(self):
        return self.maybe_package.bind_optional(lambda x: x.name).value_or(None)

    @property
    def package_purl(self):
        return self.maybe_package.bind_optional(lambda x: x.purl).value_or(None)

    @property
    def package_ecosystem(self):
        return self.maybe_package.bind_optional(lambda x: x.ecosystem).value_or(None)

    def is_affected_package(self, package: Package | QueryPackage) -> bool:
        is_same_purl = (
            self.package_purl is not None
            and self.package_purl is not None
            and package.purl == self.package_purl
        )
        if is_same_purl:
            return True

        is_same_ecosystem = package.ecosystem == self.package_ecosystem
        is_same_name = package.name == self.package_name
        return is_same_ecosystem and is_same_name

    def is_affected_version(self, version: str):
        if version in (self.versions or []):
            return True

        results = [r.is_affected_version(version) for r in self.ranges or []]
        return all(results)

    def is_affected_package_version(
        self, *, package: Package | QueryPackage, version: str
    ) -> bool:
        if not self.is_affected_package(package):
            return False

        return self.is_affected_version(version)


class Reference(BaseModel):
    type: str
    url: str


class Credit(BaseModel):
    name: str
    contact: list[str] | None = None


class Vulnerability(BaseModel):
    id: str
    schema_version: str | None = None
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

    sort: list[int | str] | None = Field(default=None)

    def is_affected_package_version(
        self, *, package: Package | QueryPackage, version: str
    ) -> bool:
        for affected in self.affected:
            if affected.is_affected_package_version(package=package, version=version):
                return True

        return False


class Query(BaseModel):
    commit: str | None = Field(
        default=None,
        description="The commit hash to query for. If specified, version should not be set.",
    )
    version: str | None = Field(
        default=None,
        description="The version string to query for. A fuzzy match is done against upstream versions. If specified, commit should not be set.",
    )
    package: QueryPackage | None = Field(
        default=None,
        description="The package to query against. When a commit hash is given, this is optional.",
    )

    search_after: list[int | str] | None = Field(default=None)

    @property
    def package_purl(self) -> PackageURL | None:
        if self.package is None or self.package.purl is None:
            return None

        return PackageURL.from_string(self.package.purl)

    @model_validator(mode="after")
    def check_consistency(self):
        has_commit = self.commit is not None
        has_version = self.version is not None
        has_package = self.package is not None

        if has_commit:
            raise ValueError("commit is not supported yet")

        if all([not has_commit, not has_package]):
            raise ValueError("commit or package should be included")

        if has_version and not has_package:
            raise ValueError("package should be included")

        return self

    @model_validator(mode="after")
    def replace_version(self):
        if self.package_purl is None:
            return self

        self.version = self.package_purl.version

        return self


class SimplifiedVulnerability(BaseModel):
    id: str
    modified: datetime


class SimplifiedVulnerabilities(BaseModel):
    vulns: list[SimplifiedVulnerability]


class Vulnerabilities(BaseModel):
    vulns: list[Vulnerability]

    def simplify(self) -> SimplifiedVulnerabilities:
        return SimplifiedVulnerabilities(
            vulns=[
                SimplifiedVulnerability(id=v.id, modified=v.modified)
                for v in self.vulns
            ]
        )


class BatchQuery(BaseModel):
    queries: list[Query] = Field(max_length=1000)

    def __iter__(self):
        return iter(self.queries)


class BatchResponse(BaseModel):
    results: list[SimplifiedVulnerabilities]
