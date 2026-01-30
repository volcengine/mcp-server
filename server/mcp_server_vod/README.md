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

### Tool 18 flip_video

#### Description

Video flip (vertical and horizontal). Supports vid, http url, and directurl input modes.

#### Trigger Example

Flip the video vertically and horizontally; video is vid1, space is space1.

### Tool 19 speedup_video

#### Description

Video speed adjustment. Supports vid, http url, and directurl input modes.

#### Trigger Example

Adjust video vid1 to 2x speed; space is space1.

### Tool 20 speedup_audio

#### Description

Audio speed adjustment. Supports vid, http url, and directurl input modes.

#### Trigger Example

Adjust audio vid1 to 2x speed; space is space1.

### Tool 21 image_to_video

#### Description

Image-to-video conversion. Supports vid, http url, and directurl input modes.

#### Trigger Example

Apply zoom and random transitions to images; image resources are vid1, vid2, vid3; space is space1.

### Tool 22 compile_video_audio

#### Description

Audio-video composition: strip original audio from video, align audio with video duration, and related capabilities.

#### Trigger Example

Merge audio and video, strip original audio from the video, use video duration as reference; video is vid1, audio is vid2; space is space1.

### Tool 23 extract_audio

#### Description

Extract audio from video. Supports configuring audio output format.

#### Trigger Example

Extract audio from vid1; space is space1.

### Tool 24 mix_audios

#### Description

Audio mixing (e.g. adding background music to audio).

#### Trigger Example

Mix audios vid1 and vid2; space is space1.

### Tool 25 add_subtitle

#### Description

Add subtitles to video. Typical flow: generate narration with a model, generate voice + subtitles, then composite into the video.

#### Trigger Example

Add subtitle `https:****.srt` to video vid1; outline color red, font size 70, outline width 10; space is space1.

### Tool 26 add_sub_video

#### Description

Picture-in-picture, add image to video, and video watermarking.

#### Trigger Example

Add watermark overlay: main video vid1, overlay video vid2; overlay at top-right, size 100×100; space is space1.

### Tool 27 get_video_audio_info

#### Description

Retrieve video/audio metadata.

#### Trigger Example

Get playback info for vid1; space is space1.

### Tool 28 get_play_url

#### Description

Get audio/video playback URL.

#### Trigger Example

Get playback URL for vid1; space is space1.

## Supported Platforms

Ark, Cursor, Trae, etc.

## Product Console

[Volcano Engine - Video on Demand - Console](https://www.volcengine.com/product/vod)

## Authentication

Apply for VOLCENGINE_ACCESS_KEY and VOLCENGINE_SECRET_KEY at [Volcano Engine - Video on Demand - Console](https://www.volcengine.com/product/vod).

## Installation

### Requirements

- Python 3.13+
- Volcano Engine account and AccessKey/SecretKey

## Deployment

### Integrate in MCP Client

Configure the MCP service in your MCP client. Example MCP JSON:

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
         "MCP_TOOLS_TYPE": "Your Source", // groups | tools
         // - In groups mode, MCP_TOOLS_SOURCE is the group name
         // - In tools mode, MCP_TOOLS_SOURCE is the tool name
        "MCP_TOOLS_SOURCE": "Your Source",

      }
    }
  }
}
```

### Cloud Deployment

**Dynamic authentication and grouping are supported. Header configuration:**

- To enable all tools:
  - x-tt-tools-type: groups
  - x-tt-tools-source: all
- You can switch MCP tools dynamically via x-tt-tools-source to reduce noise and token usage for scenario-specific agents.
- x-tt-tools-type: loading mode; values: groups | tools
- In groups mode, x-tt-tools-source is the group name; use all for all groups.
- In tools mode, x-tt-tools-source is the tool name.

### Group Configuration

**Default exposed tools:**

- get_play_url: Get playback URL
- audio_video_stitching: Audio/video stitching
- audio_video_clipping: Audio/video clipping
- get_v_creative_task_result: Query edit task result

**Full group mapping:**

```json
{
    # edit group
    "edit": [ # group name
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
    # video_play group
    "video_play": [
        "get_play_url",
        "get_video_audio_info"
    ],
    # upload group
    "upload": [
        "video_batch_upload",
        "query_batch_upload_task_info"
    ],
    # intelligent_slicing group
    "intelligent_slicing": [
        "intelligent_slicing_task"
    ],
    # intelligent_matting group
    "intelligent_matting": [
        "portrait_image_retouching_task",
        "green_screen_task"
    ],
    # subtitle_processing group
    "subtitle_processing": [
        "asr_speech_to_text_task",
        "ocr_text_to_subtitles_task",
        "video_subtitles_removal_task",
        "add_subtitle",
    ],
    # audio_processing group
    "audio_processing": [
        "voice_separation_task",
        "audio_noise_reduction_task"
    ],
    # video_enhancement group
    "video_enhancement": [
        "video_interlacing_task",
        "video_super_resolution_task",
        "video_quality_enhancement_task"
    ],
    # media_tasks group (common)
    "media_tasks": [
        "get_media_execution_task_result"
    ],
}
```

## License

MIT
