# GA MCP Server
火山引擎 GA 官方推出的 MCP Server，支持基于自然语言查询并分析加速器配置信息和监控数据。

| 版本 | v0.1.0 |
| :-: | :-: |
| 分类 | 全球加速 |
| 标签 | 全球加速 |


## Tools
GA MCP Server 支持查询并分析业务数据信息和域名配置信息，提供如下工具。

标准型加速器
- `ListAccelerators`: [查询标准型加速器列表](https://www.volcengine.com/docs/6737/1327567)
- `DescribeAccelerator`: [查询标准型加速器详情](https://www.volcengine.com/docs/6737/1327575)
- `ListListeners`: [查询监听器列表](https://www.volcengine.com/docs/6737/1347047)
- `DescribeListener`: [查询监听器配置](https://www.volcengine.com/docs/6737/1347049)
- `ListEndpointGroups`: [查询终端节点组列表](https://www.volcengine.com/docs/6737/1347801)
- `DescribeEndpointGroup`: [查询终端节点组详情](https://www.volcengine.com/docs/6737/1347776)
- `DescribeIPSet`: [查询指定的加速区域](https://www.volcengine.com/docs/6737/1347810)
- `DescribeListener`: [查询监听器配置详情](https://www.volcengine.com/docs/6737/1347049)


基础型加速器
- `ListBasicAccelerators`: [查询基础型加速器列表](https://www.volcengine.com/docs/6737/1347856)
- `DescribeBasicAccelerator`: [查询基础型加速器详情](https://www.volcengine.com/docs/6737/1285135)
- `ListBasicEndpointGroups`: [查询基础型加速器的终端节点组列表](https://www.volcengine.com/docs/6737/1350021)
- `DescribeBasicEndpointGroup`: [查询基础型加速器的终端节点组详情](https://www.volcengine.com/docs/6737/1350025)
- `ListBasicEndpoints`: [查询基础型加速器的终端节点](https://www.volcengine.com/docs/6737/1350029)
- `ListBasicIPSets`: [查询基础型加速器的加速区域列表](https://www.volcengine.com/docs/6737/1350601)
- `DescribeBasicIPSet`: [查询基础型加速器的加速区域详情](https://www.volcengine.com/docs/6737/1350613)
- `ListBasicAccelerateIPs`: [查询基础型加速器的加速IP列表](https://www.volcengine.com/docs/6737/1350593)

监控数据
- `DescribeStatistics`: [查询全球加速监控数据](https://www.volcengine.com/docs/6737/1350663)

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
