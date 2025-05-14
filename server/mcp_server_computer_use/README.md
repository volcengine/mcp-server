# Computer Use Mcp Server 

## Overview

An model context protocol server for MCP client(like Claude Desktop) to control your computer. With this MCP server, clients are capable of interacting with tools that can manipulate a computer desktop environment.

## Features

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

## Configuration

MCP server's main configuration file is located at:

```
settings.toml
```

This configuration file contains key settings for the server, such as logging and tool server configurations.

TODO 补充下apikey + endpoint ｜ 模板配置阐述 | endpoint示例修改

### Environment Variables

The following environment variables are available for configuring the MCP server:

| Environment Variable | Description | Default Value |
|----------|------|--------|
| `FASTMCP_PORT` | MCP server listening port | `8000` |
| `TOOL_SERVER_ENDPOINT` | Tool server endpoint | `http://127.0.0.1:8102` |

For example, set these environment variables before starting the server:

```bash
# Set fastmcp port and [tool server]() endpoint here
export FASTMCP_PORT=8000
export TOOL_SERVER_ENDPOINT="http://127.0.0.1:8102"
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
                "FASTMCP_PORT": "8000",
                "TOOL_SERVER_ENDPOINT": "http://127.0.0.1:8102?token=..."
            }
        }
    }
}

```


# Contributing

# License
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
