from datetime import datetime
from typing import Any

from aredis_om import Field
from aredis_om.connections import get_redis_connection

from mihama.core import settings
from mihama.monkeypatch.model import EmbeddedJsonModel, JsonModel
from mihama.osv.semver_index import parse


class Severity(EmbeddedJsonModel):
    type: str
    score: str


class Package(EmbeddedJsonModel):
    ecosystem: str = Field(index=True)
    name: str = Field(index=True)
    purl: str | None = Field(index=True)


class Event(EmbeddedJsonModel):
    introduced: str | None = None
    fixed: str | None = None
    last_affected: str | None = None
    limit: str | None = None


class Range(EmbeddedJsonModel):
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

    def get_semver_introduced(self):
        try:
            return parse(self.introduced or "")
        except ValueError:
            return None

    @property
    def fixed(self) -> str | None:
        for event in self.events:
            if event.fixed is not None:
                return event.fixed

        return None

    def get_semver_fixed(self):
        try:
            return parse(self.fixed or "")
        except ValueError:
            return None

    @property
    def last_affected(self) -> str | None:
        for event in self.events:
            if event.last_affected is not None:
                return event.last_affected

        return None

    def get_semver_last_affected(self):
        try:
            return parse(self.last_affected or "")
        except ValueError:
            return None

    def is_affected_version(self, version: str) -> bool:
        if not self.is_semver_type:
            # NOTE: it is impossible to do semantics versioning based comparison
            #       if it is not a SEMVER type
            return False

        try:
            semver_version = parse(version)
        except ValueError:
            # NOTE: if version does not follow semantics versioning,
            #       it is impossible do the comparison
            return False

        introduced = self.get_semver_introduced()

        if introduced is None:
            return False

        is_introduced = semver_version >= introduced
        if not is_introduced:
            return False

        fixed = self.get_semver_fixed()
        if fixed is not None:
            is_fixed = semver_version >= fixed
            if is_fixed:
                return False

        last_affected = self.get_semver_last_affected()
        if last_affected is None:
            return True

        return semver_version <= last_affected


class Affected(EmbeddedJsonModel):
    package: Package
    ranges: list[Range] | None = None
    versions: list[str] | None = None
    ecosystem_specific: dict[str, Any] | None = None
    database_specific: dict[str, Any] | None = None

    def is_affected_package(self, package: Package) -> bool:
        is_same_ecosystem = package.ecosystem == self.package.ecosystem
        is_same_name = package.name == self.package.name
        return is_same_ecosystem and is_same_name

    def is_affected_version(self, version: str):
        if version in (self.versions or []):
            return True

        results = [range_.is_affected_version(version) for range_ in self.ranges]
        return all(results)

    def is_affected_package_version(self, *, package: Package, version: str) -> bool:
        if not self.is_affected_package(package):
            return False

        return self.is_affected_version(version)


class Reference(EmbeddedJsonModel):
    type: str
    url: str


class Credit(EmbeddedJsonModel):
    name: str
    contact: list[str] | None = None


class Vulnerability(JsonModel):
    schema_version: str | None = None
    id: str = Field(index=True)
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

    # NOTE: this is a float version of "modified" for sorting
    timestamp: float | None = Field(None, index=True, sortable=True)

    def __init__(self, **data: Any):
        super().__init__(**data)

        self.timestamp = self.modified.timestamp()

    def is_affected_package_version(self, *, package: Package, version: str) -> bool:
        for affected in self.affected:
            if affected.is_affected_package_version(package=package, version=version):
                return True

        return False

    class Meta:
        database = get_redis_connection(
            url=str(settings.REDIS_OM_URL), decode_responses=True
        )
