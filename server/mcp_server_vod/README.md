# Volcengine MCP

Volcengine VOD 的 Model Context Protocol (MCP) Server 实现

## 项目简介

Volcengine VOD MCP是一个基于[Model Context Protocol](https://github.com/modelcontextprotocol/python-sdk)的 MCP Server，
它将 Volcengine VOD服务集成到LLM模型上下文中，使大模型能够直接操作和管理VOD资源。

## 功能特点

- 提供多种资源访问接口，便于LLM获取Volcengine VOD服务信息、视频资源等
- 实现了多个Volcengine功能的工具封装，包括上传媒资，剪辑视频等

## Available Tools

- `get_space_detail`: [get space details](https://www.volcengine.com/docs/4/107689)
- `list_space`: [list available spaces for the user](https://www.volcengine.com/docs/4/107686)
- `create_space`: [create VOD space](https://www.volcengine.com/docs/4/107685)
- `upload_media`: [upload media](https://www.volcengine.com/docs/6396/76279)
- `submit_direct_edit_task_async`: [submit direct async edit task ](https://www.volcengine.com/docs/4/102240)
- `cancel_direct_edit_task`: [cancel direct edit task](https://www.volcengine.com/docs/4/1250179)
- `get_direct_edit_progress`: [get direct edit progress](https://www.volcengine.com/docs/4/102241)
- `get_direct_edit_result`: [get direct edit result](https://www.volcengine.com/docs/4/102242)
- `upload_by_url`: [upload by url](https://www.volcengine.com/docs/4/4652)
- `get_play_info`: [get video play info](https://www.volcengine.com/docs/4/2918)
- `list_domain`: [list domain](https://www.volcengine.com/docs/4/106062)
- `get_media_info`: [get media info](https://www.volcengine.com/docs/4/1256363)
- `update_publish_status`: [update publish status](https://www.volcengine.com/docs/4/4709)
- `get_media_list`: [get media list](https://www.volcengine.com/docs/4/69205)

## 安装

### 环境要求

- Python 3.13+
- 火山引擎账号及AccessKey/SecretKey

## 使用方法

### 在 Mcp Client 中集成

在 mcp client 中配置 mcp 服务, 配置的 MCP JSON：

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

请在[火山引擎-视频点播-控制台](https://www.volcengine.com/product/vod)申请VOLCENGINE_ACCESS_KEY、VOLCENGINE_SECRET_KEY