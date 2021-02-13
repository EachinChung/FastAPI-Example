from datetime import datetime

from pydantic import BaseModel, Field


class SentryServerChenEvent(BaseModel):
    event_id: str = Field(title="监听ID")
    platform: str = Field(title="平台")
    timestamp: datetime = Field(title="时间戳")
    title: str = Field(title="标题")


class SentryServerChenPostModel(BaseModel):
    id: int
    project: str = Field(title="项目")
    project_name: str = Field(title="项目名")
    level: str = Field(title="Sentry 级别")
    culprit: str = Field(title="Sentry 罪魁祸首")
    message: str = Field(title="Sentry 信息")
    url: str = Field(title="Sentry 错误地址")
    event: SentryServerChenEvent = Field(title="监听")
