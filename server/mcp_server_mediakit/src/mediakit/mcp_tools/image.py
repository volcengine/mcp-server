from __future__ import annotations

from typing import Annotated, Any
from pydantic import Field, WithJsonSchema
from base.context import get_client
from ..utils.response import (
    async_task_response,
    error_response,
    sync_result_response,
)

TOOL_NAMES = ['add_image_watermark', 'adjust_image_color', 'compress_image', 'crop_image', 'enhance_image', 'erase_image', 'evaluate_image_quality', 'face_blur_image', 'flip_image', 'gaussian_blur_image', 'image_ocr', 'invert_image', 'mosaic_image', 'probe_image_metadata', 'remove_image_background', 'resize_image', 'rotate_image', 'round_corner_image', 'sharpen_image', 'slim_image', 'smart_crop_image']
DOMAIN = 'image'


def _structured_error(exc: Exception) -> object:
    response = getattr(exc, "response", None)
    if response is not None:
        try:
            return response.json()
        except Exception:
            pass
    return {"message": str(exc)}


def register_tools(mcp) -> None:
    @mcp.tool(name='add_image_watermark', description='为图片添加图文明水印，适用于版权标识与素材分发防盗链场景。')
    async def add_image_watermark(
        image_url: Annotated[str, WithJsonSchema({'description': '待处理的图片 URL，支持公网 HTTP/HTTPS URL、对象存储 tos:// 两种输入协议；仅支持处理静图；建议单张图片不超过 35 MB；支持 .png、.jpg、.jpeg、.webp 等主流图像格式；输入图片宽和高均不得超过 10000 像素。', 'format': 'media-to-binary', 'type': 'string'})] = Field(...),
        enable_tile: Annotated[bool | None, WithJsonSchema({'default': False, 'description': '默认 false。开启后水印将以固定的间距重复平铺在整个图片上；对于文字水印，会额外应用逆时针 30 度的旋转；对于图片水印，仅进行平铺，不应用旋转。', 'type': 'boolean'})] = Field(None, json_schema_extra={'default': False}),
        output_format: Annotated[str | None, WithJsonSchema({'default': 'original', 'description': '输出图片格式可为 original、png、jpeg、webp；original 表示保持与原图一致的格式；默认 original。', 'enum': ['original', 'png', 'jpeg', 'webp'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'original'}),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
        watermark_image_opacity: Annotated[int | None, WithJsonSchema({'default': 100, 'description': '图片水印透明度范围为 [0,100]；值越小越透明；默认 100。', 'maximum': 100, 'minimum': 0, 'type': 'integer'})] = Field(None, json_schema_extra={'default': 100}),
        watermark_image_url: Annotated[str | None, WithJsonSchema({'description': '图片水印的 URL，必须为公网可访问的 HTTP 或 HTTPS URL；不是无条件必填；建议不超过 5 MB；支持 .jpg、.jpeg、.webp 等常见图像格式。', 'format': 'media-to-imagex-uri', 'type': 'string'})] = Field(None),
        watermark_position: Annotated[str | None, WithJsonSchema({'default': 'bottom_right', 'description': '水印在图片上的九宫格布局位置，可为 top_left、top_center、top_right、left_center、center、right_center、bottom_left、bottom_center、bottom_right；默认 bottom_right；当使用包含 center 的值时，watermark_position_offset_x 和 watermark_position_offset_y 将不生效。', 'enum': ['top_left', 'top_right', 'bottom_left', 'bottom_right', 'left_center', 'right_center', 'top_center', 'bottom_center', 'center'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'bottom_right'}),
        watermark_position_offset_x: Annotated[int | None, WithJsonSchema({'default': 0, 'description': '水印在 watermark_position 基础上沿 X 轴的微调距离，单位为像素；默认 0；仅在 watermark_position 取值不包含 center 时生效。', 'minimum': 0, 'type': 'integer'})] = Field(None, json_schema_extra={'default': 0}),
        watermark_position_offset_y: Annotated[int | None, WithJsonSchema({'default': 0, 'description': '水印在 watermark_position 基础上沿 Y 轴的微调距离，单位为像素；默认 0；仅在 watermark_position 取值不包含 center 时生效。', 'minimum': 0, 'type': 'integer'})] = Field(None, json_schema_extra={'default': 0}),
        watermark_text: Annotated[str | None, WithJsonSchema({'description': '水印文字内容，不是无条件必填。', 'maxLength': 64, 'type': 'string'})] = Field(None),
        watermark_text_color: Annotated[str | None, WithJsonSchema({'default': '#FFFFFF', 'description': '文字颜色必须使用 #RRGGBB 六位十六进制格式；默认 #FFFFFF。', 'pattern': '^#[0-9a-fA-F]{6}$', 'type': 'string'})] = Field(None, json_schema_extra={'default': '#FFFFFF'}),
        watermark_text_font: Annotated[str | None, WithJsonSchema({'default': 'SourceHanSans-Regular.ttf', 'description': '文字字体支持思源黑体、思源宋体、站酷、方正兰亭黑等系列字体；默认 SourceHanSans-Regular.ttf（思源黑体）。', 'enum': ['SourceHanSans-Regular.ttf', 'SourceHanSans-Bold.ttf', 'SourceHanSans-ExtraLight.ttf', 'SourceHanSans-Heavy.ttf', 'SourceHanSans-Light.ttf', 'SourceHanSans-Medium.ttf', 'SourceHanSans-Normal.ttf', 'SourceHanSerifCN-Regular.ttf', 'SourceHanSerifCN-Bold.ttf', 'SourceHanSerifCN-ExtraLight.ttf', 'SourceHanSerifCN-Heavy.ttf', 'SourceHanSerifCN-Light.ttf', 'SourceHanSerifCN-SemiBold.ttf', 'zcool-heiti.ttf', 'zcool_gaoduanhei.ttf', 'zcool_kuaileti.ttf', 'zcool_huangyou.ttf', 'FZLTHK.TTF'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'SourceHanSans-Regular.ttf'}),
        watermark_text_font_size: Annotated[int | None, WithJsonSchema({'default': 30, 'description': '文字字号单位为像素；默认 30。', 'maximum': 200, 'minimum': 1, 'type': 'integer'})] = Field(None, json_schema_extra={'default': 30}),
        watermark_text_opacity: Annotated[int | None, WithJsonSchema({'default': 30, 'description': '文字水印透明度范围为 [0,100]；值越小越透明；默认 30。', 'maximum': 100, 'minimum': 0, 'type': 'integer'})] = Field(None, json_schema_extra={'default': 30}),
        watermark_type: Annotated[str | None, WithJsonSchema({'default': 'text', 'description': '水印类型可为 text 和 image；text 表示文字水印，image 表示图片水印；默认 text。', 'enum': ['text', 'image'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'text'}),
    ) -> dict:
        try:
            result = get_client().call('add_image_watermark', **{
                key: item for key, item in {'image_url': image_url, 'enable_tile': enable_tile, 'output_format': output_format, 'queue_id': queue_id, 'watermark_image_opacity': watermark_image_opacity, 'watermark_image_url': watermark_image_url, 'watermark_position': watermark_position, 'watermark_position_offset_x': watermark_position_offset_x, 'watermark_position_offset_y': watermark_position_offset_y, 'watermark_text': watermark_text, 'watermark_text_color': watermark_text_color, 'watermark_text_font': watermark_text_font, 'watermark_text_font_size': watermark_text_font_size, 'watermark_text_opacity': watermark_text_opacity, 'watermark_type': watermark_type}.items()
                if item is not None
            })
            return sync_result_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='adjust_image_color', description='对输入图像的亮度、对比度和饱和度进行调整，支持调亮、调暗、增强对比度、减弱对比度、增强饱和度、减弱饱和度共 6 种快速调整效果。适用于素材基础优化、统一内容视觉风格、营造庄重、复古等特殊氛围等场景。')
    async def adjust_image_color(
        adjust_type: Annotated[str, WithJsonSchema({'description': '必填的图像调整类型。支持 increase_brightness（调亮）、decrease_brightness（调暗）、increase_contrast（增强对比度）、decrease_contrast（减弱对比度）、increase_saturation（增强饱和度）、decrease_saturation（减弱饱和度）。一次仅支持选择一种效果。', 'enum': ['increase_brightness', 'decrease_brightness', 'increase_contrast', 'decrease_contrast', 'increase_saturation', 'decrease_saturation'], 'type': 'string'})] = Field(...),
        image_url: Annotated[str, WithJsonSchema({'description': '待处理图片，必填。支持公网 HTTP/HTTPS URL、火山引擎对象存储 tos:// 两种输入协议；支持 .png、.jpg、.jpeg、.webp 等主流图像格式；仅支持处理静图。建议单张图片不超过 35 MB，输入分辨率的宽和高均不得超过 10000 像素。', 'format': 'media-to-binary', 'type': 'string'})] = Field(...),
        output_format: Annotated[str | None, WithJsonSchema({'default': 'original', 'description': '输出图片格式，可选。支持 original、png、jpeg、webp；original 表示保持与原图一致的格式，默认 original。', 'enum': ['original', 'png', 'jpeg', 'webp'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'original'}),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
    ) -> dict:
        try:
            result = get_client().call('adjust_image_color', **{
                key: item for key, item in {'adjust_type': adjust_type, 'image_url': image_url, 'output_format': output_format, 'queue_id': queue_id}.items()
                if item is not None
            })
            return sync_result_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='compress_image', description='支持一站式图像体积优化，覆盖压缩质量、文件体积上限、输出格式转换和 PNG 瘦身；适用于用户上传图片前的体积治理；适用于网站与 App 的图片分发加载优化；适用于 AIGC 与多模态模型的媒体预处理。')
    async def compress_image(
        image_url: Annotated[str, WithJsonSchema({'description': '待处理图片的 URL。仅支持静图；支持公网 HTTP/HTTPS URL、火山引擎对象存储 tos:// 两种输入协议；支持 .png、.jpg、.jpeg、.webp 等主流图像格式。建议单张输入图片不超过 35 MB。输入图像的宽和高分别都不得超过 10000 像素。输出为 avif 时，建议输入图像的宽×高不超过 100,000 像素，否则任务可能失败。输出为 heic 时，建议输入图像分辨率不超过 4K（约4096×4096 像素），否则任务可能失败。', 'format': 'media-to-binary', 'type': 'string'})] = Field(...),
        max_size: Annotated[int | None, WithJsonSchema({'description': '输出图像的文件体积上限，单位为字节（Byte）。推荐设为 10,485,760 字节（10 MiB）。仅在 output_format 为 jpeg 或 webp 时生效；设置后，系统自动调整压缩参数以尽可能满足体积限制，手动设置的 quality 会被忽略。', 'minimum': 1, 'type': 'integer'})] = Field(None),
        output_format: Annotated[str | None, WithJsonSchema({'default': 'webp', 'description': '输出图片格式。支持 png、jpeg、webp、avif、heic；未提供 output_format 时默认使用 webp。若希望保持原图格式，需要显式传入原格式。', 'enum': ['png', 'jpeg', 'webp', 'avif', 'heic'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'webp'}),
        png_lossy: Annotated[bool | None, WithJsonSchema({'default': False, 'description': '可选开启 PNG 图片有损压缩，以获得更高压缩率；仅在 output_format 为 png 时生效；默认为 false。', 'type': 'boolean'})] = Field(None, json_schema_extra={'default': False}),
        quality: Annotated[int | None, WithJsonSchema({'default': 75, 'description': '压缩质量最小值为 1，最大值为 100，默认为 75。quality 越小，压缩率越高且图像质量损失越大。设置 max_size 时，quality 会被忽略。', 'maximum': 100, 'minimum': 1, 'type': 'integer'})] = Field(None, json_schema_extra={'default': 75}),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
    ) -> dict:
        try:
            result = get_client().call('compress_image', **{
                key: item for key, item in {'image_url': image_url, 'max_size': max_size, 'output_format': output_format, 'png_lossy': png_lossy, 'quality': quality, 'queue_id': queue_id}.items()
                if item is not None
            })
            return sync_result_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='crop_image', description='对输入图像进行多模式裁剪，可执行方向裁剪、定向裁剪、自定义裁剪或内切圆裁剪，适用于多端尺寸适配、主体保留、商品图去边和指定区域截取。')
    async def crop_image(
        image_url: Annotated[str, WithJsonSchema({'description': '待处理图片的 URL，仅支持处理静图。支持公网 HTTP/HTTPS URL、火山引擎对象存储 tos:// 两种输入协议，支持 .png、.jpg、.jpeg、.webp 等主流图像格式。建议单张图片不超过 35 MB。crop_mode 为 circle 时，原图最短边不得超过 2048 px。', 'format': 'media-to-binary', 'type': 'string'})] = Field(...),
        crop_height: Annotated[int | None, WithJsonSchema({'description': 'directional 模式下，crop_height 表示裁剪后图像的目标高度，单位为 px，且 crop_mode 为 directional 时必须提供 crop_height。crop_mode 为 origin 时，crop_height 表示目标高度，单位为 px。crop_height 为 0 时，高度根据 crop_width 按原图比例自适应。', 'minimum': 0, 'type': 'integer'})] = Field(None),
        crop_mode: Annotated[str | None, WithJsonSchema({'default': 'directional', 'description': '支持 directional、origin、custom、circle 四种模式。directional 根据指定宽度、高度和位置进行方向裁剪；origin 根据指定宽高、偏移量和锚点进行定向裁剪；custom 根据指定左上角和右下角坐标进行自定义裁剪；circle 执行最大内切圆裁剪，无需配置其他参数。裁剪模式决定裁剪行为及所需参数，默认 directional。', 'enum': ['directional', 'origin', 'custom', 'circle'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'directional'}),
        crop_position: Annotated[str | None, WithJsonSchema({'default': 'center', 'description': '指定裁剪区域的位置。支持 center、up、down、left、right，分别表示居中、顶部、底部、左侧、右侧，默认 center。', 'enum': ['center', 'up', 'down', 'left', 'right'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'center'}),
        crop_width: Annotated[int | None, WithJsonSchema({'description': 'directional 模式下，crop_width 表示裁剪后图像的目标宽度，单位为 px，且 crop_mode 为 directional 时必须提供 crop_width。crop_mode 为 origin 时，crop_width 表示目标宽度，单位为 px。crop_width 为 0 时，宽度根据 crop_height 按原图比例自适应。directional 模式下，crop_width 与 crop_height 不得同时为 0。', 'minimum': 0, 'type': 'integer'})] = Field(None),
        custom_x1: Annotated[int | None, WithJsonSchema({'description': 'crop_mode 为 custom 时，custom_x1 表示裁剪区域左上角横坐标（X 轴），单位为 px。', 'type': 'integer'})] = Field(None),
        custom_x2: Annotated[int | None, WithJsonSchema({'description': 'crop_mode 为 custom 时，custom_x2 表示裁剪区域右下角横坐标（X 轴），单位为 px。', 'type': 'integer'})] = Field(None),
        custom_y1: Annotated[int | None, WithJsonSchema({'description': 'crop_mode 为 custom 时，custom_y1 表示裁剪区域左上角纵坐标（Y 轴），单位为 px。', 'type': 'integer'})] = Field(None),
        custom_y2: Annotated[int | None, WithJsonSchema({'description': 'crop_mode 为 custom 时，custom_y2 表示裁剪区域右下角纵坐标（Y 轴），单位为 px。', 'type': 'integer'})] = Field(None),
        origin_gravity: Annotated[str | None, WithJsonSchema({'default': 'northwest', 'description': '指定定向裁剪的锚点（起始点）。支持 northwest、north、northeast、west、center、east、southwest、south、southeast，默认 northwest，表示左上角。', 'enum': ['northwest', 'north', 'northeast', 'west', 'center', 'east', 'southwest', 'south', 'southeast'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'northwest'}),
        origin_x: Annotated[int | None, WithJsonSchema({'description': 'crop_mode 为 origin 时，origin_x 表示相对锚点水平偏移量，单位为 px；正值向右，负值向左。', 'type': 'integer'})] = Field(None),
        origin_y: Annotated[int | None, WithJsonSchema({'description': 'crop_mode 为 origin 时，origin_y 表示相对锚点垂直偏移量，单位为 px；正值向下，负值向上。', 'type': 'integer'})] = Field(None),
        output_format: Annotated[str | None, WithJsonSchema({'default': 'original', 'description': '指定输出图片格式，默认 original，表示保持原图格式。circle 模式下，为确保背景透明，建议输出为 png 或 webp；输出 jpeg 时，非圆形区域填充为白色。', 'enum': ['original', 'png', 'jpeg', 'webp'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'original'}),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
    ) -> dict:
        try:
            result = get_client().call('crop_image', **{
                key: item for key, item in {'image_url': image_url, 'crop_height': crop_height, 'crop_mode': crop_mode, 'crop_position': crop_position, 'crop_width': crop_width, 'custom_x1': custom_x1, 'custom_x2': custom_x2, 'custom_y1': custom_y1, 'custom_y2': custom_y2, 'origin_gravity': origin_gravity, 'origin_x': origin_x, 'origin_y': origin_y, 'output_format': output_format, 'queue_id': queue_id}.items()
                if item is not None
            })
            return sync_result_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='enhance_image', description='基于图像内容理解进行智能决策，提升图片的分辨率、清晰度与色彩表现。')
    async def enhance_image(
        image_url: Annotated[str, WithJsonSchema({'description': 'image_url 是待增强图像的 URL，支持公网 HTTP/HTTPS URL、火山引擎对象存储 tos:// 两种输入协议；单张输入图片不得超过 10 MB；输入和输出尺寸范围随 tool_version 而不同；支持 .png、.jpg、.jpeg、.webp 等常见主流图像格式。', 'format': 'media-to-url', 'type': 'string'})] = Field(...),
        enable_correct_color: Annotated[bool | None, WithJsonSchema({'default': True, 'description': '系统将尽量保持增强后图片的色彩与原图一致。false：关闭色彩校正。若您发现开启色彩校正后结果出现过度锐化，建议关闭。', 'type': 'boolean'})] = Field(None, json_schema_extra={'default': True}),
        generative_enhance_mode: Annotated[str | None, WithJsonSchema({'default': 'generative_first', 'description': '生成式增强策略，用于控制模型在“忠于原图”和“创造性修复”之间的平衡点。支持取值如下：fidelity_first：保真度优先。此模式下，模型会更侧重于保留和增强图像的既有细节（如人物特征、原始纹理），尽可能减少对原始内容的改动。适用场景：当您需要高度还原细节时，如处理人像、产品图、文字截图等。generative_first：（默认）生成度优先。此模式下，模型会在保留原图结构的基础上智能生成更丰富、更自然的纹理细节，以达到最佳的主观视觉效果。适用场景：修复严重压缩或模糊的低质量图像，或当您希望获得最大程度的清晰度和细节感，并可以接受一定程度的细节再创作时。', 'enum': ['generative_first', 'fidelity_first'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'generative_first'}),
        multiple: Annotated[float | None, WithJsonSchema({'description': 'multiple 为非必选参数，表示图像处理后相对原图的放大倍数，支持 2 位小数；tool_version 为 standard 时，multiple 的范围是 [1, 8]；tool_version 为 professional 时，multiple 的范围是 [1, 30]；最终生成图像的宽度和高度不能超过所选模型版本支持的最大分辨率。', 'maximum': 30, 'minimum': 1, 'type': 'number'})] = Field(None),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
        target_height: Annotated[int | None, WithJsonSchema({'description': 'target_height 为非必选参数，表示处理后的目标高度，单位为 px；可选，通常与 target_width 配合使用，也可单独设置以保持原图宽高比；tool_version 为 standard 时，target_height 的范围是 [原图高度, 6144]，且最终放大倍数不能超过 8 倍；tool_version 为 professional 时，target_height 的范围是 [64, 10240]。', 'maximum': 10240, 'minimum': 64, 'type': 'integer'})] = Field(None),
        target_width: Annotated[int | None, WithJsonSchema({'description': 'target_width 为非必选参数，表示处理后的目标宽度，单位为 px；target_height 与 target_width 可选搭配使用，也可单独设置以保持原图宽高比；tool_version 为 standard 时，target_width 的范围是 [原图宽度, 6144]，且最终放大倍数不能超过 8 倍；tool_version 为 professional 时，target_width 的范围是 [64, 10240]。', 'maximum': 10240, 'minimum': 64, 'type': 'integer'})] = Field(None),
        tool_version: Annotated[str | None, WithJsonSchema({'default': 'standard', 'description': 'tool_version 为非必选参数，用于选择画质增强模型版本，不同版本在效果、处理范围和价格上有所差异；默认是 standard；standard 是标准版，平衡处理速度与画质效果；professional 是专业版，提供发丝级画质增强，效果更佳；', 'enum': ['standard', 'professional'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'standard'}),
    ) -> dict:
        try:
            result = get_client().call('enhance_image', **{
                key: item for key, item in {'image_url': image_url, 'enable_correct_color': enable_correct_color, 'generative_enhance_mode': generative_enhance_mode, 'multiple': multiple, 'queue_id': queue_id, 'target_height': target_height, 'target_width': target_width, 'tool_version': tool_version}.items()
                if item is not None
            })
            return sync_result_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='erase_image', description='可按不同场景控制自动检测并擦除图片中的文字或常见图标，擦除后的区域通过智能填充技术进行修复，修复后的区域与背景自然融合。')
    async def erase_image(
        image_url: Annotated[str, WithJsonSchema({'description': '待处理图像的 URL；图像来源支持公网 HTTP/HTTPS URL、火山引擎对象存储 tos:// 两种输入协议；输入图像分辨率不得小于 10x10 像素，且不得超过 2560x1440 像素，顺序为宽x高；单张输入图片大小不得超过 10 MB；输入图片支持 .png、.jpg、.jpeg、.webp、.tiff、.bmp 和 .heic 格式。', 'format': 'media-to-url', 'type': 'string'})] = Field(...),
        mask_url: Annotated[str | None, WithJsonSchema({'description': '遮罩图片 URL。通过上传一张黑白遮罩图，可以指定需要擦除的任意形状区域。仅当 standard_scene 为 selected_area_erase 时生效。遮罩图要求如下：图像来源：支持公网 HTTP/HTTPS URL、火山引擎对象存储 (tos://) 两种输入协议。分辨率要求：必须与输入图像 image_url 的分辨率一致。如果同时传入 selected_area，则擦除两个参数指定区域的并集。', 'format': 'media-to-url', 'type': 'string'})] = Field(None),
        output_format: Annotated[str | None, WithJsonSchema({'default': 'webp', 'description': '输出图片的格式，支持 webp、png 和 jpeg；默认 webp。', 'enum': ['png', 'jpeg', 'webp'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'webp'}),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
        selected_area: Annotated[dict[str, Any] | None, WithJsonSchema({'description': '指定擦除区域（矩形框）。仅当 standard_scene 为 selected_area_erase 时生效。坐标系以输入图像的左上角为原点，宽度和高度均归一化为 [0,1]。例如，(0.5, 0.5) 代表图像中心点。如果同时传入 mask_url，则擦除两个参数指定区域的并集。', 'properties': {'bottom_right_x': {'description': '矩形框右下角的 X 坐标（横向位置）。该值必须大于 top_left_x。', 'maximum': 1, 'minimum': 0, 'type': 'number'}, 'bottom_right_y': {'description': '矩形框右下角的 Y 坐标（纵向位置）。该值必须大于 top_left_y，取值范围 [0, 1]。', 'maximum': 1, 'minimum': 0, 'type': 'number'}, 'top_left_x': {'description': '矩形框左上角的 X 坐标（横向位置）。该值为相对于图片总宽度的比例。', 'maximum': 1, 'minimum': 0, 'type': 'number'}, 'top_left_y': {'description': '矩形框左上角的 Y 坐标（纵向位置）。该值为相对于图片总高度的比例。', 'maximum': 1, 'minimum': 0, 'type': 'number'}}, 'required': ['top_left_x', 'top_left_y', 'bottom_right_x', 'bottom_right_y'], 'type': 'object', 'x-field-relations': [{'left': 'bottom_right_x', 'operator': 'greater_than', 'right': 'top_left_x'}, {'left': 'bottom_right_y', 'operator': 'greater_than', 'right': 'top_left_y'}]})] = Field(None),
        standard_erase_text: Annotated[str | None, WithJsonSchema({'description': 'standard_erase_text 指定需要擦除的文字内容；仅当 standard_scene 为 full_screen_text_erase 时生效；不提供 standard_erase_text 时会擦除识别到的所有文字。', 'type': 'string'})] = Field(None),
        standard_scene: Annotated[str | None, WithJsonSchema({'default': 'full_screen_text_erase', 'description': '标准版擦除场景，仅当 tool_version 为 standard 时生效。默认值为 full_screen_text_erase。full_screen_text_erase：全屏文字擦除。可通过 standard_erase_text 字段指定要擦除的文字，不指定则默认擦除所有文字内容。full_screen_icon_erase：全屏图标擦除。selected_area_erase：指定区域擦除。使用此场景时，您必须至少提供 selected_area（矩形坐标）或 mask_url（遮罩图）中的一个参数来定义擦除范围。如果同时提供了这两个参数，系统将擦除它们所定义区域的并集。', 'enum': ['full_screen_text_erase', 'full_screen_icon_erase', 'selected_area_erase'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'full_screen_text_erase'}),
        tool_version: Annotated[str | None, WithJsonSchema({'default': 'standard', 'description': '图像擦除修复选用的模型版本；当前仅支持 standard（标准版）；standard 标准版适用于简单、明确的擦除任务。', 'enum': ['standard'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'standard'}),
    ) -> dict:
        try:
            result = get_client().call('erase_image', **{
                key: item for key, item in {'image_url': image_url, 'mask_url': mask_url, 'output_format': output_format, 'queue_id': queue_id, 'selected_area': selected_area, 'standard_erase_text': standard_erase_text, 'standard_scene': standard_scene, 'tool_version': tool_version}.items()
                if item is not None
            })
            return sync_result_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='evaluate_image_quality', description='用于图像画质评估，对输入图片进行主客观画质和美学评分，适用于质量监控、低质图筛查、内容审核、推荐排序和训练数据清洗。')
    async def evaluate_image_quality(
        image_url: Annotated[str, WithJsonSchema({'description': 'image_url 是待评估的图像 URL，支持公网 HTTP/HTTPS URL、火山引擎对象存储 tos:// 两种输入协议，支持 png、jpeg、webp 和 heic 图像格式，单张图片不得超过 10 MB，图像输入分辨率的长边不得超过 7680 px，短边不得超过 4320 px。', 'format': 'media-to-url', 'type': 'string'})] = Field(...),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
        standard_evaluate_items: Annotated[list[Any] | None, WithJsonSchema({'default': ['vqscore', 'noise', 'aesthetic', 'blur'], 'description': 'standard_evaluate_items 为非必填参数，仅当 tool_version 为 standard 时生效，用于指定需要返回的标准版评估维度。standard_evaluate_items 可选 15 个评估维度：vqscore（图片主观质量，值越高表示质量越好）、advcolor（图片整体色彩质量）、blockiness（块效应（马赛克）严重程度）、noise（图片噪声强度）、aesthetic（综合大众美学的质量评分）、blur（模糊度）、cg（是否为非自然场景，如游戏、录屏）、contrast（对比度）、texture（纹理丰富程度）、brightness（平均亮度）、overexposure（过曝光程度）、hue（色调均衡程度）、saturation（饱和度均衡程度）、green（偏绿或绿幕检测）、cmartifacts（压缩失真检测）。standard_evaluate_items 为空时默认返回 vqscore、noise、aesthetic、blur 四个维度。', 'items': {'description': '评估工具。', 'enum': ['vqscore', 'advcolor', 'blockiness', 'noise', 'aesthetic', 'blur', 'cg', 'contrast', 'texture', 'brightness', 'overexposure', 'hue', 'saturation', 'green', 'cmartifacts'], 'type': 'string'}, 'type': 'array'})] = Field(None, json_schema_extra={'default': ['vqscore', 'noise', 'aesthetic', 'blur']}),
        tool_version: Annotated[str | None, WithJsonSchema({'default': 'standard', 'description': 'tool_version 用于选择画质评估所用的模型版本，为非必填参数，支持 standard 和 professional，默认为 standard。standard 提供 15 种基础画质评估维度，可通过 standard_evaluate_items 灵活选择部分或全部维度，在成本和功能灵活性上达到较好的平衡。professional 基于大模型进行评估，直接返回一组固定的综合性评分，提供更优的综合评估效果，适用于对图像品质要求较高的场景，且不支持自定义评估维度。', 'enum': ['standard', 'professional'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'standard'}),
    ) -> dict:
        try:
            result = get_client().call('evaluate_image_quality', **{
                key: item for key, item in {'image_url': image_url, 'queue_id': queue_id, 'standard_evaluate_items': standard_evaluate_items, 'tool_version': tool_version}.items()
                if item is not None
            })
            return sync_result_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='face_blur_image', description='自动检测图片中的所有人脸区域并进行马赛克处理，用于一键保护图片中的人脸隐私。支持社交平台内容审核、街景或监控画面脱敏、新闻媒体素材处理以及 AI 训练数据集脱敏等批量人脸隐私保护场景。')
    async def face_blur_image(
        image_url: Annotated[str, WithJsonSchema({'description': '待打码的图像 URL，支持公网 HTTP/HTTPS URL、火山引擎对象存储 tos:// 两种输入协议；支持 .png、.jpg、.jpeg、.webp、.avif 格式，不支持动图。建议图像文件大小不超过 35 MB；图片文件过大可能导致处理失败；图片宽度和高度的乘积不得超过 4 亿像素。', 'format': 'media-to-url', 'type': 'string'})] = Field(...),
        blur_shape: Annotated[str | None, WithJsonSchema({'default': 'circle', 'description': '人脸模糊区域的形状，支持 circle 或 rectangle：circle 表示圆形，rectangle 表示矩形；默认 circle。', 'enum': ['circle', 'rectangle'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'circle'}),
        face_detect_thresh: Annotated[float | None, WithJsonSchema({'default': 0.9, 'description': '人脸检测置信度阈值必须大于 0 且小于 1；越高过滤越严格，过低可能误判非人脸区域，过高可能漏检人脸；默认 0.9。', 'exclusiveMaximum': 1, 'exclusiveMinimum': 0, 'type': 'number'})] = Field(None, json_schema_extra={'default': 0.9}),
        mosaic_step: Annotated[int | None, WithJsonSchema({'default': 12, 'description': '马赛克像素格大小，单位 px，必须为正整数；越大，马赛克颗粒越大且脱敏强度越高；建议范围为 [5, 100]；默认 12。', 'maximum': 100, 'minimum': 5, 'type': 'integer'})] = Field(None, json_schema_extra={'default': 12}),
        output_format: Annotated[str | None, WithJsonSchema({'default': 'webp', 'description': '输出图片格式，支持 png、jpeg 或 webp；默认 webp。', 'enum': ['png', 'jpeg', 'webp'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'webp'}),
    ) -> dict:
        try:
            result = get_client().call('face_blur_image', **{
                key: item for key, item in {'image_url': image_url, 'blur_shape': blur_shape, 'face_detect_thresh': face_detect_thresh, 'mosaic_step': mosaic_step, 'output_format': output_format}.items()
                if item is not None
            })
            return sync_result_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='flip_image', description='支持对单张图片执行水平或竖直翻转。')
    async def flip_image(
        flip_type: Annotated[str, WithJsonSchema({'description': '翻转方向包括 horizontal 和 vertical：horizontal 表示水平翻转（左右镜像），vertical 表示竖直翻转（上下翻转）。', 'enum': ['horizontal', 'vertical'], 'type': 'string'})] = Field(...),
        image_url: Annotated[str, WithJsonSchema({'description': '待处理图片仅支持处理静图，支持公网 HTTP/HTTPS URL、火山引擎对象存储 tos:// 两种输入协议；支持 .png、.jpg、.jpeg、.webp 等主流图像格式；建议单张图片不超过 35 MB，输入图片的宽和高均不得超过 10000 像素。', 'format': 'media-to-binary', 'type': 'string'})] = Field(...),
        output_format: Annotated[str | None, WithJsonSchema({'default': 'original', 'description': '输出图片格式，非必选；默认为 original，表示保持与原图一致的格式；另有 png、jpeg、webp。', 'enum': ['original', 'png', 'jpeg', 'webp'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'original'}),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
    ) -> dict:
        try:
            result = get_client().call('flip_image', **{
                key: item for key, item in {'flip_type': flip_type, 'image_url': image_url, 'output_format': output_format, 'queue_id': queue_id}.items()
                if item is not None
            })
            return sync_result_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='gaussian_blur_image', description='用于图像高斯模糊；通过设定模糊强度快速对图片进行模糊处理，适用于隐私信息弱化、背景氛围化、生成预览图及封面背景等场景。')
    async def gaussian_blur_image(
        image_url: Annotated[str, WithJsonSchema({'description': '待处理图片 URL，支持公网 HTTP/HTTPS URL、火山引擎对象存储 tos:// 两种输入协议；仅支持处理静图；支持 .png、.jpg、.jpeg、.webp 等主流图像格式。输入图像的宽和高均不得超过 10000 像素，建议单张图片不超过 35 MB。', 'format': 'media-to-binary', 'type': 'string'})] = Field(...),
        blur_strength: Annotated[int | None, WithJsonSchema({'default': 10, 'description': '高斯模糊强度，数值越大越模糊，范围 1 到 100，默认 10。推荐 10 为轻度模糊，推荐 30 为中度模糊，推荐 100 为重度模糊。', 'maximum': 100, 'minimum': 1, 'type': 'integer'})] = Field(None, json_schema_extra={'default': 10}),
        output_format: Annotated[str | None, WithJsonSchema({'default': 'original', 'description': '输出图片格式，original 表示保持与原图一致的格式；支持 original、png、jpeg、webp，默认 original。', 'enum': ['original', 'png', 'jpeg', 'webp'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'original'}),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
    ) -> dict:
        try:
            result = get_client().call('gaussian_blur_image', **{
                key: item for key, item in {'image_url': image_url, 'blur_strength': blur_strength, 'output_format': output_format, 'queue_id': queue_id}.items()
                if item is not None
            })
            return sync_result_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='image_ocr', description='识别图片中的印刷体或手写体文字并返回文本块内容、位置坐标与置信度。标准版支持简体中文和英文印刷体通用识别；加强版支持印刷体、手写体及 100+ 语种，并支持通用识别与关键词匹配识别。')
    async def image_ocr(
        image_url: Annotated[str, WithJsonSchema({'description': '待识别的图像 URL。图像来源支持公网 HTTP/HTTPS URL、火山引擎对象存储 (tos://) 两种输入协议；图像长边不得超过 3840 px，短边不得超过 2160 px，单张图片文件大小不得超过 10 MB；支持 .png、.jpg、.jpeg、.webp、.tiff、.bmp 和 .heic 格式。', 'format': 'media-to-url', 'type': 'string'})] = Field(...),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
    ) -> dict:
        try:
            result = get_client().call('image_ocr', **{
                key: item for key, item in {'image_url': image_url, 'queue_id': queue_id}.items()
                if item is not None
            })
            return sync_result_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='invert_image', description='用于图像负片，对输入图像执行负片（反相）效果，将图像的明暗关系与颜色映射为原图的相反效果，即明暗反转、色彩转为补色。')
    async def invert_image(
        image_url: Annotated[str, WithJsonSchema({'description': '待处理的图片 URL，支持公网 HTTP/HTTPS URL、火山引擎对象存储（tos://）两种输入协议；支持 .png、.jpg、.jpeg、.webp 等主流图像格式，且仅支持处理静图；建议单张图片不超过 35 MB，输入图像的宽和高均不得超过 10000 像素。', 'format': 'media-to-binary', 'type': 'string'})] = Field(...),
        output_format: Annotated[str | None, WithJsonSchema({'default': 'original', 'description': '输出图片的格式，支持 png、jpeg、webp，默认使用 original 保持与原图一致的格式。', 'enum': ['original', 'png', 'jpeg', 'webp'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'original'}),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
    ) -> dict:
        try:
            result = get_client().call('invert_image', **{
                key: item for key, item in {'image_url': image_url, 'output_format': output_format, 'queue_id': queue_id}.items()
                if item is not None
            })
            return sync_result_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='mosaic_image', description='支持对整张图像或指定矩形区域进行马赛克打码，可调整像素格形状与大小。支持用于遮挡人脸、证件信息、车牌、聊天记录等敏感内容。')
    async def mosaic_image(
        image_url: Annotated[str, WithJsonSchema({'description': '仅支持处理静图；建议单张图片不超过 35 MB；输入图像的宽和高均不得超过 10000 像素。支持 .png、.jpg、.jpeg、.webp 等主流图像格式。支持公网 HTTP/HTTPS URL、火山引擎对象存储（tos://）两种输入协议。', 'format': 'media-to-binary', 'type': 'string'})] = Field(...),
        mosaic_regions: Annotated[list[Any] | None, WithJsonSchema({'description': '最多支持 3 个矩形区域。', 'items': {'properties': {'bottom_right_x': {'description': '框选区域右下角的 X 轴坐标，单位为 px，坐标原点为图像左上角，必须大于 top_left_x。', 'minimum': 0, 'type': 'integer'}, 'bottom_right_y': {'description': '框选区域右下角的 Y 轴坐标，单位为 px，坐标原点为图像左上角，必须大于 top_left_y。', 'minimum': 0, 'type': 'integer'}, 'top_left_x': {'description': '框选区域左上角的横 X 轴坐标，单位为 px，坐标原点为图像左上角。', 'minimum': 0, 'type': 'integer'}, 'top_left_y': {'description': '框选区域左上角的 Y 轴坐标，单位为 px，坐标原点为图像左上角。', 'minimum': 0, 'type': 'integer'}}, 'required': ['top_left_x', 'top_left_y', 'bottom_right_x', 'bottom_right_y'], 'type': 'object', 'x-field-relations': [{'left': 'bottom_right_x', 'operator': 'greater_than', 'right': 'top_left_x'}, {'left': 'bottom_right_y', 'operator': 'greater_than', 'right': 'top_left_y'}]}, 'maxItems': 3, 'minItems': 1, 'type': 'array'})] = Field(None),
        mosaic_shape: Annotated[str | None, WithJsonSchema({'default': 'circle', 'description': '默认使用 circle。支持 circle 和 rectangle：circle 表示圆形/椭圆像素格，视觉更柔和；rectangle 表示矩形像素格，遮挡更规整。', 'enum': ['circle', 'rectangle'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'circle'}),
        mosaic_step_x: Annotated[int | None, WithJsonSchema({'default': 12, 'description': '控制打码像素格的宽度，单位为 px；数值越大，马赛克颗粒感越强。默认值为 12。', 'minimum': 1, 'type': 'integer'})] = Field(None, json_schema_extra={'default': 12}),
        mosaic_step_y: Annotated[int | None, WithJsonSchema({'default': 12, 'description': '控制打码像素格的高度，单位为 px；数值越大，马赛克颗粒感越强。默认值为 12。', 'minimum': 1, 'type': 'integer'})] = Field(None, json_schema_extra={'default': 12}),
        mosaic_type: Annotated[str | None, WithJsonSchema({'default': 'full-image', 'description': '默认使用 full-image，对整张图片打码。支持 full-image 和 specify-region：full-image 对整张图片打码；specify-region 仅对 mosaic_regions 指定的区域打码。', 'enum': ['full-image', 'specify-region'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'full-image'}),
        output_format: Annotated[str | None, WithJsonSchema({'default': 'original', 'description': '支持 png、jpeg、webp，也支持并默认使用 original，保持与原图一致的格式。', 'enum': ['original', 'png', 'jpeg', 'webp'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'original'}),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
    ) -> dict:
        try:
            result = get_client().call('mosaic_image', **{
                key: item for key, item in {'image_url': image_url, 'mosaic_regions': mosaic_regions, 'mosaic_shape': mosaic_shape, 'mosaic_step_x': mosaic_step_x, 'mosaic_step_y': mosaic_step_y, 'mosaic_type': mosaic_type, 'output_format': output_format, 'queue_id': queue_id}.items()
                if item is not None
            })
            return sync_result_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='probe_image_metadata', description='支持查询 metadata、avghue、alpha、blurhash 四种图像信息。')
    async def probe_image_metadata(
        image_url: Annotated[str, WithJsonSchema({'description': '待探测的图片 URL。支持公网 HTTP/HTTPS URL、与火山引擎对象存储 tos:// 两种输入协议；支持 .png、.jpg、.jpeg、.webp 格式。图片输入分辨率的宽和高均不得超过 10000 像素，建议单张图片文件大小不超过 35 MB。', 'format': 'media-to-imagex-uri', 'type': 'string'})] = Field(...),
        info_type: Annotated[str | None, WithJsonSchema({'default': 'metadata', 'description': '查询信息类型。metadata 获取图像的基本元信息；avghue 提取图像的主题色；alpha 分析图像的 Alpha 透明通道；blurhash 生成图像的 BlurHash 值。默认 metadata。', 'enum': ['metadata', 'avghue', 'alpha', 'blurhash'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'metadata'}),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
    ) -> dict:
        try:
            result = get_client().call('probe_image_metadata', **{
                key: item for key, item in {'image_url': image_url, 'info_type': info_type, 'queue_id': queue_id}.items()
                if item is not None
            })
            return sync_result_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='remove_image_background', description='自动识别并保留通用物体、人像或商品主体，移除背景；PNG、WebP 可输出透明背景，JPEG 的透明区域会填充为黑色。人像和商品场景还可生成主体描边或裁去多余透明区域。')
    async def remove_image_background(
        image_url: Annotated[str, WithJsonSchema({'description': '待处理的图像 URL，支持公网 HTTP/HTTPS URL、火山引擎对象存储 tos:// 两种输入协议；支持 .png、.jpg、.jpeg、.webp、.tiff、.bmp 和 .heic 格式；单张图片不得超过 10 MB，图像输入分辨率的长边不得超过 7680 px、短边不得超过 4320 px。', 'format': 'media-to-url', 'type': 'string'})] = Field(...),
        scene: Annotated[str, WithJsonSchema({'description': '背景移除场景可用 general、human、product；general 为通用场景，适用于期望抠出图像主体但不确定该主体所属分类的场景；human 为人像抠图场景，适用于仅需抠出图像中的人像主体的场景；product 为商品抠图场景，适用于仅需抠出图像中的商品主体的场景。', 'enum': ['general', 'human', 'product'], 'type': 'string'})] = Field(...),
        contour_color: Annotated[str | None, WithJsonSchema({'default': '#FFFFFF', 'description': '主体描边颜色，使用十六进制 RGB，默认 #FFFFFF；仅当 need_contour 为 true 且 scene 为 human 或 product 时生效。', 'pattern': '^#[0-9a-fA-F]{6}$', 'type': 'string'})] = Field(None, json_schema_extra={'default': '#FFFFFF'}),
        contour_size: Annotated[int | None, WithJsonSchema({'default': 10, 'description': '主体描边宽度，单位 px，范围 1 至 100，默认 10；仅当 need_contour 为 true 且 scene 为 human 或 product 时生效。', 'maximum': 100, 'minimum': 1, 'type': 'integer'})] = Field(None, json_schema_extra={'default': 10}),
        need_contour: Annotated[bool | None, WithJsonSchema({'default': False, 'description': '是否为主体生成描边，默认 false；仅在 scene 为 human 或 product 时生效，在 general 场景下会被忽略。', 'type': 'boolean'})] = Field(None, json_schema_extra={'default': False}),
        need_crop_background: Annotated[bool | None, WithJsonSchema({'default': False, 'description': '是否将输出图片的透明背景裁剪到刚好包裹住主体，默认 false；仅在 scene 为 human 或 product 时生效，在 general 场景下会被忽略。', 'type': 'boolean'})] = Field(None, json_schema_extra={'default': False}),
        output_format: Annotated[str | None, WithJsonSchema({'default': 'png', 'description': '输出图片格式可用 png、jpeg、webp，默认 png；png 支持透明背景，webp 支持透明背景，jpeg 不支持透明背景，jpeg 的透明区域将填充为黑色。', 'enum': ['png', 'jpeg', 'webp'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'png'}),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
    ) -> dict:
        try:
            result = get_client().call('remove_image_background', **{
                key: item for key, item in {'image_url': image_url, 'scene': scene, 'contour_color': contour_color, 'contour_size': contour_size, 'need_contour': need_contour, 'need_crop_background': need_crop_background, 'output_format': output_format, 'queue_id': queue_id}.items()
                if item is not None
            })
            return sync_result_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='resize_image', description='用于图像缩放，支持按指定宽高精确缩放，也可按长边、短边或等比模式缩放，适用于多端素材适配、封面与缩略图生成及批量图片预处理。')
    async def resize_image(
        image_url: Annotated[str, WithJsonSchema({'description': 'image_url 是待处理图片的 URL，图片来源支持公网 HTTP/HTTPS URL、火山引擎对象存储 tos:// 两种输入协议；输入支持 .png、.jpg、.jpeg、.webp 等主流图像格式；输入仅支持静图；建议单张输入图片不超过 35 MB，输入图像的宽和高均不得超过 10000 像素。', 'format': 'media-to-binary', 'type': 'string'})] = Field(...),
        output_format: Annotated[str | None, WithJsonSchema({'default': 'original', 'description': 'output_format 指定输出图片格式；支持 original、png、jpeg、webp，original 表示输出保持与原图一致的格式；默认 original。', 'enum': ['original', 'png', 'jpeg', 'webp'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'original'}),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
        resize_adaptive: Annotated[list[Any] | None, WithJsonSchema({'default': ['enlarge', 'shrink'], 'description': 'resize_adaptive 控制仅在特定条件下执行缩放；支持 enlarge、shrink；enlarge 仅在原图尺寸小于目标尺寸时执行放大，shrink 仅在原图尺寸大于目标尺寸时执行缩小；默认 enlarge、shrink，即总是执行缩放。', 'items': {'description': '缩放适配策略枚举。', 'enum': ['enlarge', 'shrink'], 'type': 'string'}, 'minItems': 1, 'type': 'array', 'uniqueItems': True})] = Field(None, json_schema_extra={'default': ['enlarge', 'shrink']}),
        resize_long: Annotated[int | None, WithJsonSchema({'default': 0, 'description': '目标图像的长边尺寸，单位为像素。等比缩放：仅设置此参数（或将 resize_short 设为 0），图像将按原始比例缩放，使长边匹配此值。组合使用：当与 resize_short 同时设置时，缩放行为由 resize_mode 参数决定。与 resize_short 必须至少提供一个大于 0 的值。', 'minimum': 0, 'type': 'integer'})] = Field(None, json_schema_extra={'default': 0}),
        resize_mode: Annotated[str | None, WithJsonSchema({'default': 'contain', 'description': 'resize_mode 定义同时指定 resize_long 和 resize_short 时的缩放行为；支持 exact、contain、cover；exact 强制将图像精确缩放到 resize_long x resize_short，可能导致拉伸或压缩变形；contain 保持原始宽高比，使图像完整包含在 resize_long x resize_short 矩形框内，最终宽高均不超过指定值；cover 保持原始宽高比，使图像完全填满 resize_long x resize_short 矩形框，并居中裁剪超出部分；默认 contain。', 'enum': ['exact', 'contain', 'cover'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'contain'}),
        resize_short: Annotated[int | None, WithJsonSchema({'default': 0, 'description': '目标图像的短边尺寸，单位为像素。等比缩放：仅设置此参数（或将 resize_long 设为 0），图像将按原始比例缩放，使短边匹配此值。组合使用：当与 resize_long 同时设置时，缩放行为由 resize_mode 参数决定。与 resize_long 必须至少提供一个大于 0 的值。', 'minimum': 0, 'type': 'integer'})] = Field(None, json_schema_extra={'default': 0}),
    ) -> dict:
        try:
            result = get_client().call('resize_image', **{
                key: item for key, item in {'image_url': image_url, 'output_format': output_format, 'queue_id': queue_id, 'resize_adaptive': resize_adaptive, 'resize_long': resize_long, 'resize_mode': resize_mode, 'resize_short': resize_short}.items()
                if item is not None
            })
            return sync_result_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='rotate_image', description='通过设置旋转角度和旋转背景样式对图片进行旋转处理，适用于图片方向校正、创意编辑和批量图像处理。')
    async def rotate_image(
        image_url: Annotated[str, WithJsonSchema({'description': '待处理图片的 URL。支持公网 HTTP/HTTPS URL、对象存储 tos:// 两种输入协议，支持 .png、.jpg、.jpeg、.webp 等主流图像格式，仅支持处理静图。输入图片宽度和高度均不得超过 10000 像素，建议单张图片不超过 35 MB。', 'format': 'media-to-binary', 'type': 'string'})] = Field(...),
        rotate_angle: Annotated[int, WithJsonSchema({'description': 'rotate_angle 表示图像逆时针旋转的角度，必须大于 0 且必须小于 360。', 'maximum': 359, 'minimum': 1, 'type': 'integer'})] = Field(...),
        fill_color: Annotated[str | None, WithJsonSchema({'default': 'Black', 'description': 'fill_color 用于填充旋转后因非正交角度产生的空白区域，支持 Black、White、Transparent。Black 表示黑色填充，White 表示白色填充，Transparent 表示透明填充，建议配合 png 格式输出，fill_color 默认为 Black。', 'enum': ['Black', 'White', 'Transparent'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'Black'}),
        output_format: Annotated[str | None, WithJsonSchema({'default': 'webp', 'description': 'output_format 用于指定输出图片格式，支持 original、png、jpeg、webp。original 表示保持与原图一致的格式，output_format 默认为 webp。', 'enum': ['original', 'png', 'jpeg', 'webp'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'webp'}),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
    ) -> dict:
        try:
            result = get_client().call('rotate_image', **{
                key: item for key, item in {'image_url': image_url, 'rotate_angle': rotate_angle, 'fill_color': fill_color, 'output_format': output_format, 'queue_id': queue_id}.items()
                if item is not None
            })
            return sync_result_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='round_corner_image', description='为图片四角快速添加正圆或椭圆圆角，适用于头像、卡片、电商主图等常见视觉编辑场景。')
    async def round_corner_image(
        image_url: Annotated[str, WithJsonSchema({'description': '待处理图片的 URL，支持公网 HTTP/HTTPS URL、火山引擎对象存储 tos:// 两种输入协议；支持 .png、.jpg、.jpeg、.webp 等主流图像格式，仅支持处理静图。建议单张图片不超过 35 MB，输入图片的宽和高均不得超过 10000 像素。', 'format': 'media-to-binary', 'type': 'string'})] = Field(...),
        circle_radius: Annotated[int | None, WithJsonSchema({'default': 50, 'description': '正圆圆角半径，单位为 px，取值范围为 [0, 原图最小边/2]；超过该范围时按最大内切圆半径处理。', 'minimum': 0, 'type': 'integer'})] = Field(None, json_schema_extra={'default': 50}),
        corner_type: Annotated[str | None, WithJsonSchema({'default': 'circle', 'description': '圆角类型支持 circle 和 ellipse。circle 表示正圆圆角，半径通过 circle_radius 配置；ellipse 表示椭圆圆角，X 轴和 Y 轴半径分别通过 ellipse_radius_x 和 ellipse_radius_y 配置。默认 circle。', 'enum': ['circle', 'ellipse'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'circle'}),
        ellipse_radius_x: Annotated[int | None, WithJsonSchema({'default': 40, 'description': '椭圆圆角 X 轴（水平）半径，单位为 px，取值大于等于 0。', 'minimum': 0, 'type': 'integer'})] = Field(None, json_schema_extra={'default': 40}),
        ellipse_radius_y: Annotated[int | None, WithJsonSchema({'default': 60, 'description': '椭圆圆角 Y 轴（垂直）半径，单位为 px，取值大于等于 0。', 'minimum': 0, 'type': 'integer'})] = Field(None, json_schema_extra={'default': 60}),
        output_format: Annotated[str | None, WithJsonSchema({'default': 'webp', 'description': '输出图片格式支持 original、png、webp 和 jpeg，默认 webp。original 保持原图格式；png 和 webp 会对圆角外区域进行透明填充，jpeg 会对圆角外区域进行白色填充。', 'enum': ['original', 'png', 'jpeg', 'webp'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'webp'}),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
    ) -> dict:
        try:
            result = get_client().call('round_corner_image', **{
                key: item for key, item in {'image_url': image_url, 'circle_radius': circle_radius, 'corner_type': corner_type, 'ellipse_radius_x': ellipse_radius_x, 'ellipse_radius_y': ellipse_radius_y, 'output_format': output_format, 'queue_id': queue_id}.items()
                if item is not None
            })
            return sync_result_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='sharpen_image', description='用于图像锐化，通过对输入图像进行锐化处理，有效增强图像的边缘细节与整体清晰度。适用于电商素材优化、UGC 画质增强、封面海报二创等场景。')
    async def sharpen_image(
        image_url: Annotated[str, WithJsonSchema({'description': '待处理图片 URL，支持 .png、.jpg、.jpeg、.webp 等主流图像格式；支持公网 HTTP/HTTPS URL、火山引擎对象存储 tos:// 两种输入协议；仅支持处理静图；输入图像的宽和高均不得超过 10000 像素；建议单张图片不超过 35 MB。', 'format': 'media-to-binary', 'type': 'string'})] = Field(...),
        output_format: Annotated[str | None, WithJsonSchema({'default': 'original', 'description': '输出图片格式，默认并支持 original，表示保持与原图一致的格式；也支持 png、jpeg、webp。', 'enum': ['original', 'png', 'jpeg', 'webp'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'original'}),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
        sharpen_level: Annotated[str | None, WithJsonSchema({'default': 'low', 'description': '锐化强度档位，支持 low（轻度锐化）、medium（中度锐化）和 high（重度锐化），默认 low。', 'enum': ['low', 'medium', 'high'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'low'}),
    ) -> dict:
        try:
            result = get_client().call('sharpen_image', **{
                key: item for key, item in {'image_url': image_url, 'output_format': output_format, 'queue_id': queue_id, 'sharpen_level': sharpen_level}.items()
                if item is not None
            })
            return sync_result_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='slim_image', description='集智瘦身通过 AI 大幅缩小图片体积，修复毛刺、彩噪和块效应等问题，增强图像边缘与纹理细节，输出更轻量且更清晰的图片。')
    async def slim_image(
        image_url: Annotated[str, WithJsonSchema({'description': '待处理图片 URL，支持公网 HTTP/HTTPS URL、火山引擎对象存储 tos:// 两种输入协议。输入图片支持 jpeg、jpg、png、heic、avif 和 webp 格式，暂不支持动图输入。建议单张输入图片不超过 50 MB；输入图像的宽度不得超过 10000 像素，高度不得超过 10000 像素。当输入图像格式为 avif 时，建议宽与高的乘积不要超过 100,000；当 avif 输入图像的宽与高乘积超过建议的 100,000 时，处理可能失败。', 'format': 'media-to-binary', 'type': 'string'})] = Field(...),
        output_format: Annotated[str | None, WithJsonSchema({'default': 'original', 'description': '输出图片格式，默认 original；original 表示输出保持与原图一致的格式，支持 original、png、jpeg 或 webp。输入和输出格式均为 JPEG 时，部分已高度压缩的源文件处理后体积可能无明显变化；JPEG 输入输出时体积可能不降或略增，与原图压缩参数及 JPEG 重新编码特性有关，属于正常现象；输入和输出格式均为 JPEG 时，少数情况下处理后体积甚至会略微增大。', 'enum': ['original', 'png', 'jpeg', 'webp'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'original'}),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
    ) -> dict:
        try:
            result = get_client().call('slim_image', **{
                key: item for key, item in {'image_url': image_url, 'output_format': output_format, 'queue_id': queue_id}.items()
                if item is not None
            })
            return sync_result_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='smart_crop_image', description='自动识别图像中的主体人脸区域，并适配指定尺寸进行裁剪；支持普通人脸和动漫人脸场景。未识别到人脸时，可按预设的降级策略输出结果。')
    async def smart_crop_image(
        image_url: Annotated[str, WithJsonSchema({'description': '待处理图片的 URL。支持公网 HTTP/HTTPS URL、火山引擎对象存储 tos:// 两种输入协议；支持 .png、.jpg、.jpeg、.webp、.tiff、.bmp、.heic 格式。图片宽和高均不得超过 6000 px，建议单张输入图片不超过 10 MB。', 'format': 'media-to-url', 'type': 'string'})] = Field(...),
        crop_strategy: Annotated[str | None, WithJsonSchema({'default': 'top_crop', 'description': '可选。裁剪后图片与目标宽高比例不一致时，使用降级裁剪策略；支持三种策略：top_crop（从图像顶部开始并水平居中裁剪，默认）、center_crop（从图像正中心开始向四周裁剪）、frosted_glass_fill（保持原图完整，并在两侧或上下添加毛玻璃背景以达到目标尺寸）。', 'enum': ['top_crop', 'center_crop', 'frosted_glass_fill'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'top_crop'}),
        frosted_glass_strength: Annotated[float | None, WithJsonSchema({'default': 100, 'description': '可选。毛玻璃填充的模糊强度，数值越大，模糊效果越强；仅在 crop_strategy 为 frosted_glass_fill 时生效。默认 100，推荐取值范围为 [10, 100]。', 'minimum': 1, 'type': 'number'})] = Field(None, json_schema_extra={'default': 100}),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
        scene: Annotated[str | None, WithJsonSchema({'default': 'person_face', 'description': '可选。用于指定识别主体的裁剪场景模型；支持 person_face 和 cartoon_face 两种场景。person_face 表示普通人脸裁剪；cartoon_face 表示动漫人脸裁剪。默认 person_face。', 'enum': ['person_face', 'cartoon_face'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'person_face'}),
        target_height: Annotated[int | None, WithJsonSchema({'default': 100, 'description': '可选。裁剪后的目标高度，单位 px；默认 100。', 'minimum': 1, 'type': 'integer'})] = Field(None, json_schema_extra={'default': 100}),
        target_width: Annotated[int | None, WithJsonSchema({'default': 100, 'description': '可选。裁剪后的目标宽度，单位 px；默认 100。', 'minimum': 1, 'type': 'integer'})] = Field(None, json_schema_extra={'default': 100}),
    ) -> dict:
        try:
            result = get_client().call('smart_crop_image', **{
                key: item for key, item in {'image_url': image_url, 'crop_strategy': crop_strategy, 'frosted_glass_strength': frosted_glass_strength, 'queue_id': queue_id, 'scene': scene, 'target_height': target_height, 'target_width': target_width}.items()
                if item is not None
            })
            return sync_result_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

