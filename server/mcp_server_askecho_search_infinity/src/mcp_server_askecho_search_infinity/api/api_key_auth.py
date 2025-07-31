from dataclasses import asdict
import json
import requests
from ..model import *

Host = "open.feedcoopapi.com"
ContentType = "application/json"


def web_search_api_key_auth(api_key: str, req: WebSearchRequest, tool_name: str):
    header = {
        "Content-Type": ContentType,
        "Authorization": f"Bearer {api_key}",
        "X-Traffic-Tag": f"ark_mcp_server_{tool_name}",
    }
    r = requests.request(method="POST",
                         url="https://{}{}".format(Host, "/search_api/web_search"),
                         headers=header,
                         timeout=3000,
                         data=json.dumps(asdict(req))
                         )
    return r