from volcengine.ServiceInfo import ServiceInfo
from volcengine.Credentials import Credentials
from volcengine.ApiInfo import ApiInfo

api_info = {
    "Es_cloudMcpDescribeZones": ApiInfo(
        "POST", "/", {"Action": "DescribeZones", "Version": "2023-01-01"}, {}, {}
    ),
    "Es_cloudMcpDescribeInstances": ApiInfo(
        "POST", "/", {"Action": "DescribeInstances", "Version": "2023-01-01"}, {}, {}
    ),
    "Es_cloudMcpCreateInstanceInOneStep": ApiInfo(
        "POST",
        "/",
        {"Action": "CreateInstanceInOneStep", "Version": "2023-01-01"},
        {},
        {},
    ),
    "Es_cloudMcpDescribeNodeAvailableSpecs": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeNodeAvailableSpecs", "Version": "2023-01-01"},
        {},
        {},
    ),
    "Es_cloudMcpDescribeInstancePlugins": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeInstancePlugins", "Version": "2023-01-01"},
        {},
        {},
    ),
    "Es_cloudMcpRenameInstance": ApiInfo(
        "POST", "/", {"Action": "RenameInstance", "Version": "2023-01-01"}, {}, {}
    ),
    "Es_cloudMcpModifyMaintenanceSetting": ApiInfo(
        "POST",
        "/",
        {"Action": "ModifyMaintenanceSetting", "Version": "2023-01-01"},
        {},
        {},
    ),
    "Es_cloudMcpModifyDeletionProtection": ApiInfo(
        "POST",
        "/",
        {"Action": "ModifyDeletionProtection", "Version": "2023-01-01"},
        {},
        {},
    ),
    "Es_cloudMcpDescribeInstance": ApiInfo(
        "POST", "/", {"Action": "DescribeInstance", "Version": "2023-01-01"}, {}, {}
    ),
    "Es_cloudMcpRestartNode": ApiInfo(
        "POST", "/", {"Action": "RestartNode", "Version": "2023-01-01"}, {}, {}
    ),
    "Es_cloudMcpDescribeInstanceNodes": ApiInfo(
        "POST",
        "/",
        {"Action": "DescribeInstanceNodes", "Version": "2023-01-01"},
        {},
        {},
    ),
    "Es_cloudMcpCreateInstance": ApiInfo(
        "POST", "/", {"Action": "CreateInstance", "Version": "2023-01-01"}, {}, {}
    ),
}
service_info_map = {
    "ap-southeast-1": ServiceInfo(
        "escloud.ap-southeast-1.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "ESCloud", "ap-southeast-1"),
        60,
        60,
        "https",
    ),
    "cn-hongkong": ServiceInfo(
        "escloud.cn-hongkong.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "ESCloud", "cn-hongkong"),
        60,
        60,
        "https",
    ),
    "ap-southeast-1": ServiceInfo(
        "escloud.ap-southeast-1.byteplusapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "ESCloud", "ap-southeast-1"),
        60,
        60,
        "https",
    ),
    "cn-hongkong": ServiceInfo(
        "escloud.cn-hongkong.byteplusapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "ESCloud", "cn-hongkong"),
        60,
        60,
        "https",
    ),
    "ap-southeast-3": ServiceInfo(
        "escloud.ap-southeast-3.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "ESCloud", "ap-southeast-3"),
        60,
        60,
        "https",
    ),
    "ap-southeast-3": ServiceInfo(
        "escloud.ap-southeast-3.byteplusapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "ESCloud", "ap-southeast-3"),
        60,
        60,
        "https",
    ),
    "cn-beijing": ServiceInfo(
        "escloud.cn-beijing.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "ESCloud", "cn-beijing"),
        60,
        60,
        "https",
    ),
    "cn-shanghai": ServiceInfo(
        "escloud.cn-shanghai.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "ESCloud", "cn-shanghai"),
        60,
        60,
        "https",
    ),
    "cn-guangzhou": ServiceInfo(
        "escloud.cn-guangzhou.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "ESCloud", "cn-guangzhou"),
        60,
        60,
        "https",
    ),
    "cn-beijing-selfdrive": ServiceInfo(
        "escloud.cn-beijing-selfdrive.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "ESCloud", "cn-beijing-selfdrive"),
        60,
        60,
        "https",
    ),
    "cn-shanghai-autodriving": ServiceInfo(
        "escloud.cn-shanghai-autodriving.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "ESCloud", "cn-shanghai-autodriving"),
        60,
        60,
        "https",
    ),
}
