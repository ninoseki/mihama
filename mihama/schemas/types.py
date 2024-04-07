from typing import Annotated

from packageurl import PackageURL
from pydantic import (
    AfterValidator,
)


def validate_optional_purl(v: str | None) -> str | None:
    if v is None:
        return v

    PackageURL.from_string(v)
    return v


OptionalPurl = Annotated[
    str | None,
    AfterValidator(validate_optional_purl),
]
