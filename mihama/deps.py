from contextlib import asynccontextmanager
from typing import Annotated

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from mihama import settings


@asynccontextmanager
async def get_es_with_context():
    es = AsyncElasticsearch(
        hosts=settings.ES_HOSTS,
        basic_auth=(settings.ES_USERNAME, str(settings.ES_PASSWORD)),
    )
    try:
        yield es
    finally:
        await es.close()


async def get_es():
    async with get_es_with_context() as es:
        yield es


Elasticsearch = Annotated[AsyncElasticsearch, Depends(get_es)]
