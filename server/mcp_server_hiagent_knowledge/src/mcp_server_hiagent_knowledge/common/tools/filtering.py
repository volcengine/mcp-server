"""Reuse the stable tool filtering implementation."""
import sys
from importlib import import_module
sys.modules[__name__] = import_module("mcp_server_hiagent_knowledge.versions.v3_1_0.tools.filtering")
