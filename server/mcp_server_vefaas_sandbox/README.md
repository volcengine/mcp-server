# veFaaS Code-Sandbox MCP Server

veFaaS Code-Sandbox 的 mcp 实现，支持 python、go、java、bash等多种运行时，适用于代码调试、AI Agent 开发等场景

| | |
|------|------|
| 版本 | v1 |
| 描述 | 发送代码至沙盒服务运行，支持多种语言运行时 |
| 分类 | 容器与中间件 |
| 标签 | FaaS、函数服务、代码沙箱、Code Sandbox |

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
- 输出：
  - 代码的执行输出结果

#### 最容易被唤起的 Prompt示例

1. 运行 python 代码：print("Hello, World!")
2. code str: puts "Hello, World!", language: ruby

## 可适配平台

方舟、cursor、python

## 服务开通链接 (整体产品)

服务类产品，无需开通

## 鉴权方式

OAuth

## 安装部署

[示例如下]

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *mcp-server-git*.

## 在不同平台的配置

### 方舟

#### 体验中心

[示例如下]

1. 查看MCP Server 详情
   在大模型生态广场，选择合适的MCP Server，并查看详情
2. 选择MCP Server即将运行的平台
   检查当前MCP Server 已适配的平台，并选择合适的平台
3. 查看并对比可用的Tools
   仔细查看可用的Tools的功能描述与所需的输入参数，并尝试运行对应的功能。
4. 获取专属的URL或代码示例
   检查账号登录状态与服务开通情况，生成唯一URL
5. 去对应的Client的平台进行使用
   点击快捷跳转按钮，前往方舟平台的体验中心进行对应MCP Server的体验

## 部署

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
        "SANDBOX_API": "your-sandbox-apig-address"
      }
    }
  }
}
```

## License

volcengine/mcp-server is licensed under the MIT License.
