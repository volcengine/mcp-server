# iam MCP Server

| 版本 |         v1.0.0          |
|:--: |:-----------------------:|
| 描述 | 访问控制(Identity and Access Management，缩写为IAM)是火山引擎为客户提供的一套权限管理系统，用于控制不同身份对云资源的访问权限。例如在企业里，企业使用主账号购置云资源，并将云资源的访问权限按需分配给不同IAM身份。企业可以允许员工使用IAM身份登录控制台访问云资源，或者将IAM用户或角色扮演产生的凭证用于企业的工作负载，以编程访问的方式请求云服务。       |
| 分类 | 工具类 |
| 标签 | 用户、用户组、身份提供商、策略、项目管理、角色、访问秘钥、标签、管理与治理           |

## Tools
本 MCP Server 产品提供以下 Tools:


- CreateGroup: 创建用户组。

- CreatePolicy: 创建自定义策略。

- CreateRole: 创建角色。

- CreateServiceLinkedRole: 创建服务关联角色。部分云服务可能会在您首次使用产品时要求授权云服务进行跨服务访问，该接口可用于新建服务关联角色以完成指定服务的跨服务访问授权。

- GetAccessKeyLastUsed: 查询指定API访问密钥的最后使用信息（包含最后使用时间、访问的服务、访问的地域）。

- GetGroup: 查询指定用户组的详情信息。

- GetLoginProfile: 查询指定IAM用户的登录配置。

- GetOAuthProvider: 查询 OAuth 身份提供商

- GetOIDCProvider: 查询 OIDC 身份提供商信息

- GetPolicy: 查询指定策略的详情信息。

- GetRole: 查询指定角色的详情信息。

- GetSAMLProvider: 查询 SAML 身份提供商

- GetSecurityConfig: 查询指定IAM用户的操作保护配置

- GetUser: 查询指定IAM用户的详情信息。

- ListAccessKeys: 获取主账号或IAM用户的密钥列表。因安全原因，该接口不返回Secret Access Key，请在首次创建密钥时保存好Secret Access Key。

- ListAttachedRolePolicies: 获取指定角色绑定的策略列表。

- ListAttachedUserGroupPolicies: 获取用户组绑定的策略列表。

- ListAttachedUserPolicies: 获取指定用户绑定的策略列表。

- ListEntitiesForPolicy: 获取指定策略所绑定的身份列表（包含用户、用户组或角色）。

- ListGroups: 获取用户组列表。

- ListGroupsForUser: 获取指定用户加入的用户组列表。

- ListIdentityProviders: 查询身份提供商列表

- ListOIDCProviders: 查询 OIDC 身份提供商列表

- ListPolicies: 获取全部策略列表（包含系统预设策略和自定义策略）。

- ListRoles: 获取角色列表。

- ListSAMLProviderCertificates: 查询身份提供商证书列表

- ListSAMLProviders: 查询 SAML 身份提供商列表

- ListTagsForResources: 查询指定用户或角色的标签列表。

- ListUsers: 获取IAM用户列表。

- ListUsersForGroup: 获取指定用户组内的用户列表。

- TagResources: 为用户或角色附加指定标签。
## 可适配平台
方舟，Python，Cursor，Trae

## 服务开通链接
https://console.volcengine.com/iam/identitymanage

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
`server/mcp_server_iam/src/mcp_server_iam/config/cfg.yaml`

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
   - mcp-server-iam 的代码库目录，例如 /Users/xxx/mcp-server/server/mcp_server_iam，对应 https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_iam

#### Run Locally
#### 如果已经下载代码库
```json
{
    "mcpServers": {
        "iam": {
            "command": "uv",
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/PARENT/FOLDER",
                "run",
                "mcp-server-iam"
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
        "iam": {
            "command": "uvx",
            "args": [
                "--from",
                "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_iam",
                "mcp-server-iam"
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
uv --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER run mcp-server-iam
```

## License
[MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE)
