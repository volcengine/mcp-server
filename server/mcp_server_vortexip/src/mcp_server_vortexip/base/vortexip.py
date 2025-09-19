import volcenginesdkcore

from mcp_server_vortexip.base.config import VortexIP_CONFIG

from volcenginesdkfasttrack.api.fasttrack_api import FASTTRACKApi
from volcenginesdkfasttrack.models import DescribeVortexIPAttributesRequest, DescribeVortexIPAttributesResponse, \
    DescribeWebScraperAttributesRequest, DescribeWebScraperAttributesResponse


class VortexIPSDK:
    """初始化 volc VortexIPSDK client"""

    def __init__(self):
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = VortexIP_CONFIG.access_key
        configuration.sk = VortexIP_CONFIG.secret_key
        configuration.region = VortexIP_CONFIG.region
        if VortexIP_CONFIG.host is not None:
            configuration.host = VortexIP_CONFIG.host
        self.client = FASTTRACKApi(volcenginesdkcore.ApiClient(configuration))

    def describe_vortex_ip_attributes(self, args: dict) -> DescribeVortexIPAttributesResponse:
        return self.client.describe_vortex_ip_attributes(DescribeVortexIPAttributesRequest(**args))

    def describe_web_scraper_attributes(self, args: dict) -> DescribeWebScraperAttributesResponse:
        return self.client.describe_web_scraper_attributes(DescribeWebScraperAttributesRequest(**args))

