from src.domain_openapi.api.api import DomainOpenapiAPI
from mcp.server.fastmcp import FastMCP
from .note import note
from src.utils.response import HandlerVolcResponse
import json


def create_mcp_server():
    service = DomainOpenapiAPI()
    mcp = FastMCP(
        "域名服务 MCP",
        instructions="Volcengine(火山引擎) 域名服务 MCP, 提供域名相关的服务",
    )

    @mcp.tool()
    def guide():
        """
        ## MCP Invocation Method Guide
        - For task decomposition, it is necessary to use the mcp tool.
        - The first step requires invoking the `get_note` function to obtain the parameter description.
        - Subsequently, the corresponding method should be called to retrieve the data.
        """
        return """use  `guide` instructions to get how to use Mcp Server"""

    @mcp.tool()
    def get_note(func_name: str) -> str:
        """
        获取参数描述

        Args:
            func_name: 函数名

        """
        return note.get(func_name)

    @mcp.tool()
    def check_fee(params: dict) -> str:
        """
        查询域名价格，能否注册以及是否包含限制词等信息。
        Call steps:
        1. Pass "check_fee" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  check_fee
        """
        reqs = service.mcp_get("McpCheckFee", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def get_domain(params: dict) -> str:
        """
        获取指定域名的详细信息。
        Call steps:
        1. Pass "get_domain" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_domain
        """
        reqs = service.mcp_get("McpGetDomain", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def get_async_task(params: dict) -> str:
        """
        查询火山引擎域名服务中异步任务的执行状态。操作包括域名注册，域名续费等。
        Call steps:
        1. Pass "get_async_task" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_async_task
        """
        reqs = service.mcp_get("McpGetAsyncTask", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def get_template(params: dict) -> str:
        """
        获取一个域名信息模板的详情。
        Call steps:
        1. Pass "get_template" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_template
        """
        reqs = service.mcp_get("McpGetTemplate", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def list_domains(params: dict) -> str:
        """
        查询您在火山引擎域名服务托管的域名的详细信息。
        Call steps:
        1. Pass "list_domains" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_domains
        """
        reqs = service.mcp_get("McpListDomains", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def list_templates(params: dict) -> str:
        """
        获取当前账号下的域名信息模板列表以及列表中每个信息模板的详细信息。您可以指定一个或者多个条件对返回的域名列表进行过滤。
        Call steps:
        1. Pass "list_templates" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_templates
        """
        reqs = service.mcp_get("McpListTemplates", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def register_domain(body: dict) -> str:
        """
        注册一个域名。该操作会生成一个异步任务。您可以使用 get_async_task 查询该任务的状态。
        Call steps:
        1. Pass "register_domain" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  register_domain
        """
        reqs = service.mcp_post("McpRegisterDomain", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    return mcp
