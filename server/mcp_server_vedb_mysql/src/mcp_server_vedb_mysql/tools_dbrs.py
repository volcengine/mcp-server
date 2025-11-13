import logging
from typing import Any, Annotated, Optional
from pydantic import Field
from mcp_server_vedb_mysql.config import mcp as mcp_server, openapi_cli as vedbm_resource_sdk
import volcenginesdkvedbm

logger = logging.getLogger(__name__)
openapi_cli = vedbm_resource_sdk.client


@mcp_server.tool(
    description="将实例的历史数据库和表恢复至原实例中。触发示例：将实例vedbm-r3xq0zdl中的数据库src恢复为dst，使用备份ID为snap-6511-ce0d"
)
def restore_table(instance_id: str,
                  table_meta: Annotated[list[dict[str, Any]], Field(description='进行恢复的库表信息(可通过调用DescribeRecoverableTables接口查看实例可恢复的库和表)', examples=['[{"DBName":"src","NewDBName":"dst"}]'])],
                  backup_id: Optional[Annotated[str,Field(description='备份文件ID。通过调用DescribeBackups接口可查询')]] = None,
                  restore_time: Optional[Annotated[str,Field(description='UTC时间。调用DescribeRecoverableTime可查询(该参数与BackupId二选一)', examples=['2023-09-19T07:21:09Z'])]] = None) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "table_meta": table_meta,
        "backup_id": backup_id,
        "restore_time": restore_time,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.restore_table(req)
    return resp.to_dict()

@mcp_server.tool(
    description="修改指定实例的数据备份策略。触发示例：将实例vedbm-r3xq0zdl****的备份策略修改为每周一、三、五的00:00-02:00进行全量备份，保留30天"
)
def modify_backup_policy(instance_id: str,
                         backup_time: Annotated[str, Field(description='UTC', examples=['02:00Z-04:00Z','04:00Z-06:00Z'])],
                         full_backup_period: Annotated[str, Field(examples=['Monday,Wednesday'])],
                         backup_retention_period: Annotated[int, Field(description='数据备份保留天数', examples=[7])]) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "backup_time": backup_time,
        "full_backup_period": full_backup_period,
        "backup_retention_period": backup_retention_period,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.modify_backup_policy(req)
    return resp.to_dict()


@mcp_server.tool(
    description="将已有实例的备份数据恢复至一个新的实例中。触发示例：使用实例vedbm-h441603c68aaa的备份数据（备份ID：snap-64b7-5935）创建一个新实例，规格为vedb.mysql.x4.large，节点数为2，VPC为vpc-3ajzohyfaru9s340jz1rp****"
)
def restore_to_new_instance(src_instance_id: str,
                            zone_ids: str,
                            node_spec: str,
                            node_number: int,
                            vpc_id: str,
                            subnet_id: str,
                            charge_type: str,
                            auto_renew: bool = None,
                            backup_id: str = None,
                            db_minor_version: str = None,
                            deletion_protection: Optional[Annotated[str,Field(examples=['disabled','enabled'])]] = None,
                            instance_name: str = None,
                            internet_protocol: str = 'IPv4',
                            period: int = None,
                            period_unit: str = None,
                            port: int = None,
                            pre_paid_storage_in_gb: int = None,
                            project_name: str = None,
                            restore_time: str = None,
                            src_project_name: str = None,
                            storage_charge_type: str = None,
                            storage_pool_name: str = None,
                            storage_pool_type: str = None,
                            tags: list[dict[str, Any]] = None,
                            template_id: str = None,
                            zone_node_infos: list[dict[str, Any]] = None) -> dict[str, Any]:
    req = {
        "src_instance_id": src_instance_id,
        "zone_ids": zone_ids,
        "node_spec": node_spec,
        "node_number": node_number,
        "vpc_id": vpc_id,
        "subnet_id": subnet_id,
        "charge_type": charge_type,
        "auto_renew": auto_renew,
        "backup_id": backup_id,
        "continuous_backup": True,
        "db_minor_version": db_minor_version,
        "deletion_protection": deletion_protection,
        "instance_name": instance_name,
        "internet_protocol": internet_protocol,
        "period": period,
        "period_unit": period_unit,
        "port": port,
        "pre_paid_storage_in_gb": pre_paid_storage_in_gb,
        "project_name": project_name,
        "restore_time": restore_time,
        "src_project_name": src_project_name,
        "storage_charge_type": storage_charge_type,
        "storage_pool_name": storage_pool_name,
        "storage_pool_type": storage_pool_type,
        "tags": tags,
        "template_id": template_id,
        "zone_node_infos": zone_node_infos,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.restore_to_new_instance(req)
    return resp.to_dict()


@mcp_server.tool(
    description="为指定实例创建数据备份。触发示例：为实例vedbm-r3xq0zdl创建一个手动全量备份"
)
def create_backup(instance_id: str) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "backup_method": "Physical",
        "backup_type": "Full",
        "create_type": "User",
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.create_backup(req)
    return resp.to_dict()

@mcp_server.tool(
    description="删除指定实例的手动备份文件。触发示例：删除实例vedbm-r3xq0zdl的手动备份文件，备份ID为snap-a3a9-8b96"
)
def delete_backup(instance_id: str, backup_id: str) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "backup_id": backup_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.delete_backup(req)
    return resp.to_dict()


@mcp_server.tool(
    description="查询指定实例的数据备份策略。触发示例：查询实例vedbm-r3xq0zdl****当前的数据备份策略"
)
def describe_backup_policy(instance_id: str) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_backup_policy(req)
    return resp.to_dict()


@mcp_server.tool(
    description="查询指定实例的备份文件列表信息。触发示例：查询实例vedbm-r3xq0zdl****的所有成功完成的备份文件"
)
def describe_backups(instance_id: str,
                     backup_end_time: Optional[Annotated[str,Field(examples=['2023-07-16T18:52:31Z'])]] = None,
                     backup_start_time: str = None,
                     backup_status: Optional[Annotated[str,Field(examples=['Failed','Running','Success'])]] = None,
                     page_number: int = 1,
                     page_size: int = 100) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "backup_end_time": backup_end_time,
        "backup_method": "Physical",
        "backup_start_time": backup_start_time,
        "backup_status": backup_status,
        "backup_type": "Full",
        "page_number": page_number,
        "page_size": page_size,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_backups(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查询实例备份可恢复的时间范围。触发示例：查询实例vedbm-r3xq0zdl****可恢复的时间范围，用于库表恢复"
)
def describe_recoverable_time(instance_id: str,
                              for_recover_table: Optional[Annotated[bool,Field(description='用于库表恢复时传True，整实例恢复时传False')]] = None) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "for_recover_table": for_recover_table,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_recoverable_time(req)
    return resp.to_dict()


@mcp_server.tool(
    description="将目标实例从指定IP白名单中解绑。触发示例：将实例vedbm-ca12cbqv从白名单acl-c2402ba601374808aeb19d06acc2中解绑"
)
def disassociate_allow_list(allow_list_ids: list[str], instance_ids: list[str]) -> dict[str, Any]:
    req = {
        "allow_list_ids": allow_list_ids,
        "instance_ids": instance_ids,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.disassociate_allow_list(req)
    return resp.to_dict()
