import asyncio

import typer
from loguru import logger

from app import crud
from app.arq.tasks import update_by_ecosystem
from app.core import settings

app = typer.Typer()


@app.command(help="Update OSV vulnerabilities")
def update(
    ecosystems: list[str] = list(settings.OSV_ECOSYSTEMS),
    overwrite: bool = typer.Option(
        True, help="Whether to overwrite vulnerability data of the same ID"
    ),
):
    for ecosystem in ecosystems:
        asyncio.run(update_by_ecosystem(ecosystem, overwrite=overwrite))


@app.command(help="Remove all OSV vulnerabilities")
def cleanup():
    async def _cleanup():
        all_pks = [pk for pk in crud.vulnerability.all_pks()]

        logger.info(f"Delete {len(all_pks)} vulnerabilities...")

        crud.vulnerability.delete_by_pks(all_pks)

        logger.info("Done")

    asyncio.run(_cleanup())


if __name__ == "__main__":
    app()
