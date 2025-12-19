from src.live.api.api import LiveAPI
from mcp.server.fastmcp import FastMCP
from .note import note
from src.utils.response import HandlerVolcResponse
import json


def create_mcp_server():
    service = LiveAPI()
    mcp = FastMCP(
        "LIVE MCP",
        instructions="Volcengine(火山引擎) LIVE(视频直播) MCP",
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
        return note.get(func_name)

    @mcp.tool()
    def describe_live_stream_count_data(body: dict) -> str:
        """
        调用 DescribeLiveStreamCountData 接口，查询时间范围内指定推流、回源流或转码流的峰值数量。
        Call steps:
        1. Pass "describe_live_stream_count_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_live_stream_count_data
        """
        reqs = service.mcp_post("McpDescribeLiveStreamCountData", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_live_batch_stream_traffic_data(body: dict) -> str:
        """
        调用 DescribeLiveBatchStreamTrafficData 接口，查询指定时间范围内的上下行流量数据及其详细数据。
        Call steps:
        1. Pass "describe_live_batch_stream_traffic_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_live_batch_stream_traffic_data
        """
        reqs = service.mcp_post(
            "McpDescribeLiveBatchStreamTrafficData", {}, json.dumps(body)
        )

        return HandlerVolcResponse(reqs)


    def describe_live_source_traffic_data(body: dict) -> str:
        """
        调用 DescribeLiveSourceTrafficData 接口，查询指定时间范围内拉流域名或回源流产生的回源流量和带宽监控数据。
        Call steps:
        1. Pass "describe_live_source_traffic_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_live_source_traffic_data
        """
        reqs = service.mcp_post(
            "McpDescribeLiveSourceTrafficData", {}, json.dumps(body)
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_live_stream_session_data(body: dict) -> str:
        """
        调用 DescribeLiveStreamSessionData 接口，查询指定时间范围内域名下所有直播流或指定直播流的请求数和最大在线人数。
        Call steps:
        1. Pass "describe_live_stream_session_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_live_stream_session_data
        """
        reqs = service.mcp_post(
            "McpDescribeLiveStreamSessionData", {}, json.dumps(body)
        )

        return HandlerVolcResponse(reqs)


    def describe_live_play_status_code_data(body: dict) -> str:
        """
        调用 DescribeLivePlayStatusCodeData 接口，查询指定时间范围内域名请求的状态码占比数据，包含推流请求、拉流请求和回源请求。
        Call steps:
        1. Pass "describe_live_play_status_code_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_live_play_status_code_data
        """
        reqs = service.mcp_post(
            "McpDescribeLivePlayStatusCodeData", {}, json.dumps(body)
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_live_push_stream_metrics(body: dict) -> str:
        """
        调用 DescribeLivePushStreamMetrics 接口，查询指定时间范围内单路直播推流的音视频帧率、码率等监控数据，用于判断直播流的健康程度。
        Call steps:
        1. Pass "describe_live_push_stream_metrics" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_live_push_stream_metrics
        """
        reqs = service.mcp_post(
            "McpDescribeLivePushStreamMetrics", {}, json.dumps(body)
        )

        return HandlerVolcResponse(reqs)


    def describe_live_source_stream_metrics(body: dict) -> str:
        """
        调用 DescribeLiveSourceStreamMetrics 接口，查询指定时间范围内单路回源流的音视频帧率、码率等监控数据，用于判断回源流的健康程度。
        Call steps:
        1. Pass "describe_live_source_stream_metrics" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_live_source_stream_metrics
        """
        reqs = service.mcp_post(
            "McpDescribeLiveSourceStreamMetrics", {}, json.dumps(body)
        )

        return HandlerVolcResponse(reqs)


    def describe_live_batch_stream_transcode_data(body: dict) -> str:
        """
        调用 DescribeLiveBatchStreamTranscodeData 接口，查询指定时间范围内域名下所有转码流的转码时长、分辨率档位、编码方式等转码数据。
        Call steps:
        1. Pass "describe_live_batch_stream_transcode_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_live_batch_stream_transcode_data
        """
        reqs = service.mcp_post(
            "McpDescribeLiveBatchStreamTranscodeData", {}, json.dumps(body)
        )

        return HandlerVolcResponse(reqs)


    def describe_live_batch_push_stream_metrics(body: dict) -> str:
        """
        调用 DescribeLiveBatchPushStreamMetrics 接口，查询指定时间范围内指定推流域名下所有直推流或指定直推流的音视频帧率、码率等监控数据，用于判断直播流的健康程度。
        Call steps:
        1. Pass "describe_live_batch_push_stream_metrics" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_live_batch_push_stream_metrics
        """
        reqs = service.mcp_post(
            "McpDescribeLiveBatchPushStreamMetrics", {}, json.dumps(body)
        )

        return HandlerVolcResponse(reqs)


    def describe_live_batch_source_stream_metrics(body: dict) -> str:
        """
        调用 DescribeLiveBatchSourceStreamMetrics 接口，查询指定时间范围内指定拉流域名下所有回源流或指定回源流的音视频帧率、码率等监控数据，用于判断回源流的健康程度。
        Call steps:
        1. Pass "describe_live_batch_source_stream_metrics" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_live_batch_source_stream_metrics
        """
        reqs = service.mcp_post(
            "McpDescribeLiveBatchSourceStreamMetrics", {}, json.dumps(body)
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_ip_info(body: dict) -> str:
        """
        调用 DescribeIpInfo 接口，查询 IP 地址是否为火山引擎归属的 CDN 节点，以及节点的区域和运营商信息。
        Call steps:
        1. Pass "describe_ip_info" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_ip_info
        """
        reqs = service.mcp_post("McpDescribeIpInfo", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def generate_play_url(body: dict) -> str:
        """
        调用 GeneratePlayURL 接口，生成直播拉流地址。
        Call steps:
        1. Pass "generate_play_url" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  generate_play_url
        """
        reqs = service.mcp_post("McpGeneratePlayURL", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def generate_push_url(body: dict) -> str:
        """
        调用 GeneratePushURL 接口，生成直播推流地址。
        Call steps:
        1. Pass "generate_push_url" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  generate_push_url
        """
        reqs = service.mcp_post("McpGeneratePushURL", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_domain(body: dict) -> str:
        """
        调用 DescribeDomain 接口，查询域名的详细信息，包括但不限于域名所属域名空间、CNAME、类型、域名状态。
        Call steps:
        1. Pass "describe_domain" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_domain
        """
        reqs = service.mcp_post("McpDescribeDomain", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def list_domain_detail(body: dict) -> str:
        """
        调用 ListDomainDetail 接口，根据域名状态、类别等信息，查询当前账号下的的域名列表信息。
        Call steps:
        1. Pass "list_domain_detail" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  list_domain_detail
        """
        reqs = service.mcp_post("McpListDomainDetail", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)


    def describe_live_isp_data() -> str:
        """
        调用 DescribeLiveISPData 接口，查询所有为火山引擎视频直播提供网络接入服务的运营商标识符。获取运营商标识符后您可以在支持以运营商为查询维度的接口中使用运营商标识符查询指定运营商的维度数据。
        Call steps:
        1. Pass "describe_live_isp_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_live_isp_data
        """
        reqs = service.mcp_post("McpDescribeLiveISPData", {}, json.dumps({}))

        return HandlerVolcResponse(reqs)


    def describe_live_region_data() -> str:
        """
        调用 DescribeLiveRegionData 接口，查询火山引擎视频直播服务覆盖的区域标识符。获取区域标识符后您可以在支持以区域为查询维度的接口中使用区域标识符查询指定区域的维度数据。
        Call steps:
        1. Pass "describe_live_region_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_live_region_data
        """
        reqs = service.mcp_post("McpDescribeLiveRegionData", {}, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_live_push_stream_info_data(body: dict) -> str:
        """
        调用 DescribeLivePushStreamInfoData 接口，查询已断开的推流流信息以及推流断开的原因。
        Call steps:
        1. Pass "describe_live_push_stream_info_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_live_push_stream_info_data
        """
        reqs = service.mcp_post(
            "McpDescribeLivePushStreamInfoData", {}, json.dumps(body)
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_live_transcode_info_data(body: dict) -> str:
        """
        调用 DescribeLiveTranscodeInfoData 接口，查询指定时间范围内直播域名或直播流的转码任务 ID、流名称、转码后缀、转码开始时间和结束时间数据等明细数据。
        Call steps:
        1. Pass "describe_live_transcode_info_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_live_transcode_info_data
        """
        reqs = service.mcp_post(
            "McpDescribeLiveTranscodeInfoData", {}, json.dumps(body)
        )

        return HandlerVolcResponse(reqs)


    def describe_live_batch_stream_session_data(body: dict) -> str:
        """
        调用 DescribeLiveBatchStreamSessionData 接口，查询指定时间范围内域名下所有直播流的请求数和最大在线人数。
        Call steps:
        1. Pass "describe_live_batch_stream_session_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_live_batch_stream_session_data
        """
        reqs = service.mcp_post(
            "McpDescribeLiveBatchStreamSessionData", {}, json.dumps(body)
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_live_top_play_data(body: dict) -> str:
        """
        调用 DescribeLiveTopPlayData 接口，查询指定时间范围内 TOPN 直播流或 TOPN 域名的流量和带宽信息。
        Call steps:
        1. Pass "describe_live_top_play_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_live_top_play_data
        """
        reqs = service.mcp_post("McpDescribeLiveTopPlayData", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)


    def describe_live_edge_stat_data(body: dict) -> str:
        """
        调用 DescribeLiveEdgeStatData 接口，查询指定协议、运营商、区域、时间范围下，直播流产生的上下行流量、上下行峰值带宽和请求数等数据。
        Call steps:
        1. Pass "describe_live_edge_stat_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_live_edge_stat_data
        """
        reqs = service.mcp_post("McpDescribeLiveEdgeStatData", {}, json.dumps(body))

        return HandlerVolcResponse(reqs)

    return mcp
