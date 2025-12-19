import json
import logging
import os
from typing import Dict, Any, List

import aiohttp

from mcp_server_emr.utils.sign_utils import request
from mcp_server_emr.utils.sign_utils import utc_now


logger = logging.getLogger(__name__)

region_endpoint_map = {
    "cn-shanghai": "emr.cn-shanghai.volcengineapi.com",
    "cn-guangzhou": "emr.cn-guangzhou.volcengineapi.com",
    "cn-beijing": "emr.cn-beijing.volcengineapi.com",
    "ap-southeast-1": "emr.ap-southeast-1.volcengineapi.com",
    "cn-beijing-selfdrive": "emr.cn-beijing-selfdrive.volcengineapi.com",
    "cn-hongkong": "emr.cn-hongkong.volcengineapi.com",
    "cn-shanghai-autodriving": "emr.cn-shanghai-autodriving.volcengineapi.com",
}


def list_clusters(
        access_key: str,
        secret_key: str,
        region: str,
        page_size: int = 20) -> List[Dict[str, Any]]:
    """
    获取 EMR on ECS 形态的集群列表信息

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
    states = ["CREATING", "FAILED", "TERMINATED_WITH_ERROR",
              "RUNNING", "EXCEPTION", "WARNING", "PAUSED", "PAUSING", "RESTORING", "SHUTDOWN", "TERMINATING",
              "PENDING_FOR_PAYMENT"]
    try:
        response = request(method="POST", date=utc_now(),
                           query={}, header={"Content-Type": "application/json"},
                           ak=access_key, sk=secret_key,
                           action="ListClusters", version="2023-08-15",
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
        logging.error(f"Unknown error occurred while getting EMR on ecs clusters from {api_url} error: {str(e)}",
                      exc_info=True)
        return []


if __name__ == "__main__":
    job_list = list_clusters(os.getenv("VOLCENGINE_ACCESS_KEY"), os.getenv("VOLCENGINE_SECRET_KEY"), os.getenv("VOLCENGINE_REGION", "cn-beijing"),)
    print(f"Cluster list: {job_list}")
