# VOD MCP Server

An efficient and convenient video editing assistant that enables various editing operations through conversational interaction, including multi-video timeline splicing, long video segmentation and splicing, and adding transition animations, lowering the technical barrier and operational costs of video editing.

| Version     | v1.0.0                                           |
| ----------- | ------------------------------------------------ |
| Description | Volcano Engine VOD Intelligent Editing Assistant |
| Category    | Video Cloud, Video-on-Demand                     |
| Tags        | VOD, Video-on-Demand, Video Editing              |

### Tool 1: audio_video_stitching

#### Description

Concatenate multiple audio and video files into a new audio and video file, supporting three input methods: vid, url, and directurl

#### Trigger Example

Concatenate vid1, vid2 and the video, with the space being space1.

### Tool 2: audio_video_clipping

#### Description

Clip an audio or video file to a new audio or video file, with the specified start and end time, supporting three input methods: vid, url, and directurl.

#### Trigger Example

Clip vid1, vid2 and the video, with the space being space1. Start time being 1s, end time being 30s.

### Tool 3: get_v_creative_task_result

#### Description

Query the result of a video creative task, including task status, processing progress, and processing results.

#### Trigger Example

Query the result of VCreativeId video creative task, with the space being space1.

## Supported Platforms

Ark, Cursor, Trae etc.

## Service Activation Link (Full Product)

[Volcano Engine-Video on Demand-Console](https://www.volcengine.com/product/vod)

## Authentication Method

Please apply for VOLCENGINE_ACCESS_KEY, VOLCENGINE_SECRET_KEY at [Volcano Engine-Video on Demand-Console](https://www.volcengine.com/product/vod)

## Installation

### Environment Requirements

- Python 3.13+
- Volcano Engine account and AccessKey/SecretKey

## Deployment

### Integration in MCP Client

Configure MCP service in mcp client, MCP JSON configuration:

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
