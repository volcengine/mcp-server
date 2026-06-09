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

class EraseVideoSubtitleProEraseRatioLocationItem(TypedDict):
    top_left_x: Required[float]
    top_left_y: Required[float]
    bottom_right_x: Required[float]
    bottom_right_y: Required[float]

TOOL_NAMES = ['enhance_video', 'erase_video_subtitle_pro']


def register_tools(mcp, client: MediKitClient) -> None:
    @mcp.tool(name="enhance_video", description="画质增强：针对 AIGC / UGC / 短剧 / 教育 / 游戏 / 老片修复等场景，提供画质提升 + 超分增强一站式解决方案。依托 AI MediaKit 智能媒体处理引擎，融合视频内容理解、画质指标智能决策、多维度增强原子算法，实现画质的全面优化。\n支持格式：主流视频格式如mp4、flv、ts、avi、mov、wmv、mkv。\n使用限制：单文件大小不超过100G。 使用 task_id, 调用 query_task 方法获取结果")
    async def enhance_video(
        video_url: str = Field(..., description="输入视频。String 类型，支持http://xxx或https://xxx格式 URL"),
        scene: Optional[str] = Field('common', description="场景化模板类型。用于选择一个针对特定业务场景的预设画质增强模板。支持的取值如下：common（默认值）: 通用模板；ugc: UGC 短视频；short_series: 短剧；aigc: AIGC 内容；old_film: 老片修复"),
        tool_version: Optional[str] = Field('standard', description="工具版本，标准版:standard，专业版：professional，默认为标准版"),
        resolution: Optional[str] = Field(None, description="目标分辨率。支持的取值如下所示。配置此参数后，不可同时配置resolution_limit字段"),
        resolution_limit: Optional[int] = Field(None, description="目标长宽限制，用于指定输出视频的长边或短边的最大像素值，取值范围为 [64, 2160]。配置此参数后，不可同时配置resolution字段"),
        fps: Optional[float] = Field(None, description="目标帧率，单位为 fps。取值范围为 (0, 120]。"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """画质增强：针对 AIGC / UGC / 短剧 / 教育 / 游戏 / 老片修复等场景，提供画质提升 + 超分增强一站式解决方案。依托 AI MediaKit 智能媒体处理引擎，融合视频内容理解、画质指标智能决策、多维度增强原子算法，实现画质的全面优化。
支持格式：主流视频格式如mp4、flv、ts、avi、mov、wmv、mkv。
使用限制：单文件大小不超过100G。"""
        try:
            result = client.call(api_name="enhance_video", video_url=video_url, scene=scene, tool_version=tool_version, resolution=resolution, resolution_limit=resolution_limit, fps=fps, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="erase_video_subtitle_pro", description="针对视频中的字幕，实现高质量的无痕擦除，最大程度的还原视频画面。\n支持格式：主流视频格式如mp4、flv、ts、avi、mov、wmv、mkv。 使用 task_id, 调用 query_task 方法获取结果")
    async def erase_video_subtitle_pro(
        video_url: str = Field(..., description="输入视频。String 类型，支持http://xxx或https://xxx格式 URL"),
        mode: Optional[str] = Field('Subtitle', description="字幕擦除模式，取值如下：Subtitle：擦除OCR检测为字幕的文本。在此模式下，系统将启用 OCR 识别，并依据检测结果进行擦除操作，仅擦除下面50%画面的字幕。 Text：擦除OCR检测为字幕及其他的文本（如人物介绍等），不包含场景文字（如宫殿门牌匾等）。"),
        output_encode_mode: Optional[str] = Field('Quality', description="输出视频编码模式，支持以下两种取值：Quality（默认值）：画质优先模式。此模式下，系统会采用较高的目标码率进行编码，以确保高画质。这通常会导致输出文件的码率显著高于源文件，文件体积也相应增大。 Size：大小优先模式。在保证一定画质的前提下，使输出码率尽量向源视频码率对齐。"),
        erase_ratio_location: Optional[List[EraseVideoSubtitleProEraseRatioLocationItem]] = Field(None, description="擦除框数组。添加擦除框后，系统仅擦除框内文本。\n子项说明：擦除框位置信息"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """针对视频中的字幕，实现高质量的无痕擦除，最大程度的还原视频画面。
支持格式：主流视频格式如mp4、flv、ts、avi、mov、wmv、mkv。"""
        try:
            result = client.call(api_name="erase_video_subtitle_pro", video_url=video_url, mode=mode, output_encode_mode=output_encode_mode, erase_ratio_location=erase_ratio_location, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    if hasattr(mcp, "register_domain_tools"):
        mcp.register_domain_tools("video", TOOL_NAMES)
