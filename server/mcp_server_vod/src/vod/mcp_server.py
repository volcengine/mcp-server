
import importlib
from src.vod.api.api import VodAPI
from src.vod.mcp_tools.media_tasks import create_transcode_result_server
from src.vod.utils.transcode import register_transcode_base_fn
from src.vod.mcp_tools.video_play import register_video_play_methods
from mcp.server.fastmcp import FastMCP
from pathlib import Path

from urllib.parse import quote
import json
import os

AVAILABLE_GROUPS = [
# 视频剪辑相关tools
"edit",
# 智能切片相关tools
"intelligent_slicing",
# 智能抠图相关tools
"intelligent_matting",
# 字幕处理相关tools
"subtitle_processing",
# 音频处理相关tools
"audio_processing",
# 视频增强相关tools
"video_enhancement",
# 上传相关
'upload',
# 视频播放相关
"video_play"
]


DEFAULT_GROUPS = [
    "edit",
    "video_play"
]

TRANSCODE_GROUPS = {
    # 智能切片相关tools
    "intelligent_slicing",
    # 智能抠图相关tools
    "intelligent_matting",
    # # 字幕处理相关tools
    # "subtitle_processing",
    # 音频处理相关tools
    "audio_processing",
    # 视频增强相关tools
    "video_enhancement",
}

ALL_GROUPS = 'all'

def create_mcp_server(groups: list[str] = None, mcp: FastMCP = None):
    ## init api client
    service = VodAPI()
    ## init public methods
    public_methods = {}

    ## init tool groups
    current_tool_groups = []
    env_type = os.getenv("MCP_TOOL_GROUPS")
   
    if groups is not None:
       if ALL_GROUPS in groups:
            current_tool_groups = AVAILABLE_GROUPS
       else:
            current_tool_groups = groups
    elif env_type is not None:
        env_grops= [group.strip() for group in env_type.split(",") if group.strip()]
        try:
            if ALL_GROUPS in env_grops:
                current_tool_groups = AVAILABLE_GROUPS
            else:
                current_tool_groups = env_grops
            print(f"[MCP] Loaded tool groups from environment: {current_tool_groups}")
        except Exception as e:
            print(f"[MCP] Error parsing MCP_TOOL_GROUPS environment variable: {e}")
            current_tool_groups = DEFAULT_GROUPS
    else:
        current_tool_groups = DEFAULT_GROUPS

    
    ## update media publish status
    def update_media_publish_status  (vid: str, SpaceName: str, PublishStatus: str) ->  str: 
        """Update the publish status of a media.
        
        Args:
            vid (str): The video ID.
            SpaceName (str): The VOD space name.
            PublishStatus (str): The publish status to set.
        
        Returns:
            str: "success" if the operation is successful.
        
        """
        try:
            service.mcp_post("McpUpdateMediaPublishStatus", {}, json.dumps({
                "Vid": vid,
                "Status": PublishStatus,
            }))
            return "success"
        except Exception as e:
           raise Exception("update_media_publish_status: %s" % e)

    def get_play_video_info  (vid: str, SpaceName: str, OutputType: str = 'CDN') ->  str: 
        """Get the publish status of a media.
        Args:
            - vid (str): The video ID.
            - SpaceName (str): The VOD space name.
            - OutputType (str, optional): The output type. Defaults to 'CDN'， 取值为： CDN 或 Origin.
        
        Returns:
            - PlayURL (str): 视频播放地址.
            - Duration (float): 视频时长，单位秒.
            - FormatName (str): 容器名称.
            - Size (float): 大小，单位为字节.
            - BitRate (str): 码率，单位为 bps.
            - CodecName (str): 编码器名称.
            - AvgFrameRate (str): 视频平均帧率，单位为 fps.
            - Width (int): 视频宽，单位为 px.
            - Height (int): 视频高，单位为 px.
        
        """
        reqs = service.mcp_get("McpGetVideoPlayInfo", {
            "Space": SpaceName,
            "Vid": vid,
            "DataType": 0,
            "OutputType": OutputType,
        },json.dumps({}))
        url =  None
        duration = 0
        formatName = ""
        size = 0
        bitRate = ""
        codecName = ""
        avgFrameRate = ""
        width = 0
        height = 0

        if isinstance(reqs, str):
            reqs = json.loads(reqs)
            result = reqs.get("Result", {})
            videoDetail = result.get("VideoDetail", {})
            videoDetailInfo = videoDetail.get("VideoDetailInfo", {})
            playInfo = videoDetailInfo.get("PlayInfo", {})
            durationValue = videoDetailInfo.get("Duration")
            duration = float(durationValue) if durationValue is not None else 0
            
            # 提取完整的视频信息
            formatName = videoDetailInfo.get("Format", "")
            sizeValue = videoDetailInfo.get("Size")
            size = float(sizeValue) if sizeValue is not None else 0
            bitRate = str(videoDetailInfo.get("Bitrate", "")) if videoDetailInfo.get("Bitrate") else ""
            codecName = videoDetailInfo.get("Codec", "")
            avgFrameRate = str(videoDetailInfo.get("Fps", "")) if videoDetailInfo.get("Fps") else ""
            width = int(videoDetailInfo.get("Width", 0)) if videoDetailInfo.get("Width") else 0
            height = int(videoDetailInfo.get("Height", 0)) if videoDetailInfo.get("Height") else 0

            if videoDetailInfo.get("PublishStatus") == 'Published':
                url = playInfo.get("MainPlayURL", None) or playInfo.get("BackupPlayUrl", None)
                if url is None:
                    urlDta = get_play_video_info(vid, SpaceName, 'Origin')
                    urlTmp = json.loads(urlDta)
                    url = urlTmp.get("PlayURL", "")
            else:
                publishStatus = update_media_publish_status(vid, SpaceName, 'Published')
                if publishStatus == 'success':
                    urlDta = get_play_video_info(vid, SpaceName, 'Origin')
                    urlTmp = json.loads(urlDta)
                    url = urlTmp.get("PlayURL", "")
                else:
                     raise Exception("update publish status failed：", reqs, publishStatus)
        if url is None:
            raise Exception("%s: get publish url failed" % vid)
        return json.dumps({
            "PlayURL": url,
            "Duration": duration,
            "FormatName": formatName,
            "Size": size,
            "BitRate": bitRate,
            "CodecName": codecName,
            "AvgFrameRate": avgFrameRate,
            "Width": width,
            "Height": height,
        })
    
    public_methods["update_media_publish_status"] = update_media_publish_status
    public_methods["get_play_video_info"] = get_play_video_info
    register_video_play_methods(service,public_methods)

    register_transcode_base_fn(service, public_methods)
    print(f"[MCP] Loaded tool groups: {public_methods}")
    

    def _load_tools(groupList: list[str]):
        """
        动态加载工具组
        """
        tools_dir = Path(__file__).parent / "mcp_tools"
        print(f"[MCP] Loaded tool: {tools_dir} groups: {groupList}")
        media_flag = True  
        for file in os.listdir(tools_dir):
            if not file.endswith(".py") or file.startswith("_") or file == "__init__.py":
                    continue
            fileName = file[:-3]
            if fileName not in AVAILABLE_GROUPS or fileName == 'media_tasks' or fileName not in groupList:
                continue
            module_name = f"src.vod.mcp_tools.{fileName}"
            module = importlib.import_module(module_name)
            if hasattr(module, "create_mcp_server"):
                # if it is transcode group, add create transcode result server
                if fileName in TRANSCODE_GROUPS:
                    module.create_mcp_server(mcp, public_methods)
                    if media_flag:
                        create_transcode_result_server(mcp, public_methods)
                        media_flag = False
                    print(f"[MCP] Loaded tool: {module_name}")
                else:
                    module.create_mcp_server(mcp, public_methods, service)
                    print(f"[MCP] Loaded tool: {module_name}")

    _load_tools(current_tool_groups)
    return mcp
