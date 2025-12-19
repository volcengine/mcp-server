# VKE MCP Server

## Version
v0.1.0

## Description

VKE (Volcengine Kubernetes Engine) MCP Server is a server that implements the Model Context Protocol (MCP). It can be integrated into MCP clients (such as Ark, Trae, Cursor, etc.) to provide the ability to interact with the Volcengine VKE service. It allows managing clusters, nodes, node pools, and addons using natural language. It also supports querying and managing K8s cluster resources and applying YAML configurations to K8s clusters.

## Category

Container Service

## Tags

Cloud Native, Container, K8s, VKE

## Tools

This MCP Server provides the following Tools (tools/capabilities):

VKE cluster, node, node pool, addon, and other management operations:

- `create_addon`: Create an addon
- `create_cluster`: Create a cluster
- `create_default_node_pool`: Create a default node pool
- `create_kubeconfig`: Create a kubeconfig
- `create_node_pool`: Create a node pool
- `create_nodes`: Create nodes
- `create_virtual_node`: Create a virtual node
- `list_addons`: List addons
- `list_clusters`: List clusters
- `list_kubeconfigs`: List kubeconfigs
- `list_node_pools`: List node pools
- `list_nodes`: List nodes
- `list_supported_addons`: List supported addons
- `list_supported_resource_types`: List supported resource types
- `list_virtual_nodes`: List virtual nodes
- `update_addon_config`: Update addon configuration
- `update_addon_version`: Update addon version

K8s resource management operations:

- `apply_yaml`: Apply YAML configuration to a K8s cluster
- `list_k8s_resources`: List K8s resources
- `manage_k8s_resources`: Manage K8s resources (e.g., create, delete, update K8s resources)

Note: Deleting or updating clusters, node pools, or nodes is temporarily not supported.

## Compatible Platforms

Ark, Trae, Cursor, Python

## Service Activation Link (Overall Product)

[Volcengine – VKE Container Service](https://console.volcengine.com/vke)

## Authentication

AccessKey/SecretKey

Recommendations:

1. Create a dedicated IAM role specifically for MCP server operations.
2. Apply the principle of least privilege by attaching only the necessary policies for your use case.
  - If only query operations are needed, configure the `VKEReadOnlyAccess` policy.
  - If support for creating clusters and other operations is also required, configure the `VKEFullAccess` policy.
3. Use resource-scoped policies whenever possible.
4. Apply permission boundaries to limit the maximum permissions.

## Installation and Deployment

### Dependencies

- Python 3.12+
- UV

### Environment Configuration

Environment Variables:

| Environment Variable | Description | Default Value | Required |
| :--- | :--- | :--- | :--- |
| `VOLCENGINE_ACCESS_KEY` | Access Key | - | Yes |
| `VOLCENGINE_SECRET_KEY` | Secret Key | - | Yes |
| `VOLCENGINE_SESSION_TOKEN`| Temporary session token | - | No |
| `ALLOW_WRITE` | Whether to enable write permissions for update and delete operations | `false` | No |

Note:

- When `ALLOW_WRITE` is `true`, the following will be supported:
  - Updating and deleting K8s resources (via the `manage_k8s_resources` tool)
  - Updating Addon versions and configurations (via the `update_addon_version` and `update_addon_config` tools)
- The following operations are not affected by `ALLOW_WRITE` and are not supported:
  - **Updating** and **deleting** clusters, nodes, and node pools
- The default region is `cn-beijing`. To operate on resources in other regions, you can specify the region in the prompt. Common regions include:
  - `cn-beijing`: China North 2 (Beijing)
  - `cn-beijing2`: China North 3 (Beijing)
  - `cn-datong`: China North 4 (Datong)
  - `cn-wulanchabu`: China North 5 (Ulanqab)
  - `cn-shanghai`: China East 2 (Shanghai)
  - `cn-guangzhou`: China South 1 (Guangzhou)
  - `cn-hongkong`: China (Hong Kong)
  - `ap-southeast-1`: Asia Pacific SE 1 (Johor)
  - `ap-southeast-3`: Asia Pacific SE 3 (Jakarta)

### Deploy in Trae

Manually add the MCP in Trae with the following configuration:

```json
{
  "mcpServers": {
    "vke": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_vke",
        "mcp-server-vke"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "YOUR_AK",
        "VOLCENGINE_SECRET_KEY": "YOUR_SK",
        "VOLCENGINE_SESSION_TOKEN": "YOUR_ST",
        "ALLOW_WRITE": "false" // Note: Please enable write permissions only when necessary to avoid data loss due to operational errors.
      }
    }
  }
}
```

## License

MIT