from dataclasses import asdict
import json
import requests
from ..model import *

Host = "open.feedcoopapi.com"
ContentType = "application/json"


def chat_completion_api_key_auth_api(api_key: str, req: OriginChatCompletionRequest, tool_name: str):
    header = {
        "Content-Type": ContentType,
        "Authorization": f"Bearer {api_key}",
        "X-Traffic-Tag": f"ark_mcp_server_{tool_name}",
    }
    r = requests.request(method="POST",
                         url="https://{}{}".format(Host, "/agent_api/agent/chat/completion"),
                         headers=header,
                         timeout=600,
                         data=json.dumps(asdict(req))
                         )
    return r
