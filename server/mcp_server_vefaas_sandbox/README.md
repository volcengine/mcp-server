# veFaaS Code-Sandbox MCP Server

veFaaS Code-Sandbox 的 mcp 实现，支持 python、go、java、bash等多种运行时，适用于代码调试、AI Agent 开发等场景

| | |
|------|------|
| 版本 | v0.0.2 |
| 描述 | 发送代码至沙盒服务运行，支持多种语言运行时 |
| 分类 | 容器与中间件 |
| 标签 | veFaaS、函数服务、代码沙箱、Code Sandbox |

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: run_code

#### 类型

saas

#### 详细描述

运行特定运行时的代码

#### 调试所需的输入参数

- 环境变量：
  - SANDBOX_API: veFaaS Code-Sandbox 服务 APIG 地址
- 输入：
  - codeStr: 待运行的 code str
  - language: 代码运行时，支持：python、nodejs、go、bash、typescript、java、cpp、php、csharp、lua、R、 swift、scala、ruby
  - compile_timeout: 编译超时时间，单位：秒，默认：60
  - run_timeout: 运行超时时间，单位：秒，默认：60
  - fetch_files: 代码执行后要获取的文件路径列表，默认为空
  - files: 从文件路径到base64编码的文件内容的字典，默认为空
- 输出：
  - 代码的执行输出结果

#### 最容易被唤起的 Prompt示例

1. 运行 python 代码：print("Hello, World!")
2. code str: puts "Hello, World!", language: ruby

## 可适配平台

方舟、cursor、python、5ire macOS App

## 服务开通链接 (整体产品)

<https://console.volcengine.com/vefaas>

## 鉴权方式

OAuth 2.0

## 部署配置

### 获取 veFaaS Code-Sandbox 服务的访问入口

参考火山引擎 veFaaS [一键部署 Code Sandbox Agent 应用](https://www.volcengine.com/docs/6662/1538139)，完成以下配置：
1. 获取 veFaaS Code Sandbox Agent 服务的访问入口，如 `xxxxxxxxxxx.apigateway-cn-beijing.volceapi.com`，获取 `xxxxxxxxxxx.apigateway-cn-beijing.volceapi.com`，用于下方的 `SANDBOX_API` 配置。
2. 获取auth token用于下方的`AUTH_TOKEN`配置。


### uvx

```json
{
  "mcpServers": {
    "mcp-server-vefaas-sandbox": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_vefaas_sandbox",
        "mcp-server-vefaas-sandbox"
      ],
      "env": {
        "SANDBOX_API": "your-sandbox-apig-address",
        "AUTH_TOKEN": "your-sandbox-apig-auth-token"
      }
    }
  }
}
```

## License

volcengine/mcp-server is licensed under the [MIT License](../../LICENSE).
