# MediaKit MCP Server

MediaKit MCP Server is a standard AI capability plugin for Volcano Engine AI MediaKit. It is built on the MCP (Model Context Protocol) protocol and exposes cloud media capabilities such as video editing, audio processing, subtitle processing, and video enhancement as tools that can be called by AI agents. With MediaKit MCP, developers can use natural language to drive intelligent media production workflows.

| Field       | Value                                                             |
| ----------- | ----------------------------------------------------------------- |
| Version     | v1.0.0                                                            |
| Description | MediaKit MCP intelligent media assistant                          |
| Categories  | Media cloud, audio/video editing, video enhancement               |
| Tags        | MCP, MediaKit, video editing, audio processing, video enhancement |

## Tool Overview

MediaKit MCP provides tools that cover the full workflow from asynchronous task query to deep media editing and video enhancement. All tools support dynamic loading by group or by tool name to optimize agent reasoning efficiency.

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
      <td><b>Task query</b>: Query asynchronous task status and results after submitting an asynchronous task. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_mediakit/src/mediakit/mcp_tools/shared.py#L37">query_task</a>.
      </td>
    </tr>
    <tr>
      <td rowspan="11"><b>Video editing</b></td>
      <td rowspan="11">editing</td>
      <td>add_image_to_video</td>
      <td><b>Add image to video</b>: Overlay an image on a video, commonly used for image watermarks. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L44">add_image_to_video</a>.
      </td>
    </tr>
    <tr>
      <td>add_subtitle_to_video</td>
      <td><b>Add subtitles to video</b>: Burn subtitle files or subtitle text into a video. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L66">add_subtitle_to_video</a>.
      </td>
    </tr>
    <tr>
      <td>adjust_video_speed</td>
      <td><b>Adjust video speed</b>: Change video playback speed for fast or slow motion effects. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L87">adjust_video_speed</a>.
      </td>
    </tr>
    <tr>
      <td>concat_audio</td>
      <td><b>Concatenate audio</b>: Merge multiple audio clips into a single audio file. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L103">concat_audio</a>.
      </td>
    </tr>
    <tr>
      <td>concat_video</td>
      <td><b>Concatenate video</b>: Merge multiple video clips into a new video with optional transitions. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L118">concat_video</a>.
      </td>
    </tr>
    <tr>
      <td>extract_audio</td>
      <td><b>Extract audio</b>: Separate the audio stream from a video and save it as an independent audio file. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L134">extract_audio</a>.
      </td>
    </tr>
    <tr>
      <td>flip_video</td>
      <td><b>Flip video</b>: Flip a video horizontally or vertically. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L150">flip_video</a>.
      </td>
    </tr>
    <tr>
      <td>image_to_video</td>
      <td><b>Image to video</b>: Create an animated video from multiple images with optional transitions. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L167">image_to_video</a>.
      </td>
    </tr>
    <tr>
      <td>mux_audio_video</td>
      <td><b>Mux audio and video</b>: Combine a video track and an audio track into one video file. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L183">mux_audio_video</a>.
      </td>
    </tr>
    <tr>
      <td>trim_audio</td>
      <td><b>Trim audio</b>: Trim an audio file by start and end time. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L203">trim_audio</a>.
      </td>
    </tr>
    <tr>
      <td>trim_video</td>
      <td><b>Trim video</b>: Trim a video by start and end time. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_mediakit/src/mediakit/mcp_tools/editing.py#L220">trim_video</a>.
      </td>
    </tr>
    <tr>
      <td rowspan="2"><b>Video enhancement</b></td>
      <td rowspan="2">video</td>
      <td>erase_video_subtitle_pro</td>
      <td><b>Erase video subtitles</b>: Remove subtitles or text from a video with high-quality restoration. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_mediakit/src/mediakit/mcp_tools/video.py#L60">erase_video_subtitle_pro</a>.
      </td>
    </tr>
    <tr>
      <td>enhance_video</td>
      <td><b>Enhance video</b>: Improve video quality for AIGC, UGC, short drama, education, gaming, and old film restoration scenarios. For detailed input and output parameters, see
        <a href="https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_mediakit/src/mediakit/mcp_tools/video.py#L38">enhance_video</a>.
      </td>
    </tr>
  </tbody>
</table>

# Quick Start in Trae

Trae is an AI-native IDE with strong agent collaboration capabilities. By connecting MediaKit MCP, you can call cloud media processing capabilities in Trae with natural language and quickly complete tasks such as video editing, subtitle processing, audio processing, and video enhancement.

## Prerequisites

- Prepare a valid MediaKit API key.
- Confirm the MediaKit service endpoint. If not explicitly configured, the default is `https://amk.cn-beijing.volces.com`.
- Install the [Trae client](https://www.trae.com.cn/).
- For local mode or self-hosted cloud mode, make sure `uvx` is installed in your local environment. Run `uvx --version` to check. If it is not installed, follow the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).

## Steps

### Step 1: Choose an Access Mode

Choose one of the following modes based on your usage scenario:

| Mode                        | Best for                                                           | Access method                                                                                  |
| --------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| **Local Mode (JSON Local)** | Personal debugging, quick trials, no self-hosted service required. | Use `uvx` to launch MediaKit MCP directly from the `mcp-server` repository subdirectory.       |
| **Cloud Mode (JSON URL)**   | Team sharing, long-term usage, centralized operations.             | Deploy MediaKit MCP Server yourself, then connect using the deployed Streamable HTTP endpoint. |

### Step 2: Add MCP Configuration

1. Open Trae and click the settings button in the top-right corner.
2. In the MCP tab, click **Add** > **Add Manually**.
3. Copy the JSON configuration for your selected mode and replace the fields as described below.

#### Local Mode (JSON Local)

Copy the following JSON and replace the fields as needed. Trae uses `uvx` to fetch the remote code and run it locally.

```json
{
  "mcpServers": {
    "mediakit_mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_mediakit",
        "mcp-server-mediakit"
      ],
      "env": {
        "MEDIAKIT_API_KEY": "your-api-key",
        "MEDIAKIT_ENDPOINT": "https://amk.cn-beijing.volces.com",
        "MCP_DOMAINS": "editing,video"
      }
    }
  }
}
```

**Field replacement notes:**

- `mediakit_mcp`: The MCP service name. You can customize it.
- `MEDIAKIT_API_KEY`: Replace with your MediaKit API key.
- `MEDIAKIT_ENDPOINT`: The MediaKit service endpoint. Keep `https://amk.cn-beijing.volces.com` if you use the default endpoint.
- `MCP_DOMAINS`: Load tools by group, for example `editing,video`. To load tools by exact tool name, use `MCP_TOOLS` instead.

To load by tool name, use a configuration like this:

```json
{
  "mcpServers": {
    "mediakit_mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_mediakit",
        "mcp-server-mediakit"
      ],
      "env": {
        "MEDIAKIT_API_KEY": "your-api-key",
        "MEDIAKIT_ENDPOINT": "https://amk.cn-beijing.volces.com",
        "MCP_TOOLS": "trim_video,query_task"
      }
    }
  }
}
```

#### Cloud Mode (JSON URL)

Cloud mode does not provide a prebuilt deployment URL. Before using this mode, you need to deploy MediaKit MCP Server yourself and make sure the service is reachable through Streamable HTTP. After deployment, record the service URL, for example `https://your-domain/mcp`, and then connect it in Trae as shown below.

A simple startup example is:

```bash
export MEDIAKIT_API_KEY="your-api-key"
export MEDIAKIT_ENDPOINT="https://amk.cn-beijing.volces.com"
export MCP_SERVER_HOST="0.0.0.0"
export MCP_SERVER_PORT="8000"
export STREAMABLE_HTTP_PATH="/mcp"

uvx --from "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_mediakit"   mcp-server-mediakit   --transport streamable-http
```

After deployment, copy the following JSON and replace the fields as needed:

```json
{
  "mcpServers": {
    "mediakit_mcp": {
      "url": "https://your-domain/mcp",
      "headers": {
        "x-amk-api-key": "your-api-key",
        "x-mediakit-endpoint": "https://amk.cn-beijing.volces.com",
        "x-mcp-domains": "editing,video"
      }
    }
  }
}
```

**Field replacement notes:**

- `mediakit_mcp`: The MCP service name. You can customize it.
- `url`: Replace with your self-hosted MediaKit MCP Streamable HTTP URL, such as `https://your-domain/mcp`.
- `x-amk-api-key`: Replace with your MediaKit API key.
- `x-mediakit-endpoint`: The MediaKit service endpoint. Use `https://amk.cn-beijing.volces.com` if you use the default endpoint.
- `x-mcp-domains`: Load tools by group, for example `editing,video`. To load tools by exact tool name, use `x-mcp-tools` instead.

To load by tool name, use a configuration like this:

```json
{
  "mcpServers": {
    "mediakit_mcp": {
      "url": "https://your-domain/mcp",
      "headers": {
        "x-amk-api-key": "your-api-key",
        "x-mediakit-endpoint": "https://amk.cn-beijing.volces.com",
        "x-mcp-tools": "trim_video,query_task"
      }
    }
  }
}
```

4. Make sure the MCP status is shown as active in Trae.

### Step 3: Start Agent Conversations

Open the chat panel in Trae and switch the agent mode to one that supports MCP. Then you can directly issue natural language instructions such as:

- Trim this video to the first 10 seconds and output a new video.
- Add Chinese subtitles to this video with font size 28.
- Remove the subtitles at the bottom of this video, then enhance the processed video quality.
- Concatenate these two audio files, and if the task is asynchronous, continue querying until the final result is ready.

## Usage Notes

- Synchronous tasks return results directly.
- Asynchronous tasks return a `task_id`, and you need to call `query_task` to get task status and results.
- Idempotency is enabled by default. Requests from the same account with the same core parameters within 2 days return the first task result instead of creating duplicate tasks.
- To control idempotency explicitly, pass `client_token`. Reuse the same value for retries and use a new unique value to force a new task.
- `client_token` is generated by the client and must not exceed 64 characters.

## MCP Configuration Reference

The table below lists the core MediaKit MCP configuration fields for cloud mode and local mode.

<table>
  <thead>
    <tr>
      <th>Cloud header</th>
      <th>Local environment variable</th>
      <th>Example</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>x-amk-api-key</td>
      <td>MEDIAKIT_API_KEY</td>
      <td>your-api-key</td>
      <td>MediaKit API key used for authentication.</td>
    </tr>
    <tr>
      <td>x-mediakit-endpoint</td>
      <td>MEDIAKIT_ENDPOINT</td>
      <td>https://amk.cn-beijing.volces.com</td>
      <td>MediaKit service endpoint. The default value is this endpoint.</td>
    </tr>
    <tr>
      <td>x-mcp-domains</td>
      <td>MCP_DOMAINS</td>
      <td>editing,video</td>
      <td>Load tools by group. Separate multiple groups with commas.</td>
    </tr>
    <tr>
      <td>x-mcp-tools</td>
      <td>MCP_TOOLS</td>
      <td>trim_video,query_task</td>
      <td>Load tools by tool name. Separate multiple tool names with commas.</td>
    </tr>
  </tbody>
</table>

For self-hosted cloud mode, you can also configure the following startup parameters:

| Environment variable   | Default value | Description                 |
| ---------------------- | ------------- | --------------------------- |
| `MCP_SERVER_HOST`      | `0.0.0.0`     | MCP service bind address.   |
| `MCP_SERVER_PORT`      | `8000`        | MCP service listening port. |
| `STREAMABLE_HTTP_PATH` | `/mcp`        | Streamable HTTP path.       |

## Tool Details

### query_task

Query asynchronous task status. Supports one-shot query or polling through `poll_interval_seconds` and `max_poll_attempts`.

### add_image_to_video

Add an image overlay to a video. Commonly used for image watermarks. Supports image width, height, horizontal position, vertical position, start time, and end time.

### add_subtitle_to_video

Burn subtitle files or subtitle text into a video. Supports subtitle position, font size, font color, and font type.

### adjust_video_speed

Adjust video playback speed. Supports speed values from `0.1` to `4`.

### concat_audio

Concatenate multiple audio clips. Supports up to 100 audio URLs.

### concat_video

Concatenate multiple video clips. Supports up to 100 video URLs and optional transition effects.

### extract_audio

Extract audio from a video. Supports `mp3` or `m4a` output.

### flip_video

Flip video frames horizontally or vertically.

### image_to_video

Create an animated video from multiple images and optional transition effects.

### mux_audio_video

Combine a video and an audio file into one video. Supports preserving the original video audio and synchronizing duration by video or audio timeline.

### trim_audio

Trim an audio file by start and end time in seconds.

### trim_video

Trim a video by start and end time in seconds.

### erase_video_subtitle_pro

Remove subtitles or text from a video with high-quality restoration. Supports mainstream video formats such as `mp4`, `flv`, `ts`, `avi`, `mov`, `wmv`, and `mkv`.

### enhance_video

Enhance video quality for scenarios such as `common`, `ugc`, `short_series`, `aigc`, and `old_film`. Supports both standard and professional versions.

## License

MIT

This software calls MediaKit APIs at runtime. Use of these APIs is subject to the following terms and privacy policies:

- [Video Cloud Service Special Terms](https://www.volcengine.com/docs/6448/79646?lang=zh)
- [Intelligent Processing Service Billing Rules](https://www.volcengine.com/docs/6448/104992?lang=zh)
- [Intelligent Processing Service Level Agreement](https://www.volcengine.com/docs/6448/79648?lang=zh)
