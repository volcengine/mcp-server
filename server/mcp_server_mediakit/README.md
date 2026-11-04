# MediaKit MCP Server

MediaKit MCP Server is a standard AI capability plugin for Volcano Engine AI MediaKit. It is built on [FastMCP](https://gofastmcp.com/servers/server) and the MCP (Model Context Protocol), exposing cloud media capabilities such as video editing, audio processing, subtitle processing, and video enhancement as tools that can be called by AI agents. With MediaKit MCP, developers can use natural language to drive intelligent media production workflows.

| Field       | Value                                                             |
| ----------- | ----------------------------------------------------------------- |
| Version     | v1.0.0                                                            |
| Description | MediaKit MCP intelligent media assistant                          |
| Categories  | Media cloud, audio/video editing, video enhancement               |
| Tags        | MCP, MediaKit, video editing, audio processing, video enhancement |

## Tool Overview

MediaKit MCP provides tools that cover the full workflow from asynchronous task query to deep media editing and video enhancement. All tools support dynamic loading by group or by tool name to optimize agent reasoning efficiency. Tool filtering applies to both `tools/list` and `tools/call`; tools in the `shared` group (such as `query_task`) are always available.

## Architecture

MediaKit MCP Server is implemented with standalone **FastMCP** and two middleware layers:

| Component | Responsibility |
| --- | --- |
| `ToolFilterMiddleware` | Filter visible and callable tools by `x-mcp-domains` / `x-mcp-tools` (HTTP) or `MCP_DOMAINS` / `MCP_TOOLS` (stdio) |
| `ClientBindMiddleware` | Bind a `MediakitClient` to the current request context before each tool call |
| `get_client()` | Tool handlers obtain the bound client through request-scoped context |

Local stdio mode passes the API key through the `MEDIAKIT_API_KEY` environment variable. Cloud HTTP mode expects each client request to carry `x-amk-api-key`. They refer to the same MediaKit credential with different transports. Do not set a shared `MEDIAKIT_API_KEY` on the server for multi-tenant deployments.

Per-tool English descriptions are not published for this Volcengine surface because the complete approved English copy set is not available. Use [README_zh.md](./README_zh.md) for the canonical tool catalog.

# Quick Start in Trae

Trae is an AI-native IDE with strong agent collaboration capabilities. By connecting MediaKit MCP, you can call cloud media processing capabilities in Trae with natural language and quickly complete tasks such as video editing, subtitle processing, audio processing, and video enhancement.

## Prerequisites

- Prepare a valid MediaKit API key.
- Confirm the MediaKit service endpoint. If not explicitly configured, the default is `https://mediakit.cn-beijing.volces.com`.
- Install the [Trae client](https://www.trae.com.cn/).
- For local mode or self-hosted cloud mode, make sure `uvx` is installed in your local environment. Run `uvx --version` to check. If it is not installed, follow the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).

## Steps

### Step 1: Choose an Access Mode

Choose one of the following modes based on your usage scenario:

| Mode                        | Best for                                                           | Access method                                                                                  |
| --------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| **Local Mode (JSON Local)** | Personal debugging, quick trials, no self-hosted service required. | Use `uvx` to launch MediaKit MCP directly from the `mcp-server` repository subdirectory.       |
| **Cloud Mode (JSON URL)**   | Team sharing, long-term usage, centralized operations.             | Deploy MediaKit MCP Server yourself, then connect using the deployed Streamable HTTP endpoint. |

### Step 2: Add MCP Configuration

1. Open Trae and click the settings button in the top-right corner.
2. In the MCP tab, click **Add** > **Add Manually**.
3. Copy the JSON configuration for your selected mode and replace the fields as described below.

#### Local Mode (JSON Local)

Copy the following JSON and replace the fields as needed. Trae uses `uvx` to fetch the remote code and run it locally.

```json
{
  "mcpServers": {
    "mediakit_mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_mediakit",
        "mcp-server-mediakit"
      ],
      "env": {
        "MEDIAKIT_API_KEY": "your-api-key",
        "MCP_DOMAINS": "editing,video"
      }
    }
  }
}
```

**Field replacement notes:**

- `mediakit_mcp`: The MCP service name. You can customize it.
- `MEDIAKIT_API_KEY`: Replace with your MediaKit API key.
- `MEDIAKIT_ENDPOINT`: Optional MediaKit service endpoint override. Omit it to use `https://mediakit.cn-beijing.volces.com`.
- `MCP_DOMAINS`: Load tools by group, for example `editing,video`. To load tools by exact tool name, use `MCP_TOOLS` instead.

To load by tool name, use a configuration like this:

```json
{
  "mcpServers": {
    "mediakit_mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_mediakit",
        "mcp-server-mediakit"
      ],
      "env": {
        "MEDIAKIT_API_KEY": "your-api-key",
        "MCP_TOOLS": "trim_video,query_task"
      }
    }
  }
}
```

#### Cloud Mode (JSON URL)

Cloud mode does not provide a prebuilt deployment URL. Before using this mode, you need to deploy MediaKit MCP Server yourself and make sure the service is reachable through Streamable HTTP. After deployment, record the service URL, for example `https://your-domain/mcp`, and then connect it in Trae as shown below.

A simple startup example is:

```bash
# Multi-tenant: do not set a shared MEDIAKIT_API_KEY on the server
export MCP_SERVER_HOST="0.0.0.0"
export MCP_SERVER_PORT="8000"
export STREAMABLE_HTTP_PATH="/mcp"
export STATLESS_HTTP="true"

uvx --from "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_mediakit" mcp-server-mediakit --transport streamable-http
```

For local development from source:

```bash
cd mcp_server_mediakit
uv sync
# Optional for single-tenant local testing only
# export MEDIAKIT_API_KEY="your-api-key"
uv run mcp-server-mediakit --transport streamable-http
```

After deployment, copy the following JSON and replace the fields as needed:

```json
{
  "mcpServers": {
    "mediakit_mcp": {
      "url": "https://your-domain/mcp",
      "headers": {
        "x-amk-api-key": "your-api-key",
        "x-mcp-domains": "editing,video"
      }
    }
  }
}
```

**Field replacement notes:**

- `mediakit_mcp`: The MCP service name. You can customize it.
- `url`: Replace with your self-hosted MediaKit MCP Streamable HTTP URL, such as `https://your-domain/mcp`.
- `x-amk-api-key`: MediaKit API key for cloud HTTP mode. **Header takes precedence** over the server process `MEDIAKIT_API_KEY`. Omit it only when the server already has a single-tenant key in the environment.
- `x-mcp-domains`: Load tools by group, for example `editing,video`. To load tools by exact tool name, use `x-mcp-tools` instead.

To load by tool name, use a configuration like this:

```json
{
  "mcpServers": {
    "mediakit_mcp": {
      "url": "https://your-domain/mcp",
      "headers": {
        "x-amk-api-key": "your-api-key",
        "x-mcp-tools": "trim_video,query_task"
      }
    }
  }
}
```

4. Make sure the MCP status is shown as active in Trae.

### Step 3: Start Agent Conversations

Open the chat panel in Trae and switch the agent mode to one that supports MCP. Then you can directly issue natural language instructions such as:

- Trim this video to the first 10 seconds and output a new video.
- Add Chinese subtitles to this video with font size 28.
- Remove the subtitles at the bottom of this video, then enhance the processed video quality.
- Concatenate these two audio files, and if the task is asynchronous, continue querying until the final result is ready.

## Usage Notes

- Synchronous tasks return results directly.
- Asynchronous tasks return a `task_id`, and you need to call `query_task` to get task status and results.
- Normal calls omit `client_token`; the runtime only forwards a value explicitly supplied by the caller.
- For an explicit retry of the same logical request, reuse the same `client_token`. Changed business parameters start a new logical request.
- The MCP runtime does not infer retry intent or generate `client_token`.

## MCP Configuration Reference

The table below lists the core MediaKit MCP configuration fields for cloud mode and local mode.

<table>
  <thead>
    <tr>
      <th>Cloud header</th>
      <th>Local environment variable</th>
      <th>Example</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>-</td>
      <td>MEDIAKIT_API_KEY</td>
      <td>your-api-key</td>
      <td>Required for stdio/local mode. Not used as the primary credential in cloud HTTP mode.</td>
    </tr>
    <tr>
      <td>x-amk-api-key</td>
      <td>-</td>
      <td>your-api-key</td>
      <td><b>Cloud HTTP:</b> per-tenant key via `x-amk-api-key`. If omitted, falls back to the server process `MEDIAKIT_API_KEY` for single-tenant deployments.</td>
    </tr>
    <tr>
      <td>x-mediakit-endpoint</td>
      <td>MEDIAKIT_ENDPOINT</td>
      <td>https://mediakit.cn-beijing.volces.com</td>
      <td>Optional MediaKit endpoint override. Header takes precedence over the process environment variable.</td>
    </tr>
    <tr>
      <td>x-mcp-domains</td>
      <td>MCP_DOMAINS</td>
      <td>editing,video</td>
      <td>Load tools by group. Separate multiple groups with commas. Applies to both listing and calling tools. The `shared` group is always loaded.</td>
    </tr>
    <tr>
      <td>x-mcp-tools</td>
      <td>MCP_TOOLS</td>
      <td>trim_video,query_task</td>
      <td>Load tools by tool name. Separate multiple tool names with commas. Applies to both listing and calling tools.</td>
    </tr>
  </tbody>
</table>

For self-hosted cloud mode, you can also configure the following startup parameters:

| Environment variable   | Default value | Description                                      |
| ---------------------- | ------------- | ------------------------------------------------ |
| `MCP_SERVER_HOST`      | `0.0.0.0`     | MCP service bind address.                        |
| `MCP_SERVER_PORT`      | `8000`        | MCP service listening port.                      |
| `STREAMABLE_HTTP_PATH` | `/mcp`        | Streamable HTTP path.                            |
| `STATLESS_HTTP`        | `true`        | Whether to run Streamable HTTP in stateless mode. |

## Tool Details

Per-tool English descriptions are not published for this Volcengine surface because the complete approved English copy set is not available. Use [README_zh.md](./README_zh.md) for the canonical tool catalog.

## License

MIT
