# -*- coding:utf-8 -*-
import argparse
import json
import os
import http.client
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("vefaas-sandbox", port=int(os.getenv("PORT", "8000")))

# Constants
Sandbox_API_BASE = (
    "xxx.apigateway-cn-beijing.volceapi.com"  # 替换为用户沙盒服务 APIG 地址
)

# send http request to SandboxFusion run_code api
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
    sandbox_api = os.getenv("SANDBOX_API", Sandbox_API_BASE)
    conn = http.client.HTTPSConnection(sandbox_api)

    conn.request("POST", "/run_code", payload, headers)

    resData = conn.getresponse().read()
    response = resData.decode("utf-8")

    # check if the code run successful
    successStr = '"status":"Success"'
    index = response.find(successStr)
    if index == -1:
        result = {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {
                    "run_result": response,
                }
            ),
        }
        return result

    # extract code run results
    run_result = json.loads(response).get("run_result")
    stdout = run_result.get("stdout")
    stderr = run_result.get("stderr")

    message = ""
    if stdout:
        message = stdout
    elif stderr:
        message = stderr

    result = {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"run_result": message}),
    }
    return result

@mcp.tool(description="""run your code str in sandbox server with your provided language,
 support to set these languages: python、nodejs、go、bash、typescript、java、cpp、php、csharp、lua、R、 swift、scala、ruby""")
def run_code(codeStr, language) -> str :
    payload = json.dumps(
        {
            "compile_timeout": 60,
            "run_timeout": 60,
            "code": codeStr,
            "language": language,
            "files": {},
        }
    )
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
