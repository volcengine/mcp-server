# MCP Server CloudSearch
| Version     | v1                                                                                                                                                                                |
|:------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Description | Cloud Search is a fully managed service providing data search and analytics capabilities including full-text search, vector search, hybrid search, and spatio-temporal retrieval. |
| Category    | Database                                                                                                                                                                          |
| Tags        | ES，Elasticsearch，OpenSearch，Search                                                                                                                                                |

## Tools
This MCP Server product provides the following Tools:
### 1. describe_zones
 - Detailed Description: Query the list of available zones.
### 2. describe_instances
 - Detailed Description: Query the list of Cloud Search instances and their configuration details.
### 3. create_instance_in_one_step
 - Detailed Description: This interface is used to create an instance (runs immediately and starts billing). It supports creating ElasticSearch (ES) or OpenSearch (OS) instances.
### 4. describe_node_available_specs
 - Detailed Description: Query the list of available node types, node specifications, and storage specifications; returns billing configuration codes.
### 5. describe_instance_plugins
 - Detailed Description: Query the list of plugins installed on the instance.
### 6. rename_instance
 - Detailed Description: Modify the name of the target instance.
### 7. modify_maintenance_setting
 - Detailed Description: Modify the maintenance time of the instance.
### 8. modify_deletion_protection
 - Detailed Description: Enable or disable the deletion protection feature for the instance.
### 9. describe_instance
 - Detailed Description: Query the configuration details of a specified instance.
### 10. restart_node
 - Detailed Description: Restart a specific member node of the instance.
### 11. describe_instance_nodes
 - Detailed Description: Query details of the instance's member nodes, including node type, running status, resource configuration, etc.
### 12. create_instance
 - Detailed Description: This interface is used to create an instance (order placed only, pending payment). It supports creating ElasticSearch (ES) or OpenSearch (OS) instances.
   When creating an instance using this interface, dedicated Master nodes must be configured, and the number of Master nodes must be 3.

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
        "VOLC_ACCESSKEY": "your_volcengine_ak",
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
        "VOLC_ACCESSKEY": "your_volcengine_ak",
        "VOLC_SECRETKEY": "your_volcengine_sk"
      }
    }
  }
}
```

## License
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).