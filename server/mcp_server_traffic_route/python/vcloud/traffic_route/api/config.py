from volcengine.ServiceInfo import ServiceInfo
from volcengine.Credentials import Credentials
from volcengine.ApiInfo import ApiInfo

api_info = {
    "McpListZones": ApiInfo(
        "POST", "/", {"Action": "ListZones", "Version": "2018-08-01"}, {}, {}
    ),
    "McpCreateZone": ApiInfo(
        "POST", "/", {"Action": "CreateZone", "Version": "2018-08-01"}, {}, {}
    ),
    "McpCreateRecord": ApiInfo(
        "POST", "/", {"Action": "CreateRecord", "Version": "2018-08-01"}, {}, {}
    ),
    "McpUpdateRecord": ApiInfo(
        "POST", "/", {"Action": "UpdateRecord", "Version": "2018-08-01"}, {}, {}
    ),
    "McpListRecords": ApiInfo(
        "POST", "/", {"Action": "ListRecords", "Version": "2018-08-01"}, {}, {}
    ),
}
service_info_map = {
    "cn-north-1": ServiceInfo(
        "dns.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "dns", "cn-north-1"),
        60,
        60,
        "http",
    ),
}
