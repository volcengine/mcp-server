from __future__ import print_function

from mcp.server.fastmcp import FastMCP
import datetime
import random
import string
import logging
from .sign import request, get_authorization_credentials
import json
from mcp.server.fastmcp import FastMCP
import os

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

mcp = FastMCP(
    "Nacos",
    host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
    port=int(os.getenv("MCP_SERVER_PORT", "8000")),
    streamable_http_path=os.getenv("STREAMABLE_HTTP_PATH", "/mcp"),
    stateless_http=True,
    json_response=True,
)
# Enable JSON response & stateless HTTP by default
os.environ["FASTMCP_JSON_RESPONSE"] = "true"


# 生成随机名称：mcp-random-string
def generate_random_name(prefix="mcp", length=8):
    """Generate a random string for nacos registry name"""
    random_str = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=length)
    )
    return f"{prefix}-{random_str}"


# 校验 region 参数
def validate_and_set_region(region: str = "cn-beijing") -> str:
    """
    Validates the provided region and returns the default if none is provided.

    Args:
        region: The region to validate

    Returns:
        A valid region string

    Raises:
        ValueError: If the provided region is invalid
    """
    valid_regions = ["ap-southeast-1", "cn-beijing", "cn-shanghai", "cn-guangzhou"]
    if region:
        if region not in valid_regions:
            raise ValueError(
                f"Invalid region. Must be one of: {', '.join(valid_regions)}"
            )
    else:
        region = "cn-beijing"
    return region


# Uniformly process requests and send requests
def handle_request(region, action, body) -> str:
    """
    Uniformly process and send requests.

    Args:
        region(str): The region of the request.
        action (str): The name of the operation to be performed by the request.
        body (dict): The main content of the request, stored in a dictionary.

    Returns:
        str: The response body of the request.
    """

    # 获取当前时间
    date = datetime.datetime.utcnow()

    # 调用 get_authorization_credentials 函数获取授权凭证
    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    # 调用 request 函数发送请求并获取响应
    response_body = request(
        "POST", date, {}, {}, region, ak, sk, token, action, json.dumps(body)
    )
    return response_body


@mcp.tool(
    description="""Retrieves detailed information about a specific nacos registry.
Use this when you need to obtain detailed information about a particular nacos registry.
The `id` parameter is required to identify the specific nacos registry you want to query.
region is the region where the nacos registry is located, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`,
`cn-shanghai`, `cn-guangzhou` as well."""
)
def get_nacos_registry(id: str = "", region: str = "cn-beijing"):
    """
    Retrieves detailed information about a specific nacos registry.

    Args:
        id (str): The ID of the nacos registry to retrieve.
        region (str): The region where the nacos registry is located.

    Returns:
        str: The response body of the request.
    """

    # Validate region parameter
    region = validate_and_set_region(region)

    # Construct the request parameter body of the tool in JSON format
    body = {"Id": id}

    # Set the action for the request
    action = "GetNacosRegistry"

    try:
        response_body = handle_request(region, action, body)
        return response_body
    except Exception as e:
        return f"Failed to get Nacos Registry with id {id}: {str(e)}"


@mcp.tool(
    description="""Creates a new Nacos registry with a random name if no name is provided.
Use this when you need to create a new nacos registry.
region is the region where the nacos registry will be created, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`,
`cn-shanghai`, `cn-guangzhou` as well.
VpcId is the ID of the VPC where the Nacos registry will be deployed, and it cannot be empty.
At least two non-empty SubnetIds are required to ensure high availability of the Nacos registry."""
)
def create_nacos_registry(
    name: str = "",
    region: str = "cn-beijing",
    VpcId: str = "",
    SubnetId1: str = "",
    SubnetId2: str = "",
    SubnetId3: str = "",
):
    """
    Creates a new Nacos registry.

    Args:
        name (str): The name of the Nacos registry. If not provided, a random name will be generated.
        region (str): The region where the nacos registry will be created. Default is cn-beijing.
        VpcId (str): The ID of the VPC where the Nacos registry will be deployed. It cannot be empty.
        SubnetId1 (str): The first subnet ID. At least two non-empty SubnetIds are required.
        SubnetId2 (str): The second subnet ID.
        SubnetId3 (str): The third subnet ID.

    Returns:
        str: The response body of the request.
    """

    # Validate region and name parameter
    nacos_registry_name = name if name != "" else generate_random_name()
    region = validate_and_set_region(region)

    # Validate VpcId and SubnetIds
    if not VpcId:
        raise ValueError("VpcId cannot be empty")
    non_empty_subnet_ids = [id for id in [SubnetId1, SubnetId2, SubnetId3] if id]
    if len(non_empty_subnet_ids) < 2:
        raise ValueError("At least two non-empty SubnetIds are required")

    # create nacos registry
    body = {
        "Name": nacos_registry_name,
        "Replicas": 3,
        "InstanceSpec": "mse.g1.medium",
        "RegistryVersion": "2.2.4",
        "NetworkSpec": {
            "VpcId": VpcId,
            "NetworkType": ["PRIVATE"],
            "SubnetId": non_empty_subnet_ids,
        },
        "ChargeSpec": {"ChargeType": "PostPaid"},
        "ProjectName": "default",
    }

    # Set the action for the request
    action = "CreateNacosRegistry"

    try:
        response = handle_request(region, action, body)
        return response
    except Exception as e:
        return (
            f"Failed to create Nacos registry with name {nacos_registry_name}: {str(e)}"
        )


@mcp.tool(
    description="""Updates the info of a specific nacos registry.
Use this when you need to update name of a particular nacos registry.
region is the region where the nacos registry is located, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`,
`cn-shanghai`, `cn-guangzhou` as well.
The `id` parameter is required to identify the specific nacos registry you want to rename.
The `name` parameter is required to identify the new name of the nacos registry."""
)
def update_registry_info(id: str = "", name: str = "", region: str = "cn-beijing"):
    """
    Updates the info of a specific nacos registry.

    Args:
        id (str): The ID of the nacos registry to retrieve.
        name (str): The new name of the nacos registry.
        region (str): The region where the nacos registry is located.

    Returns:
        str: The response body of the request.
    """

    # Validate region, id and name parameter
    if id == "" or name == "":
        return "The id and name parameters are both required."
    region = validate_and_set_region(region)

    # Construct the request parameter body of the tool in JSON format
    body = {"Id": id, "Name": name}

    # Set the action for the request
    action = "UpdateRegistryInfo"

    try:
        response_body = handle_request(region, action, body)
        return response_body
    except Exception as e:
        return f"Failed to update Nacos Registry's info with id {id}: {str(e)}"


@mcp.tool(
    description="""Retrieves a list of Nacos Registries.
Use this when you need to obtain a list of all Nacos Registries in a specific region.
region is the region where the gateways are located, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`,
`cn-shanghai`, `cn-guangzhou` as well."""
)
def list_nacos_registries(region: str = "cn-beijing"):
    """
    This function is used to retrieve a list of all Nacos registries in a specific region.

    Parameters:
    region (str): The region where the gateway is located, with a default value of "cn-beijing". Supported values include "ap-southeast-1", "cn-beijing", "cn-shanghai", and "cn-guangzhou".

    Returns:
    str: If the request is successful, returns the response body; if it fails, returns an error message.
    """

    # Validate region parameter
    region = validate_and_set_region(region)

    # Construct the request parameter body of the tool in JSON format
    body = {"PageNumber": 1, "PageSize": 100}

    # Set the action for the request
    action = "ListNacosRegistries"

    try:
        response_body = handle_request(region, action, body)
        return response_body
    except Exception as e:
        return f"Failed to get List of Nacos Registry: {str(e)}"
