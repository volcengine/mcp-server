import volcenginesdkcore

from mcp_server_eip.base.config import EIP_CONFIG
from volcenginesdkvpc.api.vpc_api import VPCApi
from volcenginesdkvpc.models import DescribeEipAddressesRequest, DescribeEipAddressesResponse, \
    DescribeEipAddressAttributesRequest, DescribeEipAddressAttributesResponse, \
    DescribeBandwidthPackagesRequest, DescribeBandwidthPackagesResponse


class EIPSDK:
    """初始化 Volc EIP SDK client"""

    def __init__(self):
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = EIP_CONFIG.access_key
        configuration.sk = EIP_CONFIG.secret_key
        configuration.region = EIP_CONFIG.region
        if EIP_CONFIG.host is not None:
            configuration.host = EIP_CONFIG.host
        self.client = VPCApi(volcenginesdkcore.ApiClient(configuration))

    def describe_eip_address_attributes(self, args: dict) -> DescribeEipAddressAttributesResponse:
        return self.client.describe_eip_address_attributes(DescribeEipAddressAttributesRequest(**args))

    def describe_eip_addresses(self, args: dict) -> DescribeEipAddressesResponse:
        return self.client.describe_eip_addresses(DescribeEipAddressesRequest(**args))

    def describe_bandwidth_packages(self, args: dict) -> DescribeBandwidthPackagesResponse:
        return self.client.describe_bandwidth_packages(DescribeBandwidthPackagesRequest(**args))
