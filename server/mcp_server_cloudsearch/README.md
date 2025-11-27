# MCP Server: CloudSearch

| Version | v2.0.0 |
|:---|:--------------------------------------------|
| Description | Cloud Search is a fully managed, one-stop information retrieval and analytics platform provided by Volcengine, supporting core capabilities such as full-text search, vector search, hybrid search, and spatio-temporal retrieval. |
| Category    | Database |
| Tags        | ES，Elasticsearch，OpenSearch，Search |

## 🛠️ Core Capabilities (Tools)

This service provides a set of tools allowing AI models to directly execute the following operations within a conversation:

### 1. Basic Resource Query
Used to query the basic environment and specifications required for instance creation.

- **`describe_zones`**
  Retrieves the list of Availability Zones (AZs) that support Cloud Search instance deployment in the current region.
- **`describe_node_available_specs`**
  Queries available node specifications, storage types, and corresponding billing configuration codes to assist in resource selection during instance creation.

### 2. Lifecycle Management
Used to manage the instance creation, deployment, and initialization processes.

- **`create_instance`**
  Creates a new Cloud Search instance order (supports Elasticsearch or OpenSearch).
  *Note: This API only generates a pending order; resource deployment begins only after payment is completed.*
- **`create_instance_in_one_step`**
  Completes Cloud Search instance creation and payment in one step (supports Elasticsearch or OpenSearch).
  *Note: Once successfully called, the instance will immediately start deploying and billing.*

### 3. Instance Information
Used to retrieve detailed status, configuration, and topology information of instances and their components.

- **`describe_instances`**
  Queries the instance list. Supports filtering by ID, name, status, etc., returning detailed configurations including network and specs.
- **`describe_instance`**
  Retrieves full details for a specific instance ID. Provides more granular configuration data than the list query.
- **`describe_instance_nodes`**
  Lists details of all member nodes within an instance, including node roles (e.g., Master/Data), hardware specifications, IP addresses, and real-time running status.
- **`describe_instance_plugins`**
  Retrieves the list of plugins currently installed on the instance, including plugin names, versions, and enablement status.

### 4. Configuration & Operations
Used to modify instance attributes and perform critical maintenance operations.

- **`rename_instance`**
  Updates the display name (Alias) of a specific instance to facilitate business identification and management.
- **`modify_maintenance_setting`**
  Sets or adjusts the maintenance window for the instance. The system will perform necessary upgrades or patch updates during this period.
- **`modify_deletion_protection`**
  Enables or disables the "Deletion Protection" feature for the instance to prevent accidental release due to misoperation.
- **`restart_node`**
  Executes a restart operation on a specific node within an instance, typically used for fault recovery or enforcing certain configurations.

## Supported Platforms
This Server follows the MCP standard protocol and supports various common platforms:
* **IDE**: Cursor, Trae, VS Code
* **Platform**: Ark (方舟)

## Service Link (Product Page)
https://console.volcengine.com/es/region:es+cn-beijing/v2/create?projectName=default

## 💻 Integration Guide

### 1. Dependencies
- Python >= 3.11
- Install [UV](https://github.com/astral-sh/uv)

### 2. Obtain Credentials
Please visit the [Volcengine IAM: API Access Key](https://console.volcengine.com/iam/keymanage/) page to obtain your `Access Key` and `Secret Key`.
- Reference Document: [Access Key Management](https://www.volcengine.com/docs/6291/65568).

### 3. Parameter Configuration
Running the MCP Server requires configuring the following environment variables:

| Environment Variable | Description | Example |
| :--- | :--- | :--- |
| `VOLCENGINE_ACCESS_KEY` | Access Key ID | `AKLTzte...` |
| `VOLCENGINE_SECRET_KEY` | Secret Access Key | `TnpCa1...` |
| `VOLCENGINE_REGION` | Region Code (Default `cn-beijing`) | `cn-shanghai` |

**Supported Region Codes:**
- `cn-beijing`: China North 2 (Beijing)
- `cn-shanghai`: China East 2 (Shanghai)
- `cn-guangzhou`: China South 1 (Guangzhou)
- `cn-hongkong`: China (Hong Kong)
- `ap-southeast-1`: Asia Pacific Southeast 1 (Johor)
- `ap-southeast-3`: Asia Pacific Southeast 3 (Jakarta)

## 🚀 Quick Deployment (MCP Settings)
Please add the following configuration to your MCP client configuration file (e.g., `mcp.json` in Cursor or Trae settings).

### Method 1: Use uvx to run directly (Recommended)
No source code download required. Loads directly from the remote repository, suitable for quick usage.

```json
{
  "mcpServers": {
    "CloudSearch": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_cloudsearch",
        "mcp-server-cloudsearch"
      ],
      "env": {
        "VOLCENGINE_REGION": "cn-beijing",
        "VOLCENGINE_ACCESS_KEY": "your_volcengine_ak",
        "VOLCENGINE_SECRET_KEY": "your_volcengine_sk"
      }
    }
  }
}
```

### Method 2: Run from local source

```json
{
  "mcpServers": {
    "CloudSearch": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/mcp-server/server/mcp_server_cloudsearch/src/ESCloud",
        "run",
        "server.py"
      ],
      "env": {
        "VOLCENGINE_REGION": "cn-beijing",
        "VOLCENGINE_ACCESS_KEY": "your_volcengine_ak",
        "VOLCENGINE_SECRET_KEY": "your_volcengine_sk"
      }
    }
  }
}
```

*Note: When running locally, please ensure you replace the path in `args` with the **absolute path** of your local repository.*

## License
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).