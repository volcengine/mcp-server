from volcengine.ServiceInfo import ServiceInfo
from volcengine.Credentials import Credentials
from volcengine.ApiInfo import ApiInfo

api_info = {
    "RtcMcpStartVoiceChat": ApiInfo(
        "POST", "/", {"Action": "StartVoiceChat", "Version": "2024-12-01"}, {}, {}
    ),
    "RtcMcpUpdateVoiceChat": ApiInfo(
        "POST", "/", {"Action": "UpdateVoiceChat", "Version": "2024-12-01"}, {}, {}
    ),
    "RtcMcpStopVoiceChat": ApiInfo(
        "POST", "/", {"Action": "StopVoiceChat", "Version": "2024-12-01"}, {}, {}
    ),
}
service_info_map = {
    "cn-north-1": ServiceInfo(
        "rtc.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "rtc", "cn-north-1"),
        60,
        60,
        "http",
    ),
    "ap-southeast-1": ServiceInfo(
        "open-ap-singapore-1.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "rtc", "ap-southeast-1"),
        60,
        60,
        "http",
    ),
}
