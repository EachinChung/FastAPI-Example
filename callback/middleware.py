from typing import NoReturn

from fastapi import FastAPI

from callback.lib.sentry import SentryMiddleware


def register_middleware(app: FastAPI) -> NoReturn:
    """安装中间价，越晚调用越先进入

    Args:
        app (FastAPI)

    Returns:
        NoReturn
    """
    app.add_middleware(SentryMiddleware)
