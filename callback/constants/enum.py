from enum import Enum


class StrEnum(str, Enum):
    pass


class Env(StrEnum):
    development = "development"
    production = "production"
