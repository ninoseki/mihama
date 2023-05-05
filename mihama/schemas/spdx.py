from pydantic import Field

from . import osv
from .api_model import APIModel


class ExternalRef(APIModel):
    comment: str | None = None
    reference_category: str = Field(
        ..., description="Category for the external reference"
    )
    reference_locator: str = Field(
        ...,
        description="The unique string with no spaces necessary to access the package-specific information, metadata, or content within the target location. The format of the locator is subject to constraints defined by the <type>.",
    )
    reference_type: str = Field(
        ...,
        description="Type of the external reference. These are defined in an appendix in the SPDX specification.",
    )

    def to_query(self) -> osv.Query | None:
        if self.reference_type != "purl":
            return None

        return osv.Query(package=osv.Package(purl=self.reference_locator))


class Package(APIModel):
    external_refs: list[ExternalRef] = Field(
        default_factory=list,
        description="An External Reference allows a Package to reference an external source of additional information, metadata, enumerations, asset identifiers, or downloadable content believed to be relevant to the Package.",
    )

    def to_queries(self) -> list[osv.Query]:
        queries = [external_ref.to_query() for external_ref in self.external_refs]
        return [q for q in queries if q is not None]


class SPDX(APIModel):
    packages: list[Package] = Field(
        default_factory=list, description="Packages referenced in the SPDX document"
    )

    def to_batch_query(self) -> osv.BatchQuery:
        queries: list[osv.Query] = []
        for package in self.packages:
            queries.extend(package.to_queries())

        return osv.BatchQuery(queries=queries)
