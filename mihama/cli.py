import asyncio
import functools

import aiometer
import typer
from loguru import logger

from mihama import crud, deps, settings
from mihama.arq.tasks import update_by_ecosystem

app = typer.Typer()


@app.command(help="Update OSV vulnerabilities by ecosystems")
def update(
    ecosystems: list[str] = list(settings.OSV_ECOSYSTEMS),  # noqa: B006
    overwrite: bool = typer.Option(
        True, help="Whether to overwrite vulnerability data with the same ID"
    ),
    max_at_once: int = typer.Option(5, help="Max number of concurrent jobs"),
):
    async def inner():
        if len(ecosystems) == 0:
            return

        async with deps.get_es_with_context() as es:
            jobs = [
                functools.partial(
                    update_by_ecosystem, es, ecosystem, overwrite=overwrite
                )
                for ecosystem in ecosystems
            ]
            await aiometer.run_all(jobs, max_at_once=max_at_once)

    asyncio.run(inner())


@app.command(help="Get OSV vulnerability by ID")
def get(id: str):
    async def inner():
        async with deps.get_es_with_context() as es:
            vuln = await crud.vulnerability.get(es, id)
            if vuln is None:
                logger.info(f"{id} does not exist")
                return

        print(vuln.model_dump_json(by_alias=True))  # noqa: T201

    asyncio.run(inner())


@app.command(help="Delete OSV vulnerability by ID")
def delete(
    id: str,
    force_delete: bool = typer.Option(
        False, help="Whether to delete vulnerability without confirmation"
    ),
):
    async def inner():
        async with deps.get_es_with_context() as es:
            if not await crud.vulnerability.exists(es, id):
                logger.info(f"{id} does not exist")
                return

            if not force_delete:
                typer.confirm(
                    f"Are you sure you want to delete {id}?",
                    abort=True,
                )

            await crud.vulnerability.delete(es, id)
            logger.info(f"{id} is deleted")

    asyncio.run(inner())


if __name__ == "__main__":
    app()
