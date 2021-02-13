from typing import Optional

from fastapi import APIRouter, Query, Request
from fastapi.responses import PlainTextResponse
from pydantic import HttpUrl

from callback import logic

router = APIRouter()


@router.get("/clash", summary="clash订阅", description="自动分流，全局广告拦截",
            response_description="请求成功，返回配置文件", response_class=PlainTextResponse)
async def clash(
        request: Request,
        clash_url: Optional[HttpUrl] = Query(None, alias="clashUrl", description="clash 订阅链接")
):
    result = await logic.get_clash_subscription(request, clash_url)
    return result


@router.get("/ssr", summary="ssr订阅", description="所有SSR节点",
            response_description="请求成功，返回配置信息", response_class=PlainTextResponse)
async def ssr():
    result = await logic.get_ssr_subscription()
    return result


@router.get("/ssr/hk", summary="ssr订阅，HK节点", description="香港中继SSR节点",
            response_description="请求成功，返回配置信息", response_class=PlainTextResponse)
async def ssr_hk():
    result = await logic.SsrHK().execute()
    return result
