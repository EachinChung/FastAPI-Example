from typing import Tuple, Union

from callback.lib.redis import Cache
from callback.models.mysql import Users


async def get_by_id(user_id: int) -> Tuple[bool, Union[Users, str]]:
    cakey = f"user:{user_id}"
    user = await Cache.get(cakey)
    if user is not None:
        return True, user

    user = await Users.filter(id=user_id, status=1).first()
    if user is None:
        return False, "用户不存在"

    await Cache.set(cakey, user, expire=600)
    return True, user
