# VOD MCP Server

VeVOD MCP 是火山引擎视频点播面向 AI 时代推出的标准能力插件。它基于 MCP (Model Context Protocol) 协议，将云端专业的视频编辑、画质增强、内容识别等原子能力封装为智能体可直观调用的工具。通过 VeVOD MCP，开发者可直接以自然语言驱动 AI 智能体完成复杂的云端视频处理任务。

<table>
  <thead>
    <tr>
      <th><nobr>字段</nobr></th>
      <th><nobr>取值</nobr></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap"><nobr>版本</nobr></td>
      <td>v1.0.0</td>
    </tr>
    <tr>
      <td style="white-space: nowrap"><nobr>描述</nobr></td>
      <td>火山引擎 VOD 智能剪辑助手</td>
    </tr>
    <tr>
      <td style="white-space: nowrap"><nobr>分类</nobr></td>
      <td>视频云，视频点播</td>
    </tr>
    <tr>
      <td style="white-space: nowrap"><nobr>标签</nobr></td>
      <td>点播，视频点播，视频剪辑</td>
    </tr>
  </tbody>
</table>

## 工具概览

VeVOD MCP 已开放的能力覆盖了从素材上传、内容理解到深度剪辑的全流程。所有工具均支持通过“分组（Group）”进行动态加载，以优化智能体的推理效率。

<table>
  <thead>
    <tr>
      <th>分⁠类⁠</th>
      <th><nobr>分组名称</nobr></th>
      <th><nobr>工具</nobr></th>
      <th><nobr>说明</nobr></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>基⁠础⁠功⁠能⁠</b></td>
      <td>upload</td>
      <td>video_batch_upload</td>
      <td><b>文件上传</b>：支持从公网 URL 批量拉取音视频、图片等文件上传至点播空间，并可查询上传任务状态。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/upload.py#L9">video_batch_upload</a>。
      </td>
    </tr>
    <tr>
      <td rowspan="10"><b>视⁠频⁠剪⁠辑⁠</b></td>
      <td rowspan="10">edit</td>
      <td>audio_video_stitching</td>
      <td><b>多片段拼接</b>：将多个视频或音频片段按指定顺序拼接成一个新文件，支持在片段间添加多种转场效果。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/edit.py#L36">audio_video_stitching</a>。
      </td>
    </tr>
    <tr>
      <td>audio_video_clipping</td>
      <td><b>片段裁剪</b>：按起止时间点（秒级）裁剪视频或音频，生成新片段。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/edit.py#L169">audio_video_clipping</a>。
      </td>
    </tr>
    <tr>
      <td>flip_video</td>
      <td><b>画面翻转</b>：对视频画面进行水平或垂直镜像翻转。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/edit.py#L381">flip_video</a>。
      </td>
    </tr>
    <tr>
      <td>speedup_video</td>
      <td><b>视频播放调速</b>：调整视频的播放速率，实现快放或慢放效果。支持调整为 0.1～4 倍。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/edit.py#L445">speedup_video</a>。
      </td>
    </tr>
    <tr>
      <td>speedup_audio</td>
      <td><b>音频播放调速</b>：调整音频文件的播放速率，实现快放或慢放效果。支持调整为 0.1～4 倍。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/edit.py#L513">speedup_audio</a>。
      </td>
    </tr>
    <tr>
      <td>image_to_video</td>
      <td><b>图片合成视频</b>：将单张或多张图片合成为一个视频文件，支持为每张图片自定义显示时长和转场效果。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/edit.py#L582">image_to_video</a>。
      </td>
    </tr>
    <tr>
      <td>compile_video_audio</td>
      <td><b>音画合成</b>：将独立的视频轨道和音频轨道叠加，合成为一个视频文件。可用于为视频添加或替换音轨。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/edit.py#L705">compile_video_audio</a>。
      </td>
    </tr>
    <tr>
      <td>extract_audio</td>
      <td><b>提取音轨</b>：从视频文件中无损分离并提取出独立的音频轨道，生成一个音频文件。支持指定输出音频的格式为 mp3 或 m4a。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/edit.py#L813">extract_audio</a>。
      </td>
    </tr>
    <tr>
      <td>mix_audios</td>
      <td><b>音频混音</b>：将多个音频文件（如背景音乐、音效、人声）进行混音，生成一个新的音频文件。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/edit.py#L878">mix_audios</a>。
      </td>
    </tr>
    <tr>
      <td>add_sub_video</td>
      <td><b>视频叠加（画中画）</b>：将一个子视频或图片素材叠加到主视频上，实现画中画、视频水印、图片水印等效果。支持自定义叠加元素的位置、尺寸及显示时段。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/edit.py#L958">add_sub_video</a>。
      </td>
    </tr>
    <tr>
      <td rowspan="3"><b>视⁠频⁠增⁠强⁠</b></td>
      <td rowspan="3">video_enhancement</td>
      <td>video_quality_enhancement_task</td>
      <td><b>综合画质修复</b>：通过 AI 综合修复视频画质，消除压缩痕迹、噪点、划痕等常见损伤，提升整体清晰度和色彩表现。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/video_enhancement.py#L9">video_quality_enhancement_task</a>。
      </td>
    </tr>
    <tr>
      <td>video_super_resolution_task</td>
      <td><b>AI 超分</b>：通过 AI 算法智能提升视频分辨率，例如将 720P 视频放大至 1080P，并锐化增强画面细节。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/video_enhancement.py#L49">video_super_resolution_task</a>。
      </td>
    </tr>
    <tr>
      <td>video_interlacing_task</td>
      <td><b>智能插帧</b>：通过运动补偿算法，将低帧率视频（如 30fps）智能插帧至高帧率（如 60fps），使运动画面更平滑流畅。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/video_enhancement.py#L119">video_interlacing_task</a>。
      </td>
    </tr>
    <tr>
      <td rowspan="4"><b>字⁠幕⁠处⁠理⁠</b></td>
      <td rowspan="4">subtitle_processing</td>
      <td>asr_speech_to_text_task</td>
      <td><b>语音转字幕 (ASR)</b>：通过 ASR 技术，将视频中的语音内容转换成带时间轴的字幕信息。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/subtitle_processing.py#L11">asr_speech_to_text_task</a>。
      </td>
    </tr>
    <tr>
      <td>ocr_text_to_subtitles_task</td>
      <td><b>画面文字提取 (OCR)</b>：通过 OCR 技术，智能提取视频画面中内嵌的文字。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/subtitle_processing.py#L66">ocr_text_to_subtitles_task</a>。
      </td>
    </tr>
    <tr>
      <td>video_subtitles_removal_task</td>
      <td><b>硬字幕擦除</b>：智能检测并无痕擦除视频画面中已有的硬字幕，保留原始背景。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/subtitle_processing.py#L91">video_subtitles_removal_task</a>。
      </td>
    </tr>
    <tr>
      <td>add_subtitle</td>
      <td><b>添加内嵌字幕</b>：将外部字幕文件（如 SRT 格式）以指定样式压制到视频画面中，生成带内嵌字幕的新视频。支持自定义字体、字幕样式以及字幕位置。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/subtitle_processing.py#L126">add_subtitle</a>。
      </td>
    </tr>
    <tr>
      <td rowspan="2"><b>音⁠频⁠处⁠理⁠</b></td>
      <td rowspan="2">audio_processing</td>
      <td>voice_separation_task</td>
      <td><b>人声/伴奏分离</b>：将音频中的人声与背景音乐精准分离，输出为两个独立的音轨文件。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/audio_processing.py#L38">voice_separation_task</a>。
      </td>
    </tr>
    <tr>
      <td>audio_noise_reduction_task</td>
      <td><b>音频降噪</b>：智能识别并消除音频中的环境噪音、电流声、风声等多种杂音，提升人声的清晰度。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/audio_processing.py#L8">audio_noise_reduction_task</a>。
      </td>
    </tr>
    <tr>
      <td><b>智⁠能⁠切⁠片⁠</b></td>
      <td>intelligent_slicing</td>
      <td>intelligent_slicing_task</td>
      <td><b>智能场景切分</b>：基于画面转场、镜头切换，智能地将长视频切分成多个有逻辑关联的短片段。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/intelligent_slicing.py">intelligent_slicing_task</a>。
      </td>
    </tr>
    <tr>
      <td rowspan="2"><b>智⁠能⁠抠⁠图⁠</b></td>
      <td rowspan="2">intelligent_matting</td>
      <td>portrait_image_retouching_task</td>
      <td><b>人像抠图</b>：自动识别视频中的主体人像并进行高精度抠图，生成带透明通道的视频素材。支持指定输出视频的封装格式为 MOV 或 WEBM。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/intelligent_matting.py#L52">portrait_image_retouching_task</a>。
      </td>
    </tr>
    <tr>
      <td>green_screen_task</td>
      <td><b>绿幕抠图</b>：对以绿幕为背景的视频进行专业级抠图，常用于影视后期与特效合成。支持指定输出视频的封装格式为 MOV 或 WEBM。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/intelligent_matting.py#L8">green_screen_task</a>。
      </td>
    </tr>
    <tr>
      <td><b>任⁠务⁠管⁠理⁠</b></td>
      <td>media_tasks</td>
      <td>get_media_execution_task_result</td>
      <td><b>异步任务查询</b>：通过任务 ID 查询并获取异步媒体处理任务的执行状态和最终产物信息（如新文件 Vid、URL 等）。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/media_tasks.py#L8">get_media_execution_task_result</a>。
      </td>
    </tr>
    <tr>
      <td rowspan="2"><b>媒⁠体⁠分⁠发⁠</b></td>
      <td rowspan="2">video_play</td>
      <td>get_play_url</td>
      <td><b>获取播放地址</b>：根据 Vid 或文件名，获取指定视频的多种清晰度、格式的播放地址。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/video_play.py#L315">get_play_url</a>。
      </td>
    </tr>
    <tr>
      <td>get_video_audio_info</td>
      <td><b>获取音视频元信息</b>：获取指定音视频的详细元数据，如时长、码率、分辨率、编码格式、帧率等。详细输入和输出参数请见
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/video_play.py#L342">get_video_audio_info</a>。
      </td>
    </tr>
  </tbody>
</table>

## 典型应用场景

您可以灵活组合 VeVOD MCP 提供的原子能力，以支持多样化的 AI 视频创作与处理场景。以下是一些典型的应用示例：

### AI 漫剧生成

将漫画或小说素材快速转化为动态视频。MCP 可根据指令，自动完成素材组合、配音、字幕添加等一系列繁琐的后期工作。核心环节：

- **画面合成**：使用 `image_to_video` 将多张漫画图片合成为视频，或使用 `audio_video_stitching` 拼接已有视频片段。
- **音轨处理**：使用 `extract_audio` 提取原声，再使用 `mix_audios` 叠加上新的配音或背景音乐。
- **字幕生成**：通过 `asr_speech_to_text_task` 将配音转换为字幕，再使用 `add_subtitle` 将其压制到视频中。
- **画质增强**：最后，可选用 `video_super_resolution_task` 提升输出视频的整体分辨率和清晰度。

### 爆款营销视频制作

在电商、广告等场景中，可将 AI 生成的商品图、用户素材或产品演示片段，通过自然语言指令快速组合生成抓人眼球的营销短视频。核心环节：

- **片段剪辑**：使用 `audio_video_clipping` 从长视频中截取高光片段。
- **拼接合成**：使用 `image_to_video` 将多张商品图合成为视频，或使用 `audio_video_stitching` 拼接已有视频片段，并添加背景音乐。
- **添加营销信息**：通过 `add_subtitle` 功能为视频添加引人注目的标题、卖点介绍或活动信息。

### 教育视频制作

在 K12、知识付费等领域，将图文课件、古诗词、绘本故事等内容自动化生成为生动有趣的教学视频。核心环节：

- **课程内容合成**：使用 `image_to_video` 将教学 PPT 或绘本图片转换为视频。同时，可调用 `audio_video_stitching` 将多个视频片段拼接起来，并添加转场效果，形成连贯的教学内容。
- **添加旁白**：调用 `audio_video_stitching` 为视频添加预先录制好的课程讲解或故事朗读。
- **添加字幕**：使用 `asr_speech_to_text_task` 和 `add_subtitle` 生成和添加同步字幕。

## 计费说明

VeVOD MCP 本身作为开源工具及协议层插件不收取额外费用。但在通过 MCP 驱动视频处理的过程中，会调用火山引擎视频点播后端的各项资源。在使用过程中，产生的费用主要由以下三部分组成：

- **媒资存储费用**：所有通过 MCP 上传的原始素材，以及处理后生成的成品视频，均存储在您的视频点播空间中，根据存储文件的占用空间（GB）按日计费。详见[媒资存储计费](/ol8o3qyn/76542)。
- **视频处理费用**： 这是费用的核心部分，根据您驱动 MCP 执行的任务类型有所不同：
  - **云剪辑**：根据输出视频的分辨率和时长计费，详见[视频剪辑计费](/ol8o3qyn/mvybepnu)。
  - **单任务处理**：视频超分、插帧、语音转写等 AI 任务将根据任务的处理规格及时长独立计费，详见[媒体处理计费](/ol8o3qyn/73msxgdi)。
- **流量费用**：当您通过 MCP 返回的播放地址观看或分发视频时，会产生下行流量。
  - 若您在视频点播中[配置加速域名](https://www.volcengine.com/docs/4/177122)，会产生[分发加速计费](/ol8o3qyn/u5kijik1)。
  - 若您未在视频点播中配置加速域名，则会产生[存储流出](/ol8o3qyn/76542)费用。

# 快速体验：在 Trae 中配置

Trae 是一款 AI 原生 IDE，提供了强大的智能体协作能力。通过接入 VeVOD MCP，您可以直接在 Trae 对话框中以 Vibe Coding 的方式，仅需 10 分钟即可完成首个 AI 视频剪辑任务，无需编写任何代码。

## 前提条件

- 已[注册火山引擎账号](https://www.volcengine.com/docs/6261/64925)并完成[实名认证](https://www.volcengine.com/docs/6261/64935)。
- 已获取[火山引擎 Access Key/Secret Key](https://www.volcengine.com/docs/6257/64983?lang=zh)（简称 AK/SK）。
- 已[开通视频点播服务](https://console.volcengine.com/vod/overview/)并[创建空间](https://www.volcengine.com/docs/4/65669)。
- （推荐）将待处理的视频素材[上传](https://www.volcengine.com/docs/4/65670?lang=zh)至点播空间，或准备好公网可访问的视频 URL。
- （可选）准备开发环境：
  - 安装 [Trae 客户端](https://www.trae.com.cn/?utm_source=volcengine&utm_medium=mcp-marketplace)。
  - 通过 `uvx --version` 命令检查您的开发环境中是否已安装 uvx。若显示 `uvx: command not found`，则参考[官方文档](https://docs.astral.sh/uv/getting-started/installation/)安装 uvx。

## 操作步骤

### 步骤 1：选择接入模式

根据您的需求选择以下两种接入模式之一：

<table>
  <thead>
    <tr>
      <th><nobr>模式</nobr></th>
      <th><nobr>适用场景</nobr></th>
      <th><nobr>接入方式</nobr></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap"><nobr><b>本地模式 (JSON Local)</b></nobr></td>
      <td>个人快速调试、处理本地敏感文件、无需公网域名。</td>
      <td>通过 <code>uvx</code> 命令直接调用本地脚本运行。您可直接跳转至<a href="#步骤-2添加-mcp-配置">步骤 2：添加 MCP 配置</a>。</td>
    </tr>
    <tr>
      <td style="white-space: nowrap"><nobr><b>云端模式 (JSON URL)</b></nobr></td>
      <td>长期稳定使用、跨团队协作、无需本地安装环境。</td>
      <td>前往<a href="https://www.volcengine.com/mcp-marketplace/detail?name=VeVOD%20MCP">火山引擎 MCP 广场</a>，在 Trae 页签下，单击<b>云部署</b>生成专属长效 URL。复制该 URL 后，前往<a href="#步骤-2添加-mcp-配置">步骤 2：添加 MCP 配置</a>。<br>
      <img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/287e233f0fbd45ff89eb44db0b1d5db5~tplv-goo7wpa0wc-image.image" alt="云部署配置示意图" /><br>
      此方式需账户余额不少于 100 元，涉及 <a href="https://www.volcengine.com/docs/6569/185249?lang=zh">API 网关</a>及<a href="https://www.volcengine.com/docs/6662/1269135?lang=zh">函数服务</a>计费。</td>
    </tr>
  </tbody>
</table>

### 步骤 2：添加 MCP 配置

1. 打开 Trae，单击 Trae 窗口右上角"设置"按钮（齿轮图标）。
2. 在 MCP 页签下，单击**添加** > **手动添加**。
3. 根据您在步骤 1 选择的模式，复制对应的配置 JSON 并根据下方文字说明进行替换。请注意，为了确保初次调用的成功率，默认仅加载了最核心的工具分组。

<div type="doc-tabs">
<div type="tab-item" title="本地模式 (JSON Local)" key="WyIYIdP2Hj">

复制以下 JSON 并根据下方文字说明进行替换。Trae 会通过 `uvx` 自动拉取最新的远程代码并在本地运行。

```JSON
{
  "mcpServers": {
    "video_process_mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_vod",
        "mcp-server-vod"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "Your_AK",
        "VOLCENGINE_SECRET_KEY": "Your_SK",
        "MCP_TOOLS_TYPE": "groups",
        "MCP_TOOLS_SOURCE": "edit,video_play,media_tasks",
        "MCP_SPACE_NAME": "Your_Space_Name"
      }
    }
  }
}
```

字段替换说明：

- `video_process_mcp`：MCP 服务的名称，您可以根据需要自定义。
- `VOLCENGINE_ACCESS_KEY` 与 `VOLCENGINE_SECRET_KEY`：请替换为您在前提条件中获取的火山引擎 AK 和 SK。
- `MCP_TOOLS_TYPE`：加载模式，可选 `groups`（按分组）或 `tools`（按工具）。
- `MCP_TOOLS_SOURCE`：加载范围。您可以填入 all 加载全部工具，或填入如 edit,upload 这种以逗号分隔的分组/工具名。注意 Trae 限制单个 MCP 工具数上限为 10 个，建议仅加载必需的分组。
- `MCP_SPACE_NAME`：请替换为您在视频点播控制台创建的空间名称。

完整参数说明，请见[MCP 配置参数说明](#mcp-配置参数说明)。

</div>
<div type="tab-item" title="云端模式 (JSON URL)" key="hYNMuldBe6">

复制以下 JSON 并根据下方文字说明进行替换：

```JSON
{
  "mcpServers": {
    "video_process_mcp": {
      "url": "https://sd60n******dddprg.apigateway-cn-beijing.volceapi.com/mcp",
      "headers": {
        "x-tt-access-key": "Your_AK",
        "x-tt-secret-key": "Your_SK",
        "x-tt-tools-type": "groups",
        "x-tt-tools-source": "edit,video_play,media_tasks",
        "x-tt-space-name": "Your_Space_Name"
      }
    }
  }
}
```

字段替换说明：

- `video_process_mcp`：MCP 服务的名称，您可以根据需要自定义。
- `url`：请替换为您在步骤 1 中从 MCP 广场获取的专属 Endpoint。
- `x-tt-access-key` 与 `x-tt-secret-key`：请替换为您在前提条件中获取的火山引擎 AK 和 SK。
- `x-tt-tools-type`：加载模式，可选 `groups`（按分组）或 `tools`（按工具）。
- `x-tt-tools-source`：加载范围。您可以填入 all 加载全部工具，或填入如 edit,upload 这种以逗号分隔的分组/工具名。注意 Trae 限制单个 MCP 工具数上限为 10 个，建议仅加载必需的分组。
- `x-tt-space-name`：请替换为您在视频点播控制台创建的空间名称。

完整参数说明，请见[MCP 配置参数说明](#mcp-配置参数说明)。

</div>
</div>

4. 确认该 MCP 的状态显示为绿色激活，如下图所示。
   ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/8dce1bccd27742d3b1f357801af719fc~tplv-goo7wpa0wc-image.image)

### 步骤 3：启用智能体对话

在 Trae 主界面打开对话面板，将底部的智能体切换为 **Builder with MCP** 模式。
<img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/b38f1ab590d74168b898b974d7d9240f~tplv-goo7wpa0wc-image.image" alt="选择 Builder with MCP 模式示意图" />
您可以直接下达提示词，例如：帮我将 test 空间中的 beach.mp4 和 sunset.mp4 拼接在一起，中间加一个“淡入淡出”转场效果，完成后把播放地址发给我。

<table>
  <thead>
    <tr>
      <th><nobr>阶段</nobr></th>
      <th><nobr>内容</nobr></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap"><nobr><b>输入视频</b></nobr></td>
      <td>
        <img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/1814f820a644484486417c3a40ce8ac3~tplv-goo7wpa0wc-image.image" alt="输入视频1" />
        <br />
        <img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/9add04fef4df4aef8ae66c1507326696~tplv-goo7wpa0wc-image.image" alt="输入视频2" />
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap"><nobr><b>处理过程</b></nobr></td>
      <td>
        您将观察到：<br /><br />
        · 自主规划：智能体将自动识别出需要调用 <code>audio_video_stitching</code> 工具。<br />
        · 异步追踪：由于云端剪辑需要时间，智能体会提交任务并返回一个任务标识（TaskID），并在后台自动轮询进度。如果您发现对话中断，可以手动追问：“刚才的任务处理完了吗？”。<br />
        · 结果交付：任务完成后，智能体会直接给出生成的视频信息以及预览链接。<br /><br />
        <img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/255337623fcf4cdaa2fac5776b76a97c~tplv-goo7wpa0wc-image.image" alt="任务执行过程示意图" />
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap"><nobr><b>输出视频</b></nobr></td>
      <td>
        <img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/faac6d11638841b2ab84953437c49560~tplv-goo7wpa0wc-image.image" alt="输出视频" />
      </td>
    </tr>
  </tbody>
</table>

# 参考信息

## 提示词编写建议

为了让智能体更准确地调用 VeVOD MCP 工具，建议在撰写提示词时遵循以下原则：

- **明确目标空间**：
  - 您可以在 MCP 配置阶段通过 x-tt-space-name 字段预先指定默认视频点播空间。配置默认空间后，所有任务将默认使用该空间进行媒资处理，无需每次提示词中重复声明。
  - 如果未在配置中指定默认空间，或者需要临时使用其他空间，请在提示词中明确目标空间，例如："请使用 my_media_space 这个空间进行处理"。
- **指定待处理视频**：您可以通过以下两种方式灵活地指定需要处理的源素材：
  - **通过 URL 指定**：直接在提示词中提供素材的公网 URL。系统会自动拉取文件并上传至点播空间，然后执行后续处理任务。例如："请帮我将 http://example.com/my_video.mp4 这个视频的语速调整为 1.5 倍，并为它生成中文字幕。"
  - **通过点播媒资指定**：如果素材已[上传](https://www.volcengine.com/docs/4/2887?lang=zh)至点播空间，您可以直接通过其 Vid (视频 ID) 或 FileName (文件名) 进行引用。例如："请帮我把 Vid 为 v03103g50000cl7p8d9o346g2n9p2lp0 的视频水平翻转，并提高它的画质到 1080P。"
- **描述执行顺序**： 对于涉及多个原子能力的复杂任务，建议使用“先...再...最后...”的结构，显式地描述步骤间的先后顺序。例如：“先执行人声分离，再对分离后的人声进行语音转写”。
- **设定质量与规格边界**：AI 的产出具有一定的概率性，显式的参数约束可以降低结果的不确定性。例如在涉及视频增强任务时，明确期望值：“请以 1080P 规格输出合成后的视频”。

## 常用提示词参考

下表展示了常见业务场景下的推荐提示词。您可以直接将这些提示词复制到对话框中尝试，并根据实际需求进行微调。

### **视觉效果变换**

提示词：帮我把这个视频进行水平翻转，并调整为 2 倍速播放。

<table>
  <thead>
    <tr>
      <th><nobr>输入视频</nobr></th>
      <th><nobr>输出视频</nobr></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap"><nobr>
        <img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/5750e89648104f9aab4ffd1421b25129~tplv-goo7wpa0wc-image.image" alt="输入视频" />
      </nobr></td>
      <td>
        <img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/ee97af04ec7445ce91586cd34a03927f~tplv-goo7wpa0wc-image.image" alt="输出视频" />
      </td>
    </tr>
  </tbody>
</table>

### **字幕提取与自动压制**

提示词：通过 ASR 识别 test 空间 speech_no_subtitle.mp4 视频中的音频，转为字幕；然后再将字幕添加到原视频中，生成一个新视频。

<table>
  <thead>
    <tr>
      <th><nobr>输入视频</nobr></th>
      <th><nobr>输出视频</nobr></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap"><nobr>
        <img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/314e504b12de45a5892d7cc7a34aa1e2~tplv-goo7wpa0wc-image.image" alt="输入视频" />
      </nobr></td>
      <td>
        <img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/7d05d8fab9d34ac2844170ef17a6a19a~tplv-goo7wpa0wc-image.image" alt="输出视频" />
      </td>
    </tr>
  </tbody>
</table>

## MCP 配置参数说明

下表列出 VeVOD MCP 的核心配置项，区分云端部署与本地部署。请根据您的实际接入场景选择对应的参数。

<table>
  <thead>
    <tr>
      <th><nobr>云端 Header 字段</nobr></th>
      <th><nobr>本地环境变量名</nobr></th>
      <th><nobr>示例</nobr></th>
      <th><nobr>说明</nobr></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap"><nobr>x-tt-access-key</nobr></td>
      <td>VOLCENGINE_ACCESS_KEY</td>
      <td>AKLTMTU2M...</td>
      <td>火山引擎访问密钥 AK</td>
    </tr>
    <tr>
      <td style="white-space: nowrap"><nobr>x-tt-secret-key</nobr></td>
      <td>VOLCENGINE_SECRET_KEY</td>
      <td>TnpZek5HT...</td>
      <td>火山引擎访问密钥 SK</td>
    </tr>
    <tr>
      <td style="white-space: nowrap"><nobr>x-tt-tools-type</nobr></td>
      <td>MCP_TOOLS_TYPE</td>
      <td>groups 或 tools</td>
      <td>加载模式。决定按“分组”还是按“具体工具”加载。</td>
    </tr>
    <tr>
      <td style="white-space: nowrap"><nobr>x-tt-tools-source</nobr></td>
      <td>MCP_TOOLS_SOURCE</td>
      <td>all 或 edit,upload</td>
      <td>
        加载范围。<br /><br />
        · 全量加载 (all)：仅在 <code>x-tt-tools-type</code> 为 <code>groups</code> 时生效。适用于功能强大的模型（如 GPT-4、Claude 3.5）。注意，在 Trae 中如果工具总数超过 10 个会报错。<br />
        · 场景化加载 (edit,upload)：例如，如果您只需剪辑功能，仅加载 edit 分组可以显著降低 Token 消耗，并提高 AI 调用的准确率。
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap"><nobr>x-tt-host</nobr></td>
      <td>VOLCENGINE_HOST</td>
      <td>vod.volcengineapi.com</td>
      <td>视频点播服务的 API 域名</td>
    </tr>
    <tr>
      <td style="white-space: nowrap"><nobr>x-tt-region</nobr></td>
      <td>VOLCENGINE_REGION</td>
      <td>cn-north-1</td>
      <td>视频点播服务所在的地域</td>
    </tr>
    <tr>
      <td style="white-space: nowrap"><nobr>x-tt-session-token</nobr></td>
      <td>VOLCENGINE_SESSION_TOKEN</td>
      <td>...</td>
      <td>（可选）使用临时凭证时填写</td>
    </tr>
  </tbody>
</table>

## License

MIT
