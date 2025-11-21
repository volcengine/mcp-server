#!/usr/bin/env python3
"""
MCP HTTP客户端使用示例
连接本地MCP服务器进行测试
"""

import asyncio
import traceback

from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def mcp_http_client():
    """测试HTTP客户端连接"""
    print("🚀 启动MCP HTTP客户端测试...")

    try:
        # 使用streamablehttp_client连接本地服务器
        # 注意：URL路径需要包含 /mcp 后缀
        # 修复：streamablehttp_client返回3个值，不是2个
        async with streamablehttp_client("http://localhost:8000/mcp") as (read, write, get_session_id):
            async with ClientSession(read, write) as session:
                print("✅ 客户端连接建立成功")

                # 1. 初始化会话
                init_result = await session.initialize()
                print(f"📋 初始化结果: {init_result}")

                # 2. 列出所有可用工具
                tools_result = await session.list_tools()
                print("🛠️ 可用工具列表:")
                for tool in tools_result.tools:
                    print(f"  - {tool.name}: {tool.description}")

                # 3. 调用list_jobs工具
                print("🔧 测试list_serverless_jobs工具...")
                jobs_result = await session.call_tool("list_serverless_jobs", {"limit": 3})
                jobs_data = jobs_result.content
                print(f"  查询到 {len(jobs_data)} 个作业")

                print("\n✅ HTTP客户端测试完成！")
    except Exception as e:
        print(f"❌ 客户端测试失败: {str(e)}")
        print("📋 详细错误堆栈:")
        traceback.print_exc()
        print("💡 请确保MCP服务器正在运行: python main.py --transport streamable-http")


async def main():
    """主函数"""
    await mcp_http_client()


if __name__ == "__main__":
    asyncio.run(main())
