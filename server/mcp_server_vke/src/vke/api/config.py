# coding=utf-8
from volcengine.ApiInfo import ApiInfo


api_info = {
    "VkeMcpCreateCluster": ApiInfo(
        "POST", "/", {"Action": "CreateCluster", "Version": "2022-05-12"}, {}, {}
    ),
    "VkeMcpListClusters": ApiInfo(
        "POST", "/", {"Action": "ListClusters", "Version": "2022-05-12"}, {}, {}
    ),
    "VkeMcpListSupportedResourceTypes": ApiInfo(
        "POST",
        "/",
        {"Action": "ListSupportedResourceTypes", "Version": "2022-05-12"},
        {},
        {},
    ),
    "VkeMcpCreateKubeconfig": ApiInfo(
        "POST", "/", {"Action": "CreateKubeconfig", "Version": "2022-05-12"}, {}, {}
    ),
    "VkeMcpListKubeconfigs": ApiInfo(
        "POST", "/", {"Action": "ListKubeconfigs", "Version": "2022-05-12"}, {}, {}
    ),
    "VkeMcpCreateNodePool": ApiInfo(
        "POST", "/", {"Action": "CreateNodePool", "Version": "2022-05-12"}, {}, {}
    ),
    "VkeMcpCreateDefaultNodePool": ApiInfo(
        "POST",
        "/",
        {"Action": "CreateDefaultNodePool", "Version": "2022-05-12"},
        {},
        {},
    ),
    "VkeMcpListNodePools": ApiInfo(
        "POST", "/", {"Action": "ListNodePools", "Version": "2022-05-12"}, {}, {}
    ),
    "VkeMcpCreateNodes": ApiInfo(
        "POST", "/", {"Action": "CreateNodes", "Version": "2022-05-12"}, {}, {}
    ),
    "VkeMcpListNodes": ApiInfo(
        "POST", "/", {"Action": "ListNodes", "Version": "2022-05-12"}, {}, {}
    ),
    "VkeMcpCreateVirtualNode": ApiInfo(
        "POST", "/", {"Action": "CreateVirtualNode", "Version": "2022-05-12"}, {}, {}
    ),
    "VkeMcpListVirtualNodes": ApiInfo(
        "POST", "/", {"Action": "ListVirtualNodes", "Version": "2022-05-12"}, {}, {}
    ),
    "VkeMcpListSupportedAddons": ApiInfo(
        "POST", "/", {"Action": "ListSupportedAddons", "Version": "2022-05-12"}, {}, {}
    ),
    "VkeMcpCreateAddon": ApiInfo(
        "POST", "/", {"Action": "CreateAddon", "Version": "2022-05-12"}, {}, {}
    ),
    "VkeMcpUpdateAddonConfig": ApiInfo(
        "POST", "/", {"Action": "UpdateAddonConfig", "Version": "2022-05-12"}, {}, {}
    ),
    "VkeMcpUpdateAddonVersion": ApiInfo(
        "POST", "/", {"Action": "UpdateAddonVersion", "Version": "2022-05-12"}, {}, {}
    ),
    "VkeMcpListAddons": ApiInfo(
        "POST", "/", {"Action": "ListAddons", "Version": "2022-05-12"}, {}, {}
    ),
}
