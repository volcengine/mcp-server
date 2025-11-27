
from volcengine.ApiInfo import ApiInfo

## 接口定义
api_info = {
    "VodMcpAsyncVCreativeTask": ApiInfo(
        "POST", "/", {"Action": "AsyncVCreativeTask", "Version": "2018-01-01"}, {}, {}
    ),
    "VodMcpGetVCreativeTaskResult": ApiInfo(
        "GET",
        "/",
        {"Action": "GetVCreativeTaskResult", "Version": "2018-01-01"},
        {},
        {},
    ),
    "McpGetVideoPlayInfo": ApiInfo("GET", "/", {"Action": "GetVideoPlayInfo", "Version": "2018-01-01"}, {}, {}),
    "McpUpdateMediaPublishStatus": ApiInfo("POST", "/", {"Action": "UpdateMediaPublishStatus", "Version": "2020-08-01"}, {}, {}),

}
