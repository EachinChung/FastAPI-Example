import copy
import logging
from re import search
from typing import List, Optional

import yaml
from fastapi import Request

from callback.constants.clash import config
from callback.dao import configs, sensitive_logs
from callback.dependency import check_root
from callback.exception import ApiHTTPException
from callback.lib.network import requests
from callback.lib.redis import Cache
from callback.lib.utils import get_unsafe_dict_value


async def match_flag(name: str, proxy_dedicated_hk: List[str], proxy_transit_hk: List[str]) -> str:
    if search(r"AC", name):
        return f"🇦🇨 {name}"
    elif search(r"(AR|阿根廷)", name):
        return f"🇦🇷 {name}"
    elif search(r"(奥地利|维也纳)", name):
        return f"🇦🇹 {name}"
    elif search(r"(AU|Australia|Sydney|澳大利亚|悉尼)", name):
        return f"🇦🇺 {name}"
    elif search(r"BE", name):
        return f"🇧🇪 {name}"
    elif search(r"(BR|Brazil|巴西|圣保罗)", name):
        return f"🇧🇷 {name}"
    elif search(r"(Canada|加拿大|蒙特利尔|温哥华|楓葉|枫叶)", name):
        return f"🇨🇦 {name}"
    elif search(r"(瑞士|苏黎世)", name):
        return f"🇨🇭 {name}"
    elif search(r"(DE|Germany|德国|法兰克福|德)", name):
        return f"🇩🇪 {name}"
    elif search(r"丹麦", name):
        return f"🇩🇰 {name}"
    elif search(r"ES", name):
        return f"🇪🇸 {name}"
    elif search(r"EU", name):
        return f"🇪🇺 {name}"
    elif search(r"(Finland|芬兰|赫尔辛基)", name):
        return f"🇫🇮 {name}"
    elif search(r"(FR|France|法国|巴黎)", name):
        return f"🇫🇷 {name}"
    elif search(r"(UK|England|UnitedKingdom|英国|英|伦敦)", name):
        return f"🇬🇧 {name}"
    elif search(r"(HK|HongKong|香港|深港|沪港|呼港|HKT|HKBN|HGC|WTT|CMI|穗港|京港|港)", name):
        flag_and_name = f"🇭🇰 {name}"
        if "专线" in name:
            proxy_dedicated_hk.append(flag_and_name)
        else:
            proxy_transit_hk.append(flag_and_name)
        return flag_and_name
    elif search(r"(Indonesia|印尼|印度尼西亚|雅加达)", name):
        return f"🇮🇩 {name}"
    elif search(r"(Ireland|爱尔兰|都柏林)", name):
        return f"🇮🇪 {name}"
    elif search(r"(India|印度|孟买)", name):
        return f"🇮🇳 {name}"
    elif search(r"(Italy|意大利|米兰)", name):
        return f"🇮🇹 {name}"
    elif search(r"(JP|Japan|日本|东京|大阪|埼玉|沪日|穗日|川日|中日|泉日|杭日)", name):
        return f"🇯🇵 {name}"
    elif search(r"(KP|朝鲜)", name):
        return f"🇰🇵 {name}"
    elif search(r"(KR|Korea|KOR|韩国|首尔|韩|韓)", name):
        return f"🇰🇷 {name}"
    elif search(r"(MO|Macao|澳门|CTM)", name):
        return f"🇲🇴 {name}"
    elif search(r"(MY|Malaysia|马来西亚)", name):
        return f"🇲🇾 {name}"
    elif search(r"(NL|Netherlands|荷兰|阿姆斯特丹)", name):
        return f"🇳🇱 {name}"
    elif search(r"(PH|Philippines|菲律宾)", name):
        return f"🇵🇭 {name}"
    elif search(r"(RO|罗马尼亚)", name):
        return f"🇷🇴 {name}"
    elif search(r"(RU|Russia|俄罗斯|伯力|莫斯科|圣彼得堡|西伯利亚|新西伯利亚|京俄|杭俄)", name):
        return f"🇷🇺 {name}"
    elif search(r"(沙特|迪拜)", name):
        return f"🇸🇦 {name}"
    elif search(r"(SE|Sweden)", name):
        return f"🇸🇪 {name}"
    elif search(r"(SG|Singapore|新加坡|狮城|沪新|京新|泉新|穗新|深新|杭新)", name):
        return f"🇸🇬 {name}"
    elif search(r"(TH|Thailand|泰国|曼谷)", name):
        return f"🇹🇭 {name}"
    elif search(r"(TR|Turkey|土耳其|伊斯坦布尔)", name):
        return f"🇹🇷 {name}"
    elif search(r"(US|America|UnitedStates|美国|美|京美|波特兰|达拉斯|俄勒冈|凤凰城|费利蒙|硅谷|拉斯维加斯|洛杉矶|圣何塞|圣克拉拉|西雅图|芝加哥|沪美)",
                name):
        return f"🇺🇲 {name}"
    elif search(r"(VN|越南)", name):
        return f"🇻🇳 {name}"
    elif search(r"(ZA|南非)", name):
        return f"🇿🇦 {name}"
    elif search(r"(CN|China|回国|中国|江苏|北京|上海|广州|深圳|杭州|常州|徐州|青岛|宁波|镇江|back|TW|Taiwan|台湾|台北|台中|新北|彰化|CHT|台|HINET)",
                name):
        return f"🇨🇳 {name}"

    logging.error(f"clash 地区匹配失败 -> {name}")
    return name


async def get_clash_url() -> str:
    await check_root()
    result, n3ro_clash = await configs.get_by_key_and_version_to_config("n3ro_clash", 1)
    if not result:
        raise ApiHTTPException(n3ro_clash)
    return n3ro_clash["url"]


async def handle_clash(proxies):
    proxy_name = []
    proxy_dedicated_hk = []
    proxy_transit_hk = []
    for proxy in proxies:
        proxy['name'] = await match_flag(proxy['name'], proxy_dedicated_hk, proxy_transit_hk)
        proxy_name.append(proxy['name'])
    clash = copy.deepcopy(config)
    clash['proxies'] = proxies
    clash['proxy-groups'][0]['proxies'].extend(proxy_name)
    clash['proxy-groups'][1]['proxies'].extend(proxy_name)
    clash['proxy-groups'][2]['proxies'].extend(proxy_dedicated_hk)
    clash['proxy-groups'][3]['proxies'].extend(proxy_transit_hk)
    clash['proxy-groups'][4]['proxies'].extend(proxy_name)
    clash['proxy-groups'][5]['proxies'].extend(proxy_name)
    clash['proxy-groups'][6]['proxies'].extend(proxy_name)
    clash['proxy-groups'][7]['proxies'].extend(proxy_name)
    clash['proxy-groups'][8]['proxies'].extend(proxy_name)
    clash['proxy-groups'][13]['proxies'].extend(proxy_name)
    return clash


async def get_clash_config(clash_url: Optional[str] = None) -> str:
    url = clash_url or await get_clash_url()

    cakey = f"clash:{url}"
    clash_yaml = await Cache.get(cakey)
    if clash_yaml is not None:
        return clash_yaml

    result = await requests.get(url, is_json=False)
    if result == "":
        raise ApiHTTPException(message="供应商返回的订阅信息为空")

    remote_config = yaml.safe_load(result)
    proxies = get_unsafe_dict_value(remote_config, "proxies")

    clash_config = await handle_clash(proxies)
    clash_yaml = yaml.safe_dump(clash_config, allow_unicode=True)
    await Cache.set(cakey, clash_yaml, expire=600)
    return clash_yaml


async def get_clash_subscription(request: Request, clash_url: Optional[str] = None) -> str:
    result = await get_clash_config(clash_url)
    await sensitive_logs.create_by_request_and_behavior(request, {
        "tag": "clash",
        "clash_url": clash_url or await get_clash_url()
    })
    return result
