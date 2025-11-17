from src.vod.api.api import VodAPI
from mcp.server.fastmcp import FastMCP
import json
import os

def create_mcp_server():
    service = VodAPI()
    mcp = FastMCP(
        name="VOD MCP",
        host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
        port=int(os.getenv("MCP_SERVER_PORT", "8000")),
        stateless_http=os.getenv("STATLESS_HTTP", "true").lower() == "true",
        streamable_http_path=os.getenv("STREAMABLE_HTTP_PATH", "/mcp"),
        instructions="""
      ## VOD MCP is the Volcengine VOD MCP Server.
      ### Before using the VOD service, please note:
      - `SpaceName` is the name of the VOD space.
      - `Vid` is the video ID.
      """,
    )

    def update_media_publish_status  (vid: str, SpaceName: str, PublishStatus: str) ->  str: 
        """Update the publish status of a media."""
        try:
            service.update_media_publish_status({
                "SpaceName": SpaceName,
                "Vid": vid,
                "PublishStatus": PublishStatus,
            })
            return "success"
        except Exception as e:
            return "failed"

    def get_play_video_info  (vid: str, SpaceName: str, DataType: int = 0, OutputType: str = 'CDN') ->  str: 
        """Get the publish status of a media."""
        reqs = service.get_media_publish_status({
            "SpaceName": SpaceName,
            "Vid": vid,
            "DataType": DataType,
            "OutputType": OutputType,
        })
        url =  None
        if isinstance(reqs, str):
            reqs = json.loads(reqs)
            result = reqs.get("Result", {})
            videoDetailInfo = result.get("VideoDetailInfo", {})
            if videoDetailInfo.get("PublishStatus") == 'Published':
                url = videoDetailInfo.get("MainPlayURL", None) or videoDetailInfo.get("BackupPlayUrl", None)
                if url is None:
                   url = get_video_publish_info(vid, SpaceName, DataType, 'Origin')
            else:
                publishStatus = update_media_publish_status(vid, SpaceName, 'Published')
                if publishStatus == 'success':
                    url = get_video_publish_info(vid, SpaceName, DataType, 'Origin')
                else:
                     raise Exception("%s: update publish status failed" % vid)
        if url is None:
            raise Exception("%s: get publish url failed" % vid)
        return url


    @mcp.tool()
    def audio_video_stitching(params: dict) -> str:
        """ Carry out video stitching, audio stitching, and support for transitions and other capabilities，需要参考 Note 中的要求。
         Note:
            -  **audio splicing does not support transitions. **
            -  ** vid 模式下需要增加  vid://  前缀， 示例：vid://123456 **
            -  ** directurl://{fileName} 格式指定资源的 FileName。示例：directurl://test.mp3**
            -  ** http(s):// 格式指定资源的 URL。示例：http://example.com/test.mp4**
         Args:
            - SpaceName(str):  **  必选字段 ** , 任务产物的上传空间。AI 处理生成的视频将被上传至此点播空间。
            - videos(List[str]): **  必选字段 **
                - 待拼接的视频列表：支持 ** vid:// ** 、 ** http:// ** 格式，** directUrl:// ** 格式
                    *** 视频要求： *** 
                        - 支持处理 MP4、AVI、MKV、MOV 等常见格式的视频。 
                        - 建议总视频时长在 5 分钟以内。 
            - transitions(List[str]): 非必选字段
                - 转场效果 ID：例如 ["1182359"]。concat_videos 工具支持非交叠转场的效果，
                    - 可用于非交叠转场的动画
                    - 分类：交替出场，ID：1182359
                    - 分类：旋转放大，ID：1182360
                    - 分类：泛开，ID：1182358
                    - 分类：风车，ID：1182362
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
            - VCreativeId(str)：AI 智剪任务 ID
            - Code(int):  任务状态码。为 0表示任务执行成功。
            - StatusMessage(str): 接口请求的状态信息。当 StatusCode 为 0 时，此时该字段返，success，表示成功；其他状态码时，该字段会返回具体的错误信息。
            - StatusCode(int):  接口请求的状态码。0表示成功，其他值表示不同的错误状态。
        
        """
        if "SpaceName" not in params:
            raise ValueError("audio_video_stitching: params must contain SpaceName")
        if not isinstance(params["SpaceName"], str):
            raise TypeError("audio_video_stitching: params['SpaceName'] must be a string")
        if not params["SpaceName"].strip():
            raise ValueError("audio_video_stitching: params['SpaceName'] cannot be empty")
        if "videos" not in params:
            raise ValueError("audio_video_stitching: params must contain videos")
        if not isinstance(params["videos"], list):
            raise TypeError("audio_video_stitching: params['videos'] must be a list")
        if not params["videos"]:
            raise ValueError("audio_video_stitching: params['videos'] must contain at least one video")
        
        
        ParamObj = {
            "space_name": params["SpaceName"],
            "videos": params["videos"],
            "transitions": params.get("transitions", []),
        }

        audioVideoStitchingParams ={
            "ParamObj": str(ParamObj),
            "Uploader": params["SpaceName"],
            "WorkflowId": "loki://154775772",
        }
        reqs = None
        try:
            reqs = service.mcp_post("VodMcpAsyncVCreativeTask", {}, json.dumps(audioVideoStitchingParams))
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
            raise Exception("audio_video_stitching: %s" % e)

    @mcp.tool()
    def audio_video_clipping(params: dict) -> str:
        """ Invoke the current tools to complete the cropping of audio and video，需要参考 Note 中的要求。
         Note:
            -  **audio splicing does not support transitions. **
            -  ** vid 模式下需要增加  vid://  前缀， 示例：vid://123456 **
            -  ** directurl://{fileName} 格式指定资源的 FileName。示例：directurl://test.mp3**
            -  ** http(s):// 格式指定资源的 URL。示例：http://example.com/test.mp4**
         Args:
            - SpaceName(str):  **  必选字段 ** , 任务产物的上传空间。AI 处理生成的视频将被上传至此点播空间。
            - videos(List[str]): **  必选字段 **
                - 待拼接的视频列表：支持 ** vid:// ** 、 ** http:// ** 格式，** directUrl:// ** 格式
                    *** 视频要求： *** 
                        - 支持处理 MP4、AVI、MKV、MOV 等常见格式的视频。 
                        - 建议总视频时长在 5 分钟以内。 
            - end_time(int): **  必选字段 **
                - 裁剪结束时间，默认为片源结尾。支持设置为 2 位小数，单位：秒。 设置设置为 8，则表示在 8 秒位置结束裁剪。 
            - start_time(int): **  必选字段 **
                - 裁剪开始时间，默认为 0， 表示从头开始裁剪。支持设置为 2 位小数，单位：秒。 例如设置为 2，则表示从 2 秒的位置开始裁剪。 
        Returns：
            - VCreativeId(str)：AI 智剪任务 ID
            - Code(int):  任务状态码。为 0表示任务执行成功。
            - StatusMessage(str): 接口请求的状态信息。当 StatusCode 为 0 时，此时该字段返，success，表示成功；其他状态码时，该字段会返回具体的错误信息。
            - StatusCode(int):  接口请求的状态码。0表示成功，其他值表示不同的错误状态。
        
        """
        if "SpaceName" not in params:
            raise ValueError("audio_video_stitching: params must contain SpaceName")
        if not isinstance(params["SpaceName"], str):
            raise TypeError("audio_video_stitching: params['SpaceName'] must be a string")
        if not params["SpaceName"].strip():
            raise ValueError("audio_video_stitching: params['SpaceName'] cannot be empty")
        if "videos" not in params:
            raise ValueError("audio_video_stitching: params must contain videos")
        if not isinstance(params["videos"], list):
            raise TypeError("audio_video_stitching: params['videos'] must be a list")
        if not params["videos"]:
            raise ValueError("audio_video_stitching: params['videos'] must contain at least one video")
        
        
        ParamObj = {
            "space_name": params["SpaceName"],
            "videos": params["videos"],
            "transitions": params.get("transitions", []),
        }

        audioVideoStitchingParams ={
            "ParamObj": str(ParamObj),
            "Uploader": params["SpaceName"],
            "WorkflowId": "loki://154419276",
        }
        reqs = None
        try:
            reqs = service.mcp_post("VodMcpAsyncVCreativeTask", {}, json.dumps(audioVideoStitchingParams))
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
            raise Exception("audio_video_stitching: %s" % e)
    
    @mcp.tool()
    def get_v_creative_task_result(params: dict) -> str:
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
        
        reqs = service.mcp_get("VodMcpGetVCreativeTaskResult", {"VCreativeId": params["VCreativeId"]}, json.dumps({}))

        if isinstance(reqs, str):
            reqs = json.loads(reqs)
            reqsTmp = reqs.get('Result', {})
            # BaseResp = reqsTmp.get("BaseResp", {})
            url = reqsTmp.get("url", "")
            # 任务状态
            taskStatus = reqsTmp.get("Status", "")
            if taskStatus is "success":
                outputJson = reqsTmp.get("OutputJson", {})
                vid = outputJson.get("vid")
                if vid is None:
                    raise Exception("get_v_creative_task_result: vid is None")
                else:
                   url = get_play_video_info(vid, params["SpaceName"])
                return json.dumps({
                    outputJson: {
                        "vid": vid,
                        "resolution": outputJson.get("resolution"),
                        "duration": outputJson.get("duration"),
                        "filename": outputJson.get("filename"),
                        "url": url,
                    },
                    "Status": taskStatus,
                })
            else:
                return json.dumps(reqsTmp)
        else:
            return reqs
    
    return mcp
