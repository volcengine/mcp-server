# CDN MCP Server
火山引擎 CDN 官方推出的 MCP Server，支持基于自然语言查询并分析业务数据和域名配置信息，适用于运维排障、数据分析等场景，助力构建更智能的云业务运维场景。

| 版本 | v0.1.0 |
| :-: | :-: |
| 描述 | 通过自然语言驱动CDN服务 |
| 分类 | CDN与边缘 |
| 标签 | CDN、 内容分发网络、业务数据分析、域名配置分析 |

## Tools
CDN MCP Server 支持查询并分析业务数据信息和域名配置信息，提供如下工具。

业务数据查询

- `DescribeDistrictData`: [获取访问统计的细分数据](https://www.volcengine.com/docs/6454/1228873)
- `DescribeEdgeData`: [获取计费区域的细分数据](https://www.volcengine.com/docs/6454/1229443)
- `DescribeDistrictSummary`: [获取访问统计的汇总数据](https://www.volcengine.com/docs/6454/1229447)
- `DescribeEdgeSummary`: [获取计费区域的汇总数据](https://www.volcengine.com/docs/6454/1229442)
- `DescribeOriginData`: [获取回源统计的细分数据](https://www.volcengine.com/docs/6454/1229441)
- `DescribeOriginSummary`: [获取回源统计的汇总数据](https://www.volcengine.com/docs/6454/1229451)
- `DescribeUserData`: [获取独立访客的细分数据](https://www.volcengine.com/docs/6454/1230197)
- `DescribeDistrictRanking`: [获取访问数据的统计排名](https://www.volcengine.com/docs/6454/1229445)
- `DescribeEdgeRanking`: [获取计费区域的统计排名](https://www.volcengine.com/docs/6454/1229448)
- `DescribeOriginRanking`: [获取回源数据的统计排名](https://www.volcengine.com/docs/6454/1229444)
- `DescribeEdgeStatusCodeRanking`: [获取访问状态码的统计排名](https://www.volcengine.com/docs/6454/1229449)
- `DescribeOriginStatusCodeRanking`: [获取回源状态码的统计排名](https://www.volcengine.com/docs/6454/1229450)
- `DescribeStatisticalRanking`: [获取热门对象的统计排名](https://www.volcengine.com/docs/6454/1230196)
- `DescribeOriginTopStatisticalData`: [获取 TOP 回源 URL](https://www.volcengine.com/docs/6454/1213039)


域名配置查询

- `DescribeCdnConfig`: [获取加速域名配置](https://www.volcengine.com/docs/6454/80320)
- `ListCdnDomains`: [获取加速域名列表](https://www.volcengine.com/docs/6454/75269)


## 可适配平台  
可以使用 Cline、Cursor、Claude Desktop 等支持 MCP Server 调用的客户端。

## 服务开通链接（整体产品）
<https://console.volcengine.com/cdn>


## 鉴权方式
从[ 火山引擎控制台-访问控制 ](https://console.volcengine.com/iam/identitymanage/user)获取 AccessKey 和 SecretKey。注：AccessKey 和 SecretKey 具备上述 OpenAPI（可用工具）的权限。

## 安装

### 环境要求

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
- 火山引擎账号及 AccessKey/SecretKey

## 部署

### 在 MCP Client 中集成

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

### 环境变量

以下环境变量可用于配置 MCP 服务器:

| 环境变量 | 描述 | 默认值 |
|----------|------|--------|
| VOLCENGINE_ACCESS_KEY | 火山引擎账号 AccessKey | - |
| VOLCENGINE_SECRET_KEY | 火山引擎账号 SecretKey | - |



## 使用示例

### 业务数据分析

| 用户输入 | 查询 CDN 过去一周的带宽数据，分析带宽峰值时间点的特征，并给出参考结论。 | 
|----------|------|
| 任务拆解 |  1.分析用户输入<br/><img src="https://lf3-static.bytednsdoc.com/obj/eden-cn/lm-pa/ljhwZthlaukjlkulzlp/mcp-icons/1e0a1a4a-22b2-4fc1-b305-3e85f796aa96.png" alt="图片alt" title="图片title"><br/>2.调用工具<br/><img src="https://lf3-static.bytednsdoc.com/obj/eden-cn/lm-pa/ljhwZthlaukjlkulzlp/mcp-icons/eae12383-6d8c-42c4-af81-7f1716037e95.png" alt="图片alt" title="图片title"><br/><img src="https://lf3-static.bytednsdoc.com/obj/eden-cn/lm-pa/ljhwZthlaukjlkulzlp/mcp-icons/0ceaf9f6-8f0c-42bd-83f0-fb104bf8e18f.png" alt="图片alt" title="图片title"><br/>|
| 分析结论 | <img src="https://lf3-static.bytednsdoc.com/obj/eden-cn/lm-pa/ljhwZthlaukjlkulzlp/mcp-icons/6fb3f79d-97a5-457e-8138-e7c6d8a345c7.png" alt="图片alt" title="图片title"><br/>|


### 域名配置分析

| 用户输入 | 查询 CDN 域名（选取前 100 个域名）的配置信息，查看这些域名的配置特征，挖掘更多信息供参考。如项目组、标签、上下线状态、加速区域、证书配置等维度。 | 
|----------|------|
| 任务拆解 |  <img src="https://lf3-static.bytednsdoc.com/obj/eden-cn/lm-pa/ljhwZthlaukjlkulzlp/mcp-icons/1.png" alt="图片alt" title="图片title"><br/><img src="https://lf3-static.bytednsdoc.com/obj/eden-cn/lm-pa/ljhwZthlaukjlkulzlp/mcp-icons/2.png" alt="图片alt" title="图片title"><br/>|
| 初步分析 | <img src="https://lf3-static.bytednsdoc.com/obj/eden-cn/lm-pa/ljhwZthlaukjlkulzlp/mcp-icons/3.png" alt="图片alt" title="图片title"><br/>|
| 持续提问 | <img src="https://lf3-static.bytednsdoc.com/obj/eden-cn/lm-pa/ljhwZthlaukjlkulzlp/mcp-icons/4.png" alt="图片alt" title="图片title"><br/>|
| 深度分析 | <img src="https://lf3-static.bytednsdoc.com/obj/eden-cn/lm-pa/ljhwZthlaukjlkulzlp/mcp-icons/5.png" alt="图片alt" title="图片title"><br/>|


## License
MIT
