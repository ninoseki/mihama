from packageurl import PackageURL
from pydantic import BaseModel, Field, validator


class BasePackage(BaseModel):
    name: str | None = Field(
        default=None,
        description="Name of the package. Should match the name used in the package ecosystem (e.g. the npm package name). For C/C++ projects integrated in OSS-Fuzz, this is the name used for the integration.",
    )
    ecosystem: str | None = Field(
        default=None,
        description="The ecosystem for this package. For the complete list of valid ecosystem names.",
    )
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
