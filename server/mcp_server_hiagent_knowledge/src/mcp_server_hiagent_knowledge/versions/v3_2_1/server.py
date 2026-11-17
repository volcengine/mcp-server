"""v3.2.1 server: shared assembly with version-specific discovery."""
from mcp_server_hiagent_knowledge.common.server import create_mcp_server as _create
from .tools import dataset
def create_mcp_server(client=None, *, enabled_tools=None, disabled_tools=None):
    return _create(client, dataset_module=dataset, hiagent_version="v3.2.1", enabled_tools=enabled_tools, disabled_tools=disabled_tools)
