import logging
from typing import Tuple, Union

import ujson as json

from callback.constants.types import DictOrList
from callback.lib.redis import use_main_rides
from callback.models.mysql import Configs


async def get_by_key_and_version_to_config(key: str, version: int) -> Tuple[bool, Union[str, DictOrList]]:
    redis = use_main_rides()
    cakey = f"config:{key}:version:{version}"
    config = await redis.get(cakey, encoding="utf-8")
    if config is not None:
        return True, json.loads(config)

    config_model = await Configs.filter(key=key, version=version, status=1).first()
    if config_model is None:
        logging.error(f"{key} 不存在")
        return False, "配置不存在"

    config = config_model.config
    await redis.set(cakey, json.dumps(config), expire=7200)
    return True, config
