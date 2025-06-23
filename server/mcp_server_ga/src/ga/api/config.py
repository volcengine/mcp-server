from volcengine.ServiceInfo import ServiceInfo
from volcengine.Credentials import Credentials
from volcengine.ApiInfo import ApiInfo

api_info = {
    "McpDescribeAccelerator": ApiInfo(
        "POST", "/", {"Action": "DescribeAccelerator", "Version": "2022-03-01"}, {}, {}
    ),
    "McpDescribeBasicAccelerator": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeBasicAccelerator", "Version": "2022-03-01"},
        {},
        {},
    ),
    "McpDescribeBasicEndpointGroup": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeBasicEndpointGroup", "Version": "2022-03-01"},
        {},
        {},
    ),
    "McpDescribeBasicIPSet": ApiInfo(
        "POST", "/", {"Action": "DescribeBasicIPSet", "Version": "2022-03-01"}, {}, {}
    ),
    "McpDescribeEndpointGroup": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeEndpointGroup", "Version": "2022-03-01"},
        {},
        {},
    ),
    "McpDescribeIPSet": ApiInfo(
        "POST", "/", {"Action": "DescribeIPSet", "Version": "2022-03-01"}, {}, {}
    ),
    "McpDescribeListener": ApiInfo(
        "POST", "/", {"Action": "DescribeListener", "Version": "2022-03-01"}, {}, {}
    ),
    "McpDescribeListenerLogs": ApiInfo(
        "POST", "/", {"Action": "DescribeListenerLogs", "Version": "2022-03-01"}, {}, {}
    ),
    "McpDescribeStatistics": ApiInfo(
        "POST", "/", {"Action": "DescribeStatistics", "Version": "2022-03-01"}, {}, {}
    ),
    "McpDescribeTopStatistics": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeTopStatistics", "Version": "2022-03-01"},
        {},
        {},
    ),
    "McpGetAcceleratorDimension": ApiInfo(
        "POST",
        "/",
        {"Action": "GetAcceleratorDimension", "Version": "2022-03-01"},
        {},
        {},
    ),
    "McpGetBandwidthPackage": ApiInfo(
        "POST", "/", {"Action": "GetBandwidthPackage", "Version": "2022-03-01"}, {}, {}
    ),
    "McpGetBasicEndpointRelatedAccInstanceInfos": ApiInfo(
        "POST",
        "/",
        {"Action": "GetBasicEndpointRelatedAccInstanceInfos", "Version": "2022-03-01"},
        {},
        {},
    ),
    "McpGetEndpointRelatedAccInstanceInfos": ApiInfo(
        "POST",
        "/",
        {"Action": "GetEndpointRelatedAccInstanceInfos", "Version": "2022-03-01"},
        {},
        {},
    ),
    "McpListAccelerateAreas": ApiInfo(
        "GET", "/", {"Action": "ListAccelerateAreas", "Version": "2022-03-01"}, {}, {}
    ),
    "McpListAccelerators": ApiInfo(
        "POST", "/", {"Action": "ListAccelerators", "Version": "2022-03-01"}, {}, {}
    ),
    "McpListBandwidthPackages": ApiInfo(
        "POST",
        "/",
        {"Action": "ListBandwidthPackages", "Version": "2022-03-01"},
        {},
        {},
    ),
    "McpListBasicAccelerateIPs": ApiInfo(
        "POST",
        "/",
        {"Action": "ListBasicAccelerateIPs", "Version": "2022-03-01"},
        {},
        {},
    ),
    "McpListBasicAccelerators": ApiInfo(
        "POST",
        "/",
        {"Action": "ListBasicAccelerators", "Version": "2022-03-01"},
        {},
        {},
    ),
    "McpListBasicEndpointGroups": ApiInfo(
        "POST",
        "/",
        {"Action": "ListBasicEndpointGroups", "Version": "2022-03-01"},
        {},
        {},
    ),
    "McpListBasicEndpoints": ApiInfo(
        "POST", "/", {"Action": "ListBasicEndpoints", "Version": "2022-03-01"}, {}, {}
    ),
    "McpListBasicIPSets": ApiInfo(
        "POST", "/", {"Action": "ListBasicIPSets", "Version": "2022-03-01"}, {}, {}
    ),
    "McpListEndpointGroups": ApiInfo(
        "POST", "/", {"Action": "ListEndpointGroups", "Version": "2022-03-01"}, {}, {}
    ),
    "McpListListeners": ApiInfo(
        "POST", "/", {"Action": "ListListeners", "Version": "2022-03-01"}, {}, {}
    ),
}
service_info_map = {
    "cn-north-1": ServiceInfo(
        "open.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "ga", "cn-north-1"),
        60,
        60,
        "http",
    ),
}
