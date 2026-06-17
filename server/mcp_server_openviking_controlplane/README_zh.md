# OpenViking 控制面 — MCP Server + CLI

OpenViking 控制面（topapi）的 MCP Server **与** CLI —— 用于管理 OV 库
（`Collection`）。两个前端共用同一套核心（`client.py`），新增一个能力即可同时被 MCP
和 CLI 使用。

覆盖 6 个核心控制面 Action：

| Action | MCP tool | CLI 命令 |
|---|---|---|
| `ListOpenVikingCollections` | `list_collections` | `ov-cp list` |
| `CreateOpenVikingCollection` | `create_collection` ⚠️ | `ov-cp create` |
| `GetOpenVikingCollection` | `get_collection` | `ov-cp get <rid>` |
| `DeleteOpenVikingCollection` | `delete_collection` ⚠️ | `ov-cp delete <rid>` |
| `GetOpenVikingUsage` | `get_usage` | `ov-cp usage <rid>` |
| `GetOpenVikingCollectionUserAccess` | `get_collection_api_key` | `ov-cp api-key <rid>` |

## 端点

控制面 TopAPI 接口已编译进 OpenViking **数据面集群**，每个 Action 由数据面网关在如下路径提供：

```text
{endpoint}/api/openviking/{Action}
# 默认 endpoint：https://api.vikingdb.cn-beijing.volces.com/openviking
# 完整 URL 例：https://api.vikingdb.cn-beijing.volces.com/openviking/api/openviking/ListOpenVikingCollections
```

Action 在 **path** 里（不走 `?Action=&Version=` query）。请求体是该 Action 的参数（如
`{"ResourceID": "..."}`）。

> 默认 endpoint 指向**预留**的公网数据面网关（尚未对外开放）。本地/联调时用
> `--endpoint` / `VIKING_ENDPOINT` 指向一个 `kubectl port-forward`，例如
> `http://localhost:18080`。

## 鉴权

唯一方式：**Ark AgentPlan ApiKey**，作为 `Authorization: Bearer <key>` 头随每个请求发送
（后端 `authorizeControlPlaneByArk` 只认 Bearer，**不兼容 `X-API-Key`**）。鉴权是可插拔的
（`common/auth.py` → `BearerTokenAuth`），后续要换 AK/SK 签名时只需替换这一处。

> ⚠️ `create` 等写接口要求账号已**开通 AgentPlan 抵扣**，否则返回 `ProductUnordered`；
> 只读接口（list/get/usage/delete）不受此限。

### 配置

| 项 | 环境变量 | CLI 参数 | 默认 |
|---|---|---|---|
| 控制面 endpoint（base URL） | `VIKING_ENDPOINT` | `--endpoint` / `-e` | `https://api.vikingdb.cn-beijing.volces.com/openviking` |
| AgentPlan ApiKey | `AGENTPLAN_API_KEY` | `--api-key` / `-k` | —（必填） |
| 默认 project | `OPENVIKING_PROJECT` | `--project` | `default` |

## CLI 用法

```bash
uv sync                      # 或：pip install -e .

# 把 key 用环境变量配一次，之后免传参
export AGENTPLAN_API_KEY=ark-xxxxxxxx

# 只读
uv run ov-cp list
uv run ov-cp get   <ResourceID>
uv run ov-cp usage <ResourceID>
uv run ov-cp api-key <ResourceID>

# 建库（消耗付费配额；source=agentplan 时只需 --name，
#       模型名取默认、模型 ApiKey 回落到配置的 key）
uv run ov-cp create --name my_kb

# 删库（不可逆）
uv run ov-cp delete <ResourceID> --yes
```

命令行参数优先于环境变量。端点默认指向公网网关；仅在测试时（如指向 port-forward）才用
`-e` / `VIKING_ENDPOINT` 覆盖：`uv run ov-cp -e http://localhost:18080 list`。
`ov-cp --help` 不需要任何配置即可运行。

## MCP 用法（stdio / uvx）

Server 默认 **stdio** 传输，可被任意 MCP 客户端作为子进程拉起。`.mcp.json` 配置：

```json
{
  "mcpServers": {
    "openviking-controlplane": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_openviking_controlplane",
        "mcp-server-openviking-controlplane"
      ],
      "env": {
        "AGENTPLAN_API_KEY": "ark-xxxxxxxx"
      }
    }
  }
}
```

本地开发可改指向你的代码检出：

```json
{
  "mcpServers": {
    "openviking-controlplane": {
      "command": "uv",
      "args": ["run", "--directory", "/abs/path/server/mcp_server_openviking_controlplane",
               "mcp-server-openviking-controlplane"],
      "env": {
        "AGENTPLAN_API_KEY": "ark-xxxxxxxx"
      }
    }
  }
}
```

需要 SSE 时：`mcp-server-openviking-controlplane --transport sse`。

> ⚠️ `create_collection` / `delete_collection` 会创建/销毁**付费**资源，且已暴露为 MCP
> tool；其描述会要求模型先与你确认。最终拦截依赖客户端的工具授权弹窗。
