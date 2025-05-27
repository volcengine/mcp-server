# GA MCP Server
Official MCP Server for Volcengine GA (Global Accelerator), supporting natural language queries to analyze accelerator configuration information and monitoring data.

| Version  | v0.1.0        |
| :------: | :------------ |
| Category | Global Accelerator |
| Tags     | Global Accelerator |


## Tools
The GA MCP Server supports querying and analyzing business data and domain configuration information, providing the following tools.

Standard Accelerators
- `ListAccelerators`: [Query Standard Accelerator List](https://www.volcengine.com/docs/6737/1327567)
- `DescribeAccelerator`: [Query Standard Accelerator Details](https://www.volcengine.com/docs/6737/1327575)
- `ListListeners`: [Query Listener List](https://www.volcengine.com/docs/6737/1347047)
- `DescribeListener`: [Query Listener Configuration](https://www.volcengine.com/docs/6737/1347049)
- `ListEndpointGroups`: [Query Endpoint Group List](https://www.volcengine.com/docs/6737/1347801)
- `DescribeEndpointGroup`: [Query Endpoint Group Details](https://www.volcengine.com/docs/6737/1347776)
- `DescribeIPSet`: [Query Specified Acceleration Region](https://www.volcengine.com/docs/6737/1347810)
- `DescribeListener`: [Query Listener Configuration Details](https://www.volcengine.com/docs/6737/1347049)


Basic Accelerators
- `ListBasicAccelerators`: [Query Basic Accelerator List](https://www.volcengine.com/docs/6737/1347856)
- `DescribeBasicAccelerator`: [Query Basic Accelerator Details](https://www.volcengine.com/docs/6737/1285135)
- `ListBasicEndpointGroups`: [Query Endpoint Group List for Basic Accelerators](https://www.volcengine.com/docs/6737/1350021)
- `DescribeBasicEndpointGroup`: [Query Endpoint Group Details for Basic Accelerators](https://www.volcengine.com/docs/6737/1350025)
- `ListBasicEndpoints`: [Query Endpoints for Basic Accelerators](https://www.volcengine.com/docs/6737/1350029)
- `ListBasicIPSets`: [Query Acceleration Region List for Basic Accelerators](https://www.volcengine.com/docs/6737/1350601)
- `DescribeBasicIPSet`: [Query Acceleration Region Details for Basic Accelerators](https://www.volcengine.com/docs/6737/1350613)
- `ListBasicAccelerateIPs`: [Query Acceleration IP List for Basic Accelerators](https://www.volcengine.com/docs/6737/1350593)

Monitoring Data
- `DescribeStatistics`: [Query Global Accelerator Monitoring Data](https://www.volcengine.com/docs/6737/1350663)

## Compatible Platforms
Clients that support MCP Server calls, such as Cline, Cursor, Claude Desktop, etc., can be used.


## Authentication Method
Obtain AccessKey and SecretKey from the [Volcengine Console - Access Control](https://console.volcengine.com/iam/identitymanage/user). Note: The AccessKey and SecretKey must have permissions for the OpenAPI (available tools) listed above.

## Installation and Deployment
### Environment Requirements
- Install Python 3.10 or higher
- Install uv
    - For Linux systems:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
    - For Windows systems:
    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
    - Sync dependencies and update uv.lock:
    ```bash
    uv sync
    ```
    - Build mcp server:
    ```bash
    uv build
    ```
### Integrate into MCP Client

```json
{
  "mcpServers": {
    "mcp-server-ga": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_ga",
        "mcp-server-ga"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "Your Volcengine AK",
        "VOLCENGINE_SECRET_KEY": "Your Volcengine SK"
      }
    }
  }
}
```

## License
MIT