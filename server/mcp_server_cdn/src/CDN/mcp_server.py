from src.CDN.api.api import CdnAPI
from mcp.server.fastmcp import FastMCP
from .note import note
from src.utils.response import HandlerVolcResponse
import json


def create_mcp_server():
    service = CdnAPI()
    mcp = FastMCP(
        "CDN MCP",
        instructions="Volcengine(火山引擎) 内容分发网络(CDN)MCP 服务",
    )

    @mcp.tool()
    def guide():
        """
        ## MCP Invocation Method Guide
        - For task decomposition, it is necessary to use the mcp tool.
        - The first step requires invoking the `get_note` function to obtain the parameter description.
        - Subsequently, the corresponding method should be called to retrieve the data.
        """
        return """use  `guide` description to get how to use Mcp Server"""

    @mcp.tool()
    def get_note(func_name: str) -> str:
        """
        获取参数描述

        Args:
            func_name: 函数名

        """
        original_note = note.get(func_name)
        return f"""
           
        定位
        1. 你是专业的火山引擎 CDN 专家，你理解火山 CDN 产品能力和业务场景，精通于为用户提供专业的技术支持服务。
        2. 为了提供最好的服务，你需要精准识别用户问题并进行拆解，调用工具（OpenAPI）获取匹配用户问题的内容，基于获取到的内容，你需要进行整合并分析，再返回给用户。
        3. 对于意图不清晰的问题，你需要和用户确认清楚再开始处理任务。
        4. 根据用户提问的语言，采用对应的语言回答，如用户使用中文提问，则用中文回答。
        技能一：理解和分析问题
        1. 需要精准理解用户问题，对于意图不清晰的问题，需要和用户进行二次确认，或者让用户描述得更清楚。
        2. 在理解用户问题后，需要对问题进行拆解，明确解决该问题所需要的步骤、指令、工具，并将相关信息打印出来。
        技能二：CDN MCP 工具调用
        1. 完成问题拆解后，调用合适的 MCP 工具执行相关操作，如查询实时监控、业务分析数据等，查询域名加速区域信息。
        2. 能够调用多个工具进行操作。
        技能三：数据分析能力
        1. 查询时间：能够精准理解用户问题中的时间概念，如“今天”、“近一周”、“本周”，需要基于当前时间，将这些时间概念转换为具体的时间范围。
        2. 问题分析：如果用户想进行数据洞察，需要能够分析所有数据指标，如带宽、流量、请求数、状态码等，并能够进行环比、同比分析等；简而言之，需要能够发散思考，聚合分析并给出合理的结果。
        3. 异常排查：如果用户反馈业务存在异常情况，但不知道具体的异常原因，需要能够分析所有指标，查看哪些指标存在突发/异常，比如 4xx 状态码飙升,TOP IP 流量占比较高等。
        技能四：域名配置分析
        1. 如果用户查询 CDN 整体的域名配置情况，调用 ListCdnDomains 查询即可，该接口同样能查询到域名的具体配置信息，需要注意请求的分页大小，如果域名较多，则需要多次请求，获取全部域名信息后再整体分析；不需要调用 DescribeCdnConfig。
        2. 如果用户查询指定域名的配置情况，调用 DescribeCdnConfig 查询即可，该接口查询指定域名的具体配置信息；不需要调用 ListCdnDomains。

           {original_note}
        """

    @mcp.tool()
    def describe_cdn_config(body: dict) -> str:
        """
        获取一个加速域名的配置详情。如果该加速域名已删除，您无法获取其配置详情。
        Call steps:
        1. Pass "describe_cdn_config" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_cdn_config
        """
        reqs = service.mcp_post("McpDescribeCdnConfig", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def list_cdn_domains(body: dict) -> str:
        """
        获取 CDN 中的加速域名列表并展示每个域名的基础信息。基础信息包含业务类型、状态、CNAME、加速区域等。要获取一个域名的 CDN 特性配置，请调用 DescribeCdnConfig。
        该 API 提供了一系列的过滤类型。您可以根据需要指定一种或多种过滤类型，以获取符合过滤条件的域名列表。
        Call steps:
        1. Pass "list_cdn_domains" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_cdn_domains
        """
        reqs = service.mcp_post("McpListCdnDomains", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_origin_top_statistical_data(body: dict) -> str:
        """
        在新版数据统计接口中，该 API 没有更新，可继续使用。
        API 说明
        基于火山引擎内容分发网络（CDN）的向源站发送的回源请求，该 API 对一个域名统计热门的回源 URL。
        要调用该 API，您需要指定一个指标和一个统计时间段。您最多能查询过去 92 天的数据。
        数据稳定性：受网络波动影响，边缘节点上统计的指标数据可能会发生变化。大多数情况下，指标数据会在 12 小时内逐步稳定下来。
        数据时效性：热门的回源 URL 是基于按小时粒度统计的指标数据。因此，数据统计可能会有 2 小时左右的延时。例如，对于 09:00 至 10:00 这个时间段的热门的回源 URL，您可以在 11:00 左右获取到准确的结果。
        Call steps:
        1. Pass "describe_origin_top_statistical_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_origin_top_statistical_data
        """
        reqs = service.mcp_post(
            "McpDescribeOriginTopStatisticalData", {}, json.dumps(body)
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_district_data(body: dict) -> str:
        """
        API 说明
        基于火山引擎内容分发网络（CDN）收到的用户请求，该 API 对一个指标统计各时间点的指标细分数据。
        要调用该 API，您需要指定一个指标，一个统计时间段和一个时间粒度。您还可以指定多个过滤条件对用户请求进行过滤。您最多能查询过去 92 天的数据。
        数据稳定性：受网络波动影响，边缘节点上统计的指标数据可能会发生变化。大多数情况下，指标数据会在 12 小时内逐步稳定下来。因此，该 API 返回的指标数据并非账单中显示的用量，仅供参考。实际用量请以账单为准。
        数据时效性：指标数据可能会有 5 分钟左右的延时。
        如果您刚开始使用 CDN 的统计 API，请务必先阅读以下文档，这将有助于您理解该 API 文档。
        * 统计时间段说明
        * 指标的定义以及统计方式
        Call steps:
        1. Pass "describe_district_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_district_data
        """
        reqs = service.mcp_post("McpDescribeDistrictData", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_district_ranking(body: dict) -> str:
        """
        API 说明
        基于火山引擎内容分发网络（CDN）收到的用户请求，该 API 按分组对一系列的指标数据进行汇总，并对这些汇总数据按从大到小排序。分组条件包括国家和地区、中国省级行政区和中国网络运营商。
        要调用该 API，您需要指定一个指标，一个分组条件，一个统计时间段和一个时间粒度。您还可以指定多个过滤条件对用户请求进行过滤。您最多能查询过去 92 天的数据。
        数据稳定性：受网络波动影响，边缘节点上统计的指标数据可能会发生变化。大多数情况下，指标数据会在 12 小时内逐步稳定下来。
        数据时效性：指标数据可能会有 5 分钟左右的延时。
        如果您是刚开始使用数据统计的 API，请务必先阅读以下文档，这将有助于您理解该 API 文档。
        * 统计时间段说明
        * 指标的定义以及统计方式
        Call steps:
        1. Pass "describe_district_ranking" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_district_ranking
        """
        reqs = service.mcp_post("McpDescribeDistrictRanking", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_edge_status_code_ranking(body: dict) -> str:
        """
        API 说明
        基于火山引擎内容分发网络（CDN）收到的用户请求，该 API 按加速域名对一系列的指标数据进行汇总，并对这些汇总数据按从大到小排序。
        要调用该 API，您需要指定一个状态码指标，一个统计时间段和一个时间粒度。您还可以指定多个过滤条件对用户请求进行过滤。您最多能查询过去 92 天的数据。
        数据稳定性：受网络波动影响，边缘节点上统计的指标数据可能会发生变化。大多数情况下，指标数据会在 12 小时内逐步稳定下来。
        数据时效性：指标数据可能会有 5 分钟左右的延时。
        如果您是刚开始使用数据统计的 API，请务必先阅读以下文档，这将有助于您理解该 API 文档。
        * 统计时间段说明
        Call steps:
        1. Pass "describe_edge_status_code_ranking" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_edge_status_code_ranking
        """
        reqs = service.mcp_post(
            "McpDescribeEdgeStatusCodeRanking", {}, json.dumps(body)
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_district_summary(body: dict) -> str:
        """
        API 说明
        基于火山引擎内容分发网络（CDN）收到的用户请求，该 API 对一个指标统计其汇总数据。
        要调用该 API，您需要指定一个指标，一个统计时间段和一个时间粒度。您还可以指定多个过滤条件对用户请求进行过滤。您最多能查询过去 92 天的数据。
        数据稳定性：受网络波动影响，边缘节点上统计的指标数据可能会发生变化。大多数情况下，指标数据会在 12 小时内逐步稳定下来。因此，该 API 返回的指标数据并非账单中显示的用量，仅供参考。实际用量请以账单为准。
        数据时效性：指标数据可能会有 5 分钟左右的延时。
        如果您是刚开始使用数据统计的 API，请务必先阅读以下文档，这将有助于您理解该 API 文档。
        * 统计时间段说明
        * 指标的定义以及统计方式
        Call steps:
        1. Pass "describe_district_summary" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_district_summary
        """
        reqs = service.mcp_post("McpDescribeDistrictSummary", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_origin_data(body: dict) -> str:
        """
        API 说明
        基于火山引擎内容分发网络（CDN）向源站发送的请求（回源请求），该 API 对一个指标统计各时间点的指标细分数据。
        要调用该 API，您需要指定一个指标，一个统计时间段和一个时间粒度。您还可以指定多个过滤条件对用户回源请求进行过滤。您最多能查询过去 92 天的数据。
        数据稳定性：受网络波动影响，回源节点上统计的指标数据可能会发生变化。大多数情况下，指标数据会在 12 小时内逐步稳定下来。
        数据时效性：指标数据可能会有 5 分钟左右的延时。
        如果您是刚开始使用数据统计的 API，请务必先阅读以下文档，这将有助于您理解该 API 文档。
        * 统计时间段说明
        * 指标的定义以及统计方式
        Call steps:
        1. Pass "describe_origin_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_origin_data
        """
        reqs = service.mcp_post("McpDescribeOriginData", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_edge_ranking(body: dict) -> str:
        """
        API 说明
        基于火山引擎内容分发网络（CDN）收到的用户请求，该 API 按分组对一系列的指标数据进行汇总，并对这些汇总数据按从大到小排序。分组条件包括加速域名和计费区域。
        要调用该 API，您需要指定一个指标，一个分组条件，一个统计时间段和一个时间粒度。您还可以指定多个过滤条件（包括计费区域）对用户请求进行过滤。您最多能查询过去 92 天的数据。
        数据稳定性：受网络波动影响，边缘节点上统计的指标数据可能会发生变化。大多数情况下，指标数据会在 12 小时内逐步稳定下来。
        数据时效性：指标数据可能会有 5 分钟左右的延时。
        如果您是刚开始使用数据统计的 API，请务必先阅读以下文档，这将有助于您理解该 API 文档。
        * 统计时间段说明
        * 指标的定义以及统计方式
        Call steps:
        1. Pass "describe_edge_ranking" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_edge_ranking
        """
        reqs = service.mcp_post("McpDescribeEdgeRanking", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_edge_data(body: dict) -> str:
        """
        API 说明
        基于火山引擎内容分发网络（CDN）收到的用户请求，该 API 对一个指标统计各时间点的指标细分数据。
        要调用该 API，您需要指定一个指标，一个统计时间段和一个时间粒度。您还可以指定多个过滤条件（包括计费区域）对用户请求进行过滤。您最多能查询过去 92 天的数据。
        数据稳定性：受网络波动影响，边缘节点上统计的指标数据可能会发生变化。大多数情况下，指标数据会在 12 小时内逐步稳定下来。
        数据时效性：指标数据可能会有 5 分钟左右的延时。
        如果您是刚开始使用数据统计的 API，请务必先阅读以下文档，这将有助于您理解该 API 文档。
        * 统计时间段说明
        * 指标的定义以及统计方式
        Call steps:
        1. Pass "describe_edge_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_edge_data
        """
        reqs = service.mcp_post("McpDescribeEdgeData", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_edge_summary(body: dict) -> str:
        """
        API 说明
        基于火山引擎内容分发网络（CDN）收到的用户请求，该 API 对一个指标统计其汇总数据。
        要调用该 API，您需要指定一个指标，一个统计时间段和一个时间粒度。您还可以指定多个过滤条件（包括计费区域）对用户请求进行过滤。您最多能查询过去 92 天的数据。
        数据稳定性：受网络波动影响，边缘节点上统计的指标数据可能会发生变化。大多数情况下，指标数据会在 12 小时内逐步稳定下来。因此，该 API 返回的指标数据并非账单中显示的用量，仅供参考。实际用量请以账单为准。
        数据时效性：指标数据可能会有 5 分钟左右的延时。
        如果您是刚开始使用数据统计的 API，请务必先阅读以下文档，这将有助于您理解该 API 文档。
        * 统计时间段说明
        * 指标的定义以及统计方式
        Call steps:
        1. Pass "describe_edge_summary" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_edge_summary
        """
        reqs = service.mcp_post("McpDescribeEdgeSummary", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_origin_ranking(body: dict) -> str:
        """
        API 说明
        基于火山引擎内容分发网络（CDN）向源站发送的请求（回源请求），该 API 按加速域名对一系列的指标数据进行汇总，并对这些汇总数据按从大到小排序。
        要调用该 API，您需要指定一个指标，一个统计时间段和一个时间粒度。您还可以指定多个过滤条件对回源请求进行过滤。您最多能查询过去 92 天的数据。
        数据稳定性：受网络波动影响，回源节点上统计的指标数据可能会发生变化。大多数情况下，指标数据会在 12 小时内逐步稳定下来。
        数据时效性：指标数据可能会有 5 分钟左右的延时。
        如果您是刚开始使用数据统计的 API，请务必先阅读以下文档，这将有助于您理解该 API 文档。
        * 统计时间段说明
        * 指标的定义以及统计方式
        Call steps:
        1. Pass "describe_origin_ranking" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_origin_ranking
        """
        reqs = service.mcp_post("McpDescribeOriginRanking", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_statistical_ranking(body: dict) -> str:
        """
        API 说明
        基于火山引擎内容分发网络（CDN）收到的用户请求，该 API 按热门对象类型对一系列的指标数据进行汇总，并对这些汇总数据按从大到小排序，最后返回这些热门对象。热门对象类型包括请求客户端所在的国家和地区、请求 URL、Referer 域名、UA 字符串中的对象、独立客户端 IP 地址的数量。
        在调用该 API 时，您需要指定一个指标，一个热门对象类型，一个统计时间段和一个时间粒度。您还可以指定多个过滤条件对用户请求进行过滤。您最多能查询过去 92 天的数据。
        数据稳定性：受网络波动影响，边缘节点上统计的指标数据可能会发生变化。大多数情况下，指标数据会在 12 小时内逐步稳定下来。
        数据时效性：热门对象是基于按小时粒度统计的指标数据。因此，数据统计可能会有 2 小时左右的延时。例如，对于 09:00 至 10:00 这个时间段的热门对象，您可以在 11:00 左右获取到准确的结果。
        Call steps:
        1. Pass "describe_statistical_ranking" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_statistical_ranking
        """
        reqs = service.mcp_post("McpDescribeStatisticalRanking", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_origin_status_code_ranking(body: dict) -> str:
        """
        API 说明
        基于火山引擎内容分发网络（CDN）从源站收到的响应状态码，该 API 按加速域名对一系列的指标数据进行汇总，并对这些汇总数据按从大到小排序。
        要调用该 API，您需要指定一个状态码指标，一个统计时间段和一个时间粒度。您还可以指定多个过滤条件对回源请求进行过滤。您最多能查询过去 92 天的数据。
        数据稳定性：受网络波动影响，回源节点上统计的指标数据可能会发生变化。大多数情况下，指标数据会在 12 小时内逐步稳定下来。
        数据时效性：指标数据可能会有 5 分钟左右的延时。
        如果您是刚开始使用数据统计的 API，请务必先阅读以下文档，这将有助于您理解该 API 文档。
        * 统计时间段说明
        Call steps:
        1. Pass "describe_origin_status_code_ranking" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_origin_status_code_ranking
        """
        reqs = service.mcp_post(
            "McpDescribeOriginStatusCodeRanking", {}, json.dumps(body)
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_user_data(body: dict) -> str:
        """

        Call steps:
        1. Pass "describe_user_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_user_data
        """
        reqs = service.mcp_post("McpDescribeUserData", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_origin_summary(body: dict) -> str:
        """
        API 说明
        基于火山引擎内容分发网络（CDN）向源站发送的请求（回源请求），该 API 对一个指标统计其汇总数据。
        要调用该 API，您需要指定一个指标，一个统计时间段和一个时间粒度。您还可以指定多个过滤条件对回源请求进行过滤。您最多能查询过去 92 天的数据。
        数据稳定性：受网络波动影响，回源节点上统计的指标数据可能会发生变化。大多数情况下，指标数据会在 12 小时内逐步稳定下来。
        数据时效性：指标数据可能会有 5 分钟左右的延时。
        如果您是刚开始使用数据统计的 API，请务必先阅读以下文档，这将有助于您理解该 API 文档。
        * 统计时间段说明
        * 指标的定义以及统计方式
        Call steps:
        1. Pass "describe_origin_summary" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_origin_summary
        """
        reqs = service.mcp_post("McpDescribeOriginSummary", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    return mcp
