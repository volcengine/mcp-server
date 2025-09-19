from dataclasses import asdict
import json
import aiohttp
from ..model import *

Host = "open.feedcoopapi.com"
ContentType = "application/json"


async def chat_completion_api_key_auth_api(api_key: str, req: OriginChatCompletionRequest, tool_name: str):
    header = {
        "Content-Type": ContentType,
        "Authorization": f"Bearer {api_key}",
        "X-Traffic-Tag": f"ark_mcp_server_{tool_name}",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f"https://{Host}/agent_api/agent/chat/completion",
            headers=header,
            timeout=aiohttp.ClientTimeout(total=600),
            data=json.dumps(asdict(req))
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data
        return None
    return None
