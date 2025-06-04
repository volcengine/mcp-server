# Computer Use Mcp Server 

## Version
v0.1.0

## Overview

Computer Use Mcp Server is a model context protocol server that provides MCP clients with the ability to control computers. It can issue commands to computers based on natural language, such as move mouse, click mouse, type text, screenshots, etc.

## 分类
Computer Use

- Trigger mouse events (move, click, scroll, and drag)
- Trigger keyboard events (key press, type text)
- Retrieve cursor position
- Retrieve screen information (screenshot, screen size)

## Available Tools

- `move_mouse`: Move the mouse to the specified coordinates.
- `click_mouse`: Perform a mouse click with the specified button.
- `drag_mouse`: Drag the mouse to the specified coordinates.
- `scroll`: Scroll the mouse wheel.
- `press_key`: Press the specified key.
- `type_text`: Type the specified text.
- `get_cursor_position`: Retrieve the current cursor position.
- `screen_shot`: Retrieve the current screen size.


## Getting Started
### Prerequisites
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

### Usage
Start the server:

#### UV
```bash
cd mcp_serve_computer_use
uv run mcp-server-computer-use

# Start with stdio mode (default stdio)
uv run mcp-server-computer-use -t sse
```

#### Connect to the sandbox
Sandbox means the actual computer you are using. The request to mcp server will be transfered to the tool server on sandbox, which actually operating the os. So, you need to create a sandbox before operating mcp server, and configure the tool server client endpoint in the mcp server as followed.


You can deploy the Computer Use Agent application with one click through the Volcngine Function Compute Platform. For detailed steps, please refer to the [Volcengine Official Document](https://www.volcengine.com/docs/6662/1555156?QualityCheckDocumentID=23876)。


To help you understand how to properly deploy and configure MCP Server, we provide detailed [Video Tutorial](https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_sth/ljhwZthlaukjlkulzlp/ark/assistant/videos/0522.mp4)


## Configuration

### Environment Variables

The following environment variables are available for configuring the MCP server:

| Environment Variable | Description | Default Value |
|----------|------|--------|
| `MCP_SERVER_PORT` | MCP server listening port | `8000` |
| `TOOL_SERVER_ENDPOINT` | Tool server endpoint | - |

For example, set these environment variables before starting the server:

```bash
# Set fastmcp port and [tool server]() endpoint here
export MCP_SERVER_PORT=8000
export TOOL_SERVER_ENDPOINT={endpoint}
cd mcp_server_computer_use
uv run mcp-server-computer-use
```

### Run with uvx
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


# License
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
