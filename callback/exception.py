import logging
import time
from typing import NoReturn, Optional

from fastapi import FastAPI, Request, status
from fastapi.responses import UJSONResponse

from callback.constants.error_code import Error
from callback.constants.types import DictOrList


class ApiHTTPException(Exception):
    def __init__(
            self,
            message: str,
            *,
            code: str = "4000",
            data: Optional[DictOrList] = None,
            status_code: int = status.HTTP_400_BAD_REQUEST
    ):
        self.code = code
        self.message = message
        self.data = data or {}
        self.status_code = status_code


async def api_http_exception_handler(request: Request, exc: ApiHTTPException) -> UJSONResponse:
    """处理自定义的api错误

    Args:
        request (Request)
        exc (ApiHTTPException)

    Returns:
        UJSONResponse
    """

    return UJSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "message": exc.message,
            "data": exc.data,
            "now_ts": int(time.time())
        },
    )


async def exception_handler(request: Request, exc: Exception) -> UJSONResponse:
    """处理全局错误

    Args:
        request (Request)
        exc (Exception)

    Returns:
        UJSONResponse
    """
    logging.exception(exc)
    code, message = Error.inter_error.unpack()
    return UJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": code,
            "message": message,
            "data": {},
            "now_ts": int(time.time())
        },
    )


def register_global_exception(app: FastAPI) -> NoReturn:
    app.add_exception_handler(Exception, exception_handler)
    app.add_exception_handler(ApiHTTPException, api_http_exception_handler)
