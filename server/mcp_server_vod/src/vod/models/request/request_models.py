from pydantic import BaseModel, Field
from typing import Optional, Literal

class BatchUploadUrlItem(BaseModel):
    SourceUrl: str
    FileExtension: str = Field(description="文件后缀，即点播存储中文件的类型,-必须以 . 开头，不超过 8 位。;当您传入 FileExtension 时,视频点播将生成 32 位随机字符串，和您传入的 FileExtension 共同拼接成文件路径")

class InputSource(BaseModel):
    type: Optional[Literal["directurl", "http", "vid"]] = Field(description="文件类型，vid、directurl、http")
    source: str = Field(description="文件信息")


class addSubVideoOptions(BaseModel):
    height: Optional[str] = Field(description="水印的高度，支持设置为百分比（相对于视频高度）或具体像素值，例如 100% 或 100")
    width: Optional[str] = Field(description="水印的宽度，支持设置为百分比（相对于视频高度）或具体像素值，String 类型，例如 100% 或 100")
    pos_x: Optional[str] = Field(description="水印在水平方向（X 轴）的位置，以视频左上角为原点，单位：像素。例如值为 0 时，表示水印处于水平方向的最左侧；值为 100 时，表示水印相对原点向右移动 100 像素")
    pos_y: Optional[str] = Field(description="水印在垂直方向（Y 轴）的位置，以视频左上角为原点，单位：像素，例如值为 0 时，表示水印在垂直方向的最上侧；值为 100 时，表示水印相对原点向下移动 100 像素")
    start_time: Optional[float] = Field(description="水印的开始时间，单位：秒")
    end_time: Optional[float] = Field(description="水印的结束时间，单位：秒")
