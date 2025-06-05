# ARK MCP Server

An MCP server for the Volcengine ARK API. This server allows you to interact with ARK's AI capabilities, including chat completions and specialized tools.

## Features

- Chat with ARK bots using the bot_chat API
- Extract content from URLs (web pages, PDFs, Douyin videos) using the link_reader tool
- Evaluate mathematical expressions using the caculator tool
- Web search capability through ARK's web plugin

## Setup

### Creating a Zero-Code Intelligent Agent

To use the web_search capability:

1. Go to the ARK official website and create a zero-code intelligent agent
2. Enable the web plugin for your agent
3. Record the bot ID for configuration

## Configuration

The server requires the following environment variables to be set:

- `ARK_API_KEY`: Required, API key for authentication with the ARK service
- `ARK_BOT_ID`: Optional, The ID of the ARK bot to use for chat completions
- `ARK_BOT_NAME`: Required if ARK_BOT_ID is set, the name of the ARK bot
- `ARK_BOT_DESCRIPTION`: Required if ARK_BOT_ID is set, the description of the ARK bot
- `ARK_TOOL_LINK_READER`: Optional, set to "true" or "1" to enable the link reader tool
- `ARK_TOOL_CACULATOR`: Optional, set to "true" or "1" to enable the calculator tool

You can set these environment variables in your shell or use a `.env` file.

### MCP Settings Configuration

```json
{
    "mcpServers": {
        "ark": {
            "command": "uvx",
            "args": [
            "--from",
            "git+https://github.com/volcengine/ai-app-lab#subdirectory=mcp/server/mcp_server_ark",
            "mcp-server-ark",
          ],
            "env": {
                "ARK_API_KEY": "your-ark-api-key",
                "ARK_BOT_ID": "your-bot-id",
                "ARK_BOT_NAME": "your-bot-name",
                "ARK_BOT_DESCRIPTION": "your-bot-description",
                "ARK_TOOL_LINK_READER": "true",
                "ARK_TOOL_CACULATOR": "true"
            }
        }
    }
}
```

## Usage

### Running the Server

```bash
# Run the server with stdio transport (default)
mcp-server-ark

# Run the server with SSE transport
mcp-server-ark --transport sse
```

### MCP Tools

The server provides the following MCP tools:

#### bot_chat

Chat with an ARK bot using the configured bot ID.

Parameters:
- `message` (string): The message to send to the bot

Example:
```json
{
  "message": "Hello, how can you help me today?"
}
```

#### link_reader

Extract content from URLs, including web pages, PDFs, and Douyin videos.

Parameters:
- `url_list` (array of strings): List of URLs to extract content from (maximum 3)

Example:
```json
{
  "url_list": ["https://example.com", "https://example.org/document.pdf"]
}
```

#### caculator

Evaluate mathematical expressions using the ARK Calculator tool.

Parameters:
- `input` (string): The mathematical expression in Wolfram Language InputForm

Example:
```json
{
  "input": "2 + 2 * 3"
}
```

#### web_search

Search the web using ARK's web plugin. This capability is available through the bot_chat tool when using a bot with the web plugin enabled.

To use web search:
1. Configure your ARK bot with the web plugin enabled
3. Config your tool name and description in MCP settings
```shell
export ARK_BOT_ID=your bod id
export ARK_BOT_DESCRIPTION=这是联网搜索工具，如果需要搜索互联网上的内容，请使用此工具。输入为查询语句
export ARK_BOT_NAME=web_search
```

2. Use the bot_chat tool with a query that requires web search

Example:
```json
{
  "message": "What are the latest news about artificial intelligence?"
}
```

## Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging experience, we strongly recommend using the MCP Inspector.

You can launch the MCP Inspector via npm with this command:

```shell
npx @modelcontextprotocol/inspector uv --directory {{your source code local directory}}/mcp-server-ark run mcp-server-ark
```

Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.

## License

This project is licensed under the MIT License.