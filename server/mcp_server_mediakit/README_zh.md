# MediaKit MCP Server

MediaKit MCP 是火山引擎 AI MediaKit 面向 AI 时代推出的标准能力插件。它基于 MCP（Model Context Protocol）协议，将云端专业的视频剪辑、音频处理、字幕处理、画质增强等原子能力封装为智能体可直观调用的工具。通过 MediaKit MCP，开发者可直接以自然语言驱动 AI 智能体完成复杂的云端媒体处理任务。

| 字段 | 取值 |
| --- | --- |
| 版本 | v1.0.0 |
| 描述 | MediaKit MCP 智能媒体助手 |
| 分类 | 视频云、音视频编辑、画质增强 |
| 标签 | MCP、MediaKit、视频剪辑、音频处理、画质增强 |

## 工具概览

MediaKit MCP 已开放的能力覆盖了从异步任务查询到深度媒体编辑、视频增强的全流程。所有工具均支持通过“分组（Group）”或“工具名”进行动态加载，以优化智能体的推理效率。

<table>
  <thead>
    <tr>
      <th>分类</th>
      <th>分组名称</th>
      <th>工具</th>
      <th>说明</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>通用能力</b></td>
      <td>shared</td>
      <td>query_task</td>
      <td><b>任务查询</b>：查询异步任务状态和结果。提交异步任务后，使用该工具获取处理进度和最终产物。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/shared.py#L33">query_task</a>。
      </td>
    </tr>
    <tr>
      <td rowspan="11"><b>视频剪辑</b></td>
      <td rowspan="11">editing</td>
      <td>add_image_to_video</td>
      <td><b>视频加图片</b>：在视频画面上叠加图片，常用于添加图片水印。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L30">add_image_to_video</a>。
      </td>
    </tr>
    <tr>
      <td>add_subtitle_to_video</td>
      <td><b>视频加字幕</b>：将字幕文件或字幕文本压制到视频画面中。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L52">add_subtitle_to_video</a>。
      </td>
    </tr>
    <tr>
      <td>adjust_video_speed</td>
      <td><b>视频播放调速</b>：调整视频播放速度，实现快放或慢放效果。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L73">adjust_video_speed</a>。
      </td>
    </tr>
    <tr>
      <td>concat_audio</td>
      <td><b>音频拼接</b>：将多个音频片段拼接为一个新的音频文件。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L89">concat_audio</a>。
      </td>
    </tr>
    <tr>
      <td>concat_video</td>
      <td><b>视频拼接</b>：将多个视频片段拼接为一个新视频，支持添加转场效果。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L104">concat_video</a>。
      </td>
    </tr>
    <tr>
      <td>extract_audio</td>
      <td><b>音频提取</b>：从视频文件中分离音频流，并保存为独立音频文件。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L120">extract_audio</a>。
      </td>
    </tr>
    <tr>
      <td>flip_video</td>
      <td><b>画面翻转</b>：对视频画面进行水平或垂直镜像翻转。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L136">flip_video</a>。
      </td>
    </tr>
    <tr>
      <td>image_to_video</td>
      <td><b>图片合成视频</b>：将多张图片合成为动画视频，支持转场效果。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L153">image_to_video</a>。
      </td>
    </tr>
    <tr>
      <td>mux_audio_video</td>
      <td><b>音画合成</b>：将视频轨道与音频轨道合成一个视频文件。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L169">mux_audio_video</a>。
      </td>
    </tr>
    <tr>
      <td>trim_audio</td>
      <td><b>音频裁剪</b>：按起止时间点裁剪音频，生成新的音频片段。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L189">trim_audio</a>。
      </td>
    </tr>
    <tr>
      <td>trim_video</td>
      <td><b>视频裁剪</b>：按起止时间点裁剪视频，生成新的视频片段。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L206">trim_video</a>。
      </td>
    </tr>
    <tr>
      <td rowspan="2"><b>视频增强</b></td>
      <td rowspan="2">video</td>
      <td>erase_video_subtitle_pro</td>
      <td><b>视频字幕擦除</b>：针对视频中的字幕或文本进行高质量无痕擦除。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/video.py#L30">erase_video_subtitle_pro</a>。
      </td>
    </tr>
    <tr>
      <td>enhance_video</td>
      <td><b>画质增强</b>：面向 AIGC、UGC、短剧、教育、游戏、老片修复等场景提升视频画质。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/video.py#L49">enhance_video</a>。
      </td>
    </tr>
  </tbody>
</table>

## 配置说明

| 变量 | 说明 | 是否必填 |
| --- | --- | --- |
| `MEDIAKIT_API_KEY` | MediaKit API Key，用于请求鉴权。 | 是 |
| `MEDIAKIT_ENDPOINT` | MediaKit API Endpoint，默认 `https://amk.cn-beijing.volces.com`。 | 否 |
| `MCP_DOMAINS` | 工具分组白名单，多个分组用英文逗号分隔，例如 `editing,video`。 | 否 |
| `MCP_TOOLS` | 工具名白名单，多个工具用英文逗号分隔，例如 `trim_video,query_task`。 | 否 |

## 快速开始

安装 MCP Server：

```bash
pip install mcp-server-mediakit
```

配置 MediaKit API Key：

```bash
export MEDIAKIT_API_KEY="your-api-key"
```

以 stdio 模式启动：

```bash
mcp-server-mediakit --transport stdio
```

以 Streamable HTTP 模式启动：

```bash
mcp-server-mediakit --transport streamable-http
```

## 使用说明

- 同步任务会直接返回结果。
- 异步任务会返回 `task_id`，需要调用 `query_task` 查询任务状态和结果。
- 默认开启幂等：相同账户和核心请求参数在 2 天内重复提交时，服务会直接返回首次任务结果，不会重复创建任务。
- 如需主动控制幂等，可传 `client_token`；请求重试时复用同一值，强制重新执行时必须传新的唯一值。
- `client_token` 由客户端生成，长度不超过 64 个字符。

## 工具详情

### query_task

查询异步任务状态。支持单次查询，也支持通过 `poll_interval_seconds` 与 `max_poll_attempts` 控制轮询。

### add_image_to_video

在视频中添加图片覆盖层，可用于图片水印。支持配置图片宽高、水平位置、垂直位置、开始时间和结束时间。

### add_subtitle_to_video

将字幕文件或字幕文本压制到视频画面中。支持字幕位置、字体大小、字体颜色和字体类型配置。

### adjust_video_speed

调整视频播放速度，实现快放或慢放效果。支持 `0.1` 到 `4` 倍速。

### concat_audio

拼接多个音频片段，最多支持 100 个音频 URL。

### concat_video

拼接多个视频片段，最多支持 100 个视频 URL，并可配置转场效果。

### extract_audio

从视频中提取音频，支持输出 `mp3` 或 `m4a`。

### flip_video

对视频画面进行水平或垂直镜像翻转。

### image_to_video

将多张图片合成为动画视频，并支持配置转场效果。

### mux_audio_video

将视频与音频合成为一个视频文件。支持保留原视频音频，并支持按视频或音频基准进行时长对齐。

### trim_audio

按秒级起止时间裁剪音频文件。

### trim_video

按秒级起止时间裁剪视频文件。

### erase_video_subtitle_pro

针对视频中的字幕或文本进行高质量擦除，尽可能还原视频画面。支持 `mp4`、`flv`、`ts`、`avi`、`mov`、`wmv`、`mkv` 等主流视频格式。

### enhance_video

针对 `common`、`ugc`、`short_series`、`aigc`、`old_film` 等场景进行画质增强，支持标准版和专业版工具版本。
