from __future__ import annotations

from typing import Any, Dict, List, Optional
from typing_extensions import NotRequired, Required, TypedDict

try:
    from pydantic import Field
except Exception:  # pragma: no cover
    def Field(*args, **kwargs):
        if args:
            return args[0]
        return kwargs.get("default", None)

try:
    from mcp.server.fastmcp.server import Context
    from mcp.server.session import ServerSession
except Exception:  # pragma: no cover
    class Context:  # type: ignore
        pass

    class ServerSession:  # type: ignore
        pass

from base.client import MediKitClient
from ..utils.response import async_task_response, error_response

TOOL_NAMES = ['probe_audio_metadata', 'separate_voice']


def register_tools(mcp, client: MediKitClient) -> None:
    @mcp.tool(name="separate_voice", description="将音频中的人声与背景音精准分离，输出为两个独立的音轨文件。\n支持格式：主流音视频格式（如mp4、mov、mp3、m4a、wav等）。\n输入：video_url和audio_url二选一。\n输出格式：AAC。 使用 task_id, 调用 query_task 方法获取结果")
    async def separate_voice(
        video_url: Optional[str] = Field(None, description="输入视频 Url（需公网可访问），与audio_url二选一，都存在时优先取video_url"),
        audio_url: Optional[str] = Field(None, description="输入音频 Url（需公网可访问），与video_url二选一，不能都为空"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """将音频中的人声与背景音精准分离，输出为两个独立的音轨文件。
支持格式：主流音视频格式（如mp4、mov、mp3、m4a、wav等）。
输入：video_url和audio_url二选一。
输出格式：AAC。"""
        try:
            result = client.call(api_name="separate_voice", video_url=video_url, audio_url=audio_url, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="probe_audio_metadata", description="获取指定音频的详细元信息，输出容器层信息（format_meta）与音频流元信息（audio_stream_meta）。\n字段分类参考 ffprobe，并对 VOD 原始返回做精简与统一。\n使用限制：支持公网 HTTP/HTTPS URL。 使用 task_id, 调用 query_task 方法获取结果")
    async def probe_audio_metadata(
        audio_url: str = Field(..., description="待探测的音频公网 HTTP/HTTPS URL。"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """获取指定音频的详细元信息，输出容器层信息（format_meta）与音频流元信息（audio_stream_meta）。
字段分类参考 ffprobe，并对 VOD 原始返回做精简与统一。
使用限制：支持公网 HTTP/HTTPS URL。"""
        try:
            result = client.call(api_name="probe_audio_metadata", audio_url=audio_url, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    if hasattr(mcp, "register_domain_tools"):
        mcp.register_domain_tools("audio", TOOL_NAMES)
