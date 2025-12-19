from src.rtc.api.api import RtcAPI
from mcp.server.fastmcp import FastMCP
from .note import note
import json
import os


def create_mcp_server():
    service = RtcAPI()
    mcp = FastMCP(
        name="mcp_server_rtc",
        instructions="""
      ## MCP Invocation Method Guide
      - For task decomposition, it is necessary to use the mcp tool.
      - The first step requires invoking the `get_note` function to obtain the parameter description.
      - Subsequently, the corresponding method should be called to retrieve the data.
        豆包同款通话服务，整合 LLM、VLM、ASR、TTS、以及音视频处理/传输能力，快速实现用户与大模型间流畅、自然、真人感的实时对话功能
      """,
        host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
        port=int(os.getenv("MCP_SERVER_PORT", "8000")),
        streamable_http_path=os.getenv("STREAMABLE_HTTP_PATH", "/mcp")
    )

    @mcp.tool()
    def guide():
        """
        ## MCP Invocation Method Guide
        - For task decomposition, it is necessary to use the mcp tool.
        - The first step requires invoking the `get_note` function to obtain the parameter description.
        - Subsequently, the corresponding method should be called to retrieve the data.
        """
        return """use  `guide` description to get how to use Mcp Server"""

    @mcp.tool()
    def get_note(func_name: str) -> str:
        """
        获取参数描述

        Args:
            func_name: 函数名

        """
        return note.get(func_name)

    @mcp.tool()
    def start_voice_chat(params: dict, body: dict) -> str:
        """
        调用 StartVoiceChat 接口，在你的应用中启动一个具备听说能力的 AI 智能体，使其与真人用户进行自然、流畅、真人感的实时对话。
        该接口一站式整合了语音识别（ASR）、大语言模型（LLM）和语音合成（TTS）能力，并通过火山引擎的低延迟实时通信技术，确保了极致的对话体验。你可以开箱即用地接入火山引擎的全套 AI 服务，也支持灵活地集成自研或第三方的 ASR、LLM 及 TTS 服务。
        Call steps:
        1. Pass "start_voice_chat" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  start_voice_chat
        """
        reqs = service.mcp_post("RtcMcpStartVoiceChat", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def update_voice_chat(params: dict, body: dict) -> str:
        """
        通过 StartVoiceChat 成功启动一个智能体任务后，你可以在对话进行中的任何时刻，调用本接口向该任务发送指令，以实现丰富的实时交互效果。使用此接口可实现包括但不限于以下功能： 打断智能体当前的语音播报；向 LLM 回传 Function Calling 的工具调用结果；结束当前用户的语音输入，触发新一轮对话；让智能体主动播报一段指定的文本；向 LLM 动态传入上下文；向具备视觉能力的 LLM 传入图片等。
        Call steps:
        1. Pass "update_voice_chat" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  update_voice_chat
        """
        reqs = service.mcp_post("RtcMcpUpdateVoiceChat", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def stop_voice_chat(params: dict, body: dict) -> str:
        """
        若你需要结束智能体的语音聊天服务，可以通过调用此接口实现。
        Call steps:
        1. Pass "stop_voice_chat" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  stop_voice_chat
        """
        reqs = service.mcp_post("RtcMcpStopVoiceChat", params, json.dumps(body))

        return reqs

    return mcp
