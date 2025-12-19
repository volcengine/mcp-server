from src.iot.api.api import IotAPI
from mcp.server.fastmcp import FastMCP
from .note import note
import json


def create_mcp_server():
    service = IotAPI()
    mcp = FastMCP(
        "IoT MCP Server",
        instructions="火山引擎物联网平台 MCP 服务",
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
    def call_service(params: dict, body: dict) -> str:
        """
        向设备主动发起调用服务
        Call steps:
        1. Pass "call_service" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  call_service
        """
        reqs = service.mcp_post("McpCallService", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def get_all_last_device_property_value(params: dict, body: dict) -> str:
        """
        获取所有模块，所有属性的最新上报值
        Call steps:
        1. Pass "get_all_last_device_property_value" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_all_last_device_property_value
        """
        reqs = service.mcp_post(
            "McpGetAllLastDevicePropertyValue", params, json.dumps(body)
        )

        return reqs

    @mcp.tool()
    def get_custom_topic_list(params: dict, body: dict) -> str:
        """
        查询自定义Topic列表
        Call steps:
        1. Pass "get_custom_topic_list" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_custom_topic_list
        """
        reqs = service.mcp_post("McpGetCustomTopicList", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def get_device_detail(params: dict, body: dict) -> str:
        """
        根据设备标示查询设备信息
        Call steps:
        1. Pass "get_device_detail" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_device_detail
        """
        reqs = service.mcp_post("McpGetDeviceDetail", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def get_device_event_record_list(params: dict, body: dict) -> str:
        """
        获取设备物模型事件上报记录
        Call steps:
        1. Pass "get_device_event_record_list" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_device_event_record_list
        """
        reqs = service.mcp_post("McpGetDeviceEventRecordList", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def get_device_list(params: dict, body: dict) -> str:
        """
        根据指定条件查询设备列表，比如名称(模糊)、状态、产品、位置(暂不支持)等
        Call steps:
        1. Pass "get_device_list" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_device_list
        """
        reqs = service.mcp_post("McpGetDeviceList", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def get_device_overview(params: dict, body: dict) -> str:
        """
        获取设备总览信息，包括当前有多少设备，多少离线，多少在线，多少未激活，多少禁用
        Call steps:
        1. Pass "get_device_overview" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_device_overview
        """
        reqs = service.mcp_post("McpGetDeviceOverview", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def get_device_status(params: dict, body: dict) -> str:
        """
        设备状态查询，如果有异常默认返回Disable，状态枚举：Online/Offline/NeverConnected/Disable，在线/离线/未激活/禁用
        Call steps:
        1. Pass "get_device_status" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_device_status
        """
        reqs = service.mcp_post("McpGetDeviceStatus", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def get_device_service_call_record_list(params: dict, body: dict) -> str:
        """
        获取设备服务调用记录
        Call steps:
        1. Pass "get_device_service_call_record_list" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_device_service_call_record_list
        """
        reqs = service.mcp_post(
            "McpGetDeviceServiceCallRecordList", params, json.dumps(body)
        )

        return reqs

    @mcp.tool()
    def get_instance_detail(params: dict, body: dict) -> str:
        """
        根据实例ID查询指定实例的详细信息
        Call steps:
        1. Pass "get_instance_detail" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_instance_detail
        """
        reqs = service.mcp_post("McpGetInstanceDetail", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def get_instance_endpoints(params: dict, body: dict) -> str:
        """
        查询实例的开发配置
        Call steps:
        1. Pass "get_instance_endpoints" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_instance_endpoints
        """
        reqs = service.mcp_post("McpGetInstanceEndpoints", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def get_instance_list(params: dict, body: dict) -> str:
        """
        根据指定条件查询是列表，包括名称、状态、实例组信息
        Call steps:
        1. Pass "get_instance_list" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_instance_list
        """
        reqs = service.mcp_post("McpGetInstanceList", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def get_last_device_property_value(params: dict, body: dict) -> str:
        """
        获取单个模块下指定属性的最新上报值
        Call steps:
        1. Pass "get_last_device_property_value" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_last_device_property_value
        """
        reqs = service.mcp_post(
            "McpGetLastDevicePropertyValue", params, json.dumps(body)
        )

        return reqs

    @mcp.tool()
    def get_product_list(params: dict, body: dict) -> str:
        """
        产品列表页查询，包含产品的基本信息
        Call steps:
        1. Pass "get_product_list" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_product_list
        """
        reqs = service.mcp_post("McpGetProductList", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def get_product_detail(params: dict, body: dict) -> str:
        """
        除了基本信息外还会返回物模型、历史版本等数据
        Call steps:
        1. Pass "get_product_detail" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_product_detail
        """
        reqs = service.mcp_post("McpGetProductDetail", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def get_property_values_by_time(params: dict, body: dict) -> str:
        """
        返回指定时间区间内的数值，对于数值型数据支持聚合计算
        Call steps:
        1. Pass "get_property_values_by_time" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_property_values_by_time
        """
        reqs = service.mcp_post("McpGetPropertyValuesByTime", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def get_thing_model(params: dict, body: dict) -> str:
        """
        获取产品当前物模型
        Call steps:
        1. Pass "get_thing_model" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  get_thing_model
        """
        reqs = service.mcp_post("McpGetThingModel", params, json.dumps(body))

        return reqs

    @mcp.tool()
    def set_property(params: dict, body: dict) -> str:
        """
        向设备主动设置属性
        Call steps:
        1. Pass "set_property" as an input parameter to invoke the `get_note` method to obtain the parameter description.
        2. After obtaining the parameter description, invoke  set_property
        """
        reqs = service.mcp_post("McpSetProperty", params, json.dumps(body))

        return reqs

    return mcp
