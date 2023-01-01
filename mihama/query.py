import functools
from typing import Optional, cast

import aiometer
from packageurl import PackageURL

from mihama import crud, schemas
from mihama.cache import cache
from mihama.core import settings


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
    package: schemas.BasePackage | schemas.Package,
) -> schemas.BasePackage | schemas.Package:
    purl: PackageURL | None = None

    if package.purl is None:
        return package

    parsed_purl = PackageURL.from_string(package.purl)
    purl = _clean_purl(parsed_purl)

    normalized = package.copy(deep=True)
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

    normalized = query.copy(deep=True)
    if normalized.package is not None and purl is not None:
        normalized.package.purl = str(purl)

    if purl_version is not None:
        normalized.version = purl_version

    return normalized


@cache()
async def cached_query(query: schemas.Query) -> schemas.Vulnerabilities:
    vulns = await crud.vulnerability.search_by_query(query)
    return schemas.Vulnerabilities(vulns=vulns)


async def batch_query(
    queries: schemas.BatchQuery,
    *,
    max_at_once: int = settings.OSV_QUERY_BATCH_MAX_AT_ONCE
):
    if len(queries.queries) == 0:
        return schemas.BatchResponse(results=[])

    jobs = [functools.partial(cached_query, q) for q in queries.queries]
    results = await aiometer.run_all(jobs, max_at_once=max_at_once)
    return schemas.BatchResponse(results=results)
