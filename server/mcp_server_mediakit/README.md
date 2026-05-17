# MediaKit MCP Server

MediaKit MCP Server is a standard AI capability plugin for Volcano Engine AI MediaKit. It is built on the MCP (Model Context Protocol) protocol and exposes cloud media capabilities such as video editing, audio/video processing, subtitle processing, and video enhancement as tools that can be called by AI agents. With MediaKit MCP, developers can use natural language to drive intelligent media production workflows.

| Field | Value |
| --- | --- |
| Version | v1.0.0 |
| Description | MediaKit MCP intelligent media assistant |
| Categories | Media cloud, audio/video editing, video enhancement |
| Tags | MCP, MediaKit, video editing, audio processing, video enhancement |

## Tool Overview

MediaKit MCP provides tools that cover the full workflow from asynchronous task query to deep media editing and video enhancement. Tools are grouped by domain and can be loaded dynamically by group or by tool name.

<table>
  <thead>
    <tr>
      <th>Category</th>
      <th>Group</th>
      <th>Tool</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Shared</b></td>
      <td>shared</td>
      <td>query_task</td>
      <td><b>Task query</b>: Query asynchronous task status and results after submitting an asynchronous MediaKit task. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/shared.py#L33">query_task</a>.
      </td>
    </tr>
    <tr>
      <td rowspan="11"><b>Video editing</b></td>
      <td rowspan="11">editing</td>
      <td>add_image_to_video</td>
      <td><b>Add image to video</b>: Add an image overlay or watermark to a video. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L30">add_image_to_video</a>.
      </td>
    </tr>
    <tr>
      <td>add_subtitle_to_video</td>
      <td><b>Add subtitles to video</b>: Burn subtitle files or subtitle text into a video. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L52">add_subtitle_to_video</a>.
      </td>
    </tr>
    <tr>
      <td>adjust_video_speed</td>
      <td><b>Adjust video speed</b>: Adjust video playback speed for fast-motion or slow-motion effects. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L73">adjust_video_speed</a>.
      </td>
    </tr>
    <tr>
      <td>concat_audio</td>
      <td><b>Concatenate audio</b>: Concatenate multiple audio clips into a single audio file. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L89">concat_audio</a>.
      </td>
    </tr>
    <tr>
      <td>concat_video</td>
      <td><b>Concatenate video</b>: Concatenate multiple video clips and optionally apply transition effects. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L104">concat_video</a>.
      </td>
    </tr>
    <tr>
      <td>extract_audio</td>
      <td><b>Extract audio</b>: Extract the audio stream from a video as an independent audio file. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L120">extract_audio</a>.
      </td>
    </tr>
    <tr>
      <td>flip_video</td>
      <td><b>Flip video</b>: Flip a video vertically or horizontally. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L136">flip_video</a>.
      </td>
    </tr>
    <tr>
      <td>image_to_video</td>
      <td><b>Image to video</b>: Generate an animated video from multiple images with optional transitions. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L153">image_to_video</a>.
      </td>
    </tr>
    <tr>
      <td>mux_audio_video</td>
      <td><b>Mux audio and video</b>: Combine an audio track and a video track into one video file. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L169">mux_audio_video</a>.
      </td>
    </tr>
    <tr>
      <td>trim_audio</td>
      <td><b>Trim audio</b>: Trim an audio file by start and end time. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L189">trim_audio</a>.
      </td>
    </tr>
    <tr>
      <td>trim_video</td>
      <td><b>Trim video</b>: Trim a video by start and end time. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L206">trim_video</a>.
      </td>
    </tr>
    <tr>
      <td rowspan="2"><b>Video enhancement</b></td>
      <td rowspan="2">video</td>
      <td>erase_video_subtitle_pro</td>
      <td><b>Erase video subtitles</b>: Remove subtitles or text from videos with high-quality restoration. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/video.py#L30">erase_video_subtitle_pro</a>.
      </td>
    </tr>
    <tr>
      <td>enhance_video</td>
      <td><b>Enhance video</b>: Improve video quality for AIGC, UGC, short drama, education, game, and old film restoration scenarios. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mediakit-interactive/blob/main/mediakit-interactive-product/mcp_server_mediakit/src/mediakit/mcp_tools/video.py#L49">enhance_video</a>.
      </td>
    </tr>
  </tbody>
</table>

## Configuration

| Variable | Description | Required |
| --- | --- | --- |
| `MEDIAKIT_API_KEY` | MediaKit API key used for authentication. | Yes |
| `MEDIAKIT_ENDPOINT` | MediaKit API endpoint. Defaults to `https://amk.cn-beijing.volces.com`. | No |
| `MCP_DOMAINS` | Comma-separated domain allowlist, such as `editing,video`. | No |
| `MCP_TOOLS` | Comma-separated tool allowlist, such as `trim_video,query_task`. | No |

## Quick Start

Install the package:

```bash
pip install mcp-server-mediakit
```

Set your MediaKit API key:

```bash
export MEDIAKIT_API_KEY="your-api-key"
```

Run with stdio transport:

```bash
mcp-server-mediakit --transport stdio
```

Run with streamable HTTP transport:

```bash
mcp-server-mediakit --transport streamable-http
```

## Usage Notes

- Synchronous tasks return results directly.
- Asynchronous tasks return a `task_id`; call `query_task` to get task status and results.
- Idempotency is enabled by default. Requests from the same account with the same core parameters within 2 days return the first task result instead of creating duplicate tasks.
- To control idempotency explicitly, pass `client_token`. Reuse the same value for retries and use a new unique value to force a new task.

## Tool Details

### query_task

Query asynchronous task status. Supports one-shot query or polling through `poll_interval_seconds` and `max_poll_attempts`.

### add_image_to_video

Add an image overlay to a video. Commonly used for image watermarks. Supports image size, position, start time, and end time.

### add_subtitle_to_video

Burn subtitle files or structured subtitle text into a video. Supports subtitle position, font size, font color, and font type.

### adjust_video_speed

Adjust video playback speed. Supports speed values from `0.1` to `4`.

### concat_audio

Concatenate audio clips. Supports up to 100 audio URLs.

### concat_video

Concatenate video clips. Supports up to 100 video URLs and optional transition effects.

### extract_audio

Extract audio from a video and output `mp3` or `m4a`.

### flip_video

Flip a video vertically or horizontally.

### image_to_video

Generate an animated video from multiple images and optional transition effects.

### mux_audio_video

Combine a video and an audio file. Supports preserving the original video audio and synchronizing audio/video duration.

### trim_audio

Trim an audio file by start and end time in seconds.

### trim_video

Trim a video by start and end time in seconds.

### erase_video_subtitle_pro

Remove subtitles or text from videos and restore the visual content. Supports mainstream video formats such as `mp4`, `flv`, `ts`, `avi`, `mov`, `wmv`, and `mkv`.

### enhance_video

Enhance video quality for scenarios such as `common`, `ugc`, `short_series`, `aigc`, and `old_film`. Supports standard and professional tool versions.
