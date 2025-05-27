# DCDN MCP Server
Official MCP Server for Volcengine DCDN, supporting natural language queries to analyze domain configuration information and monitoring data.

| Version  | v0.1.0             |
| :------: | :----------------- |
| Category | Whole Site Acceleration |
| Tags     | Whole Site Acceleration, Dynamic Acceleration |


## Tools
The DCDN MCP Server supports querying and analyzing business data and domain configuration information, providing the following tools.

Domain Configuration Query
- `ListDomainConfig`: [Query Domain Configuration](https://www.volcengine.com/docs/6559/1171745)
- `DescribeDomainConfig`: [Query Detailed Domain Configuration](https://www.volcengine.com/docs/6559/94321)
- `DescribeDomainDetail`: [Query Detailed Configuration of a Single Domain](https://www.volcengine.com/docs/6559/196456)
- `ListCert`: [Query Certificate List](https://www.volcengine.com/docs/6559/1250191)

Business Data Query
- `DescribeStatistics`: [Query Resource Usage for Access](https://www.volcengine.com/docs/6559/79733)
- `DescribeOriginStatistics`: [Query Resource Usage for Origin Pull](https://www.volcengine.com/docs/6559/79734)
- `DescribeDomainRegionData`: [Query Regional Distribution Statistics](https://www.volcengine.com/docs/6559/79738)
- `DescribeDomainIspData`: [Query ISP Distribution Statistics](https://www.volcengine.com/docs/6559/79739)
- `DescribeTopDomains`: [Query Domain Ranking Statistics](https://www.volcengine.com/docs/6559/79740)
- `DescribeTopURLs`: [Query URL Ranking Statistics](https://www.volcengine.com/docs/6559/79741)
- `DescribeTopIPs`: [Query IP Ranking Statistics](https://www.volcengine.com/docs/6559/79742)
- `DescribeTopReferers`: [Query Referer Ranking Statistics](https://www.volcengine.com/docs/6559/79743)
- `DescribeDomainPVData`: [Query PV Statistics](https://www.volcengine.com/docs/6559/79744)
- `DescribeDomainUVData`: [Query UV Statistics](https://www.volcengine.com/docs/6559/79749)
- `DescribeRealtimeData`: [Query Real-time Access Monitoring](https://www.volcengine.com/docs/6559/79735)
- `DescribeOriginRealtimeData`: [Query Real-time Origin Pull Monitoring](https://www.volcengine.com/docs/6559/79737)

## Compatible Platforms
Clients that support MCP Server calls, such as Cline, Cursor, Claude Desktop, etc., can be used.


## Authentication Method
Obtain AccessKey and SecretKey from the [Volcengine Console - Access Control](https://console.volcengine.com/iam/identitymanage/user). Note: The AccessKey and SecretKey must have permissions for the OpenAPI (available tools) listed above.

## Installation and Deployment
### Environment Requirements
- Python 3.13+
- Volcengine account and AccessKey/SecretKey

## Deployment
### Integrate into MCP Client

```json
{
  "mcpServers": {
    "mcp-server-dcdn": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_dcdn",
        "mcp-server-dcdn"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "Your Volcengine AK",
        "VOLCENGINE_SECRET_KEY": "Your Volcengine SK"
      }
    }
  }
}
## 示例
Cursor 中使用示例
![Domain Query](https://lf3-static.bytednsdoc.com/obj/eden-cn/uvzhlzeh7pbyubz/mcp-server-iga/image.png)
![Top IP](https://lf3-static.bytednsdoc.com/obj/eden-cn/uvzhlzeh7pbyubz/mcp-server-iga/topip.jpeg)
![Statistics Data](https://lf3-static.bytednsdoc.com/obj/eden-cn/uvzhlzeh7pbyubz/mcp-server-iga/statistic.png)

## License
MIT