# MCP Server CloudSearch
| 版本 | v1                                          |
|:---|:--------------------------------------------|
| 描述 | 云搜索服务（Cloud Search）是火山引擎提供的全托管一站式信息检索和分析平台  |
| 分类 | 数据库                                         |
| 标签 | ES，Elasticsearch，OpenSearch，搜索              |

## Tools
本 MCP Server 产品提供以下 Tools (工具/能力)，已按功能类别整理如下：

### 基础资源查询
用于查询创建实例所需的基础环境与规格信息。

- **`describe_zones`**
  获取当前地域下支持部署云搜索实例的可用区（Zones）列表。
- **`describe_node_available_specs`**
  查询可用的节点规格、存储类型及对应的计费配置码，用于辅助实例创建时的资源选型。

### 实例生命周期管理 
用于管理实例的创建、部署与初始化流程。

- **`create_instance`**
  创建一个新的云搜索实例订单（支持 Elasticsearch 或 OpenSearch）。
  *注意：此接口仅生成待支付订单，需完成支付后才会开始部署资源。*
- **`create_instance_in_one_step`**
  一步完成云搜索实例的创建与支付（支持 Elasticsearch 或 OpenSearch）。
  *注意：调用成功后实例将立即开始部署并进入计费状态。*

### 实例信息查询
用于获取实例及其组件的详细状态、配置与拓扑信息。

- **`describe_instances`**
  查询实例列表。支持按 ID、名称、状态、版本等条件进行过滤，返回包含规格、网络及维护窗口等维度的详细配置。
- **`describe_instance`**
  精确查询指定实例的完整详情。需提供实例 ID，返回比列表查询更详尽的配置数据。
- **`describe_instance_nodes`**
  列出实例内的所有成员节点详情，包含节点角色（如 Master/Data）、硬件规格、IP 地址及实时运行状态。
- **`describe_instance_plugins`**
  获取实例当前已安装的插件列表，包含插件名称、版本号及启用状态。

### 实例配置与运维
用于修改实例属性及执行关键的运维操作。

- **`rename_instance`**
  更新指定实例的显示名称（Alias），便于业务识别与管理。
- **`modify_maintenance_setting`**
  设置或调整实例的可维护时间窗口，系统将在该时段内进行必要的升级或补丁更新。
- **`modify_deletion_protection`**
  开启或关闭实例的“删除保护”功能，防止实例因误操作被意外释放。
- **`restart_node`**
  对实例中的指定节点执行重启操作，通常用于故障恢复或某些配置的强制生效。

## 可适配平台  
方舟、Trae、Cursor、Python

## 服务开通链接 (整体产品)
https://console.volcengine.com/es/region:es+cn-beijing/v2/create?projectName=default

## 安装部署  

### 依赖
- Python >= 3.11
- UV

### 环境配置
| 环境变量 | 描述 | 默认值 | 是否必选 |
| :--- | :--- | :--- | :--- |
| `VOLCENGINE_ACCESS_KEY` | 访问密钥 | - | 是 |
| `VOLCENGINE_SECRET_KEY` | 私有密钥 | - | 是 |
| `VOLCENGINE_REGION` | 区域 | `cn-beijing` | 否 |

- 请从 [volcengine](https://www.volcengine.com/docs/6291/65568) 获取 ak/sk。
- 默认区域为 `cn-beijing`，当前支持的区域代码如下：
  - `cn-beijing`: 华北2（北京）
  - `cn-shanghai`: 华东2（上海）
  - `cn-guangzhou`: 华南1（广州）
  - `cn-hongkong`: 中国香港
  - `ap-southeast-1`: 亚太东南（柔佛）
  - `ap-southeast-3`: 亚太东南（雅加达）

### 部署
添加以下配置到你的 mcp settings 文件中
```json
{
  "mcpServers": {
    "CloudSearch": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_cloudsearch",
        "mcp-server-cloudsearch"
      ],
      "env": {
        "VOLCENGINE_REGION": "cn-beijing",
        "VOLCENGINE_ACCESS_KEY": "your_volcengine_ak",
        "VOLCENGINE_SECRET_KEY": "your_volcengine_sk"
      }
    }
  }
}
```
或者克隆仓库到本地, 从本地代码仓库中启动
```json
{
  "mcpServers": {
    "CloudSearch": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/mcp-server/server/mcp_server_cloudsearch/src/ESCloud",
        "run",
        "server.py"
      ],
      "env": {
        "VOLCENGINE_REGION": "cn-beijing",
        "VOLCENGINE_ACCESS_KEY": "your_volcengine_ak",
        "VOLCENGINE_SECRET_KEY": "your_volcengine_sk"
      }
    }
  }
}
```

## License
[MIT](https://github.com/volcengine/mcp-server/blob/main/LICENSE)