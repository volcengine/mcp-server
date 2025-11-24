import json
import logging
import os
from typing import Dict, Any, List

import aiohttp

from server.mcp_server_emr.src.mcp_server_emr.utils.sign_utils import request, utc_now

logger = logging.getLogger(__name__)

region_endpoint_map = {
    "cn-shanghai": "emr.cn-shanghai.volcengineapi.com",
    "cn-guangzhou": "emr.cn-guangzhou.volcengineapi.com",
    "cn-beijing": "emr.cn-beijing.volcengineapi.com",
    "ap-southeast-1": "emr.ap-southeast-1.volcengineapi.com",
    "cn-beijing-selfdrive": "emr.cn-beijing-selfdrive.volcengineapi.com",
    "cn-beijing-autodriving": "emr.cn-beijing-autodriving.volcengineapi.com",
    "cn-shanghai-autodriving": "emr.cn-shanghai-autodriving.volcengineapi.com",
}


def list_virtual_clusters(
        access_key: str,
        secret_key: str,
        region: str,
        page_size: int = 20) -> List[Dict[str, Any]]:
    """
    获取 EMR on VKE 形态的虚拟集群列表信息

    Args:
        access_key: 火山引擎AccessKey
        secret_key: 火山引擎SecretKey
        region: 火山引擎Region
        page_size: 每页数量, 默认 20
    """

    # API端点
    endpoint = region_endpoint_map.get(region)
    if not endpoint:
        logging.error(f"Unsupported region: {region}")
        return []

    api_url = f"https://{endpoint}"
    states = ["INIT", "INIT_FAILED", "RUNNING", "CHANGING", "EXCEPTION", "DELETING", "STOPPED", "RECOVERING", "DELETED"]
    try:
        response = request(method="POST", date=utc_now(),
                           query={}, header={"Content-Type": "application/json"},
                           ak=access_key, sk=secret_key,
                           action="ListVirtualClusters", version="2024-06-13",
                           url=api_url, host=endpoint,
                           service="emr", region=region,
                           content_type="application/json",
                           body=json.dumps({"MaxResults": page_size, "ClusterStates": states}))
        if response.get("ResponseMetadata", {}).get("Error", None):
            logging.error(
                f"Error requesting EMR API from {api_url} error, error: {response.get("ResponseMetadata", {}).get("Error")}")
            return []
        elif response.get("Result", {}).get("Items", None):
            return response.get("Result", {}).get("Items")
        else:
            logging.error(
                f"Error requesting EMR API from {api_url} error, response: {response}")
            return []

    except aiohttp.ClientError as e:
        logging.error(f"Error requesting EMR API from {api_url} error: {str(e)}",
                      exc_info=True)
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response from EMR API {api_url} error: {str(e)}",
                      exc_info=True)
        return []
    except Exception as e:
        logging.error(
            f"Unknown error occurred while getting EMR on VKE virtual clusters from {api_url} error: {str(e)}",
            exc_info=True)
        return []


if __name__ == "__main__":
    cluster_list = list_virtual_clusters(access_key=os.getenv("VOLCENGINE_ACCESS_KEY"),
                                         secret_key=os.getenv("VOLCENGINE_SECRET_KEY"),
                                         region=os.getenv("VOLCENGINE_REGION"))
    print(f"Virtual cluster list: {cluster_list}")
