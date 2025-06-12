# MCDN MCP Server
Volcano Engine Multi-Cloud CDN officially launches the MCP Server, which supports natural language queries and analysis of domain information and monitoring data. It is suitable for scenarios such as operation and maintenance troubleshooting, data analysis, etc., helping to build more intelligent cloud business operation and maintenance scenarios.

| Version | v0.1.0 |
| :-: | :-: |
| Description | Multi-Cloud CDN Service Driven By Natural Language |
| Category | CDN And Edge |
| Tags | Multi-Cloud CDN, Business Data Analysis |

## Tools
CDN MCP Server supports querying and analyzing business data information and domain configuration information, providing the following tools.

### Cloud Account and Domain Query
- `ListCloudAccounts`: [Get cloud provider account list](https://www.volcengine.com/docs/6766/155786)
- `ListCdnDomains`: [Get third-party accelerated domain list](https://www.volcengine.com/docs/6766/165536)

### Business Data Query
- `DescribeCdnDataOffline`: [Query edge statistics data](https://www.volcengine.com/docs/6766/196433)
- `DescribeCdnOriginDataOffline`: [Query origin statistics data](https://www.volcengine.com/docs/6766/196434)
- `DescribeCdnAccessLog`: [Query access logs](https://www.volcengine.com/docs/6766/1353806)
- `DescribeCdnRegionAndIsp`: [Get region and ISP name list](https://www.volcengine.com/docs/6766/165507)

## Compatible Platforms
Can be used with clients that support MCP Server calls such as Cline, Cursor, Claude Desktop, etc.

## Service Activation Link (Overall Product)
<https://console.volcengine.com/mcdn>

## Authentication Method
Obtain AccessKey and SecretKey from [Volcano Engine Console - Access Control](https://console.volcengine.com/iam/identitymanage/user). Note: AccessKey and SecretKey must have permissions for the above OpenAPIs (available tools).

## Installation and Deployment
### System Requirements
- Python 3.10 or higher
- Install uv
  - For Linux systems:
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
    "mcp_server_mcdn": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_mcdn",
        "mcp_server_mcdn"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "Your Volcengine AK",
        "VOLCENGINE_SECRET_KEY": "Your Volcengine SK"
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


## Usage Examples

### CDN Traffic Data Analysis
| User Input | Query traffic data from the past week, compare and analyze traffic characteristics and proportions across different CDN providers, and provide traffic distribution optimization suggestions |
|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Model Inference Process | 1. Automatically decompose task execution steps based on user questions<br/>![Step 1](https://lf3-static.bytednsdoc.com/obj/eden-cn/azlafy/ljhwZthlaukjlkulzlp/mcdn_mcp/1.1.PNG)<br/>2. Call tools<br/>![Step 2](https://lf3-static.bytednsdoc.com/obj/eden-cn/azlafy/ljhwZthlaukjlkulzlp/mcdn_mcp/1.2.PNG)<br/>3. Analyze based on request data<br/>![Step 3](https://lf3-static.bytednsdoc.com/obj/eden-cn/azlafy/ljhwZthlaukjlkulzlp/mcdn_mcp/1.3.PNG) |
| Analysis Conclusion | ![Analysis Result](https://lf3-static.bytednsdoc.com/obj/eden-cn/azlafy/ljhwZthlaukjlkulzlp/mcdn_mcp/1.4.PNG) |

### CDN Service Quality Analysis
| User Input | Query overall business statistics from the past week, analyze quality differences among providers except Volcano Engine |
|------------|------------------------------------------------------------------------------------------------------------------------|
| Model Inference Process | 1. Automatically decompose task execution steps based on user questions<br/>![Step 1](https://lf3-static.bytednsdoc.com/obj/eden-cn/azlafy/ljhwZthlaukjlkulzlp/mcdn_mcp/2.1.PNG)<br/>2. Call tools<br/>![Step 2](https://lf3-static.bytednsdoc.com/obj/eden-cn/azlafy/ljhwZthlaukjlkulzlp/mcdn_mcp/2.2.PNG)<br/>3. Self-correct when encountering errors<br/>![Step 3](https://lf3-static.bytednsdoc.com/obj/eden-cn/azlafy/ljhwZthlaukjlkulzlp/mcdn_mcp/2.3.PNG)<br/>4. Analyze based on request data<br/>![Step 4](https://lf3-static.bytednsdoc.com/obj/eden-cn/azlafy/ljhwZthlaukjlkulzlp/mcdn_mcp/2.4.PNG) |
| Analysis Conclusion | ![Analysis Result](https://lf3-static.bytednsdoc.com/obj/eden-cn/azlafy/ljhwZthlaukjlkulzlp/mcdn_mcp/2.5.png) |
