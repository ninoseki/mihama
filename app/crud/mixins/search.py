from aredis_om.model.model import Expression

from app import models, schemas
from app.core import settings
from app.query import normalize_query


class CRUDVulnerabilitySearchMixin:
    async def search_by_package(
        self,
        package: schemas.Package | schemas.BasePackage,
        *,
        batch_size: int = settings.REDIS_OM_BATCH_SIZE,
        limit: int | None = None,
        offset: int | None = None,
        sort_by: list[str] | None = ["timestamp"]
    ) -> list[models.Vulnerability]:
        expressions: list[Expression] = []

        if package.name is not None:
            expressions.append(
                models.Vulnerability.affected.package.name == package.name
            )

        if package.ecosystem is not None:
            expressions.append(
                models.Vulnerability.affected.package.ecosystem == package.ecosystem
            )

        if package.purl is not None:
            expressions.append(
                models.Vulnerability.affected.package.purl == package.purl
            )

        find_query = models.Vulnerability.find(*expressions)
        if sort_by is not None:
            find_query = find_query.sort_by(*sort_by)

        if limit is None and offset is None:
            # return all results if limit and offset are None
            return await find_query.all(batch_size=batch_size)

        if limit is not None:
            find_query.limit = limit

        if offset is not None:
            find_query.offset = offset

        return await find_query.execute(exhaust_results=False)

    async def search_by_query(
        self, query: schemas.Query, *, batch_size: int = settings.REDIS_OM_BATCH_SIZE
    ) -> list[models.Vulnerability]:
        if query.package is None:
            # TODO: query by commit is not supported yet
            return []

        normalized = normalize_query(query)
        if normalized.package is None:
            return []

        vulnerabilities = await self.search_by_package(
            normalized.package, batch_size=batch_size
        )

        if normalized.version is None:
            return vulnerabilities

        return [v for v in vulnerabilities if v.is_affected_version(normalized.version)]
