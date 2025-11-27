# VOD MCP Server

一款高效便捷的视频剪辑小助手，通过对话交互的方式，实现了多视频时域拼接、长视频分段截取与拼接、添加转场动画等剪辑操作，降低了视频剪辑的技术门槛和操作成本

| 版本 | v1.0.0                    |
| ---- | ------------------------- |
| 描述 | 火山引擎 VOD 智能剪辑助手 |
| 分类 | 视频云，视频点播          |
| 标签 | 点播，视频点播，视频剪辑  |

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: audio_video_stitching

#### 功能描述

将多个音视频拼接为一个新音视频，支持 vid、url、directurl 三种输入方式

#### 最容易被唤起的 Prompt 示例

把 vid1、vid2、视频进行拼接，空间为 space1

### Tool 2: audio_video_clipping

#### 功能描述

将音视频按照指定起止时间截取，输出一个新音视频，支持 vid、url、directurl 三种输入方式

#### 最容易被唤起的 Prompt 示例

把 vid1、vid2 视频截取 第 1s 到 第 30s 时间点的内容，空间为 space1

### Tool 3: get_v_creative_task_result

#### 功能描述

查询视频创作任务结果，获取视频创作任务的处理结果，包括任务状态、处理进度、处理结果等信息。

#### 最容易被唤起的 Prompt 示例

查询 VCreativeId 视频创作任务的处理结果，空间为 space1

## 可适配平台

方舟，Cursor，Trae 等

## 服务开通链接 (整体产品)

[火山引擎-视频点播-控制台](https://www.volcengine.com/product/vod)

## 鉴权方式

请在[火山引擎-视频点播-控制台](https://www.volcengine.com/product/vod)申请 VOLCENGINE_ACCESS_KEY、VOLCENGINE_SECRET_KEY

## 安装

### 环境要求

- Python 3.13+
- 火山引擎账号及 AccessKey/SecretKey

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
