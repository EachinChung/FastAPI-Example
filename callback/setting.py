from os import getenv

import ujson as json
from pydantic import BaseModel

from callback import Env


class MySQL(BaseModel):
    host: str
    user: str
    password: str
    port: int
    database: str


class Redis(BaseModel):
    host: str
    main_db: int
    default_db: int


class Setting(BaseModel):
    sentry_dsn: str
    mysql: MySQL
    redis: Redis


def register_setting(config_name: str) -> Setting:
    with open(f"config/{config_name}.json") as file:
        config = Setting(**json.load(file))
    return config


setting = register_setting(getenv("ENV", Env.development))
