# TR MCP Server 

## 版本信息
v1.0

## 产品描述

TR MCP Server 是一个模型上下文协议(Model Context Protocol)服务器，为MCP客户端(如Claude Desktop)提供与火山引擎 TR 服务交互的能力。可以基于自然语言对云端资源进行管理，一期仅支持查询 TR 实例、带宽包实例等操作。
## 分类
网络

## 功能

- 查询满足指定条件的中转路由器实例的详细信息
- 查询满足指定条件的TR连接的详细信息

## Tools
本 MCP Server 产品提供以下 Tools (工具/能力):

业务数据查询
- `DescribeTransitRouters`: [查询满足指定条件的中转路由器实例](https://www.volcengine.com/docs/6979/156017)
- `DescribeTransitRouterAttachments`: [查询满足指定条件的TR连接](https://www.volcengine.com/docs/6979/156015)
- `DescribeTransitRouterVpcAttachments`: [查询满足指定条件的VPC类型网络实例连接](https://www.volcengine.com/docs/6979/170304)
- `DescribeTransitRouterVpnAttachments`: [查询满足指定条件的VPN类型网络实例连接](https://www.volcengine.com/docs/6979/170308)
- `DescribeTransitRouterDirectConnectGatewayAttachments`: [查询满足指定条件的专线网关类型网络实例连接](https://www.volcengine.com/docs/6979/155992)
- `DescribeTransitRouterBandwidthPackages`: [查询满足指定条件的中转路由器带宽包](https://www.volcengine.com/docs/6979/1130785)
- `DescribeTransitRouterRegions`: [查询当前账号支持的地理区域及地域](https://www.volcengine.com/docs/6979/1139502)
- `DescribeTransitRouterBandwidthPackagesBilling`: [查询中转路由器带宽包的计费信息](https://www.volcengine.com/docs/6979/1288974)
- `DescribeTransitRouterPeerAttachments`: [查询满足指定条件的跨地域连接](https://www.volcengine.com/docs/6979/1130781)
- `DescribeTransitRouterRouteTables`: [查询满足指定条件的中转路由器路由表](https://www.volcengine.com/docs/6979/170312)
- `DescribeTransitRouterRouteEntries`: [查询满足指定条件的路由条目](https://www.volcengine.com/docs/6979/170316)
- `DescribeTransitRouterRouteTableAssociations`: [查询满足指定条件的关联转发。](https://www.volcengine.com/docs/6979/170319)
- `DescribeTransitRouterRouteTablePropagations`: [查询满足指定条件的路由学习](https://www.volcengine.com/docs/6979/170322)
- `DescribeTransitRouterRoutePolicyEntries`: [查询满足指定条件的路由策略条目](https://www.volcengine.com/docs/6979/1217300)
- `DescribeTransitRouterRoutePolicyTables`: [查询满足指定条件的路由策略](https://www.volcengine.com/docs/6979/1217296)
- `DescribeTransitRouterForwardPolicyEntries`: [查询满足指定条件的转发策略条目](https://www.volcengine.com/docs/6979/1219486)
- `DescribeTransitRouterForwardPolicyTables`: [查询满足指定条件的转发策略](https://www.volcengine.com/docs/6979/1219487)
- `DescribeTransitRouterTrafficQosMarkingPolicies`: [查询满足指定条件的流标记策略](https://www.volcengine.com/docs/6979/1328793)
- `DescribeTransitRouterTrafficQosMarkingEntries`: [查询流标记策略中满足指定条件的标记规则](https://www.volcengine.com/docs/6979/1328796)
- `DescribeTransitRouterTrafficQosQueuePolicies`: [查询满足指定条件的流队列策略](https://www.volcengine.com/docs/6979/1328803)
- `DescribeTransitRouterTrafficQosQueueEntries`: [查询流队列策略中满足指定条件的队列](https://www.volcengine.com/docs/6979/1328806)

## 可适配平台

可以使用 Cline、Cursor、Claude Desktop 等支持 MCP Server 调用的客户端。

## 服务开通链接 (整体产品)

<https://www.volcengine.com/docs/6979>

## 鉴权方式

从火山引擎管理控制台获取账号 AccessKey 和 SecretKey。

### 环境变量

以下环境变量可用于配置MCP服务器:

| 环境变量                    | 描述                         | 必填 | 默认值 |
|-------------------------|----------------------------|----|-----|
| `VOLCENGINE_ACCESS_KEY` | 火山引擎账号 ACCESS KEY          | 是  | -   |
| `VOLCENGINE_SECRET_KEY` | 火山引擎账号 SECRET KEY          | 是  | -   |
| `VOLCENGINE_REGION`     | 火山引擎 Region名称（如cn-beijing） | 是  | -   |
| `VOLCENGINE_ENDPOINT`   | 火山引擎 OpenAPI Endpoint      | 是  | -   |

## 安装部署

### 系统依赖

- 安装 Python 3.11 或者更高版本
- 安装 uv
    - 如果是linux系统
  ```
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
    - 如果是window系统
  ```
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- 同步依赖项并更新uv.lock:
  ```bash
  uv sync
  ```
- 构建mcp server:
  ```bash
  uv build
  ```

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *mcp-server-transitrouter*.

#### 本地配置

添加以下配置到你的 mcp settings 文件中

```json
{
  "mcpServers": {
    "mcp-server-transitrouter": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_transitrouter",
        "mcp-server-transitrouter"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your access-key",
        "VOLCENGINE_SECRET_KEY": "your secret-key",
        "VOLCENGINE_REGION": "volcengine region",
        "VOLCENGINE_ENDPOINT": "volcengine endpoint"
      }
    }
  }
}
```

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
