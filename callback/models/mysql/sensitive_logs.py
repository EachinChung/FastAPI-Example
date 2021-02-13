import ujson as json
from tortoise import fields

from callback.models.mysql.base import BaseModel


class SensitiveLogs(BaseModel):
    user_id = fields.IntField(index=True, null=False)
    ip = fields.CharField(32, index=True, null=False)
    ua = fields.CharField(512, null=False)
    url = fields.CharField(256, null=False)
    method = fields.CharField(16, index=True, null=False)
    behavior = fields.JSONField(encoder=json.dumps, decoder=json.loads, null=False)
    create_at = fields.DatetimeField(null=False, auto_now_add=True)

    class Meta:
        table = "sensitive_logs"
