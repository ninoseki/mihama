from datetime import datetime
from typing import Any

from aredis_om import EmbeddedJsonModel, Field, JsonModel
from aredis_om.connections import get_redis_connection
from osv.semver_index import parse
from pydantic import BaseModel

from app.core import settings


class ExcludePkModel(BaseModel):
    class Config:
        fields = {"pk": {"exclude": True}}


class BaseEmbeddedJsonModel(EmbeddedJsonModel, ExcludePkModel):
    pass


class BaseJsonModel(JsonModel, ExcludePkModel):
    pass


class Severity(BaseEmbeddedJsonModel):
    type: str
    score: str


class Package(BaseEmbeddedJsonModel):
    ecosystem: str = Field(index=True)
    name: str = Field(index=True)
    purl: str | None = Field(index=True)


class Event(BaseEmbeddedJsonModel):
    introduced: str | None = None
    fixed: str | None = None
    last_affected: str | None = None
    limit: str | None = None


class Range(BaseEmbeddedJsonModel):
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
        if fixed is None:
            # it means that there is not fixed version yet
            return True

        is_fixed = semver_version >= fixed
        return not is_fixed


class Affected(BaseEmbeddedJsonModel):
    package: Package
    ranges: list[Range] | None = None
    versions: list[str] | None = None
    ecosystem_specific: dict[str, Any] | None = None
    database_specific: dict[str, Any] | None = None

    def is_affected_version(self, version: str) -> bool:
        if version in (self.versions or []):
            return True

        results = [range_.is_affected_version(version) for range_ in self.ranges]
        return all(results)


class Reference(BaseEmbeddedJsonModel):
    type: str
    url: str


class Credit(BaseEmbeddedJsonModel):
    name: str
    contact: list[str] | None = None


class Vulnerability(BaseJsonModel):
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

    def is_affected_version(self, version: str) -> bool:
        for affected in self.affected:
            if affected.is_affected_version(version):
                return True

        return False

    class Meta:
        database = get_redis_connection(
            url=str(settings.REDIS_OM_URL), decode_responses=True
        )
