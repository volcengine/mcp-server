# MCP Server CloudSearch
| 版本 | v1                                          |
|:---|:--------------------------------------------|
| 描述 | 云搜索服务（Cloud Search）是火山引擎提供的全托管一站式信息检索和分析平台  |
| 分类 | 数据库                                         |
| 标签 | ES，Elasticsearch，OpenSearch，搜索              |

## Tools
本 MCP Server 产品提供以下 Tools (工具/能力):
### 1. describe_zones
 - 查询可用区列表
### 2. describe_instances
 - 查询云搜索实例列表，以及实例配置详情
### 3. create_instance_in_one_step
 - 创建实例（立刻运行并开始计费）。支持创建 ElasticSearch (ES) 或 OpenSearch (OS) 实例。
### 4. describe_node_available_specs
 - 查询可用的节点类型、节点规格和存储规格列表，并会返回计费配置码
### 5. describe_instance_plugins
 - 查询实例中已经安装的插件列表
### 6. rename_instance
 - 修改目标实例名称
### 7. modify_maintenance_setting
 - 修改实例的可维护时间
### 8. modify_deletion_protection
 - 启停实例的删除保护功能
### 9. describe_instance
 - 查询指定实例的配置详情
### 10. restart_node
 - 重启实例的特定成员节点
### 11. describe_instance_nodes
 - 查询实例的成员节点详情，包括节点类型、运行状态、资源配置等信息
### 12. create_instance
 - 创建实例（仅下单，待支付）。支持创建 ElasticSearch (ES) 或 OpenSearch (OS) 实例。

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
  - `cn-beijing': 华北2（北京）
  - `cn-shanghai': 华东2（上海）
  - `cn-guangzhou': 华南1（广州）
  - `cn-hongkong': 中国香港
  - `ap-southeast-1': 亚太东南（柔佛）
  - `ap-southeast-3': 亚太东南（雅加达）

### 部署
添加以下配置到你的 mcp settings 文件中
```json
{
  "mcpServers": {
    "mcp-server-cloudsearch": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_cloudsearch",
        "mcp-server-cloudsearch"
      ],
      "env": {
        "VOLCENGINE_REGION": "cn-beijing",
        "VOLCENGINE_ACCESS_KEY": "your_volcengine_ak",
        "VOLCENGINE_ACCESS_KEY": "your_volcengine_sk"
      }
    }
  }
}
```
或者克隆仓库到本地, 从本地代码仓库中启动
```json
{
  "mcpServers": {
    "mcp-server-cloudsearch": {
      "command": "uv",
      "args": [
        "--directory",
        "path/to/server/mcp_server_cloudsearch/src/ESCloud",
        "run",
        "server.py"
      ],
      "env": {
        "VOLCENGINE_REGION": "cn-beijing",
        "VOLCENGINE_ACCESS_KEY": "your_volcengine_ak",
        "VOLCENGINE_ACCESS_KEY": "your_volcengine_sk"
      }
    }
  }
}
```

## License
[MIT](https://github.com/volcengine/mcp-server/blob/main/LICENSE)