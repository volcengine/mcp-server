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
| `TOOL_SERVER_ENDPOINT` | Tool server 端口 | - |

例如，在启动服务器前设置这些环境变量:

```bash
export MCP_SERVER_PORT=8000
export TOOL_SERVER_ENDPOINT={endpoint}
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
                "TOOL_SERVER_ENDPOINT": "{endpoint}"
            }
        }
    }
}

```


# 证书
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
