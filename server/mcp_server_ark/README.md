# 零代码Bot MCP Server

火山方舟[零代码应用](https://www.volcengine.com/docs/82379/1262003)，支持通过表单化创建及开箱即用的基础插件，快速实现零代码应用的搭建与体验，您可在零代码中配置联网搜索、网页解析、计算器等插件。该MCP Server能够通过 BotAPI 调用已创建的零代码应用。

# 功能

1. 通过 [BotAPI](https://www.volcengine.com/docs/82379/1526787) 与火山方舟创建的零代码应用 进行自然语言对话
	
2. 使用 网页解析插件（link\_reader）从 URL（例如，网页、PDF、抖音视频）中提取内容
	
3. 使用 计算器插件（caculator）计算数学表达式
	
4. 使用 联网内容插件（web\_search） 实现联网搜索功能
	

# Tools

本 MCP Server提供以下 Tools (工具/能力):

## Tool 1: bot_chat

该工具允许你与特定Bot ID的零代码应用进行对话。使用前请在火山方舟创建零代码应用，并记录应用 ID 以便进行配置。零代码应用操作指南详见[产品文档](https://www.volcengine.com/docs/82379/1267885)

- 调试所需的输入参数:
	- `message` (string): The message to send to the bot
		
- Tool触发prompt示例：
	

```JSON
{
  "message": "Hello, how can you help me today?"
}
```

<br>

## Tool 2: web_search

使用联网插件进行搜索。当使用启用了配置有联网插件的零代码Bot时，可以通过 bot\_chat 工具使用此功能。操作步骤如下，零代码应用创建步骤详细可见[零代码操作指南](https://www.volcengine.com/docs/82379/1267885)

- 开通[联网内容插件](https://www.volcengine.com/docs/82379/1338552)
	
- 在火山方舟创建零代码应用，并开启联网插件，记录应用 ID 以便进行配置
	
- 在 MCP 设置中配置工具名称和描述
	

```Shell
export ARK_BOT_ID=your bod id
export ARK_BOT_DESCRIPTION=这是联网搜索工具，如果需要搜索互联网上的内容，请使用此工具。输入为查询语句
export ARK_BOT_NAME=web_search
```

- Tool触发prompt示例：
	

```JSON
{
  "message": "关于AI行业的最新新闻是什么？"
}
```

<br>

## Tool 3: link_reader

[网页解析](https://www.volcengine.com/docs/82379/1284852)，可获取和解析 url 链接下的标题和内容。支持用户快速提取和检索网页、pdf等内容中有价值的信息。使用前需开通并在零代码中配置

- 调试所需的输入参数：
	- `url_list` (array of strings): 需要提取内容的 URL 列表（最多 3 个）
		
- Tool触发prompt示例：
	

```JSON
{
  "url_list": ["https://example.com", "https://example.org/document.pdf"]
}
```

<br>

## Tool 4: caculator

使用计算器工具计算数学表达式。

- 调试所需的输入参数:
	- `input` (string): 采用 Wolfram 语言 InputForm 格式的数学表达式
		
- Tool触发prompt示例：
	

```JSON
{
  "input": "2 + 2 * 3"
}
```

<br>

# 可适配平台

- 您可以使用 火山方舟，Trae，Cline，Cursor 或 其他支持 MCP 服务调用的Client平台。
	

<br>

# 服务开通链接

- 火山方舟[零代码应用](https://console.volcengine.com/ark/region:ark+cn-beijing/application)创建操作指南，详见[产品文档](https://www.volcengine.com/docs/82379/1267885)
	
- 根据业务需求开通插件，如联网内容插件、网页解析插件、计算器插件等，详情可见[服务组件库](https://console.volcengine.com/ark/region:ark+cn-beijing/components?action=%7B%7D)
	

<br>

# 鉴权方式

在火山方舟管理控制台获取API KEY，详见 [API KEY管理](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey?apikey=%7B%7D)
<br>

# 安装部署

**环境变量**设置与获取：

- `ARK_API_KEY`：必填，用于火山方舟服务身份验证的 API 密钥
	
- `ARK_BOT_ID`：用于对话的零代码应用的 ID
	
- `ARK_BOT_NAME`：如果设置了 ARK\_BOT\_ID，则为必填项，即 零代码应用 的名称
	
- `ARK_BOT_DESCRIPTION`：如果设置了 ARK\_BOT\_ID，则为必填项，即 零代码应用 的描述
	
- `ARK_TOOL_LINK_READER`：可选，设置为“true”或“1”以启用网页解析工具
	
- `ARK_TOOL_CACULATOR`：可选，设置为“true”或“1”以启用计算器工具
	

您可以在 shell 中设置这些环境变量或使用`.env`文件。
<br>

**MCP** **设置：** 

- stdio方式
	

```JSON
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
                "ARK_BOT_DESCRIPTION": "your-bot-description"
            }
        }
    }
}
```

<br>

# 操作示例

下面以Trae平台为例，展示接入该MCP服务的步骤，以实现与联网零代码应用进行对话：

1. **创建零代码应用：** 进入火山方舟-应用实验室，点击【创建应用】，并选择零代码
	

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_sth/ljhwZthlaukjlkulzlp/ark/assistant/images/mcp-readme-0.png)

2. **配置应用**：填写名称、描述，并开启联网内容插件。如您未开通[联网内容插件](https://www.volcengine.com/docs/82379/1338552)，请进行开通。
	

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_sth/ljhwZthlaukjlkulzlp/ark/assistant/images/mcp-readme-1.png)

3. **发布应用**：点击右上角【发布】按钮，并进行对话测试。记录应用ID便于后续的配置
	

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_sth/ljhwZthlaukjlkulzlp/ark/assistant/images/mcp-readme-2.png)

4. **进入Trae进行安装**：进入Trae的MCP设置页面，将“安装部署”中的MCP配置信息进行复制粘贴，并填写其中的[API\_KEY](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey?apikey=%7B%7D)、BOT\_ID、BOT\_NAME等环境变量参数。点击【确认】，完成后检查状态。
	

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_sth/ljhwZthlaukjlkulzlp/ark/assistant/images/mcp-readme-3.png)

5. **使用测试**：在Trae的Builder with MCP模式下进行对话测试
	

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_sth/ljhwZthlaukjlkulzlp/ark/assistant/images/mcp-readme-4.png)
<br>

# License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).