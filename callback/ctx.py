import contextvars
from typing import Optional

from callback.models.mysql import Users

CTX_USER: contextvars.ContextVar[Optional[Users]] = contextvars.ContextVar('user', default=None)
