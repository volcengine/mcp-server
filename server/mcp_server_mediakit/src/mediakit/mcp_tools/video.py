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

TOOL_NAMES = ['analyze_video_highlights', 'analyze_video_storyline', 'asr_subtitles', 'enhance_video', 'enhance_video_generative', 'erase_video_subtitle', 'erase_video_subtitle_pro', 'generate_highlights_microdrama', 'generate_highlights_minigame', 'matte_greenscreen_video', 'matte_portrait_video', 'probe_video_metadata', 'segment_scenes', 'video_ocr']


def register_tools(mcp, client: MediKitClient) -> None:
    @mcp.tool(name="analyze_video_highlights", description="智能捕捉视频\"情绪波峰\"与\"关键动作\"，输出精准时间戳、高光打分、OCR 文本和画面描述等元数据，供下游进行更灵活的二次开发。\n支持短剧（Miniseries）和小游戏（Game）两种分析模型。\n使用限制：单次最多 100 个视频，累计时长不超过 300 分钟。 使用 task_id, 调用 query_task 方法获取结果")
    async def analyze_video_highlights(
        video_urls: List[str] = Field(..., description="待处理的视频 URL 列表，支持 1-100 个视频\n子项说明：视频 URL，支持 http:// 或 https:// 格式"),
        model: str = Field(..., description="分析场景模型，Miniseries（短剧）或 Game（小游戏）"),
        mode: str = Field(..., description="高光提取模式。固定组合为：model=Miniseries 时 mode 只能传 StorylineCuts；model=Game 时 mode 只能传 HighlightExtract"),
        minigame_info: Optional[Dict[str, Any]] = Field(None, description="小游戏描述信息，当 model=Game 时可选填，可辅助模型更精准识别高光内容"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """智能捕捉视频"情绪波峰"与"关键动作"，输出精准时间戳、高光打分、OCR 文本和画面描述等元数据，供下游进行更灵活的二次开发。
支持短剧（Miniseries）和小游戏（Game）两种分析模型。
使用限制：单次最多 100 个视频，累计时长不超过 300 分钟。"""
        try:
            result = client.call(api_name="analyze_video_highlights", video_urls=video_urls, model=model, mode=mode, minigame_info=minigame_info, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="analyze_video_storyline", description="智能解析影视剧内容，生成结构化剧情线，供智能剪辑、内容检索与互动播放等场景使用。\n基于大模型视频理解能力，对输入的单个或多个长视频（如电影、电视剧）进行分析，提取并组织成一份完整的故事线。\n该故事线由一系列按时间顺序排列的剧情片段（Clips）和基于片段聚合的高光故事线（Highlights）组成。\n使用限制：单次最多 30 个视频，单个视频时长不超过 2.5 小时。 使用 task_id, 调用 query_task 方法获取结果")
    async def analyze_video_storyline(
        video_urls: List[str] = Field(..., description="待处理的视频 URL 列表，支持 HTTP/HTTPS 公网可访问链接，最多 30 个视频\n子项说明：视频 URL，支持 http:// 或 https:// 格式"),
        enable_snapshot: Optional[bool] = Field(False, description="是否为每个剧情片段生成关键帧快照。默认为 false。开启后，结果中将包含 clip_snapshot_url 字段"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """智能解析影视剧内容，生成结构化剧情线，供智能剪辑、内容检索与互动播放等场景使用。
基于大模型视频理解能力，对输入的单个或多个长视频（如电影、电视剧）进行分析，提取并组织成一份完整的故事线。
该故事线由一系列按时间顺序排列的剧情片段（Clips）和基于片段聚合的高光故事线（Highlights）组成。
使用限制：单次最多 30 个视频，单个视频时长不超过 2.5 小时。"""
        try:
            result = client.call(api_name="analyze_video_storyline", video_urls=video_urls, enable_snapshot=enable_snapshot, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="asr_subtitles", description="对输入视频或音频进行语音识别，输出带时间戳的字幕片段。\n支持格式：主流音视频格式（如mp4、mov、mp3、m4a、wav等）。\n输入：video_url和audio_url二选一。 使用 task_id, 调用 query_task 方法获取结果")
    async def asr_subtitles(
        video_url: Optional[str] = Field(None, description="输入视频 Url（需公网可访问），与audio_url二选一，都存在时优先取video_url"),
        audio_url: Optional[str] = Field(None, description="输入音频 Url（需公网可访问），与video_url二选一，不能都为空"),
        content_type: Optional[str] = Field(None, description="识别类型，默认值为空，算法会自动探测类型，speech: 对话，singing: 歌唱"),
        language: Optional[str] = Field(None, description="识别提示语言 ID (默认值为空，算法会自动探测语种）\n分类：简体中文，ID：cmn-Hans-CN\n分类：英语，ID：eng-US\n"),
        enable_speaker_info: Optional[bool] = Field(False, description="是否开启说话人识别"),
        enable_confidence: Optional[bool] = Field(False, description="是否返回置信度"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """对输入视频或音频进行语音识别，输出带时间戳的字幕片段。
支持格式：主流音视频格式（如mp4、mov、mp3、m4a、wav等）。
输入：video_url和audio_url二选一。"""
        try:
            result = client.call(api_name="asr_subtitles", video_url=video_url, audio_url=audio_url, content_type=content_type, language=language, enable_speaker_info=enable_speaker_info, enable_confidence=enable_confidence, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="enhance_video", description="画质增强：针对 AIGC / UGC / 短剧 / 教育 / 游戏 / 老片修复等场景，提供画质提升 + 超分增强一站式解决方案。依托 AI MediaKit 智能媒体处理引擎，融合视频内容理解、画质指标智能决策、多维度增强原子算法，实现画质的全面优化。\n支持格式：主流视频格式如mp4、flv、ts、avi、mov、wmv、mkv。\n使用限制：单文件大小不超过100G。 使用 task_id, 调用 query_task 方法获取结果")
    async def enhance_video(
        video_url: str = Field(..., description="输入视频。String 类型，支持http://xxx或https://xxx格式 URL"),
        scene: Optional[str] = Field('common', description="场景化模板类型。用于选择一个针对特定业务场景的预设画质增强模板。支持的取值如下：common（默认值）: 通用模板；ugc: UGC 短视频；short_series: 短剧；aigc: AIGC 内容；old_film: 老片修复"),
        tool_version: Optional[str] = Field('standard', description="工具版本，标准版:standard，专业版：professional，默认为标准版"),
        resolution: Optional[str] = Field(None, description="目标分辨率。支持的取值如下所示。配置此参数后，不可同时配置resolution_limit字段"),
        resolution_limit: Optional[int] = Field(None, description="指定输出视频的短边像素值，取值范围为 [128, 2160]。设置后，系统将锁定视频的短边像素值为设定值，并在保持原视频宽高比的前提下，等比缩放至该限制值。示例：若原视频为 640x480 (4:3)，设置 resolution_limit 为 720，则输出视频的短边将提升至 720，宽度等比缩放至 960。配置此参数后，不可同时配置resolution字段"),
        bitrate_level: Optional[str] = Field('medium', description="码率档位。输出视频的目标平均码率。该参数将决定视频的视觉质量和最终的文件体积。参数取值：高码率、中码率（推荐码率）、低码率。非必填，默认为中码率。"),
        fps: Optional[float] = Field(None, description="目标帧率，单位为 fps。取值范围为 [15, 120]。"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """画质增强：针对 AIGC / UGC / 短剧 / 教育 / 游戏 / 老片修复等场景，提供画质提升 + 超分增强一站式解决方案。依托 AI MediaKit 智能媒体处理引擎，融合视频内容理解、画质指标智能决策、多维度增强原子算法，实现画质的全面优化。
支持格式：主流视频格式如mp4、flv、ts、avi、mov、wmv、mkv。
使用限制：单文件大小不超过100G。"""
        try:
            result = client.call(api_name="enhance_video", video_url=video_url, scene=scene, tool_version=tool_version, resolution=resolution, resolution_limit=resolution_limit, bitrate_level=bitrate_level, fps=fps, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="enhance_video_generative", description="生成式视频增强修复（generative_video_restoration）是基于扩散大模型（Diffusion-based Large Model）的生成式视频修复技术。不仅可以还原被破坏的像素，更借助大规模预训练积累的丰富视觉先验，主动补全细节、理解语义，生成真实、自然、高保真的视频内容。 使用 task_id, 调用 query_task 方法获取结果")
    async def enhance_video_generative(
        video_url: str = Field(..., description="输入视频。String 类型，支持http://xxx或https://xxx格式 URL"),
        resolution: Optional[str] = Field('720p', description="目标分辨率。支持的取值如下所示。"),
        bitrate_level: Optional[str] = Field('medium', description="码率档位。输出视频的目标平均码率。该参数将决定视频的视觉质量和最终的文件体积。参数取值：高码率、中码率（推荐码率）、低码率。非必填，默认为中码率。"),
        fps: Optional[float] = Field(None, description="目标帧率，单位为 fps。若未指定 fps 参数，输出视频将保持与原始片源一致的帧率。取值范围为 [15, 120]。建议不超过原片的 4 倍。"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """生成式视频增强修复（generative_video_restoration）是基于扩散大模型（Diffusion-based Large Model）的生成式视频修复技术。不仅可以还原被破坏的像素，更借助大规模预训练积累的丰富视觉先验，主动补全细节、理解语义，生成真实、自然、高保真的视频内容。"""
        try:
            result = client.call(api_name="enhance_video_generative", video_url=video_url, resolution=resolution, bitrate_level=bitrate_level, fps=fps, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="erase_video_subtitle", description="智能检测并擦除视频画面中已有的硬字幕，保留原始背景。\n支持格式：主流视频格式如mp4、flv、ts、avi、mov、wmv、mkv。 使用 task_id, 调用 query_task 方法获取结果")
    async def erase_video_subtitle(
        video_url: str = Field(..., description="输入视频。String 类型，支持http://xxx或https://xxx格式 Url"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """智能检测并擦除视频画面中已有的硬字幕，保留原始背景。
支持格式：主流视频格式如mp4、flv、ts、avi、mov、wmv、mkv。"""
        try:
            result = client.call(api_name="erase_video_subtitle", video_url=video_url, callback_args=callback_args, client_token=client_token)
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

    @mcp.tool(name="generate_highlights_microdrama", description="深度理解短剧角色、剧情与故事线，自动提取高光片段并混剪成投流视频。\n支持故事线混剪模式（StorylineCuts），可选\"短剧三要素\"视觉模板，输出高光集锦、单集预告等。\n支持输出详细分镜信息（storyboard）。\n使用限制：单次最多 100 个视频，累计时长不超过 300 分钟。 使用 task_id, 调用 query_task 方法获取结果")
    async def generate_highlights_microdrama(
        video_urls: List[str] = Field(..., description="待处理的短剧原片视频 URL 列表，支持 1-100 个视频\n子项说明：视频 URL，支持 http:// 或 https:// 格式"),
        mode: Optional[str] = Field('StorylineCuts', description="短剧高光智剪模式，本期固定为 StorylineCuts（故事线混剪模式）"),
        enable_generate_video: Optional[bool] = Field(True, description="是否生成混剪成片视频。true（默认）= 同时输出混剪视频与分镜信息；false = 仅输出高光分镜信息（clips/storyboard），不生成混剪视频，此时底层请求不会携带 Edit 字段，且传入的 edit_param 将被忽略。"),
        enable_return_poster: Optional[bool] = Field(False, description="是否在结果中返回混剪视频封面图 URL。false（默认）= 不返回封面图；true = 若底层存在封面则返回 poster_url。"),
        edit_param: Optional[Dict[str, Any]] = Field(None, description="成片剪辑参数配置"),
        highlight_cuts_param: Optional[Dict[str, Any]] = Field(None, description="高光混剪参数配置"),
        opening_hook_param: Optional[Dict[str, Any]] = Field(None, description="精彩前置功能参数配置（可选）"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """深度理解短剧角色、剧情与故事线，自动提取高光片段并混剪成投流视频。
支持故事线混剪模式（StorylineCuts），可选"短剧三要素"视觉模板，输出高光集锦、单集预告等。
支持输出详细分镜信息（storyboard）。
使用限制：单次最多 100 个视频，累计时长不超过 300 分钟。"""
        try:
            result = client.call(api_name="generate_highlights_microdrama", video_urls=video_urls, mode=mode, enable_generate_video=enable_generate_video, enable_return_poster=enable_return_poster, edit_param=edit_param, highlight_cuts_param=highlight_cuts_param, opening_hook_param=opening_hook_param, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="generate_highlights_minigame", description="识别小游戏录屏视频中的核心玩法与高光事件（如连击、通关、极限操作等），\n快速生成用于买量的视频素材。支持提供游戏名称、玩法描述、高光定义以辅助模型更精准识别。\n使用限制：本期仅支持单视频输入。 使用 task_id, 调用 query_task 方法获取结果")
    async def generate_highlights_minigame(
        video_urls: List[str] = Field(..., description="待处理的小游戏视频 URL 列表，本期仅支持单视频输入\n子项说明：视频 URL，支持 http:// 或 https:// 格式"),
        mode: Optional[str] = Field('HighlightExtract', description="高光提取模式，本期支持 HighlightExtract"),
        enable_generate_video: Optional[bool] = Field(True, description="是否生成混剪成片视频。true（默认）= 同时输出混剪视频（Edit.Mode=HighlightClips）与高光片段信息；false = 仅输出高光片段信息（clips），底层请求不携带 Edit 字段，也不会生成任何混剪视频。"),
        minigame_info: Optional[Dict[str, Any]] = Field(None, description="小游戏描述信息，建议填写以辅助模型更精准识别高光内容"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """识别小游戏录屏视频中的核心玩法与高光事件（如连击、通关、极限操作等），
快速生成用于买量的视频素材。支持提供游戏名称、玩法描述、高光定义以辅助模型更精准识别。
使用限制：本期仅支持单视频输入。"""
        try:
            result = client.call(api_name="generate_highlights_minigame", video_urls=video_urls, mode=mode, enable_generate_video=enable_generate_video, minigame_info=minigame_info, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="matte_greenscreen_video", description="对以绿幕或纯色为背景的视频进行抠图，自动识别主体（人物、物品、动物等），同时移除背景，生成背景透明的视频。\n输出视频格式为 WEBM（默认）或 MOV，分辨率与原片对齐。\n支持的格式：主流视频格式如 mp4、flv、ts、avi、mov、mkv、wmv。 使用 task_id, 调用 query_task 方法获取结果")
    async def matte_greenscreen_video(
        video_url: str = Field(..., description="输入视频 Url。支持 http://xxx 或 https://xxx 格式。"),
        format: Optional[str] = Field('WEBM', description="输出视频格式：MOV / WEBM（默认）"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """对以绿幕或纯色为背景的视频进行抠图，自动识别主体（人物、物品、动物等），同时移除背景，生成背景透明的视频。
输出视频格式为 WEBM（默认）或 MOV，分辨率与原片对齐。
支持的格式：主流视频格式如 mp4、flv、ts、avi、mov、mkv、wmv。"""
        try:
            result = client.call(api_name="matte_greenscreen_video", video_url=video_url, format=format, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="matte_portrait_video", description="自动识别人物主体，同时移除背景，生成背景透明的视频，适用于背景替换等场景。\n输出格式为 WEBM（默认）或 MOV，分辨率与原片对齐。\n支持的格式：主流视频格式如 mp4、flv、ts、avi、mov、mkv、wmv。 使用 task_id, 调用 query_task 方法获取结果")
    async def matte_portrait_video(
        video_url: str = Field(..., description="输入视频 Url。支持 http://xxx 或 https://xxx 格式。"),
        format: Optional[str] = Field('WEBM', description="输出视频格式：MOV / WEBM（默认）"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """自动识别人物主体，同时移除背景，生成背景透明的视频，适用于背景替换等场景。
输出格式为 WEBM（默认）或 MOV，分辨率与原片对齐。
支持的格式：主流视频格式如 mp4、flv、ts、avi、mov、mkv、wmv。"""
        try:
            result = client.call(api_name="matte_portrait_video", video_url=video_url, format=format, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="probe_video_metadata", description="对输入视频 URL 进行探测，输出标准化媒资元信息，覆盖容器层（format_meta）、视频流层（video_stream_meta）与音频流层（audio_stream_meta）。\n字段分类参考 ffprobe，并对 VOD 原始返回做精简与统一，便于上层做分辨率/帧率/码率/编码等策略判断。\n使用限制：仅支持公网 HTTP/HTTPS URL；输入视频分辨率最高支持 4K。 使用 task_id, 调用 query_task 方法获取结果")
    async def probe_video_metadata(
        video_url: str = Field(..., description="待探测的视频公网 HTTP/HTTPS URL。"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """对输入视频 URL 进行探测，输出标准化媒资元信息，覆盖容器层（format_meta）、视频流层（video_stream_meta）与音频流层（audio_stream_meta）。
字段分类参考 ffprobe，并对 VOD 原始返回做精简与统一，便于上层做分辨率/帧率/码率/编码等策略判断。
使用限制：仅支持公网 HTTP/HTTPS URL；输入视频分辨率最高支持 4K。"""
        try:
            result = client.call(api_name="probe_video_metadata", video_url=video_url, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="segment_scenes", description="依据视频转场与画面变化自动切分场景，输出切片时间轴和（可选）切片文件。\n支持格式：MP4、FLV、ASF、RM、RMVB、MPEG、MOV、AVI、MPEGTS、M4S、WMV、3GP、TS、MPG、WEBM、MKV、WM、MPE、VOB、DAT、MP4V、M4V、F4V、MXF、QT 等主流视频格式。\n使用限制：单个视频时长不超过 2 小时。 使用 task_id, 调用 query_task 方法获取结果")
    async def segment_scenes(
        video_url: str = Field(..., description="待处理视频 Url，必须是公网可直接访问的 HTTP/HTTPS 链接"),
        enable_clip_fade: Optional[bool] = Field(False, description="是否将检测到的淡入/淡出片段作为独立切片输出"),
        segment_threshold: Optional[float] = Field(None, description="场景切分敏感度阈值，范围 [0, 100)，100 不可取。数值越低切得越细，参考经验值10"),
        min_duration: Optional[float] = Field(None, description="单个切片最小时长（秒），参考经验值3，应小于等于max_duration"),
        max_duration: Optional[float] = Field(None, description="单个切片最大时长（秒），参考经验值30，应大于等于min_duration"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """依据视频转场与画面变化自动切分场景，输出切片时间轴和（可选）切片文件。
支持格式：MP4、FLV、ASF、RM、RMVB、MPEG、MOV、AVI、MPEGTS、M4S、WMV、3GP、TS、MPG、WEBM、MKV、WM、MPE、VOB、DAT、MP4V、M4V、F4V、MXF、QT 等主流视频格式。
使用限制：单个视频时长不超过 2 小时。"""
        try:
            result = client.call(api_name="segment_scenes", video_url=video_url, enable_clip_fade=enable_clip_fade, segment_threshold=segment_threshold, min_duration=min_duration, max_duration=max_duration, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="video_ocr", description="识别视频画面中的字幕/文字内容，输出带时间戳的字幕片段。\n支持格式：主流视频格式如 mp4、flv、ts、avi、mov、wmv、mkv。 使用 task_id, 调用 query_task 方法获取结果")
    async def video_ocr(
        video_url: str = Field(..., description="输入视频 Url（需公网可访问）"),
        mode: Optional[str] = Field('Subtitle', description="工作模式（Subtitle: 识别字幕文本；Detailed: 识别更详细文本信息）"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """识别视频画面中的字幕/文字内容，输出带时间戳的字幕片段。
支持格式：主流视频格式如 mp4、flv、ts、avi、mov、wmv、mkv。"""
        try:
            result = client.call(api_name="video_ocr", video_url=video_url, mode=mode, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    if hasattr(mcp, "register_domain_tools"):
        mcp.register_domain_tools("video", TOOL_NAMES)
