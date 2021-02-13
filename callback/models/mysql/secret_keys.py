from tortoise import fields

from callback.models.mysql.base import BaseModel, DatetimeMixin


class SecretKeys(BaseModel, DatetimeMixin):
    user_id = fields.IntField(index=True, null=False)
    secret_key = fields.CharField(32, unique=True, index=True, null=False)

    class Meta:
        table = "secret_keys"
