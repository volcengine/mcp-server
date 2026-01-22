# RocketMQ MCP Server

RocketMQ MCP Server 是一个模型上下文协议(Model Context Protocol)服务器，为MCP客户端(如Claude Desktop)提供与火山引擎RocketMQ服务交互的能力。可以基于自然语言对云端实例资源进行巡检信息、地域、可用区的查询操作以及风险巡检的开关操作，实现RocketMQ资源的高效管理。


| 版本 | v0.1.0 |
| :-: | :-: |
| 描述 | 自然语言驱动 RocketMQ 运维新体验 |
| 分类 | 云基础-消息队列 |
| 标签 | RocketMQ，消息队列，MCP |

## Tools
本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: 查询可用区列表（DescribeAvailabilityZones）

#### 类型

SaaS（云 API）

#### 详细描述

查询指定地域下支持 RocketMQ 的可用区列表，便于在创建实例或规划容灾架构时选择合适的部署位置。

#### 调试所需的输入参数

- RegionId（string）：地域 ID，例如 cn-beijing。

#### 输出

- RegionId：请求的地域 ID。
- Zones：可用区列表，每个可用区包含可用区 ID、名称等信息。

#### 最容易被唤起的 Prompt 示例

- 列出北京地域的可用区。
- 查看 cn-beijing 下可以创建 RocketMQ 实例的可用区列表。

### Tool 2: 查询地域列表（DescribeRegions）

#### 类型

SaaS（云 API）

#### 详细描述

查询当前账号支持的 RocketMQ 地域列表，用于选择实例部署地域或规划多地域容灾架构。

#### 调试所需的输入参数

- 无：此工具无需额外输入参数。

#### 输出

- Regions：地域列表，每个地域包含地域 ID、名称等基础信息。

#### 最容易被唤起的 Prompt 示例

- 列出当前支持 RocketMQ 的所有地域。
- 帮我查看有哪些地域可以创建 RocketMQ 实例。

### Tool 3: 开启或关闭实例风险巡检（EnableInstanceInspect）

#### 类型

SaaS（云 API）

#### 详细描述

为指定实例开启或关闭风险巡检功能，用于按需启用巡检、控制告警数量或在变更前临时关闭巡检。

#### 调试所需的输入参数

- InstanceId（string）：实例 ID。
- Enable（boolean）：是否开启风险巡检，true 表示开启，false 表示关闭。

#### 输出

- 空对象或 OK 状态：表示实例风险巡检开关操作已执行成功。

#### 最容易被唤起的 Prompt 示例

- 帮我为实例 rocketmq-xxxx 开启风险巡检功能。
- 关闭实例 rocketmq-xxxx 的风险巡检开关。

### Tool 4: 查询巡检规则配置（GetInspectConfig）

#### 类型

SaaS（云 API）

#### 详细描述

查询指定实例已配置的巡检规则及手动触发限制，用于巡检策略排查与合规审计。

#### 调试所需的输入参数

- InstanceId（string）：实例 ID。
- PageNumber（integer）：页码，最小值为 1。
- PageSize（integer）：每页返回的巡检规则数量，取值范围 1~100。
- Filters（map，可选）：筛选条件，例如按规则类型、状态过滤。

#### 输出

- InstanceId：实例 ID。
- Configs：巡检规则配置列表，每条记录包含规则名称、类型、开关状态等信息。
- Total：巡检规则总数。
- TriggerLimit：手动触发巡检的时间间隔（秒），例如 900 表示 15 分钟。

#### 最容易被唤起的 Prompt 示例

- 查询实例 rocketmq-xxxx 当前配置了哪些巡检规则。
- 帮我查看实例 rocketmq-xxxx 的巡检规则配置和手动触发限制。

### Tool 5: 查询实例巡检异常结果（GetInstanceInspectResult）

#### 类型

SaaS（云 API）

#### 详细描述

分页查询指定实例的巡检异常结果，用于了解当前风险项、异常数量及分布情况。

#### 调试所需的输入参数

- InstanceId（string）：实例 ID。
- PageNumber（integer）：页码，最小值为 1。
- PageSize（integer）：每页返回的巡检异常结果数量，取值范围 1~100。
- SortBy（string，可选）：排序字段，目前仅支持 TimeStamp。
- SortOrder（string，可选）：排序方式，ASC（升序）或 DESC（降序）。

#### 输出

- InstanceId：实例 ID。
- Results：巡检异常结果列表，每条记录包含异常类型、级别、发生时间、建议处理方式等信息。
- Total：巡检异常结果总数。
- InspectCnt：本次统计涉及的巡检规则数量。
- UnExpectedCnt：检测到的异常数量。

#### 最容易被唤起的 Prompt 示例

- 查询实例 rocketmq-xxxx 最近的巡检异常结果，按时间倒序展示。
- 帮我看看实例 rocketmq-xxxx 当前的巡检异常概况和总数量。

### Tool 6: 手动处理巡检异常结果（ManualProcessResult）

#### 类型

SaaS（云 API）

#### 详细描述

将指定巡检异常结果标记为已处理（Solved），用于在人工排查或确认无需处理后关闭对应告警。

#### 调试所需的输入参数

- InstanceId（string）：实例 ID。
- ResultId（string）：巡检异常结果的唯一 ID，可通过 GetInstanceInspectResult 获取。

#### 输出

- 空对象或 OK 状态：表示指定巡检异常结果已成功标记为已处理。

#### 最容易被唤起的 Prompt 示例

- 将实例 rocketmq-xxxx 中 ResultId 为 45e215e9fe10... 的巡检异常标记为已处理。
- 我已经手动处理了某个巡检异常，帮我把对应的巡检结果设为已解决。

### Tool 7: 手动触发巡检（ManualTriggerInspect）

#### 类型

SaaS（云 API）

#### 详细描述

手动触发指定实例的单条巡检规则，用于在变更前后验证 Queue 资源、队列均衡或订阅一致性等情况。

#### 调试所需的输入参数

- InstanceId（string）：实例 ID。
- Type（string）：巡检规则类型，取值为 cluster、topic 或 group。
- InspectName（string）：巡检任务名称，取值为 queueInsufficient、queueBalance 或 subscribeConsistency（5.x 实例不支持 subscribeConsistency）。

#### 输出

- 空对象或 OK 状态：表示巡检任务已成功触发，可稍后通过 GetInstanceInspectResult 查询结果。

#### 最容易被唤起的 Prompt 示例

- 立刻对实例 rocketmq-xxxx 执行 Queue 资源不足巡检（cluster/queueInsufficient）。
- 对实例 rocketmq-xxxx 的 Topic 队列均衡情况执行一次手动巡检（topic/queueBalance）。

## 可适配平台

可以使用cline、cursor、claude desktop或支持MCP server调用的其它终端

## 服务开通链接

[开通 RocketMQ 服务](https://console.volcengine.com/rocketmq), 未开通的用户会自动重定向到开通页. 如果已经开通,则会跳转首页

## 鉴权方式

API Key ([签名机制]())

## 安装部署

### 系统依赖

- 安装 Python 3.10 或者更高版本
- 安装 uv

```
uv sync
source .venv/bin/activate
mv .env_example .env
```

请在.env文件中设置相关环境变量

如果是本地部署,可以设置 `VOLCENGINE_ACCESS_KEY`, `VOLCENGINE_SECRET_KEY` 等,用于当作工具的默认参数

如果是Server化部署,需设置DEPLOY_MODE=remote,且仅设置REGION

## 安装 MCP-Server
克隆仓库:
```bash
git clone git@github.com:volcengine/mcp-server.git
```

## 运行 MCP-Server 指南
### 1. 配置文件
`server/mcp_server_rocketmq/src/mcp_server_rocketmq/config/config.yaml`

### 2. 协议切换
对应配置中 `transport` 参数：
- `sse`: 使用 Server-Sent Events 协议
- - `server_port`: 用来设置 SSE 端口
- `StreamableHTTP`: 使用 StreamableHTTP 协议
- - `server_port`: 用来设置 StreamableHTTP 端口
- `stdio`: 使用标准输入输出流协议

### 3. 身份认证
若期望对MCP-Client的身份进行认证，可配置 `auth` 参数 (仅适用于SSE协议)：
- `oauth`, 使用 OAuth 认证（需要自备OAuth服务）
- `none`, 不进行身份认证

### 4. 火山访问凭证
因为MCP-Server需要调用火山OpenAPI，因此要提供火山访问凭证信息
对应配置中 `credential` 参数：
- `env`: 从环境变量获取 AK、SK 进行鉴权，取值内容参考：环境变量设置
- `token` 从Header中获取凭证，需要按照下面的流程准备
1. **准备JSON**
   - 构建一个JSON结构，其格式为`{"AccessKeyId":"","SecretAccessKey":"","SessionToken":""}`。
   - 请将`AccessKeyId`和`SecretAccessKey`替换为具体的内容，`SessionToken`可以为空。
   - 示例：`{"AccessKeyId":"AK","SecretAccessKey":"SK","SessionToken":""}`
2. **Base64编码上述JSON**
   - 使用Base64编码工具对准备好的JSON进行编码。
   - 示例：假设原始JSON为`{"AccessKeyId":"AK","SecretAccessKey":"SK","SessionToken":""}`，编码后可能为`ICB7IkFjY2Vzc0tleUlkIjoiQUsiLCJTZWNyZXRBY2Nlc3NLZXkiOiJTSyIsIlNlc3Npb25Ub2tlbiI6IiJ9`（实际编码结果可能因工具和编码规范略有差异）
3. **设置Header**
   - **Key**：设置为`Authorization`。
   - **Value**：格式为`Bearer +` 上面Base64编码的结果，注意`Bearer`后面有一个空格。
   - 示例：`Authorization = Bearer ICB7IkFjY2Vzc0tleUlkIjoiQUsiLCJTZWNyZXRBY2Nlc3NLZXkiOiJTSyIsIlNlc3Npb25Ub2tlbiI6IiJ9`

### 5. 运行模式
#### SSE/StreamableHTTP 模式
- 支持本地启动
   - 如果 `auth = oauth`: 需自行准备Oauth服务器
   - - 必须设置 `credential = env`: 并自行准备AK、SK并设置到环境变量
   - 如果 `auth = none`，则 credential 可设置为 token 或 env
#### STDIO 模式
- 只能设置 `credential = env` 需准备AK、SK并设置到环境变量

### 6. 环境变量设置
- ak 环境变量名:  VOLCENGINE_ACCESS_KEY
- sk 环境变量名:  VOLCENGINE_SECRET_KEY
- session_token 环境变量名:  VOLCENGINE_ACCESS_SESSION_TOKEN
- credential 环境变量名: VOLCENGINE_CREDENTIAL_TYPE (若设置，则优先级高于配置)
- transport 环境变量名: MCP_SERVER_MODE (若设置，则优先级高于配置)
- auth 环境变量名: MCP_SERVER_AUTH (若设置，则优先级高于配置)
- sse_port 环境变量名: MCP_SERVER_PORT (若设置，则优先级高于配置)

### 7. 运行

#### 变量说明
- /ABSOLUTE/PATH/TO/PARENT/FOLDER
   - mcp-server-rocketmq 的代码库目录，例如 /Users/xxx/mcp-server/server/mcp_server_rocketmq，对应 https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_rocketmq

#### Run Locally
#### 如果已经下载代码库
```json
{
    "mcpServers": {
        "RocketMQ": {
            "command": "uv",
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/PARENT/FOLDER",
                "run",
                "mcp-server-rocketmq"
            ],
            "env": {
                "VOLCENGINE_ACCESS_KEY": "your ak",
                "VOLCENGINE_SECRET_KEY": "your sk",
                "VOLCENGINE_ACCESS_SESSION_TOKEN": "your session token"
          }
        }
    }
}
```
#### 如果没有下载代码库
```json
{
    "mcpServers": {
        "RocketMQ": {
            "command": "uvx",
            "args": [
                "--from",
                "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_rocketmq",
                "mcp-server-rocketmq"
            ],
            "env": {
                "VOLCENGINE_ACCESS_KEY": "your ak",
                "VOLCENGINE_SECRET_KEY": "your sk",
                "VOLCENGINE_ACCESS_SESSION_TOKEN": "your session token"
            }
        }
    }
}
```
#### Run Remote
下载代码仓库，并设置transport = StreamableHTTP
```shell
uv --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER run mcp-server-rocketmq
```

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).


