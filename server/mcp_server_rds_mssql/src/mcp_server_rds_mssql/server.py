import os
import re
import argparse
import logging
from typing import List, Dict, Any, Optional, Annotated
from mcp.server.fastmcp import FastMCP
from pydantic import Field

from resource.rds_mssql_resource import RDSMSSQLSDK

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
mcp_server = FastMCP("rds_mssql_mcp_server", port=int(os.getenv("MCP_SERVER_PORT", "8000")))
rds_mssql_resource_sdk = RDSMSSQLSDK(region=os.getenv('VOLCENGINE_REGION','cn-beijing'), ak=os.getenv('VOLCENGINE_ACCESS_KEY'), sk=os.getenv('VOLCENGINE_SECRET_KEY'), host=os.getenv('VOLCENGINE_ENDPOINT'))

@mcp_server.tool(
    name="describe_available_cross_region",
    description="查看跨地域备份的目的地域。"
)
def describe_available_cross_region(instance_id: Optional[Annotated[str,Field(description='实例 ID。指定后可查询该实例可用于跨地域备份的地域。:::tip您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。:::', examples=['mssql-123456'])]] = None,
                                    region_id: Optional[Annotated[str,Field(description='发起跨地域实例所在地域 ID。', examples=['cn-guangzhou'])]] = None) -> dict[str, Any]:
    """查看跨地域备份的目的地域。

    Args:
        instance_id (str, optional): 实例 ID。指定后可查询该实例可用于跨地域备份的地域。
            :::tip
            您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。
            :::
            示例值：mssql-123456
        region_id (str, optional): 发起跨地域实例所在地域 ID。
            示例值：cn-guangzhou

    Returns: 包含以下字段的字典
        regions (list[str], optional): 跨地域备份目的地域的列表。
            示例值：[
            "cn-beijing",
            "cn-shanghai"
            ]
    """
    req = {
        "instance_id": instance_id,
        "region_id": region_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mssql_resource_sdk.describe_available_cross_region(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_cross_backup_policy",
    description="查看跨地域备份策略。"
)
def describe_cross_backup_policy(instance_id: Annotated[str, Field(description='实例 ID。:::tip您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。:::', examples=['mssql-123456'])]) -> dict[str, Any]:
    """查看跨地域备份策略。

    Args:
        instance_id (str): 实例 ID。
            :::tip
            您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。
            :::
            示例值：mssql-123456

    Returns: 包含以下字段的字典
        backup_enabled (bool, optional): 是否开启跨地域备份，取值如下：
            - `true`：表示开启跨地域备份。
            - `false`：表示关闭跨地域备份。
            示例值：true
        cross_backup_region (str, optional): 跨地域备份的目的地域 ID。
            示例值：cn-shanghai
        instance_id (str, optional): 实例 ID。
            示例值：mssql-123456
        log_backup_enabled (bool, optional): 1
        retention (int, optional): 跨地域备份保留天数。
            示例值：7
    """
    req = {
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mssql_resource_sdk.describe_cross_backup_policy(req)
    return resp.to_dict()

@mcp_server.tool(
    name="modify_cross_backup_policy",
    description="修改跨地域备份策略。"
)
def modify_cross_backup_policy(instance_id: Annotated[str, Field(description='实例 ID。:::tip您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。:::', examples=['mssql-123456'])],
                               backup_enabled: Optional[Annotated[bool,Field(description='是否开启跨地域备份，取值如下：- `true`：表示开启跨地域备份。- `false`：（默认值）表示关闭跨地域备份。', examples=['true'])]] = None,
                               cross_backup_region: Optional[Annotated[str,Field(description='跨地域备份的目的地域 ID。:::tip当 `BackupEnabled` 取值为 `true` 时，该参数必选。:::', examples=['cn-shanghai'])]] = None,
                               retention: Optional[Annotated[int,Field(description='跨地域备份保留天数，取值范围为 7~1825 天，默认值为 7。', examples=['14'])]] = None) -> dict[str, Any]:
    """修改跨地域备份策略。

    Args:
        instance_id (str): 实例 ID。
            :::tip
            您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。
            :::
            示例值：mssql-123456
        backup_enabled (bool, optional): 是否开启跨地域备份，取值如下：
            - `true`：表示开启跨地域备份。
            - `false`：（默认值）表示关闭跨地域备份。
            示例值：true
        cross_backup_region (str, optional): 跨地域备份的目的地域 ID。
            :::tip
            当 `BackupEnabled` 取值为 `true` 时，该参数必选。
            :::
            示例值：cn-shanghai
        retention (int, optional): 跨地域备份保留天数，取值范围为 7~1825 天，默认值为 7。
            示例值：14

    Returns: 包含以下字段的字典
        backup_enabled (bool, optional): 是否开启跨地域备份，取值如下：
            - `true`：表示开启跨地域备份。
            - `false`：表示关闭跨地域备份。
            示例值：true
        cross_backup_region (str, optional): 跨地域备份的目的地域 ID。
            示例值：cn-shanghai
        instance_id (str, optional): 实例 ID。
            示例值：mssql-123456
        log_backup_enabled (bool, optional): 1
        retention (int, optional): 跨地域备份保留天数。
            示例值：7
    """
    req = {
        "instance_id": instance_id,
        "backup_enabled": backup_enabled,
        "cross_backup_region": cross_backup_region,
        "retention": retention,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mssql_resource_sdk.modify_cross_backup_policy(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_backup_detail",
    description="查询备份文件的详细信息。"
)
def describe_backup_detail(instance_id: Annotated[str, Field(description='实例 ID。:::tip您可以调用 [DescribeDBInstanceDetail](https://www.volcengine.com/docs/6899/174608) 接口查看实例的 ID。:::', examples=['mssql-123456'])],
                           backup_id: Annotated[str, Field(description='备份 ID。:::tip您可以调用 [DescribeBackups](https://www.volcengine.com/docs/6899/174609) 接口查询备份 ID。:::', examples=['4969fcce7764447081c709c5********'])]) -> dict[str, Any]:
    """查询备份文件的详细信息。

    Args:
        instance_id (str): 实例 ID。
            :::tip
            您可以调用 [DescribeDBInstanceDetail](https://www.volcengine.com/docs/6899/174608) 接口查看实例的 ID。
            :::
            示例值：mssql-123456
        backup_id (str): 备份 ID。
            :::tip
            您可以调用 [DescribeBackups](https://www.volcengine.com/docs/6899/174609) 接口查询备份 ID。
            :::
            示例值：4969fcce7764447081c709c5********

    Returns: 包含以下字段的字典
        backups_info (dict[str, Any], optional): BackupsInfoObject
    """
    req = {
        "instance_id": instance_id,
        "backup_id": backup_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mssql_resource_sdk.describe_backup_detail(req)
    return resp.to_dict()

@mcp_server.tool(
    name="restore_to_existed_instance",
    description="以数据库为单位，恢复数据到已有实例。"
)
def restore_to_existed_instance(source_db_instance_id: Annotated[str, Field(description='源实例 ID。:::tip您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。:::', examples=['mssql-123456'])],
                                target_db_instance_id: Annotated[str, Field(description='目标实例 ID。:::tip- 您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。- 若与源实例 ID 相同则为恢复到源实例。:::', examples=['mssql-123456'])],
                                databases: Annotated[list[dict[str, Any]], Field(description='待恢复的数据库信息。:::tip最多可传入 100 个数据库信息。:::', examples=['无'])],
                                backup_id: Optional[Annotated[str,Field(description='源实例备份集 ID。:::tip- 按备份集恢复数据库时，您可以通过调用 DescribeBackups 查询`BackupId`。- `BackupId` 和 `RestoreTime` 传入一个即可。:::', examples=['f569f53bf60a48d5b****'])]] = None,
                                restore_time: Optional[Annotated[str,Field(description='按时间点恢复数据库，可以选择备份保留周期内的任意时间点。格式：yyyy-MM-ddTHH:mm:ssZ（UTC 时间）。:::tip`BackupId` 和 `RestoreTime` 传入一个即可。:::', examples=['2023-08-23T08:04:59Z'])]] = None) -> dict[str, Any]:
    """以数据库为单位，恢复数据到已有实例。

    Args:
        source_db_instance_id (str): 源实例 ID。
            :::tip
            您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。
            :::
            示例值：mssql-123456
        target_db_instance_id (str): 目标实例 ID。
            :::tip
            - 您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。
            - 若与源实例 ID 相同则为恢复到源实例。
            :::
            示例值：mssql-123456
        databases (list[dict[str, Any]]): 待恢复的数据库信息。
            :::tip
            最多可传入 100 个数据库信息。
            :::
            示例值：无
        backup_id (str, optional): 源实例备份集 ID。
            :::tip
            - 按备份集恢复数据库时，您可以通过调用 DescribeBackups 查询`BackupId`。
            - `BackupId` 和 `RestoreTime` 传入一个即可。
            :::
            示例值：f569f53bf60a48d5b****
        restore_time (str, optional): 按时间点恢复数据库，可以选择备份保留周期内的任意时间点。格式：yyyy-MM-ddTHH:mm:ssZ（UTC 时间）。
            :::tip
            `BackupId` 和 `RestoreTime` 传入一个即可。
            :::
            示例值：2023-08-23T08:04:59Z

    Returns: 包含以下字段的字典
        instance_id (str, optional): 源实例 ID。
            示例值：mssql-123456
    """
    req = {
        "source_db_instance_id": source_db_instance_id,
        "target_db_instance_id": target_db_instance_id,
        "databases": databases,
        "backup_id": backup_id,
        "restore_time": restore_time,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mssql_resource_sdk.restore_to_existed_instance(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_tos_restore_tasks",
    description="查询实例备份数据上云任务列表。"
)
def describe_tos_restore_tasks(instance_id: Optional[Annotated[str,Field(description='实例 ID。:::tip您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。:::', examples=['mssql-123456'])]] = None,
                               instance_name: Optional[Annotated[str,Field(description='实例名称。:::tip您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例名称。:::', examples=['testname'])]] = None,
                               page_number: Optional[Annotated[int,Field(description='当前页查询偏移量。最小为 1，最大为 2147483647，默认值为 1。', examples=['1'])]] = None,
                               page_size: Optional[Annotated[int,Field(description='每页记录数。最小为 1，最大为 1000，默认值为 10。', examples=['10'])]] = '10',
                               project_name: Optional[Annotated[str,Field(description='项目名称。当您的账号为子用户时，在调用接口时必须传入该参数进行账号鉴权，否则将无法成功调用接口。主账户默认拥有所有权限，则无需传入此参数。', examples=['default'])]] = None,
                               query_end_time: Optional[Annotated[str,Field(description='查询任务创建的结束时间。格式：yyyy-MM-ddTHH:mm:ssZ（UTC 时间）。:::tip查询结束时间需晚于查询开始时间。:::', examples=['2023-08-25T01:00:01.000Z'])]] = None,
                               query_start_time: Optional[Annotated[str,Field(description='查询任务创建的开始时间。格式：yyyy-MM-ddTHH:mm:ssZ（UTC 时间）。', examples=['2023-08-25T01:03:00.000Z'])]] = None,
                               restore_task_ids: Optional[Annotated[list[str],Field(description='恢复任务 ID。当传入多个恢复任务 ID 时，请使用英文逗号（,）隔开。', examples=['["90", "100", "10" ]'])]] = None) -> dict[str, Any]:
    """查询实例备份数据上云任务列表。

    Args:
        instance_id (str, optional): 实例 ID。
            :::tip
            您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。
            :::
            示例值：mssql-123456
        instance_name (str, optional): 实例名称。
            :::tip
            您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例名称。
            :::
            示例值：testname
        page_number (int, optional): 当前页查询偏移量。最小为 1，最大为 2147483647，默认值为 1。
            示例值：1
        page_size (int, optional): 每页记录数。最小为 1，最大为 1000，默认值为 10。
            示例值：10
        project_name (str, optional): 项目名称。
            当您的账号为子用户时，在调用接口时必须传入该参数进行账号鉴权，否则将无法成功调用接口。主账户默认拥有所有权限，则无需传入此参数。
            示例值：default
        query_end_time (str, optional): 查询任务创建的结束时间。格式：yyyy-MM-ddTHH:mm:ssZ（UTC 时间）。
            :::tip
            查询结束时间需晚于查询开始时间。
            :::
            示例值：2023-08-25T01:00:01.000Z
        query_start_time (str, optional): 查询任务创建的开始时间。格式：yyyy-MM-ddTHH:mm:ssZ（UTC 时间）。
            示例值：2023-08-25T01:03:00.000Z
        restore_task_ids (list[str], optional): 恢复任务 ID。当传入多个恢复任务 ID 时，请使用英文逗号（,）隔开。
            示例值：["90", "100", "10" ]

    Returns: 包含以下字段的字典
        restore_tasks (list[dict[str, Any]], optional): 恢复任务列表。
            示例值：RestoreTaskObject
        total (int, optional): 恢复任务总数
            示例值：1
    """
    req = {
        "instance_id": instance_id,
        "instance_name": instance_name,
        "page_number": page_number,
        "page_size": page_size,
        "project_name": project_name,
        "query_end_time": query_end_time,
        "query_start_time": query_start_time,
        "restore_task_ids": restore_task_ids,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mssql_resource_sdk.describe_tos_restore_tasks(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_tos_restore_task_detail",
    description="查询云数据库 SQL Server 版实例备份数据上云的详细信息。"
)
def describe_tos_restore_task_detail(restore_task_id: Annotated[str, Field(description='恢复任务 ID。:::tip您可以调用 [DescribeTosRestoreTasks](https://www.volcengine.com/docs/6899/1131889) 接口查看恢复任务 ID。:::', examples=['490'])],
                                     page_number: Optional[Annotated[int,Field(description='当前页查询偏移量。最小为 1，最大为 2147483647，默认值为 1。', examples=['1'])]] = '1',
                                     page_size: Optional[Annotated[int,Field(description='每页记录数。最小为 1，最大为 1000，默认值为 10。', examples=['10'])]] = '10',
                                     project_name: Optional[Annotated[str,Field(description='项目名称。当您的账号为子用户时，在调用接口时必须传入该参数进行账号鉴权，否则将无法成功调用接口。主账户默认拥有所有权限，则无需传入此参数。', examples=['default'])]] = None) -> dict[str, Any]:
    """查询云数据库 SQL Server 版实例备份数据上云的详细信息。

    Args:
        restore_task_id (str): 恢复任务 ID。
            :::tip
            您可以调用 [DescribeTosRestoreTasks](https://www.volcengine.com/docs/6899/1131889) 接口查看恢复任务 ID。
            :::
            示例值：490
        page_number (int, optional): 当前页查询偏移量。最小为 1，最大为 2147483647，默认值为 1。
            示例值：1
        page_size (int, optional): 每页记录数。最小为 1，最大为 1000，默认值为 10。
            示例值：10
        project_name (str, optional): 项目名称。
            当您的账号为子用户时，在调用接口时必须传入该参数进行账号鉴权，否则将无法成功调用接口。主账户默认拥有所有权限，则无需传入此参数。
            示例值：default

    Returns: 包含以下字段的字典
        restore_task_details (list[dict[str, Any]], optional): 恢复任务的详情列表信息。
            示例值：RestoreTaskDetailObject
        total (int, optional): 恢复任务总数。
            示例值：1
    """
    req = {
        "restore_task_id": restore_task_id,
        "page_number": page_number,
        "page_size": page_size,
        "project_name": project_name,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mssql_resource_sdk.describe_tos_restore_task_detail(req)
    return resp.to_dict()

@mcp_server.tool(
    name="create_tos_restore",
    description="将对象存储 TOS 上的备份文件恢复到云数据库 SQL Server 版实例，实现数据上云。"
)
def create_tos_restore(target_db_instance_id: Annotated[str, Field(description='实例 ID。:::tip您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。:::', examples=['mssql-123456'])],
                       tos_object_positions: Annotated[str, Field(description='TOS 的对象地址。格式为 `<TOS Endpoint 地址>:<TOS Bucket 名称>:<TOS 上的备份文件名称>`，用英文冒号（:）分隔。:::tipTOS 上的备份文件格式当前仅支持 `.bak`、`.diff`、`.trn`、`.log`。:::', examples=['tos-cn-beijing.volces.com:backname:slow_query.log'])],
                       databases: Optional[Annotated[list[dict[str, Any]],Field(description='待恢复的数据库信息。:::tip单次最多可恢复 20 个数据库信息。:::', examples=['无'])]] = None,
                       is_online: Optional[Annotated[bool,Field(description='是否上线恢复后的数据库，方便访问，取值如下：- `true`：表示上线恢复后的数据库。- `false`：表示不上线恢复后的数据库（默认值）。', examples=['true'])]] = None,
                       is_replace: Optional[Annotated[bool,Field(description='恢复时是否覆盖目标实例上已经存在的数据库，当前仅支持取值`false`，表示恢复时不覆盖目标实例上已经存在的数据库', examples=['true'])]] = None,
                       restore_type: Optional[Annotated[str,Field(description='恢复任务类型，取值如下：- `FULL`：全量恢复（默认值）。- `DIFF`：差异恢复。- `LOG`：日志恢复。', examples=['FULL'])]] = None) -> dict[str, Any]:
    """将对象存储 TOS 上的备份文件恢复到云数据库 SQL Server 版实例，实现数据上云。

    Args:
        target_db_instance_id (str): 实例 ID。
            :::tip
            您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。
            :::
            示例值：mssql-123456
        tos_object_positions (str): TOS 的对象地址。格式为 `<TOS Endpoint 地址>:<TOS Bucket 名称>:<TOS 上的备份文件名称>`，用英文冒号（:）分隔。
            :::tip
            TOS 上的备份文件格式当前仅支持 `.bak`、`.diff`、`.trn`、`.log`。
            :::
            示例值：tos-cn-beijing.volces.com:backname:slow_query.log
        databases (list[dict[str, Any]], optional): 待恢复的数据库信息。
            :::tip
            单次最多可恢复 20 个数据库信息。
            :::
            示例值：无
        is_online (bool, optional): 是否上线恢复后的数据库，方便访问，取值如下：
            - `true`：表示上线恢复后的数据库。
            - `false`：表示不上线恢复后的数据库（默认值）。
            示例值：true
        is_replace (bool, optional): 恢复时是否覆盖目标实例上已经存在的数据库，当前仅支持取值`false`，表示恢复时不覆盖目标实例上已经存在的数据库
            示例值：true
        restore_type (str, optional): 恢复任务类型，取值如下：
            - `FULL`：全量恢复（默认值）。
            - `DIFF`：差异恢复。
            - `LOG`：日志恢复。
            示例值：FULL

    Returns: 包含以下字段的字典
        restore_task_id (str, optional): 恢复任务 ID。
            示例值：490
    """
    req = {
        "target_db_instance_id": target_db_instance_id,
        "tos_object_positions": tos_object_positions,
        "databases": databases,
        "is_online": is_online,
        "is_replace": is_replace,
        "restore_type": restore_type,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mssql_resource_sdk.create_tos_restore(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_db_instance_parameters",
    description="查询实例参数。"
)
def describe_db_instance_parameters(instance_id: Annotated[str, Field(description='实例 ID:::tip您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。:::', examples=['mssql-123456'])],
                                    parameter_names: Optional[Annotated[str,Field(description='参数名。:::tip支持模糊查询，不配置此参数时，则返回实例下所有参数。:::', examples=['Agent XPs'])]] = None) -> dict[str, Any]:
    """查询实例参数。

    Args:
        instance_id (str): 实例 ID
            :::tip
            您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。
            :::
            示例值：mssql-123456
        parameter_names (str, optional): 参数名。
            :::tip
            支持模糊查询，不配置此参数时，则返回实例下所有参数。
            :::
            示例值：Agent XPs

    Returns: 包含以下字段的字典
        db_engine (str, optional): 数据库类型。当前数据库类型取值仅支持 `Sqlserver`。
            示例值：Sqlserver
        db_engine_version (str, optional): 兼容版本。取值如下：
            - `SQLServer_2019_Std`：表示 SQL Server 2019 标准版。
            - `SQLServer_2019_Web`：表示 SQL Server 2019 Web 版。
            - `SQLServer_2019_Ent`：表示 SQL Server 2019 企业版。
            示例值：SQLServer_2019_Std
        instance_id (str, optional): 实例 ID。
            示例值：mssql-123456
        instance_parameters (list[dict[str, Any]], optional): 该实例当前运行的参数列表。更多关于 InstanceParameters 的详细信息，请参见[数据结构](https://www.volcengine.com/docs/6899/174554#instanceparametersobject)。
            示例值：[
            {
            "CheckingCode": "[0~1]",
            "ForceModify": false,
            "ForceRestart": false,
            "ParameterDefaultValue": "1",
            "ParameterDescription": "代理XP选项。使用Agent XPs 选项可以启用此服务器上的 SQL Server 代理扩展存储过程。如果禁用此选项，则SQL Server Management Studio对象资源管理器将不显示 SQL Server 代理节点。",
            "ParameterName": "Agent XPs",
            "ParameterType": "Integer",
            "ParameterValue": "1"
            }
            ]
        parameter_count (int, optional): 参数个数。
            示例值：1
    """
    req = {
        "instance_id": instance_id,
        "parameter_names": parameter_names,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mssql_resource_sdk.describe_db_instance_parameters(req)
    return resp.to_dict()

@mcp_server.tool(
    name="modify_backup_policy",
    description="修改备份策略。"
)
def modify_backup_policy(instance_id: Annotated[str, Field(description='实例 ID。:::tip您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。:::', examples=['mssql-123456'])],
                         backup_time: Annotated[str, Field(description='开始执行备份任务的时间窗口，间隔窗口为 1 小时。格式：HH:mmZ-HH:mmZ（UTC时间）。', examples=['19:00Z-20:00Z'])],
                         full_backup_period: Annotated[str, Field(description='全量备份周期。多个取值用英文逗号（,）隔开。取值如下：- `Monday`：周一。- `Tuesday`：周二。- `Wednesday`：周三。- `Thursday`：周四。- `Friday`：周五。- `Saturday`：周六。- `Sunday`：周日。', examples=['Monday,Wednesday'])],
                         backup_retention_period: Annotated[int, Field(description='数据备份保留天数，取值：7~30。', examples=['7'])],
                         log_backup_interval: Optional[Annotated[int,Field(description='日志备份频率，取值如下：- `5`：默认值，表示日志备份频率为 5 分钟。- `30`：表示日志备份频率为 30 分钟。', examples=['5'])]] = None) -> dict[str, Any]:
    """修改备份策略。

    Args:
        instance_id (str): 实例 ID。
            :::tip
            您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。
            :::
            示例值：mssql-123456
        backup_time (str): 开始执行备份任务的时间窗口，间隔窗口为 1 小时。格式：HH:mmZ-HH:mmZ（UTC时间）。
            示例值：19:00Z-20:00Z
        full_backup_period (str): 全量备份周期。多个取值用英文逗号（,）隔开。取值如下：
            - `Monday`：周一。
            - `Tuesday`：周二。
            - `Wednesday`：周三。
            - `Thursday`：周四。
            - `Friday`：周五。
            - `Saturday`：周六。
            - `Sunday`：周日。
            示例值：Monday,Wednesday
        backup_retention_period (int): 数据备份保留天数，取值：7~30。
            示例值：7
        log_backup_interval (int, optional): 日志备份频率，取值如下：
            - `5`：默认值，表示日志备份频率为 5 分钟。
            - `30`：表示日志备份频率为 30 分钟。
            示例值：5

    Returns: 包含以下字段的字典
        instance_id (str, optional): 实例 ID。
            示例值：mssql-123456
    """
    req = {
        "instance_id": instance_id,
        "backup_time": backup_time,
        "full_backup_period": full_backup_period,
        "backup_retention_period": backup_retention_period,
        "log_backup_interval": log_backup_interval,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mssql_resource_sdk.modify_backup_policy(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_backups",
    description="查看备份集列表。"
)
def describe_backups(instance_id: Annotated[str, Field(description='实例 ID。:::tip您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。:::', examples=['mssql-123456'])],
                     backup_end_time: Optional[Annotated[str,Field(description='查询结束时间。格式：yyyy-MM-ddTHH:mm:ss.sZ（UTC 时间）。:::tip查询结束时间需晚于查询开始时间。:::', examples=['2023-08-23T04:06:49.000Z'])]] = None,
                     backup_id: Optional[Annotated[str,Field(description='备份 ID。:::tip您可以调用 [DescribeBackups](https://www.volcengine.com/docs/6899/174609) 接口查询备份 ID。:::', examples=['ca155ac99fcb4eed86617041bfe0****'])]] = None,
                     backup_start_time: Optional[Annotated[str,Field(description='查询开始时间。格式：yyyy-MM-ddTHH:mm:ss.sZ（UTC 时间）。', examples=['2023-08-23T04:07:02.000Z'])]] = None,
                     backup_type: Optional[Annotated[str,Field(description='备份类型。默认返回所有备份信息，取值如下：- `Full`：表示全量备份。- `Diff`：表示增量备份。- `Log`：表示日志备份。:::tip当不传该参数时，默认返回全量备份和增量备份的备份集列表。:::', examples=['Full'])]] = None,
                     page_number: Optional[Annotated[int,Field(description='当前页查询偏移量。最小为 1，最大为 2147483647，默认值为 1。', examples=['1'])]] = '1',
                     page_size: Optional[Annotated[int,Field(description='每页记录数。最小为 1，最大为 1000，默认值为 10。', examples=['10'])]] = '10') -> dict[str, Any]:
    """查看备份集列表。

    Args:
        instance_id (str): 实例 ID。
            :::tip
            您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。
            :::
            示例值：mssql-123456
        backup_end_time (str, optional): 查询结束时间。格式：yyyy-MM-ddTHH:mm:ss.sZ（UTC 时间）。
            :::tip
            查询结束时间需晚于查询开始时间。
            :::
            示例值：2023-08-23T04:06:49.000Z
        backup_id (str, optional): 备份 ID。
            :::tip
            您可以调用 [DescribeBackups](https://www.volcengine.com/docs/6899/174609) 接口查询备份 ID。
            :::
            示例值：ca155ac99fcb4eed86617041bfe0****
        backup_start_time (str, optional): 查询开始时间。格式：yyyy-MM-ddTHH:mm:ss.sZ（UTC 时间）。
            示例值：2023-08-23T04:07:02.000Z
        backup_type (str, optional): 备份类型。默认返回所有备份信息，取值如下：
            - `Full`：表示全量备份。
            - `Diff`：表示增量备份。
            - `Log`：表示日志备份。
            :::tip
            当不传该参数时，默认返回全量备份和增量备份的备份集列表。
            :::
            示例值：Full
        page_number (int, optional): 当前页查询偏移量。最小为 1，最大为 2147483647，默认值为 1。
            示例值：1
        page_size (int, optional): 每页记录数。最小为 1，最大为 1000，默认值为 10。
            示例值：10

    Returns: 包含以下字段的字典
        backups_info (list[dict[str, Any]], optional): 备份列表。
            示例值：BackupInfoObject
        total (int, optional): 备份总数。
            示例值：1
    """
    req = {
        "instance_id": instance_id,
        "backup_end_time": backup_end_time,
        "backup_id": backup_id,
        "backup_start_time": backup_start_time,
        "backup_type": backup_type,
        "page_number": page_number,
        "page_size": page_size,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mssql_resource_sdk.describe_backups(req)
    return resp.to_dict()

@mcp_server.tool(
    name="create_backup",
    description="创建备份集。"
)
def create_backup(instance_id: Annotated[str, Field(description='实例 ID。:::tip您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。:::', examples=['mssql-123456'])],
                  backup_meta: Optional[Annotated[list[dict[str, Any]],Field(description='备份的库信息。:::tip在不设置该参数时，默认为实例级备份。:::', examples=['BackupMetaObject'])]] = None,
                  backup_type: Optional[Annotated[str,Field(description='备份类型。当前仅支持全量备份，即取值为 `Full`（默认值）。', examples=['Full'])]] = None) -> dict[str, Any]:
    """创建备份集。

    Args:
        instance_id (str): 实例 ID。
            :::tip
            您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。
            :::
            示例值：mssql-123456
        backup_meta (list[dict[str, Any]], optional): 备份的库信息。
            :::tip
            在不设置该参数时，默认为实例级备份。
            :::
            示例值：BackupMetaObject
        backup_type (str, optional): 备份类型。当前仅支持全量备份，即取值为 `Full`（默认值）。
            示例值：Full

    Returns: 包含以下字段的字典
        backup_id (str, optional): 备份任务 ID。
            示例值：ca155ac99fcb4eed86617041bfe0****
        instance_id (str, optional): 实例 ID。
            示例值：mssql-123456
    """
    req = {
        "instance_id": instance_id,
        "backup_meta": backup_meta,
        "backup_type": backup_type,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mssql_resource_sdk.create_backup(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_db_instance_detail",
    description="查询实例详情信息。"
)
def describe_db_instance_detail(instance_id: Annotated[str, Field(description='实例 ID:::tip您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。:::', examples=['mssql-123456'])]) -> dict[str, Any]:
    """查询实例详情信息。

    Args:
        instance_id (str): 实例 ID
            :::tip
            您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。
            :::
            示例值：mssql-123456

    Returns: 包含以下字段的字典
        basic_info (dict[str, Any], optional): BasicInfoObject
        charge_detail (dict[str, Any], optional): ChargeDetailObject
        connection_info (list[dict[str, Any]], optional): 实例的连接信息。
            示例值：ConnectionInfo
        node_detail_info (list[dict[str, Any]], optional): 实例节点信息。
            示例值：NodeDetailInfo
    """
    req = {
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mssql_resource_sdk.describe_db_instance_detail(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_db_instances",
    description="查询实例列表。"
)
def describe_db_instances(charge_type: Optional[Annotated[str,Field(description='付费类型。取值：- `PostPaid`：按量付费。- `PrePaid`：包年包月。', examples=['PostPaid'])]] = None,
                          create_time_end: Optional[Annotated[str,Field(description='创建实例的结束时间，采用 UTC 时间格式。', examples=['2023-09-19T09:19:39.000Z'])]] = None,
                          create_time_start: Optional[Annotated[str,Field(description='创建实例的开始时间，采用 UTC 时间格式。', examples=['2023-09-10T09:19:39.000Z'])]] = None,
                          db_engine_version: Optional[Annotated[str,Field(description='兼容版本。取值如下：- `SQLServer_2019_Std`：表示 SQL Server 2019 标准版。- `SQLServer_2019_Web`：表示 SQL Server 2019 Web 版。- `SQLServer_2019_Ent`：表示 SQL Server 2019 企业版。', examples=['SQLServer_2019_Std'])]] = None,
                          instance_category: Optional[Annotated[str,Field(description='实例分类。 根据实例周期进行分类管理，不传返回所有实例。取值：- `Primary`：主实例。- `ReadOnly`：只读实例。', examples=['Primary'])]] = None,
                          instance_id: Optional[Annotated[str,Field(description='实例 ID。:::tip您可以调用 [DescribeDBInstanceDetail](https://www.volcengine.com/docs/6899/174608) 接口查看实例的 ID。:::', examples=['mssql-123456'])]] = None,
                          instance_name: Optional[Annotated[str,Field(description='实例名称。', examples=['实例样例'])]] = None,
                          instance_status: Optional[Annotated[str,Field(description='实例状态，取值：- `Running`：运行中。- `Creating`：创建中。- `Deleting`：删除中。- `Restarting`：重启中。- `Updating`：变更中。- `MasterChanging`：主节点切换中。- `Error`：错误。', examples=['Running'])]] = None,
                          instance_type: Optional[Annotated[str,Field(description='实例类型。取值如下：- `HA`：表示高可用类型。- `Basic`：表示基础版类型。- `Cluster`：表示集群版类型。:::tip- 在 `DBEngineVersion` 设置为 `SQLServer_2019_Std` 时，`InstanceType` 支持设置为 `HA` 或 `Basic`。- 在 `DBEngineVersion` 设置为 `SQLServer_2019_Ent` 时，`InstanceType` 支持设置为 `Cluster` 或 `Basic`。- 在 `DBEngineVersion` 设置为 `SQLServer_2019_Web` 时，`InstanceType` 支持设置为 `Basic`。:::', examples=['HA'])]] = None,
                          page_number: Optional[Annotated[int,Field(description='当前页查询偏移量。最小为 1，最大为 2147483647，默认值为 1。', examples=['1'])]] = '1',
                          page_size: Optional[Annotated[int,Field(description='每页记录数。最小为 1，最大为 1000，默认值为 10。', examples=['10'])]] = '10',
                          primary_instance_id: Optional[Annotated[str,Field(description='主实例ID。通过传入条件查询出所有该主实例下的只读实例信息。', examples=['mssql-123456'])]] = None,
                          project_name: Optional[Annotated[str,Field(description='所属项目', examples=['default'])]] = None,
                          server_collation: Optional[Annotated[str,Field(description='实例字符集排序规则', examples=['Chinese_PRC_CI_AS'])]] = 'Chinese_PRC_CI_AS',
                          tag_filters: Optional[Annotated[list[dict[str, Any]],Field(description='标签查询数组对象。', examples=['TagFilter'])]] = None,
                          zone_id: Optional[Annotated[str,Field(description='实例所属可用区。', examples=['cn-beijing-a'])]] = None) -> dict[str, Any]:
    """查询实例列表。

    Args:
        charge_type (str, optional): 付费类型。取值：
            - `PostPaid`：按量付费。
            - `PrePaid`：包年包月。
            示例值：PostPaid
        create_time_end (str, optional): 创建实例的结束时间，采用 UTC 时间格式。
            示例值：2023-09-19T09:19:39.000Z
        create_time_start (str, optional): 创建实例的开始时间，采用 UTC 时间格式。
            示例值：2023-09-10T09:19:39.000Z
        db_engine_version (str, optional): 兼容版本。取值如下：
            - `SQLServer_2019_Std`：表示 SQL Server 2019 标准版。
            - `SQLServer_2019_Web`：表示 SQL Server 2019 Web 版。
            - `SQLServer_2019_Ent`：表示 SQL Server 2019 企业版。
            示例值：SQLServer_2019_Std
        instance_category (str, optional): 实例分类。 根据实例周期进行分类管理，不传返回所有实例。取值：
            - `Primary`：主实例。
            - `ReadOnly`：只读实例。
            示例值：Primary
        instance_id (str, optional): 实例 ID。
            :::tip
            您可以调用 [DescribeDBInstanceDetail](https://www.volcengine.com/docs/6899/174608) 接口查看实例的 ID。
            :::
            示例值：mssql-123456
        instance_name (str, optional): 实例名称。
            示例值：实例样例
        instance_status (str, optional): 实例状态，取值：
            - `Running`：运行中。
            - `Creating`：创建中。
            - `Deleting`：删除中。
            - `Restarting`：重启中。
            - `Updating`：变更中。
            - `MasterChanging`：主节点切换中。
            - `Error`：错误。
            示例值：Running
        instance_type (str, optional): 实例类型。取值如下：
            - `HA`：表示高可用类型。
            - `Basic`：表示基础版类型。
            - `Cluster`：表示集群版类型。
            :::tip
            - 在 `DBEngineVersion` 设置为 `SQLServer_2019_Std` 时，`InstanceType` 支持设置为 `HA` 或 `Basic`。
            - 在 `DBEngineVersion` 设置为 `SQLServer_2019_Ent` 时，`InstanceType` 支持设置为 `Cluster` 或 `Basic`。
            - 在 `DBEngineVersion` 设置为 `SQLServer_2019_Web` 时，`InstanceType` 支持设置为 `Basic`。
            :::
            示例值：HA
        page_number (int, optional): 当前页查询偏移量。最小为 1，最大为 2147483647，默认值为 1。
            示例值：1
        page_size (int, optional): 每页记录数。最小为 1，最大为 1000，默认值为 10。
            示例值：10
        primary_instance_id (str, optional): 主实例ID。
            通过传入条件查询出所有该主实例下的只读实例信息。
            示例值：mssql-123456
        project_name (str, optional): 所属项目
            示例值：default
        server_collation (str, optional): 实例字符集排序规则
            示例值：Chinese_PRC_CI_AS
        tag_filters (list[dict[str, Any]], optional): 标签查询数组对象。
            示例值：TagFilter
        zone_id (str, optional): 实例所属可用区。
            示例值：cn-beijing-a

    Returns: 包含以下字段的字典
        instances_info (list[dict[str, Any]], optional): 实例列表。
            示例值：InstancesInfo
        total (int, optional): 实例总数。
            示例值：1
    """
    req = {
        "charge_type": charge_type,
        "create_time_end": create_time_end,
        "create_time_start": create_time_start,
        "db_engine_version": db_engine_version,
        "instance_category": instance_category,
        "instance_id": instance_id,
        "instance_name": instance_name,
        "instance_status": instance_status,
        "instance_type": instance_type,
        "page_number": page_number,
        "page_size": page_size,
        "primary_instance_id": primary_instance_id,
        "project_name": project_name,
        "server_collation": server_collation,
        "tag_filters": tag_filters,
        "zone_id": zone_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mssql_resource_sdk.describe_db_instances(req)
    return resp.to_dict()

@mcp_server.tool(
    name="modify_db_instance_name",
    description="修改实例名称。"
)
def modify_db_instance_name(instance_id: Annotated[str, Field(description='实例 ID。:::tip您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。:::', examples=['mssql-123456'])],
                            instance_new_name: Annotated[str, Field(description='实例名称。实例名称的命名规则如下：- 不能以数字、中划线（-）开头。- 只能包含中文、字母、数字、下划线（_）和中划线（-）。- 长度限制在 1~128 之间。', examples=['name123'])]) -> dict[str, Any]:
    """修改实例名称。

    Args:
        instance_id (str): 实例 ID。
            :::tip
            您可以调用 [DescribeDBInstances](https://www.volcengine.com/docs/6899/174607) 接口查询实例 ID。
            :::
            示例值：mssql-123456
        instance_new_name (str): 实例名称。实例名称的命名规则如下：
            - 不能以数字、中划线（-）开头。
            - 只能包含中文、字母、数字、下划线（_）和中划线（-）。
            - 长度限制在 1~128 之间。
            示例值：name123
    """
    req = {
        "instance_id": instance_id,
        "instance_new_name": instance_new_name,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mssql_resource_sdk.modify_db_instance_name(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_db_instance_specs",
    description="查询实例规格代码。"
)
def describe_db_instance_specs(db_engine_version: Optional[Annotated[str,Field(description='兼容版本。取值如下：- `SQLServer_2019_Std`：表示 SQL Server 2019 标准版。- `SQLServer_2019_Web`：表示 SQL Server 2019 Web 版。- `SQLServer_2019_Ent`：表示 SQL Server 2019 企业版。', examples=['SQLServer_2019_Std'])]] = None,
                               instance_type: Optional[Annotated[str,Field(description='实例类型。取值如下：- `HA`：表示高可用类型。- `Basic`：表示基础版类型。- `Cluster`：表示集群版类型。- `ReadOnly`：表示只读实例。:::tip若不传入该参数，将返回所有实例类型的规格。:::', examples=['Basic'])]] = None,
                               spec_code: Optional[Annotated[str,Field(description='1', examples=[''])]] = None,
                               zone_id: Optional[Annotated[str,Field(description='主实例可用区 ID。:::tip您可以调用 [DescribeAvailabilityZones](https://www.volcengine.com/docs/6899/174603) 接口查询实例可用区 ID。:::', examples=['cn-beijing-a'])]] = None) -> dict[str, Any]:
    """查询实例规格代码。

    Args:
        db_engine_version (str, optional): 兼容版本。取值如下：
            - `SQLServer_2019_Std`：表示 SQL Server 2019 标准版。
            - `SQLServer_2019_Web`：表示 SQL Server 2019 Web 版。
            - `SQLServer_2019_Ent`：表示 SQL Server 2019 企业版。
            示例值：SQLServer_2019_Std
        instance_type (str, optional): 实例类型。取值如下：
            - `HA`：表示高可用类型。
            - `Basic`：表示基础版类型。
            - `Cluster`：表示集群版类型。
            - `ReadOnly`：表示只读实例。
            :::tip
            若不传入该参数，将返回所有实例类型的规格。
            :::
            示例值：Basic
        spec_code (str, optional): 1
        zone_id (str, optional): 主实例可用区 ID。
            :::tip
            您可以调用 [DescribeAvailabilityZones](https://www.volcengine.com/docs/6899/174603) 接口查询实例可用区 ID。
            :::
            示例值：cn-beijing-a

    Returns: 包含以下字段的字典
        instance_specs_info (list[dict[str, Any]], optional): 规格列表。
    """
    req = {
        "db_engine_version": db_engine_version,
        "instance_type": instance_type,
        "spec_code": spec_code,
        "zone_id": zone_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mssql_resource_sdk.describe_db_instance_specs(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_availability_zones",
    description="查询可用区列表。"
)
def describe_availability_zones(region_id: Optional[Annotated[str,Field(description='地域 ID，可调用 [DescribeRegions](https://www.volcengine.com/docs/6899/174602) 接口查询。若此参数为空，则代表查询全部地域的可用区。', examples=['cn-beijing'])]] = None) -> dict[str, Any]:
    """查询可用区列表。

    Args:
        region_id (str, optional): 地域 ID，可调用 [DescribeRegions](https://www.volcengine.com/docs/6899/174602) 接口查询。若此参数为空，则代表查询全部地域的可用区。
            示例值：cn-beijing

    Returns: 包含以下字段的字典
        region_id (str, optional): 地域 ID。
            示例值：cn-beijing
        zones (list[dict[str, Any]], optional): 可用区列表。关于 Zones 的详细信息，请参见[数据结构](https://www.volcengine.com/docs/6899/174554#zonesobject)
            示例值：{
            "Description": "华北2（北京）-可用区A",
            "ZoneId": "cn-beijing-a",
            "ZoneName": "cn-beijing-a"
            }
    """
    req = {
        "region_id": region_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mssql_resource_sdk.describe_availability_zones(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_regions",
    description="查看云数据库 SQL Server 版支持的 Region 列表。"
)
def describe_regions() -> dict[str, Any]:
    """查看云数据库 SQL Server 版支持的 Region 列表。

    Returns: 包含以下字段的字典
        regions (list[dict[str, Any]], optional): 地域列表。
            示例值：{
            "RegionId": "cn-beijing",
            "RegionName": "cn-beijing"
            }
    """
    req = {
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mssql_resource_sdk.describe_regions(req)
    return resp.to_dict()

@mcp_server.tool(
    name="create_db_instance",
    description="创建实例。"
)
def create_db_instance(db_engine_version: Annotated[str, Field(description='兼容版本。取值如下：- `SQLServer_2019_Std`：表示 SQL Server 2019 标准版。- `SQLServer_2019_Ent`：表示 SQL Server 2019 企业版。- `SQLServer_2019_Web`：表示 SQL Server 2019 Web 版。', examples=['SQLServer_2019_Std'])],
                       instance_type: Annotated[str, Field(description='实例类型。取值如下：- `HA`：表示高可用类型。- `Basic`：表示基础版类型。- `Cluster`：表示集群版类型。:::tip- 在 `DBEngineVersion` 设置为 `SQLServer_2019_Std` 时，`InstanceType` 支持设置为 `HA` 或 `Basic`。- 在 `DBEngineVersion` 设置为 `SQLServer_2019_Ent` 时，`InstanceType` 支持设置为 `Cluster` 或 `Basic`。- 在 `DBEngineVersion` 设置为 `SQLServer_2019_Web` 时，`InstanceType` 支持设置为 `Basic`。:::', examples=['HA'])],
                       zone_id: Annotated[str, Field(description='节点所在可用区。当主备节点不在同一个可用区时，您可以使用英文分号（;）隔开，默认第一个为主节点可用区，第二个为备节点可用区。:::tip您可以调用 [DescribeAvailabilityZones](https://www.volcengine.com/docs/6899/174603) 接口查询可用区。:::', examples=['cn-beijing-a'])],
                       node_spec: Annotated[str, Field(description='实例规格代码。更多关于实例规格代码的详细信息，请参见[产品规格](https://www.volcengine.com/docs/6899/141341)。', examples=['rds.mssql.se.ha.d4.4c16g'])],
                       storage_space: Annotated[int, Field(description='存储空间大小，单位为 GiB。取值范围：20GiB ~ 4000GiB，步长为 10GiB。', examples=['100'])],
                       vpc_id: Annotated[str, Field(description='私有网络（VPC） ID。:::tip您可以调用 [DescribeVpcs](https://www.volcengine.com/docs/6401/70495) 接口查询满足指定条件的私有网络。:::', examples=['VPC123456'])],
                       subnet_id: Annotated[str, Field(description='子网 ID。当主备节点不在同一个可用区时，主备节点的子网也需设置为对应可用区私有网络下的子网，多个可用区需使用英文分号（;）隔开。:::tip您可以调用 [DescribeSubnets](https://www.volcengine.com/docs/6401/70497) 接口查询子网 ID。:::', examples=['Subnet123456'])],
                       super_account_password: Annotated[str, Field(description='高权限账号的密码。密码规则如下：- 长度为 8~32 个字符。- 由大写字母、小写字母、数字、特殊字符中的至少三种组成。- 特殊字符为 `!@#$%^&*()_+-=`。', examples=['Test@123456'])],
                       db_time_zone: Annotated[str, Field(description='时区。当前仅支持取值 `China Standard Time`。', examples=['China Standard Time'])],
                       charge_info: Annotated[dict[str, Any], Field(description='ChargeInfoObject', examples=[''])],
                       allow_list_ids: Optional[Annotated[list[str],Field(description='白名单 ID。如需绑定多个白名单，白名单 ID 用英文逗号（,）分隔。:::tip一个实例最多可绑定 100 个白名单。:::', examples=['["acl-a29be2559dc4406883d358892b90****","acl-ded4c0b707e44efd8f0dbc4e88f5****"]'])]] = None,
                       instance_name: Optional[Annotated[str,Field(description='实例名称。实例名称的命名规则如下：- 不能以数字、中划线开头。- 只能包含中文、字母、数字、下划线和中划线。- 长度限制在 1~128 之间。', examples=['Name123'])]] = None,
                       maintenance_time: Optional[Annotated[str,Field(description='实例的可维护时间段。格式：HH:mmZ-HH:mmZ（UTC时间）。默认取值为 UTC18:00Z-21:59Z（即北京时间 02:00-05:59）:::tip- 为保护云数据库的稳定性，系统会不定期对实例进行维护。可维护时间段建议设置在业务低峰期，避免对业务造成影响。- 在可维护时间段内，实例可能会出现 1~2 次的连接闪断，需确保应用程序具有自动重连机制。- 可维护时间段最小时间间隔 1 小时，最大时间间隔 24 小时，不允许跨天选择可维护时间段。- 实例创建后，调用 ModifyDBInstanceMaintenanceWindow 接口修改实例的可维护时间段。详细信息，请参见 ModifyDBInstanceMaintenanceWindow。:::', examples=['22:00Z-02:59Z'])]] = None,
                       project_name: Optional[Annotated[str,Field(description='所属项目，默认值为空。:::tip您可以调用 [GetProject](https://www.volcengine.com/docs/6649/1131876) 接口查看项目信息。:::', examples=['default'])]] = None,
                       server_collation: Optional[Annotated[str,Field(description='实例字符集排序规则，默认取值为 `Chinese_PRC_CI_AS`。目前已支持大多数原生字符集具体取值如下：- `Latin1_General_CI_AS`- `Latin1_General_CS_AS`- `SQL_Latin1_General_CP1_CI_AS`- `SQL_Latin1_General_CP1_CS_AS`- `Chinese_PRC_CI_AS`- `Chinese_PRC_CS_AS`- `Chinese_PRC_BIN`- `Japanese_CI_AS`- `Japanese_CS_AS`- `Chinese_Taiwan_Stroke_CI_AS`- `Chinese_Taiwan_Stroke_CS_AS`- `Thai_CI_AS`', examples=['Chinese_PRC_CI_AS'])]] = None,
                       tags: Optional[Annotated[list[dict[str, Any]],Field(description='实例标签。详细信息，请参见[数据结构](https://www.volcengine.com/docs/6899/174554#tagsobject)。', examples=['{"Key":"key", "Value":"value"}'])]] = None) -> dict[str, Any]:
    """创建实例。

    Args:
        db_engine_version (str): 兼容版本。取值如下：
            - `SQLServer_2019_Std`：表示 SQL Server 2019 标准版。
            - `SQLServer_2019_Ent`：表示 SQL Server 2019 企业版。
            - `SQLServer_2019_Web`：表示 SQL Server 2019 Web 版。
            示例值：SQLServer_2019_Std
        instance_type (str): 实例类型。取值如下：
            - `HA`：表示高可用类型。
            - `Basic`：表示基础版类型。
            - `Cluster`：表示集群版类型。
            :::tip
            - 在 `DBEngineVersion` 设置为 `SQLServer_2019_Std` 时，`InstanceType` 支持设置为 `HA` 或 `Basic`。
            - 在 `DBEngineVersion` 设置为 `SQLServer_2019_Ent` 时，`InstanceType` 支持设置为 `Cluster` 或 `Basic`。
            - 在 `DBEngineVersion` 设置为 `SQLServer_2019_Web` 时，`InstanceType` 支持设置为 `Basic`。
            :::
            示例值：HA
        zone_id (str): 节点所在可用区。当主备节点不在同一个可用区时，您可以使用英文分号（;）隔开，默认第一个为主节点可用区，第二个为备节点可用区。
            :::tip
            您可以调用 [DescribeAvailabilityZones](https://www.volcengine.com/docs/6899/174603) 接口查询可用区。
            :::
            示例值：cn-beijing-a
        node_spec (str): 实例规格代码。更多关于实例规格代码的详细信息，请参见[产品规格](https://www.volcengine.com/docs/6899/141341)。
            示例值：rds.mssql.se.ha.d4.4c16g
        storage_space (int): 存储空间大小，单位为 GiB。取值范围：20GiB ~ 4000GiB，步长为 10GiB。
            示例值：100
        vpc_id (str): 私有网络（VPC） ID。
            :::tip
            您可以调用 [DescribeVpcs](https://www.volcengine.com/docs/6401/70495) 接口查询满足指定条件的私有网络。
            :::
            示例值：VPC123456
        subnet_id (str): 子网 ID。当主备节点不在同一个可用区时，主备节点的子网也需设置为对应可用区私有网络下的子网，多个可用区需使用英文分号（;）隔开。
            :::tip
            您可以调用 [DescribeSubnets](https://www.volcengine.com/docs/6401/70497) 接口查询子网 ID。
            :::
            示例值：Subnet123456
        super_account_password (str): 高权限账号的密码。密码规则如下：
            - 长度为 8~32 个字符。
            - 由大写字母、小写字母、数字、特殊字符中的至少三种组成。
            - 特殊字符为 `!@#$%^&*()_+-=`。
            示例值：Test@123456
        db_time_zone (str): 时区。当前仅支持取值 `China Standard Time`。
            示例值：China Standard Time
        charge_info (dict[str, Any]): ChargeInfoObject
        allow_list_ids (list[str], optional): 白名单 ID。如需绑定多个白名单，白名单 ID 用英文逗号（,）分隔。
            :::tip
            一个实例最多可绑定 100 个白名单。
            :::
            示例值：[
            "acl-a29be2559dc4406883d358892b90****",
            "acl-ded4c0b707e44efd8f0dbc4e88f5****"
            ]
        instance_name (str, optional): 实例名称。实例名称的命名规则如下：
            - 不能以数字、中划线开头。
            - 只能包含中文、字母、数字、下划线和中划线。
            - 长度限制在 1~128 之间。
            示例值：Name123
        maintenance_time (str, optional): 实例的可维护时间段。格式：HH:mmZ-HH:mmZ（UTC时间）。默认取值为 UTC18:00Z-21:59Z（即北京时间 02:00-05:59）
            :::tip
            - 为保护云数据库的稳定性，系统会不定期对实例进行维护。可维护时间段建议设置在业务低峰期，避免对业务造成影响。
            - 在可维护时间段内，实例可能会出现 1~2 次的连接闪断，需确保应用程序具有自动重连机制。
            - 可维护时间段最小时间间隔 1 小时，最大时间间隔 24 小时，不允许跨天选择可维护时间段。
            - 实例创建后，调用 ModifyDBInstanceMaintenanceWindow 接口修改实例的可维护时间段。详细信息，请参见 ModifyDBInstanceMaintenanceWindow。
            :::
            示例值：22:00Z-02:59Z
        project_name (str, optional): 所属项目，默认值为空。
            :::tip
            您可以调用 [GetProject](https://www.volcengine.com/docs/6649/1131876) 接口查看项目信息。
            :::
            示例值：default
        server_collation (str, optional): 实例字符集排序规则，默认取值为 `Chinese_PRC_CI_AS`。目前已支持大多数原生字符集具体取值如下：
            - `Latin1_General_CI_AS`
            - `Latin1_General_CS_AS`
            - `SQL_Latin1_General_CP1_CI_AS`
            - `SQL_Latin1_General_CP1_CS_AS`
            - `Chinese_PRC_CI_AS`
            - `Chinese_PRC_CS_AS`
            - `Chinese_PRC_BIN`
            - `Japanese_CI_AS`
            - `Japanese_CS_AS`
            - `Chinese_Taiwan_Stroke_CI_AS`
            - `Chinese_Taiwan_Stroke_CS_AS`
            - `Thai_CI_AS`
            示例值：Chinese_PRC_CI_AS
        tags (list[dict[str, Any]], optional): 实例标签。详细信息，请参见[数据结构](https://www.volcengine.com/docs/6899/174554#tagsobject)。
            示例值：{"Key":"key", "Value":"value"}

    Returns: 包含以下字段的字典
        instance_id (str, optional): 实例 ID。
            示例值：mssql-44171da8****
        order_id (str, optional): 订单 ID。
            示例值：Order719479011897090****
    """
    req = {
        "db_engine_version": db_engine_version,
        "instance_type": instance_type,
        "zone_id": zone_id,
        "node_spec": node_spec,
        "storage_space": storage_space,
        "vpc_id": vpc_id,
        "subnet_id": subnet_id,
        "super_account_password": super_account_password,
        "db_time_zone": db_time_zone,
        "charge_info": charge_info,
        "allow_list_ids": allow_list_ids,
        "instance_name": instance_name,
        "maintenance_time": maintenance_time,
        "project_name": project_name,
        "server_collation": server_collation,
        "tags": tags,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mssql_resource_sdk.create_db_instance(req)
    return resp.to_dict()


"""Main entry point for the MCP server."""
def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Run the Rds Mssql MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["streamable-http", "stdio"],
        default="stdio",
        help="Transport protocol to use (streamable-http or stdio)",
    )

    args = parser.parse_args()
    try:
        logger.info(f"Starting Rds Mssql MCP Server with {args.transport} transport")
        mcp_server.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting Rds Mssql MCP Server: {str(e)}")
        raise

if __name__ == "__main__":
    main()