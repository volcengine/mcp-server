note = {
    "describe_zones": r""" 
   Args: 
       body: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            RegionId ( String ): 是  指定查询的 Region ID。 
    """,
    "describe_instances": r""" 
   Args: 
       body: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Filters ( Array of InstanceListFilter ): 否   
            PageSize ( Integer ): 否  每页展示数量，默认为 10 
            TagFilter ( Object of TagFilter ): 否  标签过滤选项 
            PageNumber ( Integer ): 否  第几页，默认为 1 
            ProjectName ( String ): 否  项目名称 
           "字段"： InstanceListFilter
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Name ( String ): 否  过滤条件名称。支持的查询条件如下： 
                  - InstanceId：实例 ID 
                  - InstanceName：实例名称 
                  - ZoneId：可用区 ID 
                  - Status：实例状态 
                  - Version：实例版本 
                  - ChargeType：计费类型 
            Values ( Array of String ): 否  用于筛选的字符串值。 
                  - Performs a case-insensitive substring match. 
                  - Treats input as a raw string; regular expressions and wildcards are NOT supported. 
           "字段"： TagFilter
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Key ( String ): 是  标签筛选键 
            Values ( Array of String ): 是  标签筛选值列表 
    """,
    "create_instance_in_one_step": r""" 
   Args: 
       body: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            NetSwitch ( Object of NetSwitch ): 否   
            ClientToken ( String ): 否  唯一标识符，用于保证请求幂等性。建议使用 UUID。 
            PackageSaleId ( String ): 否   
            InstanceConfiguration ( Object of InstanceConfigurationAssign ): 是  实例配置详情 
           "字段"： NetSwitch
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            SalesArea ( Boolean ): 否   
            PublicServiceArea ( Boolean ): 否   
           "字段"： InstanceConfigurationAssign
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            VPC ( Object of VpcInfo ): 是  实例的私有网络。 
            Period ( Integer ): 否  包年包月实例的购买时长，单位：月 
            Subnet ( Object of SubnetInfo ): 是  实例的子网。 
            UseTos ( Boolean ): 否  是否使用对象存储(TOS)。 
            ZoneId ( String ): 是  实例所在可用区。 
                  如果是多可用区部署，则填写多个 ZoneId，使用英文逗号分隔，如cn-beijing-a,cn-beijing-c。最左侧的 ZoneId 为主可用区，其余为备可用区。 
            Version ( String ): 是  实例版本。这也决定了实例类型。 
                  - ES (ElasticSearch) 类型实例可选版本：V6_8, V7_10, V8_18。推荐 V7_10。 
                  - OS (OpenSearch) 类型实例可选版本：OPEN_SEARCH_2_9。 
            IpFamily ( String ): 否  ipv4(仅有 ipv4 地址),dualstack(有 ipv4 和 ipv6 地址) 
            LogLevel ( String ): 否   
            RegionId ( String ): 是  实例所在区域 
            AutoRenew ( Boolean ): 否  包年包月实例是否配置自动续费。  
                  - true：自动续费，系统会在每次到期前自动为实例续费。  
                  - false：未开启自动续费，需要在实例到期前进行手动续费。 
            Byte2Cloud ( Object of Byte2Cloud ): 否  内场上云配置。请勿设置，该功能仅限内部使用。 
            ChargeType ( String ): 是  实例计费类型。建议优先选择按量计费。 
                  - PostPaid：按量计费。 
                  - PrePaid：包年包月。 
            InstanceId ( String ): 否  实例 ID。仅限内部使用，请勿设置。 
            SubnetList ( Array of SubnetInfo ): 否  设置实例的子网信息列表 
            EnableHttps ( Boolean ): 是  是否启用 HTTPS 访问协议。 
                  - true：启用 HTTPS 访问。 
                  - false：不启用 HTTPS，使用 HTTP 访问。（如果选择使用 HTTP 访问，将无需安全认证即可访问，并使用 HTTP 明文传输数据。您需要确保访问环境的安全性，且不要将访问接口暴露在公网环境上。） 
            ProjectName ( String ): 否  云搜索实例所属的项目，用于云资源的分组管理。  
                  - 项目是火山引擎提供的一种资源管理方式，有利于维护资源独立、数据安全；同时可从项目维度查看资源消费账单，便于计算云资源使用成本。 
            InstanceName ( String ): 是  自定义设置实例名称。  
                  - 只能包含中文、字母、数字、短横线（-）和下划线（_），开头和结尾不能是数字和短横线（-）。  
                  - 长度在 1～128 个字符内。 
            NetworkSpecs ( Array of NetworkSpec ): 否  实例公网规格配置 
            ResourceTags ( Array of TagInfo ): 否  支持为实例添加标签，可以更方便的识别和管理实例。实例最多支持添加 20 个标签。 
                  标签为键值对样式，设置时注意以下事项：  
                  - 只支持大小写字母、数字、中文和特殊字符.:/=+-_@，键值大小写敏感。  
                  - Key 不允许以volc:、Volc:、vOlc:、volc:......（16 种组合）开头。  
                  - Key 长度为 1128 字符；Value 长度为 0256 字符。 
            AdminPassword ( String ): 是  管理员密码。取值规则如下： 
                  - 密码至少包含大写字母、小写字母、数字和特殊字符中的三种，长度为 8～32 个字符。  
                  - 支持_#!@$%^&*()+=-特殊字符，不可以包含空格和中文。 
            EnableCerebro ( Boolean ): 否  是否开启 Cerebro。 
                  - true：开启 Cerebro。 
                  - false：不开启 Cerebro。 
            UserEniEnabled ( Boolean ): 否   
            EnablePureMaster ( Boolean ): 否  是否创建专用 Master 节点。生产环境、关键环境、较大规模集群建议开启。测试和演示环境建议关闭。 
                  - true：创建专用 Master 节点，Master 节点数量应该为 3 个。 
                  - false：不创建专用 Master 节点，Master 功能将内置在 Hot 节点。 
            NodeSpecsAssigns ( Array of NodeSpecsAssign ): 是  实例中各种节点的数量和规格配置。 
            ScaleCheckDetail ( Object of ScaleCheckDetailDTO ): 否   
            ConfigurationCode ( String ): 否  计费配置码，可以通过调用DescribeNodeAvailableSpecs接口获得。 
            DeletionProtection ( Boolean ): 否  是否开启实例删除保护功能，取值说明如下：  
                  - true：开启实例删除保护。（开启实例删除保护后，您将无法通过控制台或者 API 删除实例。） 
                  - false：关闭实例删除保护。 
           "字段"： VpcInfo
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            VpcId ( String ): 是  VPC ID 
            VpcName ( String ): 是  VPC 名称 
           "字段"： SubnetInfo
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            SubnetId ( String ): 是  Subnet ID 
            SubnetName ( String ): 是  Subnet 名称 
           "字段"： Byte2Cloud
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Idc ( String ): 否   
            Psm ( String ): 否   
            Consul ( String ): 否   
            Enabled ( Boolean ): 否   
            EsImageTag ( String ): 否   
            MasterNodes ( String ): 否   
            AttrNodeSetEnabled ( Boolean ): 否   
           "字段"： NetworkSpec
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Type ( String ): 否  公网应用类型Elasticsearch：es实例使用。Kibana：Dashboard使用 
            IsOpen ( Boolean ): 否  开启/关闭 
            SpecName ( String ): 否  网络资源规格名称 
            Bandwidth ( Integer ): 否  公网IP的带宽上限，默认为“1”，单位：Mbps。 
           "字段"： TagInfo
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Type ( String ): 是  标签类型。  
                  - CUSTOM：自定义标签。  
                  - SYSTEM：系统标签。 
            TagKvs ( JSON Map ): 否  更新的标签键值对 
            TagKeys ( Array of String ): 否  待删除标签键列表 
           "字段"： NodeSpecsAssign
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Type ( String ): 是  节点类型： 
                  - Master：专用主节点（负责元数据和集群管理）。  
                  - Hot：热数据节点。  
                  - Cold：冷数据节点。  
                  - Warm：温数据节点。  
                  - Kibana：数据可视化仪表板节点。  
                  - Coordinator：专用协调节点（负责数据的分发、汇总、归约）。 
            Number ( Integer ): 是  - 数据节点：数量范围 1~100（需含 ≥1 个 Hot 节点）。 
                  	- 生产建议：单可用区 ≥3；双可用区 ≥4；三可用区 ≥6。  
                  - Master 节点： 
                    - 若禁用 EnablePureMaster，则不要配置 Master 节点。 
                    - 若启用 EnablePureMaster，则数量 = 3。 
                  - Kibana 节点：固定为 1。 
                  - Coordinator 节点：可选，范围 2~50（生产建议 ≥2）。 
                  - Warm 节点：可选，上限 100（生产建议 ≥3）。 
            StorageSize ( Integer ): 是  存储容量，单位为 GiB，取值需为 10 的整数倍。 
                  - 默认值为 100 GiB，调整步长为 10 GiB。  
                  - Master 节点的 StorageSize 设置为 20 GiB，即"StorageSize": 20。  
                  - Kibana 节点的 StorageSize 设置为 0，即"StorageSize": 0。 
            StorageSpecName ( String ): 是  存储规格名称。 
                  - 可以调用 DescribeNodeAvailableSpecs 接口获取可用的存储规格列表。 
                  - Kibana 节点的 StorageSpecName 设置为空，即 "StorageSpecName": ""。 
            ExtraPerformance ( Object of ExtraPerformanceDTO ): 否  额外性能包 
            ResourceSpecName ( String ): 是  计算资源规格名称。 
                  - 可以调用 DescribeNodeAvailableSpecs 接口获取可用的节点规格列表。  
                  - 数据节点不能使用 x2.small (1c2g, 1 cpu core + 2g ram) 的实例。 
           "字段"： ScaleCheckDetailDTO
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            HealthCheck ( Boolean ): 否   
            ZoneScaleRet ( Object of ZoneScaleRet ): 否   
            CreateNetSpecs ( Array of NetworkSpec ): 否   
            ModifyNetSpecs ( Array of NetworkSpec ): 否   
            ReleaseNetSpecs ( Array of NetworkSpec ): 否   
            OnlyNetEipChange ( Boolean ): 否   
            NodeTypesForDiskScaleDown ( JSON Map ): 否   
            NodeTypesForDiskExtraUpdate ( JSON Map ): 否   
            NodeTypesForDiskTypeScaleUp ( JSON Map ): 否   
           "字段"： ExtraPerformanceDTO
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Throughput ( Integer ): 否  额外性能包吞吐量大小，单位为MB 
           "字段"： ZoneScaleRet
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            expectZoneIds ( Array of String ): 否   
            zoneScaleCode ( String ): 否   
            currentZoneIds ( Array of String ): 否   
           "字段"： NodeTypesForDiskScaleDown
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Type ( String ): 否  节点类型： 
                  - Master：专用主节点（负责元数据和集群管理）。  
                  - Hot：热数据节点。  
                  - Cold：冷数据节点。  
                  - Warm：温数据节点。  
                  - Kibana：数据可视化仪表板节点。  
                  - Coordinator：专用协调节点（负责数据的分发、汇总、归约）。 
            Number ( Integer ): 否  - 数据节点：数量范围 1~100（需含 ≥1 个 Hot 节点）。 
                  	- 生产建议：单可用区 ≥3；双可用区 ≥4；三可用区 ≥6。  
                  - Master 节点： 
                    - 若禁用 EnablePureMaster，则不要配置 Master 节点。 
                    - 若启用 EnablePureMaster，则数量 = 3。 
                  - Kibana 节点：固定为 1。 
                  - Coordinator 节点：可选，范围 2~50（生产建议 ≥2）。 
                  - Warm 节点：可选，上限 100（生产建议 ≥3）。 
            StorageSize ( Integer ): 否  存储容量，单位为 GiB，取值需为 10 的整数倍。 
                  - 默认值为 100 GiB，调整步长为 10 GiB。  
                  - Master 节点的 StorageSize 设置为 20 GiB，即"StorageSize": 20。  
                  - Kibana 节点的 StorageSize 设置为 0，即"StorageSize": 0。 
            StorageSpecName ( String ): 否  存储规格名称。 
                  - 可以调用 DescribeNodeAvailableSpecs 接口获取可用的存储规格列表。 
                  - Kibana 节点的 StorageSpecName 设置为空，即 "StorageSpecName": ""。 
            ExtraPerformance ( Object of ExtraPerformanceDTO ): 否  额外性能包 
            ResourceSpecName ( String ): 否  计算资源规格名称。 
                  - 可以调用 DescribeNodeAvailableSpecs 接口获取可用的节点规格列表。  
                  - 数据节点不能使用 x2.small (1c2g, 1 cpu core + 2g ram) 的实例。 
           "字段"： NodeTypesForDiskExtraUpdate
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Type ( String ): 否  节点类型： 
                  - Master：专用主节点（负责元数据和集群管理）。  
                  - Hot：热数据节点。  
                  - Cold：冷数据节点。  
                  - Warm：温数据节点。  
                  - Kibana：数据可视化仪表板节点。  
                  - Coordinator：专用协调节点（负责数据的分发、汇总、归约）。 
            Number ( Integer ): 否  - 数据节点：数量范围 1~100（需含 ≥1 个 Hot 节点）。 
                  	- 生产建议：单可用区 ≥3；双可用区 ≥4；三可用区 ≥6。  
                  - Master 节点： 
                    - 若禁用 EnablePureMaster，则不要配置 Master 节点。 
                    - 若启用 EnablePureMaster，则数量 = 3。 
                  - Kibana 节点：固定为 1。 
                  - Coordinator 节点：可选，范围 2~50（生产建议 ≥2）。 
                  - Warm 节点：可选，上限 100（生产建议 ≥3）。 
            StorageSize ( Integer ): 否  存储容量，单位为 GiB，取值需为 10 的整数倍。 
                  - 默认值为 100 GiB，调整步长为 10 GiB。  
                  - Master 节点的 StorageSize 设置为 20 GiB，即"StorageSize": 20。  
                  - Kibana 节点的 StorageSize 设置为 0，即"StorageSize": 0。 
            StorageSpecName ( String ): 否  存储规格名称。 
                  - 可以调用 DescribeNodeAvailableSpecs 接口获取可用的存储规格列表。 
                  - Kibana 节点的 StorageSpecName 设置为空，即 "StorageSpecName": ""。 
            ExtraPerformance ( Object of ExtraPerformanceDTO ): 否  额外性能包 
            ResourceSpecName ( String ): 否  计算资源规格名称。 
                  - 可以调用 DescribeNodeAvailableSpecs 接口获取可用的节点规格列表。  
                  - 数据节点不能使用 x2.small (1c2g, 1 cpu core + 2g ram) 的实例。 
           "字段"： NodeTypesForDiskTypeScaleUp
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Type ( String ): 否  节点类型： 
                  - Master：专用主节点（负责元数据和集群管理）。  
                  - Hot：热数据节点。  
                  - Cold：冷数据节点。  
                  - Warm：温数据节点。  
                  - Kibana：数据可视化仪表板节点。  
                  - Coordinator：专用协调节点（负责数据的分发、汇总、归约）。 
            Number ( Integer ): 否  - 数据节点：数量范围 1~100（需含 ≥1 个 Hot 节点）。 
                  	- 生产建议：单可用区 ≥3；双可用区 ≥4；三可用区 ≥6。  
                  - Master 节点： 
                    - 若禁用 EnablePureMaster，则不要配置 Master 节点。 
                    - 若启用 EnablePureMaster，则数量 = 3。 
                  - Kibana 节点：固定为 1。 
                  - Coordinator 节点：可选，范围 2~50（生产建议 ≥2）。 
                  - Warm 节点：可选，上限 100（生产建议 ≥3）。 
            StorageSize ( Integer ): 否  存储容量，单位为 GiB，取值需为 10 的整数倍。 
                  - 默认值为 100 GiB，调整步长为 10 GiB。  
                  - Master 节点的 StorageSize 设置为 20 GiB，即"StorageSize": 20。  
                  - Kibana 节点的 StorageSize 设置为 0，即"StorageSize": 0。 
            StorageSpecName ( String ): 否  存储规格名称。 
                  - 可以调用 DescribeNodeAvailableSpecs 接口获取可用的存储规格列表。 
                  - Kibana 节点的 StorageSpecName 设置为空，即 "StorageSpecName": ""。 
            ExtraPerformance ( Object of ExtraPerformanceDTO ): 否  额外性能包 
            ResourceSpecName ( String ): 否  计算资源规格名称。 
                  - 可以调用 DescribeNodeAvailableSpecs 接口获取可用的节点规格列表。  
                  - 数据节点不能使用 x2.small (1c2g, 1 cpu core + 2g ram) 的实例。 
    """,
    "describe_node_available_specs": r""" 
   Args: 
       body: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            InstanceId ( String ): 否  需要查询的实例 ID 
    """,
    "describe_instance_plugins": r""" 
   Args: 
       body: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            InstanceId ( String ): 是  实例 ID 
    """,
    "rename_instance": r""" 
   Args: 
       body: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            NewName ( String ): 是  自定义设置实例新名称。 
                  - 格式要求：长度 1-128 字符，支持中文、英文、数字、下划线及短横线，不能以数字或短横线开头。 
            InstanceId ( String ): 是  需要修改名称的实例 ID 
    """,
    "modify_maintenance_setting": r""" 
   Args: 
       body: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            InstanceId ( String ): 是  需要设置可维护时间段的实例 ID 
            MaintenanceDay ( Array of String ): 是  一周内允许平台进行维护的日期列表 
                  - 示例：["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] 
            MaintenanceTime ( String ): 是  在一天内允许平台进行维护的 UTC 时间段。 
                  - 示例："23:00-01:00" 
    """,
    "modify_deletion_protection": r""" 
   Args: 
       body: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            InstanceId ( String ): 是  需要启停删除保护功能的实例 ID 
            DeletionProtection ( Boolean ): 是  是否开启实例删除保护功能。true：开启实例删除保护false：默认值，关闭实例删除保护 
    """,
    "describe_instance": r""" 
   Args: 
       body: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            InstanceId ( String ): 是  需要查询配置详情的实例 ID 
    """,
    "restart_node": r""" 
   Args: 
       body: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Force ( Boolean ): 否  标识是否是一次强制重启，默认为false，取值说明如下：true：此次操作强制重启实例false：此次操作非强制重启 
            NodeName ( String ): 是  需要重启的成员节点 ID，调用 DescribeInstanceNodes 接口可获取成员节点列表 
            InstanceId ( String ): 是  需要重启节点的实例 ID 
    """,
    "describe_instance_nodes": r""" 
   Args: 
       body: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            InstanceId ( String ): 否  需要查询节点信息的实例 ID 
    """,
    "create_instance": r""" 
   Args: 
       body: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Tags ( Array of TagDTO ): 否  绑定的标签列表 
            InstanceId ( String ): 否   
            ClientToken ( String ): 否  唯一标识符，用于保证请求幂等性。建议使用 UUID。 
            InstanceConfiguration ( Object of InstanceConfigurationAssign ): 是  实例配置详情 
            TransactionInstanceNo ( String ): 否   
           "字段"： TagDTO
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Key ( String ): 否   
            Value ( String ): 否   
           "字段"： InstanceConfigurationAssign
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            VPC ( Object of VpcInfo ): 是  实例的私有网络。 
            Period ( Integer ): 否  包年包月实例的购买时长，单位：月 
            Subnet ( Object of SubnetInfo ): 是  实例的子网。 
            UseTos ( Boolean ): 否  是否使用对象存储(TOS)。 
            ZoneId ( String ): 是  实例所在可用区。 
                  如果是多可用区部署，则填写多个 ZoneId，使用英文逗号分隔，如cn-beijing-a,cn-beijing-c。最左侧的 ZoneId 为主可用区，其余为备可用区。 
            Version ( String ): 是  实例版本。这也决定了实例类型。 
                  - ES (ElasticSearch) 类型实例可选版本：V6_8, V7_10, V8_18。推荐 V7_10。 
                  - OS (OpenSearch) 类型实例可选版本：OPEN_SEARCH_2_9。 
            IpFamily ( String ): 否  ipv4(仅有 ipv4 地址),dualstack(有 ipv4 和 ipv6 地址) 
            LogLevel ( String ): 否   
            RegionId ( String ): 是  实例所在区域 
            AutoRenew ( Boolean ): 否  包年包月实例是否配置自动续费。  
                  - true：自动续费，系统会在每次到期前自动为实例续费。  
                  - false：未开启自动续费，需要在实例到期前进行手动续费。 
            Byte2Cloud ( Object of Byte2Cloud ): 否  内场上云配置。请勿设置，该功能仅限内部使用。 
            ChargeType ( String ): 是  实例计费类型。建议优先选择按量计费。 
                  - PostPaid：按量计费。 
                  - PrePaid：包年包月。 
            InstanceId ( String ): 否  实例 ID。仅限内部使用，请勿设置。 
            SubnetList ( Array of SubnetInfo ): 否  设置实例的子网信息列表 
            EnableHttps ( Boolean ): 是  是否启用 HTTPS 访问协议。 
                  - true：启用 HTTPS 访问。 
                  - false：不启用 HTTPS，使用 HTTP 访问。（如果选择使用 HTTP 访问，将无需安全认证即可访问，并使用 HTTP 明文传输数据。您需要确保访问环境的安全性，且不要将访问接口暴露在公网环境上。） 
            ProjectName ( String ): 否  云搜索实例所属的项目，用于云资源的分组管理。  
                  - 项目是火山引擎提供的一种资源管理方式，有利于维护资源独立、数据安全；同时可从项目维度查看资源消费账单，便于计算云资源使用成本。 
            InstanceName ( String ): 是  自定义设置实例名称。  
                  - 只能包含中文、字母、数字、短横线（-）和下划线（_），开头和结尾不能是数字和短横线（-）。  
                  - 长度在 1～128 个字符内。 
            NetworkSpecs ( Array of NetworkSpec ): 否  实例公网规格配置 
            ResourceTags ( Array of TagInfo ): 否  支持为实例添加标签，可以更方便的识别和管理实例。实例最多支持添加 20 个标签。 
                  标签为键值对样式，设置时注意以下事项：  
                  - 只支持大小写字母、数字、中文和特殊字符.:/=+-_@，键值大小写敏感。  
                  - Key 不允许以volc:、Volc:、vOlc:、volc:......（16 种组合）开头。  
                  - Key 长度为 1128 字符；Value 长度为 0256 字符。 
            AdminPassword ( String ): 是  管理员密码。取值规则如下： 
                  - 密码至少包含大写字母、小写字母、数字和特殊字符中的三种，长度为 8～32 个字符。  
                  - 支持_#!@$%^&*()+=-特殊字符，不可以包含空格和中文。 
            EnableCerebro ( Boolean ): 否  是否开启 Cerebro。 
                  - true：开启 Cerebro。 
                  - false：不开启 Cerebro。 
            UserEniEnabled ( Boolean ): 否   
            EnablePureMaster ( Boolean ): 否  是否创建专用 Master 节点。生产环境、关键环境、较大规模集群建议开启。测试和演示环境建议关闭。 
                  - true：创建专用 Master 节点，Master 节点数量应该为 3 个。 
                  - false：不创建专用 Master 节点，Master 功能将内置在 Hot 节点。 
            NodeSpecsAssigns ( Array of NodeSpecsAssign ): 是  实例中各种节点的数量和规格配置。 
            ScaleCheckDetail ( Object of ScaleCheckDetailDTO ): 否   
            ConfigurationCode ( String ): 否  计费配置码，可以通过调用DescribeNodeAvailableSpecs接口获得。 
            DeletionProtection ( Boolean ): 否  是否开启实例删除保护功能，取值说明如下：  
                  - true：开启实例删除保护。（开启实例删除保护后，您将无法通过控制台或者 API 删除实例。） 
                  - false：关闭实例删除保护。 
           "字段"： VpcInfo
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            VpcId ( String ): 是  VPC ID 
            VpcName ( String ): 是  VPC 名称 
           "字段"： SubnetInfo
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            SubnetId ( String ): 是  Subnet ID 
            SubnetName ( String ): 是  Subnet 名称 
           "字段"： Byte2Cloud
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Idc ( String ): 否   
            Psm ( String ): 否   
            Consul ( String ): 否   
            Enabled ( Boolean ): 否   
            EsImageTag ( String ): 否   
            MasterNodes ( String ): 否   
            AttrNodeSetEnabled ( Boolean ): 否   
           "字段"： NetworkSpec
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Type ( String ): 否  公网应用类型Elasticsearch：es实例使用。Kibana：Dashboard使用 
            IsOpen ( Boolean ): 否  开启/关闭 
            SpecName ( String ): 否  网络资源规格名称 
            Bandwidth ( Integer ): 否  公网IP的带宽上限，默认为“1”，单位：Mbps。 
           "字段"： TagInfo
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Type ( String ): 是  标签类型。  
                  - CUSTOM：自定义标签。  
                  - SYSTEM：系统标签。 
            TagKvs ( JSON Map ): 否  更新的标签键值对 
            TagKeys ( Array of String ): 否  待删除标签键列表 
           "字段"： NodeSpecsAssign
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Type ( String ): 是  节点类型： 
                  - Master：专用主节点（负责元数据和集群管理）。  
                  - Hot：热数据节点。  
                  - Cold：冷数据节点。  
                  - Warm：温数据节点。  
                  - Kibana：数据可视化仪表板节点。  
                  - Coordinator：专用协调节点（负责数据的分发、汇总、归约）。 
            Number ( Integer ): 是  - 数据节点：数量范围 1~100（需含 ≥1 个 Hot 节点）。 
                  	- 生产建议：单可用区 ≥3；双可用区 ≥4；三可用区 ≥6。  
                  - Master 节点： 
                    - 若禁用 EnablePureMaster，则不要配置 Master 节点。 
                    - 若启用 EnablePureMaster，则数量 = 3。 
                  - Kibana 节点：固定为 1。 
                  - Coordinator 节点：可选，范围 2~50（生产建议 ≥2）。 
                  - Warm 节点：可选，上限 100（生产建议 ≥3）。 
            StorageSize ( Integer ): 是  存储容量，单位为 GiB，取值需为 10 的整数倍。 
                  - 默认值为 100 GiB，调整步长为 10 GiB。  
                  - Master 节点的 StorageSize 设置为 20 GiB，即"StorageSize": 20。  
                  - Kibana 节点的 StorageSize 设置为 0，即"StorageSize": 0。 
            StorageSpecName ( String ): 是  存储规格名称。 
                  - 可以调用 DescribeNodeAvailableSpecs 接口获取可用的存储规格列表。 
                  - Kibana 节点的 StorageSpecName 设置为空，即 "StorageSpecName": ""。 
            ExtraPerformance ( Object of ExtraPerformanceDTO ): 否  额外性能包 
            ResourceSpecName ( String ): 是  计算资源规格名称。 
                  - 可以调用 DescribeNodeAvailableSpecs 接口获取可用的节点规格列表。  
                  - 数据节点不能使用 x2.small (1c2g, 1 cpu core + 2g ram) 的实例。 
           "字段"： ScaleCheckDetailDTO
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            HealthCheck ( Boolean ): 否   
            ZoneScaleRet ( Object of ZoneScaleRet ): 否   
            CreateNetSpecs ( Array of NetworkSpec ): 否   
            ModifyNetSpecs ( Array of NetworkSpec ): 否   
            ReleaseNetSpecs ( Array of NetworkSpec ): 否   
            OnlyNetEipChange ( Boolean ): 否   
            NodeTypesForDiskScaleDown ( JSON Map ): 否   
            NodeTypesForDiskExtraUpdate ( JSON Map ): 否   
            NodeTypesForDiskTypeScaleUp ( JSON Map ): 否   
           "字段"： ExtraPerformanceDTO
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Throughput ( Integer ): 否  额外性能包吞吐量大小，单位为MB 
           "字段"： ZoneScaleRet
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            expectZoneIds ( Array of String ): 否   
            zoneScaleCode ( String ): 否   
            currentZoneIds ( Array of String ): 否   
           "字段"： NodeTypesForDiskScaleDown
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Type ( String ): 否  节点类型： 
                  - Master：专用主节点（负责元数据和集群管理）。  
                  - Hot：热数据节点。  
                  - Cold：冷数据节点。  
                  - Warm：温数据节点。  
                  - Kibana：数据可视化仪表板节点。  
                  - Coordinator：专用协调节点（负责数据的分发、汇总、归约）。 
            Number ( Integer ): 否  - 数据节点：数量范围 1~100（需含 ≥1 个 Hot 节点）。 
                  	- 生产建议：单可用区 ≥3；双可用区 ≥4；三可用区 ≥6。  
                  - Master 节点： 
                    - 若禁用 EnablePureMaster，则不要配置 Master 节点。 
                    - 若启用 EnablePureMaster，则数量 = 3。 
                  - Kibana 节点：固定为 1。 
                  - Coordinator 节点：可选，范围 2~50（生产建议 ≥2）。 
                  - Warm 节点：可选，上限 100（生产建议 ≥3）。 
            StorageSize ( Integer ): 否  存储容量，单位为 GiB，取值需为 10 的整数倍。 
                  - 默认值为 100 GiB，调整步长为 10 GiB。  
                  - Master 节点的 StorageSize 设置为 20 GiB，即"StorageSize": 20。  
                  - Kibana 节点的 StorageSize 设置为 0，即"StorageSize": 0。 
            StorageSpecName ( String ): 否  存储规格名称。 
                  - 可以调用 DescribeNodeAvailableSpecs 接口获取可用的存储规格列表。 
                  - Kibana 节点的 StorageSpecName 设置为空，即 "StorageSpecName": ""。 
            ExtraPerformance ( Object of ExtraPerformanceDTO ): 否  额外性能包 
            ResourceSpecName ( String ): 否  计算资源规格名称。 
                  - 可以调用 DescribeNodeAvailableSpecs 接口获取可用的节点规格列表。  
                  - 数据节点不能使用 x2.small (1c2g, 1 cpu core + 2g ram) 的实例。 
           "字段"： NodeTypesForDiskExtraUpdate
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Type ( String ): 否  节点类型： 
                  - Master：专用主节点（负责元数据和集群管理）。  
                  - Hot：热数据节点。  
                  - Cold：冷数据节点。  
                  - Warm：温数据节点。  
                  - Kibana：数据可视化仪表板节点。  
                  - Coordinator：专用协调节点（负责数据的分发、汇总、归约）。 
            Number ( Integer ): 否  - 数据节点：数量范围 1~100（需含 ≥1 个 Hot 节点）。 
                  	- 生产建议：单可用区 ≥3；双可用区 ≥4；三可用区 ≥6。  
                  - Master 节点： 
                    - 若禁用 EnablePureMaster，则不要配置 Master 节点。 
                    - 若启用 EnablePureMaster，则数量 = 3。 
                  - Kibana 节点：固定为 1。 
                  - Coordinator 节点：可选，范围 2~50（生产建议 ≥2）。 
                  - Warm 节点：可选，上限 100（生产建议 ≥3）。 
            StorageSize ( Integer ): 否  存储容量，单位为 GiB，取值需为 10 的整数倍。 
                  - 默认值为 100 GiB，调整步长为 10 GiB。  
                  - Master 节点的 StorageSize 设置为 20 GiB，即"StorageSize": 20。  
                  - Kibana 节点的 StorageSize 设置为 0，即"StorageSize": 0。 
            StorageSpecName ( String ): 否  存储规格名称。 
                  - 可以调用 DescribeNodeAvailableSpecs 接口获取可用的存储规格列表。 
                  - Kibana 节点的 StorageSpecName 设置为空，即 "StorageSpecName": ""。 
            ExtraPerformance ( Object of ExtraPerformanceDTO ): 否  额外性能包 
            ResourceSpecName ( String ): 否  计算资源规格名称。 
                  - 可以调用 DescribeNodeAvailableSpecs 接口获取可用的节点规格列表。  
                  - 数据节点不能使用 x2.small (1c2g, 1 cpu core + 2g ram) 的实例。 
           "字段"： NodeTypesForDiskTypeScaleUp
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Type ( String ): 否  节点类型： 
                  - Master：专用主节点（负责元数据和集群管理）。  
                  - Hot：热数据节点。  
                  - Cold：冷数据节点。  
                  - Warm：温数据节点。  
                  - Kibana：数据可视化仪表板节点。  
                  - Coordinator：专用协调节点（负责数据的分发、汇总、归约）。 
            Number ( Integer ): 否  - 数据节点：数量范围 1~100（需含 ≥1 个 Hot 节点）。 
                  	- 生产建议：单可用区 ≥3；双可用区 ≥4；三可用区 ≥6。  
                  - Master 节点： 
                    - 若禁用 EnablePureMaster，则不要配置 Master 节点。 
                    - 若启用 EnablePureMaster，则数量 = 3。 
                  - Kibana 节点：固定为 1。 
                  - Coordinator 节点：可选，范围 2~50（生产建议 ≥2）。 
                  - Warm 节点：可选，上限 100（生产建议 ≥3）。 
            StorageSize ( Integer ): 否  存储容量，单位为 GiB，取值需为 10 的整数倍。 
                  - 默认值为 100 GiB，调整步长为 10 GiB。  
                  - Master 节点的 StorageSize 设置为 20 GiB，即"StorageSize": 20。  
                  - Kibana 节点的 StorageSize 设置为 0，即"StorageSize": 0。 
            StorageSpecName ( String ): 否  存储规格名称。 
                  - 可以调用 DescribeNodeAvailableSpecs 接口获取可用的存储规格列表。 
                  - Kibana 节点的 StorageSpecName 设置为空，即 "StorageSpecName": ""。 
            ExtraPerformance ( Object of ExtraPerformanceDTO ): 否  额外性能包 
            ResourceSpecName ( String ): 否  计算资源规格名称。 
                  - 可以调用 DescribeNodeAvailableSpecs 接口获取可用的节点规格列表。  
                  - 数据节点不能使用 x2.small (1c2g, 1 cpu core + 2g ram) 的实例。 
    """,
}
