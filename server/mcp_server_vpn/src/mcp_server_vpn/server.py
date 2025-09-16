import base64
import binascii
import json
import logging
import os
from functools import wraps
from typing import Callable, Awaitable

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from starlette.requests import Request
from mcp.types import CallToolResult, TextContent
from volcenginesdkvpn.models import (
    DescribeVpnConnectionAttributesRequest,
    DescribeVpnConnectionsRequest,
    DescribeVpnGatewayAttributesRequest,
    DescribeVpnGatewaysRequest,
    DescribeVpnGatewayRouteAttributesRequest,
    DescribeVpnGatewayRoutesRequest,
    DescribeCustomerGatewaysRequest,
    DescribeSslVpnClientCertAttributesRequest,
    DescribeSslVpnClientCertsRequest,
    DescribeSslVpnServersRequest,
)

from .clients import VPNClient
from .clients.models import (
    DescribeVpnGatewayAttributesResponse,
    DescribeVpnConnectionsResponse,
    DescribeVpnConnectionAttributesResponse,
    DescribeVpnGatewaysResponse,
    DescribeVpnGatewayRouteAttributesResponse,
    DescribeVpnGatewayRoutesResponse,
    DescribeCustomerGatewaysResponse,
    DescribeSslVpnClientCertAttributesResponse,
    DescribeSslVpnClientCertsResponse,
    DescribeSslVpnServersResponse,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
)
logger = logging.getLogger(__name__)

mcp = FastMCP("VPN MCP Server", port=int(os.getenv("PORT", "8000")))


def handle_errors(func: Callable[..., Awaitable]):
    @wraps(func)
    async def _wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as exc:
            return CallToolResult(
                isError=True,
                content=[TextContent(type="text", text=f"凭证缺失：{exc}")],
            )
        except Exception as exc:
            logger.exception("Unhandled error in %s", func.__name__)
            return CallToolResult(
                isError=True,
                content=[TextContent(type="text", text=f"查询失败：{exc}")],
            )

    return _wrapper


def _read_sts() -> dict:
    """Read STS credentials from the request header or environment."""
    ctx: Context[ServerSession, object, Request] = mcp.get_context()
    req: Request | None = ctx.request_context.request
    auth = (req.headers.get("authorization") if req else None) or os.getenv(
        "authorization"
    )
    if not auth:
        raise ValueError("Missing authorization")
    _, b64 = auth.split(" ", 1) if " " in auth else ("", auth)
    decoded = base64.b64decode(b64)
    return json.loads(decoded)


_CLIENT_CACHE: dict[tuple[str | None, str | None], VPNClient] = {}


def _get_vpn_client(region: str | None = None) -> VPNClient:
    """Create or reuse a VPN client instance using STS credentials."""
    creds = {}
    try:
        creds = _read_sts()
    except (ValueError, binascii.Error, json.JSONDecodeError):
        # Fallback to environment variables when STS header missing
        pass

    ak = creds.get("AccessKeyId") or os.getenv("VOLCENGINE_ACCESS_KEY")
    sk = creds.get("SecretAccessKey") or os.getenv("VOLCENGINE_SECRET_KEY")
    region = region or os.getenv("VOLCENGINE_REGION")
    host = os.getenv("VOLCENGINE_ENDPOINT")
    if not ak or not sk or not region:
        missing = []
        if not ak:
            missing.append("AccessKeyId")
        if not sk:
            missing.append("SecretAccessKey")
        if not region:
            missing.append("Region")
        raise ValueError(f"Missing required credentials: {', '.join(missing)}")
    key = (ak, region)

    client = _CLIENT_CACHE.get(key)
    if client is None:
        endpoint = host or "open.volcengineapi.com"
        client = VPNClient(
            region=region,
            endpoint=endpoint,
            ak=ak,
            sk=sk,
        )
        _CLIENT_CACHE[key] = client
    return client


@mcp.tool(description="Call the DescribeVpnConnectionAttributes action to query a specified Internet Protocol "
                      "Security (IPsec)-Virtual Private Network (VPN) connection.")
@handle_errors
async def describe_vpn_connection_attributes(
        vpn_connection_id: str,
        region: str | None = None,
) -> DescribeVpnConnectionAttributesResponse | CallToolResult:
    req = DescribeVpnConnectionAttributesRequest(vpn_connection_id=vpn_connection_id)
    vpn_client = _get_vpn_client(region=region)
    return vpn_client.describe_vpn_connection_attributes(req)


@mcp.tool(description="Call the DescribeVpnGatewayAttributes action to view the information of a specified Virtual "
                      "Private Network (VPN) gateway.")
@handle_errors
async def describe_vpn_gateway_attributes(
        vpn_gateway_id: str,
        region: str | None = None,
) -> DescribeVpnGatewayAttributesResponse | CallToolResult:
    req = DescribeVpnGatewayAttributesRequest(vpn_gateway_id=vpn_gateway_id)
    vpn_client = _get_vpn_client(region=region)
    return vpn_client.describe_vpn_gateway_attributes(req)


@mcp.tool(description="Call the DescribeVpnGatewayRouteAttributes action to query the information of route entries on "
                      "a specified Virtual Private Network (VPN) gateway.")
@handle_errors
async def describe_vpn_gateway_route_attributes(
        vpn_gateway_route_id: str,
        region: str | None = None,
) -> DescribeVpnGatewayRouteAttributesResponse | CallToolResult:
    req = DescribeVpnGatewayRouteAttributesRequest(
        vpn_gateway_route_id=vpn_gateway_route_id
    )
    vpn_client = _get_vpn_client(region=region)
    return vpn_client.describe_vpn_gateway_route_attributes(req)


@mcp.tool(description="Call the DescribeSslVpnClientCertAttributes action to query the information of a specified "
                      "Secure Sockets Layer (SSL) client certificate.")
@handle_errors
async def describe_ssl_vpn_client_cert_attributes(
        ssl_vpn_client_cert_id: str,
        region: str | None = None,
) -> DescribeSslVpnClientCertAttributesResponse | CallToolResult:
    req = DescribeSslVpnClientCertAttributesRequest(
        ssl_vpn_client_cert_id=ssl_vpn_client_cert_id
    )
    vpn_client = _get_vpn_client(region=region)
    return vpn_client.describe_ssl_vpn_client_cert_attributes(req)


@mcp.tool(description="Call the DescribeVpnGatewayRoutes action to query the information of destination-based route "
                      "entries on a Virtual Private Network (VPN) gateway based on conditions.")
@handle_errors
async def describe_vpn_gateway_routes(
        page_number: int | None = None,
        page_size: int | None = None,
        destination_cidr_block: str | None = None,
        next_hop_id: str | None = None,
        route_type: str | None = None,
        status: str | None = None,
        vpn_gateway_id: str | None = None,
        vpn_gateway_route_ids: list[str] | None = None,
        region: str | None = None,
) -> DescribeVpnGatewayRoutesResponse | CallToolResult:
    req = DescribeVpnGatewayRoutesRequest(
        page_number=page_number,
        page_size=page_size,
        destination_cidr_block=destination_cidr_block,
        next_hop_id=next_hop_id,
        route_type=route_type,
        status=status,
        vpn_gateway_id=vpn_gateway_id,
        vpn_gateway_route_ids=vpn_gateway_route_ids,
    )
    vpn_client = _get_vpn_client(region=region)
    return vpn_client.describe_vpn_gateway_routes(req)


@mcp.tool(description="Call the DescribeVpnConnections action to query Internet Protocol Security (IPsec)-Virtual "
                      "Private Network (VPN) connections that meet the specified conditions.")
@handle_errors
async def describe_vpn_connections(
        page_number: int | None = None,
        page_size: int | None = None,
        vpn_gateway_id: str | None = None,
        vpn_connection_name: str | None = None,
        status: str | None = None,
        region: str | None = None,
) -> DescribeVpnConnectionsResponse | CallToolResult:
    req = DescribeVpnConnectionsRequest(
        page_number=page_number,
        page_size=page_size,
        vpn_gateway_id=vpn_gateway_id,
        vpn_connection_name=vpn_connection_name,
        status=status,
    )
    vpn_client = _get_vpn_client(region=region)
    return vpn_client.describe_vpn_connections(req)


@mcp.tool(description="Call the DescribeVpnGateways action to query the information of Virtual Private Network (VPN) "
                      "gateways that meet the specified conditions.")
@handle_errors
async def describe_vpn_gateways(
        page_number: int | None = None,
        page_size: int | None = None,
        ip_address: str | None = None,
        ssl_enabled: bool | None = None,
        subnet_id: str | None = None,
        vpc_id: str | None = None,
        vpn_gateway_name: str | None = None,
        ipsec_enabled: bool | None = None,
        project_name: str | None = None,
        vpn_gateway_ids: list[str] | None = None,
        tag_filters: list[dict] | None = None,
        region: str | None = None,
) -> DescribeVpnGatewaysResponse | CallToolResult:
    req = DescribeVpnGatewaysRequest(
        page_number=page_number,
        page_size=page_size,
        ip_address=ip_address,
        ssl_enabled=ssl_enabled,
        subnet_id=subnet_id,
        vpc_id=vpc_id,
        vpn_gateway_name=vpn_gateway_name,
        ipsec_enabled=ipsec_enabled,
        project_name=project_name,
        vpn_gateway_ids=vpn_gateway_ids,
        tag_filters=tag_filters,
    )
    vpn_client = _get_vpn_client(region=region)
    return vpn_client.describe_vpn_gateways(req)


@mcp.tool(description="Call the DescribeCustomerGateways action to query the information of customer gateways based "
                      "on specified conditions.")
@handle_errors
async def describe_customer_gateways(
        page_number: int | None = None,
        page_size: int | None = None,
        customer_gateway_name: str | None = None,
        ip_address: str | None = None,
        status: str | None = None,
        project_name: str | None = None,
        customer_gateway_ids: list[str] | None = None,
        region: str | None = None,
) -> DescribeCustomerGatewaysResponse | CallToolResult:
    req = DescribeCustomerGatewaysRequest(
        page_number=page_number,
        page_size=page_size,
        customer_gateway_name=customer_gateway_name,
        ip_address=ip_address,
        status=status,
        project_name=project_name,
        customer_gateway_ids=customer_gateway_ids,
    )
    vpn_client = _get_vpn_client(region=region)
    return vpn_client.describe_customer_gateways(req)


@mcp.tool(description="Call the DescribeSslVpnClientCerts action to query the information of Secure Sockets Layer ("
                      "SSL) client certificates based on conditions.")
@handle_errors
async def describe_ssl_vpn_client_certs(
        page_number: int | None = None,
        page_size: int | None = None,
        ssl_vpn_client_cert_ids: list[str] | None = None,
        ssl_vpn_client_cert_name: str | None = None,
        ssl_vpn_server_id: str | None = None,
        region: str | None = None,
) -> DescribeSslVpnClientCertsResponse | CallToolResult:
    req = DescribeSslVpnClientCertsRequest(
        page_number=page_number,
        page_size=page_size,
        ssl_vpn_client_cert_ids=ssl_vpn_client_cert_ids,
        ssl_vpn_client_cert_name=ssl_vpn_client_cert_name,
        ssl_vpn_server_id=ssl_vpn_server_id,
    )
    vpn_client = _get_vpn_client(region=region)
    return  vpn_client.describe_ssl_vpn_client_certs(req)


@mcp.tool(description="Call the DescribeSslVpnServers action to query the information of Secure Sockets Layer (SSL) "
                      "servers.")
@handle_errors
async def describe_ssl_vpn_servers(
        page_number: int | None = None,
        page_size: int | None = None,
        project_name: str | None = None,
        vpn_gateway_id: str | None = None,
        ssl_vpn_server_name: str | None = None,
        ssl_vpn_server_ids: list[str] | None = None,
        region: str | None = None,
) -> DescribeSslVpnServersResponse | CallToolResult:
    req = DescribeSslVpnServersRequest(
        page_number=page_number,
        page_size=page_size,
        project_name=project_name,
        vpn_gateway_id=vpn_gateway_id,
        ssl_vpn_server_name=ssl_vpn_server_name,
        ssl_vpn_server_ids=ssl_vpn_server_ids,
    )
    vpn_client = _get_vpn_client(region=region)
    return vpn_client.describe_ssl_vpn_servers(req)
