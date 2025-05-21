import logging
from typing import List, Optional

from mcp_server_tos.resources.service import TosResource

from mcp_server_tos.config import TosConfig

logger = logging.getLogger(__name__)


class BucketResource(TosResource):
    """
        火山引擎TOS Bucket资源类
    """

    def __init__(self, config: TosConfig):
        super(BucketResource, self).__init__(config)

    async def list_buckets(self) -> List[dict]:
        """
        调用 ListBuckets 接口列举桶
        api: https://www.volcengine.com/docs/6349/74850
        """
        if self.configured_buckets:
            resp = await self.get(bucket="")
            configured_bucket_list = [
                bucket for bucket in resp.json().get("buckets", [])
                if bucket['Name'] in self.configured_buckets
            ]
            return configured_bucket_list
        else:
            resp = await self.get(bucket="")
            if resp.status_code == 200:
                return resp.json().get("Buckets", [])
            else:
                raise Exception(f"list buckets failed, tos server return: {resp.json()}")

    async def list_objects(self, bucket: str, prefix: Optional[str] = None, start_after: Optional[str] = None,
                           continuation_token: Optional[str] = None) -> str:
        """
        调用 ListObjects 接口列举桶
        api: https://www.volcengine.com/docs/6349/357812
        Args:
            bucket: 桶名
            prefix: 对象前缀
            start_after: 起始位置
            continuation_token: 分页标记
        """

        query = {"list-type": "2"}
        if prefix:
            query["prefix"] = prefix
        if start_after:
            query["start-after"] = start_after
        if continuation_token:
            query["continuation-token"] = continuation_token

        resp = await self.get(bucket=bucket, params=query)
        if resp.status_code == 200:
            return resp.json()
        else:
            raise Exception(f"list objects failed, tos server return: {resp.json()}")
