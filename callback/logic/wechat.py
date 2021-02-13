import logging
from typing import NoReturn

from callback.constants.url import WechatUrl
from callback.dao import configs
from callback.exception import ApiHTTPException
from callback.lib.network import requests
from callback.lib.redis import use_main_rides
from callback.lib.utils import get_unsafe_dict_value


async def get_access_token() -> str:
    redis = use_main_rides()
    cakey = "wechat:access_token"
    access_token = await redis.get(cakey, encoding="utf-8")
    if access_token is not None:
        return access_token

    result, wechat_app_id = await configs.get_by_key_and_version_to_config("wechat_app_id", 1)
    if not result:
        raise ApiHTTPException(wechat_app_id)

    result, wechat_app_secret = await configs.get_by_key_and_version_to_config("wechat_app_secret", 1)
    if not result:
        raise ApiHTTPException(wechat_app_secret)

    result = await requests.get(WechatUrl.access_token.value, params={
        "grant_type": "client_credential",
        "appid": wechat_app_id["app_id"],
        "secret": wechat_app_secret["app_secret"]
    })

    access_token = get_unsafe_dict_value(result, "access_token")
    redis.set(cakey, access_token, expire=7000)
    return access_token


async def send_template_message(open_id: str, template_id: str, data: dict, redirect: str) -> NoReturn:
    result = await requests.post(
        WechatUrl.send_template_message.value,
        params={"access_token": await get_access_token()},
        json={
            "touser": open_id,
            "template_id": template_id,
            "url": redirect,
            "data": data
        }
    )
    if get_unsafe_dict_value(result, "errcode") != 0:
        logging.error(f"微信模版消息推送失败 {result}")
