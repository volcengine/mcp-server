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

### Tool 18 flip_video

#### 功能描述

视频上下翻转、左右翻转能力，支持 vid、http url、directurl 三种模式输入

#### 最容易被唤起的 Prompt 示例

把视频上下翻转和左右翻转，视频为 vid1 空间 为 space1

### Tool 19 speedup_video

#### 功能描述

视频倍速能力，支持 vid、http url、directurl 三种模式输入

#### 最容易被唤起的 Prompt 示例

把视频 vid1 进行调整至 2 倍速， 空间 为 space1

### Tool 20 speedup_audio

#### 功能描述

音频倍速能力，支持 vid、http url、directurl 三种模式输入

#### 最容易被唤起的 Prompt 示例

把音频 vid1 进行调整至 2 倍速， 空间 为 space1

### Tool 21 image_to_video

#### 功能描述

图片转视频能力，支持 vid、http url、directurl 三种模式输入

#### 最容易被唤起的 Prompt 示例

对图片进行渐变放大，并增加随机转场， 图片资源为 vid1， vid2、vid3， 空间 为 space1

### Tool 22 compile_video_audio

#### 功能描述

音视频合成能力，支持擦除原视频流中的音频、对齐音频和视频时长等能力

#### 最容易被唤起的 Prompt 示例

进行音视频合并 ，擦除视频原始音效，以视频时长为准，视频为 vid1， 音频为 vid2， 空间 为 space1

### Tool 23 extract_audio

#### 功能描述

视频提取音频能力，支持设置音频输出格式

#### 最容易被唤起的 Prompt 示例

提取音频，音频为 vid1， 空间 为 space1

### Tool 24 mix_audios

#### 功能描述

音频叠加能力，常用场景为音频添加背景音乐

#### 最容易被唤起的 Prompt 示例

帮我进行音频合并操作 vid1， vid2 空间 为 space1

### Tool 25 add_subtitle

#### 功能描述

视频添加字幕能力，通常流程：大模型生成旁白，使用配音能力生成语音+字幕；再合成到视频中。

#### 最容易被唤起的 Prompt 示例

为视频 vid1 增加字幕 `https:****.srt` ，描边的颜色 为 红色，字体大小为 70，描边宽度为 10 ，描边的颜色 为 红色，字体大小为 70，描边宽度为 10 空间 为 space1

### Tool 26 add_sub_video

#### 功能描述

视频画中画、视频添加图片、视频水印能力

#### 最容易被唤起的 Prompt 示例

进行水印贴片，主视频为 vid1 ， 贴片视频为 vid2；贴片位于右上角，贴片宽高为 100\* 100。 空间 为 space1

### Tool 27 get_video_audio_info

#### 功能描述

视频元信息获取能力

#### 最容易被唤起的 Prompt 示例

帮我获取 vid1 的播放信息， 空间 为 space1

### Tool 28 get_play_url

#### 功能描述

音视频播放链接获取

#### 最容易被唤起的 Prompt 示例

帮我获取 vid1 的播放链接， 空间 为 space1

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
        "VOLCENGINE_SECRET_KEY": "Your Volcengine SK",
         "MCP_TOOLS_TYPE": "Your Source" // groups ｜ tools
         // - groups 模式下 为  MCP_TOOLS_SOURCE 值需要输入分组值;
         //  - tools： 模式下 MCP_TOOLS_SOURCE 值为 tool.name
        "MCP_TOOLS_SOURCE": "Your Source",

      }
    }
  }
}
```

### 云部署

** 支持动态鉴权以及分组，header 信息如下 **

- 全选设置为
  - x-tt-tools-type： groups
  - x-tt-tools-source： all
- 本期支持了可以通过配置 x-tt-tools-source 来动态切换 mcp tool，可以针对场景化智能体，减少不必要的干扰以及 token 消耗
- x-tt-tools-type： 动态加载类型的模式，支持： groups ｜ tools 两种
- groups 模式下 为 x-tt-tools-source 值需要输入分组值 、 all 为 全部设置
- tools： 模式下 x-tt-tools-source 值为 tool.name

### 分组信息

** 默认输出内容为 **

- get_play_url: 获取播放链接
- audio_video_stitching： 音视频拼接
- audio_video_clipping： 音视频剪切
- get_v_creative_task_result： 查询剪辑结果

** 详细分组信息如下： **

```json
{
    # edit 分组
    "edit": [ #分组名称
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
```

## License

MIT
