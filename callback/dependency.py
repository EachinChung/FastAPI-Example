import sentry_sdk
from fastapi import Query, status

from callback.constants.error_code import Error
from callback.ctx import CTX_USER
from callback.dao import secret_keys, users
from callback.exception import ApiHTTPException


async def check_secret_key(
        secret_key: str = Query(..., min_length=1, max_length=32, alias="secretKey", description="密钥")):
    result, user_id = await secret_keys.get_by_secret_key_to_user_id(secret_key)
    if not result:
        code, message = Error.secret_key_error.unpack()
        raise ApiHTTPException(message=message, code=code, status_code=status.HTTP_401_UNAUTHORIZED)

    result, user = await users.get_by_id(user_id)
    if not result:
        code, message = Error.secret_key_error.unpack()
        raise ApiHTTPException(message=message, code=code, status_code=status.HTTP_401_UNAUTHORIZED)

    sentry_sdk.set_user({
        "id": user.id,
        "phone": user.phone,
        "username": user.username,
    })
    CTX_USER.set(user)


async def check_root():
    user = CTX_USER.get()
    if not user.is_root:
        code, message = Error.forbidden_error.unpack()
        raise ApiHTTPException(message=message, code=code, status_code=status.HTTP_403_FORBIDDEN)
