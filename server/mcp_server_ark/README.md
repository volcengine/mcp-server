# 零代码 Bot MCP

## 功能

1. 通过 bot_chat API 与 ARK 机器人进行对话
2. 使用 link_reader 工具从 URL（网页、PDF、抖音视频）中提取内容
3. 借助 caculator 工具计算数学表达式
4. 通过 ARK 网页插件实现网络搜索功能

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: bot_chat

#### 类型

bot_chat

#### 详细描述

使用配置的 Bot ID 聊天。

#### 调试所需的输入参数，

输入：

- `message`（字符串）：发送给bot的消息

```json
{
  "message": "Hello, how can you help me today?"
}
```


### Tool 2: web_search

#### 详细描述

使用联网插件进行搜索。当使用启用了联网插件的 Bot 时，可以通过 Bot 聊天工具使用此功能。使用网络搜索：
1. 创建并配置应用
2. 开启联网插件插件
3. 在 MCP 设置中配置工具名称和描述

```shell
export ARK_BOT_ID=your bod id
export ARK_BOT_DESCRIPTION=这是联网搜索工具，如果需要搜索互联网上的内容，请使用此工具。输入为查询语句
export ARK_BOT_NAME=web_search
```

#### 调试所需的输入参数，
输入：
```json
{
  "message": "关于人工智能的最新消息是什么？"
}
```




### Tool 3: caculator

#### 详细描述

使用 ARK 计算器工具计算数学表达式。

#### 调试所需的输入参数，

输入：
- `input` (string): 采用 Wolfram 语言 InputForm 格式的数学表达式

```json

{
  "input": "2 + 2 * 3"
}
```



### Tool 4: link_reader

#### 详细描述

从 URL 中提取内容，支持网页、PDF 和抖音视频。


#### 调试所需的输入参数，

输入：
- `url_list` (array of strings): 需要提取内容的 URL 列表（最多 3 个）

```json
{
  "url_list": ["https://example.com", "https://example.org/document.pdf"]
}
```


## 可适配平台  

sse: 方舟，Python, Cline
stdio: Python, Cline

## 服务开通链接 (整体产品)  

<https://console.volcengine.com/ark>

## 鉴权方式  

OAuth 2.0

## 在不同平台的配置

### UVX

请预先获取环境变量 ARK_API_KEY 和 ARK_BOT_ID

stdio方式


```json
{
    "mcpServers": {
        "ark": {
            "command": "uvx",
            "args": [
            "--from",
            "git+https://github.com/volcengine/ai-app-lab#subdirectory=mcp/server/mcp_server_ark",
            "mcp-server-ark",
          ],
            "env": {
                "ARK_API_KEY": "your-ark-api-key",
                "ARK_BOT_ID": "your-bot-id",
                "ARK_BOT_NAME": "your-bot-name",
                "ARK_BOT_DESCRIPTION": "your-bot-description",
                "ARK_TOOL_LINK_READER": "true",
                "ARK_TOOL_CACULATOR": "true"
            }
        }
    }
}
```

## License

volcengine/mcp-server is licensed under the MIT License.