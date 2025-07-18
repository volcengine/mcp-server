import volcenginesdkcore
from .configs import get_vpc_service_endpoint_by_region, vpc_supported_regions
from volcenginesdkvpc.api.vpc_api import VPCApi
from volcenginesdkvpc.models import DescribeVpcsRequest, DescribeVpcsResponse, \
    DescribeSubnetsRequest, DescribeSubnetsResponse

class VpcSDK:
    """初始化 Volcano VPC SDK Client"""

    def __init__(self, region: str = None, ak: str = None, sk: str = None, host: str = None):
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = ak
        configuration.sk = sk
        configuration.region = region
        if region not in vpc_supported_regions:
            raise Exception(f"Vpc is not supported in region {region}.")
        if host is not None:
            configuration.host = host
        else:
            configuration.host = get_vpc_service_endpoint_by_region(region)
        self.client = VPCApi(volcenginesdkcore.ApiClient(configuration))

    def describe_vpcs(self, args:dict) -> DescribeVpcsResponse:
        return self.client.describe_vpcs(DescribeVpcsRequest(**args))

    def describe_subnets(self, args:dict) -> DescribeSubnetsResponse:
        return self.client.describe_subnets(DescribeSubnetsRequest(**args))