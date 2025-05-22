from __future__ import print_function
from mcp.server.fastmcp import FastMCP
import os
import logging
import requests

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

mcp = FastMCP("VeFaaS Browser Use")

HEADERS = {
        "X-Faas-Event-Type": "http",
        "Content-Type": "application/json"
    }

@mcp.tool(description="""Creates a browser use task which can automatically browse the web.
Use this when you need to create a browser use task with specific messages.
The endpoint is read from the environment variable BROWSER_USE_ENDPOINT.
After this tool is called, automatically call tool get_browser_use_task_result to get the result.
""")
def create_browser_use_task(task: str) -> str:
    """
    Args:
        task (str): The task description for the browser to execute. For example: "check the weather in beijing."
                The task should be a clear instruction of what you want the browser to do.

    Returns:
        str: The task ID that can be used to retrieve results later.
    """
    # check required environment variables and parameters
    endpoint = os.getenv("BROWSER_USE_ENDPOINT")

    if not endpoint:
        raise ValueError("BROWSER_USE_ENDPOINT is not set")
    
    if not task:
        raise ValueError("Task are required")
    
    if not endpoint.startswith("http://") and not endpoint.startswith("https://"):
        endpoint = f"http://{endpoint}"

    url = f"{endpoint}/tasks"
        
    payload = {
        "messages": [
            {
                "role": "user",
                "content": task
            }
        ]
    }
    
    try:
        # 1. create a new task
        response = requests.post(url, headers=HEADERS, json=payload)

        response.raise_for_status()
        
        response_json = response.json() if response.content else None
        
        task_id = response_json.get("task_id") if response_json else None

        print(f"Task ID: {task_id}")

        return task_id
        
    except requests.exceptions.RequestException as e:
        error_message = f"Error in browser use task: {str(e)}"
        raise ValueError(error_message)

@mcp.tool(description="""Retrieves the result of a browser use task.
The endpoint is read from the environment variable BROWSER_USE_ENDPOINT.
""")
def get_browser_use_task_result(task_id: str):
    """
    Args:
        task_id (str): The ID of the browser use task to retrieve results for. 
                    This is the ID returned by create_browser_use_task.

    Returns:
        str: The final result from the browser task, including any choices or completion data.
    """
    # check required environment variables and parameters
    endpoint = os.getenv("BROWSER_USE_ENDPOINT")

    if not endpoint:
        raise ValueError("BROWSER_USE_ENDPOINT is not set")

    if not task_id:
        raise ValueError("Task ID is required")
    
    if not endpoint.startswith("http://") and not endpoint.startswith("https://"):
        endpoint = f"http://{endpoint}"

    try: 
        
        # stream the response
        url = f"{endpoint}/tasks/{task_id}/stream"
        response = requests.get(url, headers=HEADERS, stream=True)
        
        response.raise_for_status()
        
        final_content = None
        
        for line in response.iter_lines(decode_unicode=True):
            if line:
                if "choices" in line:
                    return line
        
    except requests.exceptions.RequestException as e:
        error_message = f"Error in browser use task: {str(e)}"
        raise ValueError(error_message)


def main():
    logger.info("Starting veFaaS browser use MCP Server")
    
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
