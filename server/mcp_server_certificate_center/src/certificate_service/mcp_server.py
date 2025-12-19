from src.certificate_service.api.api import CertificateServiceAPI
from mcp.server.fastmcp import FastMCP
from .note import note
from src.utils.response import HandlerVolcResponse
import json


def create_mcp_server():
    service = CertificateServiceAPI()
    mcp = FastMCP(
        "证书中心 MCP",
        instructions="Volcengine(火山引擎) 证书中心 MCP, 提供证书相关的服务",
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
    def quick_apply_certificate(body: dict) -> str:
        """
        调用本接口创建一个付费证书订单并提交证书申请。
        Call steps:
        1. Pass "quick_apply_certificate" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  quick_apply_certificate
        """
        reqs = service.mcp_post("McpQuickApplyCertificate", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def certificate_get_instance(body: dict) -> str:
        """
        调用本接口查询指定SSL证书实例的详情。
        Call steps:
        1. Pass "certificate_get_instance" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  certificate_get_instance
        """
        reqs = service.mcp_post("McpCertificateGetInstance", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def import_certificate(body: dict) -> str:
        """
        调用本接口上传一本SSL证书到证书中心。
        Call steps:
        1. Pass "import_certificate" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  import_certificate
        """
        reqs = service.mcp_post("McpImportCertificate", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def certificate_get_instance_list(body: dict) -> str:
        """
        调用本接口获取SSL证书实例列表。
        Call steps:
        1. Pass "certificate_get_instance_list" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  certificate_get_instance_list
        """
        reqs = service.mcp_post("McpCertificateGetInstanceList", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def certificate_add_organization(body: dict) -> str:
        """
        调用本接口创建一个证书的信息模板。
        Call steps:
        1. Pass "certificate_add_organization" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  certificate_add_organization
        """
        reqs = service.mcp_post("McpCertificateAddOrganization", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def certificate_get_organization(body: dict) -> str:
        """
        调用本接口获取一个证书的信息模板详情。
        Call steps:
        1. Pass "certificate_get_organization" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  certificate_get_organization
        """
        reqs = service.mcp_post("McpCertificateGetOrganization", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def certificate_get_organization_list(body: dict) -> str:
        """
        调用本接口获取已有的证书信息模板列表。
        Call steps:
        1. Pass "certificate_get_organization_list" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  certificate_get_organization_list
        """
        reqs = service.mcp_post(
            "McpCertificateGetOrganizationList", {}, json.dumps(body)
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def list_tags_for_resources(body: dict) -> str:
        """
        调用本接口查询您的证书中心资源绑定的标签。
        Call steps:
        1. Pass "list_tags_for_resources" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_tags_for_resources
        """
        reqs = service.mcp_post("McpListTagsForResources", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    return mcp
