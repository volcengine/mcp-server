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
from ..utils.response import sync_result_response, error_response

TOOL_NAMES = ['enhance_image', 'erase_image', 'evaluate_image_quality', 'image_ocr', 'remove_image_background']


def register_tools(mcp, client: MediKitClient) -> None:
    @mcp.tool(name="image_ocr", description="识别图片中的通用印刷体文字，返回可编辑文本、文字框坐标和置信度。\n本期支持简体中文和英文通用场景识别。")
    async def image_ocr(
        image_url: str = Field(..., description="输入图片 URL，需为公网可访问的 png/jpg/jpeg/webp/heic/avif 图片，单图不超过 10MB。"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """识别图片中的通用印刷体文字，返回可编辑文本、文字框坐标和置信度。
本期支持简体中文和英文通用场景识别。"""
        try:
            result = client.call(api_name="image_ocr", image_url=image_url, callback_args=callback_args, client_token=client_token)
            return sync_result_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="erase_image", description="自动检测并擦除图片中的常见图标、文字或指定区域内容，并对擦除区域进行背景智能填充。")
    async def erase_image(
        image_url: str = Field(..., description="输入图片 URL，需为公网可访问的 png/jpg/jpeg/webp/tiff/bmp/heic 图片，单图不超过 10MB。"),
        tool_version: Optional[str] = Field('standard', description="图像擦除修复选用的模型版本。- standard：标准版。基于明确的规则（如文本匹配、矩形框坐标）擦除指定内容。适用于简单、明确的擦除任务。默认 standard。"),
        standard_scene: Optional[str] = Field('full_screen_text_erase', description="标准版擦除场景，仅 standard 版本生效。full_screen_text_erase：全屏文字擦除，可通过standard_erase_text字段指定要擦除的文字，不指定则默认擦除所有文字内容。full_screen_icon_erase：全屏图标擦除。"),
        standard_erase_text: Optional[str] = Field(None, description="标准版文字擦除，指定要擦除的文字，不指定则默认擦除所有文字内容。"),
        output_format: Optional[str] = Field('webp', description="输出图片格式；默认 webp。"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """自动检测并擦除图片中的常见图标、文字或指定区域内容，并对擦除区域进行背景智能填充。"""
        try:
            result = client.call(api_name="erase_image", image_url=image_url, tool_version=tool_version, standard_scene=standard_scene, standard_erase_text=standard_erase_text, output_format=output_format, callback_args=callback_args, client_token=client_token)
            return sync_result_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="remove_image_background", description="自动识别并保留图像主体，移除背景并生成透明背景图片。\n支持通用、人像、商品场景，可在人像/商品场景中生成主体描边或裁剪透明背景。")
    async def remove_image_background(
        image_url: str = Field(..., description="输入图片 URL，需为公网可访问的 png/jpg/jpeg/webp/tiff/bmp/ico 图片，单图不超过 10MB。"),
        scene: str = Field(..., description="背景移除场景：general 为通用场景，适用于期望抠出图像主体但不确定该主体所属分类的场景。human 为人像抠图场景，适用于仅需抠出图像中的人像主体的场景，product 为商品抠图场景，适用于仅需抠出图像中的商品主体的场景。"),
        need_contour: Optional[bool] = Field(False, description="是否为主体生成描边；默认 false，仅 human/product 场景生效，general 场景忽略。"),
        contour_color: Optional[str] = Field('#FFFFFF', description="主体描边颜色，十六进制 RGB；默认 #FFFFFF，仅 need_contour=true 且 human/product 场景生效。"),
        contour_size: Optional[int] = Field(10, description="主体描边宽度，单位 px；默认 10，仅 need_contour=true 且 human/product 场景生效。"),
        need_crop_background: Optional[bool] = Field(False, description="是否裁剪透明背景到刚好包住主体；默认 false，仅 human/product 场景生效，general 场景忽略。"),
        output_format: Optional[str] = Field('png', description="输出图片格式；默认 png。"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """自动识别并保留图像主体，移除背景并生成透明背景图片。
支持通用、人像、商品场景，可在人像/商品场景中生成主体描边或裁剪透明背景。"""
        try:
            result = client.call(api_name="remove_image_background", image_url=image_url, scene=scene, need_contour=need_contour, contour_color=contour_color, contour_size=contour_size, need_crop_background=need_crop_background, output_format=output_format, callback_args=callback_args, client_token=client_token)
            return sync_result_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="enhance_image", description="基于图像内容理解智能决策，全方位提升图片分辨率、清晰度与色彩表现。")
    async def enhance_image(
        image_url: str = Field(..., description="输入图片。String 类型，支持http://xxx或https://xxx格式 URL"),
        tool_version: Optional[str] = Field('standard', description="画质增强选用的模型版本，标准版:standard；专业版：professional。默认为标准版"),
        multiple: Optional[float] = Field(None, description="图像处理后较原图的分辨率倍数，支持 2 位小数。取值最大不超过 30，取值范围[1,30]。注意：图像处理后的宽度和高度不能超过target_width、target_height的上限值。standard模式下，取值最大不超过 8。"),
        target_width: Optional[int] = Field(None, description="图像处理后的宽度，单位为 px，取值不能超过 10240。注意：standard模式下，取值最大不超过 6144，且图像处理后较原图的分辨率倍数不能超过 8。"),
        target_height: Optional[int] = Field(None, description="图像处理后的高度，单位为 px，取值不能超过 10240。注意：standard模式下，取值最大不超过 6144，且图像处理后较原图的分辨率倍数不能超过 8。"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """基于图像内容理解智能决策，全方位提升图片分辨率、清晰度与色彩表现。"""
        try:
            result = client.call(api_name="enhance_image", image_url=image_url, tool_version=tool_version, multiple=multiple, target_width=target_width, target_height=target_height, callback_args=callback_args, client_token=client_token)
            return sync_result_response(result)
        except Exception as exc:
            return error_response(str(exc))

    @mcp.tool(name="evaluate_image_quality", description="对输入图片进行主客观画质和美学评分，适用于质量监控、低质图筛查、内容审核、推荐排序和训练数据清洗等场景。\n支持标准版多维评分与专业版大模型评分。")
    async def evaluate_image_quality(
        image_url: str = Field(..., description="输入图片 URL，需为公网可访问的 png/jpeg/webp/heic 图片，单图不超过 10MB。"),
        tool_version: Optional[str] = Field('standard', description="画质评估模型版本，standard 为标准版，professional 为专业版；默认 standard。"),
        standard_evaluate_items: Optional[List[str]] = Field(['vqscore', 'noise', 'aesthetic', 'blur'], description="标准版选用的评估工具\n子项说明：评估工具。"),
        callback_args: Optional[str] = Field(None, description="可选，回调参数"),
        client_token: Optional[str] = Field(None, description="可选，用于幂等，默认幂等，用户可根据需求进行调整"),
        *,
        ctx: Context,
    ) -> dict:
        """对输入图片进行主客观画质和美学评分，适用于质量监控、低质图筛查、内容审核、推荐排序和训练数据清洗等场景。
支持标准版多维评分与专业版大模型评分。"""
        try:
            result = client.call(api_name="evaluate_image_quality", image_url=image_url, tool_version=tool_version, standard_evaluate_items=standard_evaluate_items, callback_args=callback_args, client_token=client_token)
            return sync_result_response(result)
        except Exception as exc:
            return error_response(str(exc))

    if hasattr(mcp, "register_domain_tools"):
        mcp.register_domain_tools("image", TOOL_NAMES)
