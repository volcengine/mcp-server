from volcengine.ApiInfo import ApiInfo

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

from .base import BaseApi
from .models import (
    DescribeVpnConnectionAttributesResponse,
    DescribeVpnGatewayAttributesResponse,
    DescribeVpnConnectionsResponse,
    DescribeVpnGatewaysResponse,
    DescribeVpnGatewayRouteAttributesResponse,
    DescribeVpnGatewayRoutesResponse,
    DescribeCustomerGatewaysResponse,
    DescribeSslVpnClientCertAttributesResponse,
    DescribeSslVpnClientCertsResponse,
    DescribeSslVpnServersResponse,
)


class VPNClient(BaseApi):
    """VPN client implemented using BaseApi."""

    def __init__(self, region: str, endpoint: str, ak: str, sk: str) -> None:
        api_infos = {
            "DescribeVpnConnectionAttributes": ApiInfo(
                "GET",
                "/",
                {"Action": "DescribeVpnConnectionAttributes", "Version": "2020-04-01"},
                {},
                {},
            ),
            "DescribeVpnGatewayAttributes": ApiInfo(
                "GET",
                "/",
                {"Action": "DescribeVpnGatewayAttributes", "Version": "2020-04-01"},
                {},
                {},
            ),
            "DescribeVpnConnections": ApiInfo(
                "GET",
                "/",
                {"Action": "DescribeVpnConnections", "Version": "2020-04-01"},
                {},
                {},
            ),
            "DescribeVpnGateways": ApiInfo(
                "GET",
                "/",
                {"Action": "DescribeVpnGateways", "Version": "2020-04-01"},
                {},
                {},
            ),
            "DescribeVpnGatewayRouteAttributes": ApiInfo(
                "GET",
                "/",
                {"Action": "DescribeVpnGatewayRouteAttributes", "Version": "2020-04-01"},
                {},
                {},
            ),
            "DescribeVpnGatewayRoutes": ApiInfo(
                "GET",
                "/",
                {"Action": "DescribeVpnGatewayRoutes", "Version": "2020-04-01"},
                {},
                {},
            ),
            "DescribeCustomerGateways": ApiInfo(
                "GET",
                "/",
                {"Action": "DescribeCustomerGateways", "Version": "2020-04-01"},
                {},
                {},
            ),
            "DescribeSslVpnClientCertAttributes": ApiInfo(
                "GET",
                "/",
                {"Action": "DescribeSslVpnClientCertAttributes", "Version": "2020-04-01"},
                {},
                {},
            ),
            "DescribeSslVpnClientCerts": ApiInfo(
                "GET",
                "/",
                {"Action": "DescribeSslVpnClientCerts", "Version": "2020-04-01"},
                {},
                {},
            ),
            "DescribeSslVpnServers": ApiInfo(
                "GET",
                "/",
                {"Action": "DescribeSslVpnServers", "Version": "2020-04-01"},
                {},
                {},
            ),
        }
        self.region = region
        super().__init__(region, endpoint, api_infos, "vpn", ak, sk)

    def describe_vpn_connection_attributes(
            self, request: DescribeVpnConnectionAttributesRequest
    ) -> DescribeVpnConnectionAttributesResponse:
        params = self.to_params(request)
        data = self.get("DescribeVpnConnectionAttributes", params)
        return DescribeVpnConnectionAttributesResponse(**data)

    def describe_vpn_gateway_attributes(
            self, request: DescribeVpnGatewayAttributesRequest
    ) -> DescribeVpnGatewayAttributesResponse:
        params = self.to_params(request)
        data = self.get("DescribeVpnGatewayAttributes", params)
        return DescribeVpnGatewayAttributesResponse(**data)

    def describe_vpn_connections(
            self, request: DescribeVpnConnectionsRequest
    ) -> DescribeVpnConnectionsResponse:
        params = self.to_params(request)
        data = self.get("DescribeVpnConnections", params)
        return DescribeVpnConnectionsResponse(**data)

    def describe_vpn_gateways(
            self, request: DescribeVpnGatewaysRequest
    ) -> DescribeVpnGatewaysResponse:
        params = self.to_params(request)
        data = self.get("DescribeVpnGateways", params)
        return DescribeVpnGatewaysResponse(**data)

    def describe_vpn_gateway_route_attributes(
            self, request: DescribeVpnGatewayRouteAttributesRequest
    ) -> DescribeVpnGatewayRouteAttributesResponse:
        params = self.to_params(request)
        data = self.get("DescribeVpnGatewayRouteAttributes", params)
        return DescribeVpnGatewayRouteAttributesResponse(**data)

    def describe_vpn_gateway_routes(
            self, request: DescribeVpnGatewayRoutesRequest
    ) -> DescribeVpnGatewayRoutesResponse:
        params = self.to_params(request)
        data = self.get("DescribeVpnGatewayRoutes", params)
        return DescribeVpnGatewayRoutesResponse(**data)

    def describe_customer_gateways(
            self, request: DescribeCustomerGatewaysRequest
    ) -> DescribeCustomerGatewaysResponse:
        params = self.to_params(request)
        data = self.get("DescribeCustomerGateways", params)
        return DescribeCustomerGatewaysResponse(**data)

    def describe_ssl_vpn_client_cert_attributes(
            self, request: DescribeSslVpnClientCertAttributesRequest
    ) -> DescribeSslVpnClientCertAttributesResponse:
        params = self.to_params(request)
        data = self.get("DescribeSslVpnClientCertAttributes", params)
        return DescribeSslVpnClientCertAttributesResponse(**data)

    def describe_ssl_vpn_client_certs(
            self, request: DescribeSslVpnClientCertsRequest
    ) -> DescribeSslVpnClientCertsResponse:
        params = self.to_params(request)
        data = self.get("DescribeSslVpnClientCerts", params)
        return DescribeSslVpnClientCertsResponse(**data)

    def describe_ssl_vpn_servers(
            self, request: DescribeSslVpnServersRequest
    ) -> DescribeSslVpnServersResponse:
        params = self.to_params(request)
        data = self.get("DescribeSslVpnServers", params)
        return DescribeSslVpnServersResponse(**data)
