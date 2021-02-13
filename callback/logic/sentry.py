from callback.dao import configs
from callback.exception import ApiHTTPException
from callback.lib.utils import datetime_format
from callback.logic import wechat
from callback.models.request.sentry import SentryServerChenPostModel


async def send_wechat_template_message(body: SentryServerChenPostModel):
    result, sentry_wechat_push_users = await configs.get_by_key_and_version_to_config("sentry_wechat_push_users", 1)
    if not result:
        raise ApiHTTPException(sentry_wechat_push_users)

    result, sentry_wechat_template_id = await configs.get_by_key_and_version_to_config("sentry_wechat_template_id", 1)
    if not result:
        raise ApiHTTPException(sentry_wechat_template_id)

    template_id = sentry_wechat_template_id['template_id']
    data = {
        "first": {
            "value": body.event.title,
        },
        "keyword1": {
            "value": body.project,
        },
        "keyword2": {
            "value": body.level,
            "color": "#F56C6C"
        },
        "keyword3": {
            "value": body.culprit,
        },
        "keyword4": {
            "value": datetime_format(body.event.timestamp),
        },
        "remark": {
            "value": "👉👉👉 快去 Sentry 拯救一下",
        }
    }

    for user in sentry_wechat_push_users:
        await wechat.send_template_message(user, template_id, data, body.url)
