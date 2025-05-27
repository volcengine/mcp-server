# DCDN MCP Server
火山引擎 DCDN 官方推出的 MCP Server，支持基于自然语言查询并分析域名配置信息和监控数据。

| 版本 | v0.1.0 |
| :-: | :-: |
| 分类 | 全站加速 |
| 标签 | 全站加速、动态加速 |


## Tools
IGA MCP Server 支持查询并分析业务数据信息和域名配置信息，提供如下工具。

域名配置查询
- `ListDomainConfig`: [查询域名配置](https://www.volcengine.com/docs/6559/1171745)
- `DescribeDomainConfig`: [查询域名详细配置](https://www.volcengine.com/docs/6559/94321)
- `DescribeDomainDetail`: [查询单个域名详细配置](https://www.volcengine.com/docs/6559/196456)
- `ListCert`: [查询证书列表](https://www.volcengine.com/docs/6559/1250191)

业务数据查询
- `DescribeStatistics`: [查询访问资源用量](https://www.volcengine.com/docs/6559/79733)
- `DescribeOriginStatistics`: [查询回源资源用量](https://www.volcengine.com/docs/6559/79734)
- `DescribeDomainRegionData`: [查询区域分布统计数据](https://www.volcengine.com/docs/6559/79738)
- `DescribeDomainIspData`: [查询运营商分布统计数据](https://www.volcengine.com/docs/6559/79739)
- `DescribeTopDomains`: [查询域名排行统计数据](https://www.volcengine.com/docs/6559/79740)
- `DescribeTopURLs`: [查询URL排行统计数据](https://www.volcengine.com/docs/6559/79741)
- `DescribeTopIPs`: [查询IP排行统计数据](https://www.volcengine.com/docs/6559/79742)
- `DescribeTopReferers`: [查询Referer排行统计数据](https://www.volcengine.com/docs/6559/79743)
- `DescribeDomainPVData`: [查询PV统计数据](https://www.volcengine.com/docs/6559/79744)
- `DescribeDomainUVData`: [查询UV统计数据](https://www.volcengine.com/docs/6559/79749)
- `DescribeRealtimeData`:[查询访问实时监控](https://www.volcengine.com/docs/6559/79735)
- `DescribeOriginRealtimeData`:[查询回源实时监控](https://www.volcengine.com/docs/6559/79737)

## 可适配平台  
可以使用 Cline、Cursor、Claude Desktop 等支持 MCP Server 调用的客户端。


## 鉴权方式
从[ 火山引擎控制台-访问控制 ](https://console.volcengine.com/iam/identitymanage/user)获取 AccessKey 和 SecretKey。注：AccessKey 和 SecretKey 具备上述 OpenAPI（可用工具）的权限。

## 安装部署  
### 环境要求
- 安装 Python 3.10 或者更高版本
- 安装 uv
    - 如果是linux系统
    ```
    curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
    - 如果是window系统
    ```
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
    - 同步依赖项并更uv.lock:
    ```bash
    uv sync
    ```
    - 构建mcp server:
    ```bash
    uv build
    ```

### 在 MCP Client 中集成

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
```
## 示例
Cursor 中使用示例
![域名查询](https://lf3-static.bytednsdoc.com/obj/eden-cn/uvzhlzeh7pbyubz/mcp-server-iga/image.png)
![IP排行](https://lf3-static.bytednsdoc.com/obj/eden-cn/uvzhlzeh7pbyubz/mcp-server-iga/topip.jpeg)
![统计数据](https://lf3-static.bytednsdoc.com/obj/eden-cn/uvzhlzeh7pbyubz/mcp-server-iga/statistic.png)

## License
MIT