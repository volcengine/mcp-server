from volcengine.ServiceInfo import ServiceInfo
from volcengine.Credentials import Credentials
from volcengine.ApiInfo import ApiInfo

api_info = {
    "McpDescribeLiveStreamCountData": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeLiveStreamCountData", "Version": "2023-01-01"},
        {},
        {},
    ),
    "McpDescribeLiveBatchStreamTrafficData": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeLiveBatchStreamTrafficData", "Version": "2023-01-01"},
        {},
        {},
    ),
    "McpDescribeLiveSourceTrafficData": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeLiveSourceTrafficData", "Version": "2023-01-01"},
        {},
        {},
    ),
    "McpDescribeLiveStreamSessionData": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeLiveStreamSessionData", "Version": "2023-01-01"},
        {},
        {},
    ),
    "McpDescribeLivePlayStatusCodeData": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeLivePlayStatusCodeData", "Version": "2023-01-01"},
        {},
        {},
    ),
    "McpDescribeLivePushStreamMetrics": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeLivePushStreamMetrics", "Version": "2023-01-01"},
        {},
        {},
    ),
    "McpDescribeLiveSourceStreamMetrics": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeLiveSourceStreamMetrics", "Version": "2023-01-01"},
        {},
        {},
    ),
    "McpDescribeLiveBatchStreamTranscodeData": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeLiveBatchStreamTranscodeData", "Version": "2023-01-01"},
        {},
        {},
    ),
    "McpDescribeLiveBatchPushStreamMetrics": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeLiveBatchPushStreamMetrics", "Version": "2023-01-01"},
        {},
        {},
    ),
    "McpDescribeLiveBatchSourceStreamMetrics": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeLiveBatchSourceStreamMetrics", "Version": "2023-01-01"},
        {},
        {},
    ),
    "McpDescribeIpInfo": ApiInfo(
        "POST", "/", {"Action": "DescribeIpInfo", "Version": "2023-01-01"}, {}, {}
    ),
    "McpGeneratePlayURL": ApiInfo(
        "POST", "/", {"Action": "GeneratePlayURL", "Version": "2023-01-01"}, {}, {}
    ),
    "McpGeneratePushURL": ApiInfo(
        "POST", "/", {"Action": "GeneratePushURL", "Version": "2023-01-01"}, {}, {}
    ),
    "McpDescribeDomain": ApiInfo(
        "POST", "/", {"Action": "DescribeDomain", "Version": "2023-01-01"}, {}, {}
    ),
    "McpListDomainDetail": ApiInfo(
        "POST", "/", {"Action": "ListDomainDetail", "Version": "2023-01-01"}, {}, {}
    ),
    "McpDescribeLiveISPData": ApiInfo(
        "POST", "/", {"Action": "DescribeLiveISPData", "Version": "2023-01-01"}, {}, {}
    ),
    "McpDescribeLiveRegionData": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeLiveRegionData", "Version": "2023-01-01"},
        {},
        {},
    ),
    "McpDescribeLivePushStreamInfoData": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeLivePushStreamInfoData", "Version": "2023-01-01"},
        {},
        {},
    ),
    "McpDescribeLiveTranscodeInfoData": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeLiveTranscodeInfoData", "Version": "2023-01-01"},
        {},
        {},
    ),
    "McpDescribeLiveBatchStreamSessionData": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeLiveBatchStreamSessionData", "Version": "2023-01-01"},
        {},
        {},
    ),
    "McpDescribeLiveTopPlayData": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeLiveTopPlayData", "Version": "2023-01-01"},
        {},
        {},
    ),
    "McpDescribeLiveEdgeStatData": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeLiveEdgeStatData", "Version": "2023-01-01"},
        {},
        {},
    ),
}
service_info_map = {
    "cn-north-1": ServiceInfo(
        "live.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "live", "cn-north-1"),
        60,
        60,
        "https",
    ),
}
