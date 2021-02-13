from base64 import urlsafe_b64encode
from re import findall
from typing import NoReturn

from callback.dao import configs
from callback.dependency import check_root
from callback.exception import ApiHTTPException
from callback.lib.network import requests
from callback.lib.utils import safe_base64_decode


async def get_ssr_subscription() -> str:
    await check_root()
    result, n3ro_ssr = await configs.get_by_key_and_version_to_config("n3ro_ssr", 1)
    if not result:
        raise ApiHTTPException(n3ro_ssr)

    result = await requests.get(n3ro_ssr["url"], is_json=False)
    return result


class SsrHK(object):
    def __init__(self):
        self.ssr_list = []

    async def get_ssr_list(self) -> NoReturn:
        result = await get_ssr_subscription()
        ssr_list = safe_base64_decode(result)
        self.ssr_list = ssr_list.split()

    @staticmethod
    def filter(ssr: str) -> bool:
        data = safe_base64_decode(ssr[6:])
        ssr_name = safe_base64_decode(findall(r"remarks=(.+)&group", data)[0])
        return "香港" in ssr_name and "专线" in ssr_name

    async def execute(self) -> urlsafe_b64encode:
        await self.get_ssr_list()
        return urlsafe_b64encode("\n".join(filter(self.filter, self.ssr_list)).encode("utf-8"))
