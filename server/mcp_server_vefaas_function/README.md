# veFaaS MCP Server

veFaaS MCP Server 提供创建、更新、发布函数和添加触发器的能力。

| | |
|------|------|
| 描述 | veFaaS MCP Server 助你轻松管理函数和触发器生命周期|
| 分类 | 容器与中间件 |
| 标签 | FaaS，函数服务，函数，生命周期 |

## 能力概览

- 创建/更新/发布 veFaaS 函数，并管理依赖安装与触发器配置。
- 支持上传本地代码或通过已有制品（TOS、镜像）更新函数。
- 覆盖 API 网关触发器和函数列表/存在性查询等补充能力。

最新的参数、调用约束和注意事项都写在 `src/mcp_server_vefaas_function/vefaas_server.py` 的工具描述中，优先以代码为准。

## 推荐流程

1. `create_function` 创建函数（或确认已有函数 ID）。
2. `upload_code` 推送代码，必要时排除 `.venv`、`node_modules` 等本地依赖。
3. 如果触发了依赖安装任务，使用 `get_dependency_install_task_status` 轮询直至 `Succeeded/Failed`。
4. 重新发布：`release_function`，随后持续调用 `get_function_release_status` 直到成功或失败。
5. 发布成功后，再创建 API 网关触发器或其它下游资源。

## 支持的运行时

- `native-python3.12/v1`
- `native-node20/v1`
- `native/v1`

以上运行时均为原生环境，仅提供解释器/运行时，不包含任何 Web 框架或额外工具。请把依赖声明在 `requirements.txt` / `package.json` 中，由 veFaaS 自动安装。

## 常见注意事项

- 本地修改完成后务必重新执行 `upload_code`；直接调用 `release_function` 只会复用旧制品。
- 依赖安装长时间 `InProgress` 时，遵循工具描述中的退避策略并及时上报。
- API 网关相关操作在创建触发器前应复用现有关联服务，避免重复创建。

## 可适配平台

streamable-http: 方舟，Python
stdio: Python, Cursor, Claude macOS App, Cline

## 服务开通链接 (整体产品)

<https://console.volcengine.com/vefaas>

## 鉴权方式

OAuth 2.0

## 在不同平台的配置

### 方舟

#### 体验中心

1. 查看 MCP Server 详情
在大模型生态广场，选择合适的 veFaaS MCP Server，并查看详情
2. 选择 MCP Server 即将运行的平台
检查当前 MCP Server 已适配的平台，并选择合适的平台
3. 查看并对比可用的 Tools
仔细查看可用的 Tools 的功能描述与所需的输入参数，并尝试运行对应的功能。
4. 获取专属的URL或代码示例
检查账号登录状态与服务开通情况，生成唯一URL
5. 去对应的Client的平台进行使用
点击快捷跳转按钮，前往方舟平台的体验中心进行对应MCP Server的体验

### UVX

请预先获取环境变量 VOLCENGINE_ACCESS_KEY 和 VOLCENGINE_SECRET_KEY。

```json
{
  "mcpServers": {
    "vefaas": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_vefaas_function",
        "mcp-server-vefaas-function"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "xxx",
        "VOLCENGINE_SECRET_KEY": "xxx"
      }
    }
  }
}
```

## License

volcengine/mcp-server is licensed under the MIT License.
