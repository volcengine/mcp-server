# CDN MCP Server

Volcano Engine CDN officially launches the MCP Server, which supports natural language queries and analysis of business data and domain configuration information. It is suitable for scenarios such as operation and maintenance troubleshooting, data analysis, etc., helping to build more intelligent cloud business operation and maintenance scenarios.

|   Version   |                                        v0.1.0                                        |
| :---------: | :----------------------------------------------------------------------------------: |
| Description |                  CDN Service Management Driven By Natural Language                   |
|  Category   |                                     CDN And Edge                                     |
|    Tags     | CDN, Content Delivery Network, Business Data Analysis, Domain Configuration Analysis |


## Tools

The CDN MCP Server supports querying and analyzing business data information and domain configuration information, providing the following tools.

Business Data Query

- `DescribeDistrictData`: [Get detailed access statistics](https://www.volcengine.com/docs/6454/1228873)
- `DescribeEdgeData`: [Get detailed billing area data](https://www.volcengine.com/docs/6454/1229443)
- `DescribeDistrictSummary`: [Get summary access statistics](https://www.volcengine.com/docs/6454/1229447)
- `DescribeEdgeSummary`: [Get summary billing area data](https://www.volcengine.com/docs/6454/1229442)
- `DescribeOriginData`: [Get detailed origin statistics](https://www.volcengine.com/docs/6454/1229441)
- `DescribeOriginSummary`: [Get summary origin statistics](https://www.volcengine.com/docs/6454/1229451)
- `DescribeUserData`: [Get detailed unique visitor data](https://www.volcengine.com/docs/6454/1230197)
- `DescribeDistrictRanking`: [Get access data ranking](https://www.volcengine.com/docs/6454/1229445)
- `DescribeEdgeRanking`: [Get billing area data ranking](https://www.volcengine.com/docs/6454/1229448)
- `DescribeOriginRanking`: [Get origin data ranking](https://www.volcengine.com/docs/6454/1229444)
- `DescribeEdgeStatusCodeRanking`: [Get access status code ranking](https://www.volcengine.com/docs/6454/1229449)
- `DescribeOriginStatusCodeRanking`: [Get origin status code ranking](https://www.volcengine.com/docs/6454/1229450)
- `DescribeStatisticalRanking`: [Get hot object ranking](https://www.volcengine.com/docs/6454/1230196)
- `DescribeOriginTopStatisticalData`: [ Get TOP origin URLsL](https://www.volcengine.com/docs/6454/1213039)


Domain Configuration Query

- `DescribeCdnConfig`: [Get accelerated domain configuration](https://www.volcengine.com/docs/6454/80320)
- `ListCdnDomains`: [Get accelerated domain list](https://www.volcengine.com/docs/6454/75269)


## Compatible Platforms
Can be used with clients that support MCP Server calls such as Cline, Cursor, Claude Desktop, etc.

## Service Activation Link (Overall Product)
<https://console.volcengine.com/cdn>


## Authentication Method

Obtain AccessKey and SecretKey from [ Volcano Engine Console - Access Control ](https://console.volcengine.com/iam/identitymanage/user). Note: AccessKey and SecretKey must have the permissions for the above OpenAPIs (available tools).



## Installation

### System Requirements

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
- Volcano Engine account and AccessKey/SecretKey

## Deployment

### Integrate into MCP Client

```json
{
  "mcpServers": {
    "mcp-server-cdn": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_cdn",
        "mcp_cdn"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "Your Volcengine AccessKey",
        "VOLCENGINE_SECRET_KEY": "Your Volcengine SecretKey"
      }
    }
  }
}
```

### Environment Variables

The following environment variables can be used to configure the MCP server:

| Environment Variable | Description | Default Value |
|----------------------|-------------|---------------|
| VOLCENGINE_ACCESS_KEY | Volcano Engine account AccessKey | - |
| VOLCENGINE_SECRET_KEY | Volcano Engine account SecretKey | - |

## License
MIT
