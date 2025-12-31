import json
from src.vod.api.api import VodAPI
from typing import List, Optional,Dict
from src.vod.models.request.request_models import InputSource,addSubVideoOptions


def _format_source(type: str, source: str) -> str:
    """根据 type 自动添加前缀到 source
    Args:
        type: 文件类型，vid、directurl、http
        source: 文件信息
    Returns:
        格式化后的 source
    """
    if not source:
        return source
    
    # 如果已经包含协议前缀，直接返回
    if source.startswith(('vid://', 'directurl://', 'http://', 'https://')):
        return source
    
    # 根据 type 添加前缀
    if type == 'vid':
        return f'vid://{source}'
    elif type == 'directurl':
        return f'directurl://{source}'
    # http 类型不需要添加前缀，直接返回
    return source

def create_mcp_server(mcp,public_methods: dict, service: VodAPI, ):

    @mcp.tool()
    def audio_video_stitching(type: str, SpaceName: str, videos: List[str] = None, audios: List[str] = None, transitions: List[str] = None) -> dict:
        """ Carry out video stitching, audio stitching, and support for transitions and other capabilities，需要参考 Note 中的要求。
         Note:
            -  **audio splicing does not support transitions. **
            -  ** vid 模式下需要增加  vid://  前缀， 示例：vid://123456 **
            -  ** directurl://{fileName} 格式指定资源的 FileName。示例：directurl://test.mp3**
            -  ** http(s):// 格式指定资源的 URL。示例：http://example.com/test.mp4**
         Args:
            - type(str): **  必选字段 ** , 拼接类型。 `audio` | `video`
            - SpaceName(str):  **  必选字段 ** , 任务产物的上传空间。AI 处理生成的视频将被上传至此点播空间。
            - videos(List[str]): **视频下必选字段，音频下不传递 **
                - 待拼接的视频列表：支持 ** vid:// ** 、 ** http:// ** 格式，** directUrl:// ** 格式
                    *** 视频要求： *** 
                        - 支持处理 MP4、AVI、MKV、MOV 等常见格式的视频。 
                        - 建议总视频时长在 5 分钟以内。 
            - audios(List[str]): **音频下必选字段，视频下不传递 **
                - 待拼接的音频列表：支持 ** vid:// ** 、 ** http:// ** 格式，** directUrl:// ** 格式
            - transitions(List[str]): 非必选字段，，音频下不传递
                - 转场效果 ID：例如 ["1182359"]。concat_videos 工具支持非交叠转场的效果，
                    - 可用于非交叠转场的动画
                    - 分类：交替出场，ID：1182359
                    - 分类：旋转放大，ID：1182360
                    - 分类：泛开，ID：1182358
                    - 分类：六角形，ID：1182365
                    - 分类：故障转换，ID：1182367
                    - 分类：飞眼，ID：1182368
                    - 分类：梦幻放大，ID：1182369
                    - 分类：开门展现，ID：1182370
                    - 分类：立方转换，ID：1182373
                    - 分类：透镜变换，ID：1182374
                    - 分类：晚霞转场，ID：1182375
                    - 分类：圆形交替，ID：1182378
                    - 注意： 
                    - 如果不提供，则没有转场，** 音频拼接 不支持转场 **
                    - 当视频数量超过转场数量 2 个及以上时，系统将自动循环使用转场。例如有 10 个视频，2 种转场效果，那么在 9 处拼接点上，这 2 种转场效果将被依次循环使用。
        Returns：
            - VCreativeId(str)：AI 智剪任务 ID，用于查询任务状态。可以通过调用 `get_v_creative_task_result` 接口查询任务状态。
            - Code(int):  任务状态码。为 0表示任务执行成功。
            - StatusMessage(str): 接口请求的状态信息。当 StatusCode 为 0 时，此时该字段返，success，表示成功；其他状态码时，该字段会返回具体的错误信息。
            - StatusCode(int):  接口请求的状态码。0表示成功，其他值表示不同的错误状态。
        
        """
        try:
            params = {"type": type, "SpaceName": SpaceName, "videos": videos, "audios": audios, "transitions": transitions}
            if "SpaceName" not in params:
                raise ValueError("audio_video_stitching: params must contain SpaceName")
            if not isinstance(params["SpaceName"], str):
                raise TypeError("audio_video_stitching: params['SpaceName'] must be a string")
            if not params["SpaceName"].strip():
                raise ValueError("audio_video_stitching: params['SpaceName'] cannot be empty")
            
            ParamObj = None
            WorkflowId = "loki://154775772"
            ParamType = params.get("type", "video")
            if ParamType == "audio":
                if "audios" not in params:
                    raise ValueError("audio_video_stitching: params must contain audios")
                if not isinstance(params["audios"], list):
                    raise TypeError("audio_video_stitching: params['audios'] must be a list")
                if not params["audios"]:
                    raise ValueError("audio_video_stitching: params['audios'] must contain at least one audio")
                # 格式化音频列表
                formattedAudios = []
                for audio in params.get("audios", []):
                    if isinstance(audio, str):
                        # 如果已经是完整格式，直接使用
                        if audio.startswith(('vid://', 'directurl://', 'http://', 'https://')):
                            formattedAudios.append(audio)
                        else:
                            # 默认使用 vid 格式
                            formattedAudios.append(_format_source("vid", audio))
                    else:
                        formattedAudios.append(audio)
                ParamObj = {
                    "space_name": params["SpaceName"],
                    "audios": formattedAudios,
                }
                WorkflowId = "loki://158487089"
            else:
                if "videos" not in params:
                    raise Exception("audio_video_stitching: params must contain videos", params)
                if not isinstance(params["videos"], list):
                    raise Exception("audio_video_stitching: params['videos'] must be a list", params)
                if not params["videos"]:
                    raise Exception("audio_video_stitching: params['videos'] must contain at least one video", params)
                # 格式化视频列表
                formattedVideos = []
                for video in params.get("videos", []):
                    if isinstance(video, str):
                        # 如果已经是完整格式，直接使用
                        if video.startswith(('vid://', 'directurl://', 'http://', 'https://')):
                            formattedVideos.append(video)
                        else:
                            # 默认使用 vid 格式
                            formattedVideos.append(_format_source("vid", video))
                    else:
                        formattedVideos.append(video)
                ParamObj = {
                    "space_name": params["SpaceName"],
                    "videos": formattedVideos,
                    "transitions": params.get("transitions", []),
                }
                WorkflowId = "loki://154775772"

            audioVideoStitchingParams ={
                "ParamObj": ParamObj,
                "Uploader": params["SpaceName"],
                "WorkflowId": WorkflowId,
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
                        "StatusMessage":BaseResp.get("StatusMessage", ""),
                        "StatusCode": BaseResp.get("StatusCode", 0),
                    })
                else:
                    return reqs
            except Exception as e:
                raise Exception("audio_video_stitching: %s" % e, params)
        except Exception as e:
            raise Exception("audio_video_stitching: %s" % e, params)

    @mcp.tool()
    def audio_video_clipping(type: str, SpaceName: str, source: str, start_time: float, end_time: float) -> dict:
        """ Invoke the current tools to complete the cropping of audio and video，需要参考 Note 中的要求。
         Note:
            -  ** vid 模式下需要增加  vid://  前缀， 示例：vid://123456 **
            -  ** directurl://{fileName} 格式指定资源的 FileName。示例：directurl://test.mp3**
            -  ** http(s):// 格式指定资源的 URL。示例：http://example.com/test.mp4**
            -  `start_time` 和 `end_time` 必须同时指定，且 `end_time` 必须大于 `start_time`
         Args:
            - type(str): **  必选字段 ** , 拼接类型。 `audio` | `video`
            - SpaceName(str):  **  必选字段 ** , 任务产物的上传空间。AI 处理生成的视频将被上传至此点播空间。
            - source(str): **  必选字段 **
                - 输入视频：支持 ** vid:// ** 、 ** http:// ** 格式，** directUrl:// ** 格式
            - end_time(float): **  必选字段 **
                - 裁剪结束时间，默认为片源结尾。支持设置为 2 位小数，单位：秒。 设置设置为 8，则表示在 8 秒位置结束裁剪。 
            - start_time(float): **  必选字段 **
                - 裁剪开始时间，默认为 0， 表示从头开始裁剪。支持设置为 2 位小数，单位：秒。 例如设置为 2，则表示从 2 秒的位置开始裁剪。 
        Returns：
            - VCreativeId(str)：AI 智剪任务 ID，用于查询任务状态。可以通过调用 `get_v_creative_task_result` 接口查询任务状态。
            - Code(int):  任务状态码。为 0表示任务执行成功。
            - StatusMessage(str): 接口请求的状态信息。当 StatusCode 为 0 时，此时该字段返，success，表示成功；其他状态码时，该字段会返回具体的错误信息。
            - StatusCode(int):  接口请求的状态码。0表示成功，其他值表示不同的错误状态。
        
        """
        try:
            params = {"type": type, "SpaceName": SpaceName, "source": source, "start_time": start_time, "end_time": end_time}
            if "SpaceName" not in params:
                raise Exception("audio_video_clipping: params must contain SpaceName", params)
            if not isinstance(params["SpaceName"], str):
                raise Exception("audio_video_clipping: params['SpaceName'] must be a string")
            if not params["SpaceName"].strip():
                raise Exception("audio_video_clipping: params['SpaceName'] cannot be empty")
            if "source" not in params:
                raise Exception("audio_video_clipping: params must contain source")
    
            startTime = params.get("start_time", 0)
            endTime = params.get("end_time", startTime + 1)
            sourceType = params.get("type", "video")
            sourceValue = params.get("source", "")
            # 根据 type 自动添加前缀
            formattedSource = _format_source(sourceType, sourceValue) if sourceType in ["vid", "directurl"] else sourceValue
            ParamObj = {
                "space_name": params["SpaceName"],
                "source": formattedSource,
                "end_time": endTime,
                "start_time": startTime,
            }

            audioVideoStitchingParams ={
                "ParamObj": ParamObj,
                "Uploader": params["SpaceName"],
                "WorkflowId": "loki://154419276",
            }
            
            ParamType = params.get("type", "video")
            if ParamType == "audio":
                audioVideoStitchingParams["WorkflowId"] = "loki://158666752"
            else:
                audioVideoStitchingParams["WorkflowId"] = "loki://154419276"
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
                        "StatusMessage":BaseResp.get("StatusMessage", ""),
                        "StatusCode": BaseResp.get("StatusCode", 0),
                    })
                else:
                    return reqs
            except Exception as e:
                raise Exception("audio_video_clipping: %s" % e)
        except Exception as e:
            raise Exception("audio_video_clipping: %s" % e)
    
    @mcp.tool()
    def get_v_creative_task_result(VCreativeId: str, SpaceName: str) -> dict:
        """ Query the execution status and results of video stitching, audio stitching, and audio-video cropping by using the  `VCreativeId`.
        Note:   
            -  **audio splicing does not support transitions. **
        Args:
            - VCreativeId(str): `String type`, ID for AI intelligent trimming task.
            - SpaceName(str): `String type`, space name.
        Returns：
            - Status(str): 任务的当前处理状态。
                - running: 执行中
                - success: 执行成功
                - failed_run: 执行失败
            - OutputJson(dict[str,Any]): 任务的输出结果
                - vid： 输出的点播空间vid
                - resolution： 分辨率
                - filename： 文件名
                - url:  产物链接，仅当任务成功时返回
                - duration： 时长， 单位：秒(s)
        """
        params={"VCreativeId": VCreativeId, "SpaceName": SpaceName}
        if "VCreativeId" not in params:
            raise ValueError("get_v_creative_task_result: params must contain VCreativeId")
        if not isinstance(params["VCreativeId"], str):
            raise TypeError("get_v_creative_task_result: params['VCreativeId'] must be a string")
        if not params["VCreativeId"].strip():
            raise ValueError("get_v_creative_task_result: params['VCreativeId'] cannot be empty")
        if "SpaceName" not in params:
            raise ValueError("get_v_creative_task_result: params must contain SpaceName")
        if not isinstance(params["SpaceName"], str):
            raise TypeError("get_v_creative_task_result: params['SpaceName'] must be a string")
        if not params["SpaceName"].strip():
            raise ValueError("get_v_creative_task_result: params['SpaceName'] cannot be empty")
        
        reqs = service.mcp_get("McpGetVCreativeTaskResult", {"VCreativeId": params["VCreativeId"]}, json.dumps({}))

        if isinstance(reqs, str):
            reqs = json.loads(reqs)
            reqsTmp = reqs.get('Result', {})
            # BaseResp = reqsTmp.get("BaseResp", {})
            url = None
            # 任务状态
            taskStatus = reqsTmp.get("Status", "")
            if taskStatus == "success":
                outputJson = reqsTmp.get("OutputJson", {})
                # 确保outputJson是字典类型
                tempOutputJson = {}
                if isinstance(outputJson, str):
                    try:
                        tempOutputJson = json.loads(outputJson)
                    except json.JSONDecodeError:
                        tempOutputJson = {}
                elif isinstance(outputJson, dict):
                    tempOutputJson = outputJson
                vid = tempOutputJson.get("vid")

                if vid is None:
                    raise Exception("get_v_creative_task_result: vid is None")
                else:
                    urlDta = public_methods["get_play_video_info"](vid, params["SpaceName"])
                 
                    if isinstance(urlDta, str):
                        urlTmp = json.loads(urlDta)
                        url = urlTmp.get("PlayURL", "")
                    else:
                        url = None
                return json.dumps({
                    "OutputJson": {
                        "vid": vid,
                        "resolution": tempOutputJson.get("resolution"),
                        "duration": tempOutputJson.get("duration"),
                        "filename": tempOutputJson.get("filename"),
                        "url": url,
                    },
                    "Status": taskStatus,
                })
            else:
                return json.dumps(reqsTmp)
        else:
            return reqs

    @mcp.tool()
    def flip_video(type: str, source: str, space_name: str, flip_x: bool = False, flip_y: bool = False) -> dict:
        """Video rotation capability is supported, allowing for `vertical and horizontal flipping of the video`. ** Default: No flipping **
        Args:
            - type(str): ** 必选字段 **，文件类型，默认值为 `vid` 。字段取值如下
                - directurl
                - http
                - vid
            - source(str): ** 必选字段 **, 视频文件信息
            - flip_x(bool): ** 非必选字段 **, 是否对视频进行上下翻转。Boolean 类型，默认值为 false，表示不翻转。
            - flip_y(bool): ** 非必选字段 **, 是否对视频进行左右翻转。Boolean 类型，默认值为 false，表示不翻转。
            - space_name(str): ** 必选字段 ** , 任务产物的上传空间。AI 处理生成的视频将被上传至此点播空间。
        Returns:
            - VCreativeId(str): AI 智剪任务 ID，用于查询任务状态。可以通过调用 `get_v_creative_task_result` 接口查询任务状态。
            - Code(int): 任务状态码。为 0 表示任务执行成功。
            - StatusMessage(str): 接口请求的状态信息。当 StatusCode 为 0 时，此时该字段返回 success，表示成功；其他状态码时，该字段会返回具体的错误信息。
            - StatusCode(int): 接口请求的状态码。0 表示成功，其他值表示不同的错误状态。
        """
        try:
            params = {"type": type, "source": source, "space_name": space_name, "flip_x": flip_x, "flip_y": flip_y}
            if "space_name" not in params:
                raise ValueError("flip_video: params must contain space_name")
            if not isinstance(params["space_name"], str):
                raise TypeError("flip_video: params['space_name'] must be a string")
            if not params["space_name"].strip():
                raise ValueError("flip_video: params['space_name'] cannot be empty")
            if "source" not in params:
                raise ValueError("flip_video: params must contain source")
            
            formattedSource = _format_source(params.get("type", "vid"), params.get("source", ""))
            ParamObj = {
                "space_name": params["space_name"],
                "source": formattedSource,
                "flip_x": params.get("flip_x", False),
                "flip_y": params.get("flip_y", False),
            }
            
            audioVideoStitchingParams = {
                "ParamObj": ParamObj,
                "Uploader": params["space_name"],
                "WorkflowId": "loki://165221855",
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
                raise Exception("flip_video: %s" % e, params)
        except Exception as e:
            raise Exception("flip_video: %s" % e, params)

    @mcp.tool()
    def speedup_video(type: str, source: str, space_name: str, speed: float = 1.0) -> dict:
        """Adjust the speed multiplier of the video, of type Float, with a range from 0.1 to 4.
        Args:
            - type(str): ** 必选字段 **，文件类型，默认值为 `vid` 。字段取值如下
                - directurl
                - http
                - vid
            - source(str): ** 必选字段 **, 视频文件信息
            - speed(float): ** 非必选字段 **, 调整速度的倍数，Float类型，取值范围为** 0.1～4 **。参考如下：
                - 0.1：放慢至原速的 0.1 倍。
                - 1（默认值）：原速。
                - 4：加速至原速的 4 倍。
            - space_name(str): ** 必选字段 ** , 任务产物的上传空间。AI 处理生成的视频将被上传至此点播空间。
        Returns:
            - VCreativeId(str): AI 智剪任务 ID，用于查询任务状态。可以通过调用 `get_v_creative_task_result` 接口查询任务状态。
            - Code(int): 任务状态码。为 0 表示任务执行成功。
            - StatusMessage(str): 接口请求的状态信息。当 StatusCode 为 0 时，此时该字段返回 success，表示成功；其他状态码时，该字段会返回具体的错误信息。
            - StatusCode(int): 接口请求的状态码。0 表示成功，其他值表示不同的错误状态。
        """
        try:
            params = {"type": type, "source": source, "space_name": space_name, "speed": speed}
            if "space_name" not in params:
                raise ValueError("speedup_video: params must contain space_name")
            if not isinstance(params["space_name"], str):
                raise TypeError("speedup_video: params['space_name'] must be a string")
            if not params["space_name"].strip():
                raise ValueError("speedup_video: params['space_name'] cannot be empty")
            if "source" not in params:
                raise ValueError("speedup_video: params must contain source")
            
            speedValue = params.get("speed", 1.0)
            if speedValue < 0.1 or speedValue > 4:
                raise ValueError("speedup_video: speed must be between 0.1 and 4")
            
            formattedSource = _format_source(params.get("type", "vid"), params.get("source", ""))
            ParamObj = {
                "space_name": params["space_name"],
                "source": formattedSource,
                "speed": speedValue,
            }
            
            audioVideoStitchingParams = {
                "ParamObj": ParamObj,
                "Uploader": params["space_name"],
                "WorkflowId": "loki://165223469",
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
                raise Exception("speedup_video: %s" % e, params)
        except Exception as e:
            raise Exception("speedup_video: %s" % e, params)

    @mcp.tool()
    def image_to_video(images: List[dict], space_name: str, transitions: List[str] = None) -> dict:
        """The image-to-video conversion function supports non-overlapping transition effects. When the number of videos exceeds the number of transitions by 2 or more, the system will automatically cycle through the transitions. ** Default: No transition **
        Args:
            - images(list[dict]): ** 必选字段 **，待合成的图片列表，子类型取值如下
                - type(str): ** 必选字段 **，文件类型，默认值为 `vid` 。字段取值如下
                    - directurl
                    - http
                    - vid
                - source(str): ** 必选字段 **, 图片文件信息
                - duration(float): ** 非必选字段 **, 图片播放时长，`默认值：3，单位：秒，支持 2 位小数`。
                - animation_type(str): ** 非必选字段 **, 图片的动画类型，选填，不填时无动画效果，取值如下：
                    - move_up：向上移动
                    - move_down：向下移动
                    - move_left：向左移动
                    - move_right：向右移动
                    - zoom_in：缩小
                    - zoom_out：放大
                - animation_in(float): ** 非必选字段 **, 动画结束时间，支持2位小数。默认为图片展示时长，表示动画随图片播放同时结束，单位：秒。
                - animation_out(float): ** 非必选字段 **, 动画结束时间，支持2位小数。默认为图片展示时长，表示动画随图片播放同时结束，单位：秒。
            - transitions(list[str]): 非必选字段，转场效果 ID：例如 ["1182359"]。concat_videos 工具支持非交叠转场的效果，
                - 可用于非交叠转场的动画
                - 分类：交替出场，ID：1182359
                - 分类：旋转放大，ID：1182360
                - 分类：泛开，ID：1182358
                - 分类：六角形，ID：1182365
                - 分类：故障转换，ID：1182367
                - 分类：飞眼，ID：1182368
                - 分类：梦幻放大，ID：1182369
                - 分类：开门展现，ID：1182370
                - 分类：立方转换，ID：1182373
                - 分类：透镜变换，ID：1182374
                - 分类：晚霞转场，ID：1182375
                - 分类：圆形交替，ID：1182378
                - 注意：如果不提供，则没有转场
                - 当视频数量超过转场数量 2 个及以上时，系统将自动循环使用转场。例如有 10 个视频，2 种转场效果，那么在 9 处拼接点上，这 2 种转场效果将被依次循环使用。
            - space_name(str): ** 必选字段 ** , 任务产物的上传空间。AI 处理生成的视频将被上传至此点播空间。
        Returns:
            - VCreativeId(str): AI 智剪任务 ID，用于查询任务状态。可以通过调用 `get_v_creative_task_result` 接口查询任务状态。
            - Code(int): 任务状态码。为 0 表示任务执行成功。
            - StatusMessage(str): 接口请求的状态信息。当 StatusCode 为 0 时，此时该字段返回 success，表示成功；其他状态码时，该字段会返回具体的错误信息。
            - StatusCode(int): 接口请求的状态码。0 表示成功，其他值表示不同的错误状态。
        """
        try:
            params = {"images": images, "space_name": space_name, "transitions": transitions}
            if "space_name" not in params:
                raise ValueError("image_to_video: params must contain space_name")
            if not isinstance(params["space_name"], str):
                raise TypeError("image_to_video: params['space_name'] must be a string")
            if not params["space_name"].strip():
                raise ValueError("image_to_video: params['space_name'] cannot be empty")
            if "images" not in params:
                raise ValueError("image_to_video: params must contain images")
            if not isinstance(params["images"], list):
                raise TypeError("image_to_video: params['images'] must be a list")
            if not params["images"]:
                raise ValueError("image_to_video: params['images'] must contain at least one image")
            
            # 格式化图片列表
            formattedImages = []
            for image in params.get("images", []):
                if isinstance(image, dict):
                    imgType = image.get("type", "vid")
                    imgSource = image.get("source", "")
                    formattedSource = _format_source(imgType, imgSource) if imgType in ["vid", "directurl"] else imgSource
                    formattedImage = {
                        "type": imgType,
                        "source": formattedSource,
                    }
                    if "duration" in image:
                        formattedImage["duration"] = image["duration"]
                    if "animation_type" in image:
                        formattedImage["animation_type"] = image["animation_type"]
                    if "animation_in" in image:
                        formattedImage["animation_in"] = image["animation_in"]
                    if "animation_out" in image:
                        formattedImage["animation_out"] = image["animation_out"]
                    formattedImages.append(formattedImage)
                elif hasattr(image, 'type') and hasattr(image, 'source'):
                    # InputSource 对象
                    imgType = image.type or "vid"
                    imgSource = image.source or ""
                    formattedSource = _format_source(imgType, imgSource) if imgType in ["vid", "directurl"] else imgSource
                    formattedImage = {
                        "type": imgType,
                        "source": formattedSource,
                    }
                    formattedImages.append(formattedImage)
                else:
                    formattedImages.append(image)
            
            ParamObj = {
                "space_name": params["space_name"],
                "images": formattedImages,
                "transitions": params.get("transitions", []),
            }
            
            audioVideoStitchingParams = {
                "ParamObj": ParamObj,
                "Uploader": params["space_name"],
                "WorkflowId": "loki://167979998",
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
                raise Exception("image_to_video: %s" % e, params)
        except Exception as e:
            raise Exception("image_to_video: %s" % e, params)

    @mcp.tool()
    def compile_video_audio(video: dict, audio: dict, space_name: str, is_audio_reserve: bool = True, is_video_audio_sync: bool = False, sync_mode: str = "video", sync_method: str = "trim") -> dict:
        """The compilation of video and audio capabilities require the transmission of both ** audio and video resources ** for processing.
        Args:
            - video(dict): ** 必选字段 **，视频信息
                - type(str): ** 必选字段 **，文件类型，默认值为 `vid` 。字段取值如下
                    - directurl
                    - http
                    - vid
                - source(str): ** 必选字段 **, 视频文件信息
            - audio(dict): ** 必选字段 **，音频信息
                - type(str): ** 必选字段 **，文件类型，默认值为 `vid` 。字段取值如下
                    - directurl
                    - http
                    - vid
                - source(str): ** 必选字段 **, 音频文件信息
            - is_audio_reserve(bool): ** 非必选字段 **, 是否保留原视频流中的音频，取值参考如下：
                - true：保留。默认值；
                - false：不保留。
            - is_video_audio_sync(bool): ** 非必选字段 **, 是否对齐音频和视频时长，取值参考如下：
                - true：通过 output_sync 配置，对齐音频和视频时长。
                - false（默认值）：保持原样输出，不做音视频对齐。最终合成的视频时长，以较长的流为准。
            - sync_mode(str): ** 非必选字段 **, ** 设置 is_video_audio_sync 为 true 时生效 **；当音频和视频时长不相等时，可指定对齐基准，可选项：video、audio。
                - video：【默认值】以视频的时长为准。
                - audio：以音频的时长为准。
            - sync_method(str): ** 非必选字段 **, **设置 is_video_audio_sync 为 true 时生效**；指定对齐方式，支持通过裁剪或加速的方式，对齐音频和视频的时长。可选项：speed、trim。
                - speed：通过加快音频或视频的速度，对齐音频和视频的时长。
                - trim：【默认值】通过裁剪音频或视频，对齐音频和视频的时长。从头开始计算并裁剪。
            - space_name(str): ** 必选字段 ** , 任务产物的上传空间。AI 处理生成的视频将被上传至此点播空间。
        Returns:
            - VCreativeId(str): AI 智剪任务 ID，用于查询任务状态。可以通过调用 `get_v_creative_task_result` 接口查询任务状态。
            - Code(int): 任务状态码。为 0 表示任务执行成功。
            - StatusMessage(str): 接口请求的状态信息。当 StatusCode 为 0 时，此时该字段返回 success，表示成功；其他状态码时，该字段会返回具体的错误信息。
            - StatusCode(int): 接口请求的状态码。0 表示成功，其他值表示不同的错误状态。
        """
        try:
            params = {"video": video, "audio": audio, "space_name": space_name, "is_audio_reserve": is_audio_reserve, "is_video_audio_sync": is_video_audio_sync, "sync_mode": sync_mode, "sync_method": sync_method}
            if "space_name" not in params:
                raise ValueError("compile_video_audio: params must contain space_name")
            if not isinstance(params["space_name"], str):
                raise TypeError("compile_video_audio: params['space_name'] must be a string")
            if not params["space_name"].strip():
                raise ValueError("compile_video_audio: params['space_name'] cannot be empty")
            if "video" not in params:
                raise ValueError("compile_video_audio: params must contain video")
            if not isinstance(params["video"], dict) and not hasattr(params["video"], 'type'):
                raise TypeError("compile_video_audio: params['video'] must be a dict or InputSource object")
            if "audio" not in params:
                raise ValueError("compile_video_audio: params must contain audio")
            if not isinstance(params["audio"], dict) and not hasattr(params["audio"], 'type'):
                raise TypeError("compile_video_audio: params['audio'] must be a dict or InputSource object")
            
            # 格式化视频和音频
            if isinstance(params["video"], dict):
                videoType = params["video"].get("type", "vid")
                videoSource = params["video"].get("source", "")
            else:
                videoType = params["video"].type or "vid"
                videoSource = params["video"].source or ""
            formattedVideoSource = _format_source(videoType, videoSource) if videoType in ["vid", "directurl"] else videoSource
            
            if isinstance(params["audio"], dict):
                audioType = params["audio"].get("type", "vid")
                audioSource = params["audio"].get("source", "")
            else:
                audioType = params["audio"].type or "vid"
                audioSource = params["audio"].source or ""
            formattedAudioSource = _format_source(audioType, audioSource) if audioType in ["vid", "directurl"] else audioSource
            
            ParamObj = {
                "space_name": params["space_name"],
                "video": formattedVideoSource,
                "audio": formattedAudioSource,
                "is_audio_reserve": params.get("is_audio_reserve", True),
                "is_video_audio_sync": params.get("is_video_audio_sync", False),
            }
            
            if params.get("is_video_audio_sync", False):
                ParamObj["sync_mode"] = params.get("sync_mode", "video")
                ParamObj["sync_method"] = params.get("sync_method", "trim")
            
            audioVideoStitchingParams = {
                "ParamObj": ParamObj,
                "Uploader": params["space_name"],
                "WorkflowId": "loki://167984726",
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
                raise Exception("compile_video_audio: %s" % e, params)
        except Exception as e:
            raise Exception("compile_video_audio: %s" % e, params)

    @mcp.tool()
    def extract_audio(type: str, source: str, space_name: str, format: str = "m4a") -> dict:
        """Audio extraction, outputting the audio format. Supports mp3 and m4a formats. Default is m4a.
        Args:
            - type(str): ** 必选字段 **，文件类型，默认值为 `vid` 。字段取值如下
                - directurl
                - http
                - vid
            - source(str): ** 必选字段 **, 视频文件信息
            - format(str): ** 非必选字段 **, 输出音频的格式，支持 mp3、m4a 格式。默认 m4a
            - space_name(str): ** 必选字段 ** , 任务产物的上传空间。AI 处理生成的视频将被上传至此点播空间。
        Returns:
            - VCreativeId(str): AI 智剪任务 ID，用于查询任务状态。可以通过调用 `get_v_creative_task_result` 接口查询任务状态。
            - Code(int): 任务状态码。为 0 表示任务执行成功。
            - StatusMessage(str): 接口请求的状态信息。当 StatusCode 为 0 时，此时该字段返回 success，表示成功；其他状态码时，该字段会返回具体的错误信息。
            - StatusCode(int): 接口请求的状态码。0 表示成功，其他值表示不同的错误状态。
        """
        try:
            params = {"type": type, "source": source, "space_name": space_name, "format": format}
            if "space_name" not in params:
                raise ValueError("extract_audio: params must contain space_name")
            if not isinstance(params["space_name"], str):
                raise TypeError("extract_audio: params['space_name'] must be a string")
            if not params["space_name"].strip():
                raise ValueError("extract_audio: params['space_name'] cannot be empty")
            if "source" not in params:
                raise ValueError("extract_audio: params must contain source")
            
            formatValue = params.get("format", "m4a")
            if formatValue not in ["mp3", "m4a"]:
                raise ValueError("extract_audio: format must be mp3 or m4a")
            
            formattedSource = _format_source(params.get("type", "vid"), params.get("source", ""))
            ParamObj = {
                "space_name": params["space_name"],
                "source": formattedSource,
                "format": formatValue,
            }
            
            audioVideoStitchingParams = {
                "ParamObj": ParamObj,
                "Uploader": params["space_name"],
                "WorkflowId": "loki://167986559",
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
                raise Exception("extract_audio: %s" % e, params)
        except Exception as e:
            raise Exception("extract_audio: %s" % e, params)

    @mcp.tool()
    def mix_audios(audios: List[dict], space_name: str) -> dict:
        """Mix audios
        Args:
            - audios(list[dict]): ** 必选字段 **，叠加的音频列表
                - type(str): ** 必选字段 **，文件类型，默认值为 `vid` 。字段取值如下
                    - directurl
                    - http
                    - vid
                - source(str): ** 必选字段 **, 音频文件信息
            - space_name(str): ** 必选字段 ** , 任务产物的上传空间。AI 处理生成的视频将被上传至此点播空间。
        Returns:
            - VCreativeId(str): AI 智剪任务 ID，用于查询任务状态。可以通过调用 `get_v_creative_task_result` 接口查询任务状态。
            - Code(int): 任务状态码。为 0 表示任务执行成功。
            - StatusMessage(str): 接口请求的状态信息。当 StatusCode 为 0 时，此时该字段返回 success，表示成功；其他状态码时，该字段会返回具体的错误信息。
            - StatusCode(int): 接口请求的状态码。0 表示成功，其他值表示不同的错误状态。
        """
        try:
            params = {"audios": audios, "space_name": space_name}
            if "space_name" not in params:
                raise ValueError("mix_audios: params must contain space_name")
            if not isinstance(params["space_name"], str):
                raise TypeError("mix_audios: params['space_name'] must be a string")
            if not params["space_name"].strip():
                raise ValueError("mix_audios: params['space_name'] cannot be empty")
            if "audios" not in params:
                raise ValueError("mix_audios: params must contain audios")
            if not isinstance(params["audios"], list):
                raise TypeError("mix_audios: params['audios'] must be a list")
            if not params["audios"]:
                raise ValueError("mix_audios: params['audios'] must contain at least one audio")
            
            # 格式化音频列表
            formattedAudios = []
            for audio in params.get("audios", []):
                if isinstance(audio, dict):
                    audioType = audio.get("type", "vid")
                    audioSource = audio.get("source", "")
                    formattedSource = _format_source(audioType, audioSource) if audioType in ["vid", "directurl"] else audioSource
                    formattedAudios.append(formattedSource)
                elif hasattr(audio, 'type') and hasattr(audio, 'source'):
                    # InputSource 对象
                    audioType = audio.type or "vid"
                    audioSource = audio.source or ""
                    formattedSource = _format_source(audioType, audioSource) if audioType in ["vid", "directurl"] else audioSource
                    formattedAudios.append(formattedSource)
                else:
                    formattedAudios.append(audio)
            
            ParamObj = {
                "space_name": params["space_name"],
                "audios": formattedAudios,
            }
            
            audioVideoStitchingParams = {
                "ParamObj": ParamObj,
                "Uploader": params["space_name"],
                "WorkflowId": "loki://167987532",
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
                raise Exception("mix_audios: %s" % e, params)
        except Exception as e:
            raise Exception("mix_audios: %s" % e, params)

    @mcp.tool()
    def add_sub_video(video: dict, sub_video: dict, space_name: str, sub_options: Optional[dict] = None) -> dict:
        """`水印贴片`, `画中画`，Add the capability of video watermarking, support adjusting the width and height of the watermark, as well as the position in the horizontal or vertical direction, and determine the timing of the watermark's appearance in the original video by setting start_time and end_time，.
        Note:
            - 如果设置的水印开始时间、结束时间超出原始视频时长，那么输出视频的长度将以水印的结束时间为准，超出原始视频部分将以黑屏形式延续。例如原始视频为 20 秒，设置 end_time 为 30，那么输出时长为 30 秒
        Args:
            - video(dict): ** 必选字段 **，视频信息
                - type(str): ** 必选字段 **，文件类型，默认值为 `vid` 。字段取值如下
                    - directurl
                    - http
                    - vid
                - source(str): ** 必选字段 **, 视频文件信息
            - sub_video(dict): ** 必选字段 **, 水印贴片信息
                - type(str): ** 必选字段 **，文件类型，默认值为 `vid` 。字段取值如下
                    - directurl
                    - http
                    - vid
                - source(str): ** 必选字段 **, 视频文件信息
            - sub_options(dict): ** 非必选字段 **，水印贴片叠加选项信息，包含如下字段：
                - height(str): 水印的高度，支持设置为百分比（相对于视频高度）或具体像素值，例如 100% 或 100。
                - width(str): 水印的宽度，支持设置为百分比（相对于视频高度）或具体像素值，String 类型，例如 100% 或 100。
                - pos_x(str): 水印在水平方向（X 轴）的位置，以视频左上角为原点，单位：像素。例如值为 0 时，表示水印处于水平方向的最左侧；值为 100 时，表示水印相对原点向右移动 100 像素。
                - pos_y(str): 水印在垂直方向（Y 轴）的位置，以视频左上角为原点，单位：像素，例如值为 0 时，表示水印在垂直方向的最上侧；值为 100 时，表示水印相对原点向下移动 100 像素。
                - start_time(float): 水印的开始时间，单位：秒。
                - end_time(float): 水印的结束时间，单位：秒。
            - space_name(str): ** 必选字段 ** , 任务产物的上传空间。AI 处理生成的视频将被上传至此点播空间。
        Returns:
            - VCreativeId(str): AI 智剪任务 ID，用于查询任务状态。可以通过调用 `get_v_creative_task_result` 接口查询任务状态。
            - Code(int): 任务状态码。为 0 表示任务执行成功。
            - StatusMessage(str): 接口请求的状态信息。当 StatusCode 为 0 时，此时该字段返回 success，表示成功；其他状态码时，该字段会返回具体的错误信息。
            - StatusCode(int): 接口请求的状态码。0 表示成功，其他值表示不同的错误状态。
        """
        try:
            params = {"video": video, "sub_video": sub_video, "space_name": space_name, "sub_options": sub_options}
            if "space_name" not in params:
                raise ValueError("add_sub_video: params must contain space_name")
            if not isinstance(params["space_name"], str):
                raise TypeError("add_sub_video: params['space_name'] must be a string")
            if not params["space_name"].strip():
                raise ValueError("add_sub_video: params['space_name'] cannot be empty")
            if "video" not in params:
                raise ValueError("add_sub_video: params must contain video")
            if not isinstance(params["video"], dict) and not hasattr(params["video"], 'type'):
                raise TypeError("add_sub_video: params['video'] must be a dict or InputSource object")
            if "sub_video" not in params:
                raise ValueError("add_sub_video: params must contain sub_video")
            if not isinstance(params["sub_video"], dict) and not hasattr(params["sub_video"], 'type'):
                raise TypeError("add_sub_video: params['sub_video'] must be a dict or InputSource object")
            
            # 格式化视频和水印视频
            if isinstance(params["video"], dict):
                videoType = params["video"].get("type", "vid")
                videoSource = params["video"].get("source", "")
            else:
                videoType = params["video"].type or "vid"
                videoSource = params["video"].source or ""
            formattedVideoSource = _format_source(videoType, videoSource) if videoType in ["vid", "directurl"] else videoSource
            
            if isinstance(params["sub_video"], dict):
                subVideoType = params["sub_video"].get("type", "vid")
                subVideoSource = params["sub_video"].get("source", "")
            else:
                subVideoType = params["sub_video"].type or "vid"
                subVideoSource = params["sub_video"].source or ""
            formattedSubVideoSource = _format_source(subVideoType, subVideoSource) if subVideoType in ["vid", "directurl"] else subVideoSource
            
            ParamObj = {
                "space_name": params["space_name"],
                "video": formattedVideoSource,
                "sub_video": formattedSubVideoSource,
            }
            
            if params.get("sub_options") and isinstance(params["sub_options"], dict):

                    ParamObj["sub_options"] = {
                        "width": params["sub_options"].get("width", "20%"),
                        "height": params["sub_options"].get("height", "20%"),
                        "pos_x": params["sub_options"].get("pos_x", "0"),
                        "pos_y": params["sub_options"].get("pos_y", "0"),
                        **params["sub_options"],
                    }
            
            audioVideoStitchingParams = {
                "ParamObj": ParamObj,
                "Uploader": params["space_name"],
                "WorkflowId": "loki://168021310",
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
                raise Exception("add_sub_video: %s" % e, params)
        except Exception as e:
            raise Exception("add_sub_video: %s" % e, params)

  
