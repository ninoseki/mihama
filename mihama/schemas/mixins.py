from packageurl import PackageURL
from pydantic import BaseModel, Field, validator

name_description = "Name of the package. Should match the name used in the package ecosystem (e.g. the npm package name)"
ecosystem_description = "The ecosystem for this package"


class OptionalPackageNameMixin(BaseModel):
    name: str | None = Field(default=None, description=name_description)


class PackageNameMixin(BaseModel):
    name: str = Field(..., description=name_description)


class OptionalPackageEcosystemMixin(BaseModel):
    ecosystem: str | None = Field(default=None, description=ecosystem_description)


class PackageEcosystemMixin(BaseModel):
    ecosystem: str = Field(..., description=ecosystem_description)


class OptionalPurlMixin(BaseModel):
    purl: str | None = Field(
        default=None,
        description="The package URL for this package.",
    )

    @validator("purl")
    @classmethod
    def purl_format(cls, v: str | None):
        if v is None:
            return v

        PackageURL.from_string(v)
        return v
