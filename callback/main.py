from typing import NoReturn

from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from callback.exception import register_global_exception
from callback.lib.mysql import close_mysql, register_mysql
from callback.lib.network import close_requests, register_requests
from callback.lib.redis import close_redis, register_redis
from callback.lib.sentry import register_sentry
from callback.middleware import register_middleware
from callback.routers import register_router
from callback.setting import setting


def create_app() -> FastAPI:
    app = FastAPI(
        title="回调系统",
        description="基于**Python**的回调系统",
        version=setting.version,
        docs_url=setting.docs_url,
        redoc_url=setting.redoc_url,
        default_response_class=UJSONResponse
    )

    register_sentry()
    register_global_exception(app)
    register_middleware(app)
    register_event(app)
    register_mysql(app)
    register_router(app)
    return app


def register_event(app: FastAPI) -> NoReturn:
    @app.on_event("startup")
    async def startup_event():
        await register_requests()
        await register_redis()

    @app.on_event('shutdown')
    async def shutdown_event():
        await close_requests()
        await close_redis()
        await close_mysql()
