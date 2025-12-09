from typing import Any

def create_transcode_result_server(mcp,  public_methods: dict,):
    """Register all VOD media MCP tools."""
    _get_media_execution_task_result = public_methods["_get_media_execution_task_result"]
    
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


       
