from .server import run_server


def main() -> None:
    run_server(transport="streamable-http")


if __name__ == "__main__":
    main()
