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

class AddSubtitleToVideoSubtitlesItem(TypedDict):
    subtitle_text: Required[str]
    start_time: Required[float]
    end_time: Required[float]

class ImageToVideoImagesItem(TypedDict):
    image_url: Required[str]
    duration: NotRequired[float]
    animation_type: NotRequired[str]
    animation_in: NotRequired[float]
    animation_out: NotRequired[float]

TOOL_NAMES = ['add_image_to_video', 'add_subtitle_to_video', 'adjust_audio_speed', 'adjust_video_speed', 'adjust_video_volume', 'apply_video_filter', 'concat_audio', 'concat_video', 'extract_audio', 'fade_audio', 'fade_video_audio', 'flip_video', 'image_to_video', 'mix_audio', 'mux_audio_video', 'trim_audio', 'trim_video']


def register_tools(mcp, client: MediKitClient) -> None:
    @mcp.tool(name="add_image_to_video", description="视频加图片，可用作加图片水印。 使用 task_id, 调用 query_task 方法获取结果")
    async def add_image_to_video(
        video_url: str = Field(..., description="输入视频。String 类型，支持http://xxx或https://xxx格式 URL"),
        sub_image_url: str = Field(..., description="图片URL。支持http://xxx或https://xxx格式 URL"),
        sub_image_height: Optional[str] = Field('5%', description="图片的高度，字符串类型，支持具体像素值（如 '100'）或百分比（如 '20%'，相对于视频高度）。"),
        sub_image_width: Optional[str] = Field('10%', description="图片的宽度，字符串类型，支持具体像素值（如 '100'）或百分比（如 '20%'，相对于视频高度）。"),
        sub_image_pos_x: Optional[str] = Field('85%', description="图片在水平方向（X 轴）的位置，以视频左上角为原点，字符串类型，支持具体像素值（如 '100'）或百分比（如 '20%'）。例如值为 '0' 时，表示处于最左侧。"),
        sub_image_pos_y: Optional[str] = Field('90%', description="图片在垂直方向（Y 轴）的位置，以视频左上角为原点，字符串类型，支持具体像素值（如 '100'）或百分比（如 '20%'）。例如值为 '0' 时，表示处于最上侧。"),
        start_time: Optional[float] = Field(None, description="图片的开始时间，单位：秒。不传默认同视频开始时间"),
        end_time: Optional[float] = Field(None, description="图片的结束时间，单位：秒。注意：如果设置的开始/结束时间超出原始视频时长，输出视频长度将以该结束时间为准，超出部分以黑屏形式延续。不传默认同视频结束时间"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """视频加图片，可用作加图片水印。"""
        try:
            result = client.call(api_name="add_image_to_video", video_url=video_url, sub_image_url=sub_image_url, sub_image_height=sub_image_height, sub_image_width=sub_image_width, sub_image_pos_x=sub_image_pos_x, sub_image_pos_y=sub_image_pos_y, start_time=start_time, end_time=end_time, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="add_subtitle_to_video", description="将字幕文件或文本内容，以指定样式压制到视频画面中，生成带内嵌字幕的新视频。 使用 task_id, 调用 query_task 方法获取结果")
    async def add_subtitle_to_video(
        video_url: str = Field(..., description="输入视频。String 类型，支持http://xxx或https://xxx格式 URL"),
        subtitle_url: Optional[str] = Field(None, description="字幕文件 URL、filename。常见的字幕文件为 SRT、VTT、ASS 等格式。"),
        subtitles: Optional[List[AddSubtitleToVideoSubtitlesItem]] = Field(None, description="字幕列表，Array<object>类型。"),
        subtitle_pos_preset: Optional[str] = Field('bottom_center', description="预设字幕位置。底部居中（默认常用） bottom_center；顶部居中 top_center；画面正中央 center；偏下三分之一处 lower_third"),
        subtitle_font_size: Optional[int] = Field(50, description="字幕的字体大小，单位：像素。"),
        subtitle_font_color: Optional[str] = Field('#FFFFFFFF', description="字幕的字体颜色，RGBA 格式。默认#FFFFFFFF"),
        subtitle_font_type: Optional[str] = Field('sy_black', description="字幕的字体 ID。 思源黑体：sy_black （经典无衬线黑体，端正百搭，正文首选） 庞门正道标题体：pm_zhengdao （粗壮有力，硬汉气场，大标题/封面神器） 阿里巴巴普惠体：ali_puhui （现代感极强，结构饱满，屏幕阅读体验极佳） 站酷快乐体：zhanku_kuaile （圆润活泼，带手写感，适合轻松搞笑的 Vlog 氛围）"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """将字幕文件或文本内容，以指定样式压制到视频画面中，生成带内嵌字幕的新视频。"""
        try:
            result = client.call(api_name="add_subtitle_to_video", video_url=video_url, subtitle_url=subtitle_url, subtitles=subtitles, subtitle_pos_preset=subtitle_pos_preset, subtitle_font_size=subtitle_font_size, subtitle_font_color=subtitle_font_color, subtitle_font_type=subtitle_font_type, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="adjust_video_speed", description="调整视频的播放倍速，实现快放或慢放效果。 使用 task_id, 调用 query_task 方法获取结果")
    async def adjust_video_speed(
        video_url: str = Field(..., description="输入视频。String 类型，支持http://xxx或https://xxx格式 URL"),
        speed: Optional[float] = Field(1, description="调整速度的倍数，Float类型，取值范围为0.1～4。"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """调整视频的播放倍速，实现快放或慢放效果。"""
        try:
            result = client.call(api_name="adjust_video_speed", video_url=video_url, speed=speed, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="concat_audio", description="拼接多个音频片段。 使用 task_id, 调用 query_task 方法获取结果")
    async def concat_audio(
        audio_urls: List[str] = Field(..., description="待拼接的音频列表，Array<string>类型。最少传入1个，最多传入100个\n子项说明：待拼接的输入音频。String 类型，支持http://xxx或https://xxx格式 URL"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """拼接多个音频片段。"""
        try:
            result = client.call(api_name="concat_audio", audio_urls=audio_urls, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="concat_video", description="拼接多个视频片段，支持添加转场效果。 使用 task_id, 调用 query_task 方法获取结果")
    async def concat_video(
        video_urls: List[str] = Field(..., description="待拼接的视频列表，Array<string>类型。最少传入1个，最多传入100个\n子项说明：待拼接的输入视频。String 类型，支持http://xxx或https://xxx格式 URL"),
        transitions: Optional[List[str]] = Field(None, description="转场效果 ID，Array<string> 类型。如果不提供，则没有转场。当视频数量超过转场数量 2 个及以上时，系统将自动循环使用转场。例如有 10 个视频，2 种转场效果，那么在 9 处拼接点上，这 2 种转场效果将被依次循环使用。\n子项说明：转场效果 ID\n分类：交替出场，ID：1182359\n分类：旋转放大，ID：1182360\n分类：泛开，ID：1182358\n分类：六角形，ID：1182365\n分类：故障转换，ID：1182367\n分类：飞眼，ID：1182368\n分类：梦幻放大，ID：1182369\n分类：开门展现，ID：1182370\n分类：立方转换，ID：1182373\n分类：透镜变换，ID：1182374\n分类：晚霞转场，ID：1182375\n分类：圆形交替，ID：1182378"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """拼接多个视频片段，支持添加转场效果。"""
        try:
            result = client.call(api_name="concat_video", video_urls=video_urls, transitions=transitions, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="extract_audio", description="将视频文件中的音频流分离并保存为独立的音频文件。 使用 task_id, 调用 query_task 方法获取结果")
    async def extract_audio(
        video_url: str = Field(..., description="输入视频，String 类型，支持http://xxx或https://xxx格式 URL"),
        format: Optional[str] = Field('m4a', description="输出音频的格式，支持 mp3、m4a 格式。 默认m4a"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """将视频文件中的音频流分离并保存为独立的音频文件。"""
        try:
            result = client.call(api_name="extract_audio", video_url=video_url, format=format, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="flip_video", description="对视频画面进行上下或左右镜像翻转。 使用 task_id, 调用 query_task 方法获取结果")
    async def flip_video(
        video_url: str = Field(..., description="输入视频。String 类型，支持http://xxx或https://xxx格式 URL"),
        is_flip_vertical: Optional[bool] = Field(False, description="是否进行垂直翻转。Boolean 类型，默认值为 false， 表示不翻转。"),
        is_flip_horizontal: Optional[bool] = Field(False, description="是否进行水平翻转。Boolean 类型，默认值为 false， 表示不翻转。"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """对视频画面进行上下或左右镜像翻转。"""
        try:
            result = client.call(api_name="flip_video", video_url=video_url, is_flip_vertical=is_flip_vertical, is_flip_horizontal=is_flip_horizontal, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="image_to_video", description="多张图片生成动画视频。 使用 task_id, 调用 query_task 方法获取结果")
    async def image_to_video(
        images: List[ImageToVideoImagesItem] = Field(..., description="待合成的图片列表，Array<Image>类型。最少传入1个，最多传入100个\n子项说明：待合成的图片。Image类型"),
        transitions: Optional[List[str]] = Field(None, description="转场效果 ID，Array<string> 类型。如果不提供，则没有转场。当视频数量超过转场数量 2 个及以上时，系统将自动循环使用转场。例如有 10 个视频，2 种转场效果，那么在 9 处拼接点上，这 2 种转场效果将被依次循环使用。\n子项说明：转场效果 ID\n分类：交替出场，ID：1182359\n分类：旋转放大，ID：1182360\n分类：泛开，ID：1182358\n分类：六角形，ID：1182365\n分类：故障转换，ID：1182367\n分类：飞眼，ID：1182368\n分类：梦幻放大，ID：1182369\n分类：开门展现，ID：1182370\n分类：立方转换，ID：1182373\n分类：透镜变换，ID：1182374\n分类：晚霞转场，ID：1182375\n分类：圆形交替，ID：1182378"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """多张图片生成动画视频。"""
        try:
            result = client.call(api_name="image_to_video", images=images, transitions=transitions, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="mux_audio_video", description="音视频合成。 使用 task_id, 调用 query_task 方法获取结果")
    async def mux_audio_video(
        video_url: str = Field(..., description="输入视频。String 类型，支持http://xxx或https://xxx格式 URL"),
        audio_url: str = Field(..., description="输入音频。String 类型，支持http://xxx或https://xxx格式 URL"),
        is_audio_reserve: Optional[bool] = Field(True, description="Boolean 类型，是否保留原视频流中的音频。默认值 true：保留。false：不保留。"),
        is_video_audio_sync: Optional[bool] = Field(False, description="Boolean 类型，是否对齐音频和视频时长。 true：通过 output_sync 配置，对齐音频和视频时长。 false（默认值）：保持原样输出，不做音视频对齐。最终合成的视频时长，以较长的流为准。"),
        sync_mode: Optional[str] = Field('video', description="String 类型，设置 is_video_audio_sync 为 true 时生效；当音频和视频时长不相等时，可指定对齐基准，可选项：video、audio。 video：【默认值】以视频的时长为准。 audio：以音频的时长为准。"),
        sync_method: Optional[str] = Field('trim', description="String 类型，设置 is_video_audio_sync 为 true 时生效；指定对齐方式，支持通过裁剪或加速的方式，对齐音频和视频的时长。可选项：speed、trim。 speed：通过加快音频或视频的速度，对齐音频和视频的时长。 trim：【默认值】通过裁剪音频或视频，对齐音频和视频的时长。从头开始计算并裁剪。"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """音视频合成。"""
        try:
            result = client.call(api_name="mux_audio_video", video_url=video_url, audio_url=audio_url, is_audio_reserve=is_audio_reserve, is_video_audio_sync=is_video_audio_sync, sync_mode=sync_mode, sync_method=sync_method, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="trim_audio", description="按起止时间点（秒级）裁剪音频，生成新片段。 使用 task_id, 调用 query_task 方法获取结果")
    async def trim_audio(
        audio_url: str = Field(..., description="输入纯音频。String 类型，支持http://xxx或https://xxx格式 URL"),
        start_time: Optional[float] = Field(0, description="裁剪开始时间，默认为 0， 表示从头开始裁剪。支持设置为 2 位小数，单位：秒。"),
        end_time: Optional[float] = Field(None, description="裁剪结束时间，默认为片源结尾。支持设置为 2 位小数，单位：秒。"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """按起止时间点（秒级）裁剪音频，生成新片段。"""
        try:
            result = client.call(api_name="trim_audio", audio_url=audio_url, start_time=start_time, end_time=end_time, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="trim_video", description="按起止时间点裁剪视频，生成新片段。 使用 task_id, 调用 query_task 方法获取结果")
    async def trim_video(
        video_url: str = Field(..., description="输入视频。String 类型，支持http://xxx或https://xxx格式 URL"),
        start_time: Optional[float] = Field(0, description="裁剪开始时间，默认为 0， 表示从头开始裁剪。支持设置为 2 位小数，单位：秒。"),
        end_time: Optional[float] = Field(None, description="裁剪结束时间，默认为片源结尾。支持设置为 2 位小数，单位：秒。"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """按起止时间点裁剪视频，生成新片段。"""
        try:
            result = client.call(api_name="trim_video", video_url=video_url, start_time=start_time, end_time=end_time, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="adjust_audio_speed", description="调整音频的播放倍速，实现快放或慢放效果。 使用 task_id, 调用 query_task 方法获取结果")
    async def adjust_audio_speed(
        audio_url: str = Field(..., description="输入音频。支持http://xxx或https://xxx格式 Url，支持 mp3、m4a、wav 等格式"),
        speed: Optional[float] = Field(1, description="调整速度的倍数，Float类型，取值范围为0.1～4。0.1=放慢至原速的 0.1 倍，1=原速，4=加速至原速的 4 倍。"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """调整音频的播放倍速，实现快放或慢放效果。"""
        try:
            result = client.call(api_name="adjust_audio_speed", audio_url=audio_url, speed=speed, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="adjust_video_volume", description="调整视频音量大小，支持静音；输出 mp4，分辨率与原片一致。 使用 task_id, 调用 query_task 方法获取结果")
    async def adjust_video_volume(
        video_url: str = Field(..., description="输入视频。支持http://xxx或https://xxx格式 URL，支持 mp4、mov、flv、ts、avi、wmv、mkv 等格式，最高 4K"),
        volume: Optional[float] = Field(1, description="音量倍数。Float 类型，取值范围 0~4。0=静音，1=原音量，4=放大 4 倍。"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """调整视频音量大小，支持静音；输出 mp4，分辨率与原片一致。"""
        try:
            result = client.call(api_name="adjust_video_volume", video_url=video_url, volume=volume, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="apply_video_filter", description="为视频添加指定滤镜效果，输出mp4，分辨率与原片一致。 使用 task_id, 调用 query_task 方法获取结果")
    async def apply_video_filter(
        video_url: str = Field(..., description="输入视频。支持http://xxx或https://xxx格式 URL，支持 mp4、mov、flv、ts、avi、wmv、mkv 等格式，最高 4K"),
        filter_style: Optional[str] = Field('spring', description="滤镜风格。根据用户想要的视频画面效果选择：\n- spring：春日滤镜\n- sunset：晚霞滤镜\n- vivid：鲜亮滤镜\n- fair_skin：白皙滤镜\n- food：食物滤镜\n"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """为视频添加指定滤镜效果，输出mp4，分辨率与原片一致。"""
        try:
            result = client.call(api_name="apply_video_filter", video_url=video_url, filter_style=filter_style, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="fade_audio", description="对输入音频实现淡入淡出效果，输出 mp3。 使用 task_id, 调用 query_task 方法获取结果")
    async def fade_audio(
        audio_url: str = Field(..., description="输入音频。支持http://xxx或https://xxx格式 URL，支持 mp3、m4a、wav、flac 等格式"),
        fade_in_duration: Optional[float] = Field(1, description="声音淡入时长。单位：秒，可传小数（最多3位小数）。0 表示不淡入。"),
        fade_out_duration: Optional[float] = Field(1, description="声音淡出时长。单位：秒，可传小数（最多3位小数）。0 表示不淡出。"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """对输入音频实现淡入淡出效果，输出 mp3。"""
        try:
            result = client.call(api_name="fade_audio", audio_url=audio_url, fade_in_duration=fade_in_duration, fade_out_duration=fade_out_duration, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="fade_video_audio", description="对输入视频的声轨实现淡入淡出效果。\n输出 mp4，分辨率与原片一致。 使用 task_id, 调用 query_task 方法获取结果")
    async def fade_video_audio(
        video_url: str = Field(..., description="输入视频。支持http://xxx或https://xxx格式 URL，支持 mp4、mov、flv、ts、avi、wmv、mkv 等格式，最高 4K"),
        fade_in_duration: Optional[float] = Field(1, description="声音淡入时长。单位：秒，可传小数（最多3位小数）。0 表示不淡入。"),
        fade_out_duration: Optional[float] = Field(1, description="声音淡出时长。单位：秒，可传小数（最多3位小数）。0 表示不淡出。"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """对输入视频的声轨实现淡入淡出效果。
输出 mp4，分辨率与原片一致。"""
        try:
            result = client.call(api_name="fade_video_audio", video_url=video_url, fade_in_duration=fade_in_duration, fade_out_duration=fade_out_duration, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="mix_audio", description="将多个音频文件（如背景音乐、音效、人声）进行混音，生成一个新的音频文件。\n处理耗时：处理耗时与视频时长正相关。视频时长越长，处理耗时越长。平均 RTF（处理耗时/原片时长）为 1。\n输出音频的时长以最长的音频为准。\n输出视频格式：mp3 使用 task_id, 调用 query_task 方法获取结果")
    async def mix_audio(
        audio_urls: List[str] = Field(..., description="待混合的音频列表，Array<string>类型。最少传入1个，最多传入100个。\n子项说明：待混合的输入音频。支持http://xxx或https://xxx格式 URL，支持 mp3、wav、flac 等格式"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """将多个音频文件（如背景音乐、音效、人声）进行混音，生成一个新的音频文件。
处理耗时：处理耗时与视频时长正相关。视频时长越长，处理耗时越长。平均 RTF（处理耗时/原片时长）为 1。
输出音频的时长以最长的音频为准。
输出视频格式：mp3"""
        try:
            result = client.call(api_name="mix_audio", audio_urls=audio_urls, callback_args=callback_args, client_token=client_token)
            return async_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    if hasattr(mcp, "register_domain_tools"):
        mcp.register_domain_tools("editing", TOOL_NAMES)
