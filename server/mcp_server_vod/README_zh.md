# VOD MCP Server
一款高效便捷的视频剪辑小助手，通过对话交互的方式，实现了多视频时域拼接、长视频分段截取与拼接、添加转场动画等剪辑操作，降低了视频剪辑的技术门槛和操作成本

| 版本 | v1.0.0                   | 
|----|--------------------------|
| 描述 | 火山引擎 VOD 智能剪辑助手 |
| 分类 | 视频云，视频点播                       |
| 标签 | 点播，视频点播，视频剪辑              |


## 功能演示
- [多个视频按时域拼接为一个视频示例](https://lf3-static.bytednsdoc.com/obj/eden-cn/2202eh7upinuhbnnuhd/多视频按时域拼接.mp4)：在 Trae 中通过对话将两个本地视频按指定时域拼接在一起合成一个新的地址，并返回合成视频的播放地址（这一步需要已在火山引擎 VOD 服务中配置域名）
- [视频多段截取合成示例](https://lf3-static.bytednsdoc.com/obj/eden-cn/2202eh7upinuhbnnuhd/单视频多段截取.mp4) ：可以通过对话将视频分段截取，再按时域拼接为一个新的视频
- [添加文字及转场动画示例](https://lf3-static.bytednsdoc.com/obj/eden-cn/2202eh7upinuhbnnuhd/添加文字及转场动画.mp4)：将多个视频按时域拼接为一个新视频，并针对新视频添加转场动画效果以及固定文案。

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: [get_space_detail](https://www.volcengine.com/docs/4/107689) 

#### 详细描述

 获取指定空间的详细信息 ，包含所属地域、空间描述以及空间创建时间等信息

#### 最容易被唤起的Prompt示例
调用 get_space_detail 获取空间详情

### Tool 2:  [list_space](https://www.volcengine.com/docs/4/107686)

#### 详细描述

查询用户视频点播空间列表，可获取当前账号下所有空间的信息

#### 最容易被唤起的Prompt示例
调用 list_space 获取空间列表

### Tool 3:  [create_space](https://www.volcengine.com/docs/4/107685)

#### 详细描述
创建视频点播空间，空间是资源隔离的基本单位，每个空间可以独立配置业务资源、业务模板、业务流和业务策略

#### 最容易被唤起的Prompt示例
调用 create_space 创建点播空间

### Tool 4: [upload_media](https://www.volcengine.com/docs/4/65647#%E4%B8%8A%E4%BC%A0%E9%9F%B3%E8%A7%86%E9%A2%91)

#### 详细描述
上传本地视频，可上传本地视频到视频点播指定空间

#### 最容易被唤起的Prompt示例
调用 upload_media 上传本地视频

### Tool 5: [submit_direct_edit_task_async](https://www.volcengine.com/docs/4/102240)
#### 详细描述
 提交视频剪辑任务 ，可对视频点播指定空间下的视频资源进行剪辑，可以实现多视频按时域拼接、单视频多端截取、增加文字及转场动画
#### 最容易被唤起的Prompt示例
调用 submit_direct_edit_task_async 提交剪辑任务

## Tool 6: [get_direct_edit_progress](https://www.volcengine.com/docs/4/102241)

#### 详细描述
 查询视频剪辑任务处理进度，提交剪辑任务后可以查询剪辑任务处理进度

#### 最容易被唤起的Prompt示例
调用 get_direct_edit_progress 查询剪辑任务处理进度

## Tool 7: [get_direct_edit_result](https://www.volcengine.com/docs/4/102242)

#### 详细描述
查询剪辑任务处理结果

#### 最容易被唤起的Prompt示例
调用 get_direct_edit_result 查询剪辑任务处理结果

## Tool 8: [get_play_info](https://www.volcengine.com/docs/4/2918)
#### 详细描述
获取视频播放信息，可获取视频播放信息，包括播放地址、封面等

#### 最容易被唤起的Prompt示例
调用 get_play_info 查询视频播放地址

## Tool 9: [list_domain](https://www.volcengine.com/docs/4/106062)


#### 详细描述
查询域名列表，查询用户指定空间下配置的全量域名列表

#### 最容易被唤起的Prompt示例
调用 list_domain 查询点播空间配置的域名

## Tool 10: [get_media_info](https://www.volcengine.com/docs/4/1256363)

#### 详细描述
查询媒资信息，通过 Vid（视频 ID）获取媒资信息，包含基础信息、片源信息及媒体处理输出文件信息

#### 最容易被唤起的Prompt示例
调用 get_media_info 查询视频详细信息

## Tool 11: [get_media_list](https://www.volcengine.com/docs/4/69205)

#### 详细描述
 获取音视频信息，获取指定 Vid（视频 ID）的音视频信息

#### 最容易被唤起的Prompt示例
调用 get_media_list 查询点播空间媒资列表

## 可适配平台  
方舟，Cursor，Trae 等

## 服务开通链接 (整体产品)  
[火山引擎-视频点播-控制台](https://www.volcengine.com/product/vod)

## 鉴权方式  
请在[火山引擎-视频点播-控制台](https://www.volcengine.com/product/vod)申请VOLCENGINE_ACCESS_KEY、VOLCENGINE_SECRET_KEY

## 安装

### 环境要求

- Python 3.13+
- 火山引擎账号及AccessKey/SecretKey

## 部署
### 在 MCP Client 中集成

在 mcp client 中配置 mcp 服务, 配置的 MCP JSON：
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