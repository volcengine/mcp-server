# sts MCP Server

| 版本 |         v1.0.0          |
|:--: |:-----------------------:|
| 描述 | 安全凭证服务，通过角色扮演获取临时访问凭证       |
| 分类 | 工具类 |
| 标签 | 角色扮演、凭证、管理与治理           |

## Tools
本 MCP Server 产品提供以下 Tools:


- AssumeRole: 以角色身份发起一次临时会话，临时会话中包含一组短效安全凭证用于请求云服务API。关于角色的使用方法可以参考 [角色说明文档](https://www.volcengine.com/docs/6257/64979)。
## 可适配平台
方舟，Python，Cursor，Trae

## 服务开通链接
https://console.volcengine.com/iam/identitymanage/role

## 鉴权方式
仅支持本地 STDIO 模式运行

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
`server/mcp_server_sts/src/mcp_server_sts/config/cfg.yaml`

### 2. 火山访问凭证
因为MCP-Server需要调用火山OpenAPI，因此要提供火山访问凭证信息
对应配置中 `credential` 参数：
- `env`: 从环境变量获取 AK、SK 进行鉴权，取值内容参考：环境变量设置

### 3. 运行模式
#### STDIO 模式
- 设置`transport` = `stdio`、`credential = env` 需要准备AK、SK并设置到环境变量

### 4. 环境变量设置
- ak 环境变量名:  VOLCENGINE_ACCESS_KEY
- sk 环境变量名:  VOLCENGINE_SECRET_KEY
- session_token 环境变量名:  VOLCENGINE_ACCESS_SESSION_TOKEN
- credential 环境变量名: VOLCENGINE_CREDENTIAL_TYPE (若设置，则优先级高于配置)
- transport 环境变量名: MCP_SERVER_MODE (若设置，则优先级高于配置)
- auth 环境变量名: MCP_SERVER_AUTH (若设置，则优先级高于配置)
- sse_port 环境变量名: MCP_SERVER_PORT (若设置，则优先级高于配置)

### 5. 运行

#### 变量说明
- /ABSOLUTE/PATH/TO/PARENT/FOLDER
   - mcp-server-sts 的代码库目录，例如 /Users/xxx/mcp-server/server/mcp_server_sts，对应 https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_sts

#### Run Locally
#### 如果已经下载代码库
```json
{
    "mcpServers": {
        "sts": {
            "command": "uv",
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/PARENT/FOLDER",
                "run",
                "mcp-server-sts"
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
        "sts": {
            "command": "uvx",
            "args": [
                "--from",
                "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_sts",
                "mcp-server-sts"
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

## License
[MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE)
