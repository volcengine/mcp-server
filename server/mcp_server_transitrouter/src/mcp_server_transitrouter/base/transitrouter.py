import volcenginesdkcore

from mcp_server_transitrouter.base.config import TR_CONFIG
from volcenginesdktransitrouter.api.transitrouter_api import TRANSITROUTERApi

from volcenginesdktransitrouter.models import DescribeTransitRoutersRequest, DescribeTransitRoutersResponse, \
    DescribeTransitRouterAttachmentsRequest, DescribeTransitRouterAttachmentsResponse, \
    DescribeTransitRouterVpcAttachmentsRequest, DescribeTransitRouterVpcAttachmentsResponse, \
    DescribeTransitRouterVpnAttachmentsRequest, DescribeTransitRouterVpnAttachmentsResponse, \
    DescribeTransitRouterDirectConnectGatewayAttachmentsRequest, DescribeTransitRouterDirectConnectGatewayAttachmentsResponse, \
    DescribeTransitRouterBandwidthPackagesRequest, DescribeTransitRouterBandwidthPackagesResponse, \
    DescribeTransitRouterRegionsRequest, DescribeTransitRouterRegionsResponse, \
    DescribeTransitRouterBandwidthPackagesBillingRequest, DescribeTransitRouterBandwidthPackagesBillingResponse, \
    DescribeTransitRouterPeerAttachmentsRequest, DescribeTransitRouterPeerAttachmentsResponse, \
    DescribeTransitRouterRouteTablesRequest, DescribeTransitRouterRouteTablesResponse, \
    DescribeTransitRouterRouteEntriesRequest, DescribeTransitRouterRouteEntriesResponse, \
    DescribeTransitRouterRouteTableAssociationsRequest, DescribeTransitRouterRouteTableAssociationsResponse, \
    DescribeTransitRouterRouteTablePropagationsRequest, DescribeTransitRouterRouteTablePropagationsResponse, \
    DescribeTransitRouterRoutePolicyEntriesRequest, DescribeTransitRouterRoutePolicyEntriesResponse, \
    DescribeTransitRouterRoutePolicyTablesRequest, DescribeTransitRouterRoutePolicyTablesResponse, \
    DescribeTransitRouterForwardPolicyEntriesRequest, DescribeTransitRouterForwardPolicyEntriesResponse, \
    DescribeTransitRouterForwardPolicyTablesRequest, DescribeTransitRouterForwardPolicyTablesResponse, \
    DescribeTransitRouterTrafficQosMarkingPoliciesRequest, DescribeTransitRouterTrafficQosMarkingPoliciesResponse, \
    DescribeTransitRouterTrafficQosMarkingEntriesRequest, DescribeTransitRouterTrafficQosMarkingEntriesResponse, \
    DescribeTransitRouterTrafficQosQueuePoliciesRequest, DescribeTransitRouterTrafficQosQueuePoliciesResponse, \
    DescribeTransitRouterTrafficQosQueueEntriesRequest, DescribeTransitRouterTrafficQosQueueEntriesResponse


class TRSDK:
    """初始化 Volc TR SDK client"""

    def __init__(self):
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = TR_CONFIG.access_key
        configuration.sk = TR_CONFIG.secret_key
        configuration.region = TR_CONFIG.region
        if TR_CONFIG.host is not None:
            configuration.host = TR_CONFIG.host
        self.client = TRANSITROUTERApi(volcenginesdkcore.ApiClient(configuration))

    def describe_transit_routers(self, args: dict) -> DescribeTransitRoutersResponse:
        return self.client.describe_transit_routers(DescribeTransitRoutersRequest(**args))

    def describe_transit_router_attachments(self, args: dict) -> DescribeTransitRouterAttachmentsResponse:
        return self.client.describe_transit_router_attachments(DescribeTransitRouterAttachmentsRequest(**args))

    def describe_transit_router_vpc_attachments(self, args: dict) -> DescribeTransitRouterVpcAttachmentsResponse:
        return self.client.describe_transit_router_vpc_attachments(DescribeTransitRouterVpcAttachmentsRequest(**args))

    def describe_transit_router_vpn_attachments(self, args: dict) -> DescribeTransitRouterVpnAttachmentsResponse:
        return self.client.describe_transit_router_vpn_attachments(DescribeTransitRouterVpnAttachmentsRequest(**args))

    def describe_transit_router_direct_connect_gateway_attachments(self, args: dict) -> DescribeTransitRouterDirectConnectGatewayAttachmentsResponse:
        return self.client.describe_transit_router_direct_connect_gateway_attachments(DescribeTransitRouterDirectConnectGatewayAttachmentsRequest(**args))

    def describe_transit_router_bandwidth_packages(self, args: dict) -> DescribeTransitRouterBandwidthPackagesResponse:
        return self.client.describe_transit_router_bandwidth_packages(DescribeTransitRouterBandwidthPackagesRequest(**args))

    def describe_transit_router_regions(self, args: dict) -> DescribeTransitRouterRegionsResponse:
        return self.client.describe_transit_router_regions(DescribeTransitRouterRegionsRequest(**args))

    def describe_transit_router_bandwidth_packages_billing(self, args: dict) -> DescribeTransitRouterBandwidthPackagesBillingResponse:
        return self.client.describe_transit_router_bandwidth_packages_billing(DescribeTransitRouterBandwidthPackagesBillingRequest(**args))

    def describe_transit_router_peer_attachments(self, args: dict) -> DescribeTransitRouterPeerAttachmentsResponse:
        return self.client.describe_transit_router_peer_attachments(DescribeTransitRouterPeerAttachmentsRequest(**args))

    def describe_transit_router_route_tables(self, args: dict) -> DescribeTransitRouterRouteTablesResponse:
        return self.client.describe_transit_router_route_tables(DescribeTransitRouterRouteTablesRequest(**args))

    def describe_transit_router_route_entries(self, args: dict) -> DescribeTransitRouterRouteEntriesResponse:
        return self.client.describe_transit_router_route_entries(DescribeTransitRouterRouteEntriesRequest(**args))

    def describe_transit_router_route_table_associations(self, args: dict) -> DescribeTransitRouterRouteTableAssociationsResponse:
        return self.client.describe_transit_router_route_table_associations(DescribeTransitRouterRouteTableAssociationsRequest(**args))

    def describe_transit_router_route_table_propagations(self, args: dict) -> DescribeTransitRouterRouteTablePropagationsResponse:
        return self.client.describe_transit_router_route_table_propagations(DescribeTransitRouterRouteTablePropagationsRequest(**args))

    def describe_transit_router_route_policy_entries(self, args: dict) -> DescribeTransitRouterRoutePolicyEntriesResponse:
        return self.client.describe_transit_router_route_policy_entries(DescribeTransitRouterRoutePolicyEntriesRequest(**args))

    def describe_transit_router_route_policy_tables(self, args: dict) -> DescribeTransitRouterRoutePolicyTablesResponse:
        return self.client.describe_transit_router_route_policy_tables(DescribeTransitRouterRoutePolicyTablesRequest(**args))

    def describe_transit_router_forward_policy_entries(self, args: dict) -> DescribeTransitRouterForwardPolicyEntriesResponse:
        return self.client.describe_transit_router_forward_policy_entries(DescribeTransitRouterForwardPolicyEntriesRequest(**args))

    def describe_transit_router_forward_policy_tables(self, args: dict) -> DescribeTransitRouterForwardPolicyTablesResponse:
        return self.client.describe_transit_router_forward_policy_tables(DescribeTransitRouterForwardPolicyTablesRequest(**args))

    def describe_transit_router_traffic_qos_marking_policies(self, args: dict) -> DescribeTransitRouterTrafficQosMarkingPoliciesResponse:
        return self.client.describe_transit_router_traffic_qos_marking_policies(DescribeTransitRouterTrafficQosMarkingPoliciesRequest(**args))

    def describe_transit_router_traffic_qos_marking_entries(self, args: dict) -> DescribeTransitRouterTrafficQosMarkingEntriesResponse:
        return self.client.describe_transit_router_traffic_qos_marking_entries(DescribeTransitRouterTrafficQosMarkingEntriesRequest(**args))

    def describe_transit_router_traffic_qos_queue_policies(self, args: dict) -> DescribeTransitRouterTrafficQosQueuePoliciesResponse:
        return self.client.describe_transit_router_traffic_qos_queue_policies(DescribeTransitRouterTrafficQosQueuePoliciesRequest(**args))

    def describe_transit_router_traffic_qos_queue_entries(self, args: dict) -> DescribeTransitRouterTrafficQosQueueEntriesResponse:
        return self.client.describe_transit_router_traffic_qos_queue_entries(DescribeTransitRouterTrafficQosQueueEntriesRequest(**args))

                                            


