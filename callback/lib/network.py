import asyncio
import logging
from typing import Mapping, Optional

import aiohttp
import ujson
from aiohttp import ClientSession, ClientTimeout
from aiohttp.typedefs import LooseHeaders

from callback.constants.error_code import Error
from callback.constants.method import Method
from callback.constants.request import REQUEST_LIMIT_PER_HOST, REQUEST_TIMEOUT
from callback.constants.types import AioHttpResponse
from callback.exception import ApiHTTPException
from callback.lib.utils import GetSetTer

pool = GetSetTer()


async def register_requests():
    pool.value = aiohttp.TCPConnector(
        limit_per_host=REQUEST_LIMIT_PER_HOST,
        keepalive_timeout=15,
        force_close=False,
    )


async def close_requests():
    await pool.value.close()


class RequestsTool:
    @staticmethod
    async def __requests(method: str, is_json: bool = False, *args, **kwargs) -> AioHttpResponse:
        """异步发送网络请求
        Args:
            method (str): 请求方法
            is_json (bool, optional): 返回格式是否为json. Defaults to False.
        Returns:
            Tuple[bool, Union[dict, str]]: 返回的数据
        """
        try:
            async with ClientSession(
                    connector=pool.value,
                    timeout=ClientTimeout(total=REQUEST_TIMEOUT),
                    connector_owner=False,
            ) as session:
                async with getattr(session, method)(*args, **kwargs) as response:
                    content = await response.text()
                    return ujson.loads(content) if is_json else content

        except asyncio.TimeoutError:
            code, message = Error.timeout_error.unpack()
            raise ApiHTTPException(message=message, code=code)

        except Exception as e:
            logging.exception(e)
            code, message = Error.request_error.unpack()
            raise ApiHTTPException(message=message, code=code)

    async def get(
            self,
            url: str,
            params: Optional[Mapping[str, str]] = None,
            data: Optional[dict] = None,
            json: Optional[dict] = None,
            headers: Optional[LooseHeaders] = None,
            is_json: Optional[bool] = True,
            *args, **kwargs
    ) -> AioHttpResponse:
        return await self.__requests(
            Method.get, is_json, url, params=params,
            data=data, json=json, headers=headers, *args, **kwargs
        )

    async def post(
            self,
            url: str,
            params: Optional[Mapping[str, str]] = None,
            data: Optional[dict] = None,
            json: Optional[dict] = None,
            headers: Optional[LooseHeaders] = None,
            is_json: Optional[bool] = True,
            *args, **kwargs
    ) -> AioHttpResponse:
        return await self.__requests(
            Method.post, is_json, url, params=params,
            data=data, json=json, headers=headers, *args, **kwargs
        )

    async def put(
            self,
            url: str,
            params: Optional[Mapping[str, str]] = None,
            data: Optional[dict] = None,
            json: Optional[dict] = None,
            headers: Optional[LooseHeaders] = None,
            is_json: Optional[bool] = True,
            *args, **kwargs
    ) -> AioHttpResponse:
        return await self.__requests(
            Method.put, is_json, url, params=params,
            data=data, json=json, headers=headers, *args, **kwargs
        )

    async def patch(
            self,
            url: str,
            params: Optional[Mapping[str, str]] = None,
            data: Optional[dict] = None,
            json: Optional[dict] = None,
            headers: Optional[LooseHeaders] = None,
            is_json: Optional[bool] = True,
            *args, **kwargs
    ) -> AioHttpResponse:
        return await self.__requests(
            Method.patch, is_json, url, params=params,
            data=data, json=json, headers=headers, *args, **kwargs
        )

    async def delete(
            self,
            url: str,
            params: Optional[Mapping[str, str]] = None,
            data: Optional[dict] = None,
            json: Optional[dict] = None,
            headers: Optional[LooseHeaders] = None,
            is_json: Optional[bool] = True,
            *args, **kwargs
    ) -> AioHttpResponse:
        return await self.__requests(
            Method.delete, is_json, url, params=params,
            data=data, json=json, headers=headers, *args, **kwargs
        )


requests = RequestsTool()
