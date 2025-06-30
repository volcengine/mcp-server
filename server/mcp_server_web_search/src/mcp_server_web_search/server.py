import logging
import os
import requests

from typing import Any
from mcp.server.fastmcp import Context, FastMCP
from mcp_server_web_search.base.config import WEB_SEARCH_CONFIG

logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("Web Search MCP Server", port=int(os.getenv("PORT", "8000")))


@mcp.tool()
def web_search(query: str = None) -> str:
    """query a single keyword from some search engineer"""

    try:
        url = f"https://{WEB_SEARCH_CONFIG.endpoint}/v1/queries"

        headers = {
            "Content-Type": "application/json",
            "X-VE-Source": "google_search",
            "X-VE-API-Key": WEB_SEARCH_CONFIG.token,
        }
        data = {
            "query": query,
            "source": "google_search",
            "parse": True,
            "limit": "10",
            "start_page": "1",
            "pages": "1",
            "context": [
                {
                    "key": "nfpr",
                    "value": True
                },
                {
                    "key": "safe_search",
                    "value": False
                },
                {
                    "key": "filter",
                    "value": 1
                }
            ],
        }

        response = requests.post(url, headers=headers, json=data, verify=False)
        logger.info(f"response: {response}")

        response.raise_for_status()

        response_json = response.json() if response.content else None
        logger.info(f"response_json: {response_json}")
        results_dict = response_json.get('results')[0].get('content').get('results').get('organic')
        logger.info(f"results_dict: {results_dict}")

        results_str = ""
        for r in results_dict:
            dic = {"url": r.get('url'), "title": r.get('title'), "description": r.get('desc')}
            results_str += str(dic)

        logger.info(f"results_str: {results_str}")

        return results_str

    except requests.exceptions.RequestException as e:
        error_message = f"Error: {str(e)}"
        raise ValueError(error_message)
