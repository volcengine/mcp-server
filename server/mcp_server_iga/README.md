# IGA MCP Server

IGA MCP Server, officially released by Volcano Engine Intelligent Global Acceleration (IGA), supports querying and analyzing business data and domain configuration information based on natural language. It is suitable for scenarios such as operation and maintenance troubleshooting and data analysis, helping to build more intelligent cloud business operation and maintenance scenarios.

| Version | v0.1.0 |
| :-: | :-: |
| Category | Intelligent Global Acceleration |
| Tags | Intelligent Global Acceleration, Full Site Acceleration, Global Acceleration, Dynamic Acceleration |

## Tools

IGA MCP Server supports querying and analyzing business data and domain configuration information, providing the following tools.

Domain Configuration Query
- `ListDomainConfig`: [Query Domain Configuration](https://www.volcengine.com/docs/6559/1171745)
- `DescribeDomainConfig`: [Query Detailed Domain Configuration](https://www.volcengine.com/docs/6559/94321)
- `DescribeDomainDetail`: [Query Single Domain Detailed Configuration](https://www.volcengine.com/docs/6559/196456)
- `ListCert`: [Query Certificate List](https://www.volcengine.com/docs/6559/1250191)

Business Data Query
- `DescribeStatistics`: [Query Resource Usage](https://www.volcengine.com/docs/6559/79733)
- `DescribeOriginStatistics`: [Query Origin Resource Usage](https://www.volcengine.com/docs/6559/79734)
- `DescribeDomainRegionData`: [Query Regional Distribution Statistics](https://www.volcengine.com/docs/6559/79738)
- `DescribeDomainIspData`: [Query ISP Distribution Statistics](https://www.volcengine.com/docs/6559/79739)
- `DescribeTopDomains`: [Query Domain Ranking Statistics](https://www.volcengine.com/docs/6559/79740)
- `DescribeTopURLs`: [Query URL Ranking Statistics](https://www.volcengine.com/docs/6559/79741)
- `DescribeTopIPs`: [Query IP Ranking Statistics](https://www.volcengine.com/docs/6559/79742)
- `DescribeTopReferers`: [Query Referer Ranking Statistics](https://www.volcengine.com/docs/6559/79743)
- `DescribeDomainPVData`: [Query PV Statistics](https://www.volcengine.com/docs/6559/79744)
- `DescribeDomainUVData`: [Query UV Statistics](https://www.volcengine.com/docs/6559/79749)

## Supported Platforms

You can use clients that support MCP Server calls, such as Cline, Cursor, Claude Desktop, etc.

## Authentication

Obtain AccessKey and SecretKey from [Volcano Engine Console - Access Control](https://console.volcengine.com/iam/identitymanage/user). Note: The AccessKey and SecretKey must have permissions for the above OpenAPIs (available tools).

## Installation & Deployment

### Environment Requirements

- Python 3.13+
- Volcano Engine account and AccessKey/SecretKey

## Deployment

### Integrate with MCP Client

```json
{
  "mcpServers": {
    "mcp-server-iga": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_iga",
        "mcp-server-iga"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "Your Volcengine AK",
        "VOLCENGINE_SECRET_KEY": "Your Volcengine SK"
      }
    }
  }
}
```

## Example

Example usage in Cursor

![Domain Query](https://lf3-static.bytednsdoc.com/obj/eden-cn/uvzhlzeh7pbyubz/mcp-server-iga/image.png)
![Top IP](https://lf3-static.bytednsdoc.com/obj/eden-cn/uvzhlzeh7pbyubz/mcp-server-iga/topip.jpeg)
![Statistics Data](https://lf3-static.bytednsdoc.com/obj/eden-cn/uvzhlzeh7pbyubz/mcp-server-iga/statistic.png)


## License

MIT
