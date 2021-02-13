import pickle
from typing import Any, NoReturn

from aioredis import create_redis_pool

from callback.lib.utils import GetSetTer
from callback.setting import setting

redis = GetSetTer()


async def register_redis():
    redis.main = await create_redis_pool(f"redis://{setting.redis.host}/{setting.redis.main_db}")
    redis.value = await create_redis_pool(f"redis://{setting.redis.host}/{setting.redis.default_db}")


# noinspection PyUnresolvedReferences
async def close_redis():
    redis.main.close()
    redis.value.close()


class Cache:

    # noinspection SpellCheckingInspection,PyTypeChecker
    @classmethod
    async def set(cls, key: str, value: Any, expire: int = 600) -> NoReturn:
        value = pickle.dumps(value)
        await redis.value.set(key, value, expire=expire)

    @classmethod
    async def get(cls, key: str) -> Any:
        value = await redis.value.get(key)
        if value is None:
            return None
        value = pickle.loads(value)
        return value
