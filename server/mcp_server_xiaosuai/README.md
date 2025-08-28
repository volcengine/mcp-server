# 小宿智能搜索Smart Search MCP Server

一个集成远程智能搜索 API 的 MCP 服务器，实现关键词网页搜索功能。

## 特性

-   **网页搜索**：支持关键词检索、分页、语言和安全等级选项。
-   **结构化返回**：所有搜索结果以 JSON 格式返回。
-   **平台兼容**：为 火山引擎 MCP 平台优化，支持从源码直接部署。

## 工具

### `smart_search`

-   **功能**: 执行网页搜索，支持分页与安全选项。
-   **输入参数**:
    -   `query` (string): 搜索关键词
    -   `count` (number, optional): 返回结果数量 (默认 10)
    -   `offset` (number, optional): 分页偏移 (默认 0)
    -   `setLang` (string, optional): 搜索语言 (默认 'en')
    -   `safeSearch` (string, optional): 安全搜索等级 (默认 'Strict')

## 配置与部署

### 1. 获取 API 密钥

-   注册一个支持智能搜索的 API 服务。
-   获取并复制你的 API 密钥（格式通常为 `endpoint-apikey`）。

## 配置

### 获取 API 密钥
1. 登录到 [www.cloudsway.ai](https://www.cloudsway.ai) 或联系 info@cloudsway.ai 获取你的 Endpoint 和 AccessKey。
2. 将它们按 `{Endpoint}-{AccessKey}` 的格式组合，形成你的 `SERVER_KEY`.

```json
{
  "mcpServers": {
    "smartsearch": {
      "command": "npx",
      "args": [
        "-y",
        "@cloudsway-ai/smartsearch"
      ],
      "env": {
        "SERVER_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
