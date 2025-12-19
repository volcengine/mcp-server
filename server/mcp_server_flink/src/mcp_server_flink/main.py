import argparse
import logging
import os

from mcp_server_flink.server import mcp

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

LOCAL_DEPLOY_MODE = "local"
REMOTE_CLOUD_DEPLOY_MODE = "remote-cloud"
REMOTE_GATEWAY_DEPLOY_MODE = "remote-gateway"


def main():
    parser = argparse.ArgumentParser(description="Run the Serverless Flink MCP Server")
    parser.add_argument(
        "--transport", "-t",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use (stdio or streamable-http)"
    )

    args = parser.parse_args()

    try:
        deploy_mode = os.getenv("DEPLOY_MODE", LOCAL_DEPLOY_MODE)
        if deploy_mode == LOCAL_DEPLOY_MODE or deploy_mode == REMOTE_CLOUD_DEPLOY_MODE:
            validate_required_vars()
        else:
            validate_remote_required_vars()

        # Run the MCP server
        logger.info(f"Starting Serverless Flink MCP Server with {args.transport} transport")

        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting Serverless Flink MCP Server: {str(e)}")
        raise


def validate_required_vars():
    """
    Validate that all required environment variables are set.

    Raises:
    ValueError: If any required environment variable is missing.
    """
    missing_vars = []
    for var in ["VOLCENGINE_ACCESS_KEY", "VOLCENGINE_SECRET_KEY", "VOLCENGINE_REGION"]:
        if var not in os.environ:
            missing_vars.append(var)

    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")


def validate_remote_required_vars():
    """
    Validate that all required environment variables are set.

    Raises:
    ValueError: If any required environment variable is missing.
    """
    missing_vars = []
    for var in []:
        if var not in os.environ:
            missing_vars.append(var)

    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")


if __name__ == "__main__":
    main()
