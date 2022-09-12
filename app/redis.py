from aredis_om import Migrator


async def setup_redis_om():
    from app import models  # noqa: F401

    await Migrator().run()
