# Conversational AI MCP

The same calling service as Doubao, integrating large language models (LLM), visual understanding models (VLM), automatic speech recognition (ASR), text-to-speech (TTS), and audio/video processing/transmission capabilities. Quickly implement smooth, natural, and human-like real-time conversation functions between users and large models, making human-AI interaction no longer limited to text. It can be applied to AI intelligent assistants, AI customer service, AI companionship, AI oral language teaching, AI game coaching, smart hardware, smart toys, smart homes, smart educational hardware, embodied intelligence, and other application scenarios.

## Tools

This MCP Server product provides the following Tools (tools/capabilities):

### Tool1: start_voice_chat

- Detailed Description:
  Call the StartVoiceChat interface to launch an AI agent with listening and speaking capabilities in your application, enabling it to have natural, smooth, and human-like real-time conversations with real users.
  This interface integrates automatic speech recognition (ASR), large language model (LLM), and text-to-speech (TTS) capabilities in one stop, and ensures an ultimate conversation experience through Volcano Engine's low-latency real-time communication technology. You can access Volcano Engine's complete AI service suite out of the box, and also support flexible integration of self-developed or third-party ASR, LLM, and TTS services.
- Trigger Example: Start a conversational AI agent

### Tool2: update_voice_chat

- Detailed Description: After successfully starting an agent task through StartVoiceChat, you can call this interface at any moment during the conversation to send commands to the task, achieving rich real-time interactive effects. Using this interface can implement functions including but not limited to: interrupt the agent's current voice broadcast; return Function Calling tool invocation results to LLM; end the current user's voice input and trigger a new round of conversation; let the agent actively broadcast a specified text; dynamically input context to LLM; input images to LLM with visual capabilities, etc.
- Trigger Example: Interrupt this agent

### Tool3: stop_voice_chat

- Detailed Description:
  If you need to end the agent's voice chat service, you can achieve this by calling this interface.
- Trigger Example: Stop/close this agent

## Compatible Platforms

You can use Ark, Trae, Cline, Cursor, or other platforms that support MCP service calls

## Service Activation Link (Overall Product)

You can visit [Quick Start](https://console.volcengine.com/rtc/aigc/run?from=mcp) to experience a no-code real-time conversational AI Demo, learn how to activate necessary services and quickly integrate client and server to experience AI real-time interaction capabilities.

## Authentication Method

You can obtain VOLCENGINE_ACCESS_KEY and VOLCENGINE_SECRET_KEY for authentication at [Volcano API Access Keys](https://console.volcengine.com/iam/keymanage)

## Installation and Deployment

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

## Configuration on Different Platforms

### Ark

#### Experience Center

1. View MCP Server Details
   In the large model ecosystem marketplace, select an appropriate MCP Server and view its details
2. Select the Platform Where MCP Server Will Run
   Check the platforms that the current MCP Server has adapted to and select an appropriate platform
3. View and Compare Available Tools
   Carefully review the functional descriptions and required input parameters of available Tools, and try running the corresponding functions.
4. Get Exclusive URL or Code Examples
   Check account login status and service activation status, generate unique URL
5. Go to the Corresponding Client Platform for Use
   Click the quick jump button to go to the Ark platform's experience center to experience the corresponding MCP Server

## Deployment

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

#### Local Configuration

- Add the following configuration to your mcp settings file

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
