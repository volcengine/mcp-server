import datetime
import json
import logging
import os
import time
import traceback

import volcenginesdkvolcobserve

from mcp_server_cloudmonitor import client
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from mcp_server_cloudmonitor.models.request import GetMetricsDataRequest, GetMetricsDataFilter

MCP_SERVER_NAME = "CloudMonitor"
ENV_MCP_SERVER_PORT = "MCP_SERVER_PORT"
ENV_MCP_SERVER_HOST = "MCP_SERVER_HOST"

mcp = FastMCP(MCP_SERVER_NAME, log_level="DEBUG",
              host=os.getenv(ENV_MCP_SERVER_HOST,"0.0.0.0"),
              port=int(os.getenv(ENV_MCP_SERVER_PORT, "8000")),
              streamable_http_path=os.getenv("STREAMABLE_HTTP_PATH", "/mcp"))

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(MCP_SERVER_NAME)

SERVICE_NAME = "Volc_Observe"
VERSION = "2018-01-01"

@mcp.resource("schema://{code}", mime_type="application/json")
def get_schema(code: str):
    with open(f"static/schema/{code}.json", "r") as file:
        return file.read()

@mcp.tool(description="查询指定指标在指定时间选段内聚合的时序数据")
def get_metric_data(
        region: str = Field(
            description="地域code,不要自行猜测region的取值,如果无法从上下文中获取到这个值,需要询问用户让用户进行明确"
        ),
        request: GetMetricsDataRequest = Field(description="查询请求参数"),
) -> str:
    _set_default_for_get_metric_data(request)
    logger.info("enter server process")

    try:
        api_instance = client.init_client(region=region, ctx=mcp.get_context())
        if request.Instances is None:
            request.Instances = []
        response = api_instance.get_metric_data(
            volcenginesdkvolcobserve.GetMetricDataRequest(
                start_time=request.StartTime,
                end_time=request.EndTime,
                metric_name=request.MetricName,
                namespace=request.Namespace,
                sub_namespace=request.SubNamespace,
                period=request.Period,
                group_by=request.GroupBy,
                instances=[
                    volcenginesdkvolcobserve.InstanceForGetMetricDataInput(
                        dimensions=[
                            volcenginesdkvolcobserve.DimensionForGetMetricDataInput(
                                name=dimension.Name, value=dimension.Value
                            )
                            for dimension in instance.Dimensions
                        ]
                    )
                    for instance in request.Instances
                ],
            )
        )
        if not isinstance(response, volcenginesdkvolcobserve.GetMetricDataResponse):
            raise Exception("InternalError: unexpected response")
        response = response.to_dict()
    except Exception as e:
        traceback.print_exception(e)

        logger.error(f"get_metric_data error: {e}")
        raise e

    result = []
    for item in response.get("data", {}).get("metric_data_results", []):
        current_datapoints = []
        for data_point in item.get("data_points", []):
            flattened_object = {}
            flattened_object["时间"] = datetime.datetime.fromtimestamp(
                data_point.get("timestamp")
            ).strftime("%H:%M:%S")
            flattened_object["Value"] = data_point.get("value")
            flattened_object["单位"] = response.get("data", {}).get("unit", "")
            for dimension in item.get("dimensions", []):
                flattened_object[dimension.get("name")] = dimension.get("value")
            current_datapoints.append(flattened_object)
        # filter data points
        if request.Filter is not None:
            if any(
                    _match_get_metric_data_filter(data_point.get("Value"), request.Filter)
                    for data_point in current_datapoints
            ):
                result.extend(current_datapoints)
        else:
            result.extend(current_datapoints)
    return json.dumps(result)


def _match_get_metric_data_filter(value, _filter: GetMetricsDataFilter) -> bool:
    if _filter.Operator == "=":
        return value == _filter.Value
    elif _filter.Operator == "!=":
        return value != _filter.Value
    elif _filter.Operator == ">":
        return value > _filter.Value
    elif _filter.Operator == "<":
        return value < _filter.Value
    elif _filter.Operator == ">=":
        return value >= _filter.Value
    elif _filter.Operator == "<=":
        return value <= _filter.Value
    return False


def _set_default_for_get_metric_data(request: GetMetricsDataRequest):
    # set default time range
    if request.EndTime is None:
        request.EndTime = int(time.time())
    if request.StartTime is None:
        request.StartTime = request.EndTime - 3600

    # Find the smallest period that satisfies the condition
    difference = request.EndTime - request.StartTime
    for period in range(30, 86400, 30):
        if difference // period <= 10:
            request.Period = f"{period}s"
            break

@mcp.resource("data://schema", mime_type='application/json')
def get_schema():
    return json.dumps([{"Namespace": "VCM_ECS", "SubNamespace": "GPU", "Metrics": [
        {"MetricName": "GpuMemoryUsedSpace", "MetricUnit": "Bytes(IEC)", "Dimension": "ResourceID,DeviceName",
         "Description": "GPU维度显存使用量"},
        {"MetricName": "GpuUsedUtilization", "MetricUnit": "Percent", "Dimension": "ResourceID,DeviceName",
         "Description": "GPU维度GPU使用率"},
        {"MetricName": "GpuTemperature", "MetricUnit": "℃", "Dimension": "ResourceID,DeviceName",
         "Description": "GPU维度GPU温度"},
        {"MetricName": "GpuPowerReadingsPowerDraw", "MetricUnit": "W", "Dimension": "ResourceID,DeviceName",
         "Description": "GPU维度GPU功率"},
        {"MetricName": "GpuNvLinkTotalThroughputDataRX", "MetricUnit": "Kibibytes/Second",
         "Dimension": "ResourceID,DeviceName", "Description": "所有link 60秒内读入的总吞吐"},
        {"MetricName": "GpuNvLinkTotalThroughputDataTX", "MetricUnit": "Kibibytes/Second",
         "Dimension": "ResourceID,DeviceName", "Description": "所有link 60秒内输出的总吞吐"}]},
                       {"Namespace": "VCM_ECS", "SubNamespace": "Instance", "Metrics": [
                           {"MetricName": "Instance_CpuBusy", "MetricUnit": "Percent", "Dimension": "ResourceID",
                            "Description": "实例CPU使用率,不包含 I/O 等待(IoWait)状态"},
                           {"MetricName": "Instance_DiskReadBytes", "MetricUnit": "Bytes/Second(IEC)",
                            "Dimension": "ResourceID", "Description": "实例磁盘每秒读取字节数"},
                           {"MetricName": "Instance_DiskWriteBytes", "MetricUnit": "Bytes/Second(IEC)",
                            "Dimension": "ResourceID", "Description": "实例磁盘每秒写入字节数"},
                           {"MetricName": "Instance_DiskReadIOPS", "MetricUnit": "Count/Second",
                            "Dimension": "ResourceID", "Description": "实例磁盘每秒读取的IOPS数"},
                           {"MetricName": "Instance_DiskWriteIOPS", "MetricUnit": "Count/Second",
                            "Dimension": "ResourceID", "Description": "实例磁盘每秒写入的IOPS数"},
                           {"MetricName": "Instance_NetTxBits", "MetricUnit": "Bits/Second(IEC)",
                            "Dimension": "ResourceID", "Description": "实例网络每秒流出比特数"},
                           {"MetricName": "Instance_NetRxBits", "MetricUnit": "Bits/Second(IEC)",
                            "Dimension": "ResourceID", "Description": "实例网络每秒流入比特数"},
                           {"MetricName": "Instance_NetTxPackets", "MetricUnit": "Packet/Second",
                            "Dimension": "ResourceID", "Description": "实例网络每秒流出包数"},
                           {"MetricName": "Instance_NetRxPackets", "MetricUnit": "Packet/Second",
                            "Dimension": "ResourceID", "Description": "实例网络每秒流入包数"},
                           {"MetricName": "CpuTotal", "MetricUnit": "Percent", "Dimension": "ResourceID",
                            "Description": "实例CPU总使用率"},
                           {"MetricName": "MemoryUsedSpace", "MetricUnit": "Bytes(IEC)", "Dimension": "ResourceID",
                            "Description": "实例内存已使用量"},
                           {"MetricName": "MemoryUsedUtilization", "MetricUnit": "Percent", "Dimension": "ResourceID",
                            "Description": "实例已用内存量占总内存量的比例"},
                           {"MetricName": "LoadPerCore1m", "MetricUnit": "None", "Dimension": "ResourceID",
                            "Description": "实例单核1分钟平均负载"},
                           {"MetricName": "LoadPerCore5m", "MetricUnit": "None", "Dimension": "ResourceID",
                            "Description": "实例单核5分钟平均负载"},
                           {"MetricName": "LoadPerCore15m", "MetricUnit": "None", "Dimension": "ResourceID",
                            "Description": "实例单核15分钟平均负载"},
                           {"MetricName": "NetworkInPackages", "MetricUnit": "Packet/Second", "Dimension": "ResourceID",
                            "Description": "实例网络每秒流入包数"},
                           {"MetricName": "NetworkOutPackages", "MetricUnit": "Packet/Second",
                            "Dimension": "ResourceID", "Description": "实例网络每秒流出包数"},
                           {"MetricName": "NetTcpConnection", "MetricUnit": "Count", "Dimension": "ResourceID",
                            "Description": "实例TCP连接总数"},
                           {"MetricName": "NetworkInRate", "MetricUnit": "Bits/Second(IEC)", "Dimension": "ResourceID",
                            "Description": "实例网络每秒流入比特数"},
                           {"MetricName": "NetworkOutRate", "MetricUnit": "Bits/Second(IEC)", "Dimension": "ResourceID",
                            "Description": "实例网络每秒流出比特数"},
                           {"MetricName": "GpuMemoryUsedSpace", "MetricUnit": "Bytes(SI)",
                            "Dimension": "ResourceID,DeviceName", "Description": "GPU维度显存使用量"},
                           {"MetricName": "GpuUsedUtilization", "MetricUnit": "Percent",
                            "Dimension": "ResourceID,DeviceName", "Description": "GPU维度GPU使用率"},
                           {"MetricName": "GpuTemperature", "MetricUnit": "℃", "Dimension": "ResourceID,DeviceName",
                            "Description": "GPU维度GPU温度"},
                           {"MetricName": "GpuPowerReadingsPowerDraw", "MetricUnit": "W",
                            "Dimension": "ResourceID,DeviceName", "Description": "GPU维度GPU功率"},
                           {"MetricName": "PortRDMARxBits", "MetricUnit": "Bits/Second(IEC)",
                            "Dimension": "ResourceID,NetName", "Description": "实例RDMA网络每秒接收数据量"},
                           {"MetricName": "PortRDMATxBits", "MetricUnit": "Bits/Second(IEC)",
                            "Dimension": "ResourceID,NetName", "Description": "实例RDMA网络每秒发送数据量"},
                           {"MetricName": "CpuIdle", "MetricUnit": "Percent", "Dimension": "ResourceID",
                            "Description": "实例CPU空闲状态时长占总运行时长比例"},
                           {"MetricName": "CpuSystem", "MetricUnit": "Percent", "Dimension": "ResourceID",
                            "Description": "实例CPU内核态运行时长占总运行时长比例"},
                           {"MetricName": "CPUUser", "MetricUnit": "Percent", "Dimension": "ResourceID",
                            "Description": "实例CPU用户态运行时长占总运行时长比例"},
                           {"MetricName": "CPUIowait", "MetricUnit": "Percent", "Dimension": "ResourceID",
                            "Description": "实例CPU I/O 等待时长占总运行时长比例"},
                           {"MetricName": "CpuOther", "MetricUnit": "Percent", "Dimension": "ResourceID",
                            "Description": "实例CPU其他状态运行时长占总运行时长比例"},
                           {"MetricName": "MemoryTotalSpace", "MetricUnit": "Bytes(IEC)", "Dimension": "ResourceID",
                            "Description": "实例内存总量"},
                           {"MetricName": "MemoryFreeSpace", "MetricUnit": "Bytes(IEC)", "Dimension": "ResourceID",
                            "Description": "实例内存剩余容量"}, {"MetricName": "DiskTotal", "MetricUnit": "Bytes(IEC)",
                                                                 "Dimension": "ResourceID,DiskName,VolumeId",
                                                                 "Description": "实例磁盘总容量"},
                           {"MetricName": "NetworkInErrorPackages", "MetricUnit": "Count", "Dimension": "ResourceID",
                            "Description": "实例网络流入错误包数"},
                           {"MetricName": "NetworkOutErrorPackages", "MetricUnit": "Count", "Dimension": "ResourceID",
                            "Description": "实例网络流出错误包数"},
                           {"MetricName": "DiskInodesUsedPercent", "MetricUnit": "Percent",
                            "Dimension": "ResourceID,DiskName(可选)",
                            "Description": "磁盘已用Inode索引节点占总节点的比例"},
                           {"MetricName": "NetTcpConnectionStatus", "MetricUnit": "Count", "Dimension": "ResourceID",
                            "Description": "实例TCP连接各状态总数"},
                           {"MetricName": "NetTcpConnectionStatusESTABLISHED", "MetricUnit": "Count",
                            "Dimension": "ResourceID", "Description": "实例TCP连接处于ESTABLISHED状态的次数"},
                           {"MetricName": "NetTcpConnectionStatusLISTEN", "MetricUnit": "Count",
                            "Dimension": "ResourceID", "Description": "实例TCP连接处于LISTEN状态的次数"},
                           {"MetricName": "NetTcpConnectionStatusNONESTABLISHED", "MetricUnit": "Count",
                            "Dimension": "ResourceID", "Description": "实例TCP连接处于非ESTABLISHED状态的次数"},
                           {"MetricName": "MemoryAvailable", "MetricUnit": "Bytes(IEC)", "Dimension": "ResourceID",
                            "Description": "实例可用内存量"}, {"MetricName": "ProcessCPUPct", "MetricUnit": "Percent",
                                                               "Dimension": "ResourceID,Pid,Name,Cmd",
                                                               "Description": "实例进程的CPU使用率"},
                           {"MetricName": "ProcessMemPct", "MetricUnit": "Percent",
                            "Dimension": "ResourceID,Pid,Name,Cmd", "Description": "实例进程内存使用率"},
                           {"MetricName": "ProcessOpenFds", "MetricUnit": "Count",
                            "Dimension": "ResourceID,Pid,Name,Cmd", "Description": "实例进程打开文件数"},
                           {"MetricName": "ProcessThreads", "MetricUnit": "Count",
                            "Dimension": "ResourceID,Pid,Name,Cmd", "Description": "实例进程使用的线程数"},
                           {"MetricName": "ProcTxBytes", "MetricUnit": "Bytes/Second(IEC)",
                            "Dimension": "ResourceID,Pid,Name,Cmd", "Description": "实例进程每秒发送的网络字节数"},
                           {"MetricName": "ProcRxBytes", "MetricUnit": "Bytes/Second(IEC)",
                            "Dimension": "ResourceID,Pid,Name,Cmd", "Description": "实例进程每秒接收的网络字节数"},
                           {"MetricName": "ProcTxPackets", "MetricUnit": "Count",
                            "Dimension": "ResourceID,Pid,Name,Cmd", "Description": "实例进程每秒发送的网络包数量"},
                           {"MetricName": "ProcRxPackets", "MetricUnit": "Count",
                            "Dimension": "ResourceID,Pid,Name,Cmd", "Description": "实例进程每秒接收的网络包数量"},
                           {"MetricName": "MemoryActualusedSpace", "MetricUnit": "Bytes(IEC)",
                            "Dimension": "ResourceID", "Description": "用户实际使用的内存"},
                           {"MetricName": "NetworkPerNicInPackages", "MetricUnit": "Packet/Second",
                            "Dimension": "ResourceID,IPADDR", "Description": "网卡每秒流入包数"},
                           {"MetricName": "NetworkPerNicOutPackages", "MetricUnit": "Packet/Second",
                            "Dimension": "ResourceID,IPADDR", "Description": "网卡每秒流出包数"},
                           {"MetricName": "NetworkPerNicInRate", "MetricUnit": "Bits/Second(IEC)",
                            "Dimension": "ResourceID,IPADDR", "Description": "网卡每秒流入比特数"},
                           {"MetricName": "NetworkPerNicOutRate", "MetricUnit": "Bits/Second(IEC)",
                            "Dimension": "ResourceID,IPADDR", "Description": "网卡每秒流出比特数"},
                           {"MetricName": "NetworkPerNicInErrorPackages", "MetricUnit": "Count/Second",
                            "Dimension": "ResourceID,IPADDR", "Description": "网卡流入错误包数"},
                           {"MetricName": "NetworkPerNicOutErrorPackages", "MetricUnit": "Count/Second",
                            "Dimension": "ResourceID,IPADDR", "Description": "网卡流出错误包数"},
                           {"MetricName": "Load1m", "MetricUnit": "None", "Dimension": "ResourceID",
                            "Description": "实例1分钟负载"},
                           {"MetricName": "Load5m", "MetricUnit": "None", "Dimension": "ResourceID",
                            "Description": "实例5分钟负载"},
                           {"MetricName": "Load15m", "MetricUnit": "None", "Dimension": "ResourceID",
                            "Description": "实例15分钟负载"},
                           {"MetricName": "Instance_NetConcurrentConnections", "MetricUnit": "Count",
                            "Dimension": "ResourceID", "Description": "带外网络并发连接数"},
                           {"MetricName": "ProccessTotalNum", "MetricUnit": "Count", "Dimension": "ResourceID",
                            "Description": "-"}, {"MetricName": "InstancevRDMARxBits", "MetricUnit": "Bits/Second(IEC)",
                                                  "Dimension": "ResourceID,IfacePortUUID",
                                                  "Description": "vRDMA维度每秒接收数据量"},
                           {"MetricName": "InstancevRDMATxBits", "MetricUnit": "Bits/Second(IEC)",
                            "Dimension": "ResourceID,IfacePortUUID", "Description": "VRDMA维度每秒发送数据量"},
                           {"MetricName": "InstancevRDMARxPackets", "MetricUnit": "Packet/Second",
                            "Dimension": "ResourceID,IfacePortUUID", "Description": "VRDMA维度流入数据包速率"},
                           {"MetricName": "InstancevRDMATxPackets", "MetricUnit": "Packet/Second",
                            "Dimension": "ResourceID,IfacePortUUID", "Description": "VRDMA网络发送包速率"},
                           {"MetricName": "PortvRDMAMrCount", "MetricUnit": "Count", "Dimension": "ResourceID,NetName",
                            "Description": "实例RDMA维度MR(Memory Region,内存块)的数量"},
                           {"MetricName": "PortvRDMACqCount", "MetricUnit": "Count", "Dimension": "ResourceID,NetName",
                            "Description": "VRDMA维度CQ(CompletionQueue,完成队列)的数量"},
                           {"MetricName": "PortvRDMAQpCount", "MetricUnit": "Count", "Dimension": "ResourceID,NetName",
                            "Description": "VRDMA维度QP(Queue Pair,队列结构)的数量"},
                           {"MetricName": "PortvRDMAPdCount", "MetricUnit": "Count", "Dimension": "ResourceID,NetName",
                            "Description": "VRDMA维度PD(Portection Domain,保护域)的数量"},
                           {"MetricName": "MemorySwapTotalSpace", "MetricUnit": "Bytes(IEC)", "Dimension": "ResourceID",
                            "Description": "Swap空间总量"},
                           {"MetricName": "MemorySwapFreeSpace", "MetricUnit": "Bytes(IEC)", "Dimension": "ResourceID",
                            "Description": "当前未使用的Swap空间量"},
                           {"MetricName": "MemorySwapUsedSpace", "MetricUnit": "Bytes(IEC)", "Dimension": "ResourceID",
                            "Description": "当前已使用的Swap空间量"},
                           {"MetricName": "MemorySwapUsedUtilization", "MetricUnit": "Percent",
                            "Dimension": "ResourceID", "Description": "当前已使用的Swap空间百分比"}]},
                       {"Namespace": "VCM_ECS", "SubNamespace": "MLU", "Metrics": [
                           {"MetricName": "MLUPhysicalMemoryUtilization", "MetricUnit": "Percent",
                            "Dimension": "ResourceID,DeviceName", "Description": "NPU C1维度NPU C1使用率"},
                           {"MetricName": "MLUCoreAvgUtilization", "MetricUnit": "Percent",
                            "Dimension": "ResourceID,DeviceName", "Description": "NPU C1 AI Core使用率"},
                           {"MetricName": "MLUChipTemperature", "MetricUnit": "℃", "Dimension": "ResourceID,DeviceName",
                            "Description": "NPU C1温度"},
                           {"MetricName": "MLUPowerUsage", "MetricUnit": "W", "Dimension": "ResourceID,DeviceName",
                            "Description": "NPU维度NPU C1卡的功率"},
                           {"MetricName": "MLULinkRxByte", "MetricUnit": "Bits/Second(IEC)",
                            "Dimension": "ResourceID,DeviceName",
                            "Description": "NPU维度NPU C1 RDMA网络每秒接收数据量"},
                           {"MetricName": "MLULinkTxByte", "MetricUnit": "Bits/Second(IEC)",
                            "Dimension": "ResourceID,DeviceName",
                            "Description": "NPU维度NPU C1 RDMA网络每秒发送数据量"},
                           {"MetricName": "MLULinkTxPackets", "MetricUnit": "Packet/Second",
                            "Dimension": "ResourceID,DeviceName", "Description": "NPU维度NPU C1 RDMA出方向包数量"},
                           {"MetricName": "MLULinkRxPackets", "MetricUnit": "Packet/Second",
                            "Dimension": "ResourceID,DeviceName", "Description": "NPU维度NPU C1 RDMA网络接收包数量"}]},
                       {"Namespace": "VCM_ECS", "SubNamespace": "NPU", "Metrics": [
                           {"MetricName": "NpuHBMUtilization", "MetricUnit": "Percent", "Dimension": "ResourceID,NpuId",
                            "Description": "NPU维度NPU使用率"},
                           {"MetricName": "NpuAiCoreUtilization", "MetricUnit": "Percent",
                            "Dimension": "ResourceID,NpuId", "Description": "NPU维度AI Core使用率"},
                           {"MetricName": "NpuTemperature", "MetricUnit": "℃", "Dimension": "ResourceID,NpuId",
                            "Description": "NPU维度NPU温度"},
                           {"MetricName": "NpuPower", "MetricUnit": "W", "Dimension": "ResourceID,NpuId",
                            "Description": "NPU维度NPU功率"},
                           {"MetricName": "NpuRxBandwidth", "MetricUnit": "Bits/Second(IEC)",
                            "Dimension": "ResourceID,NpuId", "Description": "NPU维度RDMA网络每秒接收数据量"},
                           {"MetricName": "NpuTxBandwidth", "MetricUnit": "Bits/Second(IEC)",
                            "Dimension": "ResourceID,NpuId", "Description": "NPU维度RDMA网络每秒发送数据量"},
                           {"MetricName": "NpuRoCeTxAllPktNum", "MetricUnit": "Packet/Second",
                            "Dimension": "ResourceID,NpuId", "Description": "NPU维度RDMA出方向包数量"},
                           {"MetricName": "NpuRoCeRxAllPktNum", "MetricUnit": "Packet/Second",
                            "Dimension": "ResourceID,NpuId", "Description": "NPU维度RDMA入方向包数量"}]},
                       {"Namespace": "VCM_ECS", "SubNamespace": "RDMA", "Metrics": [
                           {"MetricName": "PortRDMARxBits", "MetricUnit": "Bits/Second(IEC)",
                            "Dimension": "ResourceID,NetName", "Description": "RDMA维度每秒接收数据量"},
                           {"MetricName": "PortRDMATxBits", "MetricUnit": "Bits/Second(IEC)",
                            "Dimension": "ResourceID,NetName", "Description": "RDMA维度每秒发送数据量"},
                           {"MetricName": "PortRxCnpHandledPackets", "MetricUnit": "Count",
                            "Dimension": "ResourceID,NetName",
                            "Description": "(接收方向)RDMA维度60s内网卡处理的CNP报文数量"},
                           {"MetricName": "PortRxEcnReceivedPackets", "MetricUnit": "Count",
                            "Dimension": "ResourceID,NetName",
                            "Description": "(接收方向)RDMA维度60s内网卡收到的ECN标记报文数量"},
                           {"MetricName": "PortRxCnpIgnoredPackets", "MetricUnit": "Count",
                            "Dimension": "ResourceID,NetName",
                            "Description": "(接收方向)RDMA维度60s内网卡忽略的CNP报文数量"},
                           {"MetricName": "PortTxCnpSendPackets", "MetricUnit": "Count",
                            "Dimension": "ResourceID,NetName",
                            "Description": "(发送方向)RDMA维度60s内网卡发出的CNP报文数量"},
                           {"MetricName": "PortTxAckTimeoutTimes", "MetricUnit": "Count",
                            "Dimension": "ResourceID,NetName", "Description": "RDMA维度发送端超时次数"},
                           {"MetricName": "PortRxOutOfSequenceTimes", "MetricUnit": "Count",
                            "Dimension": "ResourceID,NetName", "Description": "RDMA维度接收端乱序次数"},
                           {"MetricName": "PortTxOutOfSequenceTimes", "MetricUnit": "Count",
                            "Dimension": "ResourceID,NetName", "Description": "RDMA维度发送端乱序次数"},
                           {"MetricName": "PortReadRespOutOfSequenceTimes", "MetricUnit": "Count",
                            "Dimension": "ResourceID,NetName", "Description": "RDMA维度Read Response乱序次数"},
                           {"MetricName": "FiveTupleQpNums", "MetricUnit": "Count", "Dimension": "ResourceID,NetName",
                            "Description": "RDMA维度QP(Queue Pair,队列结构)的数量"},
                           {"MetricName": "PortRDMARxPackets", "MetricUnit": "Packet/Second",
                            "Dimension": "ResourceID,NetName", "Description": "RDMA入方向包数量"},
                           {"MetricName": "PortRDMATxPackets", "MetricUnit": "Packet/Second",
                            "Dimension": "ResourceID,NetName", "Description": "RDMA出方向包数量"},
                           {"MetricName": "PortRDMARxPausePackets", "MetricUnit": "Packet/Second",
                            "Dimension": "ResourceID,NetName", "Description": "RDMA入方向pause帧的数量"},
                           {"MetricName": "PortRDMATxPausePackets", "MetricUnit": "Packet/Second",
                            "Dimension": "ResourceID,NetName", "Description": "RDMA出方向pause帧的数量"},
                           {"MetricName": "PortRDMARxPauseDuration", "MetricUnit": "Microsecond",
                            "Dimension": "ResourceID,NetName", "Description": "RDMA入方向pause帧持续的时间"},
                           {"MetricName": "PortRDMATxPauseDuration", "MetricUnit": "Microsecond",
                            "Dimension": "ResourceID,NetName", "Description": "RDMA出方向pause帧持续的时间"},
                           {"MetricName": "PortvRDMAMrCount", "MetricUnit": "Count", "Dimension": "ResourceID,NetName",
                            "Description": "实例RDMA维度MR(Memory Region,内存块) 的数量"},
                           {"MetricName": "PortvRDMACqCount", "MetricUnit": "Count", "Dimension": "ResourceID,NetName",
                            "Description": "VRDMA维度CQ(CompletionQueue,完成队列)的数量"},
                           {"MetricName": "PortvRDMAQpCount", "MetricUnit": "Count", "Dimension": "ResourceID,NetName",
                            "Description": "VRDMA维度QP(Queue Pair,队列结构)的数量"},
                           {"MetricName": "PortvRDMAPdCount", "MetricUnit": "Count", "Dimension": "ResourceID,NetName",
                            "Description": "VRDMA维度PD(Portection Domain,保护域)的数量"}]},
                       {"Namespace": "VCM_ECS", "SubNamespace": "Storage", "Metrics": [
                           {"MetricName": "DiskUsageUtilization", "MetricUnit": "Percent",
                            "Dimension": "ResourceID,DiskName", "Description": "磁盘已用容量占总容量比例"},
                           {"MetricName": "DiskUsageAvail", "MetricUnit": "Bytes(SI)",
                            "Dimension": "ResourceID,DiskName", "Description": "磁盘可用容量"},
                           {"MetricName": "DiskReadBytes", "MetricUnit": "Bytes/Second(SI)",
                            "Dimension": "ResourceID,DiskName", "Description": "磁盘每秒读取字节数"},
                           {"MetricName": "DiskWriteBytes", "MetricUnit": "Bytes/Second(SI)",
                            "Dimension": "ResourceID,DiskName", "Description": "磁盘每秒写入字节数"},
                           {"MetricName": "DiskReadIOPS", "MetricUnit": "Count/Second",
                            "Dimension": "ResourceID,DiskName", "Description": "磁盘每秒读取的IOPS数"},
                           {"MetricName": "DiskWriteIOPS", "MetricUnit": "Count/Second",
                            "Dimension": "ResourceID,DiskName", "Description": "磁盘每秒写入的IOPS数"}]}])