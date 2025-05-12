from volcengine.ServiceInfo import ServiceInfo
from volcengine.Credentials import Credentials
from volcengine.ApiInfo import ApiInfo

api_info = {
    "McpCheckFee": ApiInfo(
        "GET", "/", {"Action": "CheckFee", "Version": "2022-12-12"}, {}, {}
    ),
    "McpGetDomain": ApiInfo(
        "GET", "/", {"Action": "GetDomain", "Version": "2022-12-12"}, {}, {}
    ),
    "McpGetAsyncTask": ApiInfo(
        "GET", "/", {"Action": "GetAsyncTask", "Version": "2022-12-12"}, {}, {}
    ),
    "McpGetTemplate": ApiInfo(
        "GET", "/", {"Action": "GetTemplate", "Version": "2022-12-12"}, {}, {}
    ),
    "McpListDomains": ApiInfo(
        "GET", "/", {"Action": "ListDomains", "Version": "2022-12-12"}, {}, {}
    ),
    "McpListTemplates": ApiInfo(
        "GET", "/", {"Action": "ListTemplates", "Version": "2022-12-12"}, {}, {}
    ),
    "McpRegisterDomain": ApiInfo(
        "POST", "/", {"Action": "RegisterDomain", "Version": "2022-12-12"}, {}, {}
    ),
}
service_info_map = {
    "cn-north-1": ServiceInfo(
        "open.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "domain_openapi", "cn-north-1"),
        60,
        60,
        "http",
    ),
}
