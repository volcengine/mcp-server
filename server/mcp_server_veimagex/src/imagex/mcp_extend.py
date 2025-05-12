from .api.api import ImagexAPI
from .note import note
from utils.response import HandlerVolcResponse
import json


def create_api_mcp_server(mcp):
    service = ImagexAPI()
    
    @mcp.tool()
    def get_note(func_name: str) -> str:
        """
        获取参数描述

        Args:
            func_name: 函数名

        """
        return note.get(func_name)

    @mcp.tool()
    def get_service_domains(params: dict) -> str:
        """
        本接口支持通过指定服务 ID 获取服务下所有域名信息。
        Call steps:
        1. Pass "get_service_domains" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_service_domains
        """
        reqs = service.mcp_get("McpGetServiceDomains", params, json.dumps({}))

        return HandlerVolcResponse(reqs)


    @mcp.tool()
    def describe_imagex_summary(params: dict) -> str:
        """
        本接口支持通过指定时间点以及服务 ID，查询本月用量概览，包括带宽、流量、存储、请求次数、基础图像处理。
        Call steps:
        1. Pass "describe_imagex_summary" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_summary
        """
        reqs = service.mcp_get("McpDescribeImageXSummary", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_imagex_domain_traffic_data(params: dict) -> str:
        """
        本接口支持通过自定义时间段，来查询域名流量用量。
        Call steps:
        1. Pass "describe_imagex_domain_traffic_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_domain_traffic_data
        """
        reqs = service.mcp_get(
            "McpDescribeImageXDomainTrafficData", params, json.dumps({})
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_imagex_domain_bandwidth_data(params: dict) -> str:
        """
        本接口支持通过自定义时间段，查询域名带宽用量。
        Call steps:
        1. Pass "describe_imagex_domain_bandwidth_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_domain_bandwidth_data
        """
        reqs = service.mcp_get(
            "McpDescribeImageXDomainBandwidthData", params, json.dumps({})
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_imagex_billing_request_cnt_usage(params: dict) -> str:
        """
        本接口支持通过自定义查询时间段，获取该时间段的附加组件通用请求次数。
        Call steps:
        1. Pass "describe_imagex_billing_request_cnt_usage" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_billing_request_cnt_usage
        """
        reqs = service.mcp_get(
            "McpDescribeImageXBillingRequestCntUsage", params, json.dumps({})
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_imagex_request_cnt_usage(params: dict) -> str:
        """
        本接口支持通过自定义查询时间段，查询该时间段的请求次数。
        Call steps:
        1. Pass "describe_imagex_request_cnt_usage" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_request_cnt_usage
        """
        reqs = service.mcp_get(
            "McpDescribeImageXRequestCntUsage", params, json.dumps({})
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_imagex_base_op_usage(params: dict) -> str:
        """
        本接口支持通过自定义时间段，查询该时间段的图像基础处理量。
        Call steps:
        1. Pass "describe_imagex_base_op_usage" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_base_op_usage
        """
        reqs = service.mcp_get("McpDescribeImageXBaseOpUsage", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_imagex_compress_usage(params: dict) -> str:
        """
        本接口支持通过自定义查询时间段，查询该时间段的图像高效压缩量。
        Call steps:
        1. Pass "describe_imagex_compress_usage" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_compress_usage
        """
        reqs = service.mcp_get("McpDescribeImageXCompressUsage", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_imagex_screenshot_usage(params: dict) -> str:
        """
        本接口支持通过自定义查询时间段，查询该时间段的截帧用量。
        Call steps:
        1. Pass "describe_imagex_screenshot_usage" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_screenshot_usage
        """
        reqs = service.mcp_get(
            "McpDescribeImageXScreenshotUsage", params, json.dumps({})
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_imagex_video_clip_duration_usage(params: dict) -> str:
        """
        本接口支持通过自定义查询时间段，查询该时间段的小视频转动图的视频转换时长用量。
        Call steps:
        1. Pass "describe_imagex_video_clip_duration_usage" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_video_clip_duration_usage
        """
        reqs = service.mcp_get(
            "McpDescribeImageXVideoClipDurationUsage", params, json.dumps({})
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_imagex_multi_compress_usage(params: dict) -> str:
        """
        本接口支持通过自定义查询时间段，查询该时间段的多文件压缩用量。
        Call steps:
        1. Pass "describe_imagex_multi_compress_usage" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_multi_compress_usage
        """
        reqs = service.mcp_get(
            "McpDescribeImageXMultiCompressUsage", params, json.dumps({})
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_imagex_edge_request(params: dict) -> str:
        """
        本接口支持通过自定义查询时间段，查询该时间段的边缘请求次数。
        Call steps:
        1. Pass "describe_imagex_edge_request" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_edge_request
        """
        reqs = service.mcp_get("McpDescribeImageXEdgeRequest", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_imagex_edge_request_bandwidth(params: dict) -> str:
        """
        本接口支持通过自定义查询时间段，查询该时间段的边缘分发带宽用量。
        Call steps:
        1. Pass "describe_imagex_edge_request_bandwidth" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_edge_request_bandwidth
        """
        reqs = service.mcp_get(
            "McpDescribeImageXEdgeRequestBandwidth", params, json.dumps({})
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_imagex_edge_request_traffic(params: dict) -> str:
        """
        本接口支持通过自定义查询时间段，查询该时间段的边缘分发流量用量。
        Call steps:
        1. Pass "describe_imagex_edge_request_traffic" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_edge_request_traffic
        """
        reqs = service.mcp_get(
            "McpDescribeImageXEdgeRequestTraffic", params, json.dumps({})
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_imagex_edge_request_regions(params: dict) -> str:
        """
        本接口支持通过自定义查询时间段，查询该时间段的边缘分发数据的地区列表。
        Call steps:
        1. Pass "describe_imagex_edge_request_regions" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_edge_request_regions
        """
        reqs = service.mcp_get(
            "McpDescribeImageXEdgeRequestRegions", params, json.dumps({})
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_imagex_server_qps_usage(params: dict) -> str:
        """
        本接口支持通过自定义时间段，获取当前账号的数据处理服务 QPS 用量。
        Call steps:
        1. Pass "describe_imagex_server_qps_usage" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_server_qps_usage
        """
        reqs = service.mcp_get(
            "McpDescribeImageXServerQPSUsage", params, json.dumps({})
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_imagex_hit_rate_traffic_data(params: dict) -> str:
        """
        本接口支持通过自定义查询时间段，查询该时间段的域名的 CDN 流量命中率用量数据。
        Call steps:
        1. Pass "describe_imagex_hit_rate_traffic_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_hit_rate_traffic_data
        """
        reqs = service.mcp_get(
            "McpDescribeImageXHitRateTrafficData", params, json.dumps({})
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_imagex_hit_rate_request_data(params: dict) -> str:
        """
        本接口支持通过自定义查询时间段，查询该时间段的域名的 CDN 请求次数命中率用量数据。
        Call steps:
        1. Pass "describe_imagex_hit_rate_request_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_hit_rate_request_data
        """
        reqs = service.mcp_get(
            "McpDescribeImageXHitRateRequestData", params, json.dumps({})
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_imagexcdn_top_request_data(params: dict) -> str:
        """
        本接口支持获取按照流量/请求次数排序的数据列表，即按流量或请求次数由大到小排序后，访问量最靠前的域名/URL/Refer/客户端IP/UA/访问区域/运营商等数据。
        - URL/Refer/客户端IP/UA 最多支持展示 Top 1000 的数据。
        - 访问区域/运营商可展示展示全量数据。
        Call steps:
        1. Pass "describe_imagexcdn_top_request_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagexcdn_top_request_data
        """
        reqs = service.mcp_get(
            "McpDescribeImageXCDNTopRequestData", params, json.dumps({})
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_imagex_domain_bandwidth_ninety_five_data(params: dict) -> str:
        """
        本接口支持通过自定义时间段，查询域名的 95 峰值带宽用量。
        Call steps:
        1. Pass "describe_imagex_domain_bandwidth_ninety_five_data" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_domain_bandwidth_ninety_five_data
        """
        reqs = service.mcp_get(
            "McpDescribeImageXDomainBandwidthNinetyFiveData", params, json.dumps({})
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_imagex_bucket_retrieval_usage(params: dict) -> str:
        """
        本接口支持通过自定义查询时间段，查询该时间段的每天资源占用量。
        单次查询最大时间跨度为 93 天。
        Call steps:
        1. Pass "describe_imagex_bucket_retrieval_usage" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_bucket_retrieval_usage
        """
        reqs = service.mcp_get(
            "McpDescribeImageXBucketRetrievalUsage", params, json.dumps({})
        )

        return HandlerVolcResponse(reqs)


    @mcp.tool()
    def describe_imagex_source_request(params: dict) -> str:
        """
        本接口支持通过自定义查询时间段，查询该时间段的回源请求次数。
        Call steps:
        1. Pass "describe_imagex_source_request" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_source_request
        """
        reqs = service.mcp_get("McpDescribeImageXSourceRequest", params, json.dumps({}))

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_imagex_source_request_bandwidth(params: dict) -> str:
        """
        本接口支持通过自定义查询时间段，查询该时间段的回源带宽用量。
        Call steps:
        1. Pass "describe_imagex_source_request_bandwidth" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_source_request_bandwidth
        """
        reqs = service.mcp_get(
            "McpDescribeImageXSourceRequestBandwidth", params, json.dumps({})
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_imagex_source_request_traffic(params: dict) -> str:
        """
        本接口支持通过自定义查询时间段，查询该时间段的回源流量用量。
        Call steps:
        1. Pass "describe_imagex_source_request_traffic" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_imagex_source_request_traffic
        """
        reqs = service.mcp_get(
            "McpDescribeImageXSourceRequestTraffic", params, json.dumps({})
        )

        return HandlerVolcResponse(reqs)

    @mcp.tool()
    def describe_vpc_access_config(params: dict) -> str:
        """
        本接口将为您展示指定服务的内网访问功能的配置详情。
        Call steps:
        1. Pass "describe_vpc_access_config" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  describe_vpc_access_config
        """
        reqs = service.mcp_get("McpDescribeVpcAccessConfig", params, json.dumps({}))

        return HandlerVolcResponse(reqs)
