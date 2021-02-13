import time
from typing import Optional

from pydantic import BaseModel, Field

from callback.constants.types import DictOrList


def set_response(code: str = "0000", message: str = "ok", data: Optional[DictOrList] = None) -> dict:
    """设置返回值

    Args:
        code (str, optional): 状态码. Defaults to "0000".
        message (str, optional): 信息. Defaults to "ok".
        data (Optional[DictOrList], optional): 数据. Defaults to None.

    Returns:
        dict: 返回值
    """
    return {'code': code, 'message': message, 'data': data or {}}


class BaseResponseModel(BaseModel):
    code: str = Field(title="状态码")
    message: str = Field(title="信息")
    data: DictOrList = Field(title="数据")
    now_ts: int = Field(int(time.time()), title="服务器时间")
