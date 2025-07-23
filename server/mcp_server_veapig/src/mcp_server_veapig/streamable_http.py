from .veapig_server import mcp


def main():
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
