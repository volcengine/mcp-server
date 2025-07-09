from volcengine.ServiceInfo import ServiceInfo
from volcengine.Credentials import Credentials
from volcengine.ApiInfo import ApiInfo

api_info = {
    "McpDescribeAclAttributes": ApiInfo(
        "GET", "/", {"Action": "DescribeAclAttributes", "Version": "2020-04-01"}, {}, {}
    ),
    "McpDescribeCACertificates": ApiInfo(
        "GET",
        "/",
        {"Action": "DescribeCACertificates", "Version": "2020-04-01"},
        {},
        {},
    ),
    "McpDescribeAcls": ApiInfo(
        "GET", "/", {"Action": "DescribeAcls", "Version": "2020-04-01"}, {}, {}
    ),
    "McpDescribeCertificates": ApiInfo(
        "GET", "/", {"Action": "DescribeCertificates", "Version": "2020-04-01"}, {}, {}
    ),
    "McpDescribeCustomizedCfgs": ApiInfo(
        "GET",
        "/",
        {"Action": "DescribeCustomizedCfgs", "Version": "2020-04-01"},
        {},
        {},
    ),
    "McpDescribeAllCertificates": ApiInfo(
        "GET",
        "/",
        {"Action": "DescribeAllCertificates", "Version": "2020-04-01"},
        {},
        {},
    ),
    "McpDescribeListenerAttributes": ApiInfo(
        "GET",
        "/",
        {"Action": "DescribeListenerAttributes", "Version": "2020-04-01"},
        {},
        {},
    ),
    "McpDescribeListeners": ApiInfo(
        "GET", "/", {"Action": "DescribeListeners", "Version": "2020-04-01"}, {}, {}
    ),
    "McpDescribeLoadBalancerAttributes": ApiInfo(
        "GET",
        "/",
        {"Action": "DescribeLoadBalancerAttributes", "Version": "2020-04-01"},
        {},
        {},
    ),
    "McpDescribeCustomizedCfgAttributes": ApiInfo(
        "GET",
        "/",
        {"Action": "DescribeCustomizedCfgAttributes", "Version": "2020-04-01"},
        {},
        {},
    ),
    "McpDescribeHealthCheckTemplates": ApiInfo(
        "GET",
        "/",
        {"Action": "DescribeHealthCheckTemplates", "Version": "2020-04-01"},
        {},
        {},
    ),
    "McpDescribeListenerHealth": ApiInfo(
        "GET",
        "/",
        {"Action": "DescribeListenerHealth", "Version": "2020-04-01"},
        {},
        {},
    ),
    "McpDescribeLoadBalancers": ApiInfo(
        "GET", "/", {"Action": "DescribeLoadBalancers", "Version": "2020-04-01"}, {}, {}
    ),
    "McpDescribeServerGroupAttributes": ApiInfo(
        "GET",
        "/",
        {"Action": "DescribeServerGroupAttributes", "Version": "2020-04-01"},
        {},
        {},
    ),
    "McpDescribeRules": ApiInfo(
        "GET", "/", {"Action": "DescribeRules", "Version": "2020-04-01"}, {}, {}
    ),
    "McpDescribeZones": ApiInfo(
        "GET", "/", {"Action": "DescribeZones", "Version": "2020-04-01"}, {}, {}
    ),
    "McpDescribeServerGroups": ApiInfo(
        "GET", "/", {"Action": "DescribeServerGroups", "Version": "2020-04-01"}, {}, {}
    ),
    "McpDescribeServerGroupBackendServers": ApiInfo(
        "GET",
        "/",
        {"Action": "DescribeServerGroupBackendServers", "Version": "2020-04-01"},
        {},
        {},
    ),
}
service_info_map = {
    "cn-beijing": ServiceInfo(
        "alb.cn-beijing.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "alb", "cn-beijing"),
        60,
        60,
        "https",
    ),
    "cn-shanghai": ServiceInfo(
        "alb.cn-shanghai.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "alb", "cn-shanghai"),
        60,
        60,
        "https",
    ),
    "cn-guangzhou": ServiceInfo(
        "alb.cn-guangzhou.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "alb", "cn-guangzhou"),
        60,
        60,
        "https",
    ),
    "cn-hongkong": ServiceInfo(
        "alb.cn-hongkong.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "alb", "cn-hongkong"),
        60,
        60,
        "https",
    ),
    "ap-southeast-1": ServiceInfo(
        "alb.ap-southeast-1.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "alb", "ap-southeast-1"),
        60,
        60,
        "https",
    ),
    "ap-southeast-3": ServiceInfo(
        "alb.ap-southeast-3.volcengineapi.com",
        {"Accept": "application/json", "x-tt-mcp": "volc"},
        Credentials("", "", "alb", "ap-southeast-3"),
        60,
        60,
        "https",
    ),
}
