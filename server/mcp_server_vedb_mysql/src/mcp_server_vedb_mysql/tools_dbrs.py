import logging
from typing import Any, Annotated, Optional
from pydantic import Field
from mcp_server_vedb_mysql.config import mcp as mcp_server, openapi_cli as vedbm_resource_sdk
import volcenginesdkvedbm

logger = logging.getLogger(__name__)
openapi_cli = vedbm_resource_sdk.client


@mcp_server.tool(
    description="将已有实例的备份数据恢复至一个新的实例中。触发示例：使用实例vedbm-****的备份数据（备份ID：snap-**-**）创建一个新实例，规格为vedb.mysql.x4.large，节点数为2，VPC和子网与原实例保持一致"
)
def restore_to_new_instance(src_instance_id: str,
                            zone_ids: str,
                            vpc_id: str,
                            subnet_id: str,
                            node_number: int = 2,
                            node_spec: str = "vedb.mysql.g4.large",
                            charge_type: str = "PostPaid",
                            auto_renew: bool = None,
                            backup_id: str = None,
                            db_minor_version: str = "3.0",
                            deletion_protection: Optional[Annotated[str,Field(examples=['disabled','enabled'])]] = None,
                            instance_name: str = "new_restored",
                            period: int = None,
                            period_unit: str = None,
                            port: int = None,
                            pre_paid_storage_in_gb: int = None,
                            project_name: str = None,
                            restore_time: str = None,
                            src_project_name: str = None,
                            storage_charge_type: str = None,
                            tags: list[dict[str, Any]] = None,
                            template_id: str = None) -> dict[str, Any]:
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
        "db_minor_version": db_minor_version,
        "deletion_protection": deletion_protection,
        "instance_name": instance_name,
        "period": period,
        "period_unit": period_unit,
        "port": port,
        "pre_paid_storage_in_gb": pre_paid_storage_in_gb,
        "project_name": project_name,
        "restore_time": restore_time,
        "src_project_name": src_project_name,
        "storage_charge_type": storage_charge_type,
        "tags": tags,
        "template_id": template_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.restore_to_new_instance(req)
    return resp.to_dict()


@mcp_server.tool(
    description="为指定实例创建数据备份。触发示例：为实例vedbm-instanceid创建一个手动全量备份"
)
def create_backup(instance_id: str) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "backup_method": "Physical",
        "backup_type": "Full",
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.create_backup(req)
    return resp.to_dict()


@mcp_server.tool(
    description="查询指定实例的数据备份策略。触发示例：查询实例vedbm-****当前的数据备份策略"
)
def get_backup_policy(instance_id: str) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_backup_policy(req)
    return resp.to_dict()


@mcp_server.tool(
    description="查询指定实例的备份列表。触发示例：查询实例vedbm-instanceid的所有成功完成的快照"
)
def list_backups(instance_id: str,
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
    description="查询实例备份可恢复的时间范围"
)
def get_recoverable_time(instance_id: str) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_recoverable_time(req)
    return resp.to_dict()
