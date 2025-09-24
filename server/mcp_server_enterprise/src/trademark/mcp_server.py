from src.trademark.api.api import TrademarkAPI
from mcp.server.fastmcp import FastMCP
from .note import note
import json


def create_mcp_server():
    service = TrademarkAPI()
    mcp = FastMCP(
        "mcp-server-enterprise",
        instructions="Volcengine(火山引擎) 企业服务-商标服务 MCP , 你的商标注册、管理助手",
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
    def get_applicant(params: dict) -> str:
        """
        获取商标申请人详情
        Call steps:
        1. Pass "get_applicant" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_applicant
        """
        reqs = service.mcp_get("McpGetApplicant", params, json.dumps({}))

        return reqs

    @mcp.tool()
    def get_trademark(params: dict) -> str:
        """
        获取当前账户所属的商标详情
        Call steps:
        1. Pass "get_trademark" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_trademark
        """
        reqs = service.mcp_get("McpGetTrademark", params, json.dumps({}))

        return reqs

    @mcp.tool()
    def list_applicants(params: dict) -> str:
        """
        获取商标申请人列表
        Call steps:
        1. Pass "list_applicants" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_applicants
        """
        reqs = service.mcp_get("McpListApplicants", params, json.dumps({}))

        return reqs

    @mcp.tool()
    def get_requirement(params: dict) -> str:
        """
        获取商标需求详情
        Call steps:
        1. Pass "get_requirement" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_requirement
        """
        reqs = service.mcp_get("McpGetRequirement", params, json.dumps({}))

        return reqs

    @mcp.tool()
    def list_requirements(params: dict) -> str:
        """
        获取商标需求列表
        Call steps:
        1. Pass "list_requirements" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_requirements
        """
        reqs = service.mcp_get("McpListRequirements", params, json.dumps({}))

        return reqs

    @mcp.tool()
    def list_trademarks(params: dict) -> str:
        """
        获取当前账户提交的商标列表
        Call steps:
        1. Pass "list_trademarks" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_trademarks
        """
        reqs = service.mcp_get("McpListTrademarks", params, json.dumps({}))

        return reqs

    @mcp.tool()
    def search_trademark_info(params: dict, body: dict) -> str:
        """
        根据商标注册号查询他人商标的详情
        Call steps:
        1. Pass "search_trademark_info" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  search_trademark_info
        """
        reqs = service.mcp_post("McpSearchTrademarkInfo", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def search_trademark(params: dict, body: dict) -> str:
        """
        查询注册局中记录的商标信息，常用语注册前评估意向商标的状态。支持商标名称，注册号和申请人独立搜索，且必填其一
        Call steps:
        1. Pass "search_trademark" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  search_trademark
        """
        reqs = service.mcp_post("McpSearchTrademark", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def list_barrier_trademarks(params: dict) -> str:
        """
        获取障碍商标列表
        Call steps:
        1. Pass "list_barrier_trademarks" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_barrier_trademarks
        """
        reqs = service.mcp_get("McpListBarrierTrademarks", params, json.dumps({}))

        return reqs

    return mcp
