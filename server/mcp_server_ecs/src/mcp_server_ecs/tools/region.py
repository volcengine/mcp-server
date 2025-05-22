"""
Region and available zone related tool functions
"""
from typing import List, Optional

import volcenginesdkecs
from pydantic import BaseModel, Field
from mcp import types
from volcenginesdkecs.models import *

from mcp_server_ecs.common.client import get_volc_ecs_client
from mcp_server_ecs.common.errors import handle_error
from mcp_server_ecs.tools import register_tool


class DescribeRegionsParams(BaseModel):
    Region: str = Field(
        default="cn-beijing",
        description="默认为cn-beijing. 可为：ap-southeast-1, cn-beijing2, cn-shanghai, cn-guangzhou 等",
    )

    RegionIds: List[str] = Field(
        default=[],
        description="地域ID，最多支持20个ID",
    )


class DescribeZonesParams(BaseModel):
    Region: str = Field(
        default="cn-beijing",
        description="默认为cn-beijing. 可为：ap-southeast-1, cn-beijing2, cn-shanghai, cn-guangzhou 等",
    )

    ZoneIds: List[str] = Field(
        default=[],
        description="可用区ID，最多支持20个",
    )


@register_tool(name="describe_regions",
               description="Query region list",
               model_class=DescribeRegionsParams)
async def describe_regions(args: dict) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client(args.get("Region"))
        total_results = []
        next_token = None

        while True:
            response = volc_client.describe_regions(
                volcenginesdkecs.DescribeRegionsRequest(
                    region_ids=args.get("RegionIds"),
                    next_token=next_token,
                )
            )

            if not response or not getattr(response, "regions", None):
                return handle_error("describe_regions")

            for region in response.regions:
                total_results.append(region.region_id)

            if not response.next_token:
                break

            next_token = response.next_token

        return [types.TextContent(
            type="text",
            text=f"Results: {total_results}"
        )]

    except Exception as e:
        return handle_error("describe_regions", e)


@register_tool(name="describe_zones",
               description="Query available zone list",
               model_class=DescribeZonesParams)
async def describe_zones(args: dict) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client(args.get("Region"))
        total_results = []

        response = volc_client.describe_zones(
            volcenginesdkecs.DescribeZonesRequest(
                zone_ids=args.get("ZoneIds"),
            )
        )

        if not response or not getattr(response, "zones", None):
            return handle_error("describe_zones")

        for zone in response.zones:
            total_results.append(zone.zone_id)

        return [types.TextContent(
            type="text",
            text=f"Results: {total_results}"
        )]

    except Exception as e:
        return handle_error("describe_zones", e)
