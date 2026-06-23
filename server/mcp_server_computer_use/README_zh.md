# Computer Use Mcp Server 

## 版本信息
v0.1.0

## 产品描述

Computer Use Mcp Server 是一个模型上下文协议服务器，为MCP客户端提供控制计算机的能力。可以基于自然语言对计算机进行指令下发，例如：移动鼠标、点击鼠标、输入文本、截屏等。

## 分类
Computer Use

## 功能

- 触发鼠标事件（移动、点击、滚动和拖动）
- 触发键盘事件（按键、输入文本）
- 获取光标位置
- 获取屏幕信息（屏幕截图、屏幕尺寸）

## Available Tools

- `move_mouse`: 将鼠标移动到指定坐标
- `click_mouse`: 使用指定按钮执行鼠标点击
- `drag_mouse`: 将鼠标拖动到指定坐标
- `scroll`: 滚动鼠标滚轮
- `press_key`: 按下指定键
- `type_text`: 输入指定文本
- `get_cursor_position`: 获取当前光标位置
- `screen_shot`: 获取当前截屏


## 使用指南

### 前置准备
- Python 3.12+
- UV

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**pip**
```bash
pip install uv
```

### 安装
克隆仓库:
```bash
git clone git@github.com:volcengine/mcp-server.git
```

### 使用方法
启动服务器:

#### UV
```bash
cd mcp_serve_computer_use
uv run mcp-server-computer-use

# 使用sse模式启动(默认为stdio)
uv run mcp-server-computer-use -t sse
```

#### Connect to the sandbox
沙盒指的是您正在使用的实际计算机。对MCP Server的请求将被转发到沙盒中实际运行操作系统的工具服务器。因此，您需要在运行MCP Server之前创建一个沙盒，并在Server中按如下方式配置Tool Server的Endpoint。


通过火山引擎函数计算平台可以一键部署Computer Use Agent应用，详细步骤请参[火山官方文档](https://www.volcengine.com/docs/6662/1555156?QualityCheckDocumentID=23876)。


为了帮助您了解如何正确部署和配置MCP Server，在此提供详细的[视频教程](https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_sth/ljhwZthlaukjlkulzlp/ark/assistant/videos/0522.mp4)


## 配置

### 环境变量

以下环境变量可用于配置MCP服务器:

| 环境变量 | 描述 | 默认值 |
|----------|------|--------|
| `MCP_SERVER_PORT` | MCP Server 端口 | `8000` |
| `TOOL_SERVER_ENDPOINT` | Tool server 地址。启用 HTTPS 时填 `https://...` | - |
| `AUTH_API_KEY` | 调用 Tool Server 时随 `X-API-Key` 请求头携带的鉴权 Key，需与 Tool Server `config.toml` 的 `auth_key` 一致；为空则不鉴权 | `""` |
| `TOOL_SERVER_ENABLE_HTTPS` | Tool Server 启用 HTTPS 时设为 `true`，SDK 将校验 TLS 服务端证书 | `false` |
| `TOOL_SERVER_CLIENT_CA` | 签发 Tool Server 服务端证书的 CA 证书绝对路径，`TOOL_SERVER_ENABLE_HTTPS=true` 时必填 | `""` |

例如，在启动服务器前设置这些环境变量:

```bash
export MCP_SERVER_PORT=8000
export TOOL_SERVER_ENDPOINT={endpoint}
export AUTH_API_KEY={your-secret-api-key}        # 可选
cd mcp_server_computer_use
uv run mcp-server-computer-use
```

### uvx 启动
```json
{
    "mcpServers": {
        "mcp-server-computer-use": {
            "command": "uvx",
            "args": [
            "--from",
            "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_computer_use",
            "mcp-server-computer-use"
          ],
            "env": {
                "MCP_SERVER_PORT": 8000,
                "TOOL_SERVER_ENDPOINT": "{endpoint}",
                "AUTH_API_KEY": "{your-secret-api-key}"
            }
        }
    }
}

```

### 鉴权与 HTTPS

默认情况下 MCP Server 与 Tool Server 之间走 HTTP 明文通信、且不做鉴权，只适合本地调试。一旦 Tool Server 暴露在受信任网络之外，建议至少启用 API Key 鉴权，最好同时启用 HTTPS，避免 `X-API-Key` 明文传输。

1. **API Key 鉴权（最低安全基线）**：在 Tool Server `config.toml` 中配置 `auth_key`，并在本 MCP Server 的环境变量 `AUTH_API_KEY` 中填入相同值。Tool Server 配置了 `auth_key` 后，未携带匹配 `X-API-Key` 的请求会返回 `401 Permission denied`。

2. **HTTPS（公网/跨机房推荐）**：在 Tool Server 启用 HTTPS（`plugins.enable_https = true`，`ssl.server_cert/server_key` 指向证书文件）；本 MCP Server 设置 `TOOL_SERVER_ENABLE_HTTPS=true` 和 `TOOL_SERVER_CLIENT_CA=/abs/path/ca.crt`，并把 `TOOL_SERVER_ENDPOINT` 协议改为 `https://`。两端 HTTPS 状态必须一致，否则 TLS 握手失败。


# 证书
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).