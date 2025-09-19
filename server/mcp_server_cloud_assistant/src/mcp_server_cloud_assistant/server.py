import argparse
import logging
import time
from typing import Any

import volcenginesdkcore
import base64
import json
import os

from mcp.server.session import ServerSession
from mcp.server.fastmcp import Context, FastMCP
from starlette.requests import Request
import sys
from pathlib import Path

# 检测是否以脚本模式运行（非包模式）
if __package__ is None:
    sys.path.insert(0, str(Path(__file__).parent))
else:
    from mcp_server_cloud_assistant.config import load_config, get_auth_config

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

"""
constants about server
"""

MCP_SERVER_NAME = "cloud_assist"

# ======= API ======
API_METHOD = "GET"
API_SERVICE = "ecs"
API_VERSION = "2020-04-01"
API_CHARSET = "utf-8"
API_RUN_COMMAND = "RunCommand"
API_DESCRIBE_INVOCATION_RESULTS = "DescribeInvocationResults"
API_DESCRIBE_INVOCATIONS = "DescribeInvocations"

# ======= RESPONSE ======
MAX_WAIT_COUNT = 30
WAIT_PERIOD = 5
STATUS_SUCCESS = "Success"
STATUS_FAILED = "Failed"
STATUS_PARTIAL_FAILED = "PartialFailed"

# Initialize FastMCP server
mcp = FastMCP(MCP_SERVER_NAME, port=int(os.getenv("PORT", "8000")))

# Global variables
client = None

@mcp.tool(name="run_command",description="""send commands to be executed on the specified instance.
Region is the region where the instance exists, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`, 
`cn-shanghai`, `cn-guangzhou` as well.""")
async def run_command(instance: str, region: str, command_content: str) -> str:
    """Send commands to the target instance,
        generate an execution record, wait until the execution is completed,
        and then retrieve and return the execution results.

        This provides a channel for the execution of commands within the instance.
        It cannot identify the specific content of the commands.

    Args:
        instance: target instance
        region: target region
        command_content: command content

    Returns:
        The execution result of the passed-in command on the target instance

    """
    init_client_config(region)
    # run command
    command_content = command_content.encode(API_CHARSET)
    command_content = base64.b64encode(command_content).decode(API_CHARSET)
    req = {"InstanceIds.1": instance,
           "CommandContent": command_content,
           "Type": "Shell",
           "InvocationName": "mcp-server-cloud-assistant-demo"}
    res = send_cloud_assist_request(req, API_RUN_COMMAND)
    invocation_id = res["InvocationId"]

    # wait done
    wait_invocation_done(invocation_id)

    # get result
    req = {"InvocationId": invocation_id}
    res = send_cloud_assist_request(req, API_DESCRIBE_INVOCATION_RESULTS)
    output = res["InvocationResults"][0]["Output"]
    output = base64.b64decode(output).decode(API_CHARSET)
    return output

def init_client_config(region: str) -> any:
    # 从 context 中获取 header
    ctx: Context[ServerSession, object] = mcp.get_context()
    raw_request: Request = ctx.request_context.request

    global client
    auth = None
    if raw_request:
        # 从 header 的 authorization 字段读取 base64 编码后的 sts json
        auth = raw_request.headers.get("authorization", None)
    if auth is None:
        # 如果 header 中没有认证信息，可能是 stdio 模式，尝试从环境变量获取
        auth = os.getenv("authorization", None)
    if auth is None:
        # 获取认证信息失败,尝试从环境变量中获取
        conf = load_config()
        client = init_local_client(conf, region)
    else:
        if ' ' in auth:
            _, base64_data = auth.split(' ', 1)
        else:
            base64_data = auth

        try:
            # 解码 Base64
            decoded_str = base64.b64decode(base64_data).decode('utf-8')
            data = json.loads(decoded_str)

            # 获取字段
            ak = data.get('AccessKeyId')
            sk = data.get('SecretAccessKey')
            session_token = data.get('SessionToken')
            conf = get_auth_config(ak, sk, session_token)
            client = init_client(ak, sk, conf.volcengine_endpoint, region, session_token)
        except Exception as e:
            raise ValueError("Decode authorization info error", e)

    if client is None:
        raise ValueError("Init client error")


def init_client(ak, sk, endpoint, region, token) -> any:
    configuration = volcenginesdkcore.Configuration()
    configuration.ak = ak
    configuration.sk = sk
    configuration.host = endpoint
    configuration.region = region
    configuration.session_token = token

    config = volcenginesdkcore.Configuration.set_default(configuration)
    return volcenginesdkcore.UniversalApi(volcenginesdkcore.ApiClient(config))

def init_local_client(conf: any, region: str) -> any:
    configuration = volcenginesdkcore.Configuration()
    configuration.ak = conf.volcengine_ak
    configuration.sk = conf.volcengine_sk
    configuration.host = conf.volcengine_endpoint
    configuration.region = region

    config = volcenginesdkcore.Configuration.set_default(configuration)
    return volcenginesdkcore.UniversalApi(volcenginesdkcore.ApiClient(config))


def send_cloud_assist_request(req: dict, action: str) -> dict[str, Any] | None:
    res = client.do_call(
        volcenginesdkcore.UniversalInfo(method=API_METHOD, action=action, service=API_SERVICE, version=API_VERSION),
        volcenginesdkcore.Flatten(req).flat())
    return res


def wait_invocation_done(invocation_id: str):
    for i in range(0, MAX_WAIT_COUNT):
        time.sleep(WAIT_PERIOD)
        req = {
            "InvocationId": invocation_id
        }
        res = send_cloud_assist_request(req, API_DESCRIBE_INVOCATIONS)
        status = res["Invocations"][0]["InvocationStatus"]

        if status == STATUS_SUCCESS or status == STATUS_FAILED or status == STATUS_PARTIAL_FAILED:
            return

def main():
    """Start A Cloud Assistant MCP server."""
    parser = argparse.ArgumentParser(description="Run the Cloud Assistant MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use (sse or stdio)",
    )

    args = parser.parse_args()
    logger.info(f"Starting Cloud Assistant MCP Server with {args.transport} transport")
    mcp.run(transport=args.transport)

if __name__ == "__main__":
    main()