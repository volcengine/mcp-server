# -*- coding:utf-8 -*-
import argparse
import json
import os
import logging
import http.client
from urllib.parse import urlparse
from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Optional

# Initialize FastMCP server
mcp = FastMCP("vefaas-sandbox", port=int(os.getenv("PORT", "8000")))

# Constants
Sandbox_API_BASE = (
    "xxx.apigateway-cn-beijing.volceapi.com"  # 替换为用户沙盒服务 APIG 地址
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(__name__)

# send http reqeust to SandboxFusion run_code api
def send_request(payload):
    auth_token = os.getenv("AUTH_TOKEN")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
    }
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    else:
        logger.warning("AUTH_TOKEN environment variable not set. Request will be sent without Authorization header.")

    try:
        sandbox_api = os.getenv("SANDBOX_API", Sandbox_API_BASE)
        parsed = urlparse(sandbox_api)
        if parsed.scheme:
            sandbox_api = parsed.netloc + parsed.path.rstrip('/')

        conn = http.client.HTTPSConnection(sandbox_api)
        conn.request("POST", "/run_code", payload, headers)

        response = conn.getresponse()
        res_data = response.read().decode("utf-8")

        if response.status != 200:
            return {
                "statusCode": response.status,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": f"API request failed with status {response.status}"}),
            }

        try:
            res_json = json.loads(res_data)
            if res_json.get("status") != "Success":
                return {
                    "statusCode": 500,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": "Execution failed", "details": res_json}),
                }

            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"run_result": res_json}),
            }

        except json.JSONDecodeError:
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Invalid JSON response", "raw_response": res_data}),
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)}),
        }
    finally:
        conn.close() if 'conn' in locals() else None
    return result

@mcp.tool(description="""run your code str in sandbox server with your provided language,
 support to set these languages: python、nodejs、go、bash、typescript、java、cpp、php、csharp、lua、R、 swift、scala、ruby""")
def run_code(
    codeStr: str,
    language: str,
    fetch_files: Optional[List[str]] = None,
    files: Optional[Dict[str, str]] = None,
    compile_timeout: int = 60,
    run_timeout: int = 60,
) -> str:
    """Execute code with given parameters.
    Args:
        codeStr: Source code to execute
        language: Programming language
        fetch_files: List of files to fetch
        files: Additional file contents
        compile_timeout: Compilation timeout in seconds
        run_timeout: Execution timeout in seconds

    Returns:
        Execution result as string
    """
    payload_dict = {
        "compile_timeout": compile_timeout,
        "run_timeout": run_timeout,
        "code": codeStr,
        "language": language,
    }
    if fetch_files is not None:  # 更明确的None检查
        payload_dict["fetch_files"] = fetch_files
    if files:
        payload_dict["files"] = files

    payload = json.dumps(payload_dict)

    return send_request(payload=payload)

def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Run the Code Sandbox MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio"],
        default="stdio",
        help="Transport protocol to use (sse or stdio)",
    )
    args = parser.parse_args()
    try:
        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting Code Sandbox MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
