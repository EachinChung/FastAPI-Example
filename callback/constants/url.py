from callback.constants.enum import StrEnum


class WechatUrl(StrEnum):
    access_token = "https://api.weixin.qq.com/cgi-bin/token"
    send_template_message = "https://api.weixin.qq.com/cgi-bin/message/template/send"
