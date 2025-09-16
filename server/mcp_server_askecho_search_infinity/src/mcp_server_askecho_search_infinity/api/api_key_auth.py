from dataclasses import asdict
import json
import aiohttp
from ..model import *

Host = "open.feedcoopapi.com"
ContentType = "application/json"


async def web_search_api_key_auth(api_key: str, req: WebSearchRequest, tool_name: str):
    header = {
        "Content-Type": ContentType,
        "Authorization": f"Bearer {api_key}",
        "X-Traffic-Tag": f"ark_mcp_server_{tool_name}",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f"https://{Host}/search_api/web_search",
            headers=header,
            timeout=aiohttp.ClientTimeout(total=3000),
            data=json.dumps(asdict(req))
        ) as response:
            # 在上下文内读取所有数据，避免连接关闭问题
            content = await response.read()

            # 创建一个兼容requests响应的对象
            class AsyncResponse:
                def __init__(self, status_code, content_data):
                    self.status_code = status_code
                    self._content = content_data

                def raise_for_status(self):
                    if self.status_code >= 400:
                        raise aiohttp.ClientResponseError(
                            request_info=None,
                            history=None,
                            status=self.status_code,
                            message=f"HTTP {self.status_code}"
                        )

                def json(self):
                    return json.loads(self._content.decode('utf-8'))

                async def json(self):
                    return json.loads(self._content.decode('utf-8'))

            return AsyncResponse(response.status, content)