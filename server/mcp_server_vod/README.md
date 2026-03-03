# VOD MCP Server

[VeVOD MCP](https://github.com/volcengine/mcp-vod) is a standard capability plugin launched by Volcano Engine Video on Demand for the AI era. Based on the MCP (Model Context Protocol) protocol, it encapsulates professional cloud-based video editing, quality enhancement, content recognition, and other atomic capabilities into tools that can be intuitively invoked by agents. Through VeVOD MCP, developers can directly drive AI agents to complete complex cloud-based video processing tasks using natural language.

| Version | v1.0.0 |
| --- | --- |
| Description | Volcano Engine VOD Intelligent Editing Assistant |
| Category | Video Cloud, Video on Demand |
| Tags | VOD, Video on Demand, Video Editing |

# VeVOD MCP Introduction

## Tool Overview

VeVOD MCP has opened capabilities covering the entire process from material upload and content understanding to deep editing. All tools support dynamic loading via "Group" to optimize the inference efficiency of the agent.

| **Category** | **Group Name** | **Tool** | **Description** |
| --- | --- | --- | --- |
| **Basic Functions** | upload <br> | video_batch_upload <br> | **File Upload**: Supports batch pulling audio, video, images, and other files from public URLs to upload to the VOD space, and allows querying the status of upload tasks. See detailed input and output parameters in [video_batch_upload](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/upload.py#L9). |
| **Video Editing** | edit <br> | audio_video_stitching | **Multi-segment Stitching**: Stitches multiple video or audio segments into a new file in a specified order, supporting various transition effects between segments. See detailed input and output parameters in [audio_video_stitching](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/edit.py#L36). |
| | | audio_video_clipping | **Segment Clipping**: Clips video or audio based on start and end time points (in seconds) to generate a new segment. See detailed input and output parameters in [audio_video_clipping](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/edit.py#L169). |
| | | flip_video | **Screen Flip**: Performs horizontal or vertical mirror flipping on the video screen. See detailed input and output parameters in [flip_video](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/edit.py#L381). |
| | | speedup_video | **Video Speed Adjustment**: Adjusts the playback speed of the video to achieve fast or slow motion effects. Supports adjustment from 0.1x to 4x. See detailed input and output parameters in [speedup_video](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/edit.py#L445). |
| | | speedup_audio | **Audio Speed Adjustment**: Adjusts the playback speed of audio files to achieve fast or slow motion effects. Supports adjustment from 0.1x to 4x. See detailed input and output parameters in [speedup_audio](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/edit.py#L513). |
| | | image_to_video | **Image to Video**: Synthesizes single or multiple images into a video file, supporting custom display duration and transition effects for each image. See detailed input and output parameters in [image_to_video](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/edit.py#L582). |
| | | compile_video_audio | **Audio-Video Synthesis**: Overlays independent video tracks and audio tracks to synthesize a single video file. Can be used to add or replace audio tracks for videos. See detailed input and output parameters in [compile_video_audio](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/edit.py#L705). |
| | | extract_audio | **Extract Audio Track**: Losslessly separates and extracts independent audio tracks from video files to generate an audio file. Supports specifying the output audio format as mp3 or m4a. See detailed input and output parameters in [extract_audio](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/edit.py#L813). |
| | | mix_audios | **Audio Mixing**: Mixes multiple audio files (such as background music, sound effects, vocals) to generate a new audio file. See detailed input and output parameters in [mix_audios](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/edit.py#L878). |
| | | add_sub_video | **Video Overlay (Picture-in-Picture)**: Overlays a sub-video or image material onto the main video to achieve picture-in-picture, video watermark, image watermark, etc. Supports customizing the position, size, and display period of the overlay element. See detailed input and output parameters in [add_sub_video](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/edit.py#L958). |
| **Video Enhancement** | video_enhancement <br> | video_quality_enhancement_task | **Comprehensive Quality Repair**: Uses AI to comprehensively repair video quality, eliminating common damages such as compression artifacts, noise, and scratches, improving overall clarity and color performance. See detailed input and output parameters in [video_quality_enhancement_task](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/video_enhancement.py#L9). |
| | | video_super_resolution_task | **AI Super Resolution**: Intelligently increases video resolution using AI algorithms, such as upscaling 720P video to 1080P, and sharpens to enhance screen details. See detailed input and output parameters in [video_super_resolution_task](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/video_enhancement.py#L49). |
| | | video_interlacing_task | **Intelligent Frame Interpolation**: Uses motion compensation algorithms to intelligently interpolate low frame rate videos (e.g., 30fps) to high frame rates (e.g., 60fps), making motion scenes smoother. See detailed input and output parameters in [video_interlacing_task](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/video_enhancement.py#L119). |
| **Subtitle Processing** | subtitle_processing <br> | asr_speech_to_text_task | **Speech to Subtitle (ASR)**: Converts speech content in video into subtitle information with timestamps using ASR technology. See detailed input and output parameters in [asr_speech_to_text_task](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/subtitle_processing.py#L11). |
| | | ocr_text_to_subtitles_task | **Screen Text Extraction (OCR)**: Intelligently extracts text embedded in video frames using OCR technology. See detailed input and output parameters in [ocr_text_to_subtitles_task](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/subtitle_processing.py#L66). |
| | | video_subtitles_removal_task | **Hard Subtitle Removal**: Intelligently detects and seamlessly removes existing hard subtitles from video frames, retaining the original background. See detailed input and output parameters in [video_subtitles_removal_task](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/subtitle_processing.py#L91). |
| | | add_subtitle | **Add Embedded Subtitles**: Burns external subtitle files (such as SRT format) into video frames with specified styles to generate new videos with embedded subtitles. Supports custom fonts, subtitle styles, and subtitle positions. See detailed input and output parameters in [add_subtitle](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/subtitle_processing.py#L126). |
| **Audio Processing** | audio_processing | voice_separation_task | **Vocal/Accompaniment Separation**: Accurately separates vocals and background music in audio, outputting them as two independent audio track files. See detailed input and output parameters in [voice_separation_task](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/audio_processing.py#L38). |
| | | audio_noise_reduction_task | **Audio Noise Reduction**: Intelligently identifies and eliminates various noises such as environmental noise, current noise, wind noise, etc., improving vocal clarity. See detailed input and output parameters in [audio_noise_reduction_task](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/audio_processing.py#L8). |
| **Intelligent Slicing** | intelligent_slicing | intelligent_slicing_task | **Intelligent Scene Slicing**: Based on screen transitions and shot changes, intelligently slices long videos into multiple logically related short clips. See detailed input and output parameters in [intelligent_slicing_task](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/intelligent_slicing.py). |
| **Intelligent Matting** | intelligent_matting <br> | portrait_image_retouching_task | **Portrait Matting**: Automatically identifies the main portrait in the video and performs high-precision matting, generating video material with a transparent channel. Supports specifying the output video container format as MOV or WEBM. See detailed input and output parameters in [portrait_image_retouching_task](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/intelligent_matting.py#L52). |
| | | green_screen_task | **Green Screen Matting**: Performs professional-grade matting on videos with green screen backgrounds, commonly used in post-production and special effects synthesis. Supports specifying the output video container format as MOV or WEBM. See detailed input and output parameters in [green_screen_task](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/intelligent_matting.py#L8). |
| **Task Management** | media_tasks | get_media_execution_task_result | **Async Task Query**: Queries and obtains the execution status and final product information (such as new file Vid, URL, etc.) of asynchronous media processing tasks via task ID. See detailed input and output parameters in [get_media_execution_task_result](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/media_tasks.py#L8). |
| **Media Distribution** | video_play | get_play_url | **Get Playback URL**: Obtains playback addresses for specified videos in various definitions and formats based on Vid or file name. See detailed input and output parameters in [get_play_url](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/video_play.py#L315). |
| | | get_video_audio_info | **Get Audio/Video Meta Info**: Obtains detailed metadata of specified audio/video, such as duration, bitrate, resolution, encoding format, frame rate, etc. See detailed input and output parameters in [get_video_audio_info](https://github.com/volcengine/mcp-server/blob/main/server/mcp_server_vod/src/vod/mcp_tools/video_play.py#L342). |

## Typical Application Scenarios

You can flexibly combine the atomic capabilities provided by VeVOD MCP to support diverse AI video creation and processing scenarios. Here are some typical application examples:

### AI Comic Generation

Quickly transform manga or novel materials into dynamic videos. MCP can automatically complete a series of tedious post-production works such as material combination, dubbing, and subtitle addition according to instructions. Core steps:

- **Screen Synthesis**: Use `image_to_video` to synthesize multiple comic images into a video, or use `audio_video_stitching` to stitch existing video clips.
- **Audio Track Processing**: Use `extract_audio` to extract the original sound, then use `mix_audios` to overlay new dubbing or background music.
- **Subtitle Generation**: Convert dubbing to subtitles via `asr_speech_to_text_task`, then use `add_subtitle` to burn them into the video.
- **Quality Enhancement**: Finally, `video_super_resolution_task` can be selected to improve the overall resolution and clarity of the output video.

### Viral Marketing Video Production

In scenarios such as e-commerce and advertising, AI-generated product images, user materials, or product demonstration clips can be quickly combined to generate eye-catching marketing short videos via natural language instructions. Core steps:

- **Clip Editing**: Use `audio_video_clipping` to capture highlight clips from long videos.
- **Stitching Synthesis**: Use `image_to_video` to synthesize multiple product images into a video, or use `audio_video_stitching` to stitch existing video clips and add background music.
- **Add Marketing Info**: Add attractive titles, selling point introductions, or event information to the video via the `add_subtitle` function.

### Education Video Production

In fields like K12 and paid knowledge, automate the generation of vivid and interesting teaching videos from graphic courseware, ancient poems, picture book stories, etc. Core steps:

- **Course Content Synthesis**: Use `image_to_video` to convert teaching PPTs or picture book images into videos. At the same time, `audio_video_stitching` can be called to stitch multiple video clips together and add transition effects to form coherent teaching content.
- **Add Narration**: Call `audio_video_stitching` to add pre-recorded course explanations or story readings to the video.
- **Add Subtitles**: Use `asr_speech_to_text_task` and `add_subtitle` to generate and add synchronized subtitles.

## Billing Instructions

VeVOD MCP itself, as an open-source tool and protocol layer plugin, does not charge extra fees. However, in the process of driving video processing through MCP, various resources of the Volcano Engine Video on Demand backend will be invoked. During use, the costs incurred mainly consist of the following three parts:

- **Media Storage Fees**: All original materials uploaded via MCP and finished videos generated after processing are stored in your VOD space and billed daily based on the storage space occupied (GB). See [Media Storage Billing](/ol8o3qyn/76542).
- **Video Processing Fees**: This is the core part of the cost, varying according to the type of task you drive MCP to execute:
  - **Cloud Editing**: Billed based on the resolution and duration of the output video. See [Video Editing Billing](/ol8o3qyn/mvybepnu).
  - **Single Task Processing**: AI tasks such as video super-resolution, frame interpolation, and speech transcription will be billed independently based on the processing specifications and duration of the task. See [Media Processing Billing](/ol8o3qyn/73msxgdi).
- **Traffic Fees**: When you watch or distribute videos via the playback address returned by MCP, downstream traffic will be generated.
  - If you have [configured an acceleration domain](https://www.volcengine.com/docs/4/177122) in VOD, [Distribution Acceleration Billing](/ol8o3qyn/u5kijik1) will occur.
  - If you have not configured an acceleration domain in VOD, [Storage Outbound Traffic](/ol8o3qyn/76542) fees will occur.

# Quick Experience: Configure in Trae

Trae is an AI-native IDE that provides powerful agent collaboration capabilities. By accessing VeVOD MCP, you can complete your first AI video editing task in just 10 minutes directly in the Trae dialog box using Vibe Coding, without writing any code.

## Prerequisites

- [Registered Volcano Engine account](https://www.volcengine.com/docs/6261/64925) and completed [Real-name Authentication](https://www.volcengine.com/docs/6261/64935).
- Obtained [Volcano Engine Access Key/Secret Key](https://www.volcengine.com/docs/6257/64983?lang=zh) (referred to as AK/SK).
- [Activated Video on Demand Service](https://console.volcengine.com/vod/overview/) and [Created Space](https://www.volcengine.com/docs/4/65669).
- (Recommended) [Upload](https://www.volcengine.com/docs/4/65670?lang=zh) the video materials to be processed to the VOD space, or prepare publicly accessible video URLs.
- (Optional) Prepare development environment:
  - Install [Trae Client](https://www.trae.com.cn/?utm_source=volcengine&utm_medium=mcp-marketplace).
  - Check if `uvx` is installed in your development environment via `uvx --version` command. If `uvx: command not found` is displayed, refer to [Official Documentation](https://docs.astral.sh/uv/getting-started/installation/) to install uvx.

## Operation Steps

### Step 1: Select Access Mode

Choose one of the following two access modes according to your needs:
| **Mode** | **Applicable Scenario** | **Access Method** |
| --- | --- | --- |
| **Local Mode (JSON Local)** | Personal quick debugging, processing local sensitive files, no public domain required. | Run directly via `uvx` command invoking local script. You can jump directly to [Step 2: Add MCP Configuration](/ol8o3qyn/4m0bde30). |
| **Cloud Mode (JSON URL)** | Long-term stable use, cross-team collaboration, no local installation environment required. | Go to [Volcano Engine MCP Marketplace](https://www.volcengine.com/mcp-marketplace/detail?name=VeVOD%20MCP), under the Trae tab, click **Cloud Deployment** to generate an exclusive long-term URL. After copying the URL, go to [Step 2: Add MCP Configuration](/ol8o3qyn/4m0bde30). <br> ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/287e233f0fbd45ff89eb44db0b1d5db5~tplv-goo7wpa0wc-image.image) <br> This method requires an account balance of not less than 100 RMB, involving [API Gateway](https://www.volcengine.com/docs/6569/185249?lang=zh) and [Function Service](https://www.volcengine.com/docs/6662/1269135?lang=zh) billing. <br> |

### Step 2: Add MCP Configuration

1. Open Trae, click the "Settings" button (gear icon) in the upper right corner of the Trae window.
2. Under the MCP tab, click **Add** > **Manually Add**.
3. According to the mode you selected in Step 1, copy the corresponding configuration JSON and replace it according to the text description below. Note that to ensure the success rate of the first call, only the core tool groups are loaded by default.

<div type="doc-tabs">
<div type="tab-item" title="Local Mode (JSON Local)" key="WyIYIdP2Hj">

Copy the following JSON and replace it according to the text description below. Trae will automatically pull the latest remote code via `uvx` and run it locally.

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

Field replacement description:

- `video_process_mcp`: The name of the MCP service, you can customize it as needed.
- `VOLCENGINE_ACCESS_KEY` and `VOLCENGINE_SECRET_KEY`: Please replace with the Volcano Engine AK and SK you obtained in the prerequisites.
- `MCP_TOOLS_TYPE`: Loading mode, optional `groups` (by group) or `tools` (by tool).
- `MCP_TOOLS_SOURCE`: Loading scope. You can fill in `all` to load all tools, or fill in group/tool names separated by commas like `edit,upload`. Note that Trae limits the number of single MCP tools to 10, it is recommended to load only necessary groups.
- `MCP_SPACE_NAME`: Please replace with the space name you created in the VOD console.

Complete parameter description, please see [MCP Configuration Parameter Description](/ol8o3qyn/4m0bde30).

</div>
<div type="tab-item" title="Cloud Mode (JSON URL)" key="hYNMuldBe6">

Copy the following JSON and replace it according to the text description below:

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

Field replacement description:

- `video_process_mcp`: The name of the MCP service, you can customize it as needed.
- `url`: Please replace with the exclusive Endpoint you obtained from MCP Marketplace in Step 1.
- `x-tt-access-key` and `x-tt-secret-key`: Please replace with the Volcano Engine AK and SK you obtained in the prerequisites.
- `x-tt-tools-type`: Loading mode, optional `groups` (by group) or `tools` (by tool).
- `x-tt-tools-source`: Loading scope. You can fill in `all` to load all tools, or fill in group/tool names separated by commas like `edit,upload`. Note that Trae limits the number of single MCP tools to 10, it is recommended to load only necessary groups.
- `x-tt-space-name`: Please replace with the space name you created in the VOD console.

Complete parameter description, please see [MCP Configuration Parameter Description](/ol8o3qyn/4m0bde30).

</div>
</div>

4. Confirm that the MCP status shows as green activated, as shown below.
   ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/8dce1bccd27742d3b1f357801af719fc~tplv-goo7wpa0wc-image.image)

### Step 3: Enable Agent Dialogue

Open the dialogue panel in the Trae main interface, and switch the agent at the bottom to **Builder with MCP** mode.
![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/b38f1ab590d74168b898b974d7d9240f~tplv-goo7wpa0wc-image.image)
You can give prompts directly, for example: Help me stitch beach.mp4 and sunset.mp4 in the test space together, add a "fade in and fade out" transition effect in the middle, and send me the playback address after completion.
| Stage | Content |
| --- | --- |
| **Input Video** | <video src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/1814f820a644484486417c3a40ce8ac3~tplv-goo7wpa0wc-image.image" controls width="100%"></video> <br> <video src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/9add04fef4df4aef8ae66c1507326696~tplv-goo7wpa0wc-image.image" controls width="100%"></video> |
| **Processing Process** | You will observe: <br> <br> * Autonomous Planning: The agent will automatically identify the need to call the `audio_video_stitching` tool. <br> * Asynchronous Tracking: Since cloud editing takes time, the agent will submit a task and return a task ID (TaskID), and automatically poll the progress in the background. If you find the dialogue interrupted, you can manually ask: "Is the task just now finished?" <br> * Result Delivery: After the task is completed, the agent will directly give the generated video information and preview link. <br> <br> ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/255337623fcf4cdaa2fac5776b76a97c~tplv-goo7wpa0wc-image.image) |
| **Output Video** | <video src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/faac6d11638841b2ab84953437c49560~tplv-goo7wpa0wc-image.image" controls width="100%"></video> |

# Reference Information

## Prompt Writing Suggestions

In order for the agent to call VeVOD MCP tools more accurately, it is recommended to follow the following principles when writing prompts:

- **Clarify Target Space**:
  - You can pre-specify the default video on demand space via the `x-tt-space-name` field during the MCP configuration phase. After configuring the default space, all tasks will use that space for media processing by default without repeating the declaration in every prompt.
  - If the default space is not specified in the configuration, or if you need to use another space temporarily, please clarify the target space in the prompt, for example: "Please use the my_media_space space for processing".
- **Specify Video to be Processed**: You can flexibly specify the source material to be processed in two ways:
  - **Specify by URL**: Provide the public URL of the material directly in the prompt. The system will automatically pull the file and upload it to the VOD space, and then execute subsequent processing tasks. For example: "Please help me adjust the speed of the video http://example.com/my_video.mp4 to 1.5x and generate Chinese subtitles for it."
  - **Specify by VOD Media**: If the material has been [uploaded](https://www.volcengine.com/docs/4/2887?lang=zh) to the VOD space, you can reference it directly by its Vid (Video ID) or FileName (File Name). For example: "Please help me flip the video with Vid v03103g50000cl7p8d9o346g2n9p2lp0 horizontally and improve its quality to 1080P."
- **Describe Execution Order**: For complex tasks involving multiple atomic capabilities, it is recommended to use the structure of "First... then... finally..." to explicitly describe the sequence of steps. For example: "First perform vocal separation, then perform speech transcription on the separated vocals".
- **Set Quality and Specification Boundaries**: AI output has a certain probability. Explicit parameter constraints can reduce the uncertainty of results. For example, in video enhancement tasks, clarify the expected value: "Please output the synthesized video in 1080P specification".

## Common Prompts Reference

The following table shows recommended prompts for common business scenarios. You can copy these prompts directly into the dialog box to try, and fine-tune them according to actual needs.

### **Visual Effect Transformation**

Prompt: Help me flip this video horizontally and adjust it to 2x speed playback.
| **Input Video** | **Output Video** |
| --- | --- |
| <br> <video src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/5750e89648104f9aab4ffd1421b25129~tplv-goo7wpa0wc-image.image" controls width="100%"></video> <br> | <br> <video src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/ee97af04ec7445ce91586cd34a03927f~tplv-goo7wpa0wc-image.image" controls width="100%"></video> <br> |

### **Subtitle Extraction and Automatic Burning**

Prompt: Recognize the audio in the speech_no_subtitle.mp4 video in the test space via ASR and convert it to subtitles; then add the subtitles to the original video to generate a new video.
| Input Video | Output Video |
| --- | --- |
| <br> <video src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/314e504b12de45a5892d7cc7a34aa1e2~tplv-goo7wpa0wc-image.image" controls width="100%"></video> <br> | <br> <video src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/7d05d8fab9d34ac2844170ef17a6a19a~tplv-goo7wpa0wc-image.image" controls width="100%"></video> <br> |

## MCP Configuration Parameter Description

The following table lists the core configuration items of VeVOD MCP, distinguishing between cloud deployment and local deployment. Please select the corresponding parameters according to your actual access scenario.
| **Cloud Header Field** | **Local Environment Variable** | **Example** | **Description** |
| --- | --- | --- | --- |
| x-tt-access-key | VOLCENGINE*ACCESS_KEY | AKLTMTU2M... | Volcano Engine Access Key AK |
| x-tt-secret-key | VOLCENGINE_SECRET_KEY | TnpZek5HT... | Volcano Engine Access Key SK |
| x-tt-tools-type | MCP_TOOLS_TYPE | groups or tools | Loading mode. Decides whether to load by "group" or "specific tool". |
| x-tt-tools-source <br> | MCP_TOOLS_SOURCE <br> | all or edit,upload <br> | Loading scope. <br> <br> * Full loading (all): Only effective when `x-tt-tools-type` is `groups`. Suitable for powerful models (such as GPT-4, Claude 3.5). Note that an error will occur if the total number of tools exceeds 10 in Trae. <br> * Scenario loading (edit,upload): For example, if you only need editing functions, loading only the edit group can significantly reduce Token consumption and improve AI call accuracy. |
| x-tt-host | VOLCENGINE_HOST | vod.volcengineapi.com | API domain name of VOD service |
| x-tt-region | VOLCENGINE_REGION | cn-north-1 | Region where VOD service is located |
| x-tt-session-token | VOLCENGINE_SESSION_TOKEN | ... <br> | (Optional) Fill in when using temporary credentials |

# License

MIT
