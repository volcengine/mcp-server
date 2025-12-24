from typing import Any
from src.vod.mcp_tools.edit import _format_source
import json

def_font_pos_config = {
    "height": "20%",          
    "pos_x": "5%",         
    "pos_y": "68%",           
    "width": "90%"
}

def create_mcp_server(mcp, public_methods: dict,service):
    _build_media_input = public_methods["_build_media_input"]
    _start_execution = public_methods["_start_execution"]
    
    @mcp.tool()
    def asr_speech_to_text_task(type: str, video: str, spaceName: str, language: str = None) -> Any:
        """ASR speech-to-text captioning is supported, with two input modes available: `Vid` and  `DirectUrl`.
            Note：
            - `language`:  ** 可选字段 **， 不传会探测, 仅是在 语言较相似的情况下传递 来提高识别效果 
            - `Vid`: vid 模式下不需要进行任何处理
            - `DirectUrl`: directurl 模式下需要传递 FileName，不需要进行任何处理             
            Args：
            - type(str)：** 必选字段 **，文件类型，默认值为 `Vid` 。字段取值如下
                - Vid
                - DirectUrl
            - spaceName(str)： ** 必选字段 **,  视频空间名称
            - video： ** 必选字段 **,  视频文件信息, 当 type 为 `Vid` 时， video 为视频文件 ID；当 type 为 `DirectUrl` 时， video 为 FileName
            - language(str): ** 可选字段 **,  识别提示语言，取值如下：
                - cmn-Hans-CN: 简体中文
                - cmn-Hant-CN: 繁体中文
                - eng-US: 英语
                - jpn-JP: 日语
                - kor-KR: 韩语
                - rus-RU: 俄语
                - fra-FR: 法语
                - por-PT: 葡萄牙语
                - spa-ES: 西班牙语
                - vie-VN: 越南语
                - mya-MM: 缅甸语
                - nld-NL: 荷兰语
                - deu-DE: 德语
                - ind-ID: 印尼语
                - ita-IT: 意大利语
                - pol-PL: 波兰语
                - tha-TH: 泰语
                - tur-TR: 土耳其语
                - ara-SA: 阿拉伯语
                - msa-MY: 马来语
                - ron-RO: 罗马尼亚语
                - fil-PH: 菲律宾语
                - hin-IN: 印地语
            Returns
            - RunId(str):  媒体处理任务执行 ID, 可通过 `get_media_execution_task_result` 方法进行结果查询,type 为 `asr`
         """
        media_input = _build_media_input(type, video, spaceName)
        ask = {
            "WithSpeakerInfo": True,
        }
        if language:
            ask["Language"] = language
        params = {
            "Input": media_input,
            "Operation": {"Type": "Task", "Task": {"Type": "Asr", "Asr": ask }},
        }
        return _start_execution(params)

    # OCR 
    @mcp.tool()
    def ocr_text_to_subtitles_task(type: str, video: str, spaceName: str) -> Any:
        """OCR text to subtitles is supported, with two input modes available: `Vid` and  `DirectUrl`.
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
            - RunId(str):  媒体处理任务执行 ID, 可通过 `get_media_execution_task_result` 方法进行结果查询，type 为 `ocr` 
        """
        media_input = _build_media_input(type, video, spaceName)
        params = {
            "Input": media_input,
            "Operation": {"Type": "Task", "Task": {"Type": "Ocr", "Ocr": {}}},
        }
        return _start_execution(params)

    # subtitle removal
    @mcp.tool()
    def video_subtitles_removal_task(type: str, video: str, spaceName: str) -> Any:
        """Video subtitles removal is supported, with two input modes available: `Vid` and  `DirectUrl`.
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

    @mcp.tool()
    def add_subtitle(video: dict, space_name: str, subtitle_url: str = None, text_list: list = None, subtitle_config: dict = None) -> dict:
        """Add subtitle functionality, supporting both subtitle file (subtitle_url) and subtitle list (text_list) methods. However, subtitle_url and text_list must specify that subtitle_url has a higher priority.
        Note:
            - subtitle_url 和 text_list 必须指定一个，subtitle_url 优先级更高
        Args:
            - video(dict): ** 必选字段 **，视频信息
                - type(str): ** 必选字段 **，文件类型，默认值为 `vid` 。字段取值如下
                    - directurl
                    - http
                    - vid
                - source(str): ** 必选字段 **, 视频文件信息
            - subtitle_url(str): ** 非必选字段 **, 字幕文件 URL、filename，常见的字幕文件为 SRT、VTT、ASS 等格式。` subtitle_url和text_list必须指定一个subtitle_url优先级更高 `
            - text_list(list[dict]): ** 非必选字段 **, 字幕列表
                - text(str): 输入文本
                - start_time(float): 文本开始时间，单位s
                - end_time(float): 文本结束时间，单位s
            - subtitle_config(dict): ** 非必选字段 **，字幕配置信息，包含如下字段：
                - font_size(int): 字幕的字体大小，Integer 类型，单位：像素。默认200
                - font_type(str): 字幕的字体 ID，String 类型，详情请参考字体 ID。默认 SY_BLACK（思源黑体）
                - font_color(str): 字幕的字体颜色，String 类型，RGBA 格式，默认白色 #FFFFFFFF。
                - background_border_width(number): 字幕背景的边框宽度，Number 类型，单位：像素。
                - background_color(str): 字幕的背景颜色，String 类型，RGBA 格式，默认 #00000000。
                - border_color(str): 字幕内容描边的颜色，String 类型，RGBA 格式，默认 #00000000。
                - border_width(int): 字幕内容描边的的宽度，Integer 类型，单位：像素。默认0。
                - font_pos_config(dict): 字幕位置配置
                    - width(str): 字幕的宽度，支持设置为百分比（相对于视频宽度）或具体像素值，String 类型，例如 100% 或 1000。
                    - height(str): 字幕的高度，支持设置为百分比（相对于视频高度）或具体像素值，String 类型，例如 10% 或 100。
                    - pos_x(str): 字幕在水平方向（X 轴）的位置，以视频正上方居中位置为原点，单位：像素，String 类型。例如值为 0 时，表示字幕在水平位置居中；值为 - 100 时，表示字幕向左移动 100 像素；值为 100 时，表示字幕向右移动 100 像素。
                    - pos_y(str): 水印在垂直方向（Y 轴）的位置，以视频正上方居中位置为原点，单位：像素，String 类型。例如值为 0 时，表示字幕在视频顶部；值为 100 时，表示字幕向下移动 100 像素。
            - space_name(str): ** 必选字段 ** , 任务产物的上传空间。AI 处理生成的视频将被上传至此点播空间。
        Returns:
            - VCreativeId(str): AI 智剪任务 ID，用于查询任务状态。可以通过调用 `get_v_creative_task_result` 接口查询任务状态。
            - Code(int): 任务状态码。为 0 表示任务执行成功。
            - StatusMessage(str): 接口请求的状态信息。当 StatusCode 为 0 时，此时该字段返回 success，表示成功；其他状态码时，该字段会返回具体的错误信息。
            - StatusCode(int): 接口请求的状态码。0 表示成功，其他值表示不同的错误状态。
        """
        try:
            params = {"video": video, "space_name": space_name, "subtitle_url": subtitle_url, "text_list": text_list, "subtitle_config": subtitle_config}
            if "space_name" not in params:
                raise ValueError("add_subtitle: params must contain space_name")
            if not isinstance(params["space_name"], str):
                raise TypeError("add_subtitle: params['space_name'] must be a string")
            if not params["space_name"].strip():
                raise ValueError("add_subtitle: params['space_name'] cannot be empty")
            if "video" not in params:
                raise ValueError("add_subtitle: params must contain video")
            if not isinstance(params["video"], dict):
                raise TypeError("add_subtitle: params['video'] must be a dict")
            if not params.get("subtitle_url") and not params.get("text_list"):
                raise ValueError("add_subtitle: params must contain either subtitle_url or text_list")
            
            # 格式化视频
            videoType = params["video"].get("type", "vid")
            videoSource = params["video"].get("source", "")
            formattedVideoSource = _format_source(videoType, videoSource) if videoType in ["vid", "directurl"] else videoSource
            
            ParamObj = {
                "space_name": params["space_name"],
                "video": formattedVideoSource,
            }
            
            if params.get("subtitle_url"):
                ParamObj["subtitle_url"] = params["subtitle_url"]
            elif params.get("text_list"):
                ParamObj["text_list"] = params["text_list"]
            
            if params.get("subtitle_config"):
                # 获取用户提供的 font_pos_config，如果不存在则使用空字典
                user_font_pos_config = params["subtitle_config"].get("font_pos_config", {})
                # 合并默认配置和用户配置，用户配置优先级更高
                merged_font_pos_config = {**def_font_pos_config, **user_font_pos_config}
                ParamObj["subtitle_config"] = {
                    **params["subtitle_config"],
                    "font_pos_config": merged_font_pos_config
                }
            else:
                ParamObj["subtitle_config"] = {
                    "font_pos_config": def_font_pos_config
                }

            audioVideoStitchingParams = {
                "ParamObj": ParamObj,
                "Uploader": params["space_name"],
                "WorkflowId": "loki://168214785",
            }
            
            reqs = None
            try:
                reqs = service.mcp_post("McpAsyncVCreativeTask", {}, json.dumps(audioVideoStitchingParams))
                if isinstance(reqs, str):
                    reqs = json.loads(reqs)
                    reqsTmp = reqs.get('Result', {})
                    BaseResp = reqsTmp.get("BaseResp", {})
                    return json.dumps({
                        "VCreativeId": reqsTmp.get("VCreativeId", ""),
                        "Code": reqsTmp.get("Code"),
                        "StatusMessage": BaseResp.get("StatusMessage", ""),
                        "StatusCode": BaseResp.get("StatusCode", 0),
                    })
                else:
                    return reqs
            except Exception as e:
                raise Exception("add_subtitle: %s" % e, params)
        except Exception as e:
            raise Exception("add_subtitle: %s" % e, params)
    
    


       
