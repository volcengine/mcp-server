# VikingDB MCP Server

This MCP server provides a tool to interact with the VolcEngine VikingDB Service, allowing you to search index from your collections.

## Features

- Search index based on query with customizable parameters

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
- `VIKING_DB_COLLECTION_NAME`: Your vikingdb collection name
- `VIKING_DB_INDEX_NAME`: Your vikingdb index name

Optional environment variables:
- `VIKING_DB_REGION`: Your vikingdb region (default: cn-north-1)
- `PORT`: Port for the FastMCP server (default: 8000)

## Usage

### Running the Server

The server can be run with either stdio transport (for MCP integration) or SSE transport:

```bash
python -m mcp_server_vikingdb.server --transport stdio
```

Or:

```bash
python -m mcp_server_vikingdb.server --transport sse
```

### Available Tools

#### search_vikingdb

Search index in the configured collection and configured index  based on a query.

```python
search_vikingdb(
    query="How to reset my password?",
    limit=3,
    collection_name=None,
    index_name=None,
)
```

Parameters:
- `query` (required): The search query string
- `limit` (optional): Maximum number of results to return (default: 3)
- `collection_name` (optional): vikingdb collection name to search. If not provided, uses the globally configured collection
- `index_name` (optional): vikingdb index name of the collection to search. If not provided, uses the globally configured index name

## MCP Integration

To add this server to your MCP configuration, add the following to your MCP settings file:

```json
{
  "mcpServers": {
    "vikingdb": {
      "command": "uvx",
        "args": [
          "--from",
          "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_vikingdb",
          "mcp-server-vikingdb"
        ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your-access-key",
        "VOLCENGINE_SECRET_KEY": "your-secret-key",
        "VIKING_DB_COLLECTION_NAME": "your-vikingdb-collection-name",
        "VIKING_DB_INDEX_NAME": "your-vikingdb-index-name", 
        "VIKING_DB_REGION": "your-vikingdb-collection-region"
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

Contributions to improve the Viking Knowledge Base MCP Server are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please ensure your code follows the project's coding standards and includes appropriate tests.

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
