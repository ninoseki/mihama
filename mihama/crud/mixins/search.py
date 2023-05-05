from aredis_om.model.model import Expression, FindQuery

from mihama import models, schemas
from mihama.core import settings
from mihama.query import normalize_query

PACKAGE = schemas.BasePackage | schemas.Package


def build_find_query_by_package(
    package: PACKAGE,
) -> FindQuery:
    expressions: list[Expression] = []

    if package.name is not None:
        expressions.append(models.Vulnerability.affected.package.name == package.name)  # type: ignore

    if package.ecosystem is not None:
        expressions.append(
            models.Vulnerability.affected.package.ecosystem == package.ecosystem  # type: ignore
        )

    if package.purl is not None:
        expressions.append(models.Vulnerability.affected.package.purl == package.purl)  # type: ignore

    return models.Vulnerability.find(*expressions)


class CRUDVulnerabilitySearchMixin:
    async def search_by_package(
        self,
        package: PACKAGE,
        *,
        batch_size: int = settings.REDIS_OM_BATCH_SIZE,
        limit: int | None = None,
        offset: int | None = None,
        sort_by: list[str] | None = None
    ) -> list[models.Vulnerability]:
        sort_by = sort_by or ["-timestamp"]

        find_query = build_find_query_by_package(package)
        if sort_by is not None:
            find_query = find_query.sort_by(*sort_by)

        if limit is None and offset is None:
            # return all results if limit and offset are None
            return await find_query.all(batch_size=batch_size)  # type: ignore

        if limit is not None:
            find_query.limit = limit

        if offset is not None:
            find_query.offset = offset

        return await find_query.execute(exhaust_results=False)  # type: ignore

    async def search_by_query(
        self, query: schemas.Query, *, batch_size: int = settings.REDIS_OM_BATCH_SIZE
    ) -> list[models.Vulnerability]:
        normalized = normalize_query(query)
        if normalized.package is None or normalized.version is None:
            return []

        vulnerabilities = await self.search_by_package(
            normalized.package, batch_size=batch_size
        )
        return [
            v
            for v in vulnerabilities
            if v.is_affected_package_version(
                package=normalized.package, version=normalized.version
            )
        ]

    async def count_by_package(self, package: PACKAGE) -> int:
        find_query = build_find_query_by_package(package)
        return await find_query.count()  # type: ignore
