from tortoise import fields

from callback.models.mysql.base import BaseModel, DatetimeMixin, ExtentMixin
from callback.models.mysql.base import StatusMixin


class Users(BaseModel, StatusMixin, ExtentMixin, DatetimeMixin):
    phone = fields.CharField(32, unique=True, index=True, null=False)
    country = fields.IntField(index=True, null=False)
    username = fields.CharField(32, unique=True, index=True, null=False)
    is_root = fields.BooleanField(null=False, default=False)

    class Meta:
        table = "users"
