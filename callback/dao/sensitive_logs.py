from typing import NoReturn

from fastapi import Request

from callback.constants.types import DictOrList
from callback.ctx import CTX_USER
from callback.lib.requests import get_client_ip
from callback.models.mysql import SensitiveLogs


async def create_by_request_and_behavior(request: Request, behavior: DictOrList) -> NoReturn:
    user = CTX_USER.get()
    sensitive_log = SensitiveLogs()
    sensitive_log.user_id = user.id
    sensitive_log.ip = get_client_ip(request)
    sensitive_log.ua = request.headers.get("user-agent")
    sensitive_log.url = request.scope.get("path")
    sensitive_log.method = request.method
    sensitive_log.behavior = behavior
    await sensitive_log.save()
