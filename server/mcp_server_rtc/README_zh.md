# 实时对话式 AI MCP

豆包同款通话服务，整合大模型(LLM)、视觉理解模型（VLM）、语音识别(ASR)、语音合成(TTS)、以及音视频处理/传输能力，快速实现用户与大模型间流畅、自然、真人感的实时对话功能，让人与 AI 的交互不再局限于文字，可应用于 AI 智能助手、AI 客服、AI 陪伴、AI 口语教学、AI 游戏教练、智能硬件、智能玩具、智能家居、智能教育硬件、具身智能等场景应用。

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool1: start_voice_chat

- 详细描述：
  调用 StartVoiceChat 接口，在你的应用中启动一个具备听说能力的 AI 智能体，使其与真人用户进行自然、流畅、真人感的实时对话。
  该接口一站式整合了语音识别（ASR）、大语言模型（LLM）和语音合成（TTS）能力，并通过火山引擎的低延迟实时通信技术，确保了极致的对话体验。你可以开箱即用地接入火山引擎的全套 AI 服务，也支持灵活地集成自研或第三方的 ASR、LLM 及 TTS 服务。
- 触发示例：启动一个对话式 AI 智能体

### Tool2: update_voice_chat

- 详细描述：通过 StartVoiceChat 成功启动一个智能体任务后，你可以在对话进行中的任何时刻，调用本接口向该任务发送指令，以实现丰富的实时交互效果。使用此接口可实现包括但不限于以下功能： 打断智能体当前的语音播报；向 LLM 回传 Function Calling 的工具调用结果；结束当前用户的语音输入，触发新一轮对话；让智能体主动播报一段指定的文本；向 LLM 动态传入上下文；向具备视觉能力的 LLM 传入图片等。
- 触发示例：打断这个智能体

### Tool3: stop_voice_chat

- 详细描述：
  若你需要结束智能体的语音聊天服务，可以通过调用此接口实现。
- 触发示例：停止/关闭这个智能体

## 可适配平台

您可以使用 火山方舟，Trae，Cline，Cursor 或 其他支持 MCP 服务调用

## 服务开通链接 (整体产品)

您可前往[快速跑通](https://console.volcengine.com/rtc/aigc/run?from=mcp)体验无代码接入实时对话式 AI Demo，了解如何开通必要服务并快速集成客户端与服务端体验 AI 实时交互能力。

## 鉴权方式

您可以至[火山 API 访问密钥](https://console.volcengine.com/iam/keymanage)获取 VOLCENGINE_ACCESS_KEY，VOLCENGINE_SECRET_KEY 用于鉴权

## 安装部署

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run _mcp-server-git_.

### Using PIP

Alternatively you can install `mcp-server-git` via pip:

```
pip install mcp-server-git
```

After installation, you can run it as a script using:

```
python -m mcp_server_git
```

## 在不同平台的配置

### 方舟

#### 体验中心

1. 查看 MCP Server 详情
   在大模型生态广场，选择合适的 MCP Server，并查看详情
2. 选择 MCP Server 即将运行的平台
   检查当前 MCP Server 已适配的平台，并选择合适的平台
3. 查看并对比可用的 Tools
   仔细查看可用的 Tools 的功能描述与所需的输入参数，并尝试运行对应的功能。
4. 获取专属的 URL 或代码示例
   检查账号登录状态与服务开通情况，生成唯一 URL
5. 去对应的 Client 的平台进行使用
   点击快捷跳转按钮，前往方舟平台的体验中心进行对应 MCP Server 的体验

## 部署

### Docker

```json
{
  "mcpServers": {
    "git": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--mount",
        "type=bind,src=/Users/username/Desktop,dst=/projects/Desktop",
        "--mount",
        "type=bind,src=/path/to/other/allowed/dir,dst=/projects/other/allowed/dir,ro",
        "--mount",
        "type=bind,src=/path/to/file.txt,dst=/projects/path/to/file.txt",
        "mcp/git"
      ]
    }
  }
}
```

### Using uvx

#### 本地配置

- 添加以下配置到你的 mcp settings 文件中

```json
{
  "mcpServers": {
    "mcp-server-rtc": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_rtc",
        "mcp-server-rtc"
      ],
      "env": {
        "MCP_SERVER_PORT": "<PORT>",
        "MCP_SERVER_HOST": "<HOST>",
        "VOLCENGINE_ACCESS_KEY": "your access-key-id",
        "VOLCENGINE_SECRET_KEY": "your access-key-secret"
      }
    }
  }
}
```

or

```json
{
  "mcpServers": {
    "mcp-server-rtc": {
      "command": "uvx",
      "args": [
        "--from",
        "/ABSOLUTE/PATH/TO/PARENT/mcp-server/server/mcp_server_rtc",
        "mcp-server-rtc"
      ],
      "env": {
        "MCP_SERVER_PORT": "<PORT>",
        "MCP_SERVER_HOST": "<HOST>",
        "VOLCENGINE_ACCESS_KEY": "your access-key-id",
        "VOLCENGINE_SECRET_KEY": "your access-key-secret"
      }
    }
  }
}
```

## License

MIT
