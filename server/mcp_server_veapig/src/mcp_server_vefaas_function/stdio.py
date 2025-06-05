from .vefaas_server import mcp
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    logger.info("veFaaS MCP Server started")
    
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
