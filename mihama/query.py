from typing import Optional, cast

from packageurl import PackageURL

from mihama import schemas


def _clean_purl(purl: PackageURL) -> PackageURL:
    """
    Clean a purl object.
    Removes version, subpath, and qualifiers with the exception of
    the 'arch' qualifier
    """
    values = purl.to_dict()
    values.pop("version", None)
    values.pop("subpath", None)
    qualifiers = values.pop("qualifiers", None)
    new_qualifiers = {}

    if qualifiers and "arch" in qualifiers:  # CPU arch for debian packages
        new_qualifiers["arch"] = qualifiers["arch"]

    return PackageURL(qualifiers=new_qualifiers, **values)


def normalize_package(
    package: schemas.QueryPackage | schemas.SearchPackage,
) -> schemas.QueryPackage | schemas.SearchPackage:
    purl: PackageURL | None = None

    if package.purl is None:
        return package

    parsed_purl = PackageURL.from_string(package.purl)
    purl = _clean_purl(parsed_purl)

    normalized = package.model_copy(deep=True)
    normalized.purl = str(purl)

    return normalized


def normalize_query(query: schemas.Query):
    if query.package is None:
        return query

    purl: PackageURL | None = None
    purl_version: str | None = None

    if query.package.purl is not None:
        parsed_purl = PackageURL.from_string(query.package.purl)
        purl_version = cast(Optional[str], parsed_purl.version)
        purl = _clean_purl(parsed_purl)

    normalized = query.model_copy(deep=True)
    if normalized.package is not None and purl is not None:
        normalized.package.purl = str(purl)

    if purl_version is not None:
        normalized.version = purl_version

    return normalized
