import asyncio
import json
import logging
from typing import Dict, Any, Optional

import aiohttp
from utils.sign_utils import request, utc_now

logger = logging.getLogger(__name__)

role_name = "ServiceRoleForEMR"

role_trn_format = "trn:iam:{region}:{target_account_id}:role/{role_name}"

region_endpoint_map = {
    "cn-shanghai": "emr-serverless.cn-shanghai.volcengineapi.com",
    "cn-guangzhou": "emr-serverless.cn-guangzhou.volcengineapi.com",
    "cn-beijing": "emr-serverless.cn-beijing.volcengineapi.com",
    "ap-southeast-1": "emr-serverless.ap-southeast-1.volcengineapi.com",
    "cn-beijing-selfdrive": "emr-serverless.cn-beijing-selfdrive.volcengineapi.com",
    "cn-hongkong": "emr-serverless.cn-hongkong.volcengineapi.com",
    "cn-shanghai-autodriving": "emr-serverless.cn-shanghai-autodriving.volcengineapi.com",
}


def list_serverless_jobs(secret_key: str,
                         access_key: str,
                         region: str = "cn-beijing",
                         request_body: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
    """
    获取火山引擎EMR Serverless作业列表（使用sign_utils中的AWS Signature V4签名）

    Args:
        secret_key: 密钥
        access_key: 访问密钥
        region: 区域，默认为cn-beijing
        request_body: 请求体参数

    Returns:
        作业列表的JSON响应数据
    """

    # API端点
    endpoint = region_endpoint_map.get(region)
    if not endpoint:
        logging.error(f"Unsupported region: {region}")
        return None

    api_url = f"https://{endpoint}"

    try:
        response = request(method="POST", date=utc_now(),
                           query={}, header={"Content-Type": "application/json"},
                           ak=access_key, sk=secret_key,
                           action="ListJob", version="2024-03-25",
                           url=api_url, host=endpoint,
                           service="emr_serverless", region=region,
                           content_type="application/json",
                           body=request_body)
        return response
    except aiohttp.ClientError as e:
        logging.error(f"Error requesting EMR Serverless API from {api_url} error: {str(e)}",
                      exc_info=True)
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response from EMR Serverless API {api_url} error: {str(e)}",
                      exc_info=True)
        return None
    except Exception as e:
        logging.error(f"Unknown error occurred while getting EMR Serverless jobs from {api_url} error: {str(e)}",
                      exc_info=True)
        return None


if __name__ == "__main__":
    accountId = "2100075559"
    region = "cn-beijing"
    ak = ""
    sk = ""
    # Spark sql Job
    jobId = "310931377"


    async def main():
        """主异步函数"""
        # Spark sql Job
        job_list = await list_serverless_jobs(access_key=ak, secret_key=sk, region=region)
        print(f"Job list: {job_list}")


    # 运行异步主函数
    asyncio.run(main())
