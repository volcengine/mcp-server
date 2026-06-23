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
| `TOOL_SERVER_ENDPOINT` | Tool server endpoint. Use `https://...` when HTTPS is enabled. | - |
| `AUTH_API_KEY` | API key sent to tool server via the `X-API-Key` header. Must match `auth_key` configured on the tool server. Leave empty to disable authentication. | `""` |
| `TOOL_SERVER_ENABLE_HTTPS` | Set to `true` when the tool server is served over HTTPS so that the SDK validates the TLS server certificate. | `false` |
| `TOOL_SERVER_CLIENT_CA` | Absolute path to the CA certificate that signed the tool server's server certificate. Required when `TOOL_SERVER_ENABLE_HTTPS=true`. | `""` |

For example, set these environment variables before starting the server:

```bash
# Set fastmcp port and [tool server]() endpoint here
export MCP_SERVER_PORT=8000
export TOOL_SERVER_ENDPOINT={endpoint}
export AUTH_API_KEY={your-secret-api-key}        # optional
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
                "TOOL_SERVER_ENDPOINT": "{endpoint}",
                "AUTH_API_KEY": "{your-secret-api-key}"
            }
        }
    }
}

```

### Authentication & HTTPS

By default the MCP server talks to the tool server over plain HTTP without authentication, which is fine for local development. For any deployment that exposes the tool server outside a fully trusted network, you should turn on at least the API-key authentication, and ideally HTTPS as well, so that the `X-API-Key` header is not transmitted in plain text.

1. **API-key authentication (recommended baseline)**

   Configure the **same** secret value on both sides:

   - On the **tool server**, set `auth_key` in its `config.toml`.
   - On the **MCP server**, set `AUTH_API_KEY` via the environment variable above.

   When `auth_key` is set on the tool server, requests without a matching `X-API-Key` header will be rejected with `401 Permission denied`.

2. **HTTPS (recommended for any non-trusted network)**

   - On the **tool server**, enable HTTPS (`plugins.enable_https = true`) with `ssl.server_cert` and `ssl.server_key`.
   - On the **MCP server**, set `TOOL_SERVER_ENABLE_HTTPS=true` and `TOOL_SERVER_CLIENT_CA=/abs/path/ca.crt` (the CA that signed the tool server certificate). Make sure `TOOL_SERVER_ENDPOINT` uses `https://`.

   Both ends must agree on whether HTTPS is enabled, otherwise the TLS handshake will fail.


# License
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).