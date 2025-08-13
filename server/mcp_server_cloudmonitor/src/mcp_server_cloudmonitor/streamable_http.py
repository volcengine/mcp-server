from mcp_server_cloudmonitor.server import mcp

def main():
    mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()