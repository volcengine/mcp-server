# VOD MCP Server
![Product Logo](https://lf3-static.bytednsdoc.com/obj/eden-cn/2202eh7upinuhbnnuhd/vod_small.svg)

## Version Info
v1

## Product Description
### Volcano Engine VOD Smart Editing Assistant
An efficient and convenient video editing assistant that enables multi-video timeline splicing, long video segmentation and splicing, adding transition animations and other editing operations through conversational interaction, lowering the technical threshold and operational costs of video editing.

## Category
Video Cloud, Video on Demand

## Tags
VOD, Video on Demand, Video Editing

## Feature Demos
- [Example of splicing multiple videos by timeline](https://lf3-static.bytednsdoc.com/obj/eden-cn/2202eh7upinuhbnnuhd/多视频按时域拼接.mp4): In Trae, through conversation, two local videos are spliced together at specified time intervals to create a new address, and returns the playback address of the synthesized video (this step requires having configured a domain in Volcano Engine VOD service)
- [Example of multi-segment video extraction and composition](https://lf3-static.bytednsdoc.com/obj/eden-cn/2202eh7upinuhbnnuhd/单视频多段截取.mp4): Through conversation, videos can be segmented and extracted, then spliced together by timeline to create a new video
- [Example of adding text and transition animations](https://lf3-static.bytednsdoc.com/obj/eden-cn/2202eh7upinuhbnnuhd/添加文字及转场动画.mp4): Multiple videos are spliced together by timeline to create a new video, with transition animation effects and fixed text added to the new video.

## Tools

This MCP Server product provides the following Tools (capabilities):

### Tool 1: [get_space_detail](https://www.volcengine.com/docs/4/107689) 

#### Detailed Description
Get detailed information of a specified space, including region, space description and creation time.

#### Prompt Example
Call get_space_detail to get space details

### Tool 2: [list_space](https://www.volcengine.com/docs/4/107686)

#### Detailed Description
Query user's video on demand space list, can get information of all spaces under current account.

#### Prompt Example
Call list_space to get space list

### Tool 3: [create_space](https://www.volcengine.com/docs/4/107685)

#### Detailed Description
Create video on demand space. Space is the basic unit of resource isolation, each space can independently configure business resources, business templates, business flows and business strategies.

#### Prompt Example
Call create_space to create VOD space

### Tool 4: [upload_media](https://www.volcengine.com/docs/4/65647#%E4%B8%8A%E4%BC%A0%E9%9F%B3%E8%A7%86%E9%A2%91)

#### Detailed Description
Upload local videos, can upload local videos to specified VOD space.

#### Prompt Example
Call upload_media to upload local videos

### Tool 5: [submit_direct_edit_task_async](https://www.volcengine.com/docs/4/102240)
#### Detailed Description
Submit video editing tasks, can edit video resources in specified VOD space, enabling multi-video timeline splicing, single video multi-segment extraction, adding text and transition animations.
#### Prompt Example
Call submit_direct_edit_task_async to submit editing task

## Tool 6: [get_direct_edit_progress](https://www.volcengine.com/docs/4/102241)

#### Detailed Description
Query video editing task processing progress, can query editing task processing progress after submission.

#### Prompt Example
Call get_direct_edit_progress to query editing task progress

## Tool 7: [get_direct_edit_result](https://www.volcengine.com/docs/4/102242)

#### Detailed Description
Query editing task processing result.

#### Prompt Example
Call get_direct_edit_result to query editing task result

## Tool 8: [get_play_info](https://www.volcengine.com/docs/4/2918)
#### Detailed Description
Get video playback information, can get video playback information including playback address, cover etc.

#### Prompt Example
Call get_play_info to query video playback address

## Tool 9: [list_domain](https://www.volcengine.com/docs/4/106062)

#### Detailed Description
Query domain list, query all domain lists configured under user's specified space.

#### Prompt Example
Call list_domain to query VOD space configured domains

## Tool 10: [get_media_info](https://www.volcengine.com/docs/4/1256363)

#### Detailed Description
Query media asset information, get media asset information through Vid (video ID), including basic information, source information and media processing output file information.

#### Prompt Example
Call get_media_info to query video details

## Tool 11: [get_media_list](https://www.volcengine.com/docs/4/69205)

#### Detailed Description
Get audio/video information, get audio/video information of specified Vid (video ID).

#### Prompt Example
Call get_media_list to query VOD space media asset list

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
