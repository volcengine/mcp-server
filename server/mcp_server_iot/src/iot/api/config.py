from volcengine.ServiceInfo import ServiceInfo
from volcengine.Credentials import Credentials
from volcengine.ApiInfo import ApiInfo

api_info = {
    "McpCallService": ApiInfo(
        "POST", "/", {"Action": "CallService", "Version": "2021-12-14"}, {}, {}
    ),
    "McpGetAllLastDevicePropertyValue": ApiInfo(
        "POST",
        "/",
        {"Action": "GetAllLastDevicePropertyValue", "Version": "2021-12-14"},
        {},
        {},
    ),
    "McpGetCustomTopicList": ApiInfo(
        "POST", "/", {"Action": "GetCustomTopicList", "Version": "2021-12-14"}, {}, {}
    ),
    "McpGetDeviceDetail": ApiInfo(
        "POST", "/", {"Action": "GetDeviceDetail", "Version": "2021-12-14"}, {}, {}
    ),
    "McpGetDeviceEventRecordList": ApiInfo(
        "POST",
        "/",
        {"Action": "GetDeviceEventRecordList", "Version": "2021-12-14"},
        {},
        {},
    ),
    "McpGetDeviceList": ApiInfo(
        "POST", "/", {"Action": "GetDeviceList", "Version": "2021-12-14"}, {}, {}
    ),
    "McpGetDeviceOverview": ApiInfo(
        "POST", "/", {"Action": "GetDeviceOverview", "Version": "2021-12-14"}, {}, {}
    ),
    "McpGetDeviceStatus": ApiInfo(
        "POST", "/", {"Action": "GetDeviceStatus", "Version": "2021-12-14"}, {}, {}
    ),
    "McpGetDeviceServiceCallRecordList": ApiInfo(
        "POST",
        "/",
        {"Action": "GetDeviceServiceCallRecordList", "Version": "2021-12-14"},
        {},
        {},
    ),
    "McpGetInstanceDetail": ApiInfo(
        "POST", "/", {"Action": "GetInstanceDetail", "Version": "2021-12-14"}, {}, {}
    ),
    "McpGetInstanceEndpoints": ApiInfo(
        "POST", "/", {"Action": "GetInstanceEndpoints", "Version": "2021-12-14"}, {}, {}
    ),
    "McpGetInstanceList": ApiInfo(
        "POST", "/", {"Action": "GetInstanceList", "Version": "2021-12-14"}, {}, {}
    ),
    "McpGetLastDevicePropertyValue": ApiInfo(
        "POST",
        "/",
        {"Action": "GetLastDevicePropertyValue", "Version": "2021-12-14"},
        {},
        {},
    ),
    "McpGetProductList": ApiInfo(
        "POST", "/", {"Action": "GetProductList", "Version": "2021-12-14"}, {}, {}
    ),
    "McpGetProductDetail": ApiInfo(
        "POST", "/", {"Action": "GetProductDetail", "Version": "2021-12-14"}, {}, {}
    ),
    "McpGetPropertyValuesByTime": ApiInfo(
        "POST",
        "/",
        {"Action": "GetPropertyValuesByTime", "Version": "2021-12-14"},
        {},
        {},
    ),
    "McpGetThingModel": ApiInfo(
        "POST", "/", {"Action": "GetThingModel", "Version": "2021-12-14"}, {}, {}
    ),
    "McpSetProperty": ApiInfo(
        "POST", "/", {"Action": "SetProperty", "Version": "2021-12-14"}, {}, {}
    ),
}
service_info_map = {
    "cn-shanghai": ServiceInfo(
        "iot.cn-shanghai.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "iot", "cn-shanghai"),
        60,
        60,
        "https",
    ),
}
