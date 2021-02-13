from typing import Tuple, Union

from callback.lib.redis import use_main_rides
from callback.models.mysql import SecretKeys


async def get_by_secret_key_to_user_id(secret_key: str) -> Tuple[bool, Union[int, str]]:
    redis = use_main_rides()
    cakey = f"secret_keys:{secret_key}"
    user_id = await redis.get(cakey, encoding="utf-8")
    if user_id is not None:
        return True, int(user_id)

    user_id = await SecretKeys.filter(secret_key=secret_key).first()
    if user_id is None:
        return False, "密钥不正确或不存在"

    await redis.set(cakey, user_id.user_id, expire=7200)
    return True, user_id.user_id
