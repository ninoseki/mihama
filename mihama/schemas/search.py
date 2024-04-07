from pydantic import Field

from .api_model import APIModel
from .osv import Vulnerability
from .types import OptionalPurl


class SearchResults(APIModel):
    vulns: list[Vulnerability]
    total: int


class SearchPackage(APIModel):
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


class SearchQuery(APIModel):
    package: SearchPackage
    search_after: list[int] | None = Field(default=None)
