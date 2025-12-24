from typing import Any
def create_mcp_server(mcp, public_methods: dict):
    _build_media_input = public_methods["_build_media_input"]
    _start_execution = public_methods["_start_execution"]

    """Register all VOD media MCP tools."""
    # video quality enhancement
    @mcp.tool()
    def video_quality_enhancement_task(type: str, video: str, spaceName: str) -> Any:
        """ Video quality enhancement is supported, with two input modes available: `Vid` and  `DirectUrl`.。
        Note：
            - `Vid`: vid 模式下不需要进行任何处理
            - `DirectUrl`: directurl 模式下需要传递 FileName，不需要进行任何处理
        Args：
          - type(str)：** 必选字段 **，文件类型，默认值为 `Vid` 。字段取值如下
            - Vid
            - DirectUrl
          - spaceName(str)： ** 必选字段 **,  视频空间名称
          - video： ** 必选字段 **,  视频文件信息, 当 type 为 `Vid` 时， video 为视频文件 ID；当 type 为 `DirectUrl` 时， video 为 FileName
        Returns
          - RunId(str):  媒体处理任务执行 ID, 可通过  `get_media_execution_task_result` 方法进行结果查询， 输入 type 为 `enhanceVideo`
        """

        media_input = _build_media_input(type, video, spaceName)
        params = {
            "Input": media_input,
            "Operation": {
                "Type": "Task",
                "Task": {
                    "Type": "Enhance",
                    "Enhance": {
                        "Type": "Moe",
                        "MoeEnhance": {
                            "Config": "short_series",
                            "VideoStrategy": {
                                "RepairStyle": 1,
                                "RepairStrength": 0,
                            },
                        },
                    },
                },
            },
        }
        return _start_execution(params)

    # video super-resolution
    @mcp.tool()
    def video_super_resolution_task(
        type: str, video: str, spaceName: str, Res: str = None, ResLimit: int = None
    ) -> Any:
        """ Video Super-Resolution is supported, with two input modes available: `Vid` and  `DirectUrl`.
        Note：
         - `Res` 和 `ResLimit` ** 不能同时指定，否则会返回错误  **。
         - `Vid`: vid 模式下不需要进行任何处理
         - `DirectUrl`: directurl 模式下需要传递 FileName，不需要进行任何处理
        Args：
        - type(str)：** 必选字段 **，文件类型，默认值为 `Vid` 。字段取值如下
            - Vid
            - DirectUrl
        - video： ** 必选字段 **,  视频文件信息, 当 type 为 `Vid` 时， video 为视频文件 ID；当 type 为 `DirectUrl` 时， video 为 FileName
        - spaceName(str)： ** 必选字段 **,  视频空间名称
        - Res(str): ** 必选字段 ** 目标分辨率。支持的取值如下所示。
            - 240p
            - 360p
            - 480p
            - 540p
            - 720p
            - 1080p
            - 2k
            - 4k
        - ResLimit(int): ** 必选字段 ** 目标长宽限制，用于指定输出视频的长边或短边的最大像素值，取值范围为 [64, 2160]。
        Returns
        - RunId(str):  媒体处理任务执行 ID, 可通过 `get_media_execution_task_result` 方法进行结果查询,输入 type 为 `videSuperResolution`
        """
        valid_res = {"240p", "360p", "480p", "540p", "720p", "1080p", "2k", "4k"}
        if Res is not None and Res not in valid_res:
            raise ValueError(f"Res must be one of {sorted(valid_res)}, but got {Res}")
        if ResLimit is not None and (not isinstance(ResLimit, int) or ResLimit < 64 or ResLimit > 2160):
            raise ValueError("ResLimit must be an int in [64, 2160]")

        media_input = _build_media_input(type, video, spaceName)
        target = {}
       
        if ResLimit is not None:
              target = {
                "ResLimit": ResLimit,
            }
        if Res is not None:
              target = {
                "Res": Res,
            }
       
        params = {
            "Input": media_input,
            "Operation": {
                "Type": "Task",
                "Task": {
                    "Type": "Enhance",
                    "Enhance": {
                        "Type": "Moe",
                        "MoeEnhance": {
                            "Config": "common",
                            "Target": target,
                            "VideoStrategy": {
                                "RepairStyle": 1,
                                "RepairStrength": 0,
                            },
                        },
                    },
                },
            },
        }
        return _start_execution(params)

    # video interlacing
    @mcp.tool()
    def video_interlacing_task(type: str, video: str, spaceName: str, Fps: float) -> Any:
        """ Video Super-Resolution is supported, with two input modes available: `Vid` and  `DirectUrl`.
        Args：
            - type(str)：** 必选字段 **，文件类型，默认值为 `Vid` 。字段取值如下
                - Vid
                - DirectUrl
            - video(str)： ** 必选字段 **,  视频文件信息, 当 type 为 `Vid` 时， video 为视频文件 ID；当 type 为 `DirectUrl` 时， video 为 FileName
            - spaceName(str)： ** 必选字段 **,  视频空间名称
            - Fps(Float):  目标帧率，单位为 fps。取值范围为 (0, 120]。
        Returns
             - RunId(str):  媒体处理任务执行 ID, 可通过 `get_media_execution_task_result` 方法进行结果查询,输入 type 为 `videSuperResolution`
        """
        if not isinstance(Fps, (int, float)) or Fps <= 0 or Fps > 120:
            raise ValueError("Fps must be > 0 and <= 120")

        media_input = _build_media_input(type, video, spaceName)
        params = {
            "Input": media_input,
            "Operation": {
                "Type": "Task",
                "Task": {
                    "Type": "Enhance",
                    "Enhance": {
                        "Type": "Moe",
                        "MoeEnhance": {
                            "Config": "common",
                            "Target": {"Fps": Fps},
                            "VideoStrategy": {
                                "RepairStyle": 1,
                                "RepairStrength": 0,
                            },
                        },
                    },
                },
            },
        }
        return _start_execution(params)

   