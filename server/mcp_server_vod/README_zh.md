# VOD MCP Server

一款高效便捷的视频剪辑小助手，通过对话交互的方式，实现了多视频时域拼接、长视频分段截取与拼接、添加转场动画等剪辑操作，降低了视频剪辑的技术门槛和操作成本

| 版本 | v1.0.0                    |
| ---- | ------------------------- |
| 描述 | 火山引擎 VOD 智能剪辑助手 |
| 分类 | 视频云，视频点播          |
| 标签 | 点播，视频点播，视频剪辑  |

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: audio_video_stitching

#### 功能描述

将多个音视频拼接为一个新音视频，支持 vid、url、directurl 三种输入方式

#### 最容易被唤起的 Prompt 示例

把 vid1、vid2、视频进行拼接，空间为 space1

### Tool 2: audio_video_clipping

#### 功能描述

将音视频按照指定起止时间截取，输出一个新音视频，支持 vid、url、directurl 三种输入方式

#### 最容易被唤起的 Prompt 示例

把 vid1、vid2 视频截取 第 1s 到 第 30s 时间点的内容，空间为 space1

### Tool 3: get_v_creative_task_result

#### 功能描述

查询视频创作任务结果，获取视频创作任务的处理结果，包括任务状态、处理进度、处理结果等信息。

#### 最容易被唤起的 Prompt 示例

查询 VCreativeId 视频创作任务的处理结果，空间为 space1

### Tool 4 video_batch_upload

#### 功能描述

通过源文件 URL 批量拉取媒资并上传至视频点播

#### 最容易被唤起的 Prompt 示例

把文件 url1、url2 上传到 空间为 your space ，文件后缀为 .mp4

### Tool 5 query_batch_upload_task_info

#### 功能描述

查询 URL 批量上传任务状态。

#### 最容易被唤起的 Prompt 示例

查询上传任务状态 JobId 为 xxx

### Tool 6 video_quality_enhancement_task

#### 功能描述

视频增强，支持 Vid 和 DirectUrl 两种输入模式。

#### 最容易被唤起的 Prompt 示例

把视频 vid1 进行增强 ，空间为 space1

### Tool 7 video_super_resolution_task

#### 功能描述

视频超分，支持 Vid 和 DirectUrl 两种输入模式。

#### 最容易被唤起的 Prompt 示例

把视频 vid1 进行超分 ，空间为 space1

### Tool 8 video_interlacing_task

#### 功能描述

视频插帧，支持 Vid 和 DirectUrl 两种输入模式。

#### 最容易被唤起的 Prompt 示例

把视频 vid1 进行插帧 ，空间为 space1

### Tool 9 audio\_ noise_reduction_task

#### 功能描述

音频去噪，支持 Vid 和 DirectUrl 两种输入模式。

#### 最容易被唤起的 Prompt 示例

把音频 vid1 进行去噪 ，空间为 space1

### Tool 10 asr_speech_to_text_task

#### 功能描述

ASR 语音转写字幕，支持 Vid 和 DirectUrl 两种输入模式。

#### 最容易被唤起的 Prompt 示例

把视频 vid1 进行 ASR 识别处理，空间为 space1

### Tool 11 ocr_text_to_subtitles_task

#### 功能描述

OCR 文字转字幕，支持 Vid 和 DirectUrl 两种输入模式。

#### 最容易被唤起的 Prompt 示例

把视频 vid1 进行 OCR 识别处理，空间为 space1

### Tool 12 video_subtitles_removal_task

#### 功能描述

视频字幕擦除，支持 Vid 和 DirectUrl 两种输入模式。

#### 最容易被唤起的 Prompt 示例

把视频 vid1 进行字幕擦除处理，空间为 space1

### Tool 13 voice_separation_task

#### 功能描述

视频人声分离，支持 Vid 和 DirectUrl 两种输入模式。

#### 最容易被唤起的 Prompt 示例

把视频 vid1 进行人声分离处理，空间为 space1

### Tool 14 intelligent_slicing_task

#### 功能描述

智能切片，支持 Vid 和 DirectUrl 两种输入模式。

#### 最容易被唤起的 Prompt 示例

把视频 vid1 进行智能分段切片处理，空间为 space1

### Tool 15 green_screen_task

#### 功能描述

绿幕抠图，支持 Vid 和 DirectUrl 两种输入模式。

#### 最容易被唤起的 Prompt 示例

把视频 vid1 进行绿幕抠图处理，空间为 space1

### Tool 16 portrait_image_retouching_task

#### 功能描述

人像抠图，支持 Vid 和 DirectUrl 两种输入模式。

#### 最容易被唤起的 Prompt 示例

把视频 vid1 进行人像抠图处理，空间为 space1

### Tool 17 get_media_execution_task_result

#### 功能描述

查询视频处理任务结果，获取视频处理任务的处理结果，包括任务状态、处理进度、处理结果等信息。

#### 最容易被唤起的 Prompt 示例

查询人像抠图任务的视频处理任务的处理结果，runId 为 xxx，空间为 space1

## 可适配平台

方舟，Cursor，Trae 等

## 服务开通链接 (整体产品)

[火山引擎-视频点播-控制台](https://www.volcengine.com/product/vod)

## 鉴权方式

请在[火山引擎-视频点播-控制台](https://www.volcengine.com/product/vod)申请 VOLCENGINE_ACCESS_KEY、VOLCENGINE_SECRET_KEY

## 安装

### 环境要求

- Python 3.13+
- 火山引擎账号及 AccessKey/SecretKey

## 部署

### 在 MCP Client 中集成

在 mcp client 中配置 mcp 服务, 配置的 MCP JSON：

```json
{
  "mcpServers": {
    "vevod": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_vod",
        "mcp-server-vod"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "Your Volcengine AK",
        "VOLCENGINE_SECRET_KEY": "Your Volcengine SK"
      }
    }
  }
}
```

## License

MIT
