# RabbitMQ MCP Server

RabbitMQ MCP Server 是一个模型上下文协议（Model Context Protocol，MCP）服务器，为 MCP 客户端（如 Claude Desktop）提供与火山引擎 RabbitMQ 服务交互的能力。

## Tools
本 MCP Server 产品提供以下 Tools（工具/能力）：

### Tool 1: 查询可用区列表（DescribeAvailabilityZones）

#### 类型
SaaS（云 API）

#### 详细描述
查询指定地域下支持 RabbitMQ 的可用区列表，便于在创建实例或规划容灾架构时选择合适的部署位置。

#### 调试所需的输入参数
- RegionId（string）：地域 ID，例如 cn-beijing。

#### 输出
- RegionId：请求的地域 ID。
- Zones：可用区列表，每个可用区包含可用区 ID、名称等信息。

#### 最容易被唤起的 Prompt 示例
- 列出北京地域的可用区。
- 查看 cn-beijing 下可以创建 RabbitMQ 实例的可用区列表。

### Tool 2: 查询地域列表（DescribeRegions）

#### 类型
SaaS（云 API）

#### 详细描述
查询当前账号支持的 RabbitMQ 地域列表，用于选择实例部署地域或规划多地域容灾架构。

#### 调试所需的输入参数
- 无：此工具无需额外输入参数。

#### 输出
- Regions：地域列表，每个地域包含地域 ID、名称等基础信息。

#### 最容易被唤起的 Prompt 示例
- 列出当前支持 RabbitMQ 的所有地域。
- 帮我查看有哪些地域可以创建 RabbitMQ 实例。

## 可适配平台
可以使用 cline、cursor、claude desktop 或支持 MCP Server 调用的其它终端。

## 服务开通链接
[开通 RabbitMQ 服务](https://console.volcengine.com/rabbitmq)，未开通的用户会自动重定向到开通页；如果已经开通，则会跳转控制台首页。

## 鉴权方式

### 火山 OpenAPI 鉴权
通过 AK/SK（签名机制）访问火山 OpenAPI。默认从环境变量读取（推荐）。

### MCP Client 鉴权（可选）
可通过配置 `auth=oauth` 为 MCP Client 增加 OAuth 身份认证（仅 SSE 模式适用）。

## 安装部署

### 系统依赖
- 安装 Python 3.10 或者更高版本
- 安装 uv

### 安装 uv 方法
**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 安装 MCP-Server
克隆仓库:
```bash
git clone git@github.com:volcengine/mcp-server.git
```

## 运行 MCP-Server 指南

### 1. 配置文件
`server/mcp_server_rabbitmq/src/mcp_server_rabbitmq/config/cfg.yaml`

默认配置：`transport = stdio`、`credential = env`。

### 2. 协议切换
对应配置中 `transport` 参数：
- `sse`: 使用 Server-Sent Events 协议
  - `server_port`: 用来设置 SSE 端口
- `StreamableHTTP`: 使用 StreamableHTTP 协议
  - `server_port`: 用来设置 StreamableHTTP 端口
- `stdio`: 使用标准输入输出流协议

### 3. 身份认证
若期望对 MCP Client 的身份进行认证，可配置 `auth` 参数（仅适用于 SSE 协议）：
- `oauth`, 使用 OAuth 认证（需要自备 OAuth 服务）
- `none`, 不进行身份认证

### 4. 火山访问凭证
因为 MCP Server 需要调用火山 OpenAPI，因此要提供火山访问凭证信息。
对应配置中 `credential` 参数：
- `env`: 从环境变量获取 AK、SK 进行鉴权（推荐）
- `token`: 从 Header 中获取凭证（适用于 HTTP 模式，不适用于 STDIO）

### 5. 环境变量设置
- ak 环境变量名: `VOLCENGINE_ACCESS_KEY`
- sk 环境变量名: `VOLCENGINE_SECRET_KEY`
- session_token 环境变量名: `VOLCENGINE_ACCESS_SESSION_TOKEN`
- credential 环境变量名: `VOLCENGINE_CREDENTIAL_TYPE`（若设置，则优先级高于配置）
- transport 环境变量名: `MCP_SERVER_MODE`（若设置，则优先级高于配置）
- auth 环境变量名: `MCP_SERVER_AUTH`（若设置，则优先级高于配置）
- sse_port 环境变量名: `MCP_SERVER_PORT`（若设置，则优先级高于配置）

### 6. 运行

#### 本地运行（STDIO / 默认）
```bash
uv --directory server/mcp_server_rabbitmq run mcp-server-rabbitmq
```

#### 作为远程服务（SSE / StreamableHTTP）
下载代码仓库，并设置 `transport = sse`（或 `StreamableHTTP`）。
```bash
uv --directory server/mcp_server_rabbitmq run mcp-server-rabbitmq
```

## License
MIT
