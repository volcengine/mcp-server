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
    description="查询实例列表 (Query instance list)\n\n查询一个或多个ECS实例的详细信息，包括实例ID、规格、状态、可用区、计费方式等。\n支持按实例ID、名称、状态、规格族、可用区、计费方式等条件过滤。",
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
        has_more = False

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

            if not response:
                handle_error("describe_instances")

            # 空列表是正常情况（用户没有实例）
            instances = getattr(response, "instances", None) or []
            for instance in instances:
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

            if len(total_results) >= needNum:
                total_results = total_results[:needNum]
                has_more = response.next_token is not None
                break

            if not response.next_token:
                break

            next_token = response.next_token

        # 添加分页提示
        hint = ""
        if has_more:
            hint = f" (当前返回{len(total_results)}条，还有更多实例。可通过 instanceIds/instanceName/status/zoneId 等参数过滤)"

        return [types.TextContent(type="text", text=f"Results{hint}: {total_results}")]

    except Exception as e:
        handle_error("describe_instances", e)


@mcp.tool(
    name="describe_images",
    description="查询镜像列表 (Query image list)\n\n查询可用的镜像信息，包括公共镜像、自定义镜像和共享镜像。\n支持按镜像ID、名称、平台、可见性等条件过滤。",
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

            if not response:
                handle_error("describe_images")

            images = getattr(response, "images", None) or []
            for image in images:
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
        handle_error("describe_images", e)


@mcp.tool(
    name="describe_instance_types",
    description="查询实例规格列表 (Query instance type list)\n\n查询ECS实例规格的详细信息，包括vCPU、内存、GPU、网络、存储等配置。\n规格数量较多(1000+)，建议先调用 describe_instance_type_families 了解规格族分类，再通过 instanceTypeIds 精确查询。",
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
        description="指定查询的实例规格ID，如 ecs.g3i.large、ecs.pni2.14xlarge。可先调用 describe_instance_type_families 获取规格族，再拼接规格ID",
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
        has_more = False

        while True:
            response = volc_client.describe_instance_types(
                volcenginesdkecs.DescribeInstanceTypesRequest(
                    image_id=imageId,
                    instance_type_ids=instanceTypeIds,
                    max_results=20,
                    next_token=next_token,
                )
            )

            if not response:
                handle_error("describe_instance_types")

            instance_types = getattr(response, "instance_types", None) or []
            for instance_type in instance_types:
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

            if len(total_results) >= needNum:
                total_results = total_results[:needNum]
                # 如果还有 next_token，说明可能还有更多
                has_more = response.next_token is not None
                break

            if not response.next_token:
                break

            next_token = response.next_token

        # 添加分页提示，引导模型进行精确查询
        hint = ""
        if has_more:
            hint = f" (当前返回{len(total_results)}条，还有更多规格。建议通过 instanceTypeIds 精确查询特定规格，或先调用 describe_instance_type_families 了解规格族分类)"

        return [types.TextContent(type="text", text=f"Results{hint}: {total_results}")]

    except Exception as e:
        handle_error("describe_instance_types", e)


@mcp.tool(
    name="describe_available_resource",
    description="查询可用资源 (Query available zone resource)\n\n查询指定地域或可用区内可购买的资源信息，包括实例规格、云盘类型、专有宿主机规格的可用性。\n用于创建实例前确认资源是否可用。",
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

        if not response:
            handle_error("describe_available_resource")

        available_zones = getattr(response, "available_zones", None) or []
        for available_zone in available_zones:
            filtered_available_zone = {
                "RegionId": available_zone.region_id,
                "ZoneId": available_zone.zone_id,
                "Status": available_zone.status,
                "AvailableResources": available_zone.available_resources,
            }
            total_results.append(filtered_available_zone)

        return [types.TextContent(type="text", text=f"Results: {total_results}")]

    except Exception as e:
        handle_error("describe_available_resource", e)


@mcp.tool(
    name="start_instances",
    description="启动实例 (Start instances)\n\n启动一台或多台已停止的ECS实例。\n实例必须处于已停止(STOPPED)状态才能启动。",
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
            handle_error("start_instances")

        return [
            types.TextContent(
                type="text", text=f"Results: {response.operation_details}"
            )
        ]

    except Exception as e:
        handle_error("start_instances", e)


@mcp.tool(
    name="renew_instance",
    description="续费实例 (Renew instance)\n\n为包年包月实例续费，延长实例的使用时间。\n仅支持包年包月(PrePaid)计费方式的实例。",
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
            handle_error("renew_instance")

        return [types.TextContent(type="text", text=f"Results: {response.order_id}")]

    except Exception as e:
        handle_error("renew_instance", e)


@mcp.tool(
    name="describe_instance_type_families",
    description="""查询实例规格族列表 (Query instance type families)

查询ECS实例规格族信息，了解不同规格族的用途和特点。
建议先调用此接口了解规格族分类，再通过 describe_instance_types 查询具体规格。

规格族命名规则：ecs.<类型><代数>[后缀]，如 ecs.g3i.large 表示第三代通用型Intel实例
规格族分类：
- 通用型(g): ecs.g3i/g3a/g2i 等，vCPU与内存比1:4，适合均衡计算场景
- 计算型(c): ecs.c3i/c3a/c2i 等，vCPU与内存比1:2，适合计算密集型场景
- 内存型(r): ecs.r3i/r3a/r2i 等，vCPU与内存比1:8，适合内存密集型场景
- 本地SSD型(i): ecs.i3s 等，配备本地NVMe SSD，适合高IO场景
- 大数据型(d): ecs.d3c/d2c 等，配备大容量本地HDD，适合大数据存储场景
- 高主频型(hf): ecs.hfg2/hfc2/hfr2 等，高主频CPU，适合高性能Web前端
- 共享型(s): ecs.s3 等，共享CPU资源，适合轻量级应用
- 突发性能型(t): ecs.t3 等，可积累CPU积分，适合突发性能需求
- GPU计算型: ecs.pni2(A100/A800)/g1v(V100)/g1ie(T4) 等，适合AI/ML/深度学习
- GPU渲染型: ecs.vgn2i 等，配备vGPU，适合图形渲染
- 高性能计算GPU型(hpc): ecs.hpcpni2/hpcg3ib 等，配备RDMA网络，适合HPC场景
- 高性能计算CPU型: ecs.hpcc3i 等，适合科学计算
- 弹性裸金属(ebm): ecs.ebmg3i/ebmc3i/ebmr3i 等，物理机级别性能

""",
)
async def describe_instance_type_families(
    region: str = Field(
        default="cn-beijing",
        description="默认为cn-beijing. 可为：ap-southeast-1, cn-beijing2, cn-shanghai, cn-guangzhou 等",
    ),
    generation: str = Field(
        default="",
        description="实例规格族的世代。取值：ecs-1（第一代）、ecs-2（第二代）、ecs-3（第三代）、ecs-4（第四代）",
    ),
    zoneId: str = Field(
        default="",
        description="可用区ID，您可以调用DescribeZones查询一个地域下的可用区信息",
    ),
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client(region)

        response = volc_client.describe_instance_type_families(
            volcenginesdkecs.DescribeInstanceTypeFamiliesRequest(
                generation=generation if generation else None,
                zone_id=zoneId if zoneId else None,
            )
        )

        if not response:
            handle_error("describe_instance_type_families")

        instance_type_families = (
            getattr(response, "instance_type_families", None) or []
        )
        total_results = []
        for family in instance_type_families:
            filtered_family = {
                "InstanceTypeFamily": family.instance_type_family,
                "Generation": family.generation,
                "ZoneIds": family.zone_ids,
            }
            total_results.append(filtered_family)

        return [types.TextContent(type="text", text=f"Results: {total_results}")]

    except Exception as e:
        handle_error("describe_instance_type_families", e)


@mcp.tool(
    name="get_console_output",
    description="获取实例控制台输出 (Get instance console output)\n\n获取ECS实例的串口控制台输出信息，用于诊断实例启动问题。\n可查看实例启动过程中的系统日志，帮助排查启动失败等问题。",
)
async def get_console_output(
    region: str = Field(
        default="cn-beijing",
        description="默认为cn-beijing. 可为：ap-southeast-1, cn-beijing2, cn-shanghai, cn-guangzhou 等",
    ),
    instanceId: str = Field(
        description="实例ID（必填）",
    ),
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client(region)

        response = volc_client.get_console_output(
            volcenginesdkecs.GetConsoleOutputRequest(
                instance_id=instanceId,
            )
        )

        if not response:
            handle_error("get_console_output")

        result = {
            "InstanceId": getattr(response, "instance_id", None),
            "Output": getattr(response, "output", None),
            "LastUpdateAt": getattr(response, "last_update_at", None),
        }

        return [types.TextContent(type="text", text=f"Results: {result}")]

    except Exception as e:
        handle_error("get_console_output", e)


@mcp.tool(
    name="get_console_screenshot",
    description="获取实例控制台截图 (Get instance console screenshot)\n\n获取正在运行的ECS实例的JPEG格式屏幕截图。\n用于诊断实例运行状态，如查看系统是否正常启动、是否出现蓝屏等问题。",
)
async def get_console_screenshot(
    region: str = Field(
        default="cn-beijing",
        description="默认为cn-beijing. 可为：ap-southeast-1, cn-beijing2, cn-shanghai, cn-guangzhou 等",
    ),
    instanceId: str = Field(
        description="实例ID（必填）",
    ),
    wakeUp: bool = Field(
        default=False,
        description="是否唤醒处于休眠状态的实例",
    ),
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client(region)

        response = volc_client.get_console_screenshot(
            volcenginesdkecs.GetConsoleScreenshotRequest(
                instance_id=instanceId,
                wake_up=wakeUp,
            )
        )

        if not response:
            handle_error("get_console_screenshot")

        result = {
            "InstanceId": getattr(response, "instance_id", None),
            "Screenshot": getattr(response, "screenshot", None),  # Base64 编码的截图
        }

        return [types.TextContent(type="text", text=f"Results: {result}")]

    except Exception as e:
        handle_error("get_console_screenshot", e)
