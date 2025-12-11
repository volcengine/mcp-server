import os
import argparse
import logging
from typing import List, Dict, Any, Optional, Annotated
from mcp.server.fastmcp import FastMCP
from pydantic import Field, validate_call

from .resource.rds_postgresql_resource import RDSPOSTGRESQLSDK
from .tools.credential import get_volcengine_credentials

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
mcp_server = FastMCP("rds_postgresql_mcp_server", port=int(os.getenv("MCP_SERVER_PORT", "8000")))
credentials = get_volcengine_credentials()
rds_postgresql_resource_sdk = RDSPOSTGRESQLSDK(
    region=credentials['region'],
    ak=credentials['access_key_id'],
    sk=credentials['secret_access_key'],
    token=credentials['session_token'],
    host=credentials['host'],
    header_name="X-PGMgr-Source",
    header_value="local_mcp",
)

@mcp_server.tool(
    name="describe_wal_log_backups",
    description="调用 DescribeWALLogBackups 接口获取指定实例已备份的 WAL 日志列表。"
)
def describe_wal_log_backups(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-08f97473****'])],
                             backup_id: Optional[Annotated[str,Field(description='备份文件 ID。', examples=['00000005000000010000000C'])]] = None,
                             end_time: Optional[Annotated[str,Field(description='查询时间范围的终点，格式为 `yyyy-MM-ddTHH:mm:ssZ`（UTC 时间）。:::tip- 以备份结束时间为准。- 无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。:::', examples=['2025-12-01T14:03:19Z'])]] = None,
                             page_number: Optional[Annotated[int,Field(description='分页页码。默认值为 1。', examples=['2'])]] = None,
                             page_size: Optional[Annotated[int,Field(description='每页记录数，取值应大于 0 且不超过 1000，默认值为 10。', examples=['5'])]] = None,
                             start_time: Optional[Annotated[str,Field(description='查询时间范围的起点，格式为 `yyyy-MM-ddTHH:mm:ssZ`（UTC 时间）。:::tip- 以备份结束时间为准。- 无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。:::', examples=['2025-12-01T13:00:00Z'])]] = None) -> dict[str, Any]:
    """调用 DescribeWALLogBackups 接口获取指定实例已备份的 WAL 日志列表。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-08f97473****
        backup_id (str, optional): 备份文件 ID。
            示例值：00000005000000010000000C
        end_time (str, optional): 查询时间范围的终点，格式为 `yyyy-MM-ddTHH:mm:ssZ`（UTC 时间）。
            :::tip
            - 以备份结束时间为准。
            - 无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。
            :::
            示例值：2025-12-01T14:03:19Z
        page_number (int, optional): 分页页码。默认值为 1。
            示例值：2
        page_size (int, optional): 每页记录数，取值应大于 0 且不超过 1000，默认值为 10。
            示例值：5
        start_time (str, optional): 查询时间范围的起点，格式为 `yyyy-MM-ddTHH:mm:ssZ`（UTC 时间）。
            :::tip
            - 以备份结束时间为准。
            - 无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。
            :::
            示例值：2025-12-01T13:00:00Z

    Returns: 包含以下字段的字典
        total (int, optional): 符合查询条件的 WAL 日志备份总数。
            示例值：123
        wal_log_backups (list[dict[str, Any]], optional): WAL 日志备份列表。
            示例值：请参见返回示例。
    """
    req = {
        "instance_id": instance_id,
        "backup_id": backup_id,
        "end_time": end_time,
        "page_number": page_number,
        "page_size": page_size,
        "start_time": start_time,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_wal_log_backups(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="describe_db_instance_ssl",
    description="调用 DescribeDBInstanceSSL 接口查询指定实例的 SSL 设置。"
)
def describe_db_instance_ssl(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-f006d308****'])]) -> dict[str, Any]:
    """调用 DescribeDBInstanceSSL 接口查询指定实例的 SSL 设置。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-f006d308****

    Returns: 包含以下字段的字典
        address (list[str], optional): 受保护地址。
            示例值：[
            "postgresf006d308****.rds-pg.ivolces.com"
            ]
        force_encryption (bool, optional): 是否开启了强制加密，取值：
            - `true`：是。
            - `false`：否。
            示例值：true
        is_valid (bool, optional): SSL 证书是否有效，取值：
            - `true`：是。
            - `false`：否。
            示例值：true
        ssl_enable (bool, optional): SSL 功能是否开启，取值：
            - `true`：是。
            - `false`：否。
            示例值：true
        ssl_expire_time (str, optional): SSL 证书的到期时间。格式为：`yyyy-MM-ddTHH:mm:ss`（UTC 时间）。
            示例值：2026-09-10T04:50:55Z
        tls_version (list[str], optional): 支持的 TLS 版本。
            示例值：[
            "TLSv1_2",
            "TLSv1_3"
            ]
    """
    req = {
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_db_instance_ssl(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="describe_tasks",
    description="调用 DescribeTasks 接口查询任务，查询时需要带上起止时间，最早可以查询30天前的任务，起止时间范围不能超过 7 天。"
)
@validate_call
def describe_tasks(page_number: Annotated[int, Field(description='当前页页码。最小值为 1。', examples=['1'])],
                   page_size: Annotated[int, Field(description='每页记录数。最小值为 1，最大值不超过 1000。', examples=['100'])],
                   creation_end_time: Optional[Annotated[str,Field(description='任务的结束时间。时间格式为 `yyyy-MM-ddTHH:mm:ssZ`（UTC 时间）。:::tip- 任务时间（CreationStartTime 和 CreationEndTime）与 TaskId 两组参数，二者必选其一。- 任务开始时间（CreationStartTime）与任务结束时间（CreationEndTime）的最大时间间隔不能超过 7 天。:::', examples=['2025-09-10T23:40:00Z'])]] = None,
                   creation_start_time: Optional[Annotated[str,Field(description='任务的开始时间。时间格式为 `yyyy-MM-ddTHH:mm:ssZ`（UTC 时间）。:::tip- 任务时间（CreationStartTime 和 CreationEndTime）与 TaskId 两组参数，二者必选其一。- 任务开始时间（CreationStartTime）与任务结束时间（CreationEndTime）的最大时间间隔不能超过 7 天。:::', examples=['2025-09-04T21:30:00Z'])]] = None,
                   instance_id: Optional[Annotated[str,Field(description='实例 ID。', examples=['postgres-2904ed64****'])]] = None,
                   project_name: Optional[Annotated[str,Field(description='项目名称。', examples=['default'])]] = None,
                   task_action: Optional[Annotated[str,Field(description='任务对应的 Action，一般为与任务相应的 Open API 的 Action。', examples=['ModifyDBInstanceSSL'])]] = None,
                   task_id: Optional[Annotated[str,Field(description='任务 ID。', examples=['202509102225598DA116E6B90D38F149EA-9f0b91'])]] = None,
                   task_status: Optional[Annotated[list[str],Field(description='任务状态，取值：- `Canceled`：已取消。- `WaitStart`：待执行。- `WaitSwitch`：待切换。- `Running`：运行中。- `Running_BeforeSwitch`：运行中-切换前。- `Running_Switching`：运行中-切换中。- `Running_AfterSwitch`：运行中-切换后。- `Success`：成功。- `Failed`：失败。- `Timeout`：超时。- `Rollbacking`：回滚中。- `RollbackFailed`：回滚失败。- `Paused`：已暂停。', examples=['Success'])]] = None) -> dict[str, Any]:
    """调用 DescribeTasks 接口查询任务。

    Args:
        page_number (int): 当前页页码。最小值为 1。
            示例值：1
        page_size (int): 每页记录数。最小值为 1，最大值不超过 1000。
            示例值：100
        creation_end_time (str, optional): 任务的结束时间。时间格式为 `yyyy-MM-ddTHH:mm:ssZ`（UTC 时间）。
            :::tip
            - 任务时间（CreationStartTime 和 CreationEndTime）与 TaskId 两组参数，二者必选其一。
            - 任务开始时间（CreationStartTime）与任务结束时间（CreationEndTime）的最大时间间隔不能超过 7 天。
            :::
            示例值：2025-09-10T23:40:00Z
        creation_start_time (str, optional): 任务的开始时间。时间格式为 `yyyy-MM-ddTHH:mm:ssZ`（UTC 时间）。
            :::tip
            - 任务时间（CreationStartTime 和 CreationEndTime）与 TaskId 两组参数，二者必选其一。
            - 任务开始时间（CreationStartTime）与任务结束时间（CreationEndTime）的最大时间间隔不能超过 7 天。
            :::
            示例值：2025-09-04T21:30:00Z
        instance_id (str, optional): 实例 ID。
            示例值：postgres-2904ed64****
        project_name (str, optional): 项目名称。
            示例值：default
        task_action (str, optional): 任务对应的 Action，一般为与任务相应的 Open API 的 Action。
            示例值：ModifyDBInstanceSSL
        task_id (str, optional): 任务 ID。
            示例值：202509102225598DA116E6B90D38F149EA-9f0b91
        task_status (list[str], optional): 任务状态，取值：
            - `Canceled`：已取消。
            - `WaitStart`：待执行。
            - `WaitSwitch`：待切换。
            - `Running`：运行中。
            - `Running_BeforeSwitch`：运行中-切换前。
            - `Running_Switching`：运行中-切换中。
            - `Running_AfterSwitch`：运行中-切换后。
            - `Success`：成功。
            - `Failed`：失败。
            - `Timeout`：超时。
            - `Rollbacking`：回滚中。
            - `RollbackFailed`：回滚失败。
            - `Paused`：已暂停。
            示例值：Success

    Returns: 包含以下字段的字典
        task_infos (list[dict[str, Any]], optional): 任务的详细信息。
            示例值：请参见返回示例。
        total (int, optional): 符合查询条件的任务数量。
            示例值：123
    """
    req = {
        "page_number": page_number,
        "page_size": page_size,
        "creation_end_time": creation_end_time,
        "creation_start_time": creation_start_time,
        "instance_id": instance_id,
        "project_name": project_name,
        "task_action": task_action,
        "task_id": task_id,
        "task_status": task_status,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_tasks(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="describe_db_engine_version_parameters",
    description="调用 DescribeDBEngineVersionParameters 接口查询指定数据库引擎版本支持用户设置的参数列表。"
)
def describe_db_engine_version_parameters(db_engine: Annotated[str, Field(description='参数模板的类型。当前取值仅能为 `PostgreSQL`。', examples=['PostgreSQL'])],
                                          db_engine_version: Annotated[str, Field(description='兼容版本。取值：- `PostgreSQL_11`：PostgreSQL 11。- `PostgreSQL_12`：PostgreSQL 12。- `PostgreSQL_13`：PostgreSQL 13。- `PostgreSQL_14`：PostgreSQL 14。- `PostgreSQL_15`：PostgreSQL 15。- `PostgreSQL_16`：PostgreSQL 16。- `PostgreSQL_17`：PostgreSQL 17。', examples=['PostgreSQL_12'])]) -> dict[str, Any]:
    """调用 DescribeDBEngineVersionParameters 接口查询指定数据库引擎版本支持用户设置的参数列表。

    Args:
        db_engine (str): 参数模板的类型。当前取值仅能为 `PostgreSQL`。
            示例值：PostgreSQL
        db_engine_version (str): 兼容版本。取值：
            - `PostgreSQL_11`：PostgreSQL 11。
            - `PostgreSQL_12`：PostgreSQL 12。
            - `PostgreSQL_13`：PostgreSQL 13。
            - `PostgreSQL_14`：PostgreSQL 14。
            - `PostgreSQL_15`：PostgreSQL 15。
            - `PostgreSQL_16`：PostgreSQL 16。
            - `PostgreSQL_17`：PostgreSQL 17。
            示例值：PostgreSQL_12

    Returns: 包含以下字段的字典
        db_engine_version (str, optional): 兼容版本。取值：
            - `PostgreSQL_11`：PostgreSQL 11。
            - `PostgreSQL_12`：PostgreSQL 12。
            - `PostgreSQL_13`：PostgreSQL 13。
            - `PostgreSQL_14`：PostgreSQL 14。
            - `PostgreSQL_15`：PostgreSQL 15。
            - `PostgreSQL_16`：PostgreSQL 16。
            - `PostgreSQL_17`：PostgreSQL 17。
            示例值：PostgreSQL_12
        parameter_count (str, optional): 指定数据库引擎版本下支持用户设置的参数个数。
            示例值：39
        parameters (list[dict[str, Any]], optional): 指定数据库引擎版本下支持用户设置的参数列表。
            示例值：请参见返回示例。
    """
    req = {
        "db_engine": db_engine,
        "db_engine_version": db_engine_version,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_db_engine_version_parameters(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="describe_planned_events",
    description="调用 DescribePlannedEvents 接口查询当前地域下的运维事件。"
)
@validate_call
def describe_planned_events(event_id: Optional[Annotated[str,Field(description='事件 ID。', examples=['61c7adeb0f49426ab032cb8cf1e2****'])]] = None,
                            event_type: Optional[Annotated[list[str],Field(description='事件类型。取值范围（可取多个值）：- `VersionUpgrade`：版本升级。- `HostOffline`：主机下线。', examples=['["VersionUpgrade"]'])]] = None,
                            instance_id: Optional[Annotated[str,Field(description='实例 ID。', examples=['postgres-a2f9831f****'])]] = None,
                            instance_name: Optional[Annotated[str,Field(description='实例名称。', examples=['测试实例'])]] = None,
                            page_number: Optional[Annotated[int,Field(description='当前页查询偏移量，默认值为 1。', examples=['2'])]] = None,
                            page_size: Optional[Annotated[int,Field(description='每页记录数，取值应大于 0 且不超过 1000，默认值为 10。', examples=['20'])]] = None,
                            planned_begin_time_search_range_end: Optional[Annotated[str,Field(description='按照“计划执行时间”查询事件时的时间区间的终点。格式：`yyyy-MM-ddTHH:mm:ss.sssZ`（UTC 时间）。:::tip- PlannedBeginTimeSearchRangeEnd 应晚于 PlannedBeginTimeSearchRangeStart。- PlannedBeginTimeSearchRangeStart 与 PlannedBeginTimeSearchRangeEnd 定义了一个时间段。当事件满足，其“计划执行时间”落入该时间段范围内时，该事件将被检索命中并返回。:::', examples=['2025-09-01T17:40:53.000Z'])]] = None,
                            planned_begin_time_search_range_start: Optional[Annotated[str,Field(description='按照“计划执行时间”查询事件时的时间区间的起点。格式：`yyyy-MM-ddTHH:mm:ss.sssZ`（UTC 时间）。', examples=['2025-09-01T02:06:53.000Z'])]] = None,
                            planned_switch_time_search_range_end: Optional[Annotated[str,Field(description='按照“计划切换时间”查询事件时的时间区间的终点。格式：`yyyy-MM-ddTHH:mm:ss.sssZ`（UTC 时间）。PlannedSwitchTimeSearchRangeStart 与 PlannedSwitchTimeSearchRangeEnd 定义了一个时间段。当事件的“计划切换时间段”与该时间段范围有重叠时，该事件将被返回。', examples=['2025-09-01T18:47:28.000Z'])]] = None,
                            planned_switch_time_search_range_start: Optional[Annotated[str,Field(description='按照“计划切换时间”查询事件时的时间区间的起点。格式：`yyyy-MM-ddTHH:mm:ss.sssZ`（UTC 时间）。', examples=['2025-09-01T18:17:28.000Z'])]] = None,
                            status: Optional[Annotated[list[str],Field(description='运维事件的状态。取值范围（可取多个值）：- `Canceled`：已取消。- `WaitStart`：待执行。- `WaitSwitch`：待切换。- `Running`：运行中。- `Running_BeforeSwitch`：运行中-切换前。- `Running_Switching`：运行中-切换中。- `Running_AfterSwitch`：运行中-切换后。- `Success`：成功。- `Failed`：失败。- `Timeout`：超时。- `Rollbacking`：回滚中。- `RollbackFailed`：回滚失败。', examples=['["WaitStart"]'])]] = None) -> dict[str, Any]:
    """调用 DescribePlannedEvents 接口查询当前地域下的运维事件。

    Args:
        event_id (str, optional): 事件 ID。
            示例值：61c7adeb0f49426ab032cb8cf1e2****
        event_type (list[str], optional): 事件类型。取值范围（可取多个值）：
            - `VersionUpgrade`：版本升级。
            - `HostOffline`：主机下线。
            示例值：["VersionUpgrade"]
        instance_id (str, optional): 实例 ID。
            示例值：postgres-a2f9831f****
        instance_name (str, optional): 实例名称。
            示例值：测试实例
        page_number (int, optional): 当前页查询偏移量，默认值为 1。
            示例值：2
        page_size (int, optional): 每页记录数，取值应大于 0 且不超过 1000，默认值为 10。
            示例值：20
        planned_begin_time_search_range_end (str, optional): 按照“计划执行时间”查询事件时的时间区间的终点。格式：`yyyy-MM-ddTHH:mm:ss.sssZ`（UTC 时间）。
            :::tip
            - PlannedBeginTimeSearchRangeEnd 应晚于 PlannedBeginTimeSearchRangeStart。
            - PlannedBeginTimeSearchRangeStart 与 PlannedBeginTimeSearchRangeEnd 定义了一个时间段。当事件满足，其“计划执行时间”落入该时间段范围内时，该事件将被检索命中并返回。
            :::
            示例值：2025-09-01T17:40:53.000Z
        planned_begin_time_search_range_start (str, optional): 按照“计划执行时间”查询事件时的时间区间的起点。格式：`yyyy-MM-ddTHH:mm:ss.sssZ`（UTC 时间）。
            示例值：2025-09-01T02:06:53.000Z
        planned_switch_time_search_range_end (str, optional): 按照“计划切换时间”查询事件时的时间区间的终点。格式：`yyyy-MM-ddTHH:mm:ss.sssZ`（UTC 时间）。
            PlannedSwitchTimeSearchRangeStart 与 PlannedSwitchTimeSearchRangeEnd 定义了一个时间段。当事件的“计划切换时间段”与该时间段范围有重叠时，该事件将被返回。
            示例值：2025-09-01T18:47:28.000Z
        planned_switch_time_search_range_start (str, optional): 按照“计划切换时间”查询事件时的时间区间的起点。格式：`yyyy-MM-ddTHH:mm:ss.sssZ`（UTC 时间）。
            示例值：2025-09-01T18:17:28.000Z
        status (list[str], optional): 运维事件的状态。取值范围（可取多个值）：
            - `Canceled`：已取消。
            - `WaitStart`：待执行。
            - `WaitSwitch`：待切换。
            - `Running`：运行中。
            - `Running_BeforeSwitch`：运行中-切换前。
            - `Running_Switching`：运行中-切换中。
            - `Running_AfterSwitch`：运行中-切换后。
            - `Success`：成功。
            - `Failed`：失败。
            - `Timeout`：超时。
            - `Rollbacking`：回滚中。
            - `RollbackFailed`：回滚失败。
            示例值：["WaitStart"]

    Returns: 包含以下字段的字典
        planned_events (list[dict[str, Any]], optional): 当前地域内在当前查询条件下的运维事件列表。
            示例值：请参见返回示例。
        total (int, optional): 运维事件总数。
            示例值：4
    """
    req = {
        "event_id": event_id,
        "event_type": event_type,
        "instance_id": instance_id,
        "instance_name": instance_name,
        "page_number": page_number,
        "page_size": page_size,
        "planned_begin_time_search_range_end": planned_begin_time_search_range_end,
        "planned_begin_time_search_range_start": planned_begin_time_search_range_start,
        "planned_switch_time_search_range_end": planned_switch_time_search_range_end,
        "planned_switch_time_search_range_start": planned_switch_time_search_range_start,
        "status": status,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_planned_events(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="get_backup_download_link",
    description="调用 GetBackupDownloadLink 接口获取备份的下载链接。"
)
def get_backup_download_link(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-a3e7eb2f****'])],
                             backup_id: Annotated[str, Field(description='待下载的逻辑备份的 ID。', examples=['20250512-194654-3836LI'])]) -> dict[str, Any]:
    """调用 GetBackupDownloadLink 接口获取备份的下载链接。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-a3e7eb2f****
        backup_id (str): 待下载的逻辑备份的 ID。
            示例值：20250512-194654-3836LI

    Returns: 包含以下字段的字典
        backup_description (str, optional): 备份集的描述信息。
            示例值：This is a description of the backup set.
        backup_download_link (str, optional): 备份的公网下载地址。
            示例值：请参见返回示例。
        backup_file_name (str, optional): 备份文件名。
            示例值：postgres-a3e7eb2f****-20250512-194654-3836LI.zip
        backup_file_size (int, optional): 备份文件大小，单位为 Byte。
            示例值：1024
        backup_id (str, optional): 备份的 ID。
            示例值：20250512-194654-3836LI
        backup_method (str, optional): 备份类型。取值：
            - `Physical`：物理备份。默认值。
            - `Logical`：逻辑备份。
            :::tip
            当 BackupScope 取值为 `Database` 时，BackupMethod 只能取值 `Logical`。
            :::
            示例值：Logical
        inner_backup_download_link (str, optional): 备份的私网下载地址。
            示例值：请参见返回示例。
        instance_id (str, optional): 实例 ID。
            示例值：postgres-a3e7eb2f****
        link_expired_time (str, optional): 下载链接过期时间，格式：`yyyy-MM-ddTHH:mm:ss.sssZ`（UTC 时间）。
            示例值：2025-05-19T14:03:27.603Z
        prepare_progess (int, optional): 备份文件的准备进度。调用 [DownloadBackup](https://www.volcengine.com/docs/6438/1555135) 开始下载备份的前置工作后，可通过此参数查看备份文件的准备进度，单位为 %。
            示例值：100
    """
    req = {
        "instance_id": instance_id,
        "backup_id": backup_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.get_backup_download_link(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="clone_database",
    description="调用 CloneDatabase 接口克隆已有数据库。"
)
def clone_database(instance_id: Annotated[str, Field(description='实例 ID', examples=['postgres-a3e7eb2f****'])],
                   source_db_name: Annotated[str, Field(description='源数据库名称。', examples=['database'])],
                   data_option: Optional[Annotated[str,Field(description='DataOption', examples=[''])]] = None,
                   new_db_name: Optional[Annotated[str,Field(description='设定新数据库的名称。数据库名称应满足以下规则：- 在实例内名称唯一。- 长度为 2~63 个字符。- 以字母开头，以字母或数字结尾。- 由字母、数字、下划线（\_）或中划线（-）组成。- 在数据库名称中禁用某些预留字或关键词，所有被禁用的关键词请参见[禁用关键词](https://www.volcengine.com/docs/6438/80243)。:::tip如不设定，则默认以`源数据库名称`+`_clone_`+`时间戳`为新数据库命名。:::', examples=['database_clone'])]] = None,
                   plpgsql_option: Optional[Annotated[str,Field(description='克隆数据库的 PL/pgSQL 选项。可取多个值，多个值之间用英文逗号（,）分隔。- `View`：视图。- `Procedure`：存储过程。- `Function`：函数。- `Trigger`：触发器。', examples=['View,Procedure'])]] = None) -> dict[str, Any]:
    """调用 CloneDatabase 接口克隆已有数据库。

    Args:
        instance_id (str): 实例 ID
            示例值：postgres-a3e7eb2f****
        source_db_name (str): 源数据库名称。
            示例值：database
        data_option (str, optional): DataOption
        new_db_name (str, optional): 设定新数据库的名称。数据库名称应满足以下规则：
            - 在实例内名称唯一。
            - 长度为 2~63 个字符。
            - 以字母开头，以字母或数字结尾。
            - 由字母、数字、下划线（\_）或中划线（-）组成。
            - 在数据库名称中禁用某些预留字或关键词，所有被禁用的关键词请参见[禁用关键词](https://www.volcengine.com/docs/6438/80243)。
            :::tip
            如不设定，则默认以`源数据库名称`+`_clone_`+`时间戳`为新数据库命名。
            :::
            示例值：database_clone
        plpgsql_option (str, optional): 克隆数据库的 PL/pgSQL 选项。可取多个值，多个值之间用英文逗号（,）分隔。
            - `View`：视图。
            - `Procedure`：存储过程。
            - `Function`：函数。
            - `Trigger`：触发器。
            示例值：View,Procedure
    """
    req = {
        "instance_id": instance_id,
        "source_db_name": source_db_name,
        "data_option": data_option,
        "new_db_name": new_db_name,
        "plpgsql_option": plpgsql_option,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.clone_database(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="describe_slots",
    description="调用 DescribeSlots 接口查询复制槽列表。"
)
def describe_slots(instance_id: Annotated[str, Field(description='复制槽所属实例的 ID。', examples=['postgres-96138f57****'])],
                   database: Optional[Annotated[str,Field(description='复制槽所处的数据库。:::tip- 当 SlotType 取值为 `physical` 时，不需为该字段传值。- 无默认值。不传该字段时返回其他参数所限定的查询条件下所有查询结果。:::', examples=['postgres'])]] = None,
                   ip_address: Optional[Annotated[str,Field(description='IP 地址。', examples=['10.xxx.xxx.1'])]] = None,
                   plugin: Optional[Annotated[str,Field(description='逻辑复制槽配合解析 WAL 日志的插件名称。:::tip- 当 SlotType 取值为 `physical` 时，不需为该字段传值。- 无默认值。不传该字段时返回其他参数所限定的查询条件下所有查询结果。:::', examples=['pgoutput'])]] = None,
                   slot_name: Optional[Annotated[str,Field(description='要查询的复制槽的名称。:::tip无默认值。不传该字段时返回其他参数所限定的查询条件下所有查询结果。:::', examples=['ExampleOfSlotName'])]] = None,
                   slot_status: Optional[Annotated[str,Field(description='复制槽的状态。取值：- `ACTIVE`：活跃。- `INACTIVE`：不活跃。:::tip无默认值。不传该字段时返回其他参数所限定的查询条件下所有查询结果。:::', examples=['ACTIVE'])]] = None,
                   slot_type: Optional[Annotated[str,Field(description='复制槽的类型。取值：- `physical`：物理复制槽。- `logical`：逻辑复制槽。:::tip无默认值。不传该字段时返回其他参数所限定的查询条件下所有查询结果。:::', examples=['logical'])]] = None,
                   temporary: Optional[Annotated[bool,Field(description='是否为临时的复制槽。取值：- `true`：是。- `false`：否。:::tip无默认值。不传该字段时返回其他参数所限定的查询条件下所有查询结果。:::', examples=['true'])]] = None) -> dict[str, Any]:
    """调用 DescribeSlots 接口查询复制槽列表。

    Args:
        instance_id (str): 复制槽所属实例的 ID。
            示例值：postgres-96138f57****
        database (str, optional): 复制槽所处的数据库。
            :::tip
            - 当 SlotType 取值为 `physical` 时，不需为该字段传值。
            - 无默认值。不传该字段时返回其他参数所限定的查询条件下所有查询结果。
            :::
            示例值：postgres
        ip_address (str, optional): IP 地址。
            示例值：10.xxx.xxx.1
        plugin (str, optional): 逻辑复制槽配合解析 WAL 日志的插件名称。
            :::tip
            - 当 SlotType 取值为 `physical` 时，不需为该字段传值。
            - 无默认值。不传该字段时返回其他参数所限定的查询条件下所有查询结果。
            :::
            示例值：pgoutput
        slot_name (str, optional): 要查询的复制槽的名称。
            :::tip
            无默认值。不传该字段时返回其他参数所限定的查询条件下所有查询结果。
            :::
            示例值：ExampleOfSlotName
        slot_status (str, optional): 复制槽的状态。取值：
            - `ACTIVE`：活跃。
            - `INACTIVE`：不活跃。
            :::tip
            无默认值。不传该字段时返回其他参数所限定的查询条件下所有查询结果。
            :::
            示例值：ACTIVE
        slot_type (str, optional): 复制槽的类型。取值：
            - `physical`：物理复制槽。
            - `logical`：逻辑复制槽。
            :::tip
            无默认值。不传该字段时返回其他参数所限定的查询条件下所有查询结果。
            :::
            示例值：logical
        temporary (bool, optional): 是否为临时的复制槽。取值：
            - `true`：是。
            - `false`：否。
            :::tip
            无默认值。不传该字段时返回其他参数所限定的查询条件下所有查询结果。
            :::
            示例值：true

    Returns: 包含以下字段的字典
        replication_slots (list[dict[str, Any]], optional): 实例中指定查询条件下的复制槽。
            示例值：请参见返回示例。
        total (int, optional): 实例的复制槽数量。
            示例值：3
    """
    req = {
        "instance_id": instance_id,
        "database": database,
        "ip_address": ip_address,
        "plugin": plugin,
        "slot_name": slot_name,
        "slot_status": slot_status,
        "slot_type": slot_type,
        "temporary": temporary,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_slots(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="describe_allow_list_detail",
    description="调用 DescribeAllowListDetail 接口查看白名单详情。"
)
def describe_allow_list_detail(allow_list_id: Annotated[str, Field(description='白名单的 ID。', examples=['acl-fe1339b0024e42ca9872e8f4af12****'])]) -> dict[str, Any]:
    """调用 DescribeAllowListDetail 接口查看白名单详情。

    Args:
        allow_list_id (str): 白名单的 ID。
            示例值：acl-fe1339b0024e42ca9872e8f4af12****

    Returns: 包含以下字段的字典
        allow_list (str, optional): 白名单包含的所有的 IP 地址或 IP 地址段列表。
            示例值：10.1.1.1,10.2.2.0/24
        allow_list_category (str, optional): 白名单分类。取值：
            - `Ordinary`：普通白名单。
            - `Default`：默认白名单。
            :::tip
            该参数作为请求参数时无默认值，不传入时则查询所有类别的白名单。
            :::
            示例值：Default
        allow_list_desc (str, optional): 白名单的描述信息。
            示例值：这是一段白名单的描述信息。
        allow_list_id (str, optional): 白名单的 ID。
            示例值：acl-fe1339b0024e42ca9872e8f4af12****
        allow_list_name (str, optional): 白名单的名称。
            示例值：测试白名单
        allow_list_type (str, optional): 白名单采用的网络协议类型。取值为 `IPv4`。
            示例值：IPv4
        associated_instance_num (int, optional): 该白名单绑定的实例数量。
            示例值：8
        associated_instances (list[dict[str, Any]], optional): 该白名单绑定的实例列表，包含实例 ID 和实例名称信息。
            示例值：请参见返回示例。
        security_group_bind_infos (list[dict[str, Any]], optional): 该白名单绑定的安全组列表。
            示例值：请参见返回示例。
        user_allow_list (str, optional): 安全组之外的、加入白名单的 IP 地址。
            示例值：10.1.1.1,10.2.3.0/24
    """
    req = {
        "allow_list_id": allow_list_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_allow_list_detail(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="describe_allow_lists",
    description="调用 DescribeAllowLists 接口查看指定地域下的白名单列表。"
)
def describe_allow_lists(region_id: Annotated[str, Field(description='地域 ID，可调用 [DescribeRegions](https://www.volcengine.com/docs/6438/1159931) 接口查询。', examples=['cn-beijing'])],
                         allow_list_category: Optional[Annotated[str,Field(description='白名单分类。取值：- `Ordinary`：普通白名单。- `Default`：默认白名单。:::tip该参数作为请求参数时无默认值，不传入时则查询所有类别的白名单。:::', examples=['Default'])]] = None,
                         allow_list_desc: Optional[Annotated[str,Field(description='白名单的描述信息。可通过描述信息进行模糊搜索。', examples=['这是一段白名单的描述信息。'])]] = None,
                         allow_list_id: Optional[Annotated[str,Field(description='白名单 ID。', examples=['acl-fe1339b0024e42ca9872e8f4af12****'])]] = None,
                         allow_list_name: Optional[Annotated[str,Field(description='白名单的名称。', examples=['Test_Allowlist'])]] = None,
                         instance_id: Optional[Annotated[str,Field(description='实例 ID。:::tip如不设定该字段，返回当前地域下的所有白名单。如设定该字段，则返回该实例的所有白名单。:::', examples=['postgres-sdasd***'])]] = None,
                         ip_address: Optional[Annotated[str,Field(description='按 IP 地址查询白名单。支持传入多个 IP 地址，多个 IP 地址使用英文逗号（,）分隔。:::tip如果白名单包含了多个 IP 地址的任意子集，该白名单就会被返回。:::', examples=['"2.2.2.2,1.1.1.1"'])]] = None,
                         page_number: Optional[Annotated[int,Field(description='当前页页码。取值最小为 1。默认值为 1。', examples=['2'])]] = None,
                         page_size: Optional[Annotated[int,Field(description='每页记录数。取值最小为 1，且不超过 Integer 的最大值。无默认值。', examples=['20'])]] = None) -> dict[str, Any]:
    """调用 DescribeAllowLists 接口查看指定地域下的白名单列表。

    Args:
        region_id (str): 地域 ID，可调用 [DescribeRegions](https://www.volcengine.com/docs/6438/1159931) 接口查询。
            示例值：cn-beijing
        allow_list_category (str, optional): 白名单分类。取值：
            - `Ordinary`：普通白名单。
            - `Default`：默认白名单。
            :::tip
            该参数作为请求参数时无默认值，不传入时则查询所有类别的白名单。
            :::
            示例值：Default
        allow_list_desc (str, optional): 白名单的描述信息。可通过描述信息进行模糊搜索。
            示例值：这是一段白名单的描述信息。
        allow_list_id (str, optional): 白名单 ID。
            示例值：acl-fe1339b0024e42ca9872e8f4af12****
        allow_list_name (str, optional): 白名单的名称。
            示例值：Test_Allowlist
        instance_id (str, optional): 实例 ID。
            :::tip
            如不设定该字段，返回当前地域下的所有白名单。如设定该字段，则返回该实例的所有白名单。
            :::
            示例值：postgres-sdasd***
        ip_address (str, optional): 按 IP 地址查询白名单。支持传入多个 IP 地址，多个 IP 地址使用英文逗号（,）分隔。
            :::tip
            如果白名单包含了多个 IP 地址的任意子集，该白名单就会被返回。
            :::
            示例值："2.2.2.2,1.1.1.1"
        page_number (int, optional): 当前页页码。取值最小为 1。默认值为 1。
            示例值：2
        page_size (int, optional): 每页记录数。取值最小为 1，且不超过 Integer 的最大值。无默认值。
            示例值：20

    Returns: 包含以下字段的字典
        allow_lists (list[dict[str, Any]], optional): 白名单信息。
            示例值：请参见返回示例。
        total (int, optional): 白名单的总数。
            示例值：20
    """
    req = {
        "region_id": region_id,
        "allow_list_category": allow_list_category,
        "allow_list_desc": allow_list_desc,
        "allow_list_id": allow_list_id,
        "allow_list_name": allow_list_name,
        "instance_id": instance_id,
        "ip_address": ip_address,
        "page_number": page_number,
        "page_size": page_size,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_allow_lists(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="revoke_db_account_privilege",
    description="调用 RevokeDBAccountPrivilege 接口清空对数据库账号的授权。"
)
def revoke_db_account_privilege(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-ca7b7019****'])],
                                account_name: Annotated[str, Field(description='数据库账号名称。', examples=['testuser'])]) -> dict[str, Any]:
    """调用 RevokeDBAccountPrivilege 接口清空对数据库账号的授权。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-ca7b7019****
        account_name (str): 数据库账号名称。
            示例值：testuser
    """
    req = {
        "instance_id": instance_id,
        "account_name": account_name,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.revoke_db_account_privilege(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="modify_db_endpoint_name",
    description="调用 ModifyDBEndpointName 接口修改连接终端名称。"
)
def modify_db_endpoint_name(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-0af11cd4****'])],
                            endpoint_id: Annotated[str, Field(description='实例连接终端 ID。', examples=['postgres-0af11cd4****-cluster'])],
                            endpoint_name: Annotated[str, Field(description='实例连接终端名称。连接终端的命名规则如下：- 不能以数字、中划线（-）开头。- 只能包含中文、字母、数字、下划线（_）和中划线（-）。- 长度为 1~64 个字符。', examples=['终端名称'])]) -> dict[str, Any]:
    """调用 ModifyDBEndpointName 接口修改连接终端名称。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-0af11cd4****
        endpoint_id (str): 实例连接终端 ID。
            示例值：postgres-0af11cd4****-cluster
        endpoint_name (str): 实例连接终端名称。连接终端的命名规则如下：
            - 不能以数字、中划线（-）开头。
            - 只能包含中文、字母、数字、下划线（_）和中划线（-）。
            - 长度为 1~64 个字符。
            示例值：终端名称
    """
    req = {
        "instance_id": instance_id,
        "endpoint_id": endpoint_id,
        "endpoint_name": endpoint_name,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.modify_db_endpoint_name(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="describe_detached_backups",
    description="调用 DescribeDetachedBackups 接口查询已删除实例备份。"
)
def describe_detached_backups(backup_end_time: Optional[Annotated[str,Field(description='备份创建最晚时间。以备份开始时间为准。格式为 `yyyy-MM-ddTHH:mm:ss.sssZ`（UTC 时间）。:::tip无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。:::', examples=['2022-01-01T10:10:10.000Z'])]] = None,
                              backup_id: Optional[Annotated[str,Field(description='备份 ID。', examples=['20231016-024****'])]] = None,
                              backup_start_time: Optional[Annotated[str,Field(description='备份创建最早时间。以备份开始时间为准。格式为 `yyyy-MM-ddTHH:mm:ss.sssZ`（UTC 时间）。:::tip无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。:::', examples=['2022-01-01T10:10:10.000Z'])]] = None,
                              backup_status: Optional[Annotated[str,Field(description='备份状态。可不设置，默认取值为 `Success`，即查询状态为成功的备份。', examples=['Success'])]] = None,
                              backup_type: Optional[Annotated[str,Field(description='备份类型。可不设置，默认值取值为 `Full`，即查询全量备份。', examples=['Full'])]] = None,
                              instance_id: Optional[Annotated[str,Field(description='实例 ID。:::tip无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。:::', examples=['postgres-5704170c****'])]] = None,
                              instance_name: Optional[Annotated[str,Field(description='实例名称。:::tip无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。:::', examples=['测试实例'])]] = None,
                              page_number: Optional[Annotated[int,Field(description='当前页查询偏移量，默认值为 1。', examples=['1'])]] = None,
                              page_size: Optional[Annotated[int,Field(description='每页记录数，取值应大于 0 且不超过 1000，默认值为 10。', examples=['10'])]] = None,
                              project_name: Optional[Annotated[str,Field(description='实例所属的项目。:::tip无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。:::', examples=['Test'])]] = None) -> dict[str, Any]:
    """调用 DescribeDetachedBackups 接口查询已删除实例备份。

    Args:
        backup_end_time (str, optional): 备份创建最晚时间。以备份开始时间为准。格式为 `yyyy-MM-ddTHH:mm:ss.sssZ`（UTC 时间）。
            :::tip
            无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。
            :::
            示例值：2022-01-01T10:10:10.000Z
        backup_id (str, optional): 备份 ID。
            示例值：20231016-024****
        backup_start_time (str, optional): 备份创建最早时间。以备份开始时间为准。格式为 `yyyy-MM-ddTHH:mm:ss.sssZ`（UTC 时间）。
            :::tip
            无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。
            :::
            示例值：2022-01-01T10:10:10.000Z
        backup_status (str, optional): 备份状态。可不设置，默认取值为 `Success`，即查询状态为成功的备份。
            示例值：Success
        backup_type (str, optional): 备份类型。可不设置，默认值取值为 `Full`，即查询全量备份。
            示例值：Full
        instance_id (str, optional): 实例 ID。
            :::tip
            无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。
            :::
            示例值：postgres-5704170c****
        instance_name (str, optional): 实例名称。
            :::tip
            无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。
            :::
            示例值：测试实例
        page_number (int, optional): 当前页查询偏移量，默认值为 1。
            示例值：1
        page_size (int, optional): 每页记录数，取值应大于 0 且不超过 1000，默认值为 10。
            示例值：10
        project_name (str, optional): 实例所属的项目。
            :::tip
            无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。
            :::
            示例值：Test

    Returns: 包含以下字段的字典
        backups (list[dict[str, Any]], optional): 备份列表。
            示例值：请参见返回示例。
        total (int, optional): 备份总数。
            示例值：1
    """
    req = {
        "backup_end_time": backup_end_time,
        "backup_id": backup_id,
        "backup_start_time": backup_start_time,
        "backup_status": backup_status,
        "backup_type": backup_type,
        "instance_id": instance_id,
        "instance_name": instance_name,
        "page_number": page_number,
        "page_size": page_size,
        "project_name": project_name,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_detached_backups(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="describe_backup_policy",
    description="调用 DescribeBackupPolicy 接口查询备份策略。"
)
def describe_backup_policy(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-ca7b7019****'])]) -> dict[str, Any]:
    """调用 DescribeBackupPolicy 接口查询备份策略。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-ca7b7019****

    Returns: 包含以下字段的字典
        backup_retention_period (int, optional): 备份保留天数，取值范围：7~365。
            示例值：7
        data_incr_backup_periods (str, optional): 备份方式为正常增量时的备份频率，多个取值用英文逗号（,）隔开。取值：
            - `Monday`：周一
            - `Tuesday`：周二
            - `Wednesday`：周三
            - `Thursday`：周四
            - `Friday`：周五
            - `Saturday`：周六
            - `Sunday`：周日
            :::tip
            实例未开启增量备份时则不返回该字段。
            :::
            示例值：Tuesday,Thursday
        full_backup_period (str, optional): 全量备份周期。每周至少需要指定 1 天，多个取值用英文逗号（,）隔开。取值：
            - `Monday`：周一。
            - `Tuesday`：周二。
            - `Wednesday`：周三。
            - `Thursday`：周四。
            - `Friday`：周五。
            - `Saturday`：周六。
            - `Sunday`：周日。
            示例值：Monday,Wednesday,Friday,Sunday
        full_backup_time (str, optional): 执行备份任务的时间。格式：`HH:mmZ-HH:mmZ`（UTC 时间）。
            示例值：02:00Z-03:00Z
        hourly_incr_backup_enable (bool, optional): 是否开启高频备份功能。取值:
            - `true`：是。
            - `false`：否。
            示例值：false
        increment_backup_frequency (int, optional): 增量备份的方式为高频增量时的备份频率。取值可为：`1`、`2`、`4`、`6` 或 `12`，单位：小时。
            :::tip
            该参数仅在 HourlyIncrBackupEnable 取值为 `true` 时生效。
            :::
            示例值：2
        instance_id (str, optional): 实例 ID。
            示例值：postgres-ca7b7019****
        wal_log_space_limit_enable (bool, optional): 本地剩余可用空间保护功能状态。开启时，会在实例总存储空间占用率超过 80% 或者剩余空间不足 5GB 时，自动开始清除最早的本地 WAL 日志，直至总空间占用率低于 80% 且剩余空间大于 5GB。取值范围：
            - `true`：开启。
            - `false`：关闭。
            示例值：false
    """
    req = {
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_backup_policy(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="describe_backups",
    description="调用 DescribeBackups 接口查询备份列表。"
)
def describe_backups(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-21a3333b****'])],
                     backup_database_name: Optional[Annotated[str,Field(description='备份集中包含的数据库名称。指定该字段后，会以该字段为关键词搜索备份集包含的数据库名称。:::tip仅在 BackupMethod 取值为 `Logical` 时生效。:::', examples=['database1'])]] = None,
                     backup_description: Optional[Annotated[str,Field(description='备份集的描述信息。', examples=['This is a description of the backup set.'])]] = None,
                     backup_end_time: Optional[Annotated[str,Field(description='备份创建最晚时间，格式为 `yyyy-MM-ddTHH:mm:ss.sssZ`（UTC 时间）。:::tip- 以备份开始时间为准。- 无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。:::', examples=['2023-10-19T06:20:08.000Z'])]] = None,
                     backup_id: Optional[Annotated[str,Field(description='备份 ID。:::tip无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。:::', examples=['20231101-021****_20231101-101****'])]] = None,
                     backup_method: Optional[Annotated[str,Field(description='备份类型。取值：- `Physical`：物理备份。默认值。- `Logical`：逻辑备份。:::tip当 BackupScope 取值为 `Database` 时，BackupMethod 只能取值 `Logical`。:::', examples=['Logical'])]] = None,
                     backup_scope: Optional[Annotated[str,Field(description='备份对象。取值：- `Instance`：整个实例。默认值。- `Database`：指定库。', examples=['Database'])]] = None,
                     backup_start_time: Optional[Annotated[str,Field(description='备份创建最早时间，格式为 `yyyy-MM-ddTHH:mm:ss.sssZ`（UTC 时间）。:::tip- 以备份开始时间为准。- 无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。:::', examples=['2023-10-19T06:20:06.000Z'])]] = None,
                     backup_status: Optional[Annotated[str,Field(description='备份状态，取值：- `Success`：成功。- `Failed`：失败。- `Running`：执行中。', examples=['Success'])]] = None,
                     backup_type: Optional[Annotated[str,Field(description='备份类型，取值：- `Full`：全量备份。- `Increment`：增量备份。:::tip无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。:::', examples=['Full'])]] = None,
                     create_type: Optional[Annotated[str,Field(description='创建类型，取值：- `System`：系统。- `User`：用户。:::tip无默认值。不指定时，则返回其他查询条件限定的备份。:::', examples=['System'])]] = None,
                     download_status: Optional[Annotated[str,Field(description='备份集的可下载状态。取值：- `NotAllowed`：不支持下载。:::tip当前物理备份不支持下载。:::- `NeedToPrepare`：备份集已就位，需要后台准备备份（即BackupStatus 为 Success，需发起“获取备份文件”任务）。- `LinkReady`：备份集准备完毕，并且备份的下载链接仍处于有效期中。', examples=['NotAllowed'])]] = None,
                     page_number: Optional[Annotated[int,Field(description='当前页查询偏移量，默认值为 1。', examples=['1'])]] = None,
                     page_size: Optional[Annotated[int,Field(description='每页记录数，取值应大于 0 且不超过 1000，默认值为 10。', examples=['10'])]] = None) -> dict[str, Any]:
    """调用 DescribeBackups 接口查询备份列表。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-21a3333b****
        backup_database_name (str, optional): 备份集中包含的数据库名称。指定该字段后，会以该字段为关键词搜索备份集包含的数据库名称。
            :::tip
            仅在 BackupMethod 取值为 `Logical` 时生效。
            :::
            示例值：database1
        backup_description (str, optional): 备份集的描述信息。
            示例值：This is a description of the backup set.
        backup_end_time (str, optional): 备份创建最晚时间，格式为 `yyyy-MM-ddTHH:mm:ss.sssZ`（UTC 时间）。
            :::tip
            - 以备份开始时间为准。
            - 无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。
            :::
            示例值：2023-10-19T06:20:08.000Z
        backup_id (str, optional): 备份 ID。
            :::tip
            无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。
            :::
            示例值：20231101-021****_20231101-101****
        backup_method (str, optional): 备份类型。取值：
            - `Physical`：物理备份。默认值。
            - `Logical`：逻辑备份。
            :::tip
            当 BackupScope 取值为 `Database` 时，BackupMethod 只能取值 `Logical`。
            :::
            示例值：Logical
        backup_scope (str, optional): 备份对象。取值：
            - `Instance`：整个实例。默认值。
            - `Database`：指定库。
            示例值：Database
        backup_start_time (str, optional): 备份创建最早时间，格式为 `yyyy-MM-ddTHH:mm:ss.sssZ`（UTC 时间）。
            :::tip
            - 以备份开始时间为准。
            - 无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。
            :::
            示例值：2023-10-19T06:20:06.000Z
        backup_status (str, optional): 备份状态，取值：
            - `Success`：成功。
            - `Failed`：失败。
            - `Running`：执行中。
            示例值：Success
        backup_type (str, optional): 备份类型，取值：
            - `Full`：全量备份。
            - `Increment`：增量备份。
            :::tip
            无默认值。不传该字段时返回其他参数所限定的查询条件下所有备份。
            :::
            示例值：Full
        create_type (str, optional): 创建类型，取值：
            - `System`：系统。
            - `User`：用户。
            :::tip
            无默认值。不指定时，则返回其他查询条件限定的备份。
            :::
            示例值：System
        download_status (str, optional): 备份集的可下载状态。取值：
            - `NotAllowed`：不支持下载。
            :::tip
            当前物理备份不支持下载。
            :::
            - `NeedToPrepare`：备份集已就位，需要后台准备备份（即BackupStatus 为 Success，需发起“获取备份文件”任务）。
            - `LinkReady`：备份集准备完毕，并且备份的下载链接仍处于有效期中。
            示例值：NotAllowed
        page_number (int, optional): 当前页查询偏移量，默认值为 1。
            示例值：1
        page_size (int, optional): 每页记录数，取值应大于 0 且不超过 1000，默认值为 10。
            示例值：10

    Returns: 包含以下字段的字典
        backups (list[dict[str, Any]], optional): 备份列表。
            示例值：请参见返回示例。
        total (int, optional): 备份总数。
            示例值：1
    """
    req = {
        "instance_id": instance_id,
        "backup_database_name": backup_database_name,
        "backup_description": backup_description,
        "backup_end_time": backup_end_time,
        "backup_id": backup_id,
        "backup_method": backup_method,
        "backup_scope": backup_scope,
        "backup_start_time": backup_start_time,
        "backup_status": backup_status,
        "backup_type": backup_type,
        "create_type": create_type,
        "download_status": download_status,
        "page_number": page_number,
        "page_size": page_size,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_backups(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="modify_db_instance_name",
    description="调用 ModifyDBInstanceName 接口修改实例名称。"
)
def modify_db_instance_name(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-21a3333b****'])],
                            instance_new_name: Annotated[str, Field(description='实例新名称。实例新名称的设定规则如下：- 不能以数字、中划线开头。- 只能包含中文、字母、数字、下划线和中划线。- 长度限制在 1 ~ 128 之间。', examples=['Name123'])]) -> dict[str, Any]:
    """调用 ModifyDBInstanceName 接口修改实例名称。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-21a3333b****
        instance_new_name (str): 实例新名称。实例新名称的设定规则如下：
            - 不能以数字、中划线开头。
            - 只能包含中文、字母、数字、下划线和中划线。
            - 长度限制在 1 ~ 128 之间。
            示例值：Name123
    """
    req = {
        "instance_id": instance_id,
        "instance_new_name": instance_new_name,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.modify_db_instance_name(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="describe_db_instance_parameters",
    description="调用 DescribeDBInstanceParameters 接口查询实例的参数配置。"
)
def describe_db_instance_parameters(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-21a3333b****'])],
                                    parameter_name: Optional[Annotated[str,Field(description='参数名称，支持模糊查询。:::tip不传值或传空值时，会查询指定实例下的所有参数。:::', examples=['auto_explain.log_analyze'])]] = None) -> dict[str, Any]:
    """调用 DescribeDBInstanceParameters 接口查询实例的参数配置。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-21a3333b****
        parameter_name (str, optional): 参数名称，支持模糊查询。
            :::tip
            不传值或传空值时，会查询指定实例下的所有参数。
            :::
            示例值：auto_explain.log_analyze

    Returns: 包含以下字段的字典
        db_engine_version (str, optional): 兼容版本。取值：
            - `PostgreSQL_11`：PostgreSQL 11。
            - `PostgreSQL_12`：PostgreSQL 12。
            - `PostgreSQL_13`：PostgreSQL 13。
            - `PostgreSQL_14`：PostgreSQL 14。
            - `PostgreSQL_15`：PostgreSQL 15。
            - `PostgreSQL_16`：PostgreSQL 16。
            - `PostgreSQL_17`：PostgreSQL 17。
            示例值：PostgreSQL_12
        instance_id (str, optional): 实例 ID。
            示例值：postgres-21a3333b****
        none_kernel_parameters (list[dict[str, Any]], optional): 实例当前的参数配置（非内核参数）。
            示例值：请参见返回示例。
        parameter_count (str, optional): 参数个数。
            示例值：56
        parameters (list[dict[str, Any]], optional): 实例当前的参数配置（内核参数）。
            示例值：请参见返回示例。
    """
    req = {
        "instance_id": instance_id,
        "parameter_name": parameter_name,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_db_instance_parameters(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="modify_db_instance_parameters",
    description="调用 ModifyDBInstanceParameters 接口修改实例参数。"
)
@validate_call
def modify_db_instance_parameters(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-21a3333b****'])],
                                  parameters: Annotated[list[dict[str, Any]], Field(description='参数值对象，用户基于默认参数模板自定义的参数值。', examples=['请参见请求示例。'])]) -> dict[str, Any]:
    """调用 ModifyDBInstanceParameters 接口修改实例参数。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-21a3333b****
        parameters (list[dict[str, Any]]): 参数值对象，用户基于默认参数模板自定义的参数值。
            示例值：请参见请求示例。
    """
    req = {
        "instance_id": instance_id,
        "parameters": parameters,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.modify_db_instance_parameters(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="modify_db_instance_charge_type",
    description="调用 ModifyDBInstanceChargeType 接口修改实例计费类型。"
)
def modify_db_instance_charge_type(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-21a3333b****'])],
                                   charge_type: Annotated[str, Field(description='付费类型。取值为 `PrePaid`（包年包月）。:::tip仅支持将按量计费类型的实例转为包年包月类型的实例。:::', examples=['PrePaid'])],
                                   auto_renew: Optional[Annotated[bool,Field(description='预付费场景下是否自动续费。- `true`：自动续费。- `false`：不自动续费 (默认)。', examples=['true'])]] = None,
                                   period: Optional[Annotated[int,Field(description='预付费场景下的购买时长。默认值：1。取值范围：- 当 PeriodUnit 取值为 `Month` 时，Period 的取值范围为 1~9。- 当 PeriodUnit 取值为 `Year` 时，Period 的取值范围为 1~3。', examples=['1'])]] = None,
                                   period_unit: Optional[Annotated[str,Field(description='预付费场景下的购买周期。- `Month`：包月（默认）。- `Year`：包年。', examples=['Month'])]] = None) -> dict[str, Any]:
    """调用 ModifyDBInstanceChargeType 接口修改实例计费类型。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-21a3333b****
        charge_type (str): 付费类型。取值为 `PrePaid`（包年包月）。
            :::tip
            仅支持将按量计费类型的实例转为包年包月类型的实例。
            :::
            示例值：PrePaid
        auto_renew (bool, optional): 预付费场景下是否自动续费。
            - `true`：自动续费。
            - `false`：不自动续费 (默认)。
            示例值：true
        period (int, optional): 预付费场景下的购买时长。默认值：1。取值范围：
            - 当 PeriodUnit 取值为 `Month` 时，Period 的取值范围为 1~9。
            - 当 PeriodUnit 取值为 `Year` 时，Period 的取值范围为 1~3。
            示例值：1
        period_unit (str, optional): 预付费场景下的购买周期。
            - `Month`：包月（默认）。
            - `Year`：包年。
            示例值：Month

    Returns: 包含以下字段的字典
        instance_id (str, optional): 实例 ID。
            示例值：postgres-21a3333b****
        order_no (str, optional): 订单 ID。
            示例值：Order709899242175681****
    """
    req = {
        "instance_id": instance_id,
        "charge_type": charge_type,
        "auto_renew": auto_renew,
        "period": period,
        "period_unit": period_unit,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.modify_db_instance_charge_type(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="describe_db_instance_price_difference",
    description="调用 DescribeDBInstancePriceDifference 接口查询实例差价。"
)
@validate_call
def describe_db_instance_price_difference(instance_id: Annotated[str, Field(description='实例 ID。:::tip当 ModifyType 取值为 `Temporary` 时，通过 InstanceId 指定的实例只能为预付费（包年包月）实例。:::', examples=['postgres-5aeb3f0b****'])],
                                          node_info: Annotated[list[dict[str, Any]], Field(description='实例规格配置。Primary 节点有且只有1个，Secondary 节点有且只有 1 个，Read-Only 节点可选 0-10 个。:::tip当 ModifyType 取值为 `Temporary` 时，需要指定 NodeId。:::', examples=['请参见请求示例。'])],
                                          storage_type: Annotated[str, Field(description='实例存储类型。取固定值 `LocalSSD`（本地 SSD 盘）。', examples=['LocalSSD'])],
                                          storage_space: Annotated[int, Field(description='实例存储空间。取值范围：[20, 3000]，单位为 GB，步长为 10GB。默认值：100。:::tip当 ModifyType 取值为 `Temporary` 时，该字段必选，且取值只能为实例当前的存储空间大小。:::', examples=['100'])],
                                          charge_info: Annotated[dict[str, Any], Field(description='付费方式。', examples=[''])]) -> dict[str, Any]:
    """调用 DescribeDBInstancePriceDifference 接口查询实例差价。

    Args:
        instance_id (str): 实例 ID。
            :::tip
            当 ModifyType 取值为 `Temporary` 时，通过 InstanceId 指定的实例只能为预付费（包年包月）实例。
            :::
            示例值：postgres-5aeb3f0b****
        node_info (list[dict[str, Any]]): 实例规格配置。Primary 节点有且只有1个，Secondary 节点有且只有 1 个，Read-Only 节点可选 0-10 个。
            :::tip
            当 ModifyType 取值为 `Temporary` 时，需要指定 NodeId。
            :::
            示例值：请参见请求示例。
        storage_type (str): 实例存储类型。取固定值 `LocalSSD`（本地 SSD 盘）。
            示例值：LocalSSD
        storage_space (int): 实例存储空间。取值范围：[20, 3000]，单位为 GB，步长为 10GB。默认值：100。
            :::tip
            当 ModifyType 取值为 `Temporary` 时，该字段必选，且取值只能为实例当前的存储空间大小。
            :::
            示例值：100
        charge_info (dict[str, Any]): 付费方式。

    Returns: 包含以下字段的字典
        charge_item_prices (list[dict[str, Any]], optional): 费用明细。
            示例值：请参见返回示例
        currency (str, optional): 货币单位。默认为人民币。
            示例值：人民币
        discount_price (float, optional): 实例折扣价。
            示例值：-17.5
        original_price (float, optional): 实例原价。
            示例值：-17.5
        payable_price (float, optional): 实例应付价格。
            示例值：-17.5
    """
    if charge_info is None or node_info is None:
        return {
            "Message": "执行失败，charge_info或node_info不能为空"
        }
    new_node_info = []
    for info in node_info:
        if info is None:
            continue
        new_node_info.append({
            "NodeId": info.get("node_id", ""),
            "ZoneId": info.get("zone_id", ""),
            "NodeType": info.get("node_type", ""),
            "NodeSpec": info.get("node_spec", ""),
            "NodeOperateType": info.get("node_operate_type", ""),
        })
    if charge_info.get("charge_type", "PostPaid") == "PrePaid":
        new_charge_info = {
            "ChargeType": charge_info.get("charge_type", "PrePaid"),
            "AutoRenew": charge_info.get("auto_renew", False),
            "PeriodUnit": charge_info.get("period_unit", "Month"),
            "Period": charge_info.get("period", 1),
            "Number": charge_info.get("number", 1),
        }
    else:
        new_charge_info = {
            "ChargeType": charge_info.get("charge_type", "PrePaid"),
            "Number": charge_info.get("number", 1),
        }

    req = {
        "instance_id": instance_id,
        "node_info": new_node_info,
        "storage_type": storage_type,
        "storage_space": storage_space,
        "charge_info": new_charge_info,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_db_instance_price_difference(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="modify_db_endpoint_dns",
    description="调用 ModifyDBEndpointDNS 接口修改实例私网地址的解析方式。"
)
def modify_db_endpoint_dns(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-21a3333b****'])],
                           network_type: Annotated[str, Field(description='网络类型，取值为 `Private`（私网地址）。', examples=['Private'])],
                           dns_visibility: Annotated[bool, Field(description='是否开启公网解析。- `false`：默认值，火山引擎私网解析。- `true`：火山引擎私网以及公网解析。', examples=['false'])],
                           endpoint_id: Optional[Annotated[str,Field(description='实例连接终端 ID。如不设定，默认选择默认终端。', examples=['postgres-ca7b7019****-custom-f07b'])]] = None) -> dict[str, Any]:
    """调用 ModifyDBEndpointDNS 接口修改实例私网地址的解析方式。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-21a3333b****
        network_type (str): 网络类型，取值为 `Private`（私网地址）。
            示例值：Private
        dns_visibility (bool): 是否开启公网解析。
            - `false`：默认值，火山引擎私网解析。
            - `true`：火山引擎私网以及公网解析。
            示例值：false
        endpoint_id (str, optional): 实例连接终端 ID。如不设定，默认选择默认终端。
            示例值：postgres-ca7b7019****-custom-f07b
    """
    req = {
        "instance_id": instance_id,
        "network_type": network_type,
        "dns_visibility": dns_visibility,
        "endpoint_id": endpoint_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.modify_db_endpoint_dns(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="remove_tags_from_resource",
    description="调用 RemoveTagsFromResource 接口为实例解绑标签。"
)
def remove_tags_from_resource(instance_ids: Annotated[list[str], Field(description='需要解绑标签的实例 ID。:::tip支持一次传入多个实例 ID，最多同时传入 20 个实例 ID。:::', examples=['["postgres-da8f12d3****", "postgres-6b40e576****"]'])],
                              all: Optional[Annotated[bool,Field(description='是否解绑资源上全部的标签。取值范围：- `true`：解绑全部标签。- `false`：默认值，不解绑全部标签。:::tip当请求中 TagKeys 为空时，该参数才有效。:::', examples=['false'])]] = None,
                              tag_keys: Optional[Annotated[list[str],Field(description='待移除的标签的键。:::tip支持一次传入多个标签的键，进行批量解绑。单次最多解绑 20 个标签。:::', examples=['["key1", "key2"]'])]] = None) -> dict[str, Any]:
    """调用 RemoveTagsFromResource 接口为实例解绑标签。

    Args:
        instance_ids (list[str]): 需要解绑标签的实例 ID。
            :::tip
            支持一次传入多个实例 ID，最多同时传入 20 个实例 ID。
            :::
            示例值：["postgres-da8f12d3****", "postgres-6b40e576****"]
        all (bool, optional): 是否解绑资源上全部的标签。取值范围：
            - `true`：解绑全部标签。
            - `false`：默认值，不解绑全部标签。
            :::tip
            当请求中 TagKeys 为空时，该参数才有效。
            :::
            示例值：false
        tag_keys (list[str], optional): 待移除的标签的键。
            :::tip
            支持一次传入多个标签的键，进行批量解绑。单次最多解绑 20 个标签。
            :::
            示例值：["key1", "key2"]
    """
    req = {
        "instance_ids": instance_ids,
        "all": all,
        "tag_keys": tag_keys,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.remove_tags_from_resource(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="add_tags_to_resource",
    description="调用 AddTagsToResource 接口为实例绑定标签。"
)
@validate_call
def add_tags_to_resource(instance_ids: Annotated[list[str], Field(description='实例 ID。:::tip支持传入多个实例 ID，单次最多可传入 20 个实例 ID，单个实例最多绑定 50 个标签。:::', examples=['["postgres-da8f12d3****", "postgres-6b40e576****"]'])],
                         tags: Annotated[list[dict[str, Any]], Field(description='需要绑定的标签键和标签值的数组对象。:::tip支持一次传入多组标签键值对像。单次最多可传入 20 组标签键值对，单个实例最多可绑定 50 个标签。:::', examples=['请参见请求示例。'])]) -> dict[str, Any]:
    """调用 AddTagsToResource 接口为实例绑定标签。

    Args:
        instance_ids (list[str]): 实例 ID。
            :::tip
            支持传入多个实例 ID，单次最多可传入 20 个实例 ID，单个实例最多绑定 50 个标签。
            :::
            示例值：["postgres-da8f12d3****", "postgres-6b40e576****"]
        tags (list[dict[str, Any]]): 需要绑定的标签键和标签值的数组对象。
            :::tip
            支持一次传入多组标签键值对像。单次最多可传入 20 组标签键值对，单个实例最多可绑定 50 个标签。
            :::
            示例值：请参见请求示例。
    """
    req = {
        "instance_ids": instance_ids,
        "tags": tags,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.add_tags_to_resource(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="describe_db_instance_price_detail",
    description="调用 DescribeDBInstancePriceDetail 接口查询实例价格详情。"
)
@validate_call
def describe_db_instance_price_detail(primary_zone: Annotated[str, Field(description='主节点所在可用区', examples=['cn-beijing-a'])],
                                      secondary_zone: Annotated[str, Field(description='备节点所在可用区', examples=['cn-beijing-a'])],
                                      read_only_zone: Annotated[str, Field(description='只读节点所在可用区', examples=['cn-beijing-a'])],
                                      node_spec: Annotated[str, Field(description='节点规格', examples=['rds.postgres.1c2g'])],
                                      read_only_count: Annotated[int, Field(description='只读节点数量', examples=['1'])],
                                      charge_type: Annotated[str, Field(description='付费类型', examples=['PostPaid'])],
                                      auto_renew: Annotated[bool, Field(description='预付费场景下是否自动续费', examples=['false'])],
                                      storage_type: Annotated[str, Field(description='实例存储类型。取固定值 `LocalSSD`（本地 SSD 盘）。', examples=['LocalSSD'])],
                                      storage_space: Annotated[int, Field(description='实例存储空间。取值范围：\[20, 3000\]，单位为 GB，步长为 10GB。', examples=['100'])]) -> dict[str, Any]:
    """调用 DescribeDBInstancePriceDetail 接口查询实例价格详情。

    Args:
        auto_renew: 预付费场景下是否自动续费
        charge_type: 付费类型
        read_only_count: 只读节点数量
        node_spec: 节点规格
        read_only_zone: 只读节点所在可用区
        secondary_zone: 备节点所在可用区
        primary_zone: 主节点所在可用区
        storage_type (str): 实例存储类型。取固定值 `LocalSSD`（本地 SSD 盘）。
            示例值：LocalSSD
        storage_space (int): 实例存储空间。取值范围：\[20, 3000\]，单位为 GB，步长为 10GB。
            示例值：100

    Returns: 包含以下字段的字典
        charge_item_prices (list[dict[str, Any]], optional): 费用明细。
            示例值：请参见返回示例。
        currency (str, optional): 货币单位。
            示例值：人民币
        discount_price (float, optional): 实例折扣价。
            示例值：1.125
        instance_quantity (int, optional): 实例数量。
            示例值：3
        original_price (float, optional): 实例原价。
            示例值：1.125
        payable_price (float, optional): 实例应付价格。
            示例值：1.125
    """
    node_info = [
        {
            "NodeType": "Primary",
            "ZoneId": primary_zone,
            "NodeSpec": node_spec
        },
        {
            "NodeType": "Secondary",
            "ZoneId": secondary_zone,
            "NodeSpec": node_spec
        }
    ]
    for i in range(read_only_count):
        node_info.append({
            "NodeType": "ReadOnly",
            "ZoneId": read_only_zone,
            "NodeSpec": node_spec
        })
    if charge_type == "PostPaid":
        charge_info = {
            "ChargeType": charge_type,
        }
    else:
        charge_info = {
            "ChargeType": charge_type,
            "AutoRenew": auto_renew,
        }

    req = {
        "node_info": node_info,
        "storage_type": storage_type,
        "storage_space": storage_space,
        "charge_info": charge_info,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_db_instance_price_detail(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="create_db_endpoint",
    description="调用 CreateDBEndpoint 接口为指定实例创建连接终端。"
)
def create_db_endpoint(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-21a3333b****'])],
                       endpoint_type: Annotated[str, Field(description='连接终端类型，当前仅支持取值 `Custom`，即自定义类型。', examples=['Custom'])],
                       endpoint_name: Optional[Annotated[str,Field(description='实例连接终端名称。- 不能以数字、中划线（-）开头。- 只能包含中文、字母、数字、下划线（_）和中划线（-）。- 长度需要在 1~64 个字符内。:::tip不传入时会自动将连接终端命名为“自定义终端”。:::', examples=['EndpointName'])]] = None,
                       nodes: Optional[Annotated[str,Field(description='连接终端配置的节点列表。:::tip- 当 `EndpointType` 为 `Custom` 时必选。- 主节点无需传节点 ID，传入 Primary 字符串即可。:::', examples=['Primary,postgres-ca7b7019****-rocbcb'])]] = None,
                       read_write_mode: Optional[Annotated[str,Field(description='读写模式：- `ReadWrite`：读写。- `ReadOnly`：只读。默认值。', examples=['ReadOnly'])]] = None) -> dict[str, Any]:
    """调用 CreateDBEndpoint 接口为指定实例创建连接终端。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-21a3333b****
        endpoint_type (str): 连接终端类型，当前仅支持取值 `Custom`，即自定义类型。
            示例值：Custom
        endpoint_name (str, optional): 实例连接终端名称。
            - 不能以数字、中划线（-）开头。
            - 只能包含中文、字母、数字、下划线（_）和中划线（-）。
            - 长度需要在 1~64 个字符内。
            :::tip
            不传入时会自动将连接终端命名为“自定义终端”。
            :::
            示例值：EndpointName
        nodes (str, optional): 连接终端配置的节点列表。
            :::tip
            - 当 `EndpointType` 为 `Custom` 时必选。
            - 主节点无需传节点 ID，传入 Primary 字符串即可。
            :::
            示例值：Primary,postgres-ca7b7019****-rocbcb
        read_write_mode (str, optional): 读写模式：
            - `ReadWrite`：读写。
            - `ReadOnly`：只读。默认值。
            示例值：ReadOnly

    Returns: none
    """
    req = {
        "instance_id": instance_id,
        "endpoint_type": endpoint_type,
        "endpoint_name": endpoint_name,
        "nodes": nodes,
        "read_write_mode": read_write_mode,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.create_db_endpoint(req)
    if resp is None or not hasattr(resp, 'to_dict'):
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="describe_db_instance_detail",
    description="调用 DescribeDBInstanceDetail 接口查询实例详细信息。"
)
def describe_db_instance_detail(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-21a3333b****'])]) -> dict[str, Any]:
    """调用 DescribeDBInstanceDetail 接口查询实例详细信息。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-21a3333b****

    Returns: 包含以下字段的字典
        basic_info (dict[str, Any], optional): 实例基本信息。
        charge_detail (dict[str, Any], optional): 实例计费信息。
        endpoints (list[dict[str, Any]], optional): 实例的连接信息。
            示例值：请参见返回示例。
        nodes (list[dict[str, Any]], optional): 实例节点信息。
            示例值：请参见返回示例。
    """
    req = {
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_db_instance_detail(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="modify_db_instance_spec",
    description="调用 ModifyDBInstanceSpec 接口修改实例配置。"
)
@validate_call
def modify_db_instance_spec(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-21a3333b****'])],
                            estimate_only: Optional[Annotated[bool,Field(description='是否发起变配评估。取值：- `true`：是。- `false`：否。默认值。:::tip如果发起，则按照其他字段确定的规格配置进行变配评估，实际不会执行变配动作。发起变配评估后，会返回 EstimationResult 参数，说明此次变配的影响。:::', examples=['true'])]] = None,
                            node_info: Optional[Annotated[list[dict[str, Any]],Field(description='实例规格配置。Primary 节点有且只有 1 个，Secondary 节点有且只有 1 个，Read-Only 节点可选 0~10 个。:::tip- 该参数与 `StorageSpace` 二者必选其一，且这两个参数可同时修改。- 只需在该参数中传入变配涉及的节点。:::', examples=['请参见请求示例。'])]] = None,
                            storage_space: Optional[Annotated[int,Field(description='实例存储空间。取值范围为 \[20, 3000\]，单位为 GB，步长为 10GB。:::tip- 该参数与 `NodeInfo` 二者必选其一，且这两个参数可同时修改。- 当 ModifyType 取值为 `Temporary` 时，不支持设置该参数。:::', examples=['100'])]] = None,
                            storage_type: Optional[Annotated[str,Field(description='实例存储类型。取固定值 `LocalSSD`（本地 SSD 盘）。:::tip- 该参数与 `NodeInfo` 二者必选其一，且这两个参数可同时修改。- 当 ModifyType 取值为 `Temporary` 时，不支持设置该参数。:::', examples=['LocalSSD'])]] = None) -> dict[str, Any]:
    """调用 ModifyDBInstanceSpec 接口修改实例配置。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-21a3333b****
        estimate_only (bool, optional): 是否发起变配评估。取值：
            - `true`：是。
            - `false`：否。默认值。
            :::tip
            如果发起，则按照其他字段确定的规格配置进行变配评估，实际不会执行变配动作。发起变配评估后，会返回 EstimationResult 参数，说明此次变配的影响。
            :::
            示例值：true
        node_info (list[dict[str, Any]], optional): 实例规格配置。Primary 节点有且只有 1 个，Secondary 节点有且只有 1 个，Read-Only 节点可选 0~10 个。
            :::tip
            - 该参数与 `StorageSpace` 二者必选其一，且这两个参数可同时修改。
            - 只需在该参数中传入变配涉及的节点。
            :::
            示例值：请参见请求示例。
        storage_space (int, optional): 实例存储空间。取值范围为 \[20, 3000\]，单位为 GB，步长为 10GB。
            :::tip
            - 该参数与 `NodeInfo` 二者必选其一，且这两个参数可同时修改。
            - 当 ModifyType 取值为 `Temporary` 时，不支持设置该参数。
            :::
            示例值：100
        storage_type (str, optional): 实例存储类型。取固定值 `LocalSSD`（本地 SSD 盘）。
            :::tip
            - 该参数与 `NodeInfo` 二者必选其一，且这两个参数可同时修改。
            - 当 ModifyType 取值为 `Temporary` 时，不支持设置该参数。
            :::
            示例值：LocalSSD

    Returns: 包含以下字段的字典
        estimation_result (dict[str, Any], optional): 按照当前配置变更后，预估会对实例产生的影响。
            :::tip
            当 EstimateOnly 取值为 `false` 或不为 EstimateOnly 传值时，不返回该字段。
            :::
        instance_id (str, optional): 实例 ID。
            示例值：postgres-21a3333b****
        order_id (str, optional): 订单 ID。
            :::tip
            当 EstimateOnly 取值为 `true` 时，该字段的返回值为空。
            :::
            示例值：Order725743560891294****
    """
    if node_info is None:
        return {
            "Message": "执行失败，node_info不能为空"
        }
    new_node_info = []
    for info in node_info:
        if info is None:
            continue
        new_node_info.append({
            "NodeId": info.get("node_id", ""),
            "ZoneId": info.get("zone_id", ""),
            "NodeType": info.get("node_type", ""),
            "NodeSpec": info.get("node_spec", ""),
            "NodeOperateType": info.get("node_operate_type", ""),
        })

    req = {
        "instance_id": instance_id,
        "estimate_only": estimate_only,
        "node_info": new_node_info,
        "storage_space": storage_space,
        "storage_type": storage_type,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.modify_db_instance_spec(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="restore_to_new_instance",
    description="调用 RestoreToNewInstance 接口恢复到新实例。"
)
@validate_call
def restore_to_new_instance(src_instance_id: Annotated[str, Field(description='备份文件所属原实例的 ID。', examples=['postgres-21a3333b****'])],
                            primary_zone: Annotated[str, Field(description='主节点所在可用区', examples=['cn-beijing-a'])],
                            secondary_zone: Annotated[str, Field(description='备节点所在可用区', examples=['cn-beijing-a'])],
                            read_only_zone: Annotated[str, Field(description='只读节点所在可用区', examples=['cn-beijing-a'])],
                            node_spec: Annotated[str, Field(description='节点规格', examples=['rds.postgres.1c2g'])],
                            read_only_count: Annotated[int, Field(description='只读节点数量', examples=['1'])],
                            charge_type: Annotated[str, Field(description='付费类型', examples=['PostPaid'])],
                            auto_renew: Annotated[bool, Field(description='预付费场景下是否自动续费', examples=['false'])],                            storage_type: Annotated[str, Field(description='实例存储类型。取固定值 `LocalSSD`（本地 SSD 盘）。', examples=['LocalSSD'])],
                            vpc_id: Annotated[str, Field(description='使用此参数指定实例使用的私有网络。:::tip- 如您使用 ECS 来连接 PostgreSQL 实例，则需使用和 ECS 实例相同的私有网络，否则 ECS 实例将无法通过私网连接到  PostgreSQL 实例。- 可调用 [DescribeVpcs](https://www.volcengine.com/docs/6401/70495) 接口查询可用的私有网络。- 可调用 [CreateVpc](https://www.volcengine.com/docs/6401/70492) 接口创建新的私有网络。:::', examples=['vpc-2gdgzrrl5icjk50ztyz6b****'])],
                            subnet_id: Annotated[str, Field(description='子网 ID。:::tip- 仅支持选择实例所在可用区的子网。- 可以调用 [DescribeSubnets](https://www.volcengine.com/docs/6401/70497) 接口查询指定私有网络和可用区内的所有子网信息。- 可以调用 [CreateSubnet](https://www.volcengine.com/docs/6401/70496) 接口创建新的子网。:::', examples=['subnet-30uhx4w39n75s7r2qr0lq****'])],
                            allow_list_ids: Optional[Annotated[list[str],Field(description='白名单 ID。如需绑定多个白名单，白名单 ID 用英文逗号（,）分隔。一个实例最多可绑定 100 个白名单。', examples=['["acl-fdd6293f300143f2a4932bb483c8****","acl-ded4c0b707e44efd8f0dbc4e88f5****"]'])]] = None,
                            backup_id: Optional[Annotated[str,Field(description='原实例的备份文件 ID，使用该备份文件中保存的数据创建新实例。可通过调用 [DescribeBackups](https://www.volcengine.com/docs/6438/1158713) 查询指定实例的备份文件列表信息。:::tip应至少传入 BackupId 与 RestoreTime 中的一个。如果同时传入 BackupId 和 RestoreTime，会以 BackupId 为准。:::', examples=['20230801-170****'])]] = None,
                            instance_name: Optional[Annotated[str,Field(description='实例名称。规则：- 不能以数字、中划线开头。- 只能包含中文、字母、数字、下划线和中划线。- 长度限制在 1~128之间。', examples=['Name123'])]] = None,
                            project_name: Optional[Annotated[str,Field(description='所属项目。当该参数留空时，新建的实例默认加入 default 项目。', examples=['Test'])]] = None,
                            restore_time: Optional[Annotated[str,Field(description='原实例日志备份保留时间内的任意时间点，格式为 `yyyy-MM-ddTHH:mm:ssZ`（UTC 时间）。可通过调用 [DescribeRecoverableTime](https://www.volcengine.com/docs/6438/1158721) 查询指定实例可恢复的时间范围。:::tip该参数与 BackupId 参数二者必须选择其一。:::', examples=['2022-01-01T10:10:10Z'])]] = None,
                            storage_space: Optional[Annotated[int,Field(description='实例存储空间。取值范围：\[20, 3000\]，单位：GB，步长 10GB。默认值为原实例空间大小。', examples=['100'])]] = None,
                            tags: Optional[Annotated[list[dict[str, Any]],Field(description='标签数组对象。:::tip支持一次传入多组标签键值对象。单次最多同时传入 20 组标签键值对，单个实例最多绑定 50 个标签。:::', examples=['请参见请求示例。'])]] = None) -> dict[str, Any]:
    """调用 RestoreToNewInstance 接口恢复到新实例。

    Args:
        src_instance_id (str): 备份文件所属原实例的 ID。
            示例值：postgres-21a3333b****
        auto_renew: 预付费场景下是否自动续费
        charge_type: 付费类型
        read_only_count: 只读节点数量
        node_spec: 节点规格
        read_only_zone: 只读节点所在可用区
        secondary_zone: 备节点所在可用区
        primary_zone: 主节点所在可用区
        storage_type (str): 实例存储类型。取固定值 `LocalSSD`（本地 SSD 盘）。
            示例值：LocalSSD
        vpc_id (str): 使用此参数指定实例使用的私有网络。
            :::tip
            - 如您使用 ECS 来连接 PostgreSQL 实例，则需使用和 ECS 实例相同的私有网络，否则 ECS 实例将无法通过私网连接到  PostgreSQL 实例。
            - 可调用 [DescribeVpcs](https://www.volcengine.com/docs/6401/70495) 接口查询可用的私有网络。
            - 可调用 [CreateVpc](https://www.volcengine.com/docs/6401/70492) 接口创建新的私有网络。
            :::
            示例值：vpc-2gdgzrrl5icjk50ztyz6b****
        subnet_id (str): 子网 ID。
            :::tip
            - 仅支持选择实例所在可用区的子网。
            - 可以调用 [DescribeSubnets](https://www.volcengine.com/docs/6401/70497) 接口查询指定私有网络和可用区内的所有子网信息。
            - 可以调用 [CreateSubnet](https://www.volcengine.com/docs/6401/70496) 接口创建新的子网。
            :::
            示例值：subnet-30uhx4w39n75s7r2qr0lq****
        allow_list_ids (list[str], optional): 白名单 ID。如需绑定多个白名单，白名单 ID 用英文逗号（,）分隔。一个实例最多可绑定 100 个白名单。
            示例值：[
            "acl-fdd6293f300143f2a4932bb483c8****",
            "acl-ded4c0b707e44efd8f0dbc4e88f5****"
            ]
        backup_id (str, optional): 原实例的备份文件 ID，使用该备份文件中保存的数据创建新实例。可通过调用 [DescribeBackups](https://www.volcengine.com/docs/6438/1158713) 查询指定实例的备份文件列表信息。
            :::tip
            应至少传入 BackupId 与 RestoreTime 中的一个。如果同时传入 BackupId 和 RestoreTime，会以 BackupId 为准。
            :::
            示例值：20230801-170****
        instance_name (str, optional): 实例名称。规则：
            - 不能以数字、中划线开头。
            - 只能包含中文、字母、数字、下划线和中划线。
            - 长度限制在 1~128之间。
            示例值：Name123
        project_name (str, optional): 所属项目。当该参数留空时，新建的实例默认加入 default 项目。
            示例值：Test
        restore_time (str, optional): 原实例日志备份保留时间内的任意时间点，格式为 `yyyy-MM-ddTHH:mm:ssZ`（UTC 时间）。可通过调用 [DescribeRecoverableTime](https://www.volcengine.com/docs/6438/1158721) 查询指定实例可恢复的时间范围。
            :::tip
            该参数与 BackupId 参数二者必须选择其一。
            :::
            示例值：2022-01-01T10:10:10Z
        storage_space (int, optional): 实例存储空间。取值范围：\[20, 3000\]，单位：GB，步长 10GB。默认值为原实例空间大小。
            示例值：100
        tags (list[dict[str, Any]], optional): 标签数组对象。
            :::tip
            支持一次传入多组标签键值对象。单次最多同时传入 20 组标签键值对，单个实例最多绑定 50 个标签。
            :::
            示例值：请参见请求示例。

    Returns: 包含以下字段的字典
        instance_id (str, optional): 实例 ID。
            示例值：postgres-21a3333b****
        order_id (str, optional): 订单 ID。
            示例值：Order71220115095297****
    """
    node_info = [
        {
            "NodeType": "Primary",
            "ZoneId": primary_zone,
            "NodeSpec": node_spec
        },
        {
            "NodeType": "Secondary",
            "ZoneId": secondary_zone,
            "NodeSpec": node_spec
        }
    ]
    for i in range(read_only_count):
        node_info.append({
            "NodeType": "ReadOnly",
            "ZoneId": read_only_zone,
            "NodeSpec": node_spec
        })
    if charge_type == "PostPaid":
        charge_info = {
            "ChargeType": charge_type,
        }
    else:
        charge_info = {
            "ChargeType": charge_type,
            "AutoRenew": auto_renew,
        }

    req = {
        "src_instance_id": src_instance_id,
        "node_info": node_info,
        "storage_type": storage_type,
        "vpc_id": vpc_id,
        "subnet_id": subnet_id,
        "charge_info": charge_info,
        "allow_list_ids": allow_list_ids,
        "backup_id": backup_id,
        "instance_name": instance_name,
        "project_name": project_name,
        "restore_time": restore_time,
        "storage_space": storage_space,
        "tags": tags,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.restore_to_new_instance(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="create_db_instance",
    description="调用 CreateDBInstance 接口创建实例。"
)
@validate_call
def create_db_instance(db_engine_version: Annotated[str, Field(description='兼容版本。取值：- `PostgreSQL_11`：PostgreSQL 11。- `PostgreSQL_12`：PostgreSQL 12。- `PostgreSQL_13`：PostgreSQL 13。- `PostgreSQL_14`：PostgreSQL 14。- `PostgreSQL_15`：PostgreSQL 15。- `PostgreSQL_16`：PostgreSQL 16。- `PostgreSQL_17`：PostgreSQL 17。', examples=['PostgreSQL_12'])],
                       primary_zone: Annotated[str, Field(description='主节点所在可用区', examples=['cn-beijing-a'])],
                       secondary_zone: Annotated[str, Field(description='备节点所在可用区', examples=['cn-beijing-a'])],
                       read_only_zone: Annotated[str, Field(description='只读节点所在可用区', examples=['cn-beijing-a'])],
                       node_spec: Annotated[str, Field(description='节点规格', examples=['rds.postgres.1c2g'])],
                       read_only_count: Annotated[int, Field(description='只读节点数量', examples=['1'])],
                       charge_type: Annotated[str, Field(description='付费类型', examples=['PostPaid'])],
                       auto_renew: Annotated[bool, Field(description='预付费场景下是否自动续费', examples=['false'])],
                       storage_type: Annotated[str, Field(description='实例存储类型。取固定值 `LocalSSD`（本地 SSD 盘）。', examples=['LocalSSD'])],
                       vpc_id: Annotated[str, Field(description='使用此参数指定实例使用的私有网络。:::tip- 如您使用 ECS 来连接 PostgreSQL 实例，则需使用和 ECS 实例相同的私有网络，否则 ECS 实例将无法通过私网连接到  PostgreSQL 实例。- 可调用 [DescribeVpcs](https://www.volcengine.com/docs/6401/70495) 接口查询可用的私有网络。- 可调用 [CreateVpc](https://www.volcengine.com/docs/6401/70492) 接口创建新的私有网络。:::', examples=['vpc-2gdgzrrl5icjk50ztyz6b****'])],
                       subnet_id: Annotated[str, Field(description='子网 ID。:::tip- 仅支持选择实例所在可用区的子网。- 可以调用 [DescribeSubnets](https://www.volcengine.com/docs/6401/70497) 接口查询指定私有网络和可用区内的所有子网信息。- 可以调用 [CreateSubnet](https://www.volcengine.com/docs/6401/70496) 接口创建新的子网。:::', examples=['subnet-30uhx4w39n75s7r2qr0lq****'])],
                       allow_list_ids: Optional[Annotated[list[str],Field(description='白名单 ID。如需绑定多个白名单，白名单 ID 用英文逗号（,）分隔。一个实例最多可绑定 100 个白名单。', examples=['["acl-fdd6293f300143f2a4932bb483c8****","acl-ded4c0b707e44efd8f0dbc4e88f5****"]'])]] = None,
                       instance_name: Optional[Annotated[str,Field(description='实例名称，规则：- 不能以数字、中划线开头。- 只能包含中文、字母、数字、下划线和中划线。- 长度限制在 1~128 之间。', examples=['Name123'])]] = None,
                       project_name: Optional[Annotated[str,Field(description='所属项目，默认值为 default 项目。', examples=['Test'])]] = None,
                       storage_space: Optional[Annotated[int,Field(description='实例存储空间。取值范围：\[20, 3000\]，单位：GB，步长 10GB。默认值为 100。', examples=['100'])]] = None,
                       tags: Optional[Annotated[list[dict[str, Any]],Field(description='标签数组对象。:::tip支持一次传入多组标签键值对象，多组标签键值对象间用英文逗号（,）分隔。单次最多同时传入 20 组标签键值对，单个实例最多绑定 50 个标签。:::', examples=['[{"Key": "test","Value": "123"}]'])]] = None) -> dict[str, Any]:
    """调用 CreateDBInstance 接口创建实例。

    Args:
        db_engine_version (str): 兼容版本。取值：
            - `PostgreSQL_11`：PostgreSQL 11。
            - `PostgreSQL_12`：PostgreSQL 12。
            - `PostgreSQL_13`：PostgreSQL 13。
            - `PostgreSQL_14`：PostgreSQL 14。
            - `PostgreSQL_15`：PostgreSQL 15。
            - `PostgreSQL_16`：PostgreSQL 16。
            - `PostgreSQL_17`：PostgreSQL 17。
            示例值：PostgreSQL_12
        auto_renew: 预付费场景下是否自动续费
        charge_type: 付费类型
        read_only_count: 只读节点数量
        node_spec: 节点规格
        read_only_zone: 只读节点所在可用区
        secondary_zone: 备节点所在可用区
        primary_zone: 主节点所在可用区
        storage_type (str): 实例存储类型。取固定值 `LocalSSD`（本地 SSD 盘）。
            示例值：LocalSSD
        vpc_id (str): 使用此参数指定实例使用的私有网络。
            :::tip
            - 如您使用 ECS 来连接 PostgreSQL 实例，则需使用和 ECS 实例相同的私有网络，否则 ECS 实例将无法通过私网连接到  PostgreSQL 实例。
            - 可调用 [DescribeVpcs](https://www.volcengine.com/docs/6401/70495) 接口查询可用的私有网络。
            - 可调用 [CreateVpc](https://www.volcengine.com/docs/6401/70492) 接口创建新的私有网络。
            :::
            示例值：vpc-2gdgzrrl5icjk50ztyz6b****
        subnet_id (str): 子网 ID。
            :::tip
            - 仅支持选择实例所在可用区的子网。
            - 可以调用 [DescribeSubnets](https://www.volcengine.com/docs/6401/70497) 接口查询指定私有网络和可用区内的所有子网信息。
            - 可以调用 [CreateSubnet](https://www.volcengine.com/docs/6401/70496) 接口创建新的子网。
            :::
            示例值：subnet-30uhx4w39n75s7r2qr0lq****
        allow_list_ids (list[str], optional): 白名单 ID。如需绑定多个白名单，白名单 ID 用英文逗号（,）分隔。一个实例最多可绑定 100 个白名单。
            示例值：[
            "acl-fdd6293f300143f2a4932bb483c8****",
            "acl-ded4c0b707e44efd8f0dbc4e88f5****"
            ]
        instance_name (str, optional): 实例名称，规则：
            - 不能以数字、中划线开头。
            - 只能包含中文、字母、数字、下划线和中划线。
            - 长度限制在 1~128 之间。
            示例值：Name123
        project_name (str, optional): 所属项目，默认值为 default 项目。
            示例值：Test
        storage_space (int, optional): 实例存储空间。取值范围：\[20, 3000\]，单位：GB，步长 10GB。默认值为 100。
            示例值：100
        tags (list[dict[str, Any]], optional): 标签数组对象。
            :::tip
            支持一次传入多组标签键值对象，多组标签键值对象间用英文逗号（,）分隔。单次最多同时传入 20 组标签键值对，单个实例最多绑定 50 个标签。
            :::
            示例值：[{
            "Key": "test",
            "Value": "123"
            }]

    Returns: 包含以下字段的字典
        instance_id (str, optional): 实例 ID。
            示例值：postgres-21a3333b****
        order_id (str, optional): 订单 ID。
            示例值：Order634971667632428****
    """

    node_info = [
        {
            "NodeType": "Primary",
            "ZoneId": primary_zone,
            "NodeSpec": node_spec
        },
        {
            "NodeType": "Secondary",
            "ZoneId": secondary_zone,
            "NodeSpec": node_spec
        }
    ]
    for i in range(read_only_count):
        node_info.append({
            "NodeType": "ReadOnly",
            "ZoneId": read_only_zone,
            "NodeSpec": node_spec
        })
    if charge_type == "PostPaid":
        charge_info = {
            "ChargeType": charge_type,
        }
    else:
        charge_info = {
            "ChargeType": charge_type,
            "AutoRenew": auto_renew,
        }

    req = {
        "db_engine_version": db_engine_version,
        "node_info": node_info,
        "storage_type": storage_type,
        "vpc_id": vpc_id,
        "subnet_id": subnet_id,
        "charge_info": charge_info,
        "allow_list_ids": allow_list_ids,
        "instance_name": instance_name,
        "project_name": project_name,
        "storage_space": storage_space,
        "tags": tags,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.create_db_instance(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="describe_db_instances",
    description="调用 DescribeDBInstances 接口查询实例列表。"
)
@validate_call
def describe_db_instances(charge_type: Optional[Annotated[str,Field(description='付费类型。取值：- `PostPaid`：按量付费。- `PrePaid`：包年包月', examples=['PostPaid'])]] = None,
                          create_time_end: Optional[Annotated[str,Field(description='查询创建实例创建时间范围。', examples=['2022-01-01T10:10:10.000Z'])]] = None,
                          create_time_start: Optional[Annotated[str,Field(description='查询创建实例创建时间范围。', examples=['2022-01-01T10:10:10.000Z'])]] = None,
                          db_engine_version: Optional[Annotated[str,Field(description='兼容版本。取值：- `PostgreSQL_11`：PostgreSQL 11。- `PostgreSQL_12`：PostgreSQL 12。- `PostgreSQL_13`：PostgreSQL 13。- `PostgreSQL_14`：PostgreSQL 14。- `PostgreSQL_15`：PostgreSQL 15。- `PostgreSQL_16`：PostgreSQL 16。- `PostgreSQL_17`：PostgreSQL 17。', examples=['PostgreSQL_12'])]] = None,
                          instance_id: Optional[Annotated[str,Field(description='实例 ID。', examples=['postgres-21a3333b****'])]] = None,
                          instance_name: Optional[Annotated[str,Field(description='实例名称。', examples=['测试实例'])]] = None,
                          instance_status: Optional[Annotated[str,Field(description='实例状态，取值：- `Running`：运行中。- `Creating`：创建中。- `Deleting`：删除中。- `Restarting`：重启中。- `Restoring`：恢复中。- `Updating`：变更中。- `Upgrading`：升级中。- `Error`：错误。- `Released`：已释放。- `CreateError`：创建错误。- `MasterChanging`：主节点切换中。- `Deleted`：已删除。- `Recycled`：已回收。', examples=['Running'])]] = None,
                          page_number: Optional[Annotated[int,Field(description='当前页查询偏移量，默认值为 1。', examples=['1'])]] = None,
                          page_size: Optional[Annotated[int,Field(description='每页记录数，取值应大于 0 且不超过 1000，默认值为 10。', examples=['10'])]] = None,
                          private_network_vpc_id: Optional[Annotated[str,Field(description='私有网络的 ID。可通过该字段筛选使用指定私有网络的实例。', examples=['vpc-miswzgsgy77k5smt1ar9****'])]] = None,
                          project_name: Optional[Annotated[str,Field(description='项目名称。', examples=['testProject'])]] = None,
                          storage_type: Optional[Annotated[str,Field(description='实例存储类型。取固定值 `LocalSSD`（本地 SSD 盘）。', examples=['LocalSSD'])]] = None,
                          tag_filters: Optional[Annotated[list[dict[str, Any]],Field(description='标签查询数组对象。单次最多支持同时传入 10 组标签键值对进行查询筛选。', examples=['请参见请求示例。'])]] = None,
                          zone_id: Optional[Annotated[str,Field(description='实例所属可用区。', examples=['cn-beijing-a'])]] = None) -> dict[str, Any]:
    """调用 DescribeDBInstances 接口查询实例列表。

    Args:
        charge_type (str, optional): 付费类型。取值：
            - `PostPaid`：按量付费。
            - `PrePaid`：包年包月
            示例值：PostPaid
        create_time_end (str, optional): 查询创建实例创建时间范围。
            示例值：2022-01-01T10:10:10.000Z
        create_time_start (str, optional): 查询创建实例创建时间范围。
            示例值：2022-01-01T10:10:10.000Z
        db_engine_version (str, optional): 兼容版本。取值：
            - `PostgreSQL_11`：PostgreSQL 11。
            - `PostgreSQL_12`：PostgreSQL 12。
            - `PostgreSQL_13`：PostgreSQL 13。
            - `PostgreSQL_14`：PostgreSQL 14。
            - `PostgreSQL_15`：PostgreSQL 15。
            - `PostgreSQL_16`：PostgreSQL 16。
            - `PostgreSQL_17`：PostgreSQL 17。
            示例值：PostgreSQL_12
        instance_id (str, optional): 实例 ID。
            示例值：postgres-21a3333b****
        instance_name (str, optional): 实例名称。
            示例值：测试实例
        instance_status (str, optional): 实例状态，取值：
            - `Running`：运行中。
            - `Creating`：创建中。
            - `Deleting`：删除中。
            - `Restarting`：重启中。
            - `Restoring`：恢复中。
            - `Updating`：变更中。
            - `Upgrading`：升级中。
            - `Error`：错误。
            - `Released`：已释放。
            - `CreateError`：创建错误。
            - `MasterChanging`：主节点切换中。
            - `Deleted`：已删除。
            - `Recycled`：已回收。
            示例值：Running
        page_number (int, optional): 当前页查询偏移量，默认值为 1。
            示例值：1
        page_size (int, optional): 每页记录数，取值应大于 0 且不超过 1000，默认值为 10。
            示例值：10
        private_network_vpc_id (str, optional): 私有网络的 ID。可通过该字段筛选使用指定私有网络的实例。
            示例值：vpc-miswzgsgy77k5smt1ar9****
        project_name (str, optional): 项目名称。
            示例值：testProject
        storage_type (str, optional): 实例存储类型。取固定值 `LocalSSD`（本地 SSD 盘）。
            示例值：LocalSSD
        tag_filters (list[dict[str, Any]], optional): 标签查询数组对象。单次最多支持同时传入 10 组标签键值对进行查询筛选。
            示例值：请参见请求示例。
        zone_id (str, optional): 实例所属可用区。
            示例值：cn-beijing-a

    Returns: 包含以下字段的字典
        instances (list[dict[str, Any]], optional): 实例列表。
            示例值：请参见返回示例。
        total (int, optional): 实例总数。
            示例值：1
    """
    req = {
        "charge_type": charge_type,
        "create_time_end": create_time_end,
        "create_time_start": create_time_start,
        "db_engine_version": db_engine_version,
        "instance_id": instance_id,
        "instance_name": instance_name,
        "instance_status": instance_status,
        "page_number": page_number,
        "page_size": page_size,
        "private_network_vpc_id": private_network_vpc_id,
        "project_name": project_name,
        "storage_type": storage_type,
        "tag_filters": tag_filters,
        "zone_id": zone_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_db_instances(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="describe_db_instance_specs",
    description="调用 DescribeDBInstanceSpecs 接口查询可售卖的实例规格。"
)
def describe_db_instance_specs(db_engine_version: Optional[Annotated[str,Field(description='兼容版本。取值：- `PostgreSQL_11`：PostgreSQL 11。- `PostgreSQL_12`：PostgreSQL 12。- `PostgreSQL_13`：PostgreSQL 13。- `PostgreSQL_14`：PostgreSQL 14。- `PostgreSQL_15`：PostgreSQL 15。- `PostgreSQL_16`：PostgreSQL 16。- `PostgreSQL_17`：PostgreSQL 17。', examples=['PostgreSQL_12'])]] = None,
                               spec_code: Optional[Annotated[str,Field(description='实例规格编码。:::tip关于节点规格的详细信息，请参见[产品规格](https://www.volcengine.com/docs/6438/79219)。:::', examples=['rds.postgres.1c2g'])]] = None,
                               storage_type: Optional[Annotated[str,Field(description='实例存储类型。取固定值 `LocalSSD`（本地 SSD 盘）。', examples=['LocalSSD'])]] = None,
                               zone_id: Optional[Annotated[str,Field(description='主可用区 ID，可调用 [DescribeAvailabilityZones](https://www.volcengine.com/docs/6438/1159932) 接口查询可用区列表。', examples=['cn-beijing-a'])]] = None) -> dict[str, Any]:
    """调用 DescribeDBInstanceSpecs 接口查询可售卖的实例规格。

    Args:
        db_engine_version (str, optional): 兼容版本。取值：
            - `PostgreSQL_11`：PostgreSQL 11。
            - `PostgreSQL_12`：PostgreSQL 12。
            - `PostgreSQL_13`：PostgreSQL 13。
            - `PostgreSQL_14`：PostgreSQL 14。
            - `PostgreSQL_15`：PostgreSQL 15。
            - `PostgreSQL_16`：PostgreSQL 16。
            - `PostgreSQL_17`：PostgreSQL 17。
            示例值：PostgreSQL_12
        spec_code (str, optional): 实例规格编码。
            :::tip
            关于节点规格的详细信息，请参见[产品规格](https://www.volcengine.com/docs/6438/79219)。
            :::
            示例值：rds.postgres.1c2g
        storage_type (str, optional): 实例存储类型。取固定值 `LocalSSD`（本地 SSD 盘）。
            示例值：LocalSSD
        zone_id (str, optional): 主可用区 ID，可调用 [DescribeAvailabilityZones](https://www.volcengine.com/docs/6438/1159932) 接口查询可用区列表。
            示例值：cn-beijing-a

    Returns: 包含以下字段的字典
        instance_specs (list[dict[str, Any]], optional): 规格列表。
            示例值：请参见返回示例。
        total (int, optional): 规格总数。
            示例值：1
    """
    req = {
        "db_engine_version": db_engine_version,
        "spec_code": spec_code,
        "storage_type": storage_type,
        "zone_id": zone_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_db_instance_specs(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="describe_recoverable_time",
    description="调用 DescribeRecoverableTime 接口查询实例备份可恢复的时间范围。"
)
def describe_recoverable_time(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-21a3333b****'])]) -> dict[str, Any]:
    """调用 DescribeRecoverableTime 接口查询实例备份可恢复的时间范围。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-21a3333b****

    Returns: 包含以下字段的字典
        recoverable_time_info (list[dict[str, Any]], optional): 实例最早和最晚可恢复的时间（UTC 时间），为空表示实例目前不可恢复。
            示例值：2023-10-08T18:17:12.000Z
    """
    req = {
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_recoverable_time(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="modify_db_endpoint_address",
    description="调用 ModifyDBEndpointAddress 接口修改实例私网连接地址的端口和前缀。"
)
def modify_db_endpoint_address(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-21a3333b****'])],
                               network_type: Annotated[str, Field(description='网络类型，目前仅支持 `Private`。', examples=['Private'])],
                               domain_prefix: Optional[Annotated[str,Field(description='新的访问地址前缀。访问地址前缀应满足以下规则：- 由小写字母、数字和中划线（-）组成。- 至少包含 8 个字符，总长度（含后缀）不得超过 63 个字符。- 以小写字母开头，以小写字母或数字结尾。', examples=['postgresc602d39c****'])]] = None,
                               endpoint_id: Optional[Annotated[str,Field(description='待修改连接地址的连接终端 ID。如不设定，默认选择默认终端。', examples=['postgres-ca7b7019****-custom-f07b'])]] = None,
                               port: Optional[Annotated[str,Field(description='端口的端口号。取值范围为 1000~65534。', examples=['5432'])]] = None) -> dict[str, Any]:
    """调用 ModifyDBEndpointAddress 接口修改实例私网连接地址的端口和前缀。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-21a3333b****
        network_type (str): 网络类型，目前仅支持 `Private`。
            示例值：Private
        domain_prefix (str, optional): 新的访问地址前缀。访问地址前缀应满足以下规则：
            - 由小写字母、数字和中划线（-）组成。
            - 至少包含 8 个字符，总长度（含后缀）不得超过 63 个字符。
            - 以小写字母开头，以小写字母或数字结尾。
            示例值：postgresc602d39c****
        endpoint_id (str, optional): 待修改连接地址的连接终端 ID。如不设定，默认选择默认终端。
            示例值：postgres-ca7b7019****-custom-f07b
        port (str, optional): 端口的端口号。取值范围为 1000~65534。
            示例值：5432
    """
    req = {
        "instance_id": instance_id,
        "network_type": network_type,
        "domain_prefix": domain_prefix,
        "endpoint_id": endpoint_id,
        "port": port,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.modify_db_endpoint_address(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="describe_failover_logs",
    description="调用 DescribeFailoverLogs 接口查询实例主备切换日志。"
)
def describe_failover_logs(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-21a3333b****'])],
                           context: Optional[Annotated[str,Field(description='索引信息，翻页加载更多日志时使用。透传上次返回的 context 值，获取后续的日志内容。默认值为空。', examples=['[1690808035000,100367578,8388608,null]'])]] = None,
                           limit: Optional[Annotated[int,Field(description='每页记录数，最大值为 1000，最小值为 1，默认值为 500。', examples=['1000'])]] = None,
                           query_end_time: Optional[Annotated[str,Field(description='查询结束时间，需要晚于查询开始时间，且与查询开始时间的间隔应小于 31 天。格式：`yyyy-MM-ddTHH:mmZ`（UTC 时间）。默认值为发起请求的时间。', examples=['2023-07-31T12:00:19Z'])]] = None,
                           query_start_time: Optional[Annotated[str,Field(description='查询开始时间。格式：`yyyy-MM-ddTHH:mmZ`（UTC 时间）。其中，T 指某个时间的开始；Z 指时区偏移量，例如北京时间偏移显示为+0800。默认值为实例的创建时间，即自实例创建起查询。', examples=['2023-07-31T12:00:19Z'])]] = None) -> dict[str, Any]:
    """调用 DescribeFailoverLogs 接口查询实例主备切换日志。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-21a3333b****
        context (str, optional): 索引信息，翻页加载更多日志时使用。透传上次返回的 context 值，获取后续的日志内容。
            默认值为空。
            示例值：[1690808035000,100367578,8388608,null]
        limit (int, optional): 每页记录数，最大值为 1000，最小值为 1，默认值为 500。
            示例值：1000
        query_end_time (str, optional): 查询结束时间，需要晚于查询开始时间，且与查询开始时间的间隔应小于 31 天。格式：`yyyy-MM-ddTHH:mmZ`（UTC 时间）。
            默认值为发起请求的时间。
            示例值：2023-07-31T12:00:19Z
        query_start_time (str, optional): 查询开始时间。格式：`yyyy-MM-ddTHH:mmZ`（UTC 时间）。
            其中，T 指某个时间的开始；Z 指时区偏移量，例如北京时间偏移显示为+0800。
            默认值为实例的创建时间，即自实例创建起查询。
            示例值：2023-07-31T12:00:19Z

    Returns: 包含以下字段的字典
        context (str, optional): 索引信息。以最后一个备份文件作为索引进行返回。可作为下一次请求的参数，加载更多时选择。
            示例值：[1690808035000,100367578,8388608,null]
        failover_logs (list[dict[str, Any]], optional): 实例主备切换日志列表。
            示例值：请参见返回示例。
        instance_id (str, optional): 实例 ID。
            示例值：postgres-21a3333b****
        total (int, optional): 主备切换日志总数。
            示例值：1
    """
    req = {
        "instance_id": instance_id,
        "context": context,
        "limit": limit,
        "query_end_time": query_end_time,
        "query_start_time": query_start_time,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_failover_logs(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="reset_db_account",
    description="调用 ResetDBAccount 接口重置账号的密码。"
)
def reset_db_account(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-ca7b7019****'])],
                     account_name: Annotated[str, Field(description='数据库账号名称。账号名称的设置规则如下：- 长度 2~63 个字符。- 由字母、数字、下划线（_）或中划线（-）组成。- 以字母开头，字母或数字结尾。- 不能使用保留关键字，所有被禁用的关键词请参见[禁用关键词](https://www.volcengine.com/docs/6438/80243)。', examples=['testuser'])],
                     account_password: Annotated[str, Field(description='为数据库账号重置的新密码。数据库账号密码的设置规则如下：- 长度为 8~32 个字符。- 由大写字母、小写字母、数字、特殊字符中的任意三种组成。- 特殊字符为 `!@#$%^*()&_+-=`。', examples=['Test@123456'])]) -> dict[str, Any]:
    """调用 ResetDBAccount 接口重置账号的密码。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-ca7b7019****
        account_name (str): 数据库账号名称。账号名称的设置规则如下：
            - 长度 2~63 个字符。
            - 由字母、数字、下划线（_）或中划线（-）组成。
            - 以字母开头，字母或数字结尾。
            - 不能使用保留关键字，所有被禁用的关键词请参见[禁用关键词](https://www.volcengine.com/docs/6438/80243)。
            示例值：testuser
        account_password (str): 为数据库账号重置的新密码。数据库账号密码的设置规则如下：
            - 长度为 8~32 个字符。
            - 由大写字母、小写字母、数字、特殊字符中的任意三种组成。
            - 特殊字符为 `!@#$%^*()&_+-=`。
            示例值：Test@123456
    """
    req = {
        "instance_id": instance_id,
        "account_name": account_name,
        "account_password": account_password,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.reset_db_account(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="modify_db_account_privilege",
    description="调用 ModifyDBAccountPrivilege 接口修改数据库账号权限。"
)
def modify_db_account_privilege(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-ca7b7019****'])],
                                account_name: Annotated[str, Field(description='账号名称。:::tip仅支持修改普通账号的权限。:::', examples=['testuser'])],
                                account_privileges: Annotated[str, Field(description='账号权限信息。取值：- `Login`：登录权限。- `Inherit`：继承权限。- `CreateRole`：创建角色权限。- `CreateDB`：创建数据库权限。:::tip- 不支持修改高权限账号权限。- 可在一次调用中赋予多个权限。:::', examples=['Inherit,Login,CreateRole,CreateDB'])]) -> dict[str, Any]:
    """调用 ModifyDBAccountPrivilege 接口修改数据库账号权限。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-ca7b7019****
        account_name (str): 账号名称。
            :::tip
            仅支持修改普通账号的权限。
            :::
            示例值：testuser
        account_privileges (str): 账号权限信息。取值：
            - `Login`：登录权限。
            - `Inherit`：继承权限。
            - `CreateRole`：创建角色权限。
            - `CreateDB`：创建数据库权限。
            :::tip
            - 不支持修改高权限账号权限。
            - 可在一次调用中赋予多个权限。
            :::
            示例值：Inherit,Login,CreateRole,CreateDB
    """
    req = {
        "instance_id": instance_id,
        "account_name": account_name,
        "account_privileges": account_privileges,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.modify_db_account_privilege(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="create_schema",
    description="调用 CreateSchema 接口创建 Schema。"
)
def create_schema(db_name: Annotated[str, Field(description='数据库名称。', examples=['testdb1'])],
                  schema_name: Annotated[str, Field(description='Schema 名称。- 长度 2~63 个字符。- 由字母、数字、下划线（_）或中划线（-）组成。- 以字母开头，字母或数字结尾。- 不能使用保留关键字，所有被禁用的关键词请参见[禁用关键词](https://www.volcengine.com/docs/6438/80243)。- 不能以 `pg_` 开头。', examples=['ThisIsASchemaName'])],
                  instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-21a3333b****'])],
                  owner: Annotated[str, Field(description='Schema 的 owner。:::tip实例只读账号、被禁用了 DDL 权限的高权限账号或被禁用了 DDL 权限的普通账号不能作为 Schema 的 owner。:::', examples=['User01'])]) -> dict[str, Any]:
    """调用 CreateSchema 接口创建 Schema。

    Args:
        db_name (str): 数据库名称。
            示例值：testdb1
        schema_name (str): Schema 名称。
            - 长度 2~63 个字符。
            - 由字母、数字、下划线（_）或中划线（-）组成。
            - 以字母开头，字母或数字结尾。
            - 不能使用保留关键字，所有被禁用的关键词请参见[禁用关键词](https://www.volcengine.com/docs/6438/80243)。
            - 不能以 `pg_` 开头。
            示例值：ThisIsASchemaName
        instance_id (str): 实例 ID。
            示例值：postgres-21a3333b****
        owner (str): Schema 的 owner。
            :::tip
            实例只读账号、被禁用了 DDL 权限的高权限账号或被禁用了 DDL 权限的普通账号不能作为 Schema 的 owner。
            :::
            示例值：User01
    """
    req = {
        "db_name": db_name,
        "schema_name": schema_name,
        "instance_id": instance_id,
        "owner": owner,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.create_schema(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="modify_schema_owner",
    description="调用 ModifySchemaOwner 接口修改 Schema 的 owner。"
)
@validate_call
def modify_schema_owner(db_name: Annotated[str, Field(description='数据库名。', examples=['testdb'])],
                        schema_name: Annotated[str, Field(description='数据库下的 Schema 名称。', examples=['testschema'])],
                        owner: Annotated[str, Field(description='Schema 的 owner。', examples=['testuser'])],
                        instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-21a3333b****'])]) -> dict[str, Any]:
    """调用 ModifySchemaOwner 接口修改 Schema 的 owner。

    Args:
        owner: Schema 的 owner。
        schema_name: 数据库下的 Schema 名称。
        db_name: 数据库名。
        instance_id (str): 实例 ID。
            示例值：postgres-21a3333b****
    """
    schema_info = [
        {
            "DBName": db_name,
            "SchemaName": schema_name,
            "Owner": owner,
        }
    ]
    req = {
        "schema_info": schema_info,
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.modify_schema_owner(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="describe_schemas",
    description="调用 DescribeSchemas 接口查询 Schema 列表。"
)
def describe_schemas(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-21a3333b****'])],
                     db_name: Optional[Annotated[str,Field(description='数据库名称。:::tip不传值或传空值时，会查询指定实例下的所有 Schema。:::', examples=['testdb'])]] = None,
                     page_number: Optional[Annotated[int,Field(description='当前页查询偏移量，默认值为 1。', examples=['1'])]] = None,
                     page_size: Optional[Annotated[int,Field(description='每页记录数，取值应大于 0 且不超过 1000，默认值为 10。', examples=['10'])]] = None) -> dict[str, Any]:
    """调用 DescribeSchemas 接口查询 Schema 列表。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-21a3333b****
        db_name (str, optional): 数据库名称。
            :::tip
            不传值或传空值时，会查询指定实例下的所有 Schema。
            :::
            示例值：testdb
        page_number (int, optional): 当前页查询偏移量，默认值为 1。
            示例值：1
        page_size (int, optional): 每页记录数，取值应大于 0 且不超过 1000，默认值为 10。
            示例值：10

    Returns: 包含以下字段的字典
        schemas (list[dict[str, Any]], optional): Schema 列表。
            示例值：请参见返回示例。
        total (int, optional): Schema 总数。
            示例值：1
    """
    req = {
        "instance_id": instance_id,
        "db_name": db_name,
        "page_number": page_number,
        "page_size": page_size,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_schemas(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="modify_database_owner",
    description="调用 ModifyDatabaseOwner 接口修改数据库 Owner。"
)
def modify_database_owner(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-21a3333b****'])],
                          db_name: Annotated[str, Field(description='数据库名称。可调用 [DescribeDatabases](https://www.volcengine.com/docs/6438/1158742) 接口查询数据库列表。', examples=['test1'])],
                          owner: Annotated[str, Field(description='数据库 Owner。:::tip实例只读账号、被禁用了 DDL 权限的高权限账号或被禁用了 DDL 权限的普通账号不能作为数据库的 Owner。:::', examples=['testuser'])]) -> dict[str, Any]:
    """调用 ModifyDatabaseOwner 接口修改数据库 Owner。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-21a3333b****
        db_name (str): 数据库名称。可调用 [DescribeDatabases](https://www.volcengine.com/docs/6438/1158742) 接口查询数据库列表。
            示例值：test1
        owner (str): 数据库 Owner。
            :::tip
            实例只读账号、被禁用了 DDL 权限的高权限账号或被禁用了 DDL 权限的普通账号不能作为数据库的 Owner。
            :::
            示例值：testuser
    """
    req = {
        "instance_id": instance_id,
        "db_name": db_name,
        "owner": owner,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.modify_database_owner(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="create_database",
    description="调用 CreateDatabase 接口创建数据库。"
)
def create_database(instance_id: Annotated[str, Field(description='实例 ID。可调用 [DescribeDBInstances](https://www.volcengine.com/docs/6438/1159935) 接口查询实例列表。', examples=['postgres-ca7b7019****'])],
                    db_name: Annotated[str, Field(description='数据库名称。命名规则如下：- 长度 2~63 个字符。- 由字母、数字、下划线或中划线组成。- 以字母开头，字母或数字结尾。- 不能使用保留关键字，所有被禁用的关键词请参见[禁用关键词](https://www.volcengine.com/docs/6438/80243)。', examples=['testdb1'])],
                    c_type: Optional[Annotated[str,Field(description='字符分类。取值范围： `C`（默认）、`C.UTF-8`、`en_US.utf8`、`zh_CN.utf8` 和 `POSIX`。', examples=['en_US.utf8'])]] = None,
                    character_set_name: Optional[Annotated[str,Field(description='数据库字符集。目前支持的字符集包含：`utf8`（默认）、`latin1`、`ascii`。', examples=['utf8'])]] = None,
                    collate: Optional[Annotated[str,Field(description='排序规则。取值范围：`C`（默认）、`C.UTF-8`、`en_US.utf8`、`zh_CN.utf8` 和 `POSIX`。', examples=['en_US.utf8'])]] = None,
                    owner: Optional[Annotated[str,Field(description='数据库的 owner。:::tip- 实例只读账号、被禁用了 DDL 权限的高权限账号或被禁用了 DDL 权限的普通账号不能作为数据库的 owner。- 不传值或传空值时，会为该字段取值为 rds superuser。:::', examples=['testuser'])]] = None) -> dict[str, Any]:
    """调用 CreateDatabase 接口创建数据库。

    Args:
        instance_id (str): 实例 ID。可调用 [DescribeDBInstances](https://www.volcengine.com/docs/6438/1159935) 接口查询实例列表。
            示例值：postgres-ca7b7019****
        db_name (str): 数据库名称。命名规则如下：
            - 长度 2~63 个字符。
            - 由字母、数字、下划线或中划线组成。
            - 以字母开头，字母或数字结尾。
            - 不能使用保留关键字，所有被禁用的关键词请参见[禁用关键词](https://www.volcengine.com/docs/6438/80243)。
            示例值：testdb1
        c_type (str, optional): 字符分类。取值范围： `C`（默认）、`C.UTF-8`、`en_US.utf8`、`zh_CN.utf8` 和 `POSIX`。
            示例值：en_US.utf8
        character_set_name (str, optional): 数据库字符集。目前支持的字符集包含：`utf8`（默认）、`latin1`、`ascii`。
            示例值：utf8
        collate (str, optional): 排序规则。取值范围：`C`（默认）、`C.UTF-8`、`en_US.utf8`、`zh_CN.utf8` 和 `POSIX`。
            示例值：en_US.utf8
        owner (str, optional): 数据库的 owner。
            :::tip
            - 实例只读账号、被禁用了 DDL 权限的高权限账号或被禁用了 DDL 权限的普通账号不能作为数据库的 owner。
            - 不传值或传空值时，会为该字段取值为 rds superuser。
            :::
            示例值：testuser
    """
    req = {
        "instance_id": instance_id,
        "db_name": db_name,
        "c_type": c_type,
        "character_set_name": character_set_name,
        "collate": collate,
        "owner": owner,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.create_database(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="describe_databases",
    description="调用 DescribeDatabases 接口查询数据库列表。"
)
def describe_databases(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-ca7b7019****'])],
                       db_name: Optional[Annotated[str,Field(description='数据库名称。:::tip不传值或传空值时，会查询指定实例下的所有数据库。:::', examples=['testdb1'])]] = None,
                       page_number: Optional[Annotated[int,Field(description='当前页查询偏移量，默认值为 1。', examples=['1'])]] = None,
                       page_size: Optional[Annotated[int,Field(description='每页记录数，取值应大于 0 且不超过 1000，默认值为 10。', examples=['10'])]] = None) -> dict[str, Any]:
    """调用 DescribeDatabases 接口查询数据库列表。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-ca7b7019****
        db_name (str, optional): 数据库名称。
            :::tip
            不传值或传空值时，会查询指定实例下的所有数据库。
            :::
            示例值：testdb1
        page_number (int, optional): 当前页查询偏移量，默认值为 1。
            示例值：1
        page_size (int, optional): 每页记录数，取值应大于 0 且不超过 1000，默认值为 10。
            示例值：10

    Returns: 包含以下字段的字典
        databases (list[dict[str, Any]], optional): 数据库列表。
            示例值：请参见返回示例。
        total (int, optional): 数据库总数。
            示例值：1
    """
    req = {
        "instance_id": instance_id,
        "db_name": db_name,
        "page_number": page_number,
        "page_size": page_size,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_databases(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="create_db_account",
    description="调用 CreateDBAccount 接口创建账号。"
)
def create_db_account(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-ca7b7019****'])],
                      account_name: Annotated[str, Field(description='数据库账号名称。账号名称的设置规则如下：- 长度 2~63 个字符。- 由字母、数字、下划线（_）或中划线（-）组成。- 以字母开头，字母或数字结尾。- 不能以 `pg_` 开头。- 不能使用保留关键字，所有被禁用的关键词请参见[禁用关键词](https://www.volcengine.com/docs/6438/80243)。', examples=['testuser1'])],
                      account_password: Annotated[str, Field(description='数据库账号的密码。数据库账号密码的设置规则如下：- 长度为 8~32 个字符。- 由大写字母、小写字母、数字、特殊字符中的任意三种组成。- 特殊字符为 `!@#$%^*()&_+-=`。', examples=['Test@123456'])],
                      account_type: Annotated[str, Field(description='数据库账号类型，取值范围如下：- `Super`：高权限账号。- `Normal`：普通账号。- `InstanceReadOnly`：实例只读账号。', examples=['Normal'])],
                      account_privileges: Optional[Annotated[str,Field(description='账号权限信息。多个权限中间以英文逗号（,）分隔。取值：- `Login`：登录权限。- `Inherit`：继承权限。- `CreateRole`：创建角色权限。- `CreateDB`：创建数据库权限。:::tip- 当账号类型为高权限账号时，无需传入该参数，默认支持全部权限。- 当账号类型为普通账号时，支持传入该参数，默认值为 `Login` 和 `Inherit`。- 账号类型为实例只读账号时，即 AccountType 取值为 `InstanceReadOnly` 时，不支持传入该参数。:::', examples=['Inherit,Login,CreateRole,CreateDB'])]] = None,
                      not_allow_privileges: Optional[Annotated[list[str],Field(description='为账号禁用的权限。当前仅支持取值为 `DDL`。:::tip仅支持为高权限账号或普通账号传入此字段，即 AccountType 取值为 `Super` 或 `Normal` 时。:::', examples=['DDL'])]] = None) -> dict[str, Any]:
    """调用 CreateDBAccount 接口创建账号。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-ca7b7019****
        account_name (str): 数据库账号名称。账号名称的设置规则如下：
            - 长度 2~63 个字符。
            - 由字母、数字、下划线（_）或中划线（-）组成。
            - 以字母开头，字母或数字结尾。
            - 不能以 `pg_` 开头。
            - 不能使用保留关键字，所有被禁用的关键词请参见[禁用关键词](https://www.volcengine.com/docs/6438/80243)。
            示例值：testuser1
        account_password (str): 数据库账号的密码。数据库账号密码的设置规则如下：
            - 长度为 8~32 个字符。
            - 由大写字母、小写字母、数字、特殊字符中的任意三种组成。
            - 特殊字符为 `!@#$%^*()&_+-=`。
            示例值：Test@123456
        account_type (str): 数据库账号类型，取值范围如下：
            - `Super`：高权限账号。
            - `Normal`：普通账号。
            - `InstanceReadOnly`：实例只读账号。
            示例值：Normal
        account_privileges (str, optional): 账号权限信息。多个权限中间以英文逗号（,）分隔。取值：
            - `Login`：登录权限。
            - `Inherit`：继承权限。
            - `CreateRole`：创建角色权限。
            - `CreateDB`：创建数据库权限。
            :::tip
            - 当账号类型为高权限账号时，无需传入该参数，默认支持全部权限。
            - 当账号类型为普通账号时，支持传入该参数，默认值为 `Login` 和 `Inherit`。
            - 账号类型为实例只读账号时，即 AccountType 取值为 `InstanceReadOnly` 时，不支持传入该参数。
            :::
            示例值：Inherit,Login,CreateRole,CreateDB
        not_allow_privileges (list[str], optional): 为账号禁用的权限。当前仅支持取值为 `DDL`。
            :::tip
            仅支持为高权限账号或普通账号传入此字段，即 AccountType 取值为 `Super` 或 `Normal` 时。
            :::
            示例值：DDL
    """
    req = {
        "instance_id": instance_id,
        "account_name": account_name,
        "account_password": account_password,
        "account_type": account_type,
        "account_privileges": account_privileges,
        "not_allow_privileges": not_allow_privileges,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.create_db_account(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="describe_db_accounts",
    description="调用 DescribeDBAccounts 接口查询账号列表。"
)
def describe_db_accounts(instance_id: Annotated[str, Field(description='实例 ID。', examples=['postgres-ca7b7019****'])],
                         account_name: Optional[Annotated[str,Field(description='数据库账号名称，支持模糊查询。:::tip不传值或传空值时，会查询指定实例下的所有账号。:::', examples=['testuser1'])]] = None,
                         page_number: Optional[Annotated[int,Field(description='当前页查询偏移量，默认值为 1。', examples=['1'])]] = None,
                         page_size: Optional[Annotated[int,Field(description='每页记录数，取值应大于 0 且不超过 1000，默认值为 10。', examples=['10'])]] = None) -> dict[str, Any]:
    """调用 DescribeDBAccounts 接口查询账号列表。

    Args:
        instance_id (str): 实例 ID。
            示例值：postgres-ca7b7019****
        account_name (str, optional): 数据库账号名称，支持模糊查询。
            :::tip
            不传值或传空值时，会查询指定实例下的所有账号。
            :::
            示例值：testuser1
        page_number (int, optional): 当前页查询偏移量，默认值为 1。
            示例值：1
        page_size (int, optional): 每页记录数，取值应大于 0 且不超过 1000，默认值为 10。
            示例值：10

    Returns: 包含以下字段的字典
        accounts (list[dict[str, Any]], optional): 数据库账号列表。
            示例值：请参见返回示例。
        total (int, optional): 数据库账号总数。
            示例值：1
    """
    req = {
        "instance_id": instance_id,
        "account_name": account_name,
        "page_number": page_number,
        "page_size": page_size,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource_sdk.describe_db_accounts(req)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()


"""Main entry point for the MCP server."""
def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Run the Rds Postgresql MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["streamable-http", "stdio"],
        default="stdio",
        help="Transport protocol to use (streamable-http or stdio)",
    )

    args = parser.parse_args()
    try:
        logger.info(f"Starting Rds Postgresql MCP Server with {args.transport} transport")
        mcp_server.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting Rds Postgresql MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()