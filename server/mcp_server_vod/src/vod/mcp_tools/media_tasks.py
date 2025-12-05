import json
from typing import Any, Dict
from urllib.parse import urlparse

from src.vod.api.api import VodAPI


enhance_type = ['enhanceVideo','videSuperResolution','videoInterlacing','audioNoiseReduction']

def create_media_mcp_server(mcp, service: VodAPI, public_methods: dict):
    """Register all VOD media MCP tools."""

    get_play_url = public_methods["get_play_url"]
    
    def _build_media_input(asset_type: str, asset_value: str, space_name: str) -> Dict[str, Any]:
        if asset_type not in {"Vid", "DirectUrl"}:
            raise ValueError(f"type must be Vid or DirectUrl, but got {asset_type}")
        if not asset_value:
            raise ValueError("media asset id is required")
        if not space_name:
            raise ValueError("spaceName is required")

        media_input: Dict[str, Any] = {"Type": asset_type}
        if asset_type == "Vid":
            media_input["Vid"] = asset_value
        else:
            media_input["DirectUrl"] = {"FileName": asset_value, "SpaceName": space_name}
        return media_input

    def _start_execution(payload: Dict[str, Any]) -> Any:
        response = service.mcp_post("McpStartExecution", {}, json.dumps(payload))
        if isinstance(response, str):
            response = json.loads(response)
            result = response.get("Result", {})
            return json.dumps({"RunId": result.get("RunId", "")})
        return response

    def handle_transcode_data(data: Dict[str, Any],spaceName: str) -> Dict[str, Any]:
            """Transcode data to MCP format."""
            FileId = data.get("FileId")
            StoreUri = data.get("StoreUri")
            FileName = ''
            # 从StoreUri中提取FileName
            if StoreUri and isinstance(StoreUri, str):
                parsed = urlparse(StoreUri)
                parts = parsed.path.split('/')[1:]  # 跳过第一个部分
                FileName = '/'.join(parts)
            return {
                "FileId": FileId,
                "DirectUrl": FileName,
                "Url": get_play_url(spaceName, FileName),
            }
    
    def _get_media_execution_task_result(run_id: str, task_type: str) -> Any:
        response = service.mcp_get("MCPGetExecution", {"RunId": run_id})
        ## 视频处理结果
        video_urls = []
        ## 音频处理结果
        audio_urls = []
        ## 文本处理结果
        texts = []
        if isinstance(response, str):
            temp = json.loads(response)
            temp_result = temp.get("Result", {})
            space_name = temp_result.get("Meta", {}).get("SpaceName", "")
            output = temp_result.get("Output", {}).get("Task", {})
            status = temp_result.get("Status", "")
            if status != "Success":
                return {
                        "Status": status,  
                        "Code": temp_result.get("Code", ""), 
                        "SpaceName": space_name,
                    }
            else:
                ## 智能抠图认为
                video_Matting = ['greenScreen', 'portraitImageRetouching']
                # 视频增强
                if task_type in enhance_type:
                    enhance_type_info = handle_transcode_data(output.get("Enhance", {}), space_name)
                    video_urls.append(enhance_type_info)
                # 人像抠图
                elif task_type in video_Matting:
                    video_matting_result = output.get("VideoMatting", {})
                    video_matting_result_video = video_matting_result.get("Video", {})
                    matting_file_name = video_matting_result_video.get("FileName", "")
                    video_urls.append({
                        "DirectUrl": matting_file_name,
                        "Vid": video_matting_result_video.get("Vid", ""),
                        "Url": get_play_url(space_name, matting_file_name),
                    })
                # 智能切片
                elif task_type == "intelligentSlicing":
                    tmp_segment = output.get("Segment", {})
                    tem_segments = tmp_segment.get("Segments", [])
                    for segment in tem_segments:
                        segment_file = segment.get("File", "")
                        segment_file_name = segment_file.get("FileName", "")
                        video_urls.append({
                            "DirectUrl": segment_file_name,
                            "Vid": segment_file.get("Vid", ""),
                            "Url": get_play_url(space_name, segment_file_name),
                        })
                
                # 人声分离
                elif task_type == "voiceSeparation":
                    audio_extract = output.get("AudioExtract", {})
                    voice_files = audio_extract.get("Voice", [])
                    background_files = audio_extract.get("Background", [])
                    voice_files_name = voice_files.get("FileName", "")
                    background_files_name = background_files.get("FileName", "")
                    audio_urls.append({
                            "DirectUrl": voice_files_name,
                            "Vid": voice_files.get("Vid", ""),
                            "Type": "voice",
                            "Url": get_play_url(space_name, voice_files_name),
                        })
                    
                    audio_urls.append({
                        "DirectUrl": background_files_name,
                        "Vid": background_files.get("Vid", ""),
                        "Type": "background",
                        "Url": get_play_url(space_name, background_files_name),
                    })
                # 视频字幕擦除
                elif task_type == "subtitlesRemoval":
                    subtitles_removal = output.get("Erase", {})
                    subtitles_removal_file = subtitles_removal.get("File", {})
                    subtitles_removal_file_name = subtitles_removal_file.get("FileName", "")
                    video_urls.append({
                        "DirectUrl": subtitles_removal_file_name,
                        "Vid": subtitles_removal_file.get("Vid", ""),
                        "Url": get_play_url(space_name, subtitles_removal_file_name),
                    })
                # OCR文本转写字幕
                elif task_type == "ocr":
                    ocr = output.get("Ocr", {})
                    ocr_texts = ocr.get("Texts", [])
                    texts = ocr_texts
                # ASR语音转写字幕
                elif task_type == "asr":
                    asr = output.get("Asr", {})
                    utterances = asr.get("Utterances", [])
                    for utterance in utterances:
                        attribute = utterance.get("Attribute", "")
                        speaker = attribute.get("Speaker", "")
                        texts.append({
                            "Speaker": speaker,
                            "Text": utterance.get("Text", ""),
                            "StartTime": utterance.get("Start"),
                            "EndTime": utterance.get("End"),
                        })
                
                return {
                    "Code": temp_result.get("Code", ""), 
                    "SpaceName": space_name,
                    "VideoUrls": video_urls,
                    "AudioUrls": audio_urls,
                    "Texts": texts,
                     "Status": status,  
                }
        return response

    # 视频质量增强
    @mcp.tool()
    def video_quality_enhancement_task(type: str, video: str, spaceName: str) -> Any:
        """ Video quality enhancement is supported, with two input modes available: `Vid` and  `DirectUrl`.。
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

    # 视频超分
    @mcp.tool()
    def video_super_resolution_task(
        type: str, video: str, spaceName: str, Res: str = None, ResLimit: int = None
    ) -> Any:
        """ Video Super-Resolution is supported, with two input modes available: `Vid` and  `DirectUrl`.
        Note：
         - `Res` 和 `ResLimit` ** 不能同时指定，否则会返回错误  **。
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

    # 视频插帧
    @mcp.tool()
    def video_interlacing_task(type: str, video: str, spaceName: str, Fps: float) -> Any:
        """ Video Super-Resolution is supported, with two input modes available: `Vid` and  `DirectUrl`.
        Args：
            - type(str)：** 必选字段 **，文件类型，默认值为 `Vid` 。字段取值如下
                - Vid
                - DirectUrl
            - video： ** 必选字段 **,  视频文件信息, 当 type 为 `Vid` 时， video 为视频文件 ID；当 type 为 `DirectUrl` 时， video 为 FileName
            - spaceName(str)： ** 必选字段 **,  视频空间名称
            - Res(str):  目标分辨率。支持的取值如下所示。
                - 240p
                - 360p
                - 480p
                - 540p
                - 720p
                - 1080p
                - 2k
                - 4k
            - ResLimit(int): 目标长宽限制，用于指定输出视频的长边或短边的最大像素值，取值范围为 [64, 2160]。
        Returns
             - RunId(str):  媒体处理任务执行 ID, 可通过 `get_media_execution_task_result` 方法进行结果查询,输入 type 为 `videSuperResolution`
        """
        if not isinstance(Fps, (int, float)) or Fps <= 0 or Fps > 128:
            raise ValueError("Fps must be > 0 and <= 128")

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

    # 音频降噪
    @mcp.tool()
    def audio_noise_reduction_task(type: str, audio: str, spaceName: str) -> Any:
        """ Audio noise reduction, supporting two input modes:  `Vid` and  `DirectUrl`.
            Args：
            - type(str)：** 必选字段 **，文件类型，默认值为 `Vid` 。字段取值如下
                - Vid
                - DirectUrl
            - spaceName(str)： ** 必选字段 **,  视频空间名称
            - audio： ** 必选字段 **,   音频文件信息, 当 type 为 `Vid` 时， video 为视频文件 ID；当 type 为 `DirectUrl` 时， video 为 FileName
            Returns
            - RunId(str):  媒体处理任务执行 ID, 可通过 `get_media_execution_task_result` 方法进行结果查询,type 为 `audioNoiseReduction`
        """
        media_input = _build_media_input(type, audio, spaceName)
        params = {
            "Input": media_input,
            "Operation": {
                "Type": "Task",
                "Task": {
                    "Type": "Enhance",
                    "Enhance": {"Type": "Custom", "Modules": [{"Type": "AudioDenoise"}]},
                },
            },
        }
        return _start_execution(params)

    # ASR 语音转字幕
    @mcp.tool()
    def asr_speech_to_text_task(type: str, video: str, spaceName: str) -> Any:
        """ASR speech-to-text captioning is supported, with two input modes available: `Vid` and  `DirectUrl`.
            Args：
            - type(str)：** 必选字段 **，文件类型，默认值为 `Vid` 。字段取值如下
                - Vid
                - DirectUrl
            - spaceName(str)： ** 必选字段 **,  视频空间名称
            - video： ** 必选字段 **,  视频文件信息, 当 type 为 `Vid` 时， video 为视频文件 ID；当 type 为 `DirectUrl` 时， video 为 FileName
            Returns
            - RunId(str):  媒体处理任务执行 ID, 可通过 `get_media_execution_task_result` 方法进行结果查询,type 为 `asr`
         """
        media_input = _build_media_input(type, video, spaceName)
        params = {
            "Input": media_input,
            "Operation": {"Type": "Task", "Task": {"Type": "Asr", "Asr": {}}},
        }
        return _start_execution(params)

    # OCR 文本转字幕
    @mcp.tool()
    def ocr_text_to_subtitles_task(type: str, video: str, spaceName: str) -> Any:
        """OCR text to subtitles is supported, with two input modes available: `Vid` and  `DirectUrl`.
            Args：
            - type(str)：** 必选字段 **，文件类型，默认值为 `Vid` 。字段取值如下
                - Vid
                - DirectUrl
            - spaceName(str)： ** 必选字段 **,  视频空间名称
            - video： ** 必选字段 **,  视频文件信息, 当 type 为 `Vid` 时， video 为视频文件 ID；当 type 为 `DirectUrl` 时， video 为 FileName
            Returns
            - RunId(str):  媒体处理任务执行 ID, 可通过 `get_media_execution_task_result` 方法进行结果查询，type 为 `ocr` 
        """
        media_input = _build_media_input(type, video, spaceName)
        params = {
            "Input": media_input,
            "Operation": {"Type": "Task", "Task": {"Type": "Ocr", "Ocr": {}}},
        }
        return _start_execution(params)

    # 视频字幕擦除
    @mcp.tool()
    def video_subtitles_removal_task(type: str, video: str, spaceName: str) -> Any:
        """Video subtitles removal is supported, with two input modes available: `Vid` and  `DirectUrl`.
            Args：
            - type(str)：** 必选字段 **，文件类型，默认值为 `Vid` 。字段取值如下
                - Vid
                - DirectUrl
            - spaceName(str)： ** 必选字段 **,  视频空间名称
            - video： ** 必选字段 **,  视频文件信息, 当 type 为 `Vid` 时， video 为视频文件 ID；当 type 为 `DirectUrl` 时， video 为 FileName
            Returns
            - RunId(str):  媒体处理任务执行 ID, 可通过 `get_media_execution_task_result` 方法进行结果查询,type 为 `subtitlesRemoval` 
        """
        media_input = _build_media_input(type, video, spaceName)
        params = {
            "Input": media_input,
            "Operation": {
                "Type": "Task",
                "Task": {
                    "Type": "Erase",
                    
                    "Erase": {
                        "Mode": "Auto",
                        "NewVid": True,
                        "Auto": {"Type": "Subtitle"},
                    },
                },
            },
        }
        return _start_execution(params)

    # 人声分离
    @mcp.tool()
    def voice_separation_task(type: str, video: str, spaceName: str) -> Any:
        """Voice separation is supported, with two input modes available: `Vid` and  `DirectUrl`.
            Args：
            - type(str)：** 必选字段 **，文件类型，默认值为 `Vid` 。字段取值如下
                - Vid
                - DirectUrl
            - spaceName(str)： ** 必选字段 **,  视频空间名称
            - video： ** 必选字段 **,  视频文件信息, 当 type 为 `Vid` 时， video 为视频文件 ID；当 type 为 `DirectUrl` 时， video 为 FileName
            Returns
            - RunId(str):  媒体处理任务执行 ID, 可通过 `get_media_execution_task_result` 方法进行结果查询，type 为 `voiceSeparation`
        """
        media_input = _build_media_input(type, video, spaceName)
        params = {
            "Input": media_input,
            "Operation": {
                "Type": "Task",
                "Task": {"Type": "AudioExtract", "AudioExtract": {"Voice": True}},
            },
        }
        return _start_execution(params)

    # 智能切片
    @mcp.tool()
    def intelligent_slicing_task(type: str, video: str, spaceName: str) -> Any:
        """ Intelligent slicing is supported, with two input modes available: `Vid` and  `DirectUrl`.
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

    # 绿幕抠图
    @mcp.tool()
    def green_screen_task(type: str, video: str, spaceName: str, outputFormat: str = "WEBM") -> Any:
        """Green Screen （绿幕抠图） is supported, with two input modes available: `Vid` and  `DirectUrl`.
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

    # 人像抠图
    @mcp.tool()
    def portrait_image_retouching_task(
        type: str, video: str, spaceName: str, outputFormat: str = "WEBM"
    ) -> Any:
        """Portrait image retouching is supported, with two input modes available: `Vid` and  `DirectUrl`.
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
        # 校验场景类型是否正确
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

        # 获取执行结果
        response = _get_media_execution_task_result(runId, type)
       
       
        return response


       
