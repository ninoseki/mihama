from packageurl import PackageURL
from pydantic import BaseModel, validator


class BasePackage(BaseModel):
    name: str | None
    ecosystem: str | None
    purl: str | None

    @validator("purl")
    def purl_format(cls, v: str | None):
        if v is None:
            return v

        PackageURL.from_string(v)
        return v
