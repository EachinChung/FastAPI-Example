from fastapi import APIRouter

from callback import logic
from callback.lib.responses import BaseResponseModel, set_response
from callback.models.request.sentry import SentryServerChenPostModel

router = APIRouter()


@router.post(
    "/notice/wechat/template",
    summary="微信模版通知",
    description="通过 sentry 的 webhooks，拿到数据，通知微信",
    response_model=BaseResponseModel)
async def server_chen(body: SentryServerChenPostModel):
    await logic.send_wechat_template_message(body)
    return set_response()
