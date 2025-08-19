import volcenginesdkcore

from mcp_server_cen.base.config import CEN_CONFIG
from volcenginesdkcen.api.cen_api import CENApi
from volcenginesdkcen.models import DescribeCensRequest, DescribeCensResponse, \
        DescribeCenAttributesRequest, DescribeCenAttributesResponse, \
        DescribeInstanceGrantedRulesRequest, DescribeInstanceGrantedRulesResponse, \
        DescribeGrantRulesToCenRequest, DescribeGrantRulesToCenResponse, \
        DescribeCenAttachedInstanceAttributesRequest, DescribeCenAttachedInstanceAttributesResponse, \
        DescribeCenAttachedInstancesRequest, DescribeCenAttachedInstancesResponse, \
        DescribeCenBandwidthPackagesRequest, DescribeCenBandwidthPackagesResponse, \
        DescribeCenBandwidthPackageAttributesRequest, DescribeCenBandwidthPackageAttributesResponse, \
        DescribeCenInterRegionBandwidthAttributesRequest, DescribeCenInterRegionBandwidthAttributesResponse, \
        DescribeCenInterRegionBandwidthsRequest, DescribeCenInterRegionBandwidthsResponse, \
        DescribeCenServiceRouteEntriesRequest, DescribeCenServiceRouteEntriesResponse, \
        DescribeCenRouteEntriesRequest, DescribeCenRouteEntriesResponse, \
        DescribeCenSummaryRouteEntriesRequest, DescribeCenSummaryRouteEntriesResponse


class CENSDK:
    """初始化 Volc CEN SDK client"""

    def __init__(self):
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = CEN_CONFIG.access_key
        configuration.sk = CEN_CONFIG.secret_key
        configuration.region = CEN_CONFIG.region
        if CEN_CONFIG.host is not None:
            configuration.host = CEN_CONFIG.host
        self.client = CENApi(volcenginesdkcore.ApiClient(configuration))

    def describe_cens(self, args: dict) -> DescribeCensResponse:
        return self.client.describe_cens(DescribeCensRequest(**args))

    def describe_cen_attributes(self, args: dict) -> DescribeCenAttributesResponse:
        return self.client.describe_cen_attributes(DescribeCenAttributesRequest(**args))

    def describe_instance_granted_rules(self, args: dict) -> DescribeInstanceGrantedRulesResponse:
        return self.client.describe_instance_granted_rules(DescribeInstanceGrantedRulesRequest(**args))

    def describe_grant_rules_to_cen(self, args: dict) -> DescribeGrantRulesToCenResponse:
        return self.client.describe_grant_rules_to_cen(DescribeGrantRulesToCenRequest(**args))
    
    def describe_cen_attached_instance_attributes(self, args: dict) -> DescribeCenAttachedInstanceAttributesResponse:
        return self.client.describe_cen_attached_instance_attributes(DescribeCenAttachedInstanceAttributesRequest(**args))
    
    def describe_cen_attached_instances(self, args: dict) -> DescribeCenAttachedInstancesResponse:
        return self.client.describe_cen_attached_instances(DescribeCenAttachedInstancesRequest(**args))
    
    def describe_cen_bandwidth_packages(self, args: dict) -> DescribeCenBandwidthPackagesResponse:
        return self.client.describe_cen_bandwidth_packages(DescribeCenBandwidthPackagesRequest(**args))
    
    def describe_cen_bandwidth_package_attributes(self, args: dict) -> DescribeCenBandwidthPackageAttributesResponse:
        return self.client.describe_cen_bandwidth_package_attributes(DescribeCenBandwidthPackageAttributesRequest(**args))
    
    # def describe_cen_bandwidth_packages_billing(self, args: dict) -> DescribeCenBandwidthPackagesBillingResponse:
    #     return self.client.describe_cen_bandwidth_packages_billing(DescribeCenBandwidthPackagesBillingRequest(**args))
    
    def describe_cen_inter_region_bandwidth_attributes(self, args: dict) -> DescribeCenInterRegionBandwidthAttributesResponse:
        return self.client.describe_cen_inter_region_bandwidth_attributes(DescribeCenInterRegionBandwidthAttributesRequest(**args))
    
    def describe_cen_inter_region_bandwidths(self, args: dict) -> DescribeCenInterRegionBandwidthsResponse:
        return self.client.describe_cen_inter_region_bandwidths(DescribeCenInterRegionBandwidthsRequest(**args))
    
    def describe_cen_service_route_entries(self, args: dict) -> DescribeCenServiceRouteEntriesResponse:
        return self.client.describe_cen_service_route_entries(DescribeCenServiceRouteEntriesRequest(**args))
    
    def describe_cen_route_entries(self, args: dict) -> DescribeCenRouteEntriesResponse:
        return self.client.describe_cen_route_entries(DescribeCenRouteEntriesRequest(**args))
    
    def describe_cen_summary_route_entries(self, args: dict) -> DescribeCenSummaryRouteEntriesResponse:
        return self.client.describe_cen_summary_route_entries(DescribeCenSummaryRouteEntriesRequest(**args))