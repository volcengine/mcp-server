"""Local desktop acceptance launcher; never shipped in the SMS wheel.

Run this script with the Python environment of the exact wheel under test.
The official master Skill resolves the account's existing login in-process.
Desktop configuration contains paths only, never cloud credentials. State is
temporary and removed when the server exits, so this launcher is for acceptance
sessions, not a persistent deployment.
"""

import argparse
import contextlib
import importlib
import io
import os
import pathlib
import sys
import tempfile

from cryptography.fernet import Fernet

from mcp_server_sms.server import main as server_main


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(pathlib.Path(args.skill_dir) / "scripts"))
    try:
        # A stdio host reserves stdout for MCP messages. Do not expose auth
        # diagnostics or credentials through either stream during resolution.
        with (
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            skill_api = importlib.import_module("api_client")
            credentials = skill_api.SmsApiClient()._credential_resolver.resolve()
    except Exception as error:
        print(
            "SMS desktop acceptance authentication failed: " + type(error).__name__,
            file=sys.stderr,
        )
        return 1

    with tempfile.TemporaryDirectory(prefix="sms-mcp-desktop-") as directory:
        os.environ.update(
            {
                "SMS_MCP_DATABASE_URL": "sqlite:///"
                + str(pathlib.Path(directory) / "state.db"),
                "SMS_MCP_ENCRYPTION_KEY": Fernet.generate_key().decode(),
                "SMS_MCP_LOCAL_SUBJECT": "desktop-acceptance",
                "VOLCENGINE_ACCESS_KEY": credentials.access_key,
                "VOLCENGINE_SECRET_KEY": credentials.secret_key,
                "VOLCENGINE_SESSION_TOKEN": credentials.session_token,
            }
        )
        sys.argv = ["mcp-server-sms", "--transport", "stdio"]
        server_main()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
