import json
import aiohttp
from ..model import *

Host = "open.feedcoopapi.com"
ContentType = "application/json"
REQUEST_TIMEOUT_SECONDS = 30


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
            timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT_SECONDS),
            data=json.dumps(req.to_payload())
        ) as response:
            # 在上下文内读取所有数据，避免连接关闭问题
            response.raise_for_status()  # 手动调用
            data = await response.json()
            return data
