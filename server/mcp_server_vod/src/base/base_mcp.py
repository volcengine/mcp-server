from mcp.server.fastmcp import FastMCP
from mcp.shared.context import LifespanContextT, RequestT
import logging
from typing import Dict, Any,Optional
from collections.abc import (
    Sequence,
)

from mcp.server.fastmcp.server import Context
from mcp.server.session import ServerSessionT
from mcp.types import ContentBlock
from mcp.server.session import ServerSession
from starlette.requests import Request
from src.base.constant import (
    # VOLCENGINE_ACCESS_KEY_HEADER,
    # VOLCENGINE_SECRET_KEY_HEADER,
    # VOLCENGINE_SESSION_TOKEN_HEADER,
    # VOLCENGINE_HOST_HEADER,
    # VOLCENGINE_REGION_HEADER,
    VOLCENGINE_TOOLS_SOURCE_HEADER,
    VOLCENGINE_TOOLS_TYPE_HEADER,
    VOLCENGINE_SPACE_NAME_HEADER,
    VOLCENGINE_SPACE_NAME_ENV,

    # VOLCENGINE_ACCESS_KEY_ENV,
    # VOLCENGINE_SECRET_KEY_ENV, 
    # VOLCENGINE_SESSION_TOKEN_ENV,
    # VOLCENGINE_HOST_ENV,
    # VOLCENGINE_REGION_ENV,
    VOLCENGINE_TOOLS_SOURCE_ENV,
    VOLCENGINE_TOOLS_TYPE_ENV
)

from os import environ

logger = logging.getLogger(__name__)

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

DEFAULT_TOOL_LIST = [
    "audio_video_stitching",
    "audio_video_clipping",
    "get_v_creative_task_result",
    "get_play_url",
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

# 工具分组到工具列表的映射
# 所有分组统一为列表格式，用于在 list_tools 时动态过滤
TOOL_GROUP_MAP = {
    # edit 分组
    "edit": [
        "audio_video_stitching",
        "audio_video_clipping",
        "get_v_creative_task_result",
        "flip_video",
        "speedup_video",
        "speedup_audio",
        "image_to_video",
        "compile_video_audio",
        "extract_audio",
        "mix_audios",
        "add_sub_video",
        "wait_for_v_creative_task_result",
    ],
    # video_play 分组
    "video_play": [
        "get_play_url",
        "get_video_audio_info"
    ],
    # upload 分组
    "upload": [
        "video_batch_upload",
        "query_batch_upload_task_info"
    ],
    # intelligent_slicing 分组
    "intelligent_slicing": [
        "intelligent_slicing_task"
    ],
    # intelligent_matting 分组
    "intelligent_matting": [
        "portrait_image_retouching_task",
        "green_screen_task"
    ],
    # subtitle_processing 分组
    "subtitle_processing": [
        "asr_speech_to_text_task",
        "ocr_text_to_subtitles_task",
        "video_subtitles_removal_task",
        "add_subtitle",
    ],
    # audio_processing 分组
    "audio_processing": [
        "voice_separation_task",
        "audio_noise_reduction_task"
    ],
    # video_enhancement 分组
    "video_enhancement": [
        "video_interlacing_task",
        "video_super_resolution_task",
        "video_quality_enhancement_task"
    ],
    # media_tasks 分组（通用）
    "media_tasks": [
        "get_media_execution_task_result"
    ],
}

# 工具名到工具分组的反向映射，用于快速查找工具所属分组
TOOL_NAME_TO_GROUP_MAP = {}
for group_name, tool_list in TOOL_GROUP_MAP.items():
    for tool_name in tool_list:
        TOOL_NAME_TO_GROUP_MAP[tool_name] = group_name




class BaseMCP(FastMCP):
    def __init__(self, 
        name: str | None = None, # 
        instructions: str | None = None,
        host: str = "127.0.0.1", # 
        port: int = 8000, # 
        streamable_http_path: str = "/mcp", # 
        stateless_http: bool = False, # 
        ):
        super().__init__(
            name=name,
            host=host,
            port=port,
            stateless_http=stateless_http,
            streamable_http_path=streamable_http_path,
            instructions=instructions
        )
        self._base_mcp_store = {}
    
    def set_base_mcp_store(self, store: Dict[Any, Any]) -> Dict:  
        """设置 base_mcp_store
        
        Args:
            store: 要存储的字典
            
        Returns:
            Dict: 更新后的 _base_mcp_store
        """
        self._base_mcp_store = {
            **self._base_mcp_store,
            **store
        }
        return self._base_mcp_store
    
    def get_base_mcp_store(self, key: Any) -> Any: 
        """获取 base_mcp_store 中的值
        
        Args:
            key: 要获取的键
            
        Returns:
            Any: 对应的值，如果 key 为 None 或不存在则返回 None
        """
        if key is None:
            return None
        return self._base_mcp_store.get(key)
    def get_request_ctx(self) -> Optional[Request]: 
        """获取当前请求的 Request 对象
        
        Returns:
            Optional[Request]: 当前请求的 Request 对象，如果无法获取则返回 None
        """
        try:
            ctx: Optional[Context[ServerSession, object]] = self.get_context()
            if ctx and hasattr(ctx, 'request_context') and ctx.request_context:
                raw_request: Optional[Request] = ctx.request_context.request
                return raw_request
        except Exception as e:
            logger.debug(f"Failed to get request context: {e}")
        return None

    def _handle_display_tools(self) -> tuple[Optional[str], Optional[list[str]]]: 
        """处理要显示的工具列表或分组列表
        
        优先级：header > 环境变量 > _base_mcp_store
        
        Returns:
            tuple[Optional[str], Optional[list[str]]]: (tools_type, tools/sources列表)，如果未配置则返回 (None, None)
        """
        tools_type = None
        tools_source = None
        
        # 优先级1: 从 header 获取
        try:
            raw_request: Optional[Request] = self.get_request_ctx()
            if raw_request:
                headers = raw_request.headers
                tools_type_h = headers.get(VOLCENGINE_TOOLS_TYPE_HEADER)
                tools_source_h = headers.get(VOLCENGINE_TOOLS_SOURCE_HEADER)
                
                if tools_type_h and tools_source_h:
                    if tools_type_h in ['tools', 'groups']:
                        tools_type = tools_type_h
                        tools_source = [item.strip() for item in tools_source_h.split(',') if item.strip()]
                        logger.debug(f"Got tools_type and source from header: {tools_type}, {tools_source}")
                        return (tools_type, tools_source)
        except Exception as e:
            logger.debug(f"Failed to get tools from header: {e}")
        
        # 优先级2: 从环境变量获取
        tool_type_e = environ.get(VOLCENGINE_TOOLS_TYPE_ENV)
        tools_source_e = environ.get(VOLCENGINE_TOOLS_SOURCE_ENV)

        if tool_type_e is None and tools_source_e is None:
            source_groups = environ.get("MCP_TOOL_GROUPS")
            if source_groups:
                tool_type_e = 'groups'
                tools_source_e = source_groups

        if tool_type_e and tools_source_e:
            if tool_type_e in ['tools', 'groups']:
                tools_type = tool_type_e
                tools_source = [item.strip() for item in tools_source_e.split(',') if item.strip()]
                logger.debug(f"Got tools_type and source from environment: {tools_type}, {tools_source}")
                return (tools_type, tools_source)
        
        
        # 优先级3: 从 _base_mcp_store 获取
        tools_type_store = self.get_base_mcp_store('tools_type')
        source_store = self.get_base_mcp_store('source')
        
        if tools_type_store and source_store:
            if tools_type_store in ['tools', 'groups']:
                # 如果 source_store 是字符串，需要分割
                if isinstance(source_store, str):
                    tools_source = [item.strip() for item in source_store.split(',') if item.strip()]
                elif isinstance(source_store, list):
                    tools_source = [str(item).strip() for item in source_store if item]
                else:
                    tools_source = None
                
                if tools_source:
                    tools_type = tools_type_store
                    logger.debug(f"Got tools_type and source from _base_mcp_store: {tools_type}, {tools_source}")
                    return (tools_type, tools_source)
        
        # 如果都没有配置，返回默认工具列表
        logger.debug("No tools configuration found, using DEFAULT_TOOL_LIST")
        return ('tools', DEFAULT_TOOL_LIST) 
    async def list_tools(self):
        """Get the list of tools available for this MCP instance.
        Returns:
            list[Tool]: A list of Tool objects.
        """
        try:
            res = await super().list_tools()
            
            # 获取要显示的工具列表或分组列表
            # _handle_display_tools 返回 (tools_type, tools/sources列表)
            tools_type, display_config = self._handle_display_tools()
            
            if tools_type is None or display_config is None:
                # 如果没有配置，返回所有工具
                logger.info(f"BaseMCP.list_tools: no filter, returning all {len(res)} tools")
                return res
            
            # 获取允许的工具列表
            allowed_tools = set()
            
            if tools_type == 'tools':
                # 如果指定的是工具列表，直接使用
                allowed_tools = set(display_config)
            elif tools_type == 'groups':
                # 如果指定的是分组列表，从 TOOL_GROUP_MAP 中获取对应的工具
                for group_name in display_config:
                    if group_name == ALL_GROUPS:
                        # 如果指定了 "all"，返回所有工具
                        logger.info(f"BaseMCP.list_tools: returning all {len(res)} tools (all groups)")
                        return res
                    if group_name in TOOL_GROUP_MAP:
                        logger.info(f"TOOL_GROUP_MAP {TOOL_GROUP_MAP[group_name]} tools in group {group_name}")
                        allowed_tools.update(TOOL_GROUP_MAP[group_name])
            
            # 过滤工具
            filtered_tools = []
            for tool in res:
                if tool.name in allowed_tools:
                    filtered_tools.append(tool)
            
            logger.info(f"BaseMCP.list_tools: filtered to {len(filtered_tools)}/{len(res)} tools based on {tools_type}: {display_config}")
            return filtered_tools
        except Exception as e:
            logger.error(f"BaseMCP.list_tools failed with error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return []
    async def call_tool(self,
     name: str, 
     arguments: dict[str, Any],
    ) -> Sequence[ContentBlock] | dict[str, Any]:
        """Call a tool by name with arguments."""
        try:
            context: Optional[Request] = self.get_request_ctx()
            ctx: Optional[Context[ServerSession, object]] = self.get_context()
            arguments['ctx'] = ctx
            if self._base_mcp_store.get('apiRequestInstance'):
                apiRequestInstance = self._base_mcp_store['apiRequestInstance']
                if  hasattr(apiRequestInstance, 'set_headers') and name:
                    apiRequestInstance.set_headers('x-tt-tools-name', name)

            # 兼容处理 space_name, spaceName, space
            space_name_value = None
            for key in ['space_name', 'spaceName', 'space']:
                if key in arguments and arguments[key] and isinstance(arguments[key], str) and arguments[key].strip():
                    space_name_value = arguments[key].strip()
                    break
            
            if space_name_value:
                arguments['space_name'] = space_name_value
            else:
                space_name_env = environ.get(VOLCENGINE_SPACE_NAME_ENV)
                if context and hasattr(context, 'headers'):
                    headers = context.headers
                    space_name_h = headers.get(VOLCENGINE_SPACE_NAME_HEADER)
                    if space_name_h:
                        arguments['space_name'] = space_name_h.strip()
                    elif space_name_env:
                        arguments['space_name'] = space_name_env.strip()
                elif space_name_env:
                    arguments['space_name'] = space_name_env.strip()
            space_name = arguments.get('space_name') 
            if not space_name or not isinstance(space_name, str) or not space_name.strip():
                raise Exception('space_name is required')
            print(f"space_name: {space_name}",arguments)
            return await super().call_tool(name, arguments)
        except Exception as e:
            logger.error(f"BaseMCP.call_tool failed with error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise e
