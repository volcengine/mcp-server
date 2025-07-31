import os

import volcenginesdkcore
from volcenginesdkecs.api.ecs_api import ECSApi

from mcp_server_ecs.common.auth import get_auth_info
from mcp_server_ecs.common.config import auth_config, deploy_config
from mcp_server_ecs.common.logs import LOG

_ecs_local_client = None


def get_volc_ecs_client(region: str = None) -> ECSApi:
    global _ecs_local_client
    try:
        if deploy_config["is_local"]:
            if _ecs_local_client is None:
                ecs_config = volcenginesdkcore.Configuration()
                ecs_config.ak = (
                    os.environ.get("VOLCENGINE_ACCESS_KEY") or auth_config["ak"]
                )
                ecs_config.sk = (
                    os.environ.get("VOLCENGINE_SECRET_KEY") or auth_config["sk"]
                )
                ecs_config.region = (
                    os.environ.get("VOLCENGINE_REGION") or auth_config["region"]
                )
                ecs_config.host = (
                    os.environ.get("VOLCENGINE_ENDPOINT") or auth_config["endpoint"]
                )
                ecs_config.client_side_validation = True
                volcenginesdkcore.Configuration.set_default(ecs_config)
                _ecs_local_client = ECSApi()

            return _ecs_local_client

        else:
            ak, sk, session_token = get_auth_info()
            ecs_config = volcenginesdkcore.Configuration()
            ecs_config.ak = ak
            ecs_config.sk = sk
            ecs_config.session_token = session_token
            ecs_config.client_side_validation = True
            ecs_config.region = region
            volcenginesdkcore.Configuration.set_default(ecs_config)

            return ECSApi()

    except Exception as e:
        LOG.error(f"Failed to get volc ecs client: {e}")
        raise e
