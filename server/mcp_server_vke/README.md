# VKE MCP Server

## Version
v0.1.0

## Description

VKE (Volcengine Kubernetes Engine) MCP Server is a server that implements the Model Context Protocol. It can be integrated into MCP clients (such as Trae, Cursor, etc.) to provide the ability to interact with Volcengine's VKE service, enabling cluster management, node and node pool management, and component management using natural language. It also supports querying and managing K8s cluster resources and applying YAML configurations to K8s clusters.

## Category

Container Service

## Tags

Container Service, K8s, VKE

## Tools

This MCP Server product provides the following tools/capabilities:

VKE cluster, node, node pool and addon management operations:

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


Note: Deleting or updating clusters, node pools, nodes, etc., is temporarily not supported.

## Compatible Platforms

Trae, Cursor

## Service Activation Link (Full Product)

[Volcengine - VKE Container Service](https://console.volcengine.com/vke)

## Authentication

Create an API Key (AccessKey/SecretKey) in the IAM console and ensure that the API Key has `VKEFullAccess` permissions for VKE.

## Installation and Deployment

### Dependencies

- Python 3.11+
- UV

### Environment Configuration

Environment Variables:

| Environment Variable | Description | Default | Required |
| :--- | :--- | :--- | :--- |
| `VOLCENGINE_ACCESS_KEY` | Your Access Key | - | Yes |
| `VOLCENGINE_SECRET_KEY` | Your Secret Key | - | Yes |
| `VOLCENGINE_SESSION_TOKEN`| Temporary session token | - | No |
| `VOLCENGINE_REGION` | The region | `cn-beijing` | No |
| `ALLOW_WRITE` | Whether to enable write permissions for update and delete operations | `false` | No |
| `MCP_SERVER_MODE` | Whether to enable remote deployment mode | `local` | No |

Note:
- All create and query operations are not affected by `ALLOW_WRITE`.
- Updating and deleting clusters, nodes, node pools, scaling policies, etc., are not affected by `ALLOW_WRITE` as these operations are not supported.
- When `ALLOW_WRITE` is `true`, the following will be supported:
  - Updating and deleting K8s resources (via the `manage_k8s_resources` tool)
  - Updating Addon versions and configurations

The default region is `cn-beijing`. The currently supported region codes and their corresponding names are:

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
        "VOLCENGINE_REGION": "YOUR_REGION",
        "ALLOW_WRITE": "false" // Note: Please enable write permissions only when necessary to avoid data loss due to operational errors.
      }
    }
  }
}
```

## License

MIT