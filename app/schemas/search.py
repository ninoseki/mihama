from pydantic import BaseModel

from .mixins import (
    OptionalPackageEcosystemMixin,
    OptionalPackageNameMixin,
    OptionalPurlMixin,
)
from .osv import Vulnerability


class SearchPackage(
    OptionalPurlMixin,
    OptionalPackageEcosystemMixin,
    OptionalPackageNameMixin,
    BaseModel,
):
    pass


class SearchResults(BaseModel):
    vulns: list[Vulnerability]
    total: int
