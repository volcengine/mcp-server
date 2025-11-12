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


@mcp_server.tool(
    description="开启或关闭实例删除保护功能"
)
def switch_instance_deletion_protection(deletion_protection: Annotated[str, Field(description='开启或关闭实例删除保护功能。取值范围：- `enabled`：开启。- `disabled`：关闭。', examples=['enabled枚举值：disabled,enabled'])],
                                                  instance_id: str) -> dict[str, Any]:
    req = {
        "deletion_protection": deletion_protection,
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.modify_db_instance_deletion_protection_policy(req)
    return resp.to_dict()


@mcp_server.tool()
def describe_db_instance_version(instance_id: str) -> dict[str, Any]:
    """查询目标实例的版本
    Returns: 包含以下字段的字典
        db_engine_version: 实例兼容版本。取值范围：`MySQL_8_0`，`MySQL_5_7`
        db_minor_version: 实例小版本。示例值：3.0
        db_revision_version: 实例内核版本。示例值：3.0.1.1
    """
    req = {
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_db_instance_version(req)
    return resp.to_dict()

@mcp_server.tool(
    description="为一个或多个实例绑定标签"
)
def add_tags_to_resource(instance_ids: Annotated[list[str], Field(description='需要绑定标签的实例 ID。(- 您可以调用DescribeDBInstances接口查询目标地域下所有实例的基本信息，包括实例 ID。- 单次最多支持同时传入 20 个实例 ID，单个实例最多绑定 50 个标签。)', examples=['["vedbm-r3xq0zdl****"]'])],
                         tags: Annotated[list[dict[str, Any]], Field(description='需要绑定的标签键和标签值数组对象。(- 单次最多支持同时传入 20 组标签键值对，单个实例最多支持绑定 50 个标签。- 标签键值需满足设置规则，具体规则请参见[标签设置规则](https://www.volcengine.com/docs/6357/1129788#标签设置规则)。)', examples=[''])]) -> dict[str, Any]:
    req = {
        "instance_ids": instance_ids,
        "tags": tags,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.add_tags_to_resource(req)
    return resp.to_dict()

@mcp_server.tool(
    description="为一个或多个实例解绑标签"
)
def remove_tags_from_resource(instance_ids: Annotated[list[str], Field(description='需要解绑标签的实例 ID。(- 您可以调用DescribeDBInstances接口查询目标地域下所有实例的基本信息，包括实例 ID。- 单次最多支持同时传入 20 个实例 ID。)', examples=['["vedbm-r3xq0zdl****"]'])],
                              all: Optional[Annotated[bool,Field(description='是否解绑指定实例上的所有标签。取值范围：- `true`：解绑指定实例上的所有标签。- `false`：不解绑指定实例上的所有标签（默认）。(仅当 `TagKeys` 取值为空时，`All` 参数才生效。)', examples=['false'])]] = None,
                              tag_keys: Optional[Annotated[list[str],Field(description='需要解绑的标签键。(- 单次最多支持同时传入 20 个标签键。- 当 `InstanceIds` 为多个实例 ID 时，所有实例存在传入标签键的标签都会被解绑，请谨慎操作。)', examples=['["instancetype", "chargetype"]'])]] = None) -> dict[str, Any]:
    req = {
        "instance_ids": instance_ids,
        "all": all,
        "tag_keys": tag_keys,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.remove_tags_from_resource(req)
    return resp.to_dict()

@mcp_server.tool(
    description="修改指定实例的节点配置"
)
def modify_db_instance_spec(instance_id: str,
                            node_spec: Annotated[str, Field(description='实例的节点规格代码。(关于实例节点规格的详细信息，请参见[产品规格](https://www.volcengine.com/docs/6357/73614)。)', examples=['vedb.mysql.x4.xlarge枚举值：vedb.mysql.g4.2xlarge,vedb.mysql.g4.4xlarge,vedb.mysql.g4.large,vedb.mysql.g4.xlarge,vedb.mysql.g8.2xlarge,vedb.mysql.x4.2xlarge,vedb.mysql.x4.4xlarge,vedb.mysql.x4.8xlarge,vedb.mysql.x4.large,vedb.mysql.x4.xlarge,vedb.mysql.x8.2xlarge,vedb.mysql.x8.4xlarge,vedb.mysql.x8.6xlarge,vedb.mysql.x8.8xlarge,vedb.mysql.x8.large,vedb.mysql.x8.xlarge'])],
                            node_number: Annotated[int, Field(description='实例节点数量。取值范围为 2~16 个。', examples=['2'])],
                            schedule_type: Annotated[str, Field(description='执行方式，取值：- `Immediate`：立即执行（默认）。- `MaintainTime`：可维护时间段执行。', examples=['Immediate枚举值：Immediate,MaintainTime,SpecifiedTime'])],
                            pre_paid_storage_in_gb: Optional[Annotated[int,Field(description='- 若存储计费类型为按量计费，则无需选择存储容量，存储容量会随数据量的增减而自动弹性伸缩，根据实际使用量按小时计费。- 若存储计费类型为包年包月，则需输入变更后的存储空间大小，步长为 10GiB，单位为 GiB。(不同的节点规格，存储空间取值范围不同，详情请参见[产品规格](https://www.volcengine.com/docs/6357/73614)。)', examples=['60'])]] = None,
                            zone_node_infos: Optional[Annotated[list[dict[str, Any]],Field(description='从实例可用区的节点信息。', examples=[''])]] = None) -> dict[str, Any]:
    """调用 ModifyDBInstanceSpec 接口修改指定实例的节点配置。

    Args:
        instance_id (str): 实例 ID。
            示例值：vedbm-r3xq0zdl****
        node_spec (str): 实例的节点规格代码。
            (
            关于实例节点规格的详细信息，请参见[产品规格](https://www.volcengine.com/docs/6357/73614)。
            )
            示例值：vedb.mysql.x4.xlarge
            枚举值：vedb.mysql.g4.2xlarge,vedb.mysql.g4.4xlarge,vedb.mysql.g4.large,vedb.mysql.g4.xlarge,vedb.mysql.g8.2xlarge,vedb.mysql.x4.2xlarge,vedb.mysql.x4.4xlarge,vedb.mysql.x4.8xlarge,vedb.mysql.x4.large,vedb.mysql.x4.xlarge,vedb.mysql.x8.2xlarge,vedb.mysql.x8.4xlarge,vedb.mysql.x8.6xlarge,vedb.mysql.x8.8xlarge,vedb.mysql.x8.large,vedb.mysql.x8.xlarge
        node_number (int): 实例节点数量。取值范围为 2~16 个。
            示例值：2
        schedule_type (str): 执行方式，取值：
            - `Immediate`：立即执行（默认）。
            - `MaintainTime`：可维护时间段执行。
            示例值：Immediate
            枚举值：Immediate,MaintainTime,SpecifiedTime
        one_step_order (bool, optional): OneStepOrder
        pre_paid_storage_in_gb (int, optional): - 若存储计费类型为按量计费，则无需选择存储容量，存储容量会随数据量的增减而自动弹性伸缩，根据实际使用量按小时计费。
            - 若存储计费类型为包年包月，则需输入变更后的存储空间大小，步长为 10GiB，单位为 GiB。
            (
            不同的节点规格，存储空间取值范围不同，详情请参见[产品规格](https://www.volcengine.com/docs/6357/73614)。
            )
            示例值：60
        zone_node_infos (list[dict[str, Any]], optional): 从实例可用区的节点信息。

    Returns: 包含以下字段的字典
        instance_id (str, optional): 实例 ID。
            示例值：vedbm-r3xq0zdl****
        order_id (str, optional): 订单 ID。
            示例值：Order707643373078888****
        schedule_event_id (str, optional): ScheduleEventId
    """
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


@mcp_server.tool(
    description="重启实例"
)
def restart_db_instance(instance_id: str,
                        schedule_type: Annotated[str, Field(description='执行方式，取值：- `Immediate`：立即执行（默认）。- `MaintainTime`：可维护时间段执行。', examples=['Immediate枚举值：Immediate,MaintainTime,SpecifiedTime'])],
                        node_id: Optional[Annotated[str,Field(description='需要要重启的节点 ID。(当传入该参数时，表示重启指定的节点。不传入该参数时，表示重启整个实例（所有节点）。)', examples=['vedbm-r3xq0zdl****-1'])]] = None) -> dict[str, Any]:
    """调用 RestartDBInstance 接口重启实例。

    Args:
        instance_id (str): 实例 ID。
            示例值：vedbm-r3xq0zdl****
        schedule_type (str): 执行方式，取值：
            - `Immediate`：立即执行（默认）。
            - `MaintainTime`：可维护时间段执行。
            示例值：Immediate
            枚举值：Immediate,MaintainTime,SpecifiedTime
        node_id (str, optional): 需要要重启的节点 ID。
            (
            当传入该参数时，表示重启指定的节点。不传入该参数时，表示重启整个实例（所有节点）。
            )
            示例值：vedbm-r3xq0zdl****-1

    Returns: 包含以下字段的字典
        schedule_event_id (str, optional): ScheduleEventId
    """
    req = {
        "instance_id": instance_id,
        "schedule_type": schedule_type,
        "node_id": node_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.restart_db_instance(req)
    return resp.to_dict()


@mcp_server.tool(
    description="切换主节点"
)
def change_master(cluster_name: Annotated[str, Field(description='实例 ID。', examples=['vedbm-gzwdsf9b****'])],
                  target_node: Annotated[str, Field(description='需要切换为主节点的只读节点 ID。', examples=['vedbm-gzwdsf9b****-0'])]) -> dict[str, Any]:
    """调用 ChangeMaster 接口切换主节点。

    Args:
        cluster_name (str): 实例 ID。
            示例值：vedbm-gzwdsf9b****
        target_node (str): 需要切换为主节点的只读节点 ID。
            示例值：vedbm-gzwdsf9b****-0
    """
    req = {
        "cluster_name": cluster_name,
        "target_node": target_node,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.change_master(req)
    return resp.to_dict()


@mcp_server.tool(
    description="删除实例"
)
def delete_db_instance(instance_id: str,
                       data_keep_policy: Optional[Annotated[str,Field(description='删除实例时的备份保留策略。仅支持取值为 `Last`，表示创建并保留一个最终备份文件。(- 若未传入该参数，则不保留备份。- 删除时，即便此参数传入了 All，系统也会将其转换为 Last。)', examples=['Last枚举值：Last'])]] = None) -> dict[str, Any]:
    """调用 DeleteDBInstance 接口删除实例。

    Args:
        instance_id (str): 实例 ID。
            示例值：vedbm-r3xq0zdl****
        data_keep_policy (str, optional): 删除实例时的备份保留策略。仅支持取值为 `Last`，表示创建并保留一个最终备份文件。
            (
            - 若未传入该参数，则不保留备份。
            - 删除时，即便此参数传入了 All，系统也会将其转换为 Last。
            )
            示例值：Last
            枚举值：Last
    """
    req = {
        "instance_id": instance_id,
        "data_keep_policy": data_keep_policy,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.delete_db_instance(req)
    return resp.to_dict()
