from aredis_om.model.model import Expression

from app import models, schemas
from app.query import normalize_query


class CRUDVulnerabilitySearchMixin:
    async def search_by_package(
        self, package: schemas.Package
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

        return await models.Vulnerability.find(*expressions).all()

    async def search_by_query(self, query: schemas.Query) -> list[models.Vulnerability]:
        if query.package is None:
            # TODO: query by commit is not supported yet
            return []

        normalized = normalize_query(query)
        if normalized.package is None:
            return []

        vulnerabilities = await self.search_by_package(normalized.package)

        if normalized.version is None:
            return vulnerabilities

        return [v for v in vulnerabilities if v.is_affected_version(normalized.version)]
