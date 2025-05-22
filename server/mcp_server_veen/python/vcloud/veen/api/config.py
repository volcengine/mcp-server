from volcengine.ServiceInfo import ServiceInfo
from volcengine.Credentials import Credentials
from volcengine.ApiInfo import ApiInfo

api_info = {
    "McpStartCloudServer": ApiInfo(
        "POST", "/", {"Action": "StartCloudServer", "Version": "2021-04-30"}, {}, {}
    ),
    "McpDeleteCloudServer": ApiInfo(
        "POST", "/", {"Action": "DeleteCloudServer", "Version": "2021-04-30"}, {}, {}
    ),
    "McpStopCloudServer": ApiInfo(
        "POST", "/", {"Action": "StopCloudServer", "Version": "2021-04-30"}, {}, {}
    ),
    "McpRebootCloudServer": ApiInfo(
        "POST", "/", {"Action": "RebootCloudServer", "Version": "2021-04-30"}, {}, {}
    ),
    "McpCreateCloudServer": ApiInfo(
        "POST", "/", {"Action": "CreateCloudServer", "Version": "2021-04-30"}, {}, {}
    ),
    "McpUpdateCloudServer": ApiInfo(
        "POST", "/", {"Action": "UpdateCloudServer", "Version": "2021-04-30"}, {}, {}
    ),
    "McpGetCloudServer": ApiInfo(
        "GET", "/", {"Action": "GetCloudServer", "Version": "2021-04-30"}, {}, {}
    ),
    "McpRebootInstances": ApiInfo(
        "POST", "/", {"Action": "RebootInstances", "Version": "2021-04-30"}, {}, {}
    ),
    "McpStartInstances": ApiInfo(
        "POST", "/", {"Action": "StartInstances", "Version": "2021-04-30"}, {}, {}
    ),
    "McpStopInstances": ApiInfo(
        "POST", "/", {"Action": "StopInstances", "Version": "2021-04-30"}, {}, {}
    ),
    "McpListInstances": ApiInfo(
        "GET", "/", {"Action": "ListInstances", "Version": "2021-04-30"}, {}, {}
    ),
    "McpGetInstance": ApiInfo(
        "GET", "/", {"Action": "GetInstance", "Version": "2021-04-30"}, {}, {}
    ),
    "McpResetLoginCredential": ApiInfo(
        "POST", "/", {"Action": "ResetLoginCredential", "Version": "2021-04-30"}, {}, {}
    ),
    "McpSetInstanceName": ApiInfo(
        "POST", "/", {"Action": "SetInstanceName", "Version": "2021-04-30"}, {}, {}
    ),
    "McpBatchResetSystem": ApiInfo(
        "POST", "/", {"Action": "BatchResetSystem", "Version": "2021-04-30"}, {}, {}
    ),
    "McpSetInstancesBandwidthPeak": ApiInfo(
        "POST",
        "/",
        {"Action": "SetInstancesBandwidthPeak", "Version": "2021-04-30"},
        {},
        {},
    ),
    "McpEnableInstancesIPv6": ApiInfo(
        "POST", "/", {"Action": "EnableInstancesIPv6", "Version": "2021-04-30"}, {}, {}
    ),
    "McpGetInstancesIPv6UpgradeStatus": ApiInfo(
        "GET",
        "/",
        {"Action": "GetInstancesIPv6UpgradeStatus", "Version": "2021-04-30"},
        {},
        {},
    ),
    "McpUpdateInstancesSpec": ApiInfo(
        "POST", "/", {"Action": "UpdateInstancesSpec", "Version": "2021-04-30"}, {}, {}
    ),
    "McpListInstanceInternalIps": ApiInfo(
        "GET",
        "/",
        {"Action": "ListInstanceInternalIps", "Version": "2021-04-30"},
        {},
        {},
    ),
    "McpSetBoundEipShareBandwidthPeak": ApiInfo(
        "POST",
        "/",
        {"Action": "SetBoundEipShareBandwidthPeak", "Version": "2021-04-30"},
        {},
        {},
    ),
    "McpBatchBindEipToInternalIpsRandomly": ApiInfo(
        "POST",
        "/",
        {"Action": "BatchBindEipToInternalIpsRandomly", "Version": "2021-04-30"},
        {},
        {},
    ),
    "McpBatchDeleteInternalIps": ApiInfo(
        "POST",
        "/",
        {"Action": "BatchDeleteInternalIps", "Version": "2021-04-30"},
        {},
        {},
    ),
    "McpGetInstanceCloudDiskInfo": ApiInfo(
        "GET",
        "/",
        {"Action": "GetInstanceCloudDiskInfo", "Version": "2021-04-30"},
        {},
        {},
    ),
    "McpSetCloudServerDeleteProtection": ApiInfo(
        "POST",
        "/",
        {"Action": "SetCloudServerDeleteProtection", "Version": "2021-04-30"},
        {},
        {},
    ),
    "McpSetInstanceDeleteProtection": ApiInfo(
        "POST",
        "/",
        {"Action": "SetInstanceDeleteProtection", "Version": "2021-04-30"},
        {},
        {},
    ),
    "McpListCloudServers": ApiInfo(
        "GET", "/", {"Action": "ListCloudServers", "Version": "2021-04-30"}, {}, {}
    ),
    "McpListInstanceTypes": ApiInfo(
        "GET", "/", {"Action": "ListInstanceTypes", "Version": "2021-04-30"}, {}, {}
    ),
    "McpListAvailableResourceInfo": ApiInfo(
        "GET",
        "/",
        {"Action": "ListAvailableResourceInfo", "Version": "2021-04-30"},
        {},
        {},
    ),
    "McpCreateInstance": ApiInfo(
        "POST", "/", {"Action": "CreateInstance", "Version": "2021-04-30"}, {}, {}
    ),
    "McpCreateSecondaryInternalIPAndReboot": ApiInfo(
        "POST",
        "/",
        {"Action": "CreateSecondaryInternalIPAndReboot", "Version": "2021-04-30"},
        {},
        {},
    ),
    "McpBindEipToInternalIP": ApiInfo(
        "POST", "/", {"Action": "BindEipToInternalIP", "Version": "2021-04-30"}, {}, {}
    ),
    "McpListImages": ApiInfo(
        "GET", "/", {"Action": "ListImages", "Version": "2021-04-30"}, {}, {}
    ),
    "McpGetImage": ApiInfo(
        "GET", "/", {"Action": "GetImage", "Version": "2021-04-30"}, {}, {}
    ),
    "McpBuildImageByVM": ApiInfo(
        "POST", "/", {"Action": "BuildImageByVM", "Version": "2021-04-30"}, {}, {}
    ),
    "McpUploadURLImage": ApiInfo(
        "POST", "/", {"Action": "UploadURLImage", "Version": "2021-04-30"}, {}, {}
    ),
    "McpUpdateImage": ApiInfo(
        "POST", "/", {"Action": "UpdateImage", "Version": "2021-04-30"}, {}, {}
    ),
    "McpDeleteImage": ApiInfo(
        "POST", "/", {"Action": "DeleteImage", "Version": "2021-04-30"}, {}, {}
    ),
    "McpGetVEENInstanceUsage": ApiInfo(
        "GET", "/", {"Action": "GetVEENInstanceUsage", "Version": "2021-04-30"}, {}, {}
    ),
    "McpGetVEEWInstanceUsage": ApiInfo(
        "GET", "/", {"Action": "GetVEEWInstanceUsage", "Version": "2021-04-30"}, {}, {}
    ),
    "McpGetBandwidthUsage": ApiInfo(
        "GET", "/", {"Action": "GetBandwidthUsage", "Version": "2021-04-30"}, {}, {}
    ),
    "McpGetBillingUsageDetail": ApiInfo(
        "GET", "/", {"Action": "GetBillingUsageDetail", "Version": "2021-04-30"}, {}, {}
    ),
    "McpListVPCInstances": ApiInfo(
        "GET", "/", {"Action": "ListVPCInstances", "Version": "2021-04-30"}, {}, {}
    ),
    "McpSetVPCInstanceDesc": ApiInfo(
        "POST", "/", {"Action": "SetVPCInstanceDesc", "Version": "2021-04-30"}, {}, {}
    ),
    "McpListRouteTables": ApiInfo(
        "GET", "/", {"Action": "ListRouteTables", "Version": "2021-04-30"}, {}, {}
    ),
    "McpGetRouteTable": ApiInfo(
        "GET", "/", {"Action": "GetRouteTable", "Version": "2021-04-30"}, {}, {}
    ),
    "McpSetRouteTableNameAndDesc": ApiInfo(
        "POST",
        "/",
        {"Action": "SetRouteTableNameAndDesc", "Version": "2021-04-30"},
        {},
        {},
    ),
    "McpListRouteEntries": ApiInfo(
        "GET", "/", {"Action": "ListRouteEntries", "Version": "2021-04-30"}, {}, {}
    ),
    "McpCreateRouteEntries": ApiInfo(
        "POST", "/", {"Action": "CreateRouteEntries", "Version": "2021-04-30"}, {}, {}
    ),
    "McpDeleteRouteEntry": ApiInfo(
        "POST", "/", {"Action": "DeleteRouteEntry", "Version": "2021-04-30"}, {}, {}
    ),
    "McpEnableRouteEntry": ApiInfo(
        "POST", "/", {"Action": "EnableRouteEntry", "Version": "2021-04-30"}, {}, {}
    ),
    "McpDisableRouteEntry": ApiInfo(
        "POST", "/", {"Action": "DisableRouteEntry", "Version": "2021-04-30"}, {}, {}
    ),
    "McpSetRouteEntryDesc": ApiInfo(
        "POST", "/", {"Action": "SetRouteEntryDesc", "Version": "2021-04-30"}, {}, {}
    ),
}
service_info_map = {
    "cn-north-1": ServiceInfo(
        "veenedge.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "veenedge", "cn-north-1"),
        60,
        60,
        "http",
    ),
}
