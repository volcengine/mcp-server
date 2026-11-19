"""Reuse unchanged retrieval tools for every application version."""
import sys
from importlib import import_module
sys.modules[__name__] = import_module("mcp_server_hiagent_knowledge.versions.v3_1_0.tools.knowledge")
