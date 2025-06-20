# EBS MCP Server

This MCP server provides a tool to interact with the VolcEngine EBS Service, allowing you to retrieve information about EBS volumes and snapshots using ECS instance ID, EBS volume ID, or EBS snapshot ID.

## Setup

### Prerequisites

- Python 3.10 or higher
- API credentials (AK/SK)

### Installation

1. Install the package:

```bash
pip install -e .
```

Or with uv (recommended):

```bash
uv pip install -e .
```

### Configuration

The server requires the following environment variables:

- `VOLCENGINE_ACCESS_KEY`: Your VolcEngine access key
- `VOLCENGINE_SECRET_KEY`: Your VolcEngine secret key
- `VOLCENGINE_REGION`: Your VolcEngine region (e.g., "cn-beijing")

Optional environment variables:

- `PORT`: Port for the FastMCP server (default: 8000)

## Usage

### Running the Server

The server can be run with either stdio transport (for MCP integration) or SSE transport:

```bash
python -m mcp_server_ebs.server --transport stdio
```

Or:

```bash
python -m mcp_server_ebs.server --transport sse
```

### Available Tools

####  `describe_volumes`

Get volume config information based on a volume ID.

```python
describe_volumes(
    query="What are the status and configuration of the instance's attached volumes?",
    volume_id="vol-12345678",
)

describe_volumes(
    query="What's the volume status and configuration of this instance attached?",
    instance_id="i-12345678"
)
```

Parameters:
- `query` (Optional): Specific questions about the volume (status, size, type, etc.)
- `volume_id` (Optionanl): The ID of the EBS volume to query (e.g. "vol-12345678")
- `instance_id` (Optional): The ID of the ECS instance to which the EBS volume is attached (e.g. "i-12345678")

####  `describe_snapshots`

Get snapshot config information based on a snapshot ID.

```python
describe_snapshot(
    query="What's the status and configuration of this snapshot?",
    volume_id="snap-12345678"
)
```

Parameters:
- `query` (Optional): Specific questions about the volume (status, size, type, etc.)
- `snapshot_id` (required): The ID of the EBS snapshot to query (e.g. "snap-12345678")

####  `create_volume`

Create a new EBS volume with specified parameters.

```python
create_volume(
    volume_name="my-volume",
    zone_id="cn-beijing-a",
    size=40,
    volume_type="ESSD_PL0"
)
```

Parameters:
- `volume_name` (required): The name of the EBS volume to create
- `zone_id` (required): The ID of the zone where the volume will be created
- `size` (Optional): The size of the EBS volume in GiB (default: 40)
- `volume_type` (Optional): The type of the EBS volume (default: "ESSD_PL0")
- `region_id` (Optional): The ID of the region where the volume will be created
- `snapshot_id` (Optional): The ID of the snapshot to create volume from
- `volume_charge_type` (Optional): The charge type of the volume (default: "PostPaid")
- `instance_id` (Optional): The ID of the instance to attach the volume
- `query` (Optional): Specific questions about the volume

####  `create_snapshot`

Create a new EBS snapshot from specified volume.

```python
create_snapshot(
    volume_id="vol-12345678",
    snapshot_name="my-snapshot"
)
```

Parameters:
- `volume_id` (required): The ID of the EBS volume to create snapshot from
- `snapshot_name` (Optional): The name of the EBS snapshot to create
- `region_id` (Optional): The ID of the region where the snapshot will be created
- `query` (Optional): Specific questions about the snapshot

####  `extend_volume`

Extend the size of an existing EBS volume.

```python
extend_volume(
    volume_id="vol-12345678",
    new_size=80
)
```

Parameters:
- `volume_id` (required): The ID of the EBS volume to extend
- `new_size` (required): The new size of the EBS volume in GiB
- `region_id` (Optional): The ID of the region where the volume is located
- `query` (Optional): Specific questions about the volume

## MCP Integration

To add this server to your MCP configuration, add the following to your MCP settings file:

```json
{
  "mcpServers": {
    "ebs": {
      "command": "uvx",
        "args": [
          "--from",
          "git+https://${source-repo}#subdirectory=server/mcp_server_ebs",
          "mcp-server-ebs",
        ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your-access-key",
        "VOLCENGINE_SECRET_KEY": "your-secret-key",
        "VOLCENGINE_REGION": "your-resource-region",
        "PORT": "8000",
        "ENDPOINT": "api-endpoint"
      }
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify your AK/SK credentials are correct
   - Check that you have the necessary permissions for the collection

2. **Connection Timeouts**
   - Check your network connection to the VolcEngine API
   - Verify the host configuration is correct

3. **Empty Results**
   - Verify the collection name is correct
   - Try broadening your search query

### Logging

The server uses Python's logging module with INFO level by default. You can see detailed logs in the console when running the server.

## Contributing

Contributions to improve the Viking Knowledge Base MCP Server are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please ensure your code follows the project's coding standards and includes appropriate tests.

## License

This project is licensed under the terms specified by VolcEngine.
