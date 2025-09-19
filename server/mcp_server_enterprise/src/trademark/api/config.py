from volcengine.ServiceInfo import ServiceInfo
from volcengine.Credentials import Credentials
from volcengine.ApiInfo import ApiInfo

api_info = {
    "McpGetApplicant": ApiInfo(
        "GET", "/", {"Action": "GetApplicant", "Version": "2023-06-01"}, {}, {}
    ),
    "McpGetTrademark": ApiInfo(
        "GET", "/", {"Action": "GetTrademark", "Version": "2023-06-01"}, {}, {}
    ),
    "McpListApplicants": ApiInfo(
        "GET", "/", {"Action": "ListApplicants", "Version": "2023-06-01"}, {}, {}
    ),
    "McpGetRequirement": ApiInfo(
        "GET", "/", {"Action": "GetRequirement", "Version": "2023-06-01"}, {}, {}
    ),
    "McpListRequirements": ApiInfo(
        "GET", "/", {"Action": "ListRequirements", "Version": "2023-06-01"}, {}, {}
    ),
    "McpListTrademarks": ApiInfo(
        "GET", "/", {"Action": "ListTrademarks", "Version": "2023-06-01"}, {}, {}
    ),
    "McpSearchTrademarkInfo": ApiInfo(
        "POST", "/", {"Action": "SearchTrademarkInfo", "Version": "2023-06-01"}, {}, {}
    ),
    "McpSearchTrademark": ApiInfo(
        "POST", "/", {"Action": "SearchTrademark", "Version": "2023-06-01"}, {}, {}
    ),
    "McpListBarrierTrademarks": ApiInfo(
        "GET", "/", {"Action": "ListBarrierTrademarks", "Version": "2023-06-01"}, {}, {}
    ),
}
service_info_map = {
    "cn-north-1": ServiceInfo(
        "open.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "trademark", "cn-north-1"),
        60,
        60,
        "http",
    ),
}
