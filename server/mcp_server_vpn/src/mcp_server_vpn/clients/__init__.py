from .base import BaseApi
from .vpn import VPNClient
from .models import (
    DescribeVpnConnectionAttributesResponse,
    DescribeVpnGatewayAttributesResponse,
    DescribeVpnConnectionsResponse,
    DescribeVpnGatewaysResponse,
    DescribeCustomerGatewaysResponse,
)

__all__ = [
    "BaseApi",
    "VPNClient",
    "DescribeVpnConnectionAttributesResponse",
    "DescribeVpnGatewayAttributesResponse",
    "DescribeVpnConnectionsResponse",
    "DescribeVpnGatewaysResponse",
    "DescribeCustomerGatewaysResponse",
]
