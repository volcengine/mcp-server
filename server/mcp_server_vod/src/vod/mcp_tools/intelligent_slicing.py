from typing import Any

from src.vod.api.api import VodAPI


def create_mcp_server(mcp,  public_methods: dict):
    _build_media_input = public_methods["_build_media_input"]
    _start_execution = public_methods["_start_execution"]

    # intelligent slicing
    @mcp.tool()
    def intelligent_slicing_task(type: str, video: str, spaceName: str) -> Any:
        """ Intelligent slicing is supported, with two input modes available: `Vid` and  `DirectUrl`.
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
            - RunId(str):  媒体处理任务执行 ID, 可通过 `get_media_execution_task_result` 方法进行结果查询，type 为 `intelligentSlicing`
        """
        media_input = _build_media_input(type, video, spaceName)
        params = {
            "Input": media_input,
            "Operation": {
                "Type": "Task",
                "Task": {"Type": "Segment", "Segment": {"MinDuration": 2.0, "Threshold": 15.0}},
            },
        }
        return _start_execution(params)

    # green screen
    @mcp.tool()
    def green_screen_task(type: str, video: str, spaceName: str, outputFormat: str = "WEBM") -> Any:
        """Green Screen （绿幕抠图） is supported, with two input modes available: `Vid` and  `DirectUrl`.
            Note：
                - `Vid`: vid 模式下不需要进行任何处理
                - `DirectUrl`: directurl 模式下需要传递 FileName，不需要进行任何处理          
            Args：
            - type(str)：** 必选字段 **，文件类型，默认值为 `Vid` 。字段取值如下
                - Vid
                - DirectUrl
            - spaceName(str)： ** 必选字段 **,  视频空间名称
            - video： ** 必选字段 **,  视频文件信息, 当 type 为 `Vid` 时， video 为视频文件 ID；当 type 为 `DirectUrl` 时， video 为 FileName
            - outputFormat：  ** 必选字段 **,   输出视频的封装格式，默认 `WEBM`，支持的取值如下：
                - MOV
                - WEBM
            Returns
            - RunId(str):  媒体处理任务执行 ID, 可通过 `get_media_execution_task_result` 方法进行结果查询，type 为 `greenScreen`
        """
        valid_formats = {"MOV", "WEBM"}
        fmt = outputFormat.upper()
        if fmt not in valid_formats:
            raise ValueError(f"outputFormat must be one of {sorted(valid_formats)}, but got {outputFormat}")

        media_input = _build_media_input(type, video, spaceName)
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
        type: str, video: str, spaceName: str, outputFormat: str = "WEBM"
    ) -> Any:
        """Portrait image retouching is supported, with two input modes available: `Vid` and  `DirectUrl`.
            Note：
                - `Vid`: vid 模式下不需要进行任何处理
                - `DirectUrl`: directurl 模式下需要传递 FileName，不需要进行任何处理          
            Args：
            - type(str)：** 必选字段 **，文件类型，默认值为 `Vid` 。字段取值如下
                - Vid
                - DirectUrl
            - spaceName(str)： ** 必选字段 **,  视频空间名称
            - video： ** 必选字段 **,  视频文件信息, 当 type 为 `Vid` 时， video 为视频文件 ID；当 type 为 `DirectUrl` 时， video 为 FileName
            - outputFormat：  ** 必选字段 **,   输出视频的封装格式，默认 `WEBM`，支持的取值如下：
                - MOV
                - WEBM
            Returns
            - RunId(str):  媒体处理任务执行 ID, 可通过 `get_media_execution_task_result` 方法进行结果查询，type 为 `portraitImageRetouching`
        """
        valid_formats = {"MOV", "WEBM"}
        fmt = outputFormat.upper()
        if fmt not in valid_formats:
            raise ValueError(f"outputFormat must be one of {sorted(valid_formats)}, but got {outputFormat}")

        media_input = _build_media_input(type, video, spaceName)
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

    @mcp.tool()
    def get_media_execution_task_result(type: str, runId: str) -> Any:
        """Obtain the query results of the media processing task, 场景区分， 仅仅支持单任务模式
            Args：
            - runId（str）:  ** 必选字段 **， 执行 ID。用于唯一指示当前这次媒体处理任务。
            - type（str）： ** 必选字段 **， 场景类型 ，取值如下：
                - portraitImageRetouching：人像抠图 
                - greenScreen： 绿幕抠图 
                - intelligentSlicing： 智能切片 
                - voiceSeparation： 人声分离
                - subtitlesRemoval： 视频字幕擦除
                - ocr： OCR文本转写字幕  （json）
                - asr： ASR语音转写字幕 （json）
                - audioNoiseReduction： 音频降噪
                - videoInterlacing： 视频插帧
                - videSuperResolution： 视频超分
                - enhanceVideo： 视频增强
            Returns： 
            - Code(str): 任务错误码。具体取值如下：
                - InvalidParameter.InvalidMediaStream：解析音视频流失败
                - InvalidParameter.MissingMediaStream：缺少音视频流
                - InvalidParameter.InvalidUriError：用户地址非法
                - InvalidParameter.MissingSubtitleStream：缺少字幕流
                - InvalidParameter.InvalidParam：参数错误
                - InvalidParameter.InvalidVidOrUri：输入源不存在
                - InternalError：内部错误
                - InternalError.DownloadError：系统下载错误
                - InternalError.UploadError：系统上传错误
                - InternalError.ExecutionTimeout：执行超时
            - VideoUrls(list[map[str, str]])： 视频播放信息列表
                - Vid(str): 视频 ID。
                - DirectUrl(str)：文件名
                - Url(str): 视频 播放链接。 
            - AudioUrls(list[map[str, str]]):    音频播放或者背景音信息列表
                - Vid(str):  音频频 ID。
                - DirectUrl(str)：文件名
                - Url(str): 视频 播放链接。
                - Type(str):   voice(人声) 、background(背景音)、normal(正常音频)
            - Texts(list[map[string, any]]): ocr、asr 识别结果
                - Start(Double): 开始时间，单位为秒
                - End(Double):   结束时间，单位为秒
                - Text(str):  识别的文本信息。
                - Speaker(str): 识别的说话人。 **仅当 asr 时候存在 **
        """
        # validate type
        valid_types = [
            "portraitImageRetouching",
            "greenScreen",
            "intelligentSlicing",
            "voiceSeparation",
            "subtitlesRemoval",
            "ocr",
            "asr",
            "audioNoiseReduction",
            "videoInterlacing",
            "videSuperResolution",
            "enhanceVideo",
            ]
        if type not in valid_types:
            raise ValueError(f"type must be one of {sorted(valid_types)}, but got {type}")  
        if not runId or not runId.strip():
            raise ValueError("runId must be provided")      

        # query result
        response = _get_media_execution_task_result(runId, type)
       
       
        return response


       
