
import importlib
from src.vod.api.api import VodAPI
from src.vod.mcp_tools.media_tasks import create_transcode_result_server
from src.vod.utils.transcode import register_transcode_base_fn
from src.vod.mcp_tools.video_play import register_video_play_methods
from mcp.server.fastmcp import FastMCP
from pathlib import Path


import json
import os
import logging

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

# 工具名到工具分组的映射从 base_mcp 导入
# TOOL_NAME_TO_GROUP_MAP: 工具名 -> 分组名 (用于根据工具名查找分组)
# TOOL_GROUP_MAP: 分组名 -> 工具列表 (用于根据分组名获取工具列表)


def create_mcp_server(mcp: FastMCP = None):
    ## init api client
    service = VodAPI()
    ## init public methods
    public_methods = {}
    
    # 确保 mcp 不为 None
    if mcp is None:
        raise ValueError("mcp parameter cannot be None")
    
    mcp.set_base_mcp_store({
        'apiRequestInstance': service
    })
    
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

    # Store mcp instance in service for context access
    service._mcp_instance = mcp
    logging.info(f"Set _mcp_instance on service: {mcp is not None}")
    
    # 注册所有工具（启动时注册所有工具，在 streamable HTTP 建联时会根据 header 动态过滤）
    # 注意：这里注册所有工具，而不是只注册 current_tool_groups
    # 因为 streamable HTTP 模式下，每次请求的 header 可能不同
    _load_tools(AVAILABLE_GROUPS)
    
    
    return mcp
