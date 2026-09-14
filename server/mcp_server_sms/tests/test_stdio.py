import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_standard_stdio_client_without_business_state(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    parameters = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_server_sms.server"],
        env={
            "VOLCENGINE_ACCESS_KEY": "",
            "VOLCENGINE_SECRET_KEY": "",
            "VOLCENGINE_SESSION_TOKEN": "",
        },
    )
    async with stdio_client(parameters) as (read, write):
        async with ClientSession(read, write, read_timeout_seconds=30) as session:
            await session.discover()
            assert session.protocol_version == "2026-07-28"
            tools = await session.list_tools()
            assert len(tools.tools) == 26
            result = await session.call_tool("list_message_groups", {})
            assert result.is_error
            message = " ".join(item.text for item in result.content if item.type == "text")
            assert "AccessKeyId" in message
            assert "Context is not available" not in message
    assert list(tmp_path.iterdir()) == []
