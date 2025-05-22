import base64
import logging

from mcp_server_tos.config import TosConfig
from mcp_server_tos.resources.service import TosResource

logger = logging.getLogger(__name__)


class ObjectResource(TosResource):
    """
        火山引擎TOS 对象资源操作类
    """

    def __init__(self, config: TosConfig):
        super(ObjectResource, self).__init__(config)
        self.max_object_size = config.max_object_size

    async def get_object(self, bucket_name: str, key: str) -> str:
        """
        调用 TOS GetObject 接口获取对象内容
        api: https://www.volcengine.com/docs/6349/74850
        Args:
            bucket_name: 存储桶名称
            key: 对象名称
        Returns:
            对象内容
        """
        chunk_size = 69 * 1024  # Using same chunk size as example for proven performance

        response = None
        try:
            response = await self.get(bucket=bucket_name, key=key)
            if response.status_code == 200 or response.status_code == 206:
                if int(response.headers.get('content-length', "0")) > self.max_object_size:
                    raise Exception(
                        f"Bucket: {bucket_name} object: {key} is too large, more than {self.max_object_size} bytes")

                content = bytearray()
                async for chunk in response.aiter_bytes(chunk_size):
                    content.extend(chunk)

                if is_text_file(key):
                    return content.decode('utf-8')
                else:
                    return base64.b64encode(content).decode()
            else:
                raise Exception(f"get object failed, tos server return: {response.json()}")
        finally:
            if response is not None:
                await response.aclose()


def is_text_file(key: str) -> bool:
    """Determine if a file is text-based by its extension"""
    text_extensions = {
        '.txt', '.log', '.json', '.xml', '.yml', '.yaml', '.md',
        '.csv', '.ini', '.conf', '.py', '.js', '.html', '.css',
        '.sh', '.bash', '.cfg', '.properties'
    }
    return any(key.lower().endswith(ext) for ext in text_extensions)
