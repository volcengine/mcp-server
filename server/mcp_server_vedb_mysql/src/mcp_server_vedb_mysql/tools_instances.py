import logging
from typing import Any, Final, Literal, Annotated, Optional
from pydantic import Field
from mcp_server_vedb_mysql.config import mcp as mcp_server, openapi_cli as vedbm_resource_sdk
import volcenginesdkvedbm

logger = logging.getLogger(__name__)
openapi_cli = vedbm_resource_sdk.client


@mcp_server.tool(
    description="Retrieve a list of all VeDB MySQL instances for the user, including a batch of instance IDs and basic information",
)
def list_vedb_mysql_instances(
    # query: Optional[str] = None
) -> dict[str, Any]:
    logger.info(f"list_vedb_mysql_instances")
    batch_size: Final = 100

    req = volcenginesdkvedbm.models.DescribeDBInstancesRequest(
        page_size=batch_size,
        page_number=1,
    )
    rsp = volcenginesdkvedbm.models.DescribeDBInstancesResponse(instances=[])

    try:
        while True:
            rsp_page = openapi_cli.describe_db_instances(req)
            rsp.instances.extend(rsp_page.instances)
            if len(rsp_page.instances) < batch_size:
                break
            req.page_number += 1

        rsp.total = len(rsp.instances)
        return rsp.to_dict()

    except Exception as e:
        logger.error(f"Error in describe: {str(e)}")
        return {"error": str(e)}


@mcp_server.tool(
    description="Retrieve detailed information about a specific VeDB MySQL instance",
)
def describe_vedb_mysql_detail(
    instance_id: str
) -> dict[str, Any]:
    logger.info("describe_vedb_mysql_detail")

    req = volcenginesdkvedbm.models.DescribeDBInstanceDetailRequest(instance_id=instance_id)
    try:
        rsp = openapi_cli.describe_db_instance_detail(req)
        return rsp.to_dict()

    except Exception as e:
        logger.error(f"Error in describe: {str(e)}")
        return {"error": str(e)}


@mcp_server.tool(
    description="Modify a specific VeDB MySQL instance's alias",
)
def modify_vedb_mysql_instance_alias(
        instance_id: str, new_alias: str
) -> dict[str, Any]:
    logger.info("modify_vedb_mysql_instance_alias")

    req = volcenginesdkvedbm.models.ModifyDBInstanceNameRequest(
        instance_id=instance_id,
        instance_new_name=new_alias,
    )

    try:
        openapi_cli.modify_db_instance_name(req)
        return {"success": "true"}

    except Exception as e:
        logger.error(f"Error in describe: {str(e)}")
        return {"error": str(e)}


@mcp_server.tool(
    description="Create a VeDB MySQL instance",
)
def create_vedb_mysql_instance(
    instance_alias: str,
    zone_id: str,
    vpc_id: str,
    subnet_id: Annotated[str, Field(description='<可参考现有实例属性>')],
    db_version: Literal["MySQL_8_0", "MySQL_5_7"] = "MySQL_8_0",
    lower_case_table_names: bool = False,
) -> dict[str, Any]:
    logger.info("create_vedb_mysql_instance")

    req = volcenginesdkvedbm.models.CreateDBInstanceRequest(
        charge_type="PostPaid",
        instance_name=instance_alias,
        db_engine_version=db_version,
        db_minor_version="3.0" if db_version == "MySQL_8_0" else "2.0",
        node_spec="vedb.mysql.g4.large",
        node_number=2,
        lower_case_table_names="0" if lower_case_table_names else "1",
        vpc_id=vpc_id,
        subnet_id=subnet_id,
        zone_ids=zone_id,
        tags=[volcenginesdkvedbm.TagForCreateDBInstanceInput(key="Source", value="CreateFromMCP")],
    )

    instance_id = openapi_cli.create_db_instance(req).instance_id

    # wait running
    start_at = time.time()
    running = False
    while time.time() - start_at < 20*60:
        rsp = describe_vedb_mysql_detail(instance_id=instance_id)
        if 'error' not in rsp and rsp['instance_detail']['instance_status'] == 'Running':
            running = True
            break
        time.sleep(3)

    rsp = {
        "instance_id": instance_id,
        "suggests": ["Create a network AllowList", "Bind AllowList for " + instance_id]
    }
    if not running:
        rsp["suggests"] = "Wait for instance creating finish (Running status)"
    return rsp


# @mcp_server.tool(
#     description="开启或关闭实例删除保护功能"
# )
def switch_instance_deletion_protection(deletion_protection: Annotated[str, Field(examples=['disabled','enabled'])],
                                                  instance_id: str) -> dict[str, Any]:
    req = {
        "deletion_protection": deletion_protection,
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.modify_db_instance_deletion_protection_policy(req)
    return resp.to_dict()


# @mcp_server.tool()
def describe_db_instance_version(instance_id: str) -> dict[str, Any]:
    """查询目标实例的版本
    Returns: 
        实例兼容版本。`MySQL_8_0`，`MySQL_5_7`
        实例小版本。示例值：3.0
        实例内核版本。示例值：3.0.1.1
    """
    req = {
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_db_instance_version(req)
    return resp.to_dict()

@mcp_server.tool(
    description="为实例绑定标签，支持批量操作"
)
def add_tags_to_resource(instance_ids: list[str],
                         tags: list[dict[str, Any]]) -> str:
    req = {
        "instance_ids": instance_ids,
        "tags": tags,
    }
    req = {k: v for k, v in req.items() if v is not None}
    vedbm_resource_sdk.add_tags_to_resource(req)
    return "success"

@mcp_server.tool(
    description="为实例解绑标签，支持批量操作"
)
def remove_tags_from_resource(instance_ids: list[str],
                              all: Optional[Annotated[bool,Field(description='是否解绑指定实例上的所有标签')]] = None,
                              tag_keys: list[str] = None) -> str:
    req = {
        "instance_ids": instance_ids,
        "all": all,
        "tag_keys": tag_keys,
    }
    req = {k: v for k, v in req.items() if v is not None}
    vedbm_resource_sdk.remove_tags_from_resource(req)
    return "success"

# @mcp_server.tool(
#     description="修改指定实例的节点配置"
# )
def modify_db_instance_spec(instance_id: str,
                            node_spec: Annotated[str, Field(examples=['vedb.mysql.g4.4xlarge','vedb.mysql.g4.large'])],
                            node_number: int,
                            schedule_type: Annotated[str, Field(examples=['Immediate','MaintainTime'])],
                            pre_paid_storage_in_gb: Optional[Annotated[int,Field(description='若存储计费类型为包年包月，则需输入变更后的存储空间大小', examples=[60])]] = None,
                            zone_node_infos: Optional[Annotated[list[dict[str, Any]],Field(description='从实例可用区的节点信息')]] = None) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "node_spec": node_spec,
        "node_number": node_number,
        "schedule_type": schedule_type,
        "one_step_order": True,
        "pre_paid_storage_in_gb": pre_paid_storage_in_gb,
        "zone_node_infos": zone_node_infos,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.modify_db_instance_spec(req)
    return resp.to_dict()


# @mcp_server.tool(
#     description="重启实例或重启单个节点"
# )
def restart_db_instance(instance_id: str,
                        schedule_type: Annotated[str, Field(examples=['Immediate','MaintainTime'])],
                        node_id: Optional[Annotated[str,Field(description='传入该参数时，表示重启指定的节点', examples=['vedbm-****-1'])]] = None) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "schedule_type": schedule_type,
        "node_id": node_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.restart_db_instance(req)
    return resp.to_dict()


@mcp_server.tool(
    description="切换实例主节点到指定节点"
)
def change_master(instance_id: str,
                  target_node: Annotated[str, Field(examples=['vedbm-gzwdsf9b-0'])]) -> str:
    req = {
        "cluster_name": instance_id,
        "target_node": target_node,
    }
    req = {k: v for k, v in req.items() if v is not None}
    vedbm_resource_sdk.change_master(req)
    return "success"


# @mcp_server.tool(
#     description="删除实例"
# )
def delete_db_instance(instance_id: str) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "data_keep_policy": "Last",
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.delete_db_instance(req)
    return resp.to_dict()
