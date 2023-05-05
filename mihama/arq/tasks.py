from typing import cast

from arq.connections import ArqRedis
from loguru import logger

from mihama import crud
from mihama.core import settings
from mihama.factories.vulnerability import VulnerabilityFactory

from . import constants


async def update_by_ecosystem(ecosystem: str, *, overwrite: bool = True):
    vulnerabilities = VulnerabilityFactory.by_ecosystem(ecosystem)

    logger.info(f"{ecosystem} has {len(vulnerabilities)} vulnerabilities...")

    for v in vulnerabilities:
        v_ = await crud.vulnerability.get_by_id(v.id)

        if v_ is None:
            await crud.vulnerability.save(v)
            continue

        if not overwrite:
            continue

        await crud.vulnerability.update(v_, **v.dict())

    logger.info(f"Updated {ecosystem} vulnerabilities")


async def update_by_ecosystem_task(_ctx: dict, ecosystem: str):
    await update_by_ecosystem(ecosystem)


async def update_by_ecosystems_task(ctx: dict):
    redis = cast(ArqRedis, ctx["redis"])

    for ecosystem in settings.OSV_ECOSYSTEMS:
        await redis.enqueue_job(constants.UPDATE_BY_ECOSYSTEM_TASK, ecosystem=ecosystem)
