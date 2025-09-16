import json
import logging
import time
from typing import Optional

from mcp.server.fastmcp import Context
from mcp.server.fastmcp import FastMCP
from mcp.server.session import ServerSession
from starlette.requests import Request

from mcp_server_sec_agent.client.model import *
from mcp_server_sec_agent.client.sec_intelligent_client import SecIntelligentClient
from mcp_server_sec_agent.config import load_config
from mcp_server_sec_agent.const import *
from mcp_server_sec_agent.main import config

logger = logging.getLogger(__name__)

mcp = FastMCP("Security Intelligent MCP Server")


def loop_query_result(client: SecIntelligentClient, result: dict | SecIntelligentMCPCallResult) -> str:
    it = 0
    for it in range(MAX_ITERATIONS):
        query_result = client.get_result(SecIntelligentMCPCallRequest(result["ResultID"]))
        if query_result.tool_call_status == TOOL_CALL_STATUS_FAILED:
            raise RuntimeError("loop result failed, result: {}".format(result))
        if query_result.tool_call_status == TOOL_CALL_STATUS_SUCCESS:
            break
        time.sleep(ITERATION_SLEEP_SECONDS)

    if it == MAX_ITERATIONS - 1:
        raise RuntimeError("max iterations reached:{},  last_iteration_result: {}".format(it, result))
    if config.debug:
        return json.dumps(query_result, ensure_ascii=False)
    else:
        return json.dumps(query_result.result_data, ensure_ascii=False)


@mcp.tool()
def alert_formatter(
        alert_msg: str,
) -> str:
    """
    告警参数格式化工具，用于从原始告警信息中提取核心攻击特征。通过结构化解析和关键字段提取，将非结构化的原始告警转换为标准化的安全事件特征表示，为后续分析研判提供规范化输入
    Args:
        alert_msg: 原始告警内容：包含完整细节的非结构化告警信息，通常包括时间戳、事件类型、源/目的IP、端口、协议等原始数据
    Returns:
        结构化特征对象
    """
    req = ParamsFormatRequest(
        alert_msg=alert_msg,
    )

    ctx: Context[ServerSession, object] = mcp.get_context()
    raw_request: Request = ctx.request_context.request

    config = load_config(raw_request)
    client = SecIntelligentClient(config)

    # 第一步，拿到 result id
    alert_formatter_result = client.params_format(req)

    # 第二步，调用 result 接口获取结果
    if "ResultID" not in alert_formatter_result.result:
        raise RuntimeError("ResultID not found in result, result: {}".format(alert_formatter_result.result))

    return loop_query_result(client, alert_formatter_result.result)


@mcp.tool()
def alert_investigator(
        alert_msg: str,
        data_ref: Optional[str] = "",
        principal: Optional[str] = "",
) -> str:
    """
    安全告警智能研判工具，支持结合原始告警数据、关联上下文及安全专家经验进行自动化分析。通过多维度关联分析与知识库匹配，输出研判结论与处置建议
    Args:
        alert_msg: 告警内容：告警的详细信息，如告警时间、告警级别、告警来源、告警内容等
        data_ref: (可选)关联上下文：告警关联的上下文信息，如日志、流量等
        principal: （可选）专家经验：相关的安全专家经验，如安全策略、安全最佳实践、安全专家的分析等
    Returns:
        告警研判结论
    """
    req = AlertAnalysisRequest(
        alert_msg=alert_msg,
        data_ref=data_ref,
        principal=principal,
        alert_id="",
        tool_use="",
    )

    ctx: Context[ServerSession, object] = mcp.get_context()
    raw_request: Request = ctx.request_context.request

    config = load_config(raw_request)
    client = SecIntelligentClient(config)

    # 第一步，拿到 result id
    alert_analysis_result = client.alert_analysis(req)

    # 第二步，调用 result 接口获取结果
    if "ResultID" not in alert_analysis_result.result:
        raise RuntimeError("ResultID not found in result, result: {}".format(alert_analysis_result.result))

    return loop_query_result(client, alert_analysis_result.result)


@mcp.tool()
def dlp_screenshot_analyzer(
        snapshot: str,
) -> str:
    """
    数据防泄漏智能检测平台，识别终端截图中的敏感文档操作、数据外发等违规行为。支持检测多类高风险操作场景（含代码泄露/财务数据展示/客户信息浏览等内容）
    Args:
        snapshot: 终端屏幕截图访问链接（需支持直接下载）
    Returns:
        截图分析结果
    """
    req = DLPEndpointCaptureAnalysisRequest(
        image_url=snapshot,
    )

    ctx: Context[ServerSession, object] = mcp.get_context()
    raw_request: Request = ctx.request_context.request

    config = load_config(raw_request)
    client = SecIntelligentClient(config)

    # 第一步，拿到 result id
    dlp_screenshot_analyzer_result = client.dlp_endpoint_capture_analysis(req)

    # 第二步，调用 result 接口获取结果
    if "ResultID" not in dlp_screenshot_analyzer_result.result:
        raise RuntimeError(
            "ResultID not found in result, result: {}".format(dlp_screenshot_analyzer_result.result))

    return loop_query_result(client, dlp_screenshot_analyzer_result.result)


@mcp.tool()
def pcap_analysis(
        pcap: str,
) -> str:
    """
    网络流量深度分析工具，提供从基础协议解析到高级威胁检测的全维度pcap分析能力
    Args:
        pcap: base64 编码的 pcap 文件内容，支持包含完整网络会话的抓包数据
    Returns:
        pcap 包分析结果
    """
    req = PcapAnalysisRequest(
        pcap_base64_encoded=pcap,
    )

    ctx: Context[ServerSession, object] = mcp.get_context()
    raw_request: Request = ctx.request_context.request

    config = load_config(raw_request)
    client = SecIntelligentClient(config)

    # 第一步，拿到 result id
    pcap_analysis_result = client.pcap_analysis(req)

    # 第二步，调用 result 接口获取结果
    if "ResultID" not in pcap_analysis_result.result:
        raise RuntimeError("ResultID not found in result, result: {}".format(pcap_analysis_result.result))

    return loop_query_result(client, pcap_analysis_result.result)


@mcp.tool()
def sensitive_data_detector(
        file_content: str,
        extract_type: Optional[str] = "",
) -> str:
    """
    敏感数据智能识别引擎，支持检测各类敏感数据。支持自定义识别规则与行业合规标准（GDPR/HIPAA/PCIDSS）联动，提供数据定位、风险评级等分析内容
    Args:
        file_content: 待检测的原始数据内容，支持文本/文档/日志等多种文件内容
        extract_type: （可选）自定义敏感数据标准
    Returns:
        敏感数据分析结果
    """
    req = SensitiveDataIdentificationRequest(
        file_content=file_content,
        extract_type=extract_type,
    )

    ctx: Context[ServerSession, object] = mcp.get_context()
    raw_request: Request = ctx.request_context.request

    config = load_config(raw_request)
    client = SecIntelligentClient(config)

    # 第一步，拿到 result id
    sensitive_data_detector_result = client.sensitive_data_identification(req)

    # 第二步，调用 result 接口获取结果
    if "ResultID" not in sensitive_data_detector_result.result:
        raise RuntimeError(
            "ResultID not found in result, result: {}".format(sensitive_data_detector_result.result))

    return loop_query_result(client, sensitive_data_detector_result.result)


@mcp.tool()
def threat_intel_producer(
        input_msg: str,
) -> str:
    """
    威胁情报自动化生产系统，通过自然语言处理与结构化分析引擎，从非结构化安全报告中提取IOC（入侵指标）、TTP（战术技术与过程）、攻击者画像等要素。集成MITRE ATT&CK框架映射，输出符合STIX/TAXII标准的可机读威胁情报
    Args:
        input_msg: 待转换的安全文本内容
    Returns:
        结构化的威胁情报数据
    """
    req = ThreatIntelligenceProductionRequest(
        url="",
        input_msg=input_msg,
    )

    ctx: Context[ServerSession, object] = mcp.get_context()
    raw_request: Request = ctx.request_context.request

    config = load_config(raw_request)
    client = SecIntelligentClient(config)

    # 第一步，拿到 result id
    threat_intel_producer_result = client.threat_intelligence_production(req)

    # 第二步，调用 result 接口获取结果
    if "ResultID" not in threat_intel_producer_result.result:
        raise RuntimeError(
            "ResultID not found in result, result: {}".format(threat_intel_producer_result.result))

    return loop_query_result(client, threat_intel_producer_result.result)


@mcp.tool()
def web_risk_assessor(
        snapshot: str,
        url: Optional[str] = "",
        icp_info: Optional[str] = "",
) -> str:
    """
    网页安全风险多维评估系统，通过视觉特征分析、备案信息核验与威胁情报交叉比对，识别钓鱼网站/仿冒页面等各类网页风险
    Args:
        snapshot: 网页截图链接（需支持直接下载）
        url:（可选）网页原始URL
        icp_info:（可选）ICP备案信息
    Returns:
        网页风险评估结果
    """
    req = URLRiskDetectionRequest(
        snap_shot=snapshot,
        url=url,
        icp_info=icp_info,
    )

    ctx: Context[ServerSession, object] = mcp.get_context()
    raw_request: Request = ctx.request_context.request

    config = load_config(raw_request)
    client = SecIntelligentClient(config)

    # 第一步，拿到 result id
    web_risk_assessor_result = client.url_risk_detection(req)

    # 第二步，调用 result 接口获取结果
    if "ResultID" not in web_risk_assessor_result.result:
        raise RuntimeError(
            "ResultID not found in result, result: {}".format(web_risk_assessor_result.result))

    return loop_query_result(client, web_risk_assessor_result.result)
