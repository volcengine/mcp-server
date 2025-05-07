# Volcengine MCP Server for VOD

Implementation of Model Context Protocol (MCP) Server for Volcengine VOD

## Project Overview

Volcengine VOD MCP is an MCP Server based on [Model Context Protocol](https://github.com/modelcontextprotocol/python-sdk) that integrates Volcengine VOD services into LLM model contexts, enabling large language models to directly operate and manage VOD resources.

## Key Features

- Provides multiple resource access interfaces for LLMs to obtain Volcengine VOD service information and video resources
- Implements tool encapsulation for various Volcengine functionalities including media upload and video editing

## Feature Demos
- [Multiple videos spliced by timeline example](https://lf3-static.bytednsdoc.com/obj/eden-cn/2202eh7upinuhbnnuhd/多视频按时域拼接.mp4): In Cline, splice two local videos together by specified timeline through conversation to generate a new address and return the playback URL of the synthesized video (requires domain configuration in Volcengine VOD service)
- [Video multi-segment extraction and composition example](https://lf3-static.bytednsdoc.com/obj/eden-cn/2202eh7upinuhbnnuhd/单视频多段截取.mp4): Extract video segments through conversation and splice them by timeline into a new video
- [Adding text and transition effects example](https://lf3-static.bytednsdoc.com/obj/eden-cn/2202eh7upinuhbnnuhd/添加文字及转场动画.mp4): Splice multiple videos by timeline into a new video and add transition effects and fixed text.

## Available Tools

- `get_space_detail`: [Get detailed information of specified space](https://www.volcengine.com/docs/4/107689), including region, description and creation time.
- `list_space`: [List video-on-demand spaces](https://www.volcengine.com/docs/4/107686), get information of all spaces under current account.
- `create_space`: [Create video-on-demand space](https://www.volcengine.com/docs/4/107685), space is the basic unit for resource isolation, each can be independently configured with business resources, templates, workflows and policies.
- `upload_media`: [Upload video](https://www.volcengine.com/docs/4/65647#%E4%B8%8A%E4%BC%A0%E9%9F%B3%E8%A7%86%E9%A2%91), upload local video to specified VOD space
- `submit_direct_edit_task_async`: [Submit video editing task](https://www.volcengine.com/docs/4/102240), edit video resources in specified VOD space, supporting timeline splicing, multi-segment extraction, adding text and transitions
- `get_direct_edit_progress`: [Check video editing task progress](https://www.volcengine.com/docs/4/102241), query processing progress after submitting editing task
- `get_direct_edit_result`: [Get editing task result](https://www.volcengine.com/docs/4/102242)
- `upload_by_url`: [URL video upload](https://www.volcengine.com/docs/4/4652), upload video to specified VOD space by pulling from URL
- `get_play_info`: [Get video playback information](https://www.volcengine.com/docs/4/2918), including playback URL, cover image etc.
- `list_domain`: [List domains](https://www.volcengine.com/docs/4/106062), query all domain lists configured under specified space
- `get_media_info`: [Query media information](https://www.volcengine.com/docs/4/1256363), get media info by Vid (Video ID), including basic info, source files and processed output files
- `get_media_list`: [Get audio/video information](https://www.volcengine.com/docs/4/69205), get audio/video info by specified Vid (Video ID).

## Installation

### Requirements

- Python 3.13+
- Volcengine account with AccessKey/SecretKey

## Usage

### Integration in Mcp Client

Configure MCP service in mcp client with this JSON:

```json
{
  "mcpServers": {
    "vevod": {
      "command": "uvx",
      "args": [
          "--from",
          "git+https://github.com/volcengine/mcp-server#subdirectory=mcp_server_vod",
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

Apply for VOLCENGINE_ACCESS_KEY and VOLCENGINE_SECRET_KEY at [Volcengine VOD Console](https://www.volcengine.com/product/vod)
