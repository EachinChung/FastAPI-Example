import pickle
from typing import Any, NoReturn

from aioredis import Redis, create_redis_pool

from callback.lib.utils import GetSetTer
from callback.setting import setting

redis_pool = GetSetTer()


async def register_redis():
    redis_pool.main = await create_redis_pool(f"redis://{setting.redis_pool.host}/{setting.redis_pool.main_db}")
    redis_pool.value = await create_redis_pool(f"redis://{setting.redis_pool.host}/{setting.redis_pool.default_db}")


# noinspection PyUnresolvedReferences
async def close_redis():
    redis_pool.main.close()
    redis_pool.value.close()
    await redis_pool.main.wait_closed()
    await redis_pool.value.wait_closed()


# noinspection PyUnresolvedReferences
def use_main_rides() -> Redis:
    return redis_pool.main


def use_default_rides() -> Redis:
    return redis_pool.value


class Cache:

    # noinspection SpellCheckingInspection,PyTypeChecker
    @classmethod
    async def set(cls, key: str, value: Any, expire: int = 600) -> NoReturn:
        value = pickle.dumps(value)
        await redis_pool.value.set(key, value, expire=expire)

    @classmethod
    async def get(cls, key: str) -> Any:
        value = await redis_pool.value.get(key)
        if value is None:
            return None
        value = pickle.loads(value)
        return value
