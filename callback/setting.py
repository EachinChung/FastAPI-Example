import ujson as json
from pydantic import BaseModel

from callback.constants.enum import StrEnum


class Env(StrEnum):
    development = "development"
    production = "production"


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
    version: str
    env: Env
    docs_url: str
    redoc_url: str
    sentry_dsn: str
    mysql: MySQL
    redis: Redis


def register_setting() -> Setting:
    with open(f"config.json") as file:
        config = Setting(**json.load(file))
    return config


setting = register_setting()
