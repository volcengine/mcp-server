from __future__ import annotations
from typing import Any
import pytest
from mcp_server_hiagent_knowledge import main as main_module

class _StubMCP:
    def run(self, *args, **kwargs):
        return None

@pytest.fixture
def captured(monkeypatch):
    calls = {}
    def fake_create(**kwargs):
        calls.update(kwargs)
        return _StubMCP()
    for key in ["HIAGENT_TOOLS", "HIAGENT_DISABLED_TOOLS", "HIAGENT_VERSION"]:
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setattr("mcp_server_hiagent_knowledge.versions.v3_3_0.create_mcp_server", fake_create)
    return calls

def _run(monkeypatch, argv):
    monkeypatch.setattr("sys.argv", ["hiagent", *argv])
    main_module.main()

def test_no_filter_flags_pass_none(monkeypatch, captured):
    _run(monkeypatch, [])
    assert captured["enabled_tools"] is None
    assert captured["disabled_tools"] is None

def test_tools_short_flag_maps_to_allowlist(monkeypatch, captured):
    _run(monkeypatch, ["-t", "search_wiki,read_wiki_page"])
    assert captured["enabled_tools"] == ["search_wiki", "read_wiki_page"]
    assert captured["disabled_tools"] is None

def test_disabled_tools_flag_maps_to_denylist(monkeypatch, captured):
    _run(monkeypatch, ["--disabled-tools", "grep_knowledge_chunks"])
    assert captured["disabled_tools"] == ["grep_knowledge_chunks"]

def test_env_vars_used_when_flags_absent(monkeypatch, captured):
    monkeypatch.setenv("HIAGENT_TOOLS", "search_wiki")
    monkeypatch.setenv("HIAGENT_DISABLED_TOOLS", "read_wiki_page")
    _run(monkeypatch, [])
    assert captured["enabled_tools"] == ["search_wiki"]
    assert captured["disabled_tools"] == ["read_wiki_page"]

def test_empty_env_var_means_all_tools(monkeypatch, captured):
    monkeypatch.setenv("HIAGENT_TOOLS", "")
    monkeypatch.setenv("HIAGENT_DISABLED_TOOLS", "  ")
    _run(monkeypatch, [])
    assert captured["enabled_tools"] is None
    assert captured["disabled_tools"] is None

def test_cli_flag_overrides_env(monkeypatch, captured):
    monkeypatch.setenv("HIAGENT_TOOLS", "search_wiki")
    _run(monkeypatch, ["--tools", "search_knowledge"])
    assert captured["enabled_tools"] == ["search_knowledge"]

def test_transport_no_longer_accepts_short_t(monkeypatch, captured):
    _run(monkeypatch, ["-t", "stdio"])
    assert captured["enabled_tools"] == ["stdio"]

def test_unknown_tool_name_exits(monkeypatch, captured):
    def raising_create(**kwargs):
        raise ValueError("unknown tool name(s): nope")
    monkeypatch.setattr("mcp_server_hiagent_knowledge.versions.v3_3_0.create_mcp_server", raising_create)
    with pytest.raises(SystemExit):
        _run(monkeypatch, ["--tools", "nope"])

@pytest.mark.parametrize("source", ["cli", "env"])
def test_invalid_version_has_concise_cli_error(monkeypatch, captured, capsys, source):
    argv = []
    if source == "cli":
        argv = ["--hiagent-version", "v9.9.9"]
    else:
        monkeypatch.setenv("HIAGENT_VERSION", "v9.9.9")
    with pytest.raises(SystemExit) as exc:
        _run(monkeypatch, argv)
    assert exc.value.code == 2
    error = capsys.readouterr().err
    assert "unsupported HIAGENT_VERSION 'v9.9.9'" in error
    assert "supported versions: v3.1.0, v3.2.1, v3.3.0" in error
    assert "Traceback" not in error
    assert not captured

@pytest.mark.parametrize("value", ["", "   "])
def test_blank_cli_version_uses_default(monkeypatch, captured, value):
    _run(monkeypatch, ["--hiagent-version", value])
    assert "enabled_tools" in captured
