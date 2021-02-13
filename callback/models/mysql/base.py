import ujson as json
from tortoise import Model, fields


class StatusMixin(object):
    status = fields.IntField(null=True, default=1)


class ExtentMixin(object):
    json_extent = fields.JSONField(encoder=json.dumps, decoder=json.loads, null=True)


class DatetimeMixin(object):
    create_at = fields.DatetimeField(null=False, auto_now_add=True)
    modified_at = fields.DatetimeField(null=False, auto_now=True)


class BaseModel(Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True
