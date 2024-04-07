import typing

from packageurl import PackageURL
from returns.result import safe
from semver.version import Version
from starlette.datastructures import CommaSeparatedStrings

from .osv.semver_index import parse

T = typing.TypeVar("T")


def cast_csv(
    csv: CommaSeparatedStrings,
    cast: typing.Callable[[typing.Any], T],
):
    return [cast(v) for v in csv]


@safe
def safe_parse_version(version: str | None) -> Version:
    if version is None:
        raise ValueError("version is None")

    return parse(version)


@safe
def safe_parse_purl(purl: str) -> PackageURL:
    return PackageURL.from_string(purl)
