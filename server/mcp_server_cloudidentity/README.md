# cloudidentity MCP Server

| 版本 |         v1.0.0          |
|:--: |:-----------------------:|
| 描述 | 云身份中心（Cloud Identity）是链接外部身份和火山引擎云上身份的统一管理平台。使用云身份中心，您可以统一管理您的企业员工登录火山引擎的方式、一键同步员工身份至火山引擎，并可以基于企业组织的多账号管理，一次性配置企业身份管理系统到火山引擎多账号下的单点登录、及时对企业员工“入离转调”产生的访问权限变动进行管理和同步。       |
| 分类 | 工具类 |
| 标签 | 管理、云身份、用户、角色、管理与治理           |

## Tools
本 MCP Server 产品提供以下 Tools:

- CreateAccountAssignment: 创建角色访问授权

- CreateGroup: 创建用户组

- CreateUser: 创建用户

- CreateUserProvisioning: 创建用户访问授权任务

- GetExternalSAMLIdentityProvider: 获取云身份中心中已经配置的外部SAML身份提供商信息。

- GetGroup: 查询用户组详情

- GetPermissionSet: 获取权限集信息

- GetPortalLoginConfig: 获取登录配置

- GetSAMLServiceProvider: 获取云身份中心SAML服务提供商相关信息

- GetServiceStatus: 获取云身份中心服务启用状态

- GetTaskStatus: 获取任务状态

- GetUser: 查询用户信息

- GetUserProvisioning: 查看用户访问授权任务

- ListAccountAssignments: 获取角色访问授权列表

- ListGroupMembers: 查询用户组成员

- ListGroups: 查询用户组列表

- ListPermissionPoliciesInPermissionSet: 获取权限集策略列表

- ListPermissionSetProvisionings: 获取权限集部署列表

- ListPermissionSets: 获取权限集列表

- ListPortalLoginSettings: 查询门户登录配置列表

- ListTasks: 获取任务列表

- ListUserProvisioningEvents: 授权记录列表

- ListUserProvisionings: 查看用户访问授权任务列表

- ListUsers: 查询用户列表
## 可适配平台
方舟，Python，Cursor，Trae

## 服务开通链接
https://console.volcengine.com/cloudidentity

## 鉴权方式
支持Oauth鉴权，需要提供三方OAuth服务器，如GitHub Oauth应用

## 系统依赖
- 安装 Python 3.11 或者更高版本
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
`server/mcp_server_cloudidentity/src/mcp_server_cloudidentity/config/cfg.yaml`

### 2. 协议切换
对应配置中 `transport` 参数：
- `sse`: 使用 Server-Sent Events 协议
- - `sse_port`: 用来设置 SSE 端口
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
#### SSE 模式
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
   - mcp-server-cloudidentity 的代码库目录，例如 /Users/xxx/mcp-server/server/mcp_server_cloudidentity，对应 https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_cloudidentity

#### Run Locally
#### 如果已经下载代码库
```json
{
    "mcpServers": {
        "cloudidentity": {
            "command": "uv",
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/PARENT/FOLDER",
                "run",
                "mcp-server-cloudidentity"
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
        "cloudidentity": {
            "command": "uvx",
            "args": [
                "--from",
                "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_cloudidentity",
                "mcp-server-cloudidentity"
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
下载代码仓库，并设置transport = sse
```shell
uv --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER run mcp-server-cloudidentity
```

## License
[MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE)
