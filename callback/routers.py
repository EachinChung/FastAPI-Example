from typing import NoReturn

from fastapi import Depends, FastAPI

from callback.controller import sentry, subscription
from callback.dependency import check_root, check_secret_key


def register_router(app: FastAPI) -> NoReturn:
    app.include_router(
        subscription.router,
        prefix="/subscription",
        tags=["订阅"],
        dependencies=(Depends(check_secret_key),)
    )
    app.include_router(
        sentry.router,
        prefix="/sentry",
        tags=["sentry"],
        dependencies=(Depends(check_secret_key), Depends(check_root))
    )
