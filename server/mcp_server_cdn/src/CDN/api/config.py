from volcengine.ServiceInfo import ServiceInfo
from volcengine.Credentials import Credentials
from volcengine.ApiInfo import ApiInfo

api_info = {
    "McpDescribeCdnConfig": ApiInfo(
        "POST", "/", {"Action": "DescribeCdnConfig", "Version": "2021-03-01"}, {}, {}
    ),
    "McpListCdnDomains": ApiInfo(
        "POST", "/", {"Action": "ListCdnDomains", "Version": "2021-03-01"}, {}, {}
    ),
    "McpDescribeOriginTopStatisticalData": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeOriginTopStatisticalData", "Version": "2021-03-01"},
        {},
        {},
    ),
    "McpDescribeDistrictData": ApiInfo(
        "POST", "/", {"Action": "DescribeDistrictData", "Version": "2021-03-01"}, {}, {}
    ),
    "McpDescribeDistrictRanking": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeDistrictRanking", "Version": "2021-03-01"},
        {},
        {},
    ),
    "McpDescribeEdgeStatusCodeRanking": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeEdgeStatusCodeRanking", "Version": "2021-03-01"},
        {},
        {},
    ),
    "McpDescribeDistrictSummary": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeDistrictSummary", "Version": "2021-03-01"},
        {},
        {},
    ),
    "McpDescribeOriginData": ApiInfo(
        "POST", "/", {"Action": "DescribeOriginData", "Version": "2021-03-01"}, {}, {}
    ),
    "McpDescribeEdgeRanking": ApiInfo(
        "POST", "/", {"Action": "DescribeEdgeRanking", "Version": "2021-03-01"}, {}, {}
    ),
    "McpDescribeEdgeData": ApiInfo(
        "POST", "/", {"Action": "DescribeEdgeData", "Version": "2021-03-01"}, {}, {}
    ),
    "McpDescribeEdgeSummary": ApiInfo(
        "POST", "/", {"Action": "DescribeEdgeSummary", "Version": "2021-03-01"}, {}, {}
    ),
    "McpDescribeOriginRanking": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeOriginRanking", "Version": "2021-03-01"},
        {},
        {},
    ),
    "McpDescribeStatisticalRanking": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeStatisticalRanking", "Version": "2021-03-01"},
        {},
        {},
    ),
    "McpDescribeOriginStatusCodeRanking": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeOriginStatusCodeRanking", "Version": "2021-03-01"},
        {},
        {},
    ),
    "McpDescribeUserData": ApiInfo(
        "POST", "/", {"Action": "DescribeUserData", "Version": "2021-03-01"}, {}, {}
    ),
    "McpDescribeOriginSummary": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeOriginSummary", "Version": "2021-03-01"},
        {},
        {},
    ),
}
service_info_map = {
    "cn-north-1": ServiceInfo(
        "cdn.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "CDN", "cn-north-1"),
        60,
        60,
        "http",
    ),
}
