#!/usr/bin/env python3
import argparse
import base64
import json
import logging
import os
import time
from datetime import datetime # Added for _parse_and_validate_sts_token

from typing import Dict, Optional # Removed Tuple as it's no longer used by _parse_and_validate_sts_token

import volcenginesdkcore
import volcenginesdkstorageebs
from starlette.requests import Request

from mcp_server_ebs.config import load_config
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession

# Configure structured logging (moved logger definition higher for visibility)
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mcp_server_ebs.log')
logger = logging.getLogger(__name__) # Define logger earlier
logger.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - '
        'module=%(module)s func=%(funcName)s line=%(lineno)d - %(message)s'
)

# Create handlers
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(stream_handler)

def _parse_and_validate_sts_token(auth_header_value: str) -> Dict[str, str]: # Changed signature
    """Helper function to parse and validate STS token from authorization header.
    
    Args:
        auth_header_value: The raw authorization header string.

    Returns:
        A dictionary containing 'ak', 'sk', and optionally 'session_token'.

    Raises:
        ValueError: If the token is invalid, expired, or processing fails.
    """
    try:
        base64_data = auth_header_value.split(' ')[1] if ' ' in auth_header_value else auth_header_value
        decoded_str = base64.b64decode(base64_data).decode('utf-8')
        data = json.loads(decoded_str)

        # Validate token expiration
        current_time_str = data.get('CurrentTime')
        expired_time_str = data.get('ExpiredTime')
        if current_time_str and expired_time_str:
            try:
                current_dt = datetime.fromisoformat(current_time_str)
                expired_dt = datetime.fromisoformat(expired_time_str)
                if current_dt > expired_dt:
                    logger.error("STS token expired")
                    # return None, {"error": "sts token is expired"}
                    raise ValueError("STS token is expired")
            except ValueError as e:
                logger.error(f"Invalid time format in STS token: {str(e)}")
                # return None, {"error": f"Invalid time format in STS token: {str(e)}"}
                raise ValueError(f"Invalid time format in STS token: {str(e)}")

        credentials = {
            'ak': data.get('AccessKeyId'),
            'sk': data.get('SecretAccessKey')
        }
        if 'SessionToken' in data:
            credentials['session_token'] = data['SessionToken']
        
        if not credentials.get('ak') or not credentials.get('sk'):
            logger.error("AccessKeyId or SecretAccessKey missing in STS token")
            # return None, {"error": "AccessKeyId or SecretAccessKey missing in STS token"}
            raise ValueError("AccessKeyId or SecretAccessKey missing in STS token")

        return credentials # Changed: return only credentials on success

    except Exception as e:
        logger.error(f"Failed to decode or process auth data: {str(e)}", exc_info=True)
        # return None, {"error": f"Authentication data processing failed: {str(e)}"}
        raise ValueError(f"Authentication data processing failed: {str(e)}")

def init_ebs_service(config: object, region_id: str = None) -> volcenginesdkstorageebs.STORAGEEBSApi:
    """
    Initialize EBS service configuration and return client instance
    
    Args:
        config: Configuration object containing endpoint, access keys and region
        region_id: Optional region override
        
    Returns:
        Initialized STORAGEEBSApi client instance.

    Raises:
        ValueError: If authentication fails (e.g., STS token issues, missing credentials).
        ConnectionError: If the EBS service client fails to initialize.
    """
    configuration = volcenginesdkcore.Configuration()
    configuration.host = config.endpoint

    # Get request context
    ctx: Context[ServerSession, object] = mcp.get_context()
    raw_request: Request = ctx.request_context.request

    # Handle authentication
    auth_header = None
    if raw_request:
        auth_header = raw_request.headers.get("authorization", None)
        if auth_header is None:
            # If no auth info in header, it might be stdio mode, try to get from environment variables
            auth_header = os.getenv("authorization", None)
        
        if auth_header:
            try:
                credentials = _parse_and_validate_sts_token(auth_header)
                # _parse_and_validate_sts_token now raises an exception on error or returns valid credentials.
                # No need to check for error_detail or if credentials is None explicitly here,
                # as an exception would have been raised already.
                
                configuration.ak = credentials.get('ak') # Corrected key to 'ak'
                configuration.sk = credentials.get('sk') # Corrected key to 'sk'
                configuration.session_token = credentials.get('session_token') # Corrected key to 'session_token'

                if not configuration.ak or not configuration.sk:
                    # This should ideally be caught by _parse_and_validate_sts_token, but as a safeguard:
                    logger.error("Critical credentials (AK/SK) missing after STS token parsing.")
                    raise ValueError("Authentication failed: AK/SK missing from parsed STS token.")

            except ValueError as e:
                logger.error(f"STS token validation or processing failed: {str(e)}")
                raise ValueError(f"Authentication failed due to STS token issue: {str(e)}")
        else:
            # Fallback to config credentials if no auth_header is present
            configuration.ak = config.access_key_id
            configuration.sk = config.access_key_secret
            if not configuration.ak or not configuration.sk:
                 logger.error("Fallback credentials (AK/SK) missing from config.")
                 raise ValueError("Authentication failed: AK/SK missing from configuration.")
    else:
        # Fallback to config credentials if no raw_request (e.g. during startup or specific test scenarios)
        configuration.ak = config.access_key_id
        configuration.sk = config.access_key_secret

    # Set region
    configuration.region = region_id if region_id else config.region
    
    try:
        volcenginesdkcore.Configuration.set_default(configuration)
        logger.info("Successfully initialized EBS service configuration")
        return volcenginesdkstorageebs.STORAGEEBSApi()
    except Exception as e:
        logger.error(f"Failed to initialize EBS service: {str(e)}", 
                    exc_info=True, stack_info=True)
        # return {"error": f"Service initialization failed: {str(e)}"}
        raise ConnectionError(f"EBS service initialization failed: {str(e)}")

# Global variables
storage_ebs_service = None

# Create MCP server
mcp = FastMCP("Storage EBS MCP Server", 
    port=int(os.getenv("PORT", "8000")),
    host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"))

@mcp.tool()
def describe_volume(
    volume_id: Optional[str] = None,
    instance_id: Optional[str] = None,
    region_id: Optional[str] = None,
    query: Optional[str] = None
) -> Dict:
    """Query information about a specific EBS volume.
    This tool retrieves details of an EBS volume including status, size, creation time etc.

    Args:
        volume_id: The ID of the EBS volume id to query (e.g. "vol-12345678")
        instance_id: The ID of the instance associated with the volume (e.g. "i-12345678")
        query: Optional specific questions about the volume(status, size, creation time etc.)
    """

    ebs_cli = init_ebs_service(config,region_id)
    try:
        volumes_ids = []
        if volume_id is not None:
            volumes_ids = [volume_id]
        describe_request = volcenginesdkstorageebs.DescribeVolumesRequest(
            volume_ids=volumes_ids,
            instance_id=instance_id
        )

        describe_response = ebs_cli.describe_volumes(describe_request)
        if not describe_response.volumes:
            error_msg = f"No volume found with ID: {volume_id}"
            if instance_id:
                error_msg += f" or instance ID: {instance_id}"
            return {"error": error_msg}
            
        # Iterate through all volumes
        volumes_data = []
        for volume in describe_response.volumes:
            volumes_data.append({
                "volume_id": volume.volume_id,
                "status": volume.status,
                "size": volume.size,
                # Add other required fields here
            })
            
        return {
            "volumes": volumes_data,
            "count": len(volumes_data),
            "data": describe_response.to_str()
        }

    except Exception as e:
        logger.error(
            "Error in describe_volume",
            extra={
                "error": str(e),
                "volume_id": volume_id,
                "instance_id": instance_id,
                "region_id": region_id
            }
        )
        return {
            "error": "Failed to describe volume",
            "details": str(e),
            "code": "EBS_DESCRIBE_VOLUME_ERROR"
        }


@mcp.tool()
def describe_snapshot(
    snapshot_id: str,
    region_id: Optional[str] = None,
    query: Optional[str] = None
) -> Dict:
    """Query information about a specific EBS snapshot.
    This tool retrieves details of an EBS snapshot including status, size, creation time etc.

    Args:
        snapshot_id: The ID of the EBS snapshot to query (e.g. "snap-12345678")
        region_id: The ID of the region where the snapshot is located (e.g. "cn-beijing")
        query: Optional specific questions about the snapshot (status, size, creation time etc.)
    """
    ebs_cli = init_ebs_service(config,region_id)

    try:
        describe_request = volcenginesdkstorageebs.DescribeSnapshotsRequest(
            snapshot_ids=[snapshot_id]
        )

        describe_response = ebs_cli.describe_snapshots(describe_request)

        snapshot = describe_response.snapshots[0]
        if not snapshot:
            return {"error": f"No snapshot found with ID: {snapshot_id}"}
                    
        # If query is provided, add additional processing logic here
        if query:
            # You can add NLP processing to answer specific questions
            pass
            
        return {
            "snapshot_id": snapshot_id,
            "data": describe_response.to_str()
        }

    except Exception as e:
        logger.error(
            "Error in describe_snapshot",
            extra={
                "error": str(e),
                "snapshot_id": snapshot_id,
                "region_id": region_id
            }
        )
        return {
            "error": "Failed to describe snapshot",
            "details": str(e),
            "code": "EBS_DESCRIBE_SNAPSHOT_ERROR"
        }

@mcp.tool()
def create_volume(
    volume_name: str,
    zone_id: str,
    size: Optional[int] = None,
    volume_type: Optional[str]  = None,
    region_id: Optional[str] = None,
    snapshot_id: Optional[str] = None,
    volume_charge_type: Optional[str] = None,
    instance_id: Optional[str] = None,
    query: Optional[str] = None
) -> Dict:
    """Create a new EBS volume.
    This tool creates a new EBS volume with the specified size and instance ID.
    Args:
        volume_name: The name of the EBS volume to create (e.g. "my-volume")
        zone_id: The ID of the zone where the volume will be created (e.g. "cn-beijing-a")
        size: The size of the EBS volume in GiB (e.g. 40)
        volume_type: The type of the EBS volume (e.g. "ESSD_PL0")
        region_id: The ID of the region where the volume will be created (e.g. "cn-beijing")
        query: Optional specific questions about the volume (status, size, creation time etc.)
    """
    ebs_cli = init_ebs_service(config,region_id)

    if size is None:
        size = 40

    if volume_type is None:
        volume_type = "ESSD_PL0"
    if volume_charge_type is None:
        volume_charge_type = "PostPaid"
    kind = "data"

    try:
        create_request = volcenginesdkstorageebs.CreateVolumeRequest(
            kind = kind,
            zone_id=zone_id,
            volume_name=volume_name,
            size=size,
            volume_type=volume_type,
            snapshot_id=snapshot_id,
            volume_charge_type=volume_charge_type,
            instance_id=instance_id,
            description="mcp-create"
            )

        create_response = ebs_cli.create_volume(create_request)
        
        # If query is provided, add additional processing logic here
        if query:
            # You can add NLP processing to answer specific questions
            pass

        return {
            "volume_id": create_response.volume_id,
            "data": create_response.to_str()
        }
    except Exception as e:
        logger.error(
            "Error in create_volume",
            extra={
                "error": str(e),
                "volume_name": volume_name,
                "zone_id": zone_id,
                "region_id": region_id
            }
        )
        return {
            "error": "Failed to create volume",
            "details": str(e),
            "code": "EBS_CREATE_VOLUME_ERROR"
        }


@mcp.tool()
def create_snapshot(
    volume_id: str,
    snapshot_name: Optional[str] = None,
    region_id: Optional[str] = None,
    query: Optional[str] = None
) -> Dict:
    """Create a new EBS snapshot.
    This tool creates a new EBS snapshot from the specified volume.
    Args:
        volume_id: The ID of the EBS volume to create a snapshot from (e.g. "vol-12345678")
        snapshot_name: The name of the EBS snapshot to create (e.g. "my-snapshot")
        region_id: The ID of the region where the snapshot will be created (e.g. "cn-beijing")
        query: Optional specific questions about the snapshot (status, size, creation time etc.)
    """
    ebs_cli = init_ebs_service(config,region_id)

    if snapshot_name is None:
        snapshot_name = "snapshot-mcp-"+volume_id + "_" + time.strftime("%Y%m%d_%H%M", time.localtime())
    
    try:
        create_request = volcenginesdkstorageebs.CreateSnapshotRequest(
            volume_id=volume_id,
            snapshot_name=snapshot_name,
            description="mcp-create"
        )
        create_response = ebs_cli.create_snapshot(create_request)

        describe_snapshot_request = volcenginesdkstorageebs.DescribeSnapshotsRequest(
            snapshot_ids=[create_response.snapshot_id]
        )
        describe_snapshot_response = ebs_cli.describe_snapshots(describe_snapshot_request)
        # If query is provided, add additional processing logic here
        if query:
            # You can add NLP processing to answer specific questions
            pass
        return {
            "snapshot_id": create_response.snapshot_id,
            "data": create_response.to_str(),
            "snapshot_info":describe_snapshot_response.snapshots[0]
        }
    except Exception as e:
        logger.error(
            "Error in create_snapshot",
            extra={
                "error": str(e),
                "volume_id": volume_id,
                "region_id": region_id
            }
        )
        return {
            "error": "Failed to create snapshot",
            "details": str(e),
            "code": "EBS_CREATE_SNAPSHOT_ERROR"
        }


@mcp.tool()
def extend_volume(
    volume_id: str,
    new_size: int,
    region_id: Optional[str] = None,
    query: Optional[str] = None
) -> Dict:
    """Extend the size of an EBS volume.
    This tool extends the size of an existing EBS volume to the specified size.
    Args:
        volume_id: The ID of the EBS volume to extend (e.g. "vol-12345678")
        new_size: The new size of the EBS volume in GiB (e.g. 80)
        region_id: The ID of the region where the volume is located (e.g. "cn-beijing")
        query: Optional specific questions about the volume (status, size, creation time etc.)
    """
    ebs_cli = init_ebs_service(config,region_id)
    try:
        extend_request = volcenginesdkstorageebs.ExtendVolumeRequest(
            volume_id=volume_id,
            new_size=new_size
        )
        extend_response = ebs_cli.extend_volume(extend_request)
        # If query is provided, add additional processing logic here

        describe_volume_request = volcenginesdkstorageebs.DescribeVolumesRequest(
            volume_ids=[volume_id]
        )           
        describe_volume_response = ebs_cli.describe_volumes(describe_volume_request)
            
        if query:
            # You can add NLP processing to answer specific questions
            pass
        return {
            "data": describe_volume_response.to_str()
        }
    except Exception as e:
        logger.error(
            "Error in extend_volume",
            extra={
                "error": str(e),
                "volume_id": volume_id,
                "new_size": new_size,
                "region_id": region_id
            }
        )
        return {
            "error": "Failed to extend volume",
            "details": str(e),
            "code": "EBS_EXTEND_VOLUME_ERROR"
        }


def main():
    """Main entry point for the Storage EBS MCP Server."""
    parser = argparse.ArgumentParser(description="Run the Storage EBS MCP Server")
    parser.add_argument("--transport", "-t", choices=["sse", "stdio", "streamable-http"], default="stdio")
    parser.add_argument("--config", "-c", help="Path to config file")
    
    args = parser.parse_args()
    global config # Keep 'global config' as it's assigned and used by other functions
    try:
        # Simplified config loading
        config_path = args.config if args.config else None
        config = load_config(config_path)
        
        # Removed unused global ebs_cli initialization
        logger.info(
            f"Initialized Storage EBS Base service with config from: {config_path if config_path else 'default locations'}"
        )

        # Run the MCP server
        logger.info(
            f"Starting Storage EBS MCP Server with {args.transport} transport"
        )
        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting Storage EBS MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
