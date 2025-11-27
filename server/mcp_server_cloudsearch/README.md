# MCP Server CloudSearch
| Version     | v1                                                                                                                                                                                |
|:------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Description | Cloud Search is a fully managed service providing data search and analytics capabilities including full-text search, vector search, hybrid search, and spatio-temporal retrieval. |
| Category    | Database                                                                                                                                                                          |
| Tags        | ES，Elasticsearch，OpenSearch，Search                                                                                                                                                |

## Tools
This MCP Server product provides the following Tools (capabilities), organized by functional category:

### Basic Resource Query
Used to query the basic environment and specifications required for instance creation.

- **`describe_zones`**
  Retrieves the list of Availability Zones (AZs) that support Cloud Search instance deployment in the current region.
- **`describe_node_available_specs`**
  Queries available node specifications, storage types, and corresponding billing configuration codes to assist in resource selection during instance creation.

### Lifecycle Management
Used to manage the instance creation, deployment, and initialization processes.

- **`create_instance`**
  Creates a new Cloud Search instance order (supports Elasticsearch or OpenSearch).
  *Note: This API only generates a pending order; resource deployment begins only after payment is completed.*
- **`create_instance_in_one_step`**
  Completes Cloud Search instance creation and payment in one step (supports Elasticsearch or OpenSearch).
  *Note: Once successfully called, the instance will immediately start deploying and billing.*

### Instance Information
Used to retrieve detailed status, configuration, and topology information of instances and their components.

- **`describe_instances`**
  Queries the instance list. Supports filtering by ID, name, status, etc., returning detailed configurations including network and specs.
- **`describe_instance`**
  Retrieves full details for a specific instance ID. Provides more granular configuration data than the list query.
- **`describe_instance_nodes`**
  Lists details of all member nodes within an instance, including node roles (e.g., Master/Data), hardware specifications, IP addresses, and real-time running status.
- **`describe_instance_plugins`**
  Retrieves the list of plugins currently installed on the instance, including plugin names, versions, and enablement status.

### Configuration & Operations
Used to modify instance attributes and perform critical maintenance operations.

- **`rename_instance`**
  Updates the display name (Alias) of a specific instance to facilitate business identification and management.
- **`modify_maintenance_setting`**
  Sets or adjusts the maintenance window for the instance. The system will perform necessary upgrades or patch updates during this period.
- **`modify_deletion_protection`**
  Enables or disables the "Deletion Protection" feature for the instance to prevent accidental release due to misoperation.
- **`restart_node`**
  Executes a restart operation on a specific node within an instance, typically used for fault recovery or enforcing certain configurations.

## Platform  
Ark, Trae, Cursor, Python

## Service Link
https://console.volcengine.com/es/region:es+cn-beijing/v2/create?projectName=default

## Installation and Deployment

### Dependencies
- Python 3.12+
- UV

### Environment Variables
| Environment Variable | Description | Default | Required |
| :--- | :--- | :--- | :--- |
| `VOLCENGINE_ACCESS_KEY` | Your Access Key | - | Yes |
| `VOLCENGINE_SECRET_KEY` | Your Secret Key | - | Yes |
| `VOLCENGINE_REGION` | The region | `cn-beijing` | No |

- Please get ak/sk from [volcengine](https://www.volcengine.com/docs/6291/65568).
- The default region is `cn-beijing`. The currently supported region codes are:
  - `cn-beijing`: China North 2 (Beijing)
  - `cn-shanghai`: China East 2 (Shanghai)
  - `cn-guangzhou`: China South 1 (Guangzhou)
  - `cn-hongkong`: China (Hong Kong)
  - `ap-southeast-1`: Asia Pacific Southeast 1 (Johor)
  - `ap-southeast-3`: Asia Pacific Southeast 3 (Jakarta)

### Deployment
Add the following configuration to your mcp settings file
```json
{
  "mcpServers": {
    "mcp-server-cloudsearch": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_cloudsearch",
        "mcp-server-cloudsearch"
      ],
      "env": {
        "VOLCENGINE_REGION": "cn-beijing",
        "VOLCENGINE_ACCESS_KEY": "your_volcengine_ak",
        "VOLC_SECRETKEY": "your_volcengine_sk"
      }
    }
  }
}
```
Or clone the repository to your local and start from the local code repository
```json
{
  "mcpServers": {
    "mcp-server-cloudsearch": {
      "command": "uv",
      "args": [
        "--directory",
        "path/to/server/mcp_server_cloudsearch/src/ESCloud",
        "run",
        "server.py"
      ],
      "env": {
        "VOLCENGINE_REGION": "cn-beijing",
        "VOLCENGINE_ACCESS_KEY": "your_volcengine_ak",
        "VOLC_SECRETKEY": "your_volcengine_sk"
      }
    }
  }
}
```

## License
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).