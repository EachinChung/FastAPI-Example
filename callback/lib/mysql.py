from typing import NoReturn

from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from callback.setting import setting


def register_mysql(app: FastAPI) -> NoReturn:
    mysql = setting.mysql
    register_tortoise(
        app,
        db_url=f"mysql://{mysql.user}:{mysql.password}@{mysql.host}:{mysql.port}/{mysql.database}?charset=utf8mb4",
        modules={"models": ["callback.models.mysql"]},
    )


async def close_mysql():
    await Tortoise.close_connections()
