#!/usr/bin/env python3
import logging
from mcp_server_vedb_mysql.config import mcp, args

import mcp_server_vedb_mysql.tools_args 
import mcp_server_vedb_mysql.tools_net
import mcp_server_vedb_mysql.tools_instances
import mcp_server_vedb_mysql.tools_db_accts
import mcp_server_vedb_mysql.tools_dbrs
import mcp_server_vedb_mysql.tools_info
# import mcp_server_vedb_mysql.tools_tasks


def main():
    logger = logging.getLogger(__name__)
    # Run the MCP server
    logger.info(f"Starting VeDB MySQL MCP Server with {args.transport} transport")
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
