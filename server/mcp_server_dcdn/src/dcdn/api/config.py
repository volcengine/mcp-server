from volcengine.ServiceInfo import ServiceInfo
from volcengine.Credentials import Credentials
from volcengine.ApiInfo import ApiInfo

api_info = {
    "McpListDomainConfig": ApiInfo(
        "POST", "/", {"Action": "ListDomainConfig", "Version": "2021-04-01"}, {}, {}
    ),
    "McpDescribeDcdnRegionAndIsp": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeDcdnRegionAndIsp", "Version": "2021-04-01"},
        {},
        {},
    ),
    "McpDescribeDomainIspData": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeDomainIspData", "Version": "2021-04-01"},
        {},
        {},
    ),
    "McpDescribeDomainPVData": ApiInfo(
        "POST", "/", {"Action": "DescribeDomainPVData", "Version": "2021-04-01"}, {}, {}
    ),
    "McpDescribeRealtimeData": ApiInfo(
        "POST", "/", {"Action": "DescribeRealtimeData", "Version": "2021-04-01"}, {}, {}
    ),
    "McpDescribeDomainUVData": ApiInfo(
        "POST", "/", {"Action": "DescribeDomainUVData", "Version": "2021-04-01"}, {}, {}
    ),
    "McpDescribeOriginStatisticsDetail": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeOriginStatisticsDetail", "Version": "2021-04-01"},
        {},
        {},
    ),
    "McpDescribeOriginRealtimeData": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeOriginRealtimeData", "Version": "2021-04-01"},
        {},
        {},
    ),
    "McpDescribeOriginStatistics": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeOriginStatistics", "Version": "2021-04-01"},
        {},
        {},
    ),
    "McpDescribeTopDomains": ApiInfo(
        "POST", "/", {"Action": "DescribeTopDomains", "Version": "2021-04-01"}, {}, {}
    ),
    "McpDescribeTopIPs": ApiInfo(
        "POST", "/", {"Action": "DescribeTopIPs", "Version": "2021-04-01"}, {}, {}
    ),
    "McpDescribeTopReferers": ApiInfo(
        "POST", "/", {"Action": "DescribeTopReferers", "Version": "2021-04-01"}, {}, {}
    ),
    "McpDescribeTopUrls": ApiInfo(
        "POST", "/", {"Action": "DescribeTopUrls", "Version": "2021-04-01"}, {}, {}
    ),
    "McpListCert": ApiInfo(
        "POST", "/", {"Action": "ListCert", "Version": "2021-04-01"}, {}, {}
    ),
    "McpListCertBind": ApiInfo(
        "POST", "/", {"Action": "ListCertBind", "Version": "2021-04-01"}, {}, {}
    ),
    "McpDescribeDomainRegionData": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeDomainRegionData", "Version": "2021-04-01"},
        {},
        {},
    ),
    "McpDescribeStatistics": ApiInfo(
        "POST", "/", {"Action": "DescribeStatistics", "Version": "2021-04-01"}, {}, {}
    ),
}
service_info_map = {
    "cn-north-1": ServiceInfo(
        "open.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "dcdn", "cn-north-1"),
        60,
        60,
        "http",
    ),
}
