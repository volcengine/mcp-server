"""
Region and available zone related tool functions
"""

from typing import List

import volcenginesdkecs
from mcp import types
from pydantic import Field
from volcenginesdkecs.models import *

from mcp_server_ecs.common.client import get_volc_ecs_client
from mcp_server_ecs.common.errors import handle_error
from mcp_server_ecs.tools import mcp


@mcp.tool(
    name="describe_regions",
    description="查询地域列表 (Query region list)\n\n查询火山引擎ECS支持的地域信息。\n地域是指物理的数据中心所在位置，如 cn-beijing、cn-shanghai、ap-southeast-1 等。",
)
async def describe_regions(
    region: str = Field(
        default="cn-beijing",
        description="默认为cn-beijing. 可为：ap-southeast-1, cn-beijing2, cn-shanghai, cn-guangzhou 等",
    ),
    regionIds: List[str] = Field(
        default=[],
        description="地域ID，最多支持20个ID",
    ),
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client(region)
        total_results = []
        next_token = None

        while True:
            response = volc_client.describe_regions(
                volcenginesdkecs.DescribeRegionsRequest(
                    region_ids=regionIds,
                    next_token=next_token,
                )
            )

            if not response:
                handle_error("describe_regions")

            regions = getattr(response, "regions", None) or []
            for region in regions:
                total_results.append(region.region_id)

            if not response.next_token:
                break

            next_token = response.next_token

        return [types.TextContent(type="text", text=f"Results: {total_results}")]

    except Exception as e:
        handle_error("describe_regions", e)


@mcp.tool(
    name="describe_zones",
    description="查询可用区列表 (Query available zone list)\n\n查询指定地域下的可用区信息。\n可用区是地域内的独立电力和网络域，如 cn-beijing-a、cn-beijing-b 等。",
)
async def describe_zones(
    region: str = Field(
        default="cn-beijing",
        description="默认为cn-beijing. 可为：ap-southeast-1, cn-beijing2, cn-shanghai, cn-guangzhou 等",
    ),
    zoneIds: List[str] = Field(
        default=[],
        description="可用区ID，最多支持20个",
    ),
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client(region)
        total_results = []

        response = volc_client.describe_zones(
            volcenginesdkecs.DescribeZonesRequest(
                zone_ids=zoneIds,
            )
        )

        if not response:
            handle_error("describe_zones")

        zones = getattr(response, "zones", None) or []
        for zone in zones:
            total_results.append(zone.zone_id)

        return [types.TextContent(type="text", text=f"Results: {total_results}")]

    except Exception as e:
        handle_error("describe_zones", e)
