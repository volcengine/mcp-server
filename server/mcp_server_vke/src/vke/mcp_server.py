# coding=utf-8
import os
import http
import json
import yaml

from mcp.server.fastmcp import FastMCP

from .api.api import VkeAPI
from .note import note
from .k8s_api import (
    new_api_client,
    get_resources,
    patch_resource,
    create_resource,
    delete_resource,
    update_resource,
    apply_from_yaml,
)

allow_write = os.getenv("ALLOW_WRITE", "false").lower() == "true"


def create_mcp_server():
    mcp = FastMCP(
        name="VKE MCP",
        host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
        port=int(os.getenv("MCP_SERVER_PORT", "8000")),
        instructions="""
        ## MCP Invocation Method Guide
        The steps to invoke the MCP are as follows:
        - For task decomposition, it is necessary to use the mcp tool.
        - The first step requires invoking the `get_note` function to obtain the parameter description.
        - Subsequently, the corresponding method should be called.
        Notice:
        - For any operation that requires creation, deletion, or update any resources, you must confirm with the user before execution.
        - Any sensitive data should not be shown in the output.
        """,
    )

    @mcp.tool(
        description="""
        Guide
        """
    )
    async def guide():
        return """
        ## MCP Invocation Method Guide
        - For task decomposition, it is necessary to use the mcp tool.
        - The first step requires invoking the `get_note` function to obtain the parameter description.
        - Subsequently, the corresponding method should be called.
        Notice:
        - For any operation that requires creation, deletion, or update any resources, you must confirm with the user before execution.
        - Any sensitive data should not be shown in the output.
        """

    @mcp.tool(
        description="""
        Get parameter description

        Args:
            func_name: function name
        """
    )
    async def get_note(func_name: str) -> str:
        return note.get(func_name)

    @mcp.tool(
        description="""
        Create a container service cluster.
        Call steps:
        1. Pass "create_cluster" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, requires user confirmation to invoke create_cluster with the parameter description.
        """
    )
    async def create_cluster(params: dict, body: dict) -> str:
        if "Region" not in body:
            region = "cn-beijing"
        else:
            region = body["Region"]

        service = VkeAPI(mcp, region=region)
        reqs = service.mcp_post("VkeMcpCreateCluster", params, json.dumps(body))

        return reqs

    @mcp.tool(
        description="""
        Query the list of cluster details that meet the conditions.
        Call steps:
        1. Pass "list_clusters" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke list_clusters
        """
    )
    async def list_clusters(params: dict, body: dict) -> str:
        if "Region" not in body:
            region = "cn-beijing"
        else:
            region = body["Region"]

        service = VkeAPI(mcp, region=region)
        reqs = service.mcp_post("VkeMcpListClusters", params, json.dumps(body))

        return reqs

    @mcp.tool(
        description="""
        Query the list of Kubeconfig details of clusters that meet the conditions.
        Call steps:
        1. Pass "list_kubeconfigs" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke list_kubeconfigs
        Notice:
        - Any sensitive data MUST not be shown in the output.
        """
    )
    async def list_kubeconfigs(params: dict, body: dict) -> str:
        if "Region" not in body:
            region = "cn-beijing"
        else:
            region = body["Region"]

        service = VkeAPI(mcp, region=region)
        reqs = service.mcp_post("VkeMcpListKubeconfigs", params, json.dumps(body))

        return reqs

    @mcp.tool(
        description="""
        Generate Kubeconfig credentials for the cluster.
        Call steps:
        1. Pass "create_kubeconfig" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, requires user confirmation to invoke create_kubeconfig with the parameter description.
        """
    )
    async def create_kubeconfig(params: dict, body: dict) -> str:
        if "Region" not in body:
            region = "cn-beijing"
        else:
            region = body["Region"]

        service = VkeAPI(mcp, region=region)
        reqs = service.mcp_post("VkeMcpCreateKubeconfig", params, json.dumps(body))

        return reqs

    @mcp.tool(
        description="""
        Query the list of resource types of peripheral products supported by the container service.
        Call steps:
        1. Pass "list_supported_resource_types" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke list_supported_resource_types
        """
    )
    async def list_supported_resource_types(params: dict, body: dict) -> str:
        if "Region" not in body:
            region = "cn-beijing"
        else:
            region = body["Region"]

        service = VkeAPI(mcp, region=region)
        reqs = service.mcp_post(
            "VkeMcpListSupportedResourceTypes", params, json.dumps(body)
        )

        return reqs

    @mcp.tool(
        description="""
        Query the list of component details currently supported by the container service.
        Call steps:
        1. Pass "list_supported_addons" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke list_supported_addons
        """
    )
    async def list_supported_addons(params: dict, body: dict) -> str:
        if "Region" not in body:
            region = "cn-beijing"
        else:
            region = body["Region"]

        service = VkeAPI(mcp, region=region)
        reqs = service.mcp_post("VkeMcpListSupportedAddons", params, json.dumps(body))

        return reqs

    @mcp.tool(
        description="""
        Install components for the specified cluster.
        Call steps:
        1. Pass "create_addon" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, requires user confirmation to invoke create_addon with the parameter description.
        """
    )
    async def create_addon(params: dict, body: dict) -> str:
        if "Region" not in body:
            region = "cn-beijing"
        else:
            region = body["Region"]

        service = VkeAPI(mcp, region=region)
        reqs = service.mcp_post("VkeMcpCreateAddon", params, json.dumps(body))

        return reqs

    @mcp.tool(
        description="""
        Update the specified component configuration under the specified cluster.
        Call steps:
        1. Pass "update_addon_config" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, requires user confirmation to invoke update_addon_config with the parameter description.
        """
    )
    async def update_addon_config(params: dict, body: dict) -> str:
        if "Region" not in body:
            region = "cn-beijing"
        else:
            region = body["Region"]

        if not allow_write:
            raise ValueError("update operation is not allowed")

        service = VkeAPI(mcp, region=region)
        reqs = service.mcp_post("VkeMcpUpdateAddonConfig", params, json.dumps(body))

        return reqs

    @mcp.tool(
        description="""
        Query the list of installed component details that meet the conditions.
        Call steps:
        1. Pass "list_addons" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke list_addons
        """
    )
    async def list_addons(params: dict, body: dict) -> str:
        if "Region" not in body:
            region = "cn-beijing"
        else:
            region = body["Region"]

        service = VkeAPI(mcp, region=region)
        reqs = service.mcp_post("VkeMcpListAddons", params, json.dumps(body))

        return reqs

    @mcp.tool(
        description="""
        Update the specified component version under the specified cluster.
        Call steps:
        1. Pass "update_addon_version" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, requires user confirmation to invoke update_addon_version with the parameter description.
        """
    )
    async def update_addon_version(params: dict, body: dict) -> str:
        if "Region" not in body:
            region = "cn-beijing"
        else:
            region = body["Region"]

        if not allow_write:
            raise ValueError("update operation is not allowed")

        service = VkeAPI(mcp, region=region)
        reqs = service.mcp_post("VkeMcpUpdateAddonVersion", params, json.dumps(body))

        return reqs

    @mcp.tool(
        description="""
        Create a node pool under the specified cluster.
        Call steps:
        1. Pass "create_node_pool" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, requires user confirmation to invoke create_node_pool with the parameter description.
        """
    )
    async def create_node_pool(params: dict, body: dict) -> str:
        if "Region" not in body:
            region = "cn-beijing"
        else:
            region = body["Region"]

        service = VkeAPI(mcp, region=region)
        reqs = service.mcp_post("VkeMcpCreateNodePool", params, json.dumps(body))

        return reqs

    @mcp.tool(
        description="""
        Query the list of node pool information that meets the conditions.
        Call steps:
        1. Pass "list_node_pools" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke list_node_pools
        """
    )
    async def list_node_pools(params: dict, body: dict) -> str:
        if "Region" not in body:
            region = "cn-beijing"
        else:
            region = body["Region"]

        service = VkeAPI(mcp, region=region)
        reqs = service.mcp_post("VkeMcpListNodePools", params, json.dumps(body))

        return reqs

    @mcp.tool(
        description="""
        Create a default node pool under the specified cluster.
        Call steps:
        1. Pass "create_default_node_pool" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, requires user confirmation to invoke create_default_node_pool with the parameter description.
        """
    )
    async def create_default_node_pool(params: dict, body: dict) -> str:
        if "Region" not in body:
            region = "cn-beijing"
        else:
            region = body["Region"]

        service = VkeAPI(mcp, region=region)
        reqs = service.mcp_post("VkeMcpCreateDefaultNodePool", params, json.dumps(body))

        return reqs

    @mcp.tool(
        description="""
        Create nodes.
        Call steps:
        1. Pass "create_nodes" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, requires user confirmation to invoke create_nodes with the parameter description.
        """
    )
    async def create_nodes(params: dict, body: dict) -> str:
        if "Region" not in body:
            region = "cn-beijing"
        else:
            region = body["Region"]

        service = VkeAPI(mcp, region=region)
        reqs = service.mcp_post("VkeMcpCreateNodes", params, json.dumps(body))

        return reqs

    @mcp.tool(
        description="""
        Query the node list.
        Call steps:
        1. Pass "list_nodes" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke list_nodes
        """
    )
    async def list_nodes(params: dict, body: dict) -> str:
        if "Region" not in body:
            region = "cn-beijing"
        else:
            region = body["Region"]

        service = VkeAPI(mcp, region=region)
        reqs = service.mcp_post("VkeMcpListNodes", params, json.dumps(body))

        return reqs

    @mcp.tool(
        description="""
        Create a virtual node.
        Call steps:
        1. Pass "create_virtual_node" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, requires user confirmation to invoke create_virtual_node with the parameter description.
        """
    )
    async def create_virtual_node(params: dict, body: dict) -> str:
        if "Region" not in body:
            region = "cn-beijing"
        else:
            region = body["Region"]

        service = VkeAPI(mcp, region=region)
        reqs = service.mcp_post("VkeMcpCreateVirtualNode", params, json.dumps(body))

        return reqs

    @mcp.tool(
        description="""
        Query the virtual node list.
        Call steps:
        1. Pass "list_virtual_nodes" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke list_virtual_nodes
        """
    )
    async def list_virtual_nodes(params: dict, body: dict) -> str:
        if "Region" not in body:
            region = "cn-beijing"
        else:
            region = body["Region"]

        service = VkeAPI(mcp, region=region)
        reqs = service.mcp_post("VkeMcpListVirtualNodes", params, json.dumps(body))

        return reqs

    @mcp.tool(
        description="""
        Query the list of k8s resources that meet the conditions.
        Call steps:
        1. Pass "list_k8s_resources" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke list_k8s_resources
        """
    )
    async def list_k8s_resources(params: dict, body: dict) -> str:
        if "Region" not in body:
            region = "cn-beijing"
        else:
            region = body["Region"]

        if "ClusterId" not in body:
            raise ValueError("ClusterId is required")
        if "Kind" not in body:
            raise ValueError("Kind is required")
        if "ApiVersion" not in body:
            raise ValueError("ApiVersion is required")

        service = VkeAPI(mcp, region=region)
        cluster_id = body["ClusterId"]
        kind = body["Kind"]
        api_version = body["ApiVersion"]

        response = get_resources(
            new_api_client(service, cluster_id),
            kind,
            api_version,
            namespace=body.get("Namespace", ""),
            label_selectors=body.get("LabelSelectors", ""),
            field_selectors=body.get("FieldSelectors", ""),
            limit=body.get("Limit", 500),
        )

        return json.dumps(response)

    @mcp.tool(
        description="""
        Manage k8s resources.
        Call steps:
        1. Pass "manage_k8s_resources" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, requires user confirmation to invoke manage_k8s_resources with the parameter description.
        3. Ask user to confirm the operation and show the parameters before invoking the API.
        """
    )
    async def manage_k8s_resources(params: dict, body: dict) -> str:
        if "Region" not in body:
            region = "cn-beijing"
        else:
            region = body["Region"]

        if "ClusterId" not in body:
            raise ValueError("ClusterId is required")
        if "Kind" not in body:
            raise ValueError("Kind is required")
        if "ApiVersion" not in body:
            raise ValueError("ApiVersion is required")
        if "Method" not in body:
            raise ValueError("Method is required")

        service = VkeAPI(mcp, region=region)

        cluster_id = body["ClusterId"]
        kind = body["Kind"]
        api_version = body["ApiVersion"]
        method = body["Method"]

        api_client = new_api_client(service, cluster_id)

        if method == http.HTTPMethod.DELETE:
            response = delete_resource(
                api_client,
                kind,
                api_version,
                namespace=body.get("Namespace", ""),
                name=body.get("Name", ""),
            )
        elif method == http.HTTPMethod.PUT:
            response = update_resource(
                api_client,
                kind,
                api_version,
                body.get("Body", {}),
                namespace=body.get("Namespace", ""),
                name=body.get("Name", ""),
            )
        elif method == http.HTTPMethod.POST:
            response = create_resource(
                api_client,
                kind,
                api_version,
                body.get("Body", {}),
                namespace=body.get("Namespace", ""),
            )
        elif method == http.HTTPMethod.PATCH:
            response = patch_resource(
                api_client,
                kind,
                api_version,
                body.get("Body", {}),
                namespace=body.get("Namespace", ""),
                name=body.get("Name", ""),
            )
        else:
            raise ValueError(f"unsupported method: {method}")

        return json.dumps(response)

    @mcp.tool(
        description="""
        Apply k8s resources from YAML.
        Call steps:
        1. Pass "apply_yaml" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, requires user confirmation to invoke apply_yaml with the parameter description.
        3. Ask user to confirm the operation and show the parameters before invoking the API.
        """
    )
    async def apply_yaml(params: dict, body: dict) -> str:
        if "Region" not in body:
            region = "cn-beijing"
        else:
            region = body["Region"]

        if "ClusterId" not in body:
            raise ValueError("ClusterId is required")
        if "Content" not in body:
            raise ValueError("Content is required")

        service = VkeAPI(mcp, region=region)

        cluster_id = body["ClusterId"]
        yaml_content = body["Content"]

        response = apply_from_yaml(
            new_api_client(service, cluster_id),
            yaml.safe_load_all(yaml_content),
            namespace=body.get("Namespace", ""),
            force=body.get("Force", False),
        )

        return json.dumps(response)

    return mcp
