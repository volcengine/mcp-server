#!/usr/bin/env python3
"""
Test script to verify MCP server functionality and tool registration.
"""

import os
import sys
import time
import requests
from importlib import import_module, reload

# Internal import from project
from src.mcp_server_vefaas_function.config_utils import set_mcp_config_env


def test_tool_registration():
    """Test that all tools are properly registered."""
    print("🔍 Testing tool registration...")

    # Test 1: Default configuration (original behavior)
    print("  Testing default configuration...")
    try:
        from src.mcp_server_vefaas_function.vefaas_server import mcp

        # Check if tools are registered
        if hasattr(mcp, '_tool_manager') and hasattr(mcp._tool_manager, '_tools'):
            tool_count = len(mcp._tool_manager._tools)
            print(f"    ✅ Tools registered in default configuration - {tool_count} tools found")
        else:
            print("    ❌ No tools found in default configuration")
            return False
    except Exception as e:
        print(f"    ❌ Error importing default configuration: {e}")
        return False

    # Test 2: Environment variable configuration
    print("  Testing environment variable configuration...")
    try:
        # Configure streamable mode; it automatically sets JSON_RESPONSE / STATELESS_HTTP
        set_mcp_config_env("streamable")

        # Force-reload vefaas_server so it picks up the new environment variables
        module_name = "src.mcp_server_vefaas_function.vefaas_server"
        if module_name in sys.modules:
            reload(sys.modules[module_name])  # type: ignore[arg-type]
        else:
            import_module(module_name)

        from src.mcp_server_vefaas_function.vefaas_server import mcp as mcp_streamable

        if hasattr(mcp_streamable, '_tool_manager') and hasattr(mcp_streamable._tool_manager, '_tools'):
            tool_count = len(mcp_streamable._tool_manager._tools)
            print(f"    ✅ Tools registered in streamable configuration - {tool_count} tools found")
        else:
            print("    ❌ No tools found in streamable configuration")
            return False

    except Exception as e:
        print(f"    ❌ Error testing streamable configuration: {e}")
        return False
    finally:
        # Clean up environment variables to avoid side effects on other tests
        for key in list(os.environ.keys()):
            if key.startswith("FASTMCP_"):
                os.environ.pop(key, None)

    print("✅ Tool registration tests passed")
    return True


def test_streamable_http_server():
    """Test the streamable HTTP server."""
    print("🌐 Testing streamable HTTP server...")

    try:
        # Start server in background
        import multiprocessing
        import threading

        def start_server():
            """在单独线程中启动服务器，使用新版 main.py 的命令行 flag 方式。"""

            import sys  # 局部导入，避免污染全局

            # 通过修改 sys.argv 来模拟命令行启动参数
            sys.argv = [
                "mcp-server",
                "--transport", "streamable-http",
                # 不传递 --host/--port，使用 main.py 默认的 127.0.0.1:8000
            ]

            # 延迟导入，确保 sys.argv 已就绪
            from src.mcp_server_vefaas_function.main import main as server_main  # pylint: disable=import-error,import-outside-toplevel

            server_main()

        # Start server in separate thread
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()

        # Wait for server to start
        time.sleep(3)

        # Test server endpoints
        base_url = "http://127.0.0.1:8000"

        # Test initialization
        init_response = requests.post(f"{base_url}/mcp/",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "test-client", "version": "1.0.0"}
                }
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            timeout=10)

        if init_response.status_code == 200:
            print("    ✅ Server initialization successful")
        else:
            print(f"    ❌ Server initialization failed: {init_response.status_code}")
            return False

        # Test tool listing
        tools_response = requests.post(f"{base_url}/mcp/",
            json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            timeout=10)

        if tools_response.status_code == 200:
            tools_data = tools_response.json()
            if 'result' in tools_data and 'tools' in tools_data['result']:
                tool_count = len(tools_data['result']['tools'])
                print(f"    ✅ Tools listing successful - {tool_count} tools found")

                # Print some tool names for verification
                if tool_count > 0:
                    tool_names = [tool['name'] for tool in tools_data['result']['tools'][:5]]
                    print(f"    📋 Sample tools: {', '.join(tool_names)}")

                if tool_count > 0:
                    return True
                else:
                    print("    ❌ No tools found in tools/list response")
                    return False
            else:
                print("    ❌ Invalid tools/list response format")
                return False
        else:
            print(f"    ❌ Tools listing failed: {tools_response.status_code}")
            return False

    except Exception as e:
        print(f"    ❌ Error testing streamable HTTP server: {e}")
        return False


def test_function_configurations():
    """Test different function configurations."""
    print("⚙️  Testing function configurations...")

    try:
        # Use config_utils to set env vars for testing
        set_mcp_config_env("streamable", host="127.0.0.1", port=9000, debug=True)

        # Test different modes
        for mode in ["streamable", "sse", "stdio"]:
            # Provide dummy custom parameters for each mode to verify they are written
            if mode == "streamable":
                extras = {"extra": "foo"}
            elif mode == "sse":
                extras = {"host": "127.0.0.1", "port": 18081}
            else:
                extras = {"debug": True}

            set_mcp_config_env(mode, **extras)
            if os.environ.get("FASTMCP_STATELESS_HTTP") == "true":
                print(f"    ✅ Mode '{mode}' configuration working")
            else:
                print(f"    ❌ Mode '{mode}' configuration failed")
                return False

        print("✅ Function configuration tests passed")
        return True

    except Exception as e:
        print(f"    ❌ Error testing function configurations: {e}")
        return False
    finally:
        # Clean up environment variables to avoid side effects on subsequent tests
        for key in list(os.environ.keys()):
            if key.startswith("FASTMCP_"):
                os.environ.pop(key, None)


def test_tool_functionality():
    """Test that specific tools work correctly."""
    print("🔧 Testing tool functionality...")

    try:
        from src.mcp_server_vefaas_function.vefaas_server import supported_runtimes, validate_and_set_region

        # Test supported_runtimes function
        runtimes = supported_runtimes()
        if isinstance(runtimes, list) and len(runtimes) > 0:
            print(f"    ✅ supported_runtimes working - {len(runtimes)} runtimes found")
        else:
            print("    ❌ supported_runtimes not working properly")
            return False

        # Test validate_and_set_region function
        region = validate_and_set_region("cn-beijing")
        if region == "cn-beijing":
            print("    ✅ validate_and_set_region working")
        else:
            print("    ❌ validate_and_set_region not working properly")
            return False

        # Test with None region (should return default)
        default_region = validate_and_set_region(None)
        if default_region == "cn-beijing":
            print("    ✅ validate_and_set_region default working")
        else:
            print("    ❌ validate_and_set_region default not working properly")
            return False

        print("✅ Tool functionality tests passed")
        return True

    except Exception as e:
        print(f"    ❌ Error testing tool functionality: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 Starting MCP functionality tests...\n")

    tests = [
        test_tool_registration,
        test_function_configurations,
        test_tool_functionality,
        test_streamable_http_server,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print()
        except Exception as e:
            print(f"❌ Test failed with exception: {e}\n")
            results.append(False)

    # Summary
    passed = sum(results)
    total = len(results)

    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! MCP functionality is working correctly.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please check the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
