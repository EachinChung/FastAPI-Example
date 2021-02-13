import ujson as json
from tortoise import fields

from callback.models.mysql.base import BaseModel, DatetimeMixin, StatusMixin


class Configs(BaseModel, DatetimeMixin, StatusMixin):
    key = fields.CharField(64, unique=True, index=True, null=False)
    version = fields.IntField(index=True, null=False)
    config = fields.JSONField(encoder=json.dumps, decoder=json.loads, null=False)

    class Meta:
        table = "configs"
