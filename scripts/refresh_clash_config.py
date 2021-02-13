import asyncio
import os
import sys

import yaml
from pydantic import BaseModel, Field

sys.path.append(os.path.join(os.path.dirname(os.getcwd()), "callback"))

from callback.lib.network import close_requests, register_requests, requests


class ClashConfig(BaseModel):
    mixed_port: int = Field(7890, alias="mixed-port")
    external_controller: str = Field("127.0.0.1:9090", alias="external-controller")
    allow_lan: bool = Field(False, alias="allow-lan")
    log_level: str = Field("warning", alias="log-level")
    proxy_groups: list = Field(alias="proxy-groups")
    mode: str = "rule"
    proxies: list
    rules: list


async def get_config():
    return await requests.get("https://subcon.dlj.tf/sub", is_json=False, params={
        "target": "clash",
        "new_name": "true",
        "url": "https://cdn.eachin-life.com/ssr.txt",
        "insert": "false",
        "config": "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_AdblockPlus.ini"
    })


async def save_config(config: dict):
    with open("callback/constants/clash.py", "w") as file:
        file.write(f"config = {config}")


async def refresh_clash_config():
    result = await get_config()
    config = yaml.safe_load(result)
    config = ClashConfig(**config)
    config.proxies = []
    config.proxy_groups = [
        {
            'name': '🚀 节点选择',
            'type': 'select',
            'proxies': ['🇭🇰 香港专线', '🇭🇰 香港中继', '♻️ 自动选择', 'DIRECT', ]
        },
        {
            'name': '♻️ 自动选择',
            'type': 'url-test',
            'url': 'http://www.gstatic.com/generate_204',
            'interval': 300,
            'tolerance': 50,
            'proxies': []
        },
        {
            'name': '🇭🇰 香港专线',
            'type': 'url-test',
            'url': 'http://www.gstatic.com/generate_204',
            'interval': 300,
            'tolerance': 50,
            'proxies': []
        },
        {
            'name': '🇭🇰 香港中继',
            'type': 'url-test',
            'url': 'http://www.gstatic.com/generate_204',
            'interval': 300,
            'tolerance': 50,
            'proxies': []
        },
        {
            'name': '🌍 国外媒体',
            'type': 'select',
            'proxies': ['🇭🇰 香港专线', '🇭🇰 香港中继', '🚀 节点选择', '🎯 全球直连', ]
        },
        {
            'name': '📢 谷歌FCM',
            'type': 'select',
            'proxies': ['🇭🇰 香港专线', '🇭🇰 香港中继', '🚀 节点选择', '🎯 全球直连', ]
        },
        {
            'name': '📲 电报信息',
            'type': 'select',
            'proxies': ['🇭🇰 香港专线', '🇭🇰 香港中继', '🚀 节点选择', '🎯 全球直连', ]
        },
        {
            'name': 'Ⓜ️ 微软服务',
            'type': 'select',
            'proxies': ['🎯 全球直连', '🇭🇰 香港专线', '🇭🇰 香港中继', '🚀 节点选择', ]
        },
        {
            'name': '🍎 苹果服务',
            'type': 'select',
            'proxies': ['🎯 全球直连', '🇭🇰 香港专线', '🇭🇰 香港中继', '🚀 节点选择', ]
        },
        {
            'name': '🎯 全球直连',
            'type': 'select',
            'proxies': ['DIRECT', '🚀 节点选择', ]
        },
        {
            'name': '🛑 全球拦截',
            'type': 'select',
            'proxies': ['REJECT', 'DIRECT']
        },
        {
            'name': '🍃 应用净化',
            'type': 'select',
            'proxies': ['REJECT', 'DIRECT']
        },
        {
            'name': '🆎 AdBlock',
            'type': 'select',
            'proxies': ['REJECT', 'DIRECT']
        },
        {
            'name': '🐟 漏网之鱼',
            'type': 'select',
            'proxies': ['🚀 节点选择', '🎯 全球直连']
        }
    ]
    await save_config(config.dict(by_alias=True))


async def run():
    await register_requests()
    await refresh_clash_config()
    await close_requests()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
