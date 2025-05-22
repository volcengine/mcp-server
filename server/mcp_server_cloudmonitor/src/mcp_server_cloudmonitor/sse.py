from mcp_server_cloudmonitor.server import mcp

def main():
    import asyncio

    asyncio.run(mcp.run(transport="sse"))

if __name__ == "__main__":
    main()

    # import asyncio

    # asyncio.run(run())