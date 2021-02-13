import functools
from os import getenv
from typing import NoReturn, Optional
from urllib import parse

import sentry_sdk
from starlette.types import ASGIApp, Receive, Scope, Send

from callback import Env
from callback.constants.types import Event, Hint
from callback.setting import setting


def register_sentry():
    sentry_sdk.init(
        dsn=setting.sentry_dsn,
        release="callback@1.1.4",
        environment=getenv("ENV", Env.development.value),
        traces_sample_rate=0.2,
    )


class SentryMiddleware(object):
    def __init__(self, app: ASGIApp):
        self.app = app
        self.headers = {}

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> NoReturn:
        hub = sentry_sdk.Hub.current
        with sentry_sdk.Hub(hub) as hub:
            with hub.configure_scope() as sentry_scope:
                processor = functools.partial(self.__event_processor, scope=scope)
                sentry_scope.add_event_processor(processor)

                with sentry_sdk.start_transaction():
                    try:
                        await self.app(scope, receive, send)
                    except Exception as exc:
                        hub.capture_exception(exc)
                        raise exc from None

    # noinspection PyUnusedLocal
    def __event_processor(self, event: Event, hint: Hint, scope: Scope) -> dict:
        if scope["type"] in ("http", "websocket"):
            self.headers = self.__get_headers(scope)
            event["request"] = {
                "url": self.__get_url(scope),
                "method": scope["method"],
                "headers": self.headers,
                "query_string": self.__get_query(scope),
            }
        if scope.get("client"):
            event["request"]["env"] = {"REMOTE_ADDR": self.__get_client_ip(scope)}
        if scope.get("endpoint"):
            event["transaction"] = self.__get_transaction(scope)

        return event

    def __get_url(self, scope: Scope) -> Optional[str]:
        """从ASGI范围中提取URL，但不包括查询字符串。

        Args:
            scope (Scope)

        Returns:
            Optional[str]
        """
        scheme = scope.get("scheme", "http")
        path = scope.get("root_path", "") + scope["path"]

        if host := self.headers.get("host"):
            return "%s://%s%s" % (scheme, host, path)

        if server := scope.get("server"):
            host, port = server
            default_port = {"http": 80, "https": 443, "ws": 80, "wss": 443}[scheme]
            if port != default_port:
                return "%s://%s:%s%s" % (scheme, host, port, path)
            return "%s://%s%s" % (scheme, host, path)
        return path

    @staticmethod
    def __get_query(scope: Scope) -> str:
        """以Sentry协议期望的格式从ASGI范围提取查询字符串。

        Args:
            scope (Scope)

        Returns:
            str
        """
        return parse.unquote(scope["query_string"].decode("latin-1"))

    @staticmethod
    def __get_headers(scope: Scope) -> dict:
        """以Sentry协议期望的格式从ASGI范围提取标头。

        Args:
            scope (Scope)

        Returns:
            dict
        """
        headers = {}
        for raw_key, raw_value in scope["headers"]:
            key = raw_key.decode("latin-1")
            value = raw_value.decode("latin-1")
            if key in headers:
                headers[key] = headers[key] + ", " + value
            else:
                headers[key] = value
        return headers

    @staticmethod
    def __get_transaction(scope: Scope) -> Optional[str]:
        """返回事务字符串以标识路由的端点。

        Args:
            scope (Scope)

        Returns:
            Optional[str]
        """
        endpoint = scope["endpoint"]
        qualname = (
                getattr(endpoint, "__qualname__", None)
                or getattr(endpoint, "__name__", None)
                or None
        )
        if not qualname:
            return None
        return "%s.%s" % (endpoint.__module__, qualname)

    def __get_client_ip(self, scope: Scope) -> Optional[str]:
        """获取客户端的ip

        Args:
            scope (Scope)

        Returns:
            Optional[str]
        """
        if x_forwarded_for := self.headers.get('x-forwarded-for'):
            return x_forwarded_for.split(", ", 1)[0]

        if x_real_ip := self.headers.get('x-real-ip'):
            return x_real_ip

        if client := scope.get("client"):
            return client[0]
