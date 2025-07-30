# Viking Memory MCP Server

This MCP server provides a tool to interact with the VolcEngine Viking Memory Service, allowing you to add and search memory from your collections. 


## Features

- Search memory on queries with customizable parameters

## Setup

### Prerequisites

- Python 3.10 or higher
- API credentials (AK/SK)

### Installation

1. Install the package:

```bash
pip install -e .
```

Or with uv (recommended):

```bash
uv pip install -e .
```

### Configuration

The server requires the following environment variables:

- `VOLCENGINE_ACCESS_KEY`: Your VolcEngine access key
- `VOLCENGINE_SECRET_KEY`: Your VolcEngine secret key

Optional environment variables:
- `MEMORY_PROJECT`: Your viking memory project name
- `MEMORY_REGION`: Your viking memory region,if not provided, will use `cn-north-1` as default
- `MEMORY_COLLECTION_NAME`: Your viking memory collection name
- `MEMORY_USER_ID`: Your userid

## Usage

### Running the Server

The server can be run with either stdio transport (for MCP integration) or SSE transport:

```bash
python -m mcp_server_vikingdb_memory.server --transport stdio
```

Or:

```bash
python -m mcp_server_vikingdb_memory.server --transport sse
```

### Available Tools

#### add_memories

Add memory to a collection in your project.

```python
add_memories(
    text="some memory"
)
```

Parameters:
- `text` (required): memory text .

#### search_memory

Search memory by query .

```python
search_memory(
    query="query"
)
```

Parameters:
- `query` (required): the query wants to retrieve from the memory store .

## MCP Integration

To add this server to your MCP configuration, add the following to your MCP settings file:

```json
{
  "mcpServers": {
    "mcp-server-vikingdb-memory": {
      "command": "uvx",
        "args": [
          "--from",
          "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_vikingdb_memory",
          "mcp-server-vikingdb-memory"
        ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your-access-key",
        "VOLCENGINE_SECRET_KEY": "your-secret-key",
        "MEMORY_PROJECT": "default",
        "MEMORY_REGION": "cn-north-1",
        "MEMORY_COLLECTION_NAME": "your-memory-collection", 
        "MEMORY_USER_ID": "your-user-id"
      }
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify your AK/SK credentials are correct
   - Check that you have the necessary permissions for the collection

2. **Connection Timeouts**
   - Check your network connection to the VolcEngine API
   - Verify the host configuration is correct

3. **Empty Results**
   - Verify the collection name is correct
   - Try broadening your search query

### Logging

The server uses Python's logging module with INFO level by default. You can see detailed logs in the console when running the server.

## Contributing

Contributions to improve the Viking Memory MCP Server are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please ensure your code follows the project's coding standards and includes appropriate tests.

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
