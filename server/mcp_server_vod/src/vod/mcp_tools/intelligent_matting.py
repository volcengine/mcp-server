from typing import Any

def create_mcp_server(mcp,  public_methods: dict):
    _build_media_input = public_methods["_build_media_input"]
    _start_execution = public_methods["_start_execution"]
    # green screen
    @mcp.tool()
    def green_screen_task(type: str, video: str, space_name: str = None, output_format: str = "WEBM") -> Any:
        """
        Green Screen （绿幕抠图） is supported, with two input modes available: `Vid` and  `DirectUrl`.
            Note：
                - `Vid`: vid 模式下不需要进行任何处理
                - `DirectUrl`: directurl 模式下需要传递 FileName，不需要进行任何处理   
       
            Args：
            - type(str)：** 必选字段 **，文件类型，默认值为 `Vid` 。字段取值如下
                - Vid
                - DirectUrl
            - space_name(str)： ** 非必选字段 **,  视频空间名称
            - video： ** 必选字段 **,  视频文件信息, 当 type 为 `Vid` 时， video 为视频文件 ID；当 type 为 `DirectUrl` 时， video 为 FileName
            - output_format  ** 必选字段 **,   输出视频的封装格式，默认 `WEBM`，支持的取值如下：
                - MOV
                - WEBM
            Returns
            - RunId(str):  媒体处理任务执行 ID, 可通过 `get_media_execution_task_result` 方法进行结果查询，type 为 `greenScreen`
        """
        valid_formats = {"MOV", "WEBM"}
        fmt = output_format.upper()
        if fmt not in valid_formats:
            raise ValueError(f"output_format must be one of {sorted(valid_formats)}, but got {output_format}")


        media_input = _build_media_input(type, video, space_name)
        params = {
            "Input": media_input,
            "Operation": {
                "Type": "Task",
                "Task": {
                    "Type": "VideoMatting",
                    "VideoMatting": {
                        "Model": "GreenScreen",
                        "VideoOption": {"Format": fmt},
                        "NewVid": True,
                    },
                },
            },
        }
        return _start_execution(params)

    # portrait image retouching
    @mcp.tool()
    def portrait_image_retouching_task(
        type: str, video: str, space_name: str = None, output_format: str = "WEBM"
    ) -> Any:
        """
        Portrait image retouching is supported, with two input modes available: `Vid` and  `DirectUrl`.
            Note：
                - `Vid`: vid 模式下不需要进行任何处理
                - `DirectUrl`: directurl 模式下需要传递 FileName，不需要进行任何处理          
   
            Args：
            - type(str)：** 必选字段 **，文件类型，默认值为 `Vid` 。字段取值如下
                - Vid
                - DirectUrl
            - space_name(str)： ** 非必选字段 **,  视频空间名称
            - video： ** 必选字段 **,  视频文件信息, 当 type 为 `Vid` 时， video 为视频文件 ID；当 type 为 `DirectUrl` 时， video 为 FileName
            - output_format  ** 必选字段 **,   输出视频的封装格式，默认 `WEBM`，支持的取值如下：
                - MOV
                - WEBM
            Returns
            - RunId(str):  媒体处理任务执行 ID, 可通过 `get_media_execution_task_result` 方法进行结果查询，type 为 `portraitImageRetouching`
        """
        valid_formats = {"MOV", "WEBM"}
        fmt = output_format.upper()
        if fmt not in valid_formats:
            raise ValueError(f"output_format must be one of {sorted(valid_formats)}, but got {output_format}")

        media_input = _build_media_input(type, video, space_name)
        params = {
            "Input": media_input,
            "Operation": {
                "Type": "Task",
                "Task": {
                    "Type": "VideoMatting",
                    "VideoMatting": {
                        "Model": "Human",
                        "VideoOption": {"Format": fmt},
                        "NewVid": True,
                    },
                },
            },
        }
        return _start_execution(params)



       
