from volcengine.ServiceInfo import ServiceInfo
from volcengine.Credentials import Credentials
from volcengine.ApiInfo import ApiInfo

api_info = {
    "McpListCloudAccounts": ApiInfo(
        "POST", "/", {"Action": "ListCloudAccounts", "Version": "2022-03-01"}, {}, {}
    ),
    "McpListCdnDomains": ApiInfo(
        "POST", "/", {"Action": "ListCdnDomains", "Version": "2022-03-01"}, {}, {}
    ),
    "McpDescribeCdnDomainConfig": ApiInfo(
        "GET",
        "/",
        {"Action": "DescribeCdnDomainConfig", "Version": "2022-03-01"},
        {},
        {},
    ),
    "McpDescribeCdnAccessLog": ApiInfo(
        "POST", "/", {"Action": "DescribeCdnAccessLog", "Version": "2022-03-01"}, {}, {}
    ),
    "McpDescribeCdnRegionAndIsp": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeCdnRegionAndIsp", "Version": "2022-03-01"},
        {},
        {},
    ),
    "McpDescribeCdnDataOffline": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeCdnDataOffline", "Version": "2022-03-01"},
        {},
        {},
    ),
    "McpDescribeCdnOriginDataOffline": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeCdnOriginDataOffline", "Version": "2022-03-01"},
        {},
        {},
    ),
}
service_info_map = {
    "cn-north-1": ServiceInfo(
        "open.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "mcdn", "cn-north-1"),
        60,
        60,
        "http",
    ),
}
