# 多云CDN MCP Server
火山引擎 多云CDN 官方推出的 MCP Server，支持自然语言查询并分析域名信息和监控数据，适用于运维排障、数据分析等场景，助力构建更智能的云业务运维场景。

| 版本 | v0.1.0 |
| :-: | :-: |
| 描述 | 通过自然语言驱动多云CDN服务 |
| 分类 | CDN与边缘 |
| 标签 | 多云CDN、业务数据分析 |

## Tools
CDN MCP Server 支持查询并分析业务数据信息和域名配置信息，提供如下工具。

云账号与域名查询

- `ListCloudAccounts`: [获取云服务商账号列表](https://www.volcengine.com/docs/6766/155786)
- `ListCdnDomains`: [获取第三方加速域名列表](https://www.volcengine.com/docs/6766/165536)


业务数据查询

- `DescribeCdnDataOffline`: [查询边缘统计数据](https://www.volcengine.com/docs/6766/196433)
- `DescribeCdnOriginDataOffline`: [查询回源统计数据](https://www.volcengine.com/docs/6766/196434)
- `DescribeCdnAccessLog`: [查询访问日志](https://www.volcengine.com/docs/6766/1353806)
- `DescribeCdnRegionAndIsp`: [获取地区和运营商名称列表](https://www.volcengine.com/docs/6766/165507)


## 可适配平台  
可以使用 Cline、Cursor、Claude Desktop 等支持 MCP Server 调用的客户端。

## 服务开通链接（整体产品）
<https://console.volcengine.com/mcdn>


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

### 环境变量

以下环境变量可用于配置 MCP 服务器:

| 环境变量 | 描述 | 默认值 |
|----------|------|--------|
| VOLCENGINE_ACCESS_KEY | 火山引擎账号 AccessKey | - |
| VOLCENGINE_SECRET_KEY | 火山引擎账号 SecretKey | - |



## 使用示例

### CDN流量数据分析

| 用户输入 | 查询过去一周的流量数据，对比分析不同CDN服务商的流量特征及比例，并给出流量分配优化建议 | 
|----------|------|
| 模型推理过程 |  1. 根据用户问题，自动拆解任务执行步骤<br/><img src="https://lf3-static.bytednsdoc.com/obj/eden-cn/azlafy/ljhwZthlaukjlkulzlp/mcdn_mcp/1.1.PNG" alt="图片alt" title="图片title"><br/>2.调用工具<br/><img src="https://lf3-static.bytednsdoc.com/obj/eden-cn/azlafy/ljhwZthlaukjlkulzlp/mcdn_mcp/1.2.PNG" alt="图片alt" title="图片title">3.3. 基于请求数据进行分析<br/><img src="https://lf3-static.bytednsdoc.com/obj/eden-cn/azlafy/ljhwZthlaukjlkulzlp/mcdn_mcp/1.3.PNG" alt="图片alt" title="图片title"><br/><br/>|
| 分析结论 | <img src="https://lf3-static.bytednsdoc.com/obj/eden-cn/azlafy/ljhwZthlaukjlkulzlp/mcdn_mcp/1.4.PNG" alt="图片alt" title="图片title"><br/>|


### CDN服务质量分析

| 用户输入 | 查询过去一周整体的业务统计数据，分析除火山引擎外各服务商的质量差异 | 
|----------|------|
| 模型推理过程 | 1.根据用户问题，自动拆解任务执行步骤 <img src="https://lf3-static.bytednsdoc.com/obj/eden-cn/azlafy/ljhwZthlaukjlkulzlp/mcdn_mcp/2.1.PNG" alt="图片alt" title="图片title"><br/>2.调用工具<img src="https://lf3-static.bytednsdoc.com/obj/eden-cn/azlafy/ljhwZthlaukjlkulzlp/mcdn_mcp/2.2.PNG" alt="图片alt" title="图片title"><br/>3.调用报错时自主修正<img src="https://lf3-static.bytednsdoc.com/obj/eden-cn/azlafy/ljhwZthlaukjlkulzlp/mcdn_mcp/2.3.PNG" alt="图片alt" title="图片title">4.基于请求数据进行分析<img src="https://lf3-static.bytednsdoc.com/obj/eden-cn/azlafy/ljhwZthlaukjlkulzlp/mcdn_mcp/2.4.PNG" alt="图片alt" title="图片title"><br/>|
| 分析结论 | <img src="https://lf3-static.bytednsdoc.com/obj/eden-cn/azlafy/ljhwZthlaukjlkulzlp/mcdn_mcp/2.5.png" alt="图片alt" title="图片title"><br/>|



## License
MIT
