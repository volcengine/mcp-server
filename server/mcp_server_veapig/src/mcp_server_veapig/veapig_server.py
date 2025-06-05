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

mcp = FastMCP("VeAPIG")


def validate_and_set_region(region: str = None) -> str:
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
            raise ValueError(f"Invalid region. Must be one of: {', '.join(valid_regions)}")
    else:
        region = "cn-beijing"
    return region

# Uniformly process requests and send requests
def handle_request(method, query, header, action, body) -> str:
    """
    Uniformly process and send requests.

    Args:
        method (str): HTTP request method, such as "GET", "POST", etc.
        query (dict): Query parameters of the request, stored in a dictionary.
        header (dict): Header information of the request, stored in a dictionary.
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
    response_body = request(method, date, query, header, ak, sk, token, action, json.dumps(body))
    return response_body

# Tool 1: list_gateways
@mcp.tool(description="""Retrieves a list of VeAPIG gateways.
Use this when you need to obtain a list of all VeAPIG gateways in a specific region.
region is the region where the gateways are located, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`, 
`cn-shanghai`, `cn-guangzhou` as well.
""")
def list_gateways(region: str = "cn-beijing") -> str:

    # Validate region parameter
    region = validate_and_set_region(region)

    # Construct the request parameter body of the tool in JSON format
    body = {
        "Top": {
            "Region": region
        },
        "PageNumber": 1,
        "PageSize": 100
    }

    # Set the action for the request
    action = "ListGateways"

    # Send the request and return the response body 
    response_body = handle_request("POST", {}, {}, action, body)
    return response_body

# Tool 2: get_gateway
@mcp.tool(description="""Retrieves detailed information about a specific VeAPIG gateway.
Use this when you need to obtain detailed information about a particular VeAPIG gateway.
region is the region where the gateway is located, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`, 
`cn-shanghai`, `cn-guangzhou` as well.
Note: 
1. The `id` parameter is required to identify the specific gateway you want to query.""")
def get_gateway(id: str = "", region: str = "cn-beijing") -> str:

    # Validate region parameter
    region = validate_and_set_region(region)

    # Construct the request parameter body of the tool in JSON format
    body = {
        "Id": id,
        "Top": {
            "Region": region
        }
    }

    # Set the action for the request
    action = "GetGateway"

    # Send the request and return the response body 
    response_body = handle_request("POST", {}, {}, action, body)
    return response_body


# Tool 4: list_gateway_services
@mcp.tool(description="""Query the list of services under a specified gateway instance.
Use this tool when you need to retrieve all services under a specific gateway instance in a particular region.
The gateway_id parameter is required to specify the gateway instance for which you want to query the service list.
region indicates the region where the gateway instance is located, defaulting to cn-beijing. It also supports ap-southeast-1, cn-shanghai, and cn-guangzhou.
Note:
1. The gateway_id parameter is mandatory and used to identify the specific gateway instance whose service list you want to query.""")
def list_gateway_services(gateway_id: str = "", region: str = "cn-beijing") -> str:
    # Validate region parameter
    region = validate_and_set_region(region)

    # Construct the request parameter body of the tool in JSON format
    body = {
        "Top": {
            "Region": region
        },
        "PageNumber": 1,
        "PageSize": 100,
        "GatewayId": gateway_id
    }

    # Set the action for the request
    action = "ListGatewayServices"

    # Send the request and return the response body
    response_body = handle_request("POST", {}, {}, action, body)
    return response_body


# Tool 7: list_gateway_routes
@mcp.tool(description="""Query the list of routes under a specified gateway instance.
Use this tool when you need to retrieve all routes under a specific gateway instance in a particular region.
The gateway_id parameter is required to specify the gateway instance for which you want to query the route list.
region indicates the region where the gateway instance is located, defaulting to cn-beijing. It also supports ap-southeast-1, cn-shanghai, and cn-guangzhou.
Note:
1. The gateway_id parameter is mandatory and used to identify the specific gateway instance whose route list you want to query.""")
def list_gateway_routes(gateway_id: str = "", region: str = "cn-beijing") -> str:
    # Validate region parameter
    region = validate_and_set_region(region)

    # Construct the request parameter body of the tool in JSON format
    body = {
        "Top": {
            "Region": region
        },
        "PageNumber": 1,
        "PageSize": 100,
        "GatewayId": gateway_id
    }

    # Set the action for the request
    action = "ListRoutes"

    # Send the request and return the response body
    response_body = handle_request("POST", {}, {}, action, body)
    return response_body    



