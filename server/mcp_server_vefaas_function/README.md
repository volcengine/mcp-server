# veFaaS MCP Server

veFaaS MCP Server 提供创建、更新、发布 veFaaS 函数以及管理应用的自动化能力，帮助在 MCP 体系内快速对接 veFaaS 服务。

## 安装与快速开始

推荐使用 `uvx` 在本地快速拉起服务，请将 VOLCENGINE_ACCESS_KEY 和 VOLCENGINE_SECRET_KEY 内容替换为您账号的 AK/SK。

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

## 前置条件与注意事项

- 凭证管理：AK/SK 为账号敏感信息，请妥善保管，避免泄露。
- 服务开通：生成公网访问链接依赖 API 网关等前置资源，使用前请确认账号已在控制台开通相关服务。
- 代码包与运行时：编译型语言需先在本地生成 Linux 可执行文件；解释型语言需提供启动脚本和依赖声明文件（`requirements.txt` / `package.json`）以便平台自动安装依赖。
- 模型与 Agent 效果：MCP 的执行效果受所选模型和 Agent 策略影响，若结果不理想，可补充上下文、调整提示词或切换模型/Agent。

## 能力概览

- 函数生命周期：创建、更新、发布、删除 veFaaS 函数，支持本地代码包、TOS 制品或镜像等多种来源。
- 代码与依赖：上传代码、触发依赖安装任务、轮询安装状态，并可下载线上代码。
- 运行时与配置：管理命令、环境变量、VPC 配置等基础属性。
- 应用与访问：查询可用的 API 网关资源，创建并发布 veFaaS 应用，检索模板信息。

## 支持的运行时

- `native-python3.12/v1`
- `native-node20/v1`
- `native/v1`

以上运行时均为原生环境，仅提供解释器/运行时，不包含额外框架或工具。

## 官方资源

- veFaaS 控制台：<https://console.volcengine.com/vefaas>
- veFaaS MCP 操作文档：<https://www.volcengine.com/docs/6662/1852853#VCm9Uhw2>

## License

volcengine/mcp-server is licensed under the MIT License.
