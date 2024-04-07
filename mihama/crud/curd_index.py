from typing import Any

from elasticsearch import AsyncElasticsearch, NotFoundError

from mihama import settings


class CRUDIndex:
    async def create(
        self,
        es: AsyncElasticsearch,
        index: str = settings.ES_INDEX,
    ):
        return await es.indices.create(index=index)

    async def create_if_not_exists(
        self,
        es: AsyncElasticsearch,
        index: str = settings.ES_INDEX,
    ):
        if await self.exists(es, index):
            return None

        return self.create(es, index=index)

    async def exists(
        self,
        es: AsyncElasticsearch,
        index: str = settings.ES_INDEX,
    ) -> bool:
        try:
            await es.indices.get(index=index)
            return True
        except NotFoundError:
            return False

    async def pu_mapping(
        self,
        es: AsyncElasticsearch,
        *,
        properties: dict[str, Any],
        index: str = settings.ES_INDEX,
    ):
        return await es.indices.put_mapping(index=index, properties=properties)


index = CRUDIndex()
