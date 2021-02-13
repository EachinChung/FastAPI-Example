from enum import unique

from callback.constants.enum import StrEnum


@unique
class Method(StrEnum):
    get = "get"
    post = "post"
    put = "put"
    patch = "patch"
    delete = "delete"
