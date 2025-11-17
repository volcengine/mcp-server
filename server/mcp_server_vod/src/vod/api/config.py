
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
    "McpGetPlayInfo": ApiInfo("GET", "/", {"Action": "GetPlayInfo", "Version": "2020-08-01"}, {}, {}),
}
