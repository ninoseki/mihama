from typing import cast

from arq.connections import ArqRedis
from elasticsearch import AsyncElasticsearch
from loguru import logger

from mihama import crud, deps, schemas, settings
from mihama.factories.vulnerability import VulnerabilityFactory

from . import constants


async def update_vulns(
    es: AsyncElasticsearch,
    vulns: list[schemas.Vulnerability],
    overwrite: bool = True,
):
    if overwrite:
        try:
            await crud.vulnerability.bulk_index(es, vulns)
        except Exception as e:
            logger.exception(e)
        return

    missing_vulns = [
        vuln for vuln in vulns if not (await crud.vulnerability.exists(es, vuln.id))
    ]
    await crud.vulnerability.bulk_index(es, missing_vulns)


async def update_by_ecosystem(
    es: AsyncElasticsearch, ecosystem: str, *, overwrite: bool = True
):
    vulns = VulnerabilityFactory.by_ecosystem(ecosystem)

    logger.info(f"osv.dev's {ecosystem} ecosystem has {len(vulns)} vulnerabilities.")
    await update_vulns(es, vulns, overwrite=overwrite)
    logger.info(f"Updated {len(vulns)} {ecosystem} ecosystem vulnerabilities.")


async def update_by_ecosystem_task(_ctx: dict, ecosystem: str):
    async with deps.get_es_with_context() as es:
        await update_by_ecosystem(es, ecosystem)


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
    logger.info(f"OSSF malicious packages repo has {len(vulns)} vulnerabilities.")

    async with deps.get_es_with_context() as es:
        await update_vulns(es, vulns, overwrite=overwrite)

    logger.info(f"Updated {len(vulns)} OSSF malicious packages vulnerabilities.")
