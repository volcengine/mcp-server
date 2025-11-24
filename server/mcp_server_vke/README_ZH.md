# VKE MCP Server

## 版本信息
v0.1.0

## 产品描述

VKE(Volcengine Kubernetes Engine) MCP Server 是实现了模型上下文协议（Model Context Protocol）的服务器，可集成到 MCP 客户端（如 Trae、Cursor 等）中，提供与火山引擎 VKE 服务交互的能力，使用自然语言实现集群管理、节点与节点池管理、组件管理等操作，同时支持查询与管理 K8s 集群的资源以及应用 YAML 配置到 K8s 集群。

## 分类

容器服务

## 标签

容器服务、K8s、VKE

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

VKE 集群、节点、节点池、组件等管理操作：

- create_addon: 创建组件
- create_cluster: 创建集群
- create_default_node_pool: 创建默认节点池
- create_kubeconfig: 创建 kubeconfig
- create_node_pool: 创建节点池
- create_nodes: 创建节点
- create_virtual_node: 创建虚拟节点
- list_addons: 查询组件列表
- list_clusters: 查询集群列表
- list_kubeconfigs: 查询 kubeconfig 列表
- list_node_pools: 查询节点池列表
- list_nodes: 查询节点列表
- list_supported_addons: 查询支持的组件
- list_supported_resource_types: 查询支持的资源类型
- list_virtual_nodes: 查询虚拟节点列表
- update_addon_config: 更新组件配置
- update_addon_version: 更新组件版本

K8s 资源管理操作：

- apply_yaml: 应用 YAML 配置到 K8s 集群
- list_k8s_resources: 查询 K8s 资源列表
- manage_k8s_resources: 管理 K8s 资源（如创建、删除、更新 K8s 资源）


注意：暂时不支持删除、更新集群或者节点池、节点等操作。

## 可适配平台

Trae、Cursor

## 服务开通链接（整体产品）

[火山引擎 - 容器服务 VKE](https://console.volcengine.com/vke)

## 鉴权方式

在 IAM 控制台创建 API Key（AccessKey/SecretKey）并确保该 API Key 具备 VKE 的 `VKEFullAccess` 权限 。

## 安装部署  

### 安装依赖

- Python 3.11+
- UV

### 环境配置

环境变量：

| 环境变量 | 描述 | 默认值 | 是否必选 |
| :--- | :--- | :--- | :--- |
| `VOLCENGINE_ACCESS_KEY` | 访问密钥 | - | 是 |
| `VOLCENGINE_SECRET_KEY` | 私有密钥 | - | 是 |
| `VOLCENGINE_SESSION_TOKEN`| 临时会话令牌 | - | 否 |
| `VOLCENGINE_REGION` | 区域 | `cn-beijing` | 否 |
| `ALLOW_WRITE` | 是否开启写权限，允许更新、删除操作 | `false` | 否 |
| `MCP_SERVER_MODE` | 是否开启远程部署模式 | `local` | 否 |

注意：

- 所有创建、查询操作不受 `ALLOW_WRITE` 影响
- 更新与删除集群、节点、节点池、伸缩策略等不受 `ALLOW_WRITE` 影响，这些操作均不支持
- 当 `ALLOW_WRITE` 为 `true` 时，将支持：
  - 更新、删除 K8s 资源（通过 manage_k8s_resources 工具）
  - 更新 Addon 版本与配置

默认地域为 `cn-beijing`，当前支持的地域代码以及对应的地域名称：

- `cn-beijing`：华北2（北京）
- `cn-beijing2`：华北3（北京）
- `cn-datong`：华北4（大同）
- `cn-wulanchabu`：华北5（乌兰察布）
- `cn-shanghai`：华东2（上海）
- `cn-guangzhou`：华南1（广州）
- `cn-hongkong`：中国香港
- `ap-southeast-1`：亚太东南（柔佛）
- `ap-southeast-3`：亚太东南（雅加达）

### 部署在 Trae 中

在 Trae 中手动添加 MCP，配置如下：

```json
{
  "mcpServers": {
    "vke": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_vke",
        "mcp-server-vke"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "YOUR_AK",
        "VOLCENGINE_SECRET_KEY": "YOUR_SK",
        "VOLCENGINE_REGION": "YOUR_REGION",
        "ALLOW_WRITE": "false", // 注意，请仅在必要时开启写权限，避免操作失误导致数据丢失
      }
    }
  }
}
```

## License

MIT
