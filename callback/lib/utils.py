import datetime
import logging
from base64 import urlsafe_b64decode
from typing import Any

from pytz import timezone

from callback.constants.error_code import Error
from callback.constants.types import IntOrStr
from callback.exception import ApiHTTPException


def datetime_format(the_datetime: datetime.datetime, include_time: bool = True) -> str:
    if include_time:
        fmt = '%Y-%m-%d %H:%M:%S'
    else:
        fmt = '%Y-%m-%d'

    return the_datetime.astimezone(timezone('Asia/Shanghai')).strftime(fmt)


def safe_base64_decode(s: str) -> str:
    """安全的解码base64

    Args:
        s (str): base64 字符串

    Returns:
        str: 解码后的内容
    """
    if len(s) % 4 != 0:
        s = s + "=" * (4 - len(s) % 4)

    if not isinstance(s, bytes):
        s = bytes(s, encoding="utf-8")

    base64_str = urlsafe_b64decode(s)
    return base64_str.decode("utf-8")


def get_unsafe_dict_value(unsafe_dict: dict, key: IntOrStr) -> Any:
    """获取不安全的字典的值

    Args:
        unsafe_dict (dict): 不安全的字典
        key (IntOrStr)

    Raises:
        ApiHTTPException: 抛出网络异常

    Returns:
        Any: value
    """
    try:
        return unsafe_dict[key]
    except Exception as e:
        logging.exception(e)
        code, message = Error.request_error.unpack()
        raise ApiHTTPException(message=message, code=code)


def get_pyobject_type(pyobject: Any) -> str:
    """获取python对象的名字

    Args:
        pyobject (Any): python对象

    Returns:
        str: 对象类型
    """
    return pyobject.__class__.__name__


class GetSetTer(object):
    def __init__(self):
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, _value):
        self.__value = _value

    @value.deleter
    def value(self):
        del self.__value
