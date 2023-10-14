from typing import cast

from arq.connections import ArqRedis
from loguru import logger

from mihama import crud, models
from mihama.core import settings
from mihama.factories.vulnerability import VulnerabilityFactory

from . import constants


async def update_vulns(vulns: list[models.Vulnerability], *, overwrite: bool = True):
    for v in vulns:
        v_ = await crud.vulnerability.get_by_id(v.id)

        if v_ is None:
            await crud.vulnerability.save(v)
            continue

        if not overwrite:
            continue

        await crud.vulnerability.update(v_, **v.dict())


async def update_by_ecosystem(ecosystem: str, *, overwrite: bool = True):
    vulns = VulnerabilityFactory.by_ecosystem(ecosystem)

    logger.info(f"{ecosystem} has {len(vulns)} vulnerabilities...")
    await update_vulns(vulns, overwrite=overwrite)
    logger.info(f"Updated {len(vulns)} vulnerabilities from OSV's {ecosystem}")


async def update_by_ecosystem_task(_ctx: dict, ecosystem: str):
    await update_by_ecosystem(ecosystem)


async def update_by_ecosystems_task(ctx: dict, *, ecosystems=settings.OSV_ECOSYSTEMS):
    redis = cast(ArqRedis, ctx["redis"])

    for ecosystem in ecosystems:
        await redis.enqueue_job(constants.UPDATE_BY_ECOSYSTEM_TASK, ecosystem=ecosystem)


async def update_ossf_malicious_packages_task(
    _ctx: dict,
    *,
    repo_url: str = settings.OSSF_MALICIOUS_PACKAGES_REPO_URL,
    overwrite: bool = True,
):
    vulns = VulnerabilityFactory.from_repo_url(repo_url)
    logger.info(f"OSSF malicious packages repo has {len(vulns)} vulnerabilities...")
    await update_vulns(vulns, overwrite=overwrite)
    logger.info(
        f"Updated {len(vulns)} vulnerabilities from OSSF malicious packages repo"
    )
