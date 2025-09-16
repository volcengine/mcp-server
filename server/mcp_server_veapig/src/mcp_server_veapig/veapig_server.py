import logging
import json
import random
import os
import string


from mcp.server.fastmcp import FastMCP
from .common.client import get_volc_apig_client
from .common.client20221112 import get_volc_apig_client20221112


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

mcp = FastMCP("VeAPIG", stateless_http=True, json_response=True)
# Enable JSON response & stateless HTTP by default
os.environ["FASTMCP_JSON_RESPONSE"] = "true"


# 生成随机字符串作为网关名称
def generate_random_name(prefix="mcp", length=8):
    """Generate a random string for function name"""
    random_str = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=length)
    )
    return f"{prefix}-{random_str}"


# 验证并设置区域
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


@mcp.tool(
    description="""Retrieves a list of VeAPIG gateways.
Use this when you need to obtain a list of all VeAPIG gateways in a specific region.
region is the region where the gateways are located, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`,
`cn-shanghai`, `cn-guangzhou` as well."""
)
def list_gateways(region: str = "cn-beijing"):

    # Validate region parameter
    region = validate_and_set_region(region)

    try:
        # 获取 APIGApi 客户端
        apig_client = get_volc_apig_client(mcp, region)

        # 调用 ListGateways 方法 - 使用模型对象传递参数
        from volcenginesdkapig.models import ListGatewaysRequest

        request = ListGatewaysRequest(page_number=1, page_size=100)
        response = apig_client.list_gateways(request)

        # 将响应对象转换为JSON字符串并返回
        return json.dumps(response.to_dict(), ensure_ascii=False)
    except Exception as e:
        logger.error(f"Failed to list gateways: {str(e)}")
        return f"Failed to list gateways: {str(e)}"


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

    try:
        # 获取 APIGApi 客户端
        apig_client = get_volc_apig_client(mcp, region)

        # 调用 ListGateways 方法 - 使用模型对象传递参数
        from volcenginesdkapig.models import GetGatewayRequest

        request = GetGatewayRequest(id=id)
        response = apig_client.get_gateway(request)

        # 将响应对象转换为JSON字符串并返回
        return json.dumps(response.to_dict(), ensure_ascii=False)
    except Exception as e:
        logger.error(f"Failed to get gateway: {str(e)}")
        return f"Failed to get gateway: {str(e)}"


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
    try:
        # 获取 APIGApi 客户端
        apig_client = get_volc_apig_client(mcp, region)

        # 调用 ListGatewayServices 方法 - 使用模型对象传递参数
        from volcenginesdkapig.models import ListGatewayServicesRequest

        request = ListGatewayServicesRequest(
            gateway_id=gateway_id, page_number=1, page_size=100
        )
        response = apig_client.list_gateway_services(request)

        # 将响应对象转换为JSON字符串并返回
        return json.dumps(response.to_dict(), ensure_ascii=False)
    except Exception as e:
        logger.error(f"Failed to get list of gatewayservices: {str(e)}")
        return f"Failed to get list of gatewayservices: {str(e)}"


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
    # Validate region parameter
    region = validate_and_set_region(region)
    try:
        # 获取 APIGApi 客户端
        apig_client = get_volc_apig_client(mcp, region)

        # 调用 GetGatewayService 方法 - 使用模型对象传递参数
        from volcenginesdkapig.models import GetGatewayServiceRequest

        request = GetGatewayServiceRequest(id=service_id)
        response = apig_client.get_gateway_service(request)

        # 将响应对象转换为JSON字符串并返回
        return json.dumps(response.to_dict(), ensure_ascii=False)
    except Exception as e:
        logger.error(
            f"Failed to get VeApig serverless gateway service with id {service_id}: {str(e)}"
        )
        return f"Failed to get VeApig serverless gateway service with id {service_id}: {str(e)}"


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

    try:
        # 获取 APIGApi 客户端
        apig_client = get_volc_apig_client20221112(mcp, region)

        # 调用 ListRoutes 方法 - 使用模型对象传递参数
        from volcenginesdkapig20221112.models import ListRoutesRequest

        request = ListRoutesRequest(gateway_id=gateway_id, page_number=1, page_size=100)
        response = apig_client.list_routes(request)

        # 将响应对象转换为JSON字符串并返回
        return json.dumps(response.to_dict(), ensure_ascii=False)
    except Exception as e:
        logger.error(
            f"Failed to get list of gateway_routes with gateway_id {gateway_id}: {str(e)}"
        )
        return f"Failed to get list of gateway_routes with gateway_id {gateway_id}: {str(e)}"


@mcp.tool(
    description="""Gets detailed informantion about a specific VeApig route.
route_id is the id of the route. The route_id is required.
region is the region where the route is located, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`,
`cn-shanghai`, `cn-guangzhou` as well."""
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
    try:
        # 获取 APIGApi 客户端
        apig_client = get_volc_apig_client20221112(mcp, region)

        # 调用 GetRoute 方法 - 使用模型对象传递参数
        from volcenginesdkapig20221112.models import GetRouteRequest

        request = GetRouteRequest(id=route_id)
        response = apig_client.get_route(request)

        # 将响应对象转换为JSON字符串并返回
        return json.dumps(response.to_dict(), ensure_ascii=False)
    except Exception as e:
        logger.error(f"Failed to get VeApig route with id {route_id}: {str(e)}")
        return f"Failed to get VeApig route with id {route_id}: {str(e)}"


@mcp.tool(
    description="""Creates a new VeApig serverless gateway.
gateway_name is the name of the serverless gateway. If not provided, a random name will be generated.
region is the region where the serverless gateway will be created, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`,
`cn-shanghai`, `cn-guangzhou` as well."""
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
    # 检查参数是否为空，如果name为空，则生成随机名称
    gateway_name = name if name != "" else generate_random_name()
    # 验证region参数
    region = validate_and_set_region(region)

    try:
        # 获取 APIGApi 客户端
        apig_client = get_volc_apig_client(mcp, region)

        # 调用 CreateGateway 方法 - 使用模型对象传递参数
        from volcenginesdkapig.models import CreateGatewayRequest

        resource_spec_json = {
            "Replicas": 2,
            "InstanceSpecCode": "1c2g",
            "CLBSpecCode": "small_1",
            "PublicNetworkBillingType": "traffic",
            "NetworkType": {"EnablePublicNetwork": True, "EnablePrivateNetwork": False},
        }
        request = CreateGatewayRequest(
            name=gateway_name,
            region=region,
            type="serverless",
            resource_spec=resource_spec_json,
        )
        response = apig_client.create_gateway(request)

        # 将响应对象转换为JSON字符串并返回
        return json.dumps(response.to_dict(), ensure_ascii=False)
    except Exception as e:
        logger.error(
            f"Failed to create VeApig serverless gateway with name {gateway_name}: {str(e)}"
        )
        return f"Failed to create VeApig serverless gateway with name {gateway_name}: {str(e)}"


@mcp.tool(
    description="""Creates a new VeApig serverless gateway service with a random name if no name is provided.
gateway_id is the id of the serverless gateway where the service will be created. The gateway_id is required.
region is the region where the serverless gateway service will be created, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`,
`cn-shanghai`, `cn-guangzhou` as well."""
)
def create_gateway_service(gateway_id: str, name: str = "", region: str = "cn-beijing"):
    """
    Creates a new VeApig serverless gateway service.

    Args:
        gateway_id (str): The id of the serverless gateway where the service will be created.
        name (str): The name of the serverless gateway service. If not provided, a random name will be generated.
        region (str): The region where the serverless gateway service will be created. Default is cn-beijing.

    Returns:
        str: The response body of the request.
    """
    # 检查参数是否为空，如果name为空，则生成随机名称
    service_name = name if name != "" else generate_random_name()
    # 验证region参数
    region = validate_and_set_region(region)

    try:
        # 获取 APIGApi 客户端
        apig_client = get_volc_apig_client(mcp, region)

        # 调用 CreateGatewayService 方法 - 使用模型对象传递参数
        from volcenginesdkapig.models import CreateGatewayServiceRequest

        request = CreateGatewayServiceRequest(
            service_name=service_name,
            gateway_id=gateway_id,
            protocol=["HTTP", "HTTPS"],
            auth_spec={"Enable": False},
        )
        response = apig_client.create_gateway_service(request)

        # 将响应对象转换为JSON字符串并返回
        return json.dumps(response.to_dict(), ensure_ascii=False)
    except Exception as e:
        logger.error(
            f"Failed to create VeApig serverless gateway service with name {service_name}: {str(e)}"
        )
        return f"Failed to create VeApig serverless gateway service with name {service_name}: {str(e)}"
