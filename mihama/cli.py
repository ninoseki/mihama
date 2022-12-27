import asyncio
import functools

import aiometer
import decorator
import typer
from loguru import logger

from mihama import crud
from mihama.arq.tasks import update_by_ecosystem
from mihama.core import settings
from mihama.redis import setup_redis_om

app = typer.Typer()


@decorator.decorator
async def with_redis_om_setup(func, *args, **kwargs):
    await setup_redis_om()
    return await func(*args, **kwargs)


@app.command(help="Update OSV vulnerabilities by ecosystems")
def update(
    ecosystems: list[str] = list(settings.OSV_ECOSYSTEMS),
    overwrite: bool = typer.Option(
        True, help="Whether to overwrite vulnerability data with the same ID"
    ),
    max_at_once: int = typer.Option(5, help="Max number of concurrent jobs"),
):
    @with_redis_om_setup
    async def _update():
        if len(ecosystems) == 0:
            return

        jobs = [
            functools.partial(update_by_ecosystem, ecosystem, overwrite=overwrite)
            for ecosystem in ecosystems
        ]
        await aiometer.run_all(jobs, max_at_once=max_at_once)

    asyncio.run(_update())


@app.command(help="Get OSV vulnerability by ID")
def get(id: str):
    @with_redis_om_setup
    async def _get_by_id():
        vuln = await crud.vulnerability.get_by_id(id)
        if vuln is None:
            logger.info(f"{id} does not exist")
            return

        print(vuln.json())  # noqa: T201

    asyncio.run(_get_by_id())


@app.command(help="Delete OSV vulnerability by ID")
def delete(
    id: str,
    force_delete: bool = typer.Option(
        False, help="Whether to delete vulnerability without confirmation"
    ),
):
    @with_redis_om_setup
    async def _delete_by_id():
        vuln = await crud.vulnerability.get_by_id(id)
        if vuln is None:
            logger.info(f"{id} does not exist")
            return

        if not force_delete:
            typer.confirm(
                f"Are you sure you want to delete {id}?",
                abort=True,
            )

        await crud.vulnerability.delete(vuln)
        logger.info(f"{id} is deleted")

    asyncio.run(_delete_by_id())


@app.command(help="Remove all OSV vulnerabilities")
def cleanup(
    force_delete: bool = typer.Option(
        False, help="Whether to delete vulnerabilities without confirmation"
    )
):
    @with_redis_om_setup
    async def _cleanup():
        all_pks: list[str] = []
        async for pk in await crud.vulnerability.all_pks():
            all_pks.append(pk)

        if not force_delete:
            typer.confirm(
                f"Are you sure you want to delete {len(all_pks)} vulnerabilities?",
                abort=True,
            )

        logger.info(f"Delete {len(all_pks)} vulnerabilities...")

        await crud.vulnerability.delete_by_pks(all_pks)

        logger.info("Done")

    asyncio.run(_cleanup())


if __name__ == "__main__":
    app()
