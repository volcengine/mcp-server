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

### Tool 4 video_batch_upload

#### Description

Batch fetch and upload by URLs. Synchronously upload audio/video to the specified space.

#### Trigger Example

Upload the files at URLs url1 and url2 to the space named "your space", ensuring the file extensions are .mp4.

### Tool 5 query_batch_upload_task_info

#### Description

Query the status of URL batch upload tasks.

#### Trigger Example

Query the upload task status with JobId xxx.

### Tool 6 video_quality_enhancement_task

#### Description

Video enhancement, supporting Vid and DirectUrl input modes.

#### Trigger Example

Enhance video vid1 in space space1.

### Tool 7 video_super_resolution_task

#### Description

Video super-resolution, supporting Vid and DirectUrl input modes.

#### Trigger Example

Apply super-resolution to video vid1 in space space1.

### Tool 8 video_interlacing_task

#### Description

Video frame interpolation, supporting Vid and DirectUrl input modes.

#### Trigger Example

Apply frame interpolation to video vid1 in space space1.

### Tool 9 audio\_ noise_reduction_task

#### Description

Audio noise reduction, supporting Vid and DirectUrl input modes.

#### Trigger Example

Apply noise reduction to audio vid1 in space space1.

### Tool 10 asr_speech_to_text_task

#### Description

ASR speech-to-text captioning, supporting Vid and DirectUrl input modes.

#### Trigger Example

Run ASR recognition on video vid1 in space space1.

### Tool 11 ocr_text_to_subtitles_task

#### Description

OCR text to subtitles, supporting Vid and DirectUrl input modes.

#### Trigger Example

Run OCR recognition on video vid1 in space space1.

### Tool 12 video_subtitles_removal_task

#### Description

Video subtitle removal, supporting Vid and DirectUrl input modes.

#### Trigger Example

Remove subtitles from video vid1 in space space1.

### Tool 13 voice_separation_task

#### Description

Vocal separation from video, supporting Vid and DirectUrl input modes.

#### Trigger Example

Separate vocals for video vid1 in space space1.

### Tool 14 intelligent_slicing_task

#### Description

Intelligent slicing, supporting Vid and DirectUrl input modes.

#### Trigger Example

Perform intelligent segment slicing on video vid1 in space space1.

### Tool 15 green_screen_task

#### Description

Green screen keying, supporting Vid and DirectUrl input modes.

#### Trigger Example

Apply green screen keying to video vid1 in space space1.

### Tool 16 portrait_image_retouching_task

#### Description

Portrait cutout, supporting Vid and DirectUrl input modes.

#### Trigger Example

Apply portrait cutout processing to video vid1 in space space1.

### Tool 17 get_media_execution_task_result

#### Description

Query media processing task results, including task status, processing progress, and output information.

#### Trigger Example

Query the media processing result for the portrait cutout task with runId xxx in space space1.

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
        "VOLCENGINE_SECRET_KEY": "Your Volcengine SK",
        "MCP_TOOL_GROUPS": "YOUR_TOOL_GROUPS"
      }
    }
  }
}
```

## License

MIT
