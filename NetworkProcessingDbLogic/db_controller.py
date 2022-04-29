import argparse
import os
import pathlib

import trafaret as t
from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from trafaret_config import commandline

from NetworkProcessingDbLogic.graph_model import DeclarativeBase


class DbController:
    BASE_DIR = pathlib.Path(__file__).parent
    DEFAULT_CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

    TRAFARET = t.Dict(
        {
            t.Key("postgres"): t.Dict(
                {
                    "database": t.String(),
                    "user": t.String(),
                    "password": t.String(),
                    "host": t.String(),
                    "port": t.Int(),
                }
            )
        }
    )

    def __init__(self, app: web.Application, argv=None):
        self.engine = None
        self.session = None
        app["config"] = self.get_config(argv)

    def __getattr__(self, name):
        return getattr(self.session, name)

    async def create_metadata(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(DeclarativeBase.metadata.create_all)

    def get_config(self, argv=None) -> dict:
        ap = argparse.ArgumentParser()
        commandline.standard_argparse_options(
            ap, default_config=self.DEFAULT_CONFIG_PATH
        )
        # ignore unknown options
        options, unknown = ap.parse_known_args(argv)
        config = commandline.config_from_options(options, self.TRAFARET)
        return config

    async def init_database(self, app) -> None:
        """
        This is signal for success creating connection with database
        """
        config = app["config"]["postgres"]
        connection_url = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **config
        )
        self.engine = create_async_engine(connection_url)
        await self.create_metadata()
        self.session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )()
        app["db"] = self.engine

    async def close_database(self, app) -> None:
        """
        This is signal for success closing connection with database before shutdown
        """
        app["db"].close()
        await app["db"].wait_closed()

    def init_app(self, app) -> web.Application:
        app.on_startup.extend([self.init_database])
        app.on_cleanup.extend([self.close_database])
        return app
