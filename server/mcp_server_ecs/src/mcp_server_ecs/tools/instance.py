"""
Instance related tool functions
"""

from typing import List

import volcenginesdkecs
from mcp import types
from pydantic import Field
from volcenginesdkecs.models import *

from mcp_server_ecs.common.client import get_volc_ecs_client
from mcp_server_ecs.common.errors import handle_error
from mcp_server_ecs.tools import mcp


@mcp.tool(
    name="describe_instances",
    description="Query instance list",
)
async def describe_instances(
    region: str = Field(
        default="cn-beijing",
        description="默认为cn-beijing. 可为：ap-southeast-1, cn-beijing2, cn-shanghai, cn-guangzhou 等",
    ),
    eipAddresses: List[str] = Field(
        default=[],
        description="公网IP地址，最多支持100个。您可以调用DescribeEipAddresses接口查询公网IP地址",
    ),
    instanceChargeType: str = Field(
        default="",
        description="实例的计费方式，取值：PostPaid：按量计费，PrePaid：包年包月",
    ),
    instanceIds: List[str] = Field(
        default=[],
        description="实例ID，最多支持100个",
    ),
    instanceName: str = Field(
        default="",
        description="实例的名称，支持关键字模糊查询",
    ),
    instanceTypeFamilies: List[str] = Field(
        default=[],
        description="根据规格族过滤实例，最多支持100个实例规格族",
    ),
    instanceTypeIds: List[str] = Field(
        default=[],
        description="根据规格过滤实例，最多支持100个实例规格",
    ),
    projectName: str = Field(
        default="",
        description="资源所属项目，一个资源只能归属于一个项目。只能包含字母、数字、下划线'_'、点'.'和中划线'-'。长度限制在64个字符以内",
    ),
    status: str = Field(
        default="",
        description="实例的状态，取值：CREATING：创建中，RUNNING：运行中，STOPPING：停止中，STOPPED：已停止，REBOOTING: 重启中，STARTING：启动中，REBUILDING：重装中，RESIZING：更配中，ERROR：错误，DELETING：删除中",
    ),
    zoneId: str = Field(
        default="",
        description="实例所属可用区ID。您可以调用DescribeZones查询一个地域下的可用区信息",
    ),
    needNum: int = Field(
        default=20,
        description="实例较多时，可以通过该字段控制查询总数，需要根据用户的意图来设置",
    ),
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client(region)
        total_results = []
        next_token = None

        while True:
            response = volc_client.describe_instances(
                volcenginesdkecs.DescribeInstancesRequest(
                    eip_addresses=eipAddresses,
                    instance_charge_type=instanceChargeType,
                    instance_ids=instanceIds,
                    instance_name=instanceName,
                    instance_type_families=instanceTypeFamilies,
                    instance_types=instanceTypeIds,
                    project_name=projectName,
                    status=status,
                    zone_id=zoneId,
                    max_results=20,
                    next_token=next_token,
                )
            )

            if not response or not getattr(response, "instances", None):
                return handle_error("describe_instances")

            for instance in response.instances:
                filtered_instance = {
                    "Cpus": instance.cpus,
                    "CpuOptions": instance.cpu_options,
                    "CreatedAt": instance.created_at,
                    "EipAddress": instance.eip_address,
                    "ExpiredAt": instance.expired_at,
                    "ImageId": instance.image_id,
                    "InstanceChargeType": instance.instance_charge_type,
                    "InstanceId": instance.instance_id,
                    "InstanceTypeId": instance.instance_type_id,
                    "MemorySize": instance.memory_size,
                    "OsName": instance.os_name,
                    "ProjectName": instance.project_name,
                    "Status": instance.status,
                    "StoppedMode": instance.stopped_mode,
                    "ZoneId": instance.zone_id,
                    "LocalVolumes": instance.local_volumes,
                }
                total_results.append(filtered_instance)

            if len(total_results) >= needNum or not response.next_token:
                total_results = total_results[:needNum]
                break

            next_token = response.next_token

        return [types.TextContent(type="text", text=f"Results: {total_results}")]

    except Exception as e:
        return handle_error("describe_instances", e)


@mcp.tool(
    name="describe_images",
    description="Query image list",
)
async def describe_images(
    region: str = Field(
        default="cn-beijing",
        description="默认为cn-beijing. 可为：ap-southeast-1, cn-beijing2, cn-shanghai, cn-guangzhou 等",
    ),
    imageIds: List[str] = Field(
        default=[],
        description="镜像的ID，最多支持100个ID",
    ),
    imageName: str = Field(default="", description="镜像名称"),
    instanceTypeId: str = Field(
        default="",
        description="实例的规格ID，传入本参数时，将返回该规格可用的镜像ID列表",
    ),
    platform: str = Field(
        default="",
        description="镜像操作系统的发行版本。取值：CentOS，Debian，veLinux，Windows Server，Fedora，OpenSUSE，Ubuntu",
    ),
    projectName: str = Field(default="", description="资源所属项目"),
    status: List[str] = Field(
        default=[],
        description="镜像状态，最多支持10个。取值：available（默认）：可用，creating：创建中，error：错误",
    ),
    visibility: str = Field(
        default="",
        description="镜像的可见性。取值：public：公共镜像，private：自定义镜像，shared：共享镜像",
    ),
    needNum: int = Field(
        default=20,
        description="镜像较多时，可以通过该字段控制查询总数，需要根据用户的意图来设置",
    ),
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client(region)
        total_results = []
        next_token = None

        while True:
            response = volc_client.describe_images(
                volcenginesdkecs.DescribeImagesRequest(
                    image_ids=imageIds,
                    image_name=imageName,
                    instance_type_id=instanceTypeId,
                    platform=platform,
                    project_name=projectName,
                    status=status,
                    visibility=visibility,
                    max_results=20,
                    next_token=next_token,
                )
            )

            if not response or not getattr(response, "images", None):
                return handle_error("describe_images")

            for image in response.images:
                filtered_image = {
                    "Architecture": image.architecture,
                    "BootMode": image.boot_mode,
                    "ProjectName": image.project_name,
                    "CreatedAt": image.created_at,
                    "ImageId": image.image_id,
                    "ImageName": image.image_name,
                    "Kernel": image.kernel,
                    "OsName": image.os_name,
                    "OsType": image.os_type,
                    "Platform": image.platform,
                    "PlatformVersion": image.platform_version,
                    "Size": image.size,
                    "Visibility": image.visibility,
                }
                total_results.append(filtered_image)

            if len(total_results) >= needNum or not response.next_token:
                total_results = total_results[:needNum]
                break

            next_token = response.next_token

        return [types.TextContent(type="text", text=f"Results: {total_results}")]

    except Exception as e:
        return handle_error("describe_images", e)


@mcp.tool(
    name="describe_instance_types",
    description="Query instance type list",
)
async def describe_instance_types(
    region: str = Field(
        default="cn-beijing",
        description="默认为cn-beijing. 可为：ap-southeast-1, cn-beijing2, cn-shanghai, cn-guangzhou 等",
    ),
    imageId: str = Field(
        default="",
        description="镜像ID，查询该镜像可创建的实例规格",
    ),
    instanceTypeIds: List[str] = Field(
        default=[],
        description="指定查询的实例规格",
    ),
    needNum: int = Field(
        default=20,
        description="实例规格较多时，可以通过该字段控制查询总数，需要根据用户的意图来设置",
    ),
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client(region)
        total_results = []
        next_token = None

        while True:
            response = volc_client.describe_instance_types(
                volcenginesdkecs.DescribeInstanceTypesRequest(
                    image_id=imageId,
                    instance_type_ids=instanceTypeIds,
                    max_results=20,
                    next_token=next_token,
                )
            )

            if not response or not getattr(response, "instance_types", None):
                return handle_error("describe_instance_types")

            for instance_type in response.instance_types:
                filtered_instance_type = {
                    "GPU": instance_type.gpu,
                    "InstanceTypeFamily": instance_type.instance_type_family,
                    "InstanceTypeId": instance_type.instance_type_id,
                    "Memory": instance_type.memory,
                    "Processor": instance_type.processor,
                    "Network": instance_type.network,
                    "Rdma": instance_type.rdma,
                    "Volume": instance_type.volume,
                    "LocalVolumes": instance_type.local_volumes,
                }
                total_results.append(filtered_instance_type)

            if len(total_results) >= needNum or not response.next_token:
                total_results = total_results[:needNum]
                break

            next_token = response.next_token

        return [types.TextContent(type="text", text=f"Results: {total_results}")]

    except Exception as e:
        return handle_error("describe_instance_types", e)


@mcp.tool(
    name="describe_available_resource",
    description="Query available zone resource",
)
async def describe_available_resource(
    region: str = Field(
        default="cn-beijing",
        description="默认为cn-beijing. 可为：ap-southeast-1, cn-beijing2, cn-shanghai, cn-guangzhou 等",
    ),
    destinationResource: str = Field(
        default="",
        description="要查询的资源类型(必填参数)。取值：InstanceType：实例规格。VolumeType：云盘类型。DedicatedHost：专有宿主机规格。专有宿主机规格请参见规格介绍",
    ),
    instanceChargeType: str = Field(
        default="",
        description="资源的计费类型。取值：PostPaid：按量计费。PrePaid：包年包月。ReservedInstance：预留实例券",
    ),
    instanceTypeId: str = Field(
        default="", description="指定一个要查询的实例规格或专有宿主机规格"
    ),
    zoneId: str = Field(
        default="",
        description="可用区ID，您可以调用DescribeZones查询一个地域下的可用区信息。说明：默认为空，表示返回当前地域（RegionId）下的所有可用区中所有符合条件的资源，比如：cn-beijing-a",
    ),
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client(region)
        total_results = []

        response = volc_client.describe_available_resource(
            volcenginesdkecs.DescribeAvailableResourceRequest(
                destination_resource=destinationResource,
                instance_charge_type=instanceChargeType,
                instance_type_id=instanceTypeId,
                zone_id=zoneId,
            )
        )

        if not response or not getattr(response, "available_zones", None):
            return handle_error("describe_available_resource")

        for available_zone in response.available_zones:
            filtered_available_zone = {
                "RegionId": available_zone.region_id,
                "ZoneId": available_zone.zone_id,
                "Status": available_zone.status,
                "AvailableResources": available_zone.available_resources,
            }
            total_results.append(filtered_available_zone)

        return [types.TextContent(type="text", text=f"Results: {total_results}")]

    except Exception as e:
        return handle_error("describe_available_resource", e)


@mcp.tool(
    name="start_instances",
    description="Start instances",
)
async def start_instances(
    region: str = Field(
        default="cn-beijing",
        description="默认为cn-beijing. 可为：ap-southeast-1, cn-beijing2, cn-shanghai, cn-guangzhou 等",
    ),
    instanceIds: List[str] = Field(
        default=[],
        description="实例ID，最多支持100个",
    ),
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client(region)

        response = volc_client.start_instances(
            volcenginesdkecs.StartInstancesRequest(
                instance_ids=instanceIds,
            )
        )

        if not response or not getattr(response, "operation_details", None):
            return handle_error("start_instances")

        return [
            types.TextContent(
                type="text", text=f"Results: {response.operation_details}"
            )
        ]

    except Exception as e:
        return handle_error("start_instances", e)


@mcp.tool(
    name="renew_instance",
    description="Renew instance",
)
async def renew_instance(
    region: str = Field(
        default="cn-beijing",
        description="默认为cn-beijing. 可为：ap-southeast-1, cn-beijing2, cn-shanghai, cn-guangzhou 等",
    ),
    instanceId: str = Field(
        default="",
        description="实例ID",
    ),
    period: int = Field(
        default=1,
        description="续费的月数，取值：1、2、3、4、5、6、7、8、9、12、24、36",
    ),
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client(region)

        response = volc_client.renew_instance(
            volcenginesdkecs.RenewInstanceRequest(
                instance_id=instanceId,
                period=period,
                period_unit="Month",
            )
        )

        if not response or not getattr(response, "order_id", None):
            return handle_error("renew_instance")

        return [types.TextContent(type="text", text=f"Results: {response.order_id}")]

    except Exception as e:
        return handle_error("renew_instance", e)
