# MCP Server 产品名称：AI数据湖服务LAS ![产品Logo](https://lf3-static.bytednsdoc.com/obj/eden-cn/mgneh7nulmpgvhn/las/LAS%20LOGO.svg)

AI多模态数据湖服务LAS，提供多模态数据集的创建、预览、查询分析、编辑和清洗加工能力。

<table>
  <tr>
    <td>版本</td>
    <td>V1</td>
  </tr>
  <tr>
    <td>描述</td>
    <td>LAS提供多模态数据集管理及清洗能力
</td>
  </tr>
  <tr>
    <td>分类</td>
    <td>大数据-数据中台
</td>
  </tr>
  <tr>
    <td>标签</td>
    <td>多模态数据，数据集，数据湖，数据清洗
</td>
  </tr>
</table>

# Tools

## Tool 1: 获取数据集详情

### 详细描述

获取数据集详细信息，包括大小，总行数，表结构schema等信息

### 调试所需的输入参数:

输入：

```json
{
    "inputSchema": {
      "type": "object",
      "required": ["dataset_id"],
      "properties": {
        "dataset_id": {
          "description": "数据集id",
          "type": "string"
        }
      }
    },
    "name": "get_dataset_info",
    "description": "获取数据集详细信息，包括大小，总行数，表结构schema等信息"
}
```

输出：

- 输出结果描述
- 当前数据集id对应的数据集信息

### 最容易被唤起的 Prompt示例

LAS中，数据集id为ds_public的数据集是做什么的

## Tool 2: 查询数据集

### 详细描述

检索数据集，通过query，检索匹配名称的数据集

### 调试所需的输入参数:

输入：

```json
{
    "inputSchema": {
      "type": "object",
      "required": ["query"],
      "properties": {
        "query": {
          "description": "检索内容",
          "type": "string"
        }
      }
    },
    "name": "search_dataset",
    "description": "检索数据集，通过query，检索匹配名称的数据集"
}
```

输出：

- 输出结果描述
- 匹配query的数据集基本信息list

### 最容易被唤起的 Prompt示例

LAS中，有哪些关于 image 的数据集

## Tool 3: 检索数据集数据项
### 详细描述

通过query，检索特定数据集中的内容，将数据项检索出来

### 调试所需的输入参数:

输入：

```json
{
    "inputSchema": {
      "type": "object",
      "required": ["query"],
      "properties": {
        "query": {
          "description": "检索内容",
          "type": "string"
        }
      }
    },
    "name": "search_dataset_item",
    "description": "通过query，检索特定数据集中的内容，将数据项检索出来"
}
```

输出：

- 输出结果描述
- 匹配query的数据集数据内容数据项list

### 最容易被唤起的 Prompt示例

LAS中，数据集中关于 RAY 相关的内容有哪些

# 可适配平台

方舟，python，cursor， Claude Desktop

# 服务开通链接

[火山引擎AI数据湖服务LAS](https://www.volcengine.com/product/las)

# 鉴权方式

火山引擎 AKSK 鉴权体系

# 安装部署

## 系统依赖

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
- 构建cmp server:
  
  ```bash
  uv build
  ```

## 方舟

### 体验中心

[示例如下]

1. 查看MCP Server 详情
   在大模型生态广场，选择合适的MCP Server，并查看详情
2. 选择MCP Server即将运行的平台
   检查当前MCP Server 已适配的平台，并选择合适的平台
3. 查看并对比可用的Tools
   仔细查看可用的Tools的功能描述与所需的输入参数，并尝试运行对应的功能。
4. 获取专属的URL或代码示例
   检查账号登录状态与服务开通情况，生成唯一URL
5. 去对应的Client的平台进行使用
   点击快捷跳转按钮，前往方舟平台的体验中心进行对应MCP Server的体验

## 部署

### UVX

```json
{
    "mcpServers": {
        "las-dataset-mcp": {
            "command": "uvx",
            "args": [
            "--from",
            "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_las",
            "mcp-server-las"
          ],
            "env": {
                "VOLCENGINE_ACCESS_KEY": "your-access-key-id",
                "VOLCENGINE_SECRET_KEY": "your-access-key-secret",
                "LAS_DATASET_ID": "your-dataset-id"
            }
        }
    }
}
```

## License
volcengine/mcp-server is licensed under the MIT License.
