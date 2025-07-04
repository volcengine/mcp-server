from __future__ import print_function

import io
from typing import Union
from mcp.server.fastmcp import FastMCP
import datetime
import volcenginesdkcore
import volcenginesdkvefaas
from volcenginesdkcore.rest import ApiException
import random
import string
import os
import base64
import logging
import zipfile
from .sign import request, get_authorization_credentials
import json
from mcp.server.session import ServerSession
from mcp.server.fastmcp import Context, FastMCP
from starlette.requests import Request
import os
import subprocess
import zipfile
import pyzipper
from io import BytesIO
from typing import Tuple
import requests
import shutil

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

mcp = FastMCP("VeAPIG", stateless_http=True, json_response=True)
# Enable JSON response & stateless HTTP by default
os.environ["FASTMCP_JSON_RESPONSE"] = "true"

def generate_random_name(prefix="mcp", length=8):
    """Generate a random string for function name"""
    random_str = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=length)
    )
    return f"{prefix}-{random_str}"


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
    description="""Retrieves a list of VeAPIG gateways.
Use this when you need to obtain a list of all VeAPIG gateways in a specific region.
region is the region where the gateways are located, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`,
`cn-shanghai`, `cn-guangzhou` as well.
"""
)
def list_gateways(region: str = "cn-beijing"):

    # Validate region parameter
    region = validate_and_set_region(region)

    # Construct the request parameter body of the tool in JSON format
    body = {"PageNumber": 1, "PageSize": 100}

    # Set the action for the request
    action = "ListGateways"

    # Send the request and return the response body
    response_body = handle_request(region, action, body)
    return response_body


@mcp.tool(
    description="""Retrieves detailed information about a specific VeAPIG gateway.
Use this when you need to obtain detailed information about a particular VeAPIG gateway.
region is the region where the gateway is located, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`,
`cn-shanghai`, `cn-guangzhou` as well.
Note:
1. The `id` parameter is required to identify the specific gateway you want to query."""
)
def get_gateway(id: str = "", region: str = "cn-beijing"):

    # Validate region parameter
    region = validate_and_set_region(region)

    # Construct the request parameter body of the tool in JSON format
    body = {"Id": id}

    # Set the action for the request
    action = "GetGateway"

    # Send the request and return the response body
    response_body = handle_request(region, action, body)
    return response_body


@mcp.tool(
    description="""Query the list of services under a specified gateway instance.
Use this tool when you need to retrieve all services under a specific gateway instance in a particular region.
The gateway_id parameter is required to specify the gateway instance for which you want to query the service list.
region indicates the region where the gateway instance is located, defaulting to cn-beijing. It also supports ap-southeast-1, cn-shanghai, and cn-guangzhou.
Note:
1. The gateway_id parameter is mandatory and used to identify the specific gateway instance whose service list you want to query."""
)
def list_gateway_services(gateway_id: str = "", region: str = "cn-beijing"):
    # Validate region parameter
    region = validate_and_set_region(region)

    # Construct the request parameter body of the tool in JSON format
    body = {
        "PageNumber": 1,
        "PageSize": 100,
        "GatewayId": gateway_id,
    }

    # Set the action for the request
    action = "ListGatewayServices"

    # Send the request and return the response body
    response_body = handle_request(region, action, body)
    return response_body


@mcp.tool(
    description="""Gets detailed information about a specific VeApig serverless gateway service.
service_id is the id of the serverless gateway service. The service_id is required.
region is the region where the serverless gateway service is located, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`,
`cn-shanghai`, `cn-guangzhou` as well.
"""
)
def get_gateway_service(service_id: str, region: str = "cn-beijing"):
    """
    Gets detailed information about a specific VeApig serverless gateway service.

    Args:
        service_id (str): The id of the serverless gateway service.
        region (str): The region where the serverless gateway service is located.

    Returns:
        str: The response body of the request.
    """
    region = validate_and_set_region(region)
    body = {
        "Id": service_id,
    }
    try:
        response = handle_request(region, "GetGatewayService", body)
        return response
    except Exception as e:
        return f"Failed to get VeApig serverless gateway service with id {service_id}: {str(e)}"


# Tool 7: list_gateway_routes
@mcp.tool(
    description="""Query the list of routes under a specified gateway instance.
Use this tool when you need to retrieve all routes under a specific gateway instance in a particular region.
The gateway_id parameter is required to specify the gateway instance for which you want to query the route list.
region indicates the region where the gateway instance is located, defaulting to cn-beijing. It also supports ap-southeast-1, cn-shanghai, and cn-guangzhou.
Note:
1. The gateway_id parameter is mandatory and used to identify the specific gateway instance whose route list you want to query."""
)
def list_gateway_routes(gateway_id: str, region: str = "cn-beijing"):
    # Validate region parameter
    region = validate_and_set_region(region)

    # Construct the request parameter body of the tool in JSON format
    body = {
        "PageNumber": 1,
        "PageSize": 100,
        "GatewayId": gateway_id,
    }

    # Set the action for the request
    action = "ListRoutes"

    # Send the request and return the response body
    response_body = handle_request(region, action, body)
    return response_body


@mcp.tool(
    description="""Gets detailed informantion about a specific VeApig route.
route_id is the id of the route. The route_id is required.
region is the region where the route is located, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`,
`cn-shanghai`, `cn-guangzhou` as well.
"""
)
def get_gateway_route(route_id: str, region: str = "cn-beijing"):
    """
    Gets detailed informantion about a specific VeApig route.

    Args:
        route_id (str): The id of the route.
        region (str): The region where the route is located.

    Returns:
        str: The response body of the request.
    """
    region = validate_and_set_region(region)
    body = {
        "Id": route_id,
    }
    try:
        response = handle_request(region, "GetRoute", body)
        return response
    except Exception as e:
        return f"Failed to get VeApig route with id {route_id}: {str(e)}"


@mcp.tool(
    description="""Creates a new VeApig serverless gateway.
gateway_name is the name of the serverless gateway. If not provided, a random name will be generated.
region is the region where the serverless gateway will be created, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`,
`cn-shanghai`, `cn-guangzhou` as well.
"""
)
def create_serverless_gateway(name: str = "", region: str = "cn-beijing"):
    """
    Creates a new VeApig serverless gateway.

    Args:
        name (str): The name of the serverless gateway. If not provided, a random name will be generated.
        region (str): The region where the serverless gateway will be created. Default is cn-beijing.

    Returns:
        str: The response body of the request.
    """
    gateway_name = name if name != "" else generate_random_name()
    region = validate_and_set_region(region)
    body = {
        "Name": gateway_name,
        "Region": region,
        "Type": "serverless",
        "ResourceSpec": {
            "Replicas": 2,
            "InstanceSpecCode": "1c2g",
            "CLBSpecCode": "small_1",
            "PublicNetworkBillingType": "traffic",
            "NetworkType": {"EnablePublicNetwork": True, "EnablePrivateNetwork": False},
        },
    }
    try:
        response = handle_request(region, "CreateGateway", body)
        return response
    except Exception as e:
        return f"Failed to create VeApig serverless gateway with name {gateway_name}: {str(e)}"


@mcp.tool(
    description="""Creates a new VeApig serverless gateway service with a random name if no name is provided.
gateway_id is the id of the serverless gateway where the service will be created. The gateway_id is required.
region is the region where the serverless gateway service will be created, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`,
`cn-shanghai`, `cn-guangzhou` as well.
"""
)
def create_gateway_service(
    gateway_id: str, name: str = "", region: str = "cn-beijing"
):
    """
    Creates a new VeApig serverless gateway service.

    Args:
        gateway_id (str): The id of the serverless gateway where the service will be created.
        name (str): The name of the serverless gateway service. If not provided, a random name will be generated.
        region (str): The region where the serverless gateway service will be created. Default is cn-beijing.

    Returns:
        str: The response body of the request.
    """

    service_name = name if name != "" else generate_random_name()
    region = validate_and_set_region(region)
    body = {
        "ServiceName": service_name,
        "GatewayId": gateway_id,
        "Protocol": ["HTTP", "HTTPS"],
        "AuthSpec": {"Enable": False},
    }

    try:
        response = handle_request(region, "CreateGatewayService", body)
        return response
    except Exception as e:
        return f"Failed to create VeApig serverless gateway service with name {service_name}: {str(e)}"
