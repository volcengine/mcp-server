import os
import logging
import argparse
from typing import Any
from mcp.server.fastmcp import FastMCP

from mcp_server_redis.resource.vpc_resource import VpcSDK
from mcp_server_redis.resource.redis_resource import RedisSDK
from mcp_server_redis.params import func_available_params_map

# Initialize the MCP service
mcp_server = FastMCP("redis_mcp_server", port=int(os.getenv("MCP_SERVER_PORT", "8000")),
                     description="Volcengine(火山引擎) Redis(缓存数据库) MCP , 你的缓存数据库管理助手")
redis_resource = RedisSDK(
    region=os.getenv('VOLCENGINE_REGION'), host=os.getenv('VOLCENGINE_ENDPOINT'),
    ak=os.getenv('VOLCENGINE_ACCESS_KEY'), sk=os.getenv('VOLCENGINE_SECRET_KEY')
)
vpc_resource = VpcSDK(
    region=os.getenv('VOLCENGINE_REGION'), host=None,
    ak=os.getenv('VOLCENGINE_ACCESS_KEY'), sk=os.getenv('VOLCENGINE_SECRET_KEY')
)
logger = logging.getLogger("mcp_server_redis")


@mcp_server.tool(
    name="get_available_params",
    description="Query the list of available regional resources for Redis"
)
def get_available_params(func_name: str) -> str:
    """Query the available params for target function name

    Args:
        func_name: function name
    """
    available_func_params = func_available_params_map.get(func_name)
    return f"""
    Position and Role
    
    1. You are a professional Volcano Engine Redis expert who understands Volcano Redis product capabilities and business scenarios, excelling at providing professional technical support services.
    2. To provide the best service, you need to accurately identify and break down user issues, call tools (OpenAPI) to obtain content matching user questions, integrate and analyze the obtained content, and then return it to users.
    3. For questions with unclear intent, you need to confirm with users before starting to process the task.
    4. Respond in the same language as the user's question, for example, if users ask in Chinese, respond in Chinese.
    
    Skill 1: Understanding and Analyzing Problems
    
    1. Need to accurately understand user questions; for unclear questions, need to double-check with users or ask them to describe more clearly.
    2. After understanding the user's question, break down the problem, clarify the steps, commands, and tools needed to solve it, and print out the relevant information.

    Skill 2: Redis MCP Tool Usage
    
    1. After breaking down the problem, call appropriate MCP tools to perform related operations, such as querying instance information, parameter information, business log data, etc.
    2. Able to call multiple tools for operations.
    
    Skill 3: Data Analysis Capability
    
    1. Query Time: Able to accurately understand time concepts in user questions, such as "today", "last week", "this week", and convert these time concepts into specific time ranges based on current time.
    2. Problem Analysis and Anomaly Investigation: If users want to conduct data insights or report business anomalies; need to analyze all metrics, check which metrics have sudden changes/anomalies, such as whitelist exceptions, slow logs, big keys, hot keys, etc. In short, need to think divergently, aggregate analysis, and provide reasonable results.

    The available parameters and values for the function {func_name} to be called are shown below:
    {available_func_params}
    """


@mcp_server.tool(
    name="describe_regions",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Query available regions for Redis instances"
)
def describe_regions(region_id: str = None) -> dict[str, Any]:
    """Query available regions for Redis instances
       Args:
           region_id (str, optional): The region ID. If not specified, returns information about all available regions
                                    for the current account.
    """
    req = {
        "region_id": region_id
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = redis_resource.describe_regions(req)
    return resp.to_dict()


@mcp_server.tool(
    name="describe_zones",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Query the list of available zone resources for Redis in the specified region"
)
def describe_zones(region_id: str) -> dict[str, Any]:
    """Query the list of available zone resources for Redis in the specified region
       Args:
           region_id (str): The region ID. You can call describe_regions to query all available region information for Redis instances.
    """
    req = {
        "region_id": region_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = redis_resource.describe_zones(req)
    return resp.to_dict()


@mcp_server.tool(
    name="describe_vpcs",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Query VPC information"
)
def describe_vpcs(
    vpc_name: str = None,
    project_name: str = None,
    is_default: bool = None,
    vpc_owner_id: int = None,
    page_number: int = 1,
    page_size: int = 20,
    next_token: str = None,
    max_results: int = 10
) -> dict[str, Any]:
    """Query VPC information
       Args:
           vpc_name (str, optional): The VPC name.
           project_name (str, optional): The project name that VPC belongs to.
           is_default (bool, optional): Whether the VPC is default VPC.
                                      True: System auto-created VPC for ECS instances
                                      False: User manually created VPC
           vpc_owner_id (int, optional): The ID of main account that owns the VPC.
           page_number (int, optional): The page number, starting from 1. Default: 1.
                                      Note: This parameter will be deprecated,
                                      use next_token and max_results instead.
           page_size (int, optional): The number of records per page.
                                    Range: 1-100, Default: 20.
                                    Note: This parameter will be deprecated,
                                    use next_token and max_results instead.
           next_token (str, optional): The pagination token.
                                     Leave empty to query from beginning.
                                     Use token from previous response to continue query.
           max_results (int, optional): The number of records to return.
                                      Range: 1-100, Default: 10.
    """
    req = {
        "vpc_name": vpc_name,
        "project_name": project_name,
        "is_default": is_default,
        "vpc_owner_id": vpc_owner_id,
        "page_number": page_number,
        "page_size": page_size,
        "next_token": next_token,
        "max_results": max_results
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vpc_resource.describe_vpcs(req)
    return resp.to_dict()


@mcp_server.tool(
    name="describe_subnets",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Query subnet information"
)
def describe_subnets(
    zone_id: str = None,
    vpc_id: str = None,
    subnet_name: str = None,
    subnet_owner_id: str = None,
    route_table_id: str = None,
    project_name: str = None,
    is_default: bool = None,
    page_number: int = 1,
    page_size: int = 20,
    next_token: str = None,
    max_results: int = 10
) -> dict[str, Any]:
    """Query subnet information
       Args:
           zone_id (str, optional): The availability zone ID.
           vpc_id (str, optional): The VPC ID.
                                 You can call describe_vpcs to query VPC information.
           subnet_name (str, optional): The subnet name.
           subnet_owner_id (str, optional): The ID of account that owns the subnet.
           route_table_id (str, optional): The route table ID.
           project_name (str, optional): The project name that subnet belongs to.
                                       Default: 'default'
           is_default (bool, optional): Whether the subnet is default subnet.
                                      True: System auto-created subnet
                                      False: User manually created subnet
           page_number (int, optional): The page number, starting from 1. Default: 1.
                                      Note: This parameter will be deprecated,
                                      use next_token and max_results instead.
           page_size (int, optional): The number of records per page.
                                    Range: 1-100, Default: 20.
                                    Note: This parameter will be deprecated,
                                    use next_token and max_results instead.
           next_token (str, optional): The pagination token.
                                     Leave empty to query from beginning.
                                     Use token from previous response to continue query.
           max_results (int, optional): The number of records to return.
                                      Range: 1-100, Default: 10.
    """
    req = {
        "zone_id": zone_id,
        "vpc_id": vpc_id,
        "subnet_name": subnet_name,
        "subnet_owner_id": subnet_owner_id,
        "route_table_id": route_table_id,
        "project_name": project_name,
        "is_default": is_default,
        "page_number": page_number,
        "page_size": page_size,
        "next_token": next_token,
        "max_results": max_results
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vpc_resource.describe_subnets(req)
    return resp.to_dict()


@mcp_server.tool(
    name="describe_db_instances",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Query basic information of Redis instances"
)
def describe_db_instances(
    region_id: str = None,
    page_number: int = 1,
    page_size: int = 10,
    zone_id: str = None,
    instance_id: str = None,
    instance_name: str = None,
    sharded_cluster: int = None,
    status: str = None,
    engine_version: str = None,
    vpc_id: str = None,
    charge_type: str = None,
    tag_filters: list[dict[str, str]] = None,
    project_name: str = None,
    service_type: str = "Basic",
    data_layout: str = None
) -> dict[str, Any]:
    """Query basic information of Redis instances
       Args:
           region_id (str, optional): The region ID.
                                    If not specified, uses the region from signature.
                                    Call DescribeRegions to query available regions.
           page_number (int, optional): The page number, starting from 1. Default: 1.
           page_size (int, optional): The number of records per page, range: 1-1000. Default: 10.
           zone_id (str, optional): The availability zone ID (supports fuzzy search).
                                  Call DescribeZones to query available zones.
           instance_id (str, optional): The instance ID (exact match).
           instance_name (str, optional): The instance name (supports fuzzy search).
           sharded_cluster (int, optional): Whether sharding is enabled.
                                          Values: 0 (disabled), 1 (enabled)
           status (str, optional): The instance status.
           engine_version (str, optional): The database version.
                                         Values: '5.0', '6.0', '7.0'
           vpc_id (str, optional): The VPC ID (supports fuzzy search).
                                 Call DescribeVpcs to query VPC information.
           charge_type (str, optional): The billing method.
                                      Values: 'PostPaid' (pay-as-you-go),
                                             'PrePaid' (subscription)
           tag_filters (list[dict], optional): List of tag filters. Each dict contains:
                                             - 'Key' (str): Tag key (required)
                                             - 'Value' (str, optional): Tag value
                                             Max 10 tag pairs.
                                             Empty value means no restriction on tag value.
           project_name (str, optional): The project name.
           service_type (str, optional): The service type.
                                       Values: 'Basic' (default, community edition),
                                              'Enterprise' (enterprise edition)
           data_layout (str, optional): The data storage format.
                                      Only meaningful for enterprise edition.
                                      Fixed as 'RAM' for community edition.
    """
    req = {
        "region_id": region_id,
        "page_number": page_number,
        "page_size": page_size,
        "zone_id": zone_id,
        "instance_id": instance_id,
        "instance_name": instance_name,
        "sharded_cluster": sharded_cluster,
        "status": status,
        "engine_version": engine_version,
        "vpc_id": vpc_id,
        "charge_type": charge_type,
        "tag_filters": tag_filters,
        "project_name": project_name,
        "service_type": service_type,
        "data_layout": data_layout
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = redis_resource.describe_db_instances(req)
    return resp.to_dict()


@mcp_server.tool(
    name="describe_db_instance_detail",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Query the details of an Redis instance"
)
def describe_db_instance_detail(instance_id: str) -> dict[str, Any]:
    """Query the details of a Redis instance
       Args:
           instance_id (str): The instance ID
   """
    req = {
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = redis_resource.describe_db_instance_detail(req)
    return resp.to_dict()


@mcp_server.tool(
    name="describe_db_instance_specs",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Query the list of instance specifications supported by Redis"
)
def describe_db_instance_specs(arch_type: str = None, instance_class: str = None) -> dict[str, Any]:
    """Query the list of instance specifications supported by Redis
       Args:
           arch_type (str, optional): The architecture type of Redis instance.
                                    Values: 'Cluster' (enabled sharding), 'Standard' (disabled sharding)
           instance_class (str, optional): The instance class type.
                                         Values: 'PrimarySecondary' (master-slave), 'Standalone' (single node)
    """
    req = {
        "arch_type": arch_type,
        "instance_class": instance_class,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = redis_resource.describe_db_instance_specs(req)
    return resp.to_dict()


@mcp_server.tool(
    name="describe_slow_logs",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Query slow log details of the target Redis instance within specified time period"
)
def describe_slow_logs(
    instance_id: str,
    page_size: int,
    node_ids: list[str] = None,
    slow_log_type: str = None,
    query_start_time: str = None,
    query_end_time: str = None,
    db_name: str = None,
    context: str = None
) -> dict[str, Any]:
    """Query slow log details of the target Redis instance within specified time period
       Args:
           instance_id (str): The instance ID. You can call describe_db_instances to query basic information of all Redis instances.
           page_size (int): The number of records per page, range: 1-1000.
           node_ids (list[str], optional): The node IDs to query slow logs.
                                         If not specified, queries slow logs of all nodes.
                                         Multiple node IDs should be separated by commas.
                                         Total length should not exceed 1024 bytes, recommended no more than 8 nodes.
           slow_log_type (str, optional): The type of slow log.
                                        Values: 'Server' (Server node slow log), 'Proxy' (Proxy node slow log).
                                        If not specified, returns slow logs of all node types.
           query_start_time (str, optional): The start time of the query in format yyyy-MM-ddTHH:mm:ssZ (UTC).
                                           If not specified, defaults to 3 days before current time.
           query_end_time (str, optional): The end time of the query in format yyyy-MM-ddTHH:mm:ssZ (UTC).
                                         If not specified, defaults to current time.
                                         Must be later than query_start_time.
           db_name (str, optional): The database where slow logs are located.
                                  For Proxy node: integers between 0-256
                                  For Server node: only '-' is supported
                                  If not specified, returns slow logs from all databases.
           context (str, optional): The context for pagination.
                                  Used when loading more slow log records based on ListOver value in response.
    """
    req = {
        "instance_id": instance_id,
        "page_size": page_size,
        "node_ids": node_ids,
        "slow_log_type": slow_log_type,
        "query_start_time": query_start_time,
        "query_end_time": query_end_time,
        "db_name": db_name,
        "context": context
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = redis_resource.describe_slow_logs(req)
    return resp.to_dict()


@mcp_server.tool(
    name="describe_hot_keys",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Query hot key details of the target Redis instance within specified time period"
)
def describe_hot_keys(
    instance_id: str,
    page_size: int,
    query_start_time: str = None,
    query_end_time: str = None,
    key_type: str = None,
    shard_ids: list[str] = None
) -> dict[str, Any]:
    """Query hot key details of the target Redis instance within specified time period
       Args:
           instance_id (str): The instance ID.
                             You can call DescribeDBInstances to query basic information of all Redis instances.
           page_size (int): The number of records per page, range: 1-1000.
           query_start_time (str, optional): The start time of the query in format yyyy-MM-ddTHH:mm:ssZ (UTC).
                                           If not specified, defaults to 1 hour before current time.
                                           Can query up to 15 days of historical data.
           query_end_time (str, optional): The end time of the query in format yyyy-MM-ddTHH:mm:ssZ (UTC).
                                         If not specified, defaults to current time.
                                         Must be later than query_start_time.
                                         Time interval cannot exceed 15 days.
           key_type (str, optional): The data type to filter hot keys.
                                   Values: 'string', 'list', 'set', 'zset', 'hash'
                                   If not specified, no filtering by data type.
           shard_ids (list[str], optional): The list of shard IDs to filter results.
                                          Maximum 40 shard IDs, separated by commas.
                                          If not specified, no filtering by shard ID.
                                          You can call DescribeDBInstanceShards to query shard details.
    """
    req = {
        "instance_id": instance_id,
        "page_size": page_size,
        "query_start_time": query_start_time,
        "query_end_time": query_end_time,
        "key_type": key_type,
        "shard_ids": shard_ids
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = redis_resource.describe_hot_keys(req)
    return resp.to_dict()


@mcp_server.tool(
    name="describe_big_keys",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Query big key details of the target Redis instance within specified time period"
)
def describe_big_keys(
    instance_id: str,
    page_size: int,
    query_start_time: str = None,
    query_end_time: str = None,
    key_type: str = None,
    order_by: str = None
) -> dict[str, Any]:
    """Query big key details of the target Redis instance within specified time period
       Args:
           instance_id (str): The instance ID.
                             You can call DescribeDBInstances to query basic information of all Redis instances.
           page_size (int): The number of records per page, range: 1-100.
           query_start_time (str, optional): The start time of the query in format yyyy-MM-ddTHH:mm:ssZ (UTC).
                                           If not specified, defaults to 24 hours before current time.
                                           Can query up to 15 days of historical data.
                                           Time interval cannot exceed 24 hours.
           query_end_time (str, optional): The end time of the query in format yyyy-MM-ddTHH:mm:ssZ (UTC).
                                         If not specified, defaults to current time.
                                         Must be later than query_start_time.
                                         Time interval cannot exceed 24 hours.
           key_type (str, optional): The data type to filter big keys.
                                   Values: 'string', 'list', 'set', 'zset', 'hash'
                                   If not specified, no filtering by data type.
           order_by (str, optional): The sorting condition for query results.
                                   Values: 'ValueSize' (sort by memory usage, default),
                                          'ValueLen' (sort by number of elements)
    """
    req = {
        "instance_id": instance_id,
        "page_size": page_size,
        "query_start_time": query_start_time,
        "query_end_time": query_end_time,
        "key_type": key_type,
        "order_by": order_by
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = redis_resource.describe_big_keys(req)
    return resp.to_dict()


@mcp_server.tool(
    name="describe_backups",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Query the backup set list of Redis instances"
)
def describe_backups(
    scope: str = "OneInstance",
    instance_id: str = None,
    start_time: str = None,
    end_time: str = None,
    backup_strategy_list: list[str] = None,
    backup_point_name: str = None,
    project_name: str = None,
    page_size: int = None,
    page_number: int = None,
    backup_point_id: str = None
) -> dict[str, Any]:
    """Query the backup set list of Redis instances
       Args:
           scope (str, optional): The backup query scope.
                                Values: 'OneInstance' (default, query single instance),
                                       'AccountInstances' (query current account)
           instance_id (str, optional): The instance ID.
                                      Required when scope is 'OneInstance'.
                                      You can call DescribeDBInstances to query instance information.
           start_time (str, optional): The start time in format yyyy-MM-ddTHH:mm:ssZ (UTC).
                                     If specified, end_time is required.
           end_time (str, optional): The end time in format yyyy-MM-ddTHH:mm:ssZ (UTC).
                                   Required if start_time is specified.
                                   Must be later than start_time.
           backup_strategy_list (list[str], optional): The list of backup strategies.
                                                     Values: 'ManualBackup', 'AutomatedBackup'
                                                     Multiple strategies separated by commas.
           backup_point_name (str, optional): The backup name (supports fuzzy search).
                                            Only effective when scope is 'AccountInstances'.
           project_name (str, optional): The project name of the backup.
                                       Only effective when scope is 'AccountInstances'.
           page_size (int, optional): The number of records per page, range: 1-1000.
                                    Required if page_number is specified.
           page_number (int, optional): The page number, starting from 1.
                                      Required if page_size is specified.
           backup_point_id (str, optional): The backup ID (supports fuzzy search).
                                          Only effective when scope is 'AccountInstances'.
    """
    req = {
        "scope": scope,
        "instance_id": instance_id,
        "start_time": start_time,
        "end_time": end_time,
        "backup_strategy_list": backup_strategy_list,
        "backup_point_name": backup_point_name,
        "project_name": project_name,
        "page_size": page_size,
        "page_number": page_number,
        "backup_point_id": backup_point_id
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = redis_resource.describe_backups(req)
    return resp.to_dict()


@mcp_server.tool(
    name="describe_db_instance_params",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Query the list of parameters supported by the target Redis instance"
)
def describe_db_instance_params(
    instance_id: str,
    page_number: int,
    page_size: int
) -> dict[str, Any]:
    """Query the list of parameters supported by the target Redis instance
       Args:
           instance_id (str): The instance ID.
                             You can call describe_db_instances to query basic information of all Redis instances.
           page_number (int): The page number of parameter list, starting from 1.
                             Must not exceed the maximum value of Integer type.
           page_size (int): The number of records per page, range: 1-1000.
    """
    req = {
        "instance_id": instance_id,
        "page_number": page_number,
        "page_size": page_size
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = redis_resource.describe_db_instance_params(req)
    return resp.to_dict()


@mcp_server.tool(
    name="describe_parameter_groups",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Query the basic information of parameter templates under the current account and region"
)
def describe_parameter_groups(
    page_number: int,
    page_size: int,
    engine_version: str = None,
    source: str = None
) -> dict[str, Any]:
    """Query the basic information of parameter templates under the current account and region
       Args:
           page_number (int): The page number of parameter template list, starting from 1.
                             Must not exceed the maximum value of Integer type.
           page_size (int): The number of records per page, range: 1-100.
           engine_version (str, optional): The Redis database version for the parameter template.
                                         Values: '7.0' (Redis 7.0), '6.0' (Redis 6.0), '5.0' (Redis 5.0)
           source (str, optional): The source of parameter template creation.
                                 Values: 'User' (user-created custom template),
                                        'System' (system-created template)
    """
    req = {
        "page_number": page_number,
        "page_size": page_size,
        "engine_version": engine_version,
        "source": source
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = redis_resource.describe_parameter_groups(req)
    return resp.to_dict()


@mcp_server.tool(
    name="describe_parameter_group_detail",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Query detailed information of the target parameter template"
)
def describe_parameter_group_detail(parameter_group_id: str) -> dict[str, Any]:
    """Query detailed information of the target parameter template
       Args:
           parameter_group_id (str): The parameter template ID.
                                   You can call describe_parameter_groups to query basic information
                                   of all parameter templates under the current account and region.
    """
    req = {
        "parameter_group_id": parameter_group_id
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = redis_resource.describe_parameter_group_detail(req)
    return resp.to_dict()


@mcp_server.tool(
    name="describe_allow_lists",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Query the IP whitelist list in the specified region"
)
def describe_allow_lists(
    region_id: str,
    instance_id: str = None,
    query_default: bool = None,
    ip_address: list[str] = None,
    ip_segment: list[str] = None,
    project_name: str = None
) -> dict[str, Any]:
    """Query the IP whitelist list in the specified region
       Args:
           region_id (str): The region ID.
                           You can call describe_regions to query all available region information.
           instance_id (str, optional): The instance ID.
                                      You can call describe_db_instances to query instance information.
           query_default (bool, optional): Whether to query only default whitelists.
                                         Values: True (query only default whitelists),
                                                False (query only normal whitelists)
                                         If not specified, returns all types of whitelists.
           ip_address (list[str], optional): Filter whitelists by IP addresses.
                                           Matches exact IP addresses and IP segments containing these addresses.
                                           Maximum 50 IP addresses, separated by commas.
           ip_segment (list[str], optional): Filter whitelists by IP segments.
                                           Matches exact IP segments.
                                           Maximum 50 IP segments, separated by commas.
           project_name (str, optional): The project name of the whitelist.
    """
    req = {
        "region_id": region_id,
        "instance_id": instance_id,
        "query_default": query_default,
        "ip_address": ip_address,
        "ip_segment": ip_segment,
        "project_name": project_name
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = redis_resource.describe_allow_lists(req)
    return resp.to_dict()


@mcp_server.tool(
    name="describe_allow_list_detail",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Query detailed information of the target whitelist"
)
def describe_allow_list_detail(allow_list_id: str) -> dict[str, Any]:
    """Query detailed information of the target whitelist
       Args:
           allow_list_id (str): The whitelist ID.
                               You can call describe_allow_lists to query all whitelist information
                               under the current account in the specified region.
    """
    req = {
        "allow_list_id": allow_list_id
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = redis_resource.describe_allow_list_detail(req)
    return resp.to_dict()


@mcp_server.tool(
    name="list_db_account",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Query account information in Redis instance"
)
def list_db_account(instance_id: str, account_name: str = None) -> dict[str, Any]:
    """Query account information in Redis instance
       Args:
           instance_id (str): The instance ID.
                             You can call describe_db_instances to query basic information
                             of all Redis instances.
           account_name (str, optional): The account name.
                                       If not specified, no filtering by account name.
    """
    req = {
        "instance_id": instance_id,
        "account_name": account_name
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = redis_resource.list_db_account(req)
    return resp.to_dict()


@mcp_server.tool(
    name="create_db_instance",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Create a Redis instance"
)
def create_db_instance(
    region_id: str,
    engine_version: str,
    sharded_cluster: int,
    node_number: int,
    shard_capacity: int,
    multi_az: str,
    configure_nodes: list[dict],
    vpc_id: str,
    subnet_id: str,
    shard_number: int = None,
    instance_name: str = None,
    password: str = None,
    port: int = 6379,
    project_name: str = "default",
    allow_list_ids: list[str] = None,
    tags: list[dict[str, str]] = None,
    charge_type: str = "PostPaid",
    purchase_months: int = None,
    auto_renew: bool = False,
    deletion_protection: str = "disabled",
    no_auth_mode: str = "close",
    parameter_group_id: str = None,
    client_token: str = None
) -> dict[str, Any]:
    """Create a Redis instance
       Args:
           region_id (str): The region ID.
                           You can call DescribeRegions to query available regions.
           engine_version (str): Redis version.
                               Values: '5.0', '6.0', '7.0'
           sharded_cluster (int): Whether to enable sharding cluster.
                                Values:
                                - 0: disabled
                                - 1: enabled
                                See product architecture documentation for details.
           node_number (int): Number of nodes per shard.
                            Range: 1-6
                            Note:
                            - Default quota: 4 nodes of 256MiB per region
                            - Node=1: single node instance
                            - Node>1: master-replica instance
                            See feature differences documentation.
           shard_capacity (int): Memory capacity per shard in MiB.
                               Without sharding (sharded_cluster=0):
                               [256,512,1024,2048,4096,8192,16384,32768,24576,65536]
                               With sharding (sharded_cluster=1):
                               [1024,2048,4096,8192,16384]
                               Note: 256MiB not available for single node instances.
           multi_az (str): Availability zone deployment type.
                          Values:
                          - 'disabled': single zone
                          - 'enabled': multi zone
                          Note: Must be 'disabled' for single node instances.
           configure_nodes (list[dict]): Node zone configuration list.
                           Format depends on node_number and multi_az:
                           1. For single node (node_number=1):
                              multi_az must be 'disabled'
                              Example:
                              {
                                  "NodeNumber": 1,
                                  "MultiAZ": "disabled",
                                  "ConfigureNodes": [
                                      {
                                          "AZ": "cn-beijing-a"
                                      }
                                  ]
                              }

                           2. For master-replica (node_number>=2):
                              With multi_az='enabled':
                              - Must specify different zones for nodes
                              - Number of configure_nodes must match node_number
                              Example for 3 nodes across zones A and C:
                              {
                                  "NodeNumber": 3,
                                  "MultiAZ": "enabled",
                                  "ConfigureNodes": [
                                      {
                                          "AZ": "cn-beijing-a"
                                      },
                                      {
                                          "AZ": "cn-beijing-c"
                                      },
                                      {
                                          "AZ": "cn-beijing-c"
                                      }
                                  ]
                              }

                              With multi_az='disabled':
                              - All nodes must be in same zone
                              - Number of configure_nodes must match node_number
                              Example for 3 nodes in same zone:
                              {
                                  "NodeNumber": 3,
                                  "MultiAZ": "disabled",
                                  "ConfigureNodes": [
                                      {
                                          "AZ": "cn-beijing-a"
                                      },
                                      {
                                          "AZ": "cn-beijing-a"
                                      },
                                      {
                                          "AZ": "cn-beijing-a"
                                      }
                                  ]
                              }

                           Note:
                           - You can call describe_zones to query available zones
                           - AZ format must match the zone ID format, e.g. "cn-beijing-a"

           vpc_id (str): The VPC ID.
                        Recommend using same VPC as target ECS instances.
                        You can call describe_vpcs to query VPCs.
           subnet_id (str): The subnet ID.
                          Must be in same zone as instance.
                          You can call describe_subnets to query subnets.
           shard_number (int, optional): Number of shards.
                                       Range: 2-256
                                       Required when sharded_cluster=1
           instance_name (str, optional): Instance name.
                                        Rules:
                                        - Cannot start with number or hyphen
                                        - Can contain Chinese chars, letters, numbers, underscore, hyphen
                                        - Length: 1-128 chars
                                        Default: instance ID
           password (str, optional): Password for default account.
                                   Rules:
                                   - Length: 8-32 chars
                                   - Must contain 2 types from: upper/lower/digits/special
                                   - Special chars: ()`~!@#$%^&*-+=_|{}[];<>,.?
                                   Default: random password
           port (int, optional): Private network port.
                               Range: 1024-65535
                               Default: 6379
           project_name (str, optional): Project name.
                                       Default: 'default'
           allow_list_ids (list[str], optional): List of whitelist IDs.
                                               Max 100 whitelists per instance.
                                               Max 1000 IPs/CIDRs total.
           tags (list[dict], optional): List of tags.
                                      Each dict:
                                      - 'Key' (str, required): tag key
                                      - 'Value' (str, optional): tag value
                                      Max 20 tags per request.
                                      Max 50 tags per instance.
           charge_type (str, optional): Billing method.
                                      Values:
                                      - 'PostPaid': pay-as-you-go (default)
                                      - 'PrePaid': subscription
           purchase_months (int, optional): Subscription period in months.
                                         Monthly: [1-9]
                                         Yearly: [12,24,36]
                                         Required for PrePaid
           auto_renew (bool, optional): Enable auto-renewal.
                                      Default: False
                                      Only valid for PrePaid
           deletion_protection (str, optional): Instance deletion protection.
                                              Values:
                                              - 'disabled': off (default)
                                              - 'enabled': on
           no_auth_mode (str, optional): Password-free access.
                                       Values:
                                       - 'close': disabled (default)
                                       - 'open': enabled
                                       Case insensitive
           parameter_group_id (str, optional): Parameter template ID.
                                             Default: system template for engine version
           client_token (str, optional): Idempotency token.
                                       Max 127 ASCII chars.
                                       Must be unique between requests.
    """
    req = {
        "region_id": region_id,
        "engine_version": engine_version,
        "sharded_cluster": sharded_cluster,
        "node_number": node_number,
        "shard_capacity": shard_capacity,
        "multi_az": multi_az,
        "configure_nodes": configure_nodes,
        "vpc_id": vpc_id,
        "subnet_id": subnet_id,
        "shard_number": shard_number,
        "instance_name": instance_name,
        "password": password,
        "port": port,
        "project_name": project_name,
        "allow_list_ids": allow_list_ids,
        "tags": tags,
        "charge_type": charge_type,
        "purchase_months": purchase_months,
        "auto_renew": auto_renew,
        "deletion_protection": deletion_protection,
        "no_auth_mode": no_auth_mode,
        "parameter_group_id": parameter_group_id,
        "client_token": client_token
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = redis_resource.create_db_instance(req)
    return resp.to_dict()


@mcp_server.tool(
    name="modify_db_instance_params",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Modify parameter configurations of the target Redis instance"
)
def modify_db_instance_params(
    instance_id: str,
    param_values: list[dict[str, str]],
    client_token: str = None
) -> dict[str, Any]:
    """Modify parameter configurations of the target Redis instance
       Args:
           instance_id (str): The instance ID.
                             You can call describe_db_instances to query basic information
                             of all Redis instances.
           param_values (list[dict]): List of parameter configurations to modify.
                                    Each dict contains:
                                    - 'Name' (str): Parameter name
                                    - 'Value' (str): Parameter value
                                    You can call describe_db_instance_params to query supported
                                    parameters and their valid values.
           client_token (str, optional): Idempotency token, max 127 ASCII chars.
                                       Must be unique between different requests.
    """
    req = {
        "instance_id": instance_id,
        "param_values": param_values,
        "client_token": client_token
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = redis_resource.modify_db_instance_params(req)
    if resp is None or (isinstance(resp, dict) and len(resp) == 0):
        return {
            "result": "please call describe_db_instance_params to check params!",
        }
    return resp.to_dict()


@mcp_server.tool(
    name="create_db_account",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Create an account for the target Redis instance"
)
def create_db_account(
    instance_id: str,
    account_name: str,
    role_name: str,
    password: str,
    description: str = None,
    client_token: str = None
) -> dict[str, Any]:
    """Create an account for the target Redis instance
       Args:
           instance_id (str): The instance ID.
                             You can call describe_db_instances to query basic information
                             of all Redis instances.
           account_name (str): The account name.
                              Requirements:
                              - Start with lowercase letter
                              - End with lowercase letter or number
                              - Length: 2-16 characters
                              - Can contain lowercase letters, numbers, underscore(_)
           role_name (str): The role name. Available roles:
                           - 'Administrator': Allow all commands on all keys
                           - 'ReadWrite': Allow all non-admin commands on all keys
                           - 'ReadOnly': Allow all read commands on all keys
                           - 'NotDangerous': Allow all non-dangerous commands on all keys
                           You can call DescribeDBInstanceAclCategories and
                           DescribeDBInstanceAclCommands to query supported commands.
           password (str): The account password.
                          Requirements:
                          - Length: 8-32 characters
                          - Must contain at least 2 types from: uppercase letters,
                            lowercase letters, numbers, special characters
                          - Supported special characters: ()`~!@#$%^&*-+=_{}[];,.?
           description (str, optional): Account description, max 256 characters.
           client_token (str, optional): Idempotency token, max 127 ASCII chars.
                                       Must be unique between different requests.
    """
    req = {
        "instance_id": instance_id,
        "account_name": account_name,
        "role_name": role_name,
        "password": password,
        "description": description,
        "client_token": client_token
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = redis_resource.create_db_account(req)
    if resp is None or (isinstance(resp, dict) and len(resp) == 0):
        return {
            "result": "please call list_db_account to check account!",
        }
    return resp.to_dict()


@mcp_server.tool(
    name="create_allow_list",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Create a new IP whitelist"
)
def create_allow_list(
    allow_list_name: str,
    allow_list: str = None,
    allow_list_desc: str = None,
    allow_list_category: str = "Ordinary",
    security_group_bind_infos: list[dict[str, str]] = None,
    project_name: str = None,
    client_token: str = None
) -> dict[str, Any]:
    """Create a new IP whitelist
       Args:
           allow_list_name (str): The whitelist name.
                                 Requirements:
                                 - Cannot start with number or dash(-)
                                 - Can contain Chinese characters, letters, numbers, underscore(_), dash(-)
                                 - Length: 1-32 characters
           allow_list (str, optional): IP addresses or CIDR blocks, separated by commas.
                                     Special values:
                                     - '0.0.0.0/0': allow all addresses
                                     - '127.0.0.1': deny all addresses
                                     - CIDR format like '192.168.1.0/24': allow IP range
                                     - Single IP like '192.168.1.1': allow specific IP
                                     Cannot be empty if security_group_bind_infos is not provided.
           allow_list_desc (str, optional): Whitelist description, max 200 characters.
           allow_list_category (str, optional): Whitelist type.
                                              Values: 'Ordinary' (default), 'Default'
                                              Only one default whitelist allowed per region.
           security_group_bind_infos (list[dict], optional): List of ECS security groups to associate.
                                                           Each dict contains:
                                                           - 'BindMode' (str): 'IngressDirectionIp' or 'AssociateEcsIp'
                                                           - 'SecurityGroupId' (str): Security group ID
                                                           Cannot be empty if allow_list is not provided.
                                                           Max 10 security groups per whitelist.
           project_name (str, optional): Project name for the whitelist.
                                       If not specified, joins the 'default' project.
           client_token (str, optional): Idempotency token, max 127 ASCII chars.
                                       Must be unique between different requests.
    """
    req = {
        "allow_list_name": allow_list_name,
        "allow_list": allow_list,
        "allow_list_desc": allow_list_desc,
        "allow_list_category": allow_list_category,
        "security_group_bind_infos": security_group_bind_infos,
        "project_name": project_name,
        "client_token": client_token
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = redis_resource.create_allow_list(req)
    return resp.to_dict()


@mcp_server.tool(
    name="associate_allow_list",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Bind Redis instances to specified IP whitelists"
)
def associate_allow_list(
    instance_ids: list[str],
    allow_list_ids: list[str],
    client_token: str = None
) -> dict[str, Any]:
    """Bind Redis instances to specified IP whitelists
       Args:
           instance_ids (list[str]): List of instance IDs to bind.
                                    You can call describe_db_instances to query instance information.
                                    Multiple IDs separated by commas.
                                    Note: Cannot bind multiple instances and multiple whitelists simultaneously.
           allow_list_ids (list[str]): List of whitelist IDs to bind.
                                      You can call describe_allow_lists to query whitelist information.
                                      Multiple IDs separated by commas.
                                      Note: Cannot bind multiple instances and multiple whitelists simultaneously.
           client_token (str, optional): Idempotency token, max 127 ASCII chars.
                                       Must be unique between different requests.

       Note:
           You can only:
           - Bind multiple instances to one whitelist, OR
           - Bind one instance to multiple whitelists
           You cannot bind multiple instances to multiple whitelists in a single request.
    """
    req = {
        "instance_ids": instance_ids,
        "allow_list_ids": allow_list_ids,
        "client_token": client_token
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = redis_resource.associate_allow_list(req)
    if resp is None or (isinstance(resp, dict) and len(resp) == 0):
        return {
            "result": "please call describe_allow_list_detail to check associate_allow_list result!",
        }
    return resp.to_dict()


@mcp_server.tool(
    name="disassociate_allow_list",
    description="1.Invoke `get_available_params` to retrieve available parameters before utilizing any tool. 2.Unbind Redis instances from specified IP whitelists"
)
def disassociate_allow_list(
    instance_ids: list[str],
    allow_list_ids: list[str],
    client_token: str = None
) -> dict[str, Any]:
    """Unbind Redis instances from specified IP whitelists
       Args:
           instance_ids (list[str]): List of instance IDs to unbind.
                                    You can call describe_db_instances to query instance information.
                                    Multiple IDs separated by commas.
                                    Note: Cannot unbind multiple instances and multiple whitelists simultaneously.
           allow_list_ids (list[str]): List of whitelist IDs to unbind.
                                      You can call describe_allow_lists to query whitelist information.
                                      Multiple IDs separated by commas.
                                      Note: Cannot unbind multiple instances and multiple whitelists simultaneously.
           client_token (str, optional): Idempotency token, max 127 ASCII chars.
                                       Must be unique between different requests.

       Note:
           You can only:
           - Unbind multiple instances from one whitelist, OR
           - Unbind one instance from multiple whitelists
           You cannot unbind multiple instances from multiple whitelists in a single request.
    """
    req = {
        "instance_ids": instance_ids,
        "allow_list_ids": allow_list_ids,
        "client_token": client_token
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = redis_resource.disassociate_allow_list(req)
    if resp is None or (isinstance(resp, dict) and len(resp) == 0):
        return {
            "result": "please call describe_allow_list_detail to check disassociate_allow_list result!",
        }
    return resp.to_dict()


def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Run the Redis MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["streamable-http", "stdio"],
        default="stdio",
        help="Transport protocol to use (streamable-http or stdio)",
    )

    args = parser.parse_args()
    try:
        logger.info(f"Starting Redis MCP Server with {args.transport} transport")
        mcp_server.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting Redis MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()