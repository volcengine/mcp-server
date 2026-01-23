from typing import Any

from src.vod.api.api import VodAPI


def create_mcp_server(mcp,  public_methods: dict):
    _build_media_input = public_methods["_build_media_input"]
    _start_execution = public_methods["_start_execution"]

    # intelligent slicing
    @mcp.tool(
        description="""
         Intelligent slicing is supported, with two input modes available: `Vid` and  `DirectUrl`.
            Note：
                - `Vid`: vid 模式下不需要进行任何处理
                - `DirectUrl`: directurl 模式下需要传递 FileName，不需要进行任何处理         
        """,
    )
    def intelligent_slicing_task(type: str, video: str, space_name: str = None) -> Any:
        """
            Args：
            - type(str)：** 必选字段 **，文件类型，默认值为 `Vid` 。字段取值如下
                - Vid
                - DirectUrl
            - space_name(str)： ** 非必选字段 **,  视频空间名称
            - video： ** 必选字段 **,  视频文件信息, 当 type 为 `Vid` 时， video 为视频文件 ID；当 type 为 `DirectUrl` 时， video 为 FileName
            Returns
            - RunId(str):  媒体处理任务执行 ID, 可通过 `get_media_execution_task_result` 方法进行结果查询，type 为 `intelligentSlicing`
        """
        media_input = _build_media_input(type, video, space_name)
        params = {
            "Input": media_input,
            "Operation": {
                "Type": "Task",
                "Task": {"Type": "Segment", "Segment": {"MinDuration": 2.0, "Threshold": 15.0}},
            },
        }
        return _start_execution(params)

