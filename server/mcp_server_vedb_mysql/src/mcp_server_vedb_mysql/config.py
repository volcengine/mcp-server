import os
import logging
import json
import argparse
from mcp_server_vedb_mysql.api import VEDBMSDK
from mcp.server.fastmcp import FastMCP


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="/tmp/mcp.vedbmysql.log"
)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP("VeDB MySQL MCP Server", port=int(os.getenv("MCP_SERVER_PORT", "8000")),
              host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
              streamable_http_path=os.getenv("STREAMABLE_HTTP_PATH", "/mcp"))

# Initialize OpenAPI client
openapi_cli = None
args = None
try:
    parser = argparse.ArgumentParser(description="Run the VeDB MySQL MCP Server")
    parser.add_argument("--config", "-c", help="Path to config file")
    parser.add_argument("--transport", "-t", choices=["sse", "stdio", "streamable-http"], default="stdio")
    args = parser.parse_args()

    # 优先从config文件加载
    if args.config:
        try:
            with open(args.config) as f:
                config_data = json.load(f)
                env_vars = config_data.get('env', {})
                openapi_cli = VEDBMSDK(
                    region=env_vars.get("VOLCENGINE_REGION", os.getenv("VOLCENGINE_REGION", "cn-beijing")),
                    ak=env_vars.get("VOLCENGINE_ACCESS_KEY", os.environ["VOLCENGINE_ACCESS_KEY"]),
                    sk=env_vars.get("VOLCENGINE_SECRET_KEY", os.environ["VOLCENGINE_SECRET_KEY"]))
        except Exception as e:
            logger.warning(f"Failed to load config file, fallback to env vars: {str(e)}")
    else:
        # 从环境变量加载
        required_vars = ["VOLCENGINE_ACCESS_KEY", "VOLCENGINE_SECRET_KEY", "VOLCENGINE_REGION"]
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

        openapi_cli = VEDBMSDK(
            region=os.getenv("VOLCENGINE_REGION", "cn-beijing"),
            ak=os.environ["VOLCENGINE_ACCESS_KEY"],
            sk=os.environ["VOLCENGINE_SECRET_KEY"])
except Exception as e:
    logger.error(f"Error starting VeDB MySQL MCP Server: {str(e)}")
    raise

logger.info(f"Initialized VeDB MySQL Base service")
