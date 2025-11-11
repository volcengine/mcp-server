from src.cr.api.api import CrAPI
from mcp.server.fastmcp import FastMCP
from .note import note
import json
import os


def create_mcp_server():
    service = CrAPI()
    mcp = FastMCP(
        name="CR MCP",
        host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
        port=int(os.getenv("MCP_SERVER_PORT", "8000")),
        stateless_http=os.getenv("STATLESS_HTTP", "true").lower() == "true",
        streamable_http_path=os.getenv("STREAMABLE_HTTP_PATH", "/mcp"),
        instructions="""
      ## MCP Invocation Method Guide
      - For task decomposition, it is necessary to use the mcp tool.
      - The first step requires invoking the `get_note` function to obtain the parameter description.
      - Subsequently, the corresponding method should be called to retrieve the data.
        Volcengine(火山引擎) CR(镜像仓库) MCP , 你的镜像仓库助手
      """,
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
    def create_namespace(params: dict, body: dict) -> str:
        """
        在指定的镜像仓库实例下创建命名空间。
        Call steps:
        1. Pass "create_namespace" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  create_namespace
        """
        reqs = service.mcp_post("CrMcpCreateNamespace", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def get_authorization_token(params: dict, body: dict) -> str:
        """
        获取登录镜像仓库实例的临时访问密钥。
        Call steps:
        1. Pass "get_authorization_token" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_authorization_token
        """
        reqs = service.mcp_post("CrMcpGetAuthorizationToken", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def list_domains(params: dict, body: dict) -> str:
        """
        查询镜像仓库实例域名。
        Call steps:
        1. Pass "list_domains" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_domains
        """
        reqs = service.mcp_post("CrMcpListDomains", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def list_tags(params: dict, body: dict) -> str:
        """
        查询指定 OCI 制品仓库下的一个或多个 OCI 制品（镜像、Helm Chart）版本。
        Call steps:
        1. Pass "list_tags" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_tags
        """
        reqs = service.mcp_post("CrMcpListTags", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def create_repository(params: dict, body: dict) -> str:
        """
        在指定命名空间下创建 OCI 制品仓库。
        Call steps:
        1. Pass "create_repository" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  create_repository
        """
        reqs = service.mcp_post("CrMcpCreateRepository", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def list_repositories(params: dict, body: dict) -> str:
        """
        查询指定镜像仓库实例下的一个或多个 OCI 制品仓库。
        Call steps:
        1. Pass "list_repositories" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_repositories
        """
        reqs = service.mcp_post("CrMcpListRepositories", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def list_namespaces(params: dict, body: dict) -> str:
        """
        查询指定镜像仓库实例下的单个或多个命名空间。
        Call steps:
        1. Pass "list_namespaces" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_namespaces
        """
        reqs = service.mcp_post("CrMcpListNamespaces", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def create_registry(params: dict, body: dict) -> str:
        """
        创建镜像仓库标准版实例。
        Call steps:
        1. Pass "create_registry" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  create_registry
        """
        reqs = service.mcp_post("CrMcpCreateRegistry", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def list_registries(params: dict, body: dict) -> str:
        """
        查询一个或多个镜像仓库实例。
        Call steps:
        1. Pass "list_registries" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_registries
        """
        reqs = service.mcp_post("CrMcpListRegistries", params, json.dumps(body))

        return reqs

    return mcp
