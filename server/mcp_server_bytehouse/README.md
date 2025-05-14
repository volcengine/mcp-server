# ByteHouse MCP Server

An MCP server for ByteHouse. ByteHouse MCP Server serves as a communication bridge between large language models and ByteHouse instances, capable of efficiently transmitting information to achieve seamless docking and collaboration between the two. It also provides intelligent services throughout the entire life cycle for ByteHouse data development, query optimization, and cluster operation and maintenance. During data development, it offers precise guidance and suggestions to improve efficiency and quality. In terms of query optimization, it supports the analysis of statements and the optimization of performance. In the aspect of cluster operation and maintenance, it provides services such as monitoring the status, warning of risks, and automatic diagnosis and repair to ensure the efficient operation of the system.

## Features

### Tools

* `run_select_query`
  - Execute SQL queries on your ByteHouse cluster.
  - Input: `sql` (string): The SQL query to execute.
  - All ByteHouse queries are run with `readonly = 1` to ensure they are safe.

* `list_databases`
  - List all databases on your ByteHouse cluster.

* `list_tables`
  - List all tables in a database.
  - Input: `database` (string): The name of the database.

* `run_dml_ddl_query`
  - Execute DML or DDL queries on your ByteHouse cluster.
  - Input: `sql` (string): The SQL query to execute.

* `get_bytehouse_table_engine_doc`
  - Get ByteHouse Engine Manual.
  - Input: `doc_name` (string): The name of the doc.

## Configuration

### Running the Server

```bash
# Run the server with stdio transport (default)
mcp-bytehouse

# Run the server with SSE transport
mcp-bytehouse --transport sse
```

1. Open the Claude Desktop configuration file located at:
   - On macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

2. Add the following:

```json
{
  "mcpServers": {
    "mcp-bytehouse": {
      "command": "uvx",
      "args": [
            "--from",
            "git+https://github.com/volcengine/mcp-server@main#subdirectory=server/mcp_server_bytehouse",
            "--python",
            "3.13",
            "mcp_bytehouse",
      ],
      "env": {
        "BYTEHOUSE_HOST": "<ByteHouse-host>",
        "BYTEHOUSE_PORT": "<ByteHouse-port>",
        "BYTEHOUSE_USER": "<ByteHouse-user>",
        "BYTEHOUSE_PASSWORD": "<ByteHouse-password>",
        "BYTEHOUSE_SECURE": "true",
        "BYTEHOUSE_VERIFY": "true",
        "BYTEHOUSE_CONNECT_TIMEOUT": "30",
        "BYTEHOUSE_SEND_RECEIVE_TIMEOUT": "30"
      }
    }
  }
}
```

## License

This project is licensed under the Apache License.
