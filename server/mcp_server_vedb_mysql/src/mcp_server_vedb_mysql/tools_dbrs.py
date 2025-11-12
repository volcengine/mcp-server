import logging
from typing import Any, Annotated, Optional
from pydantic import Field
from mcp_server_vedb_mysql.config import mcp as mcp_server, openapi_cli as vedbm_resource_sdk
import volcenginesdkvedbm

logger = logging.getLogger(__name__)
openapi_cli = vedbm_resource_sdk.client


@mcp_server.tool(
    description="将实例的历史数据库和表恢复至原实例中"
)
def restore_table(instance_id: str,
                  table_meta: Annotated[list[dict[str, Any]], Field(description='进行恢复的库表信息(可通过调用DescribeRecoverableTables接口查看实例可恢复的库和表)', examples=['[{"DBName":"src","NewDBName":"dst"}]'])],
                  backup_id: Optional[Annotated[str,Field(description='备份文件 ID。通过调用DescribeBackups接口可查询 `BackupID`。(该参数与 RestoreTime 参数二者必选其一。)', examples=['snap-6511****-ce0d'])]] = None,
                  restore_time: Optional[Annotated[str,Field(description='实例备份保留周期内的任意时间点，格式为 yyyy-MM-ddTHH:mm:ssZ（UTC 时间）。通过调用DescribeRecoverableTime可查询实例备份可恢复的时间范围。(该参数与 BackupId 参数二者必选其一。)', examples=['2023-09-19T07:21:09Z'])]] = None) -> dict[str, Any]:
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
    description="修改指定实例的数据备份策略"
)
def modify_backup_policy(instance_id: str,
                         backup_time: Annotated[str, Field(description='执行备份任务的时间，间隔窗口为 2 小时，且必须为偶数整点时间。格式：HH:mmZ-HH:mmZ（UTC 时间）。', examples=['00:00Z-02:00Z枚举值：00:00Z-02:00Z,02:00Z-04:00Z,04:00Z-06:00Z,06:00Z-08:00Z,08:00Z-10:00Z,10:00Z-12:00Z,12:00Z-14:00Z,14:00Z-16:00Z,16:00Z-18:00Z,18:00Z-20:00Z,20:00Z-22:00Z,22:00Z-00:00Z,22:00Z-24:00Z'])],
                         full_backup_period: Annotated[str, Field(description='全量备份周期。建议每周至少选择 2 天进行全量备份，多个取值用英文逗号（,）隔开。取值：- `Monday`：周一。- `Tuesday`：周二。- `Wednesday`：周三。- `Thursday`：周四。- `Friday`：周五。- `Saturday`：周六。- `Sunday`：周日。', examples=['Monday,Wednesday'])],
                         backup_retention_period: Annotated[int, Field(description='数据备份保留天数，取值：7~365 天。', examples=['7'])]) -> dict[str, Any]:
    """调用 ModifyBackupPolicy 接口修改指定实例的数据备份策略。

    Args:
        instance_id (str): 实例 ID。
            示例值：vedbm-r3xq0zdl****
        backup_time (str): 执行备份任务的时间，间隔窗口为 2 小时，且必须为偶数整点时间。格式：HH:mmZ-HH:mmZ（UTC 时间）。
            示例值：00:00Z-02:00Z
            枚举值：00:00Z-02:00Z,02:00Z-04:00Z,04:00Z-06:00Z,06:00Z-08:00Z,08:00Z-10:00Z,10:00Z-12:00Z,12:00Z-14:00Z,14:00Z-16:00Z,16:00Z-18:00Z,18:00Z-20:00Z,20:00Z-22:00Z,22:00Z-00:00Z,22:00Z-24:00Z
        full_backup_period (str): 全量备份周期。建议每周至少选择 2 天进行全量备份，多个取值用英文逗号（,）隔开。取值：
            - `Monday`：周一。
            - `Tuesday`：周二。
            - `Wednesday`：周三。
            - `Thursday`：周四。
            - `Friday`：周五。
            - `Saturday`：周六。
            - `Sunday`：周日。
            示例值：Monday,Wednesday
        backup_retention_period (int): 数据备份保留天数，取值：7~365 天。
            示例值：7
    """
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
    description="将已有实例的备份数据恢复至一个新的实例中"
)
def restore_to_new_instance(src_instance_id: str,
                            zone_ids: Annotated[str, Field(description='可用区 ID。(可调用DescribeAvailabilityZones接口查询实例支持的可用区资源。)', examples=['cn-beijing-b'])],
                            node_spec: Annotated[str, Field(description='实例的规格代码。详细信息，请参见[产品规格](https://www.volcengine.com/docs/6357/73614)。', examples=['vedb.mysql.x4.large'])],
                            node_number: Annotated[int, Field(description='实例节点数量。取值范围为 2~16 个。', examples=['2'])],
                            vpc_id: Annotated[str, Field(description='私有网络（VPC） ID。(您可以调用DescribeVpcs接口查询要创建实例的 VPC ID。)', examples=['vpc-3ajzohyfaru9s340jz1rp****'])],
                            subnet_id: Annotated[str, Field(description='子网 ID。子网必须属于所选的可用区。(- 子网是私有网络内的 IP 地址块，私有网络中的所有云资源都必须部署在子网内，子网为云资源分配私网 IP 地址。- 您可以调用CreateSubnet接口创建子网，调用DescribeSubnets接口查询指定可用区内的所有子网列表信息，包括子网 ID。)', examples=['subnet-1g15j13jtzgu88ibuxwqp****'])],
                            charge_type: Annotated[str, Field(description='付费类型，取值：- `PostPaid`：按量计费（后付费）。<ve>- `PrePaid`：包年包月（预付费）。</ve>', examples=['PostPaid'])],
                            auto_renew: Optional[Annotated[bool,Field(description='预付费场景下是否自动续费。取值：- `true`：自动续费。- `false`：不自动续费。(当 `ChargeType`（计算计费类型） 取值为 `PrePaid`（包年包月） 时，该参数必填。)', examples=['false'])]] = None,
                            backup_id: Optional[Annotated[str,Field(description='原实例的备份文件 ID，使用该备份文件中保存的数据创建新实例。(- 该参数与 RestoreTime 参数二者必须选择其一。- 您可以调用DescribeBackups查询指定实例的备份文件列表信息。)', examples=['snap-64b7****-5935'])]] = None,
                            continuous_backup: Optional[Annotated[bool,Field(description='ContinuousBackup', examples=[''])]] = 'true',
                            db_minor_version: Optional[Annotated[str,Field(description='根据兼容版本，选择实例的小版本，默认与原实例保持一致。<ve>关于版本号的详细说明请参见[版本号管理](https://www.volcengine.com/docs/6357/1330616)。</ve><ve>- 当原实例兼容版本为 `MySQL_5_7` 时，该参数取值默认为 `2.0`。- 当原实例兼容版本为 `MySQL_8_0` 时，该参数取值范围如下：- `3.0`：veDB MySQL 稳定版，100% 兼容 MySQL 8.0。- `3.1`：原生支持 HTAP 应用场景，加速复杂查询。- `3.2`：原生支持 HTAP 应用场景，加速复杂查询。此外，内置冷数据归档能力，可将低频访问的数据归档至对象存储 TOS 中，降低存储成本，详情请参见[冷热分离介绍](https://www.volcengine.com/docs/6357/1231210)。(- 仅支持由低版本向高版本恢复，如 **veDB** **MySQL 3.1** 可选择恢复为 **veDB MySQL 3.2**。- MySQL 5.7、HTAP 和冷热分离目前为白名单功能，如需使用，请[提交工单](https://console.volcengine.com/workorder/create)联系技术支持。- 实例创建成功后，您需要立即为该实例创建分析节点，才能正常使用 HTAP 功能，详情请参见 [ModifyDBInstanceSpec](https://www.volcengine.com/docs/6357/1120269)。)</ve>', examples=['3.0枚举值：2.0,3.0,3.1,3.2,3.3'])]] = None,
                            deletion_protection: Optional[Annotated[str,Field(description='开启或关闭实例删除保护功能，取值范围：- `enabled`：开启。- `disabled`：关闭（默认）。(开启后，将无法删除该实例。如需删除实例，您需要先关闭该功能。)', examples=['disabled枚举值：disabled,enabled'])]] = None,
                            instance_name: Optional[Annotated[str,Field(description='实例名称。命名规则：- 不能以数字、中划线（-）开头。- 只能包含中文、字母、数字、下划线（_）和中划线（-）。- 长度需在 1~128 个字符内。', examples=['Name123'])]] = None,
                            internet_protocol: Optional[Annotated[str,Field(description='InternetProtocol枚举值：DualStack,IPv4', examples=[''])]] = 'IPv4',
                            period: Optional[Annotated[int,Field(description='预付费场景下的购买时长。(当 `ChargeType`（计算计费类型） 取值为 `PrePaid`（包年包月） 时，该参数必填。)', examples=['1'])]] = None,
                            period_unit: Optional[Annotated[str,Field(description='预付费场景下的购买周期。- `Month`：包月。- `Year`：包年。(当 `ChargeType`（计算计费类型） 取值为 `PrePaid`（包年包月） 时，该参数必填。)', examples=['Month枚举值：Month,Year'])]] = None,
                            port: Optional[Annotated[int,Field(description='为实例默认创建的连接终端指定私网端口号。默认取值为 3306，取值范围为 1000~65534。(- 该配置项仅对**主节点终端**、**默认终端**<ve>、**HTAP集群终端**生效</ve>。即实例创建成功后，新建的自定义终端，端口号依旧默认为 3306。- 实例创建成功后，您也可以随时修改端口号，当前仅支持通过控制台修改端口号，操作详情请参见[修改连接地址前缀和端口](https://www.volcengine.com/docs/6357/1330611)。)', examples=['3306'])]] = None,
                            pre_paid_storage_in_gb: Optional[Annotated[int,Field(description='预付费场景下的存储空间大小。(当 `StorageChargeType`（存储计费类型） 取值为 `PrePaid`（包年包月） 时，该参数必填。)', examples=['50'])]] = None,
                            project_name: Optional[Annotated[str,Field(description='所属项目名称，创建时若该参数留空，则默认加入 `default` 项目。(项目是一个虚拟的概念，包括一组资源、用户和角色。通过项目可以对一组资源进行统一的查看和管理，并且控制项目内用户和角色管理这些资源的权限。更多详情，请参见[资源管理](https://www.volcengine.com/docs/6649/94333)。)', examples=['default'])]] = None,
                            restore_time: Optional[Annotated[str,Field(description='原实例日志备份保留时间内的任意时间点，格式为 yyyy-MM-ddTHH:mm:ssZ（UTC 时间）。(- 该参数与 BackupId 参数二者必须选择其一。- 您可以调用DescribeRecoverableTime查询指定实例可恢复的时间范围。)', examples=['2023-07-14T15:47:10Z'])]] = None,
                            src_project_name: Optional[Annotated[str,Field(description='源实例备份文件所属的项目名称。', examples=['default'])]] = None,
                            storage_charge_type: Optional[Annotated[str,Field(description='存储计费类型。不传入该参数时，存储计费类型默认与计算计费类型取值一致，取值如下：- `PostPaid`：按量计费（后付费）。<ve>- `PrePaid`：包年包月（预付费）。)warning- 当计算计费类型取值为 `PostPaid` 时，存储计费类型也只能取值为 `PostPaid`。- 当计算计费类型取值为 `PrePaid` 时，存储计费类型可取值为 `PrePaid` 或 `PostPaid`。)</ve>', examples=['PostPaid'])]] = None,
                            storage_pool_name: Optional[Annotated[str,Field(description='StoragePoolName', examples=[''])]] = None,
                            storage_pool_type: Optional[Annotated[str,Field(description='StoragePoolType枚举值：Dedicated,Serverless,Standard', examples=[''])]] = None,
                            tags: Optional[Annotated[list[dict[str, Any]],Field(description='需要绑定的标签键和标签值数组对象。(- 单次最多支持同时传入 20 组标签键值对，单个实例最多绑定 50 个标签。- 标签键值需满足设置规则，具体规则请参见[标签设置规则](https://www.volcengine.com/docs/6357/1129788#标签设置规则)。)', examples=[''])]] = None,
                            template_id: Optional[Annotated[str,Field(description='参数模板 ID。', examples=['vedbmpt-5j37992t****'])]] = None,
                            zone_node_infos: Optional[Annotated[list[dict[str, Any]],Field(description='从实例可用区的节点信息。', examples=[''])]] = None) -> dict[str, Any]:
    """调用 RestoreToNewInstance 接口将已有实例的备份数据恢复至一个新的实例中。

    Args:
        src_instance_id (str): 备份文件所属原实例的 ID。
            (
            您可以调用DescribeDBInstances接口查询实例 ID。
            )
            示例值：vedbm-h441603c68aaa****
        zone_ids (str): 可用区 ID。
            (
            可调用DescribeAvailabilityZones接口查询实例支持的可用区资源。
            )
            示例值：cn-beijing-b
        node_spec (str): 实例的规格代码。详细信息，请参见[产品规格](https://www.volcengine.com/docs/6357/73614)。
            示例值：vedb.mysql.x4.large
        node_number (int): 实例节点数量。取值范围为 2~16 个。
            示例值：2
        vpc_id (str): 私有网络（VPC） ID。
            (
            您可以调用DescribeVpcs接口查询要创建实例的 VPC ID。
            )
            示例值：vpc-3ajzohyfaru9s340jz1rp****
        subnet_id (str): 子网 ID。子网必须属于所选的可用区。
            (
            - 子网是私有网络内的 IP 地址块，私有网络中的所有云资源都必须部署在子网内，子网为云资源分配私网 IP 地址。
            - 您可以调用CreateSubnet接口创建子网，调用DescribeSubnets接口查询指定可用区内的所有子网列表信息，包括子网 ID。
            )
            示例值：subnet-1g15j13jtzgu88ibuxwqp****
        charge_type (str): 付费类型，取值：
            - `PostPaid`：按量计费（后付费）。
            <ve>- `PrePaid`：包年包月（预付费）。</ve>
            示例值：PostPaid
        auto_renew (bool, optional): 预付费场景下是否自动续费。取值：
            - `true`：自动续费。
            - `false`：不自动续费。
            (
            当 `ChargeType`（计算计费类型） 取值为 `PrePaid`（包年包月） 时，该参数必填。
            )
            示例值：false
        backup_id (str, optional): 原实例的备份文件 ID，使用该备份文件中保存的数据创建新实例。
            (
            - 该参数与 RestoreTime 参数二者必须选择其一。
            - 您可以调用DescribeBackups查询指定实例的备份文件列表信息。
            )
            示例值：snap-64b7****-5935
        continuous_backup (bool, optional): ContinuousBackup
        db_minor_version (str, optional): 根据兼容版本，选择实例的小版本，默认与原实例保持一致。<ve>关于版本号的详细说明请参见[版本号管理](https://www.volcengine.com/docs/6357/1330616)。</ve>
            <ve>
            - 当原实例兼容版本为 `MySQL_5_7` 时，该参数取值默认为 `2.0`。
            - 当原实例兼容版本为 `MySQL_8_0` 时，该参数取值范围如下：
            - `3.0`：veDB MySQL 稳定版，100% 兼容 MySQL 8.0。
            - `3.1`：原生支持 HTAP 应用场景，加速复杂查询。
            - `3.2`：原生支持 HTAP 应用场景，加速复杂查询。此外，内置冷数据归档能力，可将低频访问的数据归档至对象存储 TOS 中，降低存储成本，详情请参见[冷热分离介绍](https://www.volcengine.com/docs/6357/1231210)。
            (
            - 仅支持由低版本向高版本恢复，如 **veDB** **MySQL 3.1** 可选择恢复为 **veDB MySQL 3.2**。
            - MySQL 5.7、HTAP 和冷热分离目前为白名单功能，如需使用，请[提交工单](https://console.volcengine.com/workorder/create)联系技术支持。
            - 实例创建成功后，您需要立即为该实例创建分析节点，才能正常使用 HTAP 功能，详情请参见 [ModifyDBInstanceSpec](https://www.volcengine.com/docs/6357/1120269)。
            )
            </ve>
            示例值：3.0
            枚举值：2.0,3.0,3.1,3.2,3.3
        deletion_protection (str, optional): 开启或关闭实例删除保护功能，取值范围：
            - `enabled`：开启。
            - `disabled`：关闭（默认）。
            (
            开启后，将无法删除该实例。如需删除实例，您需要先关闭该功能。
            )
            示例值：disabled
            枚举值：disabled,enabled
        instance_name (str, optional): 实例名称。命名规则：
            - 不能以数字、中划线（-）开头。
            - 只能包含中文、字母、数字、下划线（_）和中划线（-）。
            - 长度需在 1~128 个字符内。
            示例值：Name123
        internet_protocol (str, optional): InternetProtocol
            枚举值：DualStack,IPv4
        period (int, optional): 预付费场景下的购买时长。
            (
            当 `ChargeType`（计算计费类型） 取值为 `PrePaid`（包年包月） 时，该参数必填。
            )
            示例值：1
        period_unit (str, optional): 预付费场景下的购买周期。
            - `Month`：包月。
            - `Year`：包年。
            (
            当 `ChargeType`（计算计费类型） 取值为 `PrePaid`（包年包月） 时，该参数必填。
            )
            示例值：Month
            枚举值：Month,Year
        port (int, optional): 为实例默认创建的连接终端指定私网端口号。默认取值为 3306，取值范围为 1000~65534。
            (
            - 该配置项仅对**主节点终端**、**默认终端**<ve>、**HTAP集群终端**生效</ve>。即实例创建成功后，新建的自定义终端，端口号依旧默认为 3306。
            - 实例创建成功后，您也可以随时修改端口号，当前仅支持通过控制台修改端口号，操作详情请参见[修改连接地址前缀和端口](https://www.volcengine.com/docs/6357/1330611)。
            )
            示例值：3306
        pre_paid_storage_in_gb (int, optional): 预付费场景下的存储空间大小。
            (
            当 `StorageChargeType`（存储计费类型） 取值为 `PrePaid`（包年包月） 时，该参数必填。
            )
            示例值：50
        project_name (str, optional): 所属项目名称，创建时若该参数留空，则默认加入 `default` 项目。
            (
            项目是一个虚拟的概念，包括一组资源、用户和角色。通过项目可以对一组资源进行统一的查看和管理，并且控制项目内用户和角色管理这些资源的权限。更多详情，请参见[资源管理](https://www.volcengine.com/docs/6649/94333)。
            )
            示例值：default
        restore_time (str, optional): 原实例日志备份保留时间内的任意时间点，格式为 yyyy-MM-ddTHH:mm:ssZ（UTC 时间）。
            (
            - 该参数与 BackupId 参数二者必须选择其一。
            - 您可以调用DescribeRecoverableTime查询指定实例可恢复的时间范围。
            )
            示例值：2023-07-14T15:47:10Z
        src_project_name (str, optional): 源实例备份文件所属的项目名称。
            示例值：default
        storage_charge_type (str, optional): 存储计费类型。不传入该参数时，存储计费类型默认与计算计费类型取值一致，取值如下：
            - `PostPaid`：按量计费（后付费）。
            <ve>
            - `PrePaid`：包年包月（预付费）。
            )warning
            - 当计算计费类型取值为 `PostPaid` 时，存储计费类型也只能取值为 `PostPaid`。
            - 当计算计费类型取值为 `PrePaid` 时，存储计费类型可取值为 `PrePaid` 或 `PostPaid`。
            )
            </ve>
            示例值：PostPaid
        storage_pool_name (str, optional): StoragePoolName
        storage_pool_type (str, optional): StoragePoolType
            枚举值：Dedicated,Serverless,Standard
        tags (list[dict[str, Any]], optional): 需要绑定的标签键和标签值数组对象。
            (
            - 单次最多支持同时传入 20 组标签键值对，单个实例最多绑定 50 个标签。
            - 标签键值需满足设置规则，具体规则请参见[标签设置规则](https://www.volcengine.com/docs/6357/1129788#标签设置规则)。
            )
        template_id (str, optional): 参数模板 ID。
            示例值：vedbmpt-5j37992t****
        zone_node_infos (list[dict[str, Any]], optional): 从实例可用区的节点信息。

    Returns: 包含以下字段的字典
        instance_id (str, optional): 实例 ID。
            示例值：vedbm-r3xq0zdl****
        order_id (str, optional): 订单 ID。
            示例值：Order707643373078888****
    """
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
        "continuous_backup": continuous_backup,
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
    description="为指定实例创建数据备份"
)
def create_backup(instance_id: str,
                  backup_method: Optional[Annotated[str,Field(description='备份方式，目前仅支持物理备份，取值为 `Physical`。', examples=['Physical枚举值：Physical'])]] = None,
                  backup_type: Optional[Annotated[str,Field(description='备份类型，目前仅支持全量备份，取值为 `Full`。', examples=['Full枚举值：Full'])]] = None,
                  create_type: Optional[Annotated[str,Field(description='CreateType枚举值：System,User', examples=[''])]] = None) -> dict[str, Any]:
    """调用 CreateBackup 接口为指定实例创建数据备份。

    Args:
        instance_id (str): 实例 ID。
            示例值：vedbm-r3xq0zdl****
        backup_method (str, optional): 备份方式，目前仅支持物理备份，取值为 `Physical`。
            示例值：Physical
            枚举值：Physical
        backup_type (str, optional): 备份类型，目前仅支持全量备份，取值为 `Full`。
            示例值：Full
            枚举值：Full
        create_type (str, optional): CreateType
            枚举值：System,User

    Returns: 包含以下字段的字典
        backup_id (str, optional): 备份 ID。
            示例值：snap-64b6****-7837
    """
    req = {
        "instance_id": instance_id,
        "backup_method": backup_method,
        "backup_type": backup_type,
        "create_type": create_type,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.create_backup(req)
    return resp.to_dict()

@mcp_server.tool(
    description="删除指定实例的手动备份文件"
)
def delete_backup(instance_id: str,
                  backup_id: Annotated[str, Field(description='备份文件 ID。可调用DescribeBackups接口查询指定实例的备份文件列表。(仅支持删除手动创建的备份文件，即 `CreateType` 取值为 `User`。)', examples=['snap-a3a9****-8b96'])]) -> dict[str, Any]:
    """调用 DeleteBackup 接口删除指定实例的手动备份文件。

    Args:
        instance_id (str): 实例 ID。
            示例值：vedbm-r3xq0zdl****
        backup_id (str): 备份文件 ID。可调用DescribeBackups接口查询指定实例的备份文件列表。
            (
            仅支持删除手动创建的备份文件，即 `CreateType` 取值为 `User`。
            )
            示例值：snap-a3a9****-8b96
    """
    req = {
        "instance_id": instance_id,
        "backup_id": backup_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.delete_backup(req)
    return resp.to_dict()


@mcp_server.tool()
def describe_backup_policy(instance_id: str) -> dict[str, Any]:
    """查询指定实例的数据备份策略
    Returns: 
        backup_retention_period: 数据备份保留天数，取值：7~365 天
        backup_time: 执行备份任务的时间，间隔窗口为 2 小时，且必须为偶数整点时间。格式：HH:mmZ-HH:mmZ（UTC 时间）
        full_backup_period: 全量备份周期，多个取值用英文逗号隔开。示例值：Monday,Wednesday
    """
    req = {
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_backup_policy(req)
    return resp.to_dict()


@mcp_server.tool(
    description="查询指定实例的备份文件列表信息"
)
def describe_backups(instance_id: str,
                     backup_end_time: Optional[Annotated[str,Field(description='备份创建的最晚时间，格式：yyyy-MM-ddTHH:mm:ssZ（UTC 时间），以备份任务开始执行的时间为准。', examples=['2023-07-16T18:52:31Z'])]] = None,
                     backup_method: Optional[Annotated[str,Field(description='备份方式，目前仅支持物理备份，取值为 `Physical`。', examples=['Physical枚举值：Physical'])]] = None,
                     backup_start_time: Optional[Annotated[str,Field(description='备份创建的最早时间，格式：yyyy-MM-ddTHH:mm:ssZ（UTC 时间），以备份任务开始执行的时间为准。', examples=['2023-07-14T18:43:00Z'])]] = None,
                     backup_status: Optional[Annotated[str,Field(description='备份状态，取值：- `Success`：成功。- `Failed`：失败。- `Running`：执行中。', examples=['Success枚举值：Failed,Running,Success'])]] = None,
                     backup_type: Optional[Annotated[str,Field(description='备份类型，目前仅支持全量备份，取值为 `Full`。', examples=['Full枚举值：Full'])]] = None,
                     page_number: Optional[Annotated[int,Field(description='页码，取值大于等于 1，且不超过 Integer 的最大值，默认值为 1。', examples=['1'])]] = '1',
                     page_size: Optional[Annotated[int,Field(description='每页记录数。取值范围 1~1000，默认值为 10。', examples=['10'])]] = '10') -> dict[str, Any]:
    """调用 DescribeBackups 接口查询指定实例的备份文件列表信息。

    Args:
        instance_id (str): 实例 ID。
            示例值：vedbm-r3xq0zdl****
        backup_end_time (str, optional): 备份创建的最晚时间，格式：yyyy-MM-ddTHH:mm:ssZ（UTC 时间），以备份任务开始执行的时间为准。
            示例值：2023-07-16T18:52:31Z
        backup_method (str, optional): 备份方式，目前仅支持物理备份，取值为 `Physical`。
            示例值：Physical
            枚举值：Physical
        backup_start_time (str, optional): 备份创建的最早时间，格式：yyyy-MM-ddTHH:mm:ssZ（UTC 时间），以备份任务开始执行的时间为准。
            示例值：2023-07-14T18:43:00Z
        backup_status (str, optional): 备份状态，取值：
            - `Success`：成功。
            - `Failed`：失败。
            - `Running`：执行中。
            示例值：Success
            枚举值：Failed,Running,Success
        backup_type (str, optional): 备份类型，目前仅支持全量备份，取值为 `Full`。
            示例值：Full
            枚举值：Full
        page_number (int, optional): 页码，取值大于等于 1，且不超过 Integer 的最大值，默认值为 1。
            示例值：1
        page_size (int, optional): 每页记录数。取值范围 1~1000，默认值为 10。
            示例值：10

    Returns: 包含以下字段的字典
        backups_info (list[dict[str, Any]], optional): 备份列表。
        total (int, optional): 符合查询条件的数量。
            示例值：2
    """
    req = {
        "instance_id": instance_id,
        "backup_end_time": backup_end_time,
        "backup_method": backup_method,
        "backup_start_time": backup_start_time,
        "backup_status": backup_status,
        "backup_type": backup_type,
        "page_number": page_number,
        "page_size": page_size,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_backups(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查询实例备份可恢复的时间范围"
)
def describe_recoverable_time(instance_id: str,
                              for_recover_table: Optional[Annotated[bool,Field(description='用于库表恢复时传True，整实例恢复时传False')]] = None) -> dict[str, Any]:
    """调用 DescribeRecoverableTime 接口查询实例备份可恢复的时间范围。

    Args:
        instance_id (str): 实例 ID。
            示例值：vedbm-r3xq0zdl****
        for_recover_table (bool, optional): ForRecoverTable

    Returns: 包含以下字段的字典
        recoverable_time_info (list[dict[str, Any]], optional): 实例可恢复的时间范围，为空表示实例目前不可恢复。
    """
    req = {
        "instance_id": instance_id,
        "for_recover_table": for_recover_table,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_recoverable_time(req)
    return resp.to_dict()


@mcp_server.tool(
    description="将目标实例从指定 IP 白名单中解绑"
)
def disassociate_allow_list(allow_list_ids: Annotated[list[str], Field(description='需要解绑实例的白名单 ID。(* 您可以调用DescribeAllowLists接口查询指定地域下白名单列表信息，包括白名单 ID。* 不支持同时传入多个实例 ID 和白名单 ID，即仅允许一次为多个实例同时解绑同一个白名单，或为一个实例同时解绑多个白名单。)', examples=['["acl-c2402ba601374808aeb19d06acc2****"]'])],
                            instance_ids: Annotated[list[str], Field(description='需要解绑白名单的实例 ID。(* 您可以调用DescribeDBInstances接口查询目标地域下所有实例的基本信息，包括实例 ID。* 不支持同时传入多个实例 ID 和白名单 ID，即仅允许一次为多个实例同时解绑同一个白名单，或为一个实例同时解绑多个白名单。)', examples=['["vedbm-ca12cbqv****"]'])]) -> dict[str, Any]:
    """调用 DisassociateAllowList 接口将目标实例从指定 IP 白名单中解绑。 

    Args:
        allow_list_ids (list[str]): 需要解绑实例的白名单 ID。
            (
            * 您可以调用DescribeAllowLists接口查询指定地域下白名单列表信息，包括白名单 ID。
            * 不支持同时传入多个实例 ID 和白名单 ID，即仅允许一次为多个实例同时解绑同一个白名单，或为一个实例同时解绑多个白名单。
            )
            示例值：["acl-c2402ba601374808aeb19d06acc2****"]
        instance_ids (list[str]): 需要解绑白名单的实例 ID。
            (
            * 您可以调用DescribeDBInstances接口查询目标地域下所有实例的基本信息，包括实例 ID。
            * 不支持同时传入多个实例 ID 和白名单 ID，即仅允许一次为多个实例同时解绑同一个白名单，或为一个实例同时解绑多个白名单。
            )
            示例值：["vedbm-ca12cbqv****"]
    """
    req = {
        "allow_list_ids": allow_list_ids,
        "instance_ids": instance_ids,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.disassociate_allow_list(req)
    return resp.to_dict()
