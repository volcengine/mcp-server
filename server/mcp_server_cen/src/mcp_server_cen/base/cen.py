import volcenginesdkcore

from mcp_server_cen.base.config import CEN_CONFIG
from volcenginesdkcen.api.cen_api import CENApi
from volcenginesdkcen.models import DescribeCensRequest, DescribeCensResponse, \
        DescribeCenAttributesRequest, DescribeCenAttributesResponse, \
        DescribeInstanceGrantedRulesRequest, DescribeInstanceGrantedRulesResponse, \
        DescribeGrantRulesToCenRequest, DescribeGrantRulesToCenResponse


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