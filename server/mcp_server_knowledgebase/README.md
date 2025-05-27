# Viking Knowledge Base MCP Server

This MCP server provides a tool to interact with the VolcEngine Viking Knowledge Base Service, allowing you to search and retrieve knowledge from your collections, meanwhile,
allowing you to add doc to your collections and get doc processing info by doc_id.

## Features

- Search knowledge based on queries with customizable parameters

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
- `KNOWLEDGE_BASE_PROJECT`: Your viking knowledge base project name
- `KNOWLEDGE_BASE_REGION`: Your viking knowledge base region,if not provided, will use `cn-north-1` as default
- `PORT`: Port for the FastMCP server (default: 8000)

## Usage

### Running the Server

The server can be run with either stdio transport (for MCP integration) or SSE transport:

```bash
python -m mcp_server_knowledgebase.server --transport stdio
```

Or:

```bash
python -m mcp_server_knowledgebase.server --transport sse
```

### Available Tools

#### get_collection

Get information about a viking knowledge base collection from your project .

```python
get_collection(
    collection_name="collection_name",
)
```

Parameters:
- `collection_name` (required): the name of the collection you want to get information .


#### list_collections

List all knowledge base collections of the globally configured project .

```python
list_collections(
)
```


#### search_knowledge

Search for knowledge in the configured collection based on a query.

```python
search_knowledge(
    query="How to reset my password?",
    limit=3,
    collection_name=None
)
```

Parameters:
- `query` (required): The search query string
- `limit` (optional): Maximum number of results to return (default: 3)
- `collection_name` (optional): Knowledge base collection name to search. If not provided, llm will choose some collections to search based on the description of collection

## MCP Integration

To add this server to your MCP configuration, add the following to your MCP settings file:

```json
{
  "mcpServers": {
    "knowledgebase": {
      "command": "uvx",
        "args": [
          "--from",
          "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_knowledgebase",
          "mcp-server-knowledgebase",
        ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your-access-key",
        "VOLCENGINE_SECRET_KEY": "your-secret-key", 
        "KNOWLEDGE_BASE_PROJECT": "your-project-name",
        "KNOWLEDGE_BASE_REGION": "your-region"
      },
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
