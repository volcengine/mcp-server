from volcengine.ServiceInfo import ServiceInfo
from volcengine.Credentials import Credentials
from volcengine.ApiInfo import ApiInfo

api_info = {
    "CrMcpCreateNamespace": ApiInfo(
        "POST", "/", {"Action": "CreateNamespace", "Version": "2022-05-12"}, {}, {}
    ),
    "CrMcpGetAuthorizationToken": ApiInfo(
        "POST",
        "/",
        {"Action": "GetAuthorizationToken", "Version": "2022-05-12"},
        {},
        {},
    ),
    "CrMcpListDomains": ApiInfo(
        "POST", "/", {"Action": "ListDomains", "Version": "2022-05-12"}, {}, {}
    ),
    "CrMcpListTags": ApiInfo(
        "POST", "/", {"Action": "ListTags", "Version": "2022-05-12"}, {}, {}
    ),
    "CrMcpCreateRepository": ApiInfo(
        "POST", "/", {"Action": "CreateRepository", "Version": "2022-05-12"}, {}, {}
    ),
    "CrMcpListRepositories": ApiInfo(
        "POST", "/", {"Action": "ListRepositories", "Version": "2022-05-12"}, {}, {}
    ),
    "CrMcpListNamespaces": ApiInfo(
        "POST", "/", {"Action": "ListNamespaces", "Version": "2022-05-12"}, {}, {}
    ),
    "CrMcpCreateRegistry": ApiInfo(
        "POST", "/", {"Action": "CreateRegistry", "Version": "2022-05-12"}, {}, {}
    ),
    "CrMcpListRegistries": ApiInfo(
        "POST", "/", {"Action": "ListRegistries", "Version": "2022-05-12"}, {}, {}
    ),
}
service_info_map = {
    "cn-beijing": ServiceInfo(
        "cr.cn-beijing.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "cr", "cn-beijing"),
        60,
        60,
        "https",
    ),
    "cn-guangzhou": ServiceInfo(
        "cr.cn-guangzhou.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "cr", "cn-guangzhou"),
        60,
        60,
        "https",
    ),
    "cn-shanghai": ServiceInfo(
        "cr.cn-shanghai.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "cr", "cn-shanghai"),
        60,
        60,
        "https",
    ),
    "ap-southeast-1": ServiceInfo(
        "cr.ap-southeast-1.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "cr", "ap-southeast-1"),
        60,
        60,
        "https",
    ),
    "cn-beijing2": ServiceInfo(
        "cr.cn-beijing2.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "cr", "cn-beijing2"),
        60,
        60,
        "https",
    ),
    "cn-datong": ServiceInfo(
        "cr.cn-datong.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "cr", "cn-datong"),
        60,
        60,
        "https",
    ),
    "cn-beijing-selfdrive": ServiceInfo(
        "cr.cn-beijing-selfdrive.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "cr", "cn-beijing-selfdrive"),
        60,
        60,
        "https",
    ),
    "cn-hongkong": ServiceInfo(
        "cr.cn-hongkong.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "cr", "cn-hongkong"),
        60,
        60,
        "https",
    ),
    "cn-beijing-autodriving": ServiceInfo(
        "cr.cn-beijing-autodriving.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "cr", "cn-beijing-autodriving"),
        60,
        60,
        "https",
    ),
    "ap-southeast-3": ServiceInfo(
        "cr.ap-southeast-3.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "cr", "ap-southeast-3"),
        60,
        60,
        "https",
    ),
    "cn-shanghai-autodriving": ServiceInfo(
        "cr.cn-shanghai-autodriving.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "cr", "cn-shanghai-autodriving"),
        60,
        60,
        "https",
    ),
    "cn-wulanchabu": ServiceInfo(
        "cr.cn-wulanchabu.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "cr", "cn-wulanchabu"),
        60,
        60,
        "https",
    ),
}
