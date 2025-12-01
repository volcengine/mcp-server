
from volcengine.ApiInfo import ApiInfo

## 接口定义
api_info = {
    "McpAsyncVCreativeTask": ApiInfo(
        "POST", "/", {"Action": "AsyncVCreativeTask", "Version": "2018-01-01"}, {}, {}
    ),
    "McpGetVCreativeTaskResult": ApiInfo(
        "GET",
        "/",
        {"Action": "GetVCreativeTaskResult", "Version": "2018-01-01"},
        {},
        {},
    ),
    "McpGetVideoPlayInfo": ApiInfo("GET", "/", {"Action": "GetVideoPlayInfo", "Version": "2018-01-01"}, {}, {}),
    "McpUpdateMediaPublishStatus": ApiInfo("POST", "/", {"Action": "UpdateMediaPublishStatus", "Version": "2020-08-01"}, {}, {}),
    "McpStartExecution": ApiInfo("POST", "/", {"Action": "StartExecution", "Version": "2025-01-01"}, {}, {}),
    "MCPGetExecution": ApiInfo("GET", "/", {"Action": "GetExecution", "Version": "2025-01-01"}, {}, {}),
    "MCPQueryUploadTaskInfo": ApiInfo("GET", "/", {"Action": "QueryUploadTaskInfo", "Version": "2020-08-01"}, {}, {}),
    "MCPListDomain": ApiInfo("GET", "/", {"Action": "ListDomain", "Version": "2023-01-01"}, {}, {}),
    "MCPDescribeDomainConfig": ApiInfo("GET", "/", {"Action": "DescribeDomainConfig", "Version": "2023-07-01"}, {}, {}),
    "MCPGetStorageConfig": ApiInfo("GET", "/", {"Action": "GetStorageConfig", "Version": "2023-07-01"}, {}, {}),
}
