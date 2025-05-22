from .server import serve


def main():
    """Volcengine MCP Server"""
    import asyncio
    asyncio.run(serve())


if __name__ == "__main__":
    main()
