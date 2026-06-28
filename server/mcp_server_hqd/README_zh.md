# 高质量数据集多源搜索 MCP Server

## 版本信息

v0.1

## 产品描述

### 短描述

查询 HQD（高质量数据集）多源搜索服务中的企业数据，涵盖基本信息、风险、经营、知识产权和诉讼数据。

### 长描述

HQD 多源搜索 MCP Server 是一个轻量代理，连接部署在火山引擎上的远端 HQD MCP 服务。通过两阶段交互模式提供对 5 个企业数据源的统一访问：先通过 `describe_datasource` 发现元数据，再通过 `query_datasource` 检索数据。所有查询均转发到远端服务，本地不进行数据处理。

## 分类

数据智能

## 标签

企业数据、多源搜索、HQD

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: describe_datasource

获取数据源的可查询元数据信息，包括维度（dimensions）、指标（metrics）和过滤条件（filters）。Agent 应先调用此工具了解数据结构，再进行查询。

### Tool 2: query_datasource

查询指定数据源的实际数据，支持过滤、聚合和分页。支持的过滤操作符：`eq`（精确）、`like`（模糊）、`in`（批量）、`not_in`（排除）、`between`（范围）、`range`（数值范围）、`keyword`（全文搜索）。

## 可适配平台

- Python

## 鉴权方式

Bearer Token

### 获取 Auth Token

请联系 HQD 服务管理员获取认证令牌。

### 环境变量配置

| 变量名 | 值 |
| ---------- | ---------- |
| `HQD_AUTH_TOKEN` | 远端 HQD MCP 服务的认证令牌 |
| `HQD_MCP_ENDPOINT` | 远端 HQD MCP 端点地址（可选，有默认值） |

## Python 版 MCP server

### 依赖项

运行 MCP server 的设备需要安装以下依赖项。

- [Python](https://www.python.org/downloads/) 3.10 或更高版本。
- [`uv`](https://docs.astral.sh/uv/) & [`uvx`](https://docs.astral.sh/uv/guides/tools/)。

### 部署与配置

```json
{
  "mcpServers": {
    "mcp-server-hqd": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_hqd",
        "mcp-server-hqd"
      ],
      "env": {
        "HQD_AUTH_TOKEN": "Your HQD Auth Token"
      }
    }
  }
}
```

> 注：请将上方 `Your HQD Auth Token` 替换为 HQD 服务管理员提供的认证令牌。

## 使用客户端

支持通过以下客户端与 MCP Server 交互，具体配置可查阅该客户端文档。

- Cursor
- [Trae](https://www.trae.com.cn/)
- Claude Desktop
- 方舟

支持 [Cline](https://cline.bot/) 插件。

## 可用数据源

| ID | 名称 |
|----|------|
| `enterprise_basic_wide` | 企业基本信息宽表 |
| `enterprise_risk_wide` | 企业风险信息宽表 |
| `enterprise_operation_wide` | 企业经营信息宽表 |
| `enterprise_ip_wide` | 企业知识产权宽表 |
| `enterprise_litigation` | 企业诉讼信息 |

## 对话发起示例

- 列出所有可用的数据源。
- 查询名为"字节跳动"的企业基本信息。
- 搜索北京市注册资本超过1000万的企业。

## 许可

[MIT](../../LICENSE)
