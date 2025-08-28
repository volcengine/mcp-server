# CEN MCP Server 

## 版本信息
v1.0

## 产品描述

CEN MCP Server 是一个模型上下文协议(Model Context Protocol)服务器，为MCP客户端(如Claude Desktop)提供与火山引擎 CEN 服务交互的能力。可以基于自然语言对云端资源进行管理，一期仅支持查询 CEN 实例、带宽包实例等操作。
## 分类
网络

## 功能

- 查询满足指定条件的云企业网实例的详细信息
- 查询指定云企业网实例的详细信息

## Tools
本 MCP Server 产品提供以下 Tools (工具/能力):

业务数据查询
- `describe_cens`: [查询满足指定条件的云企业网实例的详细信息](https://www.volcengine.com/docs/6405/78275)
- `describe_cen_attributes`: [查询指定云企业网实例的详细信息](https://www.volcengine.com/docs/6405/78273)
- `describe_instance_granted_rules`: [查看满足指定条件的网络实例的跨账号授权信息](https://www.volcengine.com/docs/6405/108810)
- `describe_grant_rules_to_cen`: [查看满足指定条件的云企业网实例的跨账号授权信息](https://www.volcengine.com/docs/6405/108811)
- `describe_cen_attached_instance_attributes`: [查看指定网络实例的详情](https://www.volcengine.com/docs/6405/78279)
- `describe_cen_attached_instances`: [查询满足指定条件的网络实例](https://www.volcengine.com/docs/6405/78280)
- `describe_cen_bandwidth_packages`: [查询满足指定条件的带宽包的详细信息](https://www.volcengine.com/docs/6405/101141)
- `describe_cen_bandwidth_package_attributes`: [查询指定带宽包的详细信息](https://www.volcengine.com/docs/6405/101142)
- `describe_cen_inter_region_bandwidth_attributes`: [查询指定云企业网实例域间带宽的详细信息](https://www.volcengine.com/docs/6405/81008)
- `describe_cen_inter_region_bandwidths`: [查询满足指定条件的云企业网实例域间带宽的详细信息](https://www.volcengine.com/docs/6405/81009)
- `describe_cen_service_route_entries`: [查询满足指定条件的云服务访问路由的详细信息](https://www.volcengine.com/docs/6405/119648)
- `describe_cen_route_entries`: [查询指定云企业网实例的路由条目](https://www.volcengine.com/docs/6405/78283)
- `describe_cen_summary_route_entries`: [查询满足指定条件的CEN汇总路由](https://www.volcengine.com/docs/6405/68979)

## 可适配平台

可以使用 Cline、Cursor、Claude Desktop 等支持 MCP Server 调用的客户端。

## 服务开通链接 (整体产品)

<https://www.volcengine.com/docs/6405>

## 鉴权方式

从火山引擎管理控制台获取账号 AccessKey 和 SecretKey。

### 环境变量

以下环境变量可用于配置MCP服务器:

| 环境变量                    | 描述                         | 必填 | 默认值 |
|-------------------------|----------------------------|----|-----|
| `VOLCENGINE_ACCESS_KEY` | 火山引擎账号 ACCESS KEY          | 是  | -   |
| `VOLCENGINE_SECRET_KEY` | 火山引擎账号 SECRET KEY          | 是  | -   |
| `VOLCENGINE_REGION`     | 火山引擎 Region名称（如cn-beijing) | 是  | -   |
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
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *mcp-server-cen*.

#### 本地配置

添加以下配置到你的 mcp settings 文件中

```json
{
  "mcpServers": {
    "mcp-server-cen": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_cen",
        "mcp-server-cen"
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
