note = {
    "describe_accelerator": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 是  加速器ID。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 加速器ID。 
        AccountID ( String ): 用户ID。 
        Name ( String ): 加速器名称。 
        State ( String ): 标准型加速器的状态。取值： 
            - active：运行中。 
            - inactive：待配置。 
            - deploying：配置中。 
            - overdue：欠费中。 
            - expired：已过期。 
        CNAME ( String ): 标准加速器的 CNAME。 
        BillingType ( String ): 对于按量付费加速器（ChargeType 为POSTPAY）的具体计费标准： 
            - PayByTrafficDaily：按日流量后付费。 
            - PayByTrafficMonthly：按月流量后付费。 
            - PayByBandwidthMonthly：按月95峰值带宽后付费。 
            对于包年包月加速器（ChargeType 为PREPAY），该值始终为 ByBandwidthPrePay。 
        BillingSpec ( String ): 标准型加速器规格。取值： 
            - small：小型。 
            - middle：中型。 
            - large：大型。 
        Bandwidth ( Integer ): 加速器的实际带宽上限。单位：Mb。 
            - 如果是按量付费的加速器，或未绑定带宽包的包年包月加速器，则为与加速器规格匹配的带宽上限。 
            - 如果是绑定了带宽包的包年包月加速器，则为带宽包的带宽规格。 
        ConnectionNum ( Integer ): 与加速器规格匹配的最大并发连接数。 
        RegionNum ( Integer ): 与加速器规格匹配的最多可添加的加速区域数量。 
        ChargeType ( String ): 标准型加速器的计费类型。取值如下： 
            - PREPAY：包年包月。 
            - POSTPAY：按量付费。 
        RenewType ( Integer ): 标准型加速器的续费类型，取值： 
            - 0：该加速器的计费类型是后付费。 
            - 1：该加速器的计费类型是预付费，续费类型是手动续费。 
            - 2：该加速器的计费类型是预付费，续费类型是自动续费。 
        BandwidthPackageIds ( Array of String ): 绑定的公网带宽包的ID列表。 
        CrossDomainBandwidthIds ( Array of String ): 绑定的跨域带宽包ID列表。 
        RegionCount ( Integer ): 该加速器下的加速区域数量。 
        ListenerCount ( Integer ): 该加速器下的监听器数量。 
        CreateTime ( Integer ): 标准型加速器的创建时间，用 Unix 时间戳表示。 
        CreateTimeStr ( String ): 标准型加速器的创建时间，用字符串表示。 
        BeginTime ( Integer ): 加速器生效时间，用 Unix 时间戳表示。 
        ExpiredTime ( Integer ): 过期时间，用 Unix 时间戳表示。仅包年包月加速器（ChargeType 为 PREPAY）包含此字段。 
        BillingSpecEffectiveTime ( Integer ): 计费生效时间，用 Unix 时间戳表示。 
        ProjectName ( String ): 加速器所属项目。 
        ResourceTags ( Array of ResourceTags ): 指定的资源标签的集合，每个对象为一个名值对格式的标签。 
        IPSets ( Array of IPSets ): 加速区域列表。 
       "字段"： ResourceTags
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Key ( String ): 标签名称。 
        Value ( String ): 和标签名称对应的值。 
       "字段"： IPSets
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 标准型加速器 ID 。 
        IPSetId ( String ): 加速区域对应的 ID。 
            - CN_North：华北 
            - CN_East：华东 
            - CN_South：华南 
            - CN_NorthEast：东北 
            - CN_Central：华中 
            - CN_NorthWest：西北 
            - CN_SouthWest：西南 
            - AP1：亚太1 
        IPVersion ( String ): 加速区域支持的 IP 协议版本： 
            - IPv4：表示加速器支持客户端使用 IPv4 地址进行访问。 
            - IPv4/IPv6：表示加速器支持客户端使用 IPv4 和 IPv6 地址进行访问。 
        AccelerateRegion ( String ): 加速区域所在的区域中文名称。 
            - 东北 
            - 华北 
            - 华东 
            - 华南 
            - 华中 
            - 西北 
            - 西南 
            - 亚太1 
    """,
    "describe_basic_accelerator": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 是  基础型加速器ID。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 基础型加速器ID。 
        AccountID ( String ): 您的火山引擎账号ID。 
        AccountName ( String ): 您的火山引擎账号名称。 
        BandwidthPackageIds ( Array of String ): 绑定的公网带宽包的ID列表。 
        BandwidthPackageVolume ( Integer ): 带宽包的带宽规格。单位：Mb。 
        BeginTime ( Integer ): 计费生效时间，用 Unix 时间戳表示。 
        BillingType ( String ): 对于按量付费加速器（ChargeType 为POSTPAY）的具体计费标准： 
            - PayByTrafficDaily：按日流量后付费。 
            - PayByTrafficMonthly：按月流量后付费。 
            - PayByBandwidthMonthly：按月95峰值带宽后付费。 
            对于包年包月加速器（ChargeType 为PREPAY），该值始终为 ByBandwidthPrePay。 
        ChargeType ( String ): 基础型加速器的计费类型。取值： 
            - PREPAY：包年包月。 
            - POSTPAY：按量付费。 
        CreateTime ( Integer ): 加速器的创建时间，用 Unix 时间戳表示。 
        CreateTimeStr ( String ): 加速器的创建时间，用字符串表示。 
        CrossDomainBandwidthIds ( Array of String ): 绑定的跨域带宽包ID列表。 
        EndPointGroups ( Array of EndPointGroups ): 终端节点组列表。 
        ExpiredTime ( Integer ): 过期时间，用 Unix 时间戳表示。仅包年包月加速器（ChargeType 为 PREPAY）包含此字段。 
        IPSets ( Array of IPSets ): 加速区域列表。 
        Name ( String ): 加速器名称。 
        ProjectName ( String ): 加速器所属项目。 
        RenewType ( Integer ): 基础型加速器的续费类型，取值： 
            - 0：该加速器的计费类型是后付费。 
            - 1：该加速器的计费类型是预付费，续费类型是手动续费。 
            - 2：该加速器的计费类型是预付费，续费类型是自动续费。 
        ResourceTags ( Array of ResourceTags ): 指定的资源标签的集合，每个对象为一个名值对格式的标签。 
        State ( String ): 查询处于何种状态的基础型加速器。 
            - active：运行中。 
            - inactive：待配置。 
            - deploying：配置中。 
            - overdue：欠费中。 
            - expired：已过期。 
       "字段"： EndPointGroups
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        EndPointGroupId ( String ): 终端节点组ID。 
        Region ( String ): 终端节点组区域。 
            - CN_North：华北 
            - CN_East：华东 
            - CN_South：华南 
            - CN_NorthEast：东北 
            - CN_Central：华中 
            - CN_NorthWest：西北 
            - CN_SouthWest：西南 
            - AP1：亚太1 
       "字段"： IPSets
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        IPSetId ( String ): 加速区域ID。 
        Region ( String ): 加速区域所在的区域： 
            - CN_South：华南 
            - CN_North：华北 
            - CN_East：华东 
            - CN_NorthEast：东北 
            - CN_Central：华中 
            - CN_NorthWest：西北 
            - CN_SouthWest：西南 
            - AP1：亚太1 
       "字段"： ResourceTags
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Key ( String ): 标签名称。 
        Value ( String ): 与标签名称对应的值。 
    """,
    "describe_basic_endpoint_group": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 是  基础型加速器ID。 
             EndpointGroupId ( String ): 是  终端节点组ID。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 基础型加速器ID。 
        EndpointGroupId ( String ): 终端节点组ID。 
        Name ( String ): 终端节点组名称。 
        Region ( String ): 终端节点组所在区域。 
            - CN_North：华北 
            - CN_East：华东 
            - CN_South：华南 
            - CN_NorthEast：东北 
            - CN_Central：华中 
            - CN_NorthWest：西北 
            - CN_SouthWest：西南 
            - AP1：亚太1 
        State ( String ): 终端节点组的状态。取值： 
            - active：运行中 
            - deploying：配置中 
        EndpointType ( String ): 终端节点类型。同一终端节点组的终端节点类型相同。取值： 
            - public：公网类型 
            - private：私网类型 
        ExistBoundEndpoint ( Boolean ): 终端节点组是否包含已绑定到加速IP的终端节点。 
            - true：包含已绑定加速IP的终端节点。 
            - false：组内所有终端节点均未绑定加速IP。 
        Endpoints ( Array of Endpoints ): 终端节点列表。 
       "字段"： Endpoints
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        EndpointId ( String ): 终端节点ID。 
        Type ( String ): 终端节点的类型。 
            - 公网类型终端节点组（EndpointType为public）取值： 
            	- ECS：边缘计算节点。 
            	- ENI：弹性网卡实例。 
            	- IP：IPv4类型的自定义源站 IP 。 
            - 私网类型终端节点组（EndpointType为private）取值： 
            	- EDX_IP：EDX私网IP。 
        EndpointAddress ( String ): 与您选择的终端节点类型对应的终端节点地址。具体如下 
            - ECS：边缘计算实节点的ID。 
            - ENI：弹性网卡实例的ID。 
            - IP：自定义源站 IP 的公网 IPv4 地址。 
            - EDX_IP：EDX私网IP的地址。 
        EdgeNodeName ( String ): ECS或ENI所属的边缘节点名称，终端节点Type为ECS或ENI时存在。 
        PrivateInstanceID ( String ): 私有实例ID，终端节点组类型为私网时存在。 
    """,
    "describe_basic_ip_set": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 是  基础型加速器ID。 
             IPSetId ( String ): 是  加速区域ID。您可以调用 ListBasicIPSets 获取指定基础型加速器上的加速区域列表。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AccelerateIPs ( Array of String ): 加速IP的ID列表。 
        AcceleratorId ( String ): 基础型加速器ID。 
        ExistBoundIP ( Boolean ): 是否已绑定加速IP。 
        IPSetId ( String ): 加速区域ID。 
        IPVersion ( String ): 加速区域支持的 IP 协议版本： 
            - IPv4：表示加速器支持客户端使用 IPv4 地址进行访问。 
            - IPv4/IPv6：表示加速器支持客户端使用 IPv4 和 IPv6 地址进行访问。 
        Region ( String ): 加速区域所在的区域： 
            - CN_South：华南 
            - CN_North：华北 
            - CN_East：华东 
            - CN_NorthEast：东北 
            - CN_Central：华中 
            - CN_NorthWest：西北 
            - CN_SouthWest：西南 
            - AP1：亚太1 
        State ( String ): 加速区域的状态。 
            - active：运行中 
            - deploying：配置中 
    """,
    "describe_endpoint_group": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             EndpointGroupId ( String ): 是  终端节点组ID 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 加速器 ID。 
        Region ( String ): 终端节点组区域。 
            - CN_North：华北 
            - CN_East：华东 
            - CN_South：华南 
            - CN_NorthEast：东北 
            - CN_Central：华中 
            - CN_NorthWest：西北 
            - CN_SouthWest：西南 
            - AP1：亚太1 
        HealthCheckStatus ( String ): 该终端节点组的健康检查状态。 
            - detecting：探测中 
            - disable：未开启 
            - available：可用 
            - unavailable：不可用 
            - normal：正常 
            - abnormal：异常 
            - partiallyAbnormal：部分异常 
        HealthyConfig ( Object of HealthyConfig ): 健康检查的配置信息。 
        TrafficPercentage ( Integer ): 分配到该终端节点组的流量权重，即本终端节点组接入的流量在所有终端节点组接入流量的比例。 
            - 一个监听默认可以关联2个默认终端节点组，如果需要创建更多默认终端节点组，请联系客服经理。 
            - 每个终端节点组的流量调配取值范围：1~100。 
        ListenerId ( String ): 监听器 ID。 
        EndpointGroupId ( String ): 终端节点组ID。 
        Name ( String ): 终端节点组名称。 
        State ( String ): 终端节点组状态： 
            - active：运行中 
            - deleting： 删除中 
            - deploying：配置中 
        EndpointConfigurations ( Array of EndpointConfigurations ): 终端节点组包含的各终端节点的配置。 
        IsVolcSource ( Boolean ): 后端应用是否为托管在火山引擎的服务。 
        KeepClientIP ( Boolean ): 是否开启基于Proxy Protocol的保持客户端源IP功能。 
            - true：启用了保持客户端源IP功能。 
            - false：未启用此功能。 
        KeepClientIPMethod ( String ): Proxy Protocol 协议版本。取值： 
            - ProxyProtocolV1：仅支持TCP协议。通过在报文Payload开头添加Proxy Protocol v1报头（ASCII码格式）传递客户端源IP。 
            - ProxyProtocolV2：通过在报文Payload开头添加 Proxy Protocol v2报头（二进制格式）传递客户端源IP。 
        EndpointType ( String ): 终端节点类型，支持取值： 
            - public：公网 
            - private：私网 
        SourceIP ( Array of SourceIP ): 表示私网回源IP网段集合，仅在终端节点为私网类型时存在。 
        Role ( String ): 该终端节点组为主终端节点组还是备终端节点组： 
            - main：主终端节点组 
            - backup：备终端节点组 
       "字段"： HealthyConfig
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        HealthCheckEnable ( Boolean ): 是否开启健康检查： 
            - true：开启了健康检查功能。 
            - false：未开启健康检查功能。 
        HealthCheckProtocol ( String ): 健康检查协议，当前仅支持 TCP 协议。 
        HealthCheckPort ( Integer ): 健康检查端口。取值：1~65535。 
        HealthResponseTimeOut ( Integer ): 健康检查超时时间，即等待健康检查响应的时间上限。 
            - 如果后端服务器在指定时间内没有正确响应，则判定本次健康检查异常。 
            - 默认响应超时时间为2秒，可设置的超时时间范围为1～50秒。 
        HealthCheckInterval ( Integer ): 健康检查间隔时间。 
        HealthyThreshold ( Integer ): 健康阈值，即连续健康检查请求成功的次数，系统以此来判断终端节点是否健康。 
            - 健康阈值默认为3次，指连续3次健康检查请求成功，才能判定终端节点状态健康。 
            - 允许设置的健康阈值为2～10次。 
       "字段"： EndpointConfigurations
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Type ( String ): 终端节点组内的终端节点类型，取值： 
            - IP：自定义IP。 
            - Domain：自定义域名。 
            - EDX_IP：私网 IP。 
        Endpoint ( String ): 与终端节点类型相对应的终端节点的值。例如：Type 为 IP 时，终端节点的 Endpoint 值则是一个 IP 地址。 
        Weight ( Integer ): 终端节点的权重。 
            - 终端节点权重决定了终端节点组内每个终端节点接收的流量比例。 
            - 您可以为每个终端节点设置 1 到 100 之间的权重值。 
            - 系统会计算终端节点组内所有终端节点权重的总和。然后，根据其权重与总权重的比例，将流量转发到每个终端节点。 
            - 如果某个终端节点健康检查失败，流量将按比例分配到该终端节点组中其余健康的终端节点。 
        PrivateInstanceID ( String ): 私网终端节点所在的私有实例IP，仅在终端节点类型为私网时存在。 
       "字段"： SourceIP
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        IPRange ( String ): 私网回源IP网段。 
        IPRangeId ( String ): 私网回源IP网段ID。 
    """,
    "describe_ip_set": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 是  标准型加速器 ID 。 
             IPSetId ( String ): 是  加速区域对应的 ID。 
                   - CN_North：华北 
                   - CN_East：华东 
                   - CN_South：华南 
                   - CN_NorthEast：东北 
                   - CN_Central：华中 
                   - CN_NorthWest：西北 
                   - CN_SouthWest：西南 
                   - AP1：亚太1 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        IPSet ( Object of IPSet ): 加速区域详细信息。 
       "字段"： IPSet
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 标准型加速器 ID 。 
        IPSetId ( String ): 加速区域对应的 ID。 
            - CN_North：华北 
            - CN_East：华东 
            - CN_South：华南 
            - CN_NorthEast：东北 
            - CN_Central：华中 
            - CN_NorthWest：西北 
            - CN_SouthWest：西南 
            - AP1：亚太1 
        IPVersion ( String ): 加速区域支持的 IP 协议版本： 
            - IPv4：表示加速器支持客户端使用 IPv4 地址进行访问。 
            - IPv4/IPv6：表示加速器支持客户端使用 IPv4 和 IPv6 地址进行访问。 
        AccelerateRegion ( String ): 加速区域所在的区域中文名称。 
            - 东北 
            - 华北 
            - 华东 
            - 华南 
            - 华中 
            - 西北 
            - 西南 
            - 亚太1 
        State ( String ): 加速区域的状态。 
            - active：运行中 
            - deploying：配置中 
        IspType ( String ): 加速区域对应的公网类型： 
            - Standard：标准公网 
            - Advanced：精品公网 
    """,
    "describe_listener": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             ListenerId ( String ): 是  监听器 ID。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 加速器 ID。 
        AccountID ( String ): 当前用户账号 ID。 
        ListenerId ( String ): 监听器 ID。 
        Name ( String ): 监听器名称。 
        CreateTime ( Integer ): 监听器创建时间，以 UNIX 时间戳格式表示。 
        State ( String ): 监听器状态。取值： 
            - active：运行中 
            - deleting：删除中 
            - deploying：配置中 
        Protocol ( String ): 监听协议。取值： 
            - TCP 
            - UDP 
        PortRanges ( Array of PortRanges ): 监听器端口范围集合。每个端口范围由一个起始端口和一个结束端口定义。 
        EndpointGroupIds ( Array of String ): 主终端节点组 ID 的列表。 
        BackupEndpointGroupIds ( Array of String ): 备终端节点组 ID 的列表。 
        EnableAffinity ( Boolean ): 是否启用客户端亲和性。取值： 
            - true：启用 
            - false：不启用 
        DisableIsolateTCPNullConn ( Boolean ): 是否禁用隔离 TCP 空连接。取值： 
            - true：禁用“隔离 TCP 空连接” 
            - false：启用“隔离 TCP 空连接” 
        DisablePreConnect ( Boolean ): 是否禁用预连接。取值： 
            - true：禁用预连接 
            - false：启用预连接 
        FixedSourceReturn ( Object of FixedSourceReturn ): 固定转发 IP 相关配置。 
        IPAccess ( Object of IPAccess ): 基于源 IP 地址的访问控制相关配置。 
       "字段"： PortRanges
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        FromPort ( Integer ): 起始端口。 
        ToPort ( Integer ): 结束端口。如果指定单个端口，则起始端口和结束端口相同。 
       "字段"： FixedSourceReturn
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否启用固定转发 IP。 取值： 
            - true：启用。 
            - false：不启用。 
        GroupID ( Integer ): 固定转发集群 ID。 
        Cidrs ( Array of String ): 固定转发 IP 开启后，出口 IP 网段的列表。 
       "字段"： IPAccess
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否启用基于源 IP 地址的访问控制。默认不启用。取值： 
            - true：启用。 
            - false：不启用。 
        FilterType ( String ): 表明访问控制是基于黑名单还是白名单。当 Enable 字段为 true 时，此选项必填。取值： 
            - WhiteList：白名单列表，仅允许列表中的 IP 地址访问监听器。 
            - BlackList：黑名单列表，仅阻止列表中的 IP 地址访问监听器。 
        FilterList ( Array of String ): 白名单或黑名单中的 IP 地址集合。单个值为一个 IP 地址和网段，最多输入 100 个值。当 Enable 字段为 true 时，此选项必填。 
    """,
    "describe_listener_logs": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             StartTime ( String ): 是  查询起始时间 
             EndTime ( String ): 是  查询结束时间 
             ListenerId ( String ): 是  监听器ID 
             PageNum ( Integer ): 否  页码 
             PageSize ( Integer ): 否  页大小 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        FilesCount ( Integer ): 日志总数 
        FileLists ( Array of FileLists ): 日志详情列表 
        PageNum ( Integer ): 页码 
        PageSize ( Integer ): 页大小 
       "字段"： FileLists
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        ListenerId ( String ): 监听器ID 
        StartTime ( String ): 日志起始时间 
        EndTime ( String ): 日志结束时间 
        FileName ( String ): 日志文件名称 
        FilePath ( String ): 日志文件地址 
        FileSize ( Float ): 日志包大小 
    """,
    "describe_statistics": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             InputIdType ( String ): 是  查询数据类型，支持参数： 
                   - AcceleratorId：加速器ID，表示查询加速器维度的监控数据。 
                   - ListenerId：监听ID，表示查询监听维度的监控数据。 
                   基础型加速器只具备加速器维度的数据监控。 
             InputId ( Array of String ): 是  根据您InputIdType参数的值（AcceleratorId或ListenerId），指定查询的加速器ID或监听器ID列表。当指定加速器时，不能同时包含标准型加速器和基础型加速器。 
             Interval ( Integer ): 是  查询数据的时间粒度，单位：秒，支持参数： 
                   - 60：表示按照1分钟的时间粒度进行查询。1分钟粒度最多允许查看15天时间段的监控数据。 
                   - 300：表示按照5分钟的时间粒度进行查询。5分钟粒度最多允许查看31天时间段的监控数据。 
             StartTime ( String ): 是  查询时间段的起始时间。 
                   - 您可以查看最近 90 天的指标数据。 
                   - 时间跨度最长为 31 天。 
             EndTime ( String ): 是  查询时间段的结束时间。结束时间不得早于起始时间。 
             Metrics ( Array of String ): 否  查询指标列表。不指定时返回全部指标。 
             RegionType ( String ): 否  您可以选择加速区域或终端节点组来查看监控的数据指标的信息。 
                   - AccelerateRegion：表示选择加速区域维度来查看监控的数据指标。 
                   - EndPointGroupRegion：表示选择终端节点组来维度查看监控的数据指标。 
             Region ( Array of String ): 否  查询的区域列表。不填时，默认查询全部可查询的区域。 
                   - CN_North：华北 
                   - CN_East：华东 
                   - CN_South：华南 
                   - CN_NorthEast：东北 
                   - CN_Central：华中 
                   - CN_NorthWest：西北 
                   - CN_SouthWest：西南 
                   - AP1：亚太1 
                   对于非白名单用户： 
                   - 标准型加速器的可查询的加速区域为：CN_North、CN_East、CN_South、AP1。 
                   - 基础型加速器的可查询的加速区域为：CN_South、AP1。 
             GroupByListener ( Boolean ): 否  是否按监听器对数据进行聚合。 
                   - true：按监听器对数据进行聚合。 
                   - false（默认值）：所有监听器的数据聚合汇总在一起。 
                   当GroupByListener为true时，InputIdType必须为ListenerId。 
             GroupByRegion ( Boolean ): 否  是否按区域对数据进行聚合。 
                   - true：按区域对数据进行聚合。 
                   - false（默认值）：所有区域的数据聚合汇总在一起。 
                   当GroupByRegion为true时，必须在Region参数中指定需要返回的区域。 
             GroupByAccelerator ( Boolean ): 否  是否按加速器对数据进行聚合。取值： 
                   - true：按指定的加速器ID聚合数据。 
                   - false（默认值）：所有加速器的数据聚合汇总在一起。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Results ( Array of Results ): 时间序列组织的查询结果明细。 
        TotalStatisticResults ( Array of TotalStatisticResults ): 在您的筛选条件下，汇总数据信息列表。 
       "字段"： Results
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        TimeStamp ( String ): 单个时间段的开始时间（基于您指定的时间颗粒度），以字符串格式表示。 
        TimeStampInt ( Integer ): 单个时间段的开始时间（基于您指定的时间颗粒度），以UNIX时间戳格式表示。 
        StatisticsResults ( Array of StatisticsResults ): 当前时间段的统计数据。 
       "字段"： TotalStatisticResults
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        TotalTraffic ( Float ): 总流量，单位：byte。 
        MaxBandwidth ( Float ): 峰值带宽，单位：bps。 
        MaxBandwidth95 ( Float ): 95峰值带宽，单位：bps。 
        MaxConnectionNum ( Float ): 峰值并发连接数。 
       "字段"： StatisticsResults
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 加速器ID。仅当请求中InputIdType为AcceleratorId且GroupByAccelerator为true时才会返回此参数。 
        ListenerId ( String ): 监听器ID。仅当请求中InputIdType为ListenerId且GroupByListener为true时才会返回此参数。 
        Region ( String ): 区域ID。仅当请求中GroupByRegion为true时才会返回此参数。 
        DetailInfo ( Array of DetailInfo ): 监控数据指标的详细信息列表。 
       "字段"： DetailInfo
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Name ( String ): 监控数据指标。根据您的筛选条件展示下列指标信息。 
            - InboundBandwidth：入方向带宽（单位：bps） 
            - OutboundBandwidth：出方向带宽（单位：bps） 
            - ConnectionNum：并发连接数 
            - OutboundTraffic：出方向流量（单位：byte） 
            - InboundTraffic：入方向流量（单位：byte） 
            - InboundTrafficAccumulation：入方向累计流量（单位：byte） 
            - OutboundTrafficAccumulation：出方向累计流量（单位：byte） 
            “出方向”为从终端节点区域到加速区域的方向。“入方向”为加速区域到终端节点区域的方向。 
        Value ( Float ): 对应该指标的数据值。 
    """,
    "describe_top_statistics": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             InputIdType ( String ): 是  查询ID类型，支持参数：AcceleratorId,ListenerId 
             StartTime ( String ): 是  查询起始时间 
             EndTime ( String ): 是  查询结束时间 
             InputId ( Array of String ): 是  查询ID列表 
             SortMetric ( String ): 否  排序指标 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        SortMetric ( String ): 排序指标 
        TopStatistics ( Array of TopStatistics ): TOP数据列表 
       "字段"： TopStatistics
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        ID ( String ): 资源ID 
        MaxBandwidth ( Float ): 最大带宽 
        MaxBandwidth95 ( Float ): 最大95带宽 
        MaxConnectionNum ( Float ): 最大连接数 
        Name ( String ): 资源名称 
        Rank ( Integer ): 排名 
        TotalTraffic ( Float ): 总流量 
    """,
    "get_accelerator_dimension": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorType ( String ): 是  加速器类型 
             Filters ( Array of Filters ): 是  过滤条件 
             TargetName ( String ): 是  查询维度 
            "字段"： Filters
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Name ( String ): 否  条件名 
             Values ( Array of String ): 否  条件值 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Values ( Array of Values ): 维度值列表 
       "字段"： Values
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        DescriptionCN ( String ): 纬度名 
        DescriptionEN ( String ): 纬度名英文 
        Value ( String ): 纬度值 
    """,
    "get_bandwidth_package": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             BandwidthPackageId ( String ): 是  带宽包ID 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        BandwidthPackageInfo ( Object of BandwidthPackageInfo ): 带宽包信息 
       "字段"： BandwidthPackageInfo
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 加速器ID 
        AccountID ( String ): 账户ID 
        ActivatedTime ( Integer ): 生效时间 
        Bandwidth ( Integer ): 带宽 
        BillingType ( String ): 计费类型 
        ChargeType ( String ): 计费方式 PREPAY:预付费 POSTPAY:后付费 
        CreateTime ( Integer ): 创建时间 
        CrossDomainBandwidthLines ( Array of CrossDomainBandwidthLines ): 线路列表 
        Desc ( String ): 描述 
        EndpointA ( String ): 终端节点A 
        EndpointB ( String ): 终端节点B 
        ExpiredTime ( Integer ): 过期时间 
        Id ( String ): 带宽包ID 
        IsAllowShared ( Boolean ): 是否允许共享 
        Isp ( String ): 运营商 
        RenewType ( Integer ): 是否自动续费 
        SharedQuotaRemain ( Integer ): 共享带宽剩余配额 
        State ( String ): 带宽包状态 
        ProjectName ( String ): 项目名 
        ResourceTags ( Array of ResourceTags ): 标签列表 
       "字段"： CrossDomainBandwidthLines
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Bandwidth ( Integer ): 带宽 
        EndpointA ( String ): 终端节点A 
        EndpointB ( String ): 终端节点B 
        Id ( String ): 线路ID 
        Name ( String ): 线路名 
       "字段"： ResourceTags
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Key ( String ): 标签名称，支持大/小写字母、数字和中文组成，支持"+-=@/._"等特殊字符，长度不超过 128 个字符，不允许以volc开头。 
        Value ( String ): 标签名称对应的值，由大/小写字母、数字和中文组成，支持"+-=@/._"等特殊字符，长度不超过 256个字符。 
    """,
    "get_basic_endpoint_related_acc_instance_infos": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Domains ( Array of String ): 否  域名列表 
             IPs ( Array of String ): 否  IP列表 
             ECSIDs ( Array of String ): 否  ECSID列表 
             ENIIDs ( Array of String ): 否  ENIID列表 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Infos ( Array of Infos ): 终端节点相关加速器实例信息列表 
       "字段"： Infos
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        EndpointInfo ( String ): 终端节点信息 
        AccInstanceInfos ( Array of AccInstanceInfos ): 加速器实例信息列表 
       "字段"： AccInstanceInfos
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        ID ( String ): 加速器ID 
        Name ( String ): 加速器名称 
    """,
    "get_endpoint_related_acc_instance_infos": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Domains ( Array of String ): 否  域名列表 
             IPs ( Array of String ): 否  IP列表 
             ECSIDs ( Array of String ): 否  ECSID列表 
             ENIIDs ( Array of String ): 否  ENIID列表 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Infos ( Array of Infos ): 终端节点相关加速实例信息 
       "字段"： Infos
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        EndpointInfo ( String ): 终端节点信息 
        AccInstanceInfos ( Array of AccInstanceInfos ): 加速实例信息列表 
       "字段"： AccInstanceInfos
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        ID ( String ): 加速实例ID 
        Name ( String ): 加速实例名称 
    """,
    "list_accelerate_areas": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorType ( String ): 否  加速器类型 
             ResourceType ( String ): 否  资源类型 
             AcceleratorId ( String ): 否  加速器ID 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Areas ( Array of Areas ): 区域信息列表 
        TopAreas ( Array of TopAreas ): 第一级区域信息列表 
       "字段"： Areas
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AreaID ( String ): 区域ID 
        AreaName ( String ): 区域名称 
        Area ( String ): 上级区域名称 
        Nodes ( Array of Nodes ): 区域节点列表 
        AreaIspType ( Array of AreaIspType ):  
       "字段"： TopAreas
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AreaID ( String ): 区域ID 
        AreaName ( String ): 区域名称 
        Area ( String ): 上级区域名称 
        Nodes ( Array of Nodes ): 区域节点列表 
        AreaIspType ( Array of AreaIspType ):  
       "字段"： Nodes
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Name ( String ): 节点名称 
        Alias ( String ): 节点别名 
        ISP ( String ): 节点运营商 
        AllowCreate ( Boolean ):  
        BindEndpointType ( Array of String ):  
        Reason ( String ):  
        SupportModeList ( Array of String ):  
       "字段"： AreaIspType
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        IspType ( String ):  
        IspTypeNameCN ( String ):  
        IspTypeNameEN ( String ):  
    """,
    "list_accelerators": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 否  标准型加速器 ID 。用来查询单个加速器。 
             State ( String ): 否  标准型加速器的状态。取值： 
                   - active：运行中。 
                   - inactive：待配置。 
                   - deploying：配置中。 
                   - overdue：欠费中。 
                   - expired：已过期。 
             ChargeType ( String ): 否  标准型加速器的计费类型。取值如下： 
                   - PREPAY：包年包月。 
                   - POSTPAY：按量付费。 
             BillingSpec ( String ): 否  标准型加速器规格。不同类型加速器的具体规格，参见计费概述。具体取值如下： 
                   - small：小型。 
                   - middle：中型。 
                   - large：大型。 
             Name ( String ): 否  加速器名称。可以指定名称包含的关键字进行部分匹配查询。 
             WithBandwidthPackage ( Boolean ): 否  是否绑定了公网带宽包。 
             ProjectName ( String ): 否  资源所属项目名。 
             ResourceTagFilter ( Object of ResourceTagFilter ): 否  指定关联的资源标签。可以调用 ListResourceTags 查看资源标签列表。 
             PageSize ( Integer ): 否  分页中显示的最大条目数。 
             PageNum ( Integer ): 否  返回分页的页码。 
            "字段"： ResourceTagFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             FilterType ( String ): 否  当您指定了多个资源标签时，该参数指定标签组合的逻辑： 
                   - and：同时具有所有指定标签 
                   - or：具有任一指定标签 
             ResourceTags ( Array of ResourceTags ): 否  指定的资源标签的集合，每个对象为一个名值对格式的标签。 
            "字段"： ResourceTags
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Key ( String ): 是  标签名称。 
             Value ( String ): 是  标签名称对应的值。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Accelerators ( Array of Accelerators ): 加速器列表。 
        PageNum ( Integer ): 返回分页的页码。 
        PageSize ( Integer ): 分页中显示的最大条目数。 
        TotalCount ( Integer ): 查询到的总条目数。 
       "字段"： Accelerators
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 加速器ID。 
        AccountID ( String ): 账号ID。 
        Name ( String ): 加速器名称。 
        State ( String ): 标准型加速器的状态。取值： 
            - active：运行中。 
            - inactive：待配置。 
            - deploying：配置中。 
            - overdue：欠费中。 
            - expired：已过期。 
        CNAME ( String ): 标准加速器的 CNAME。 
        ChargeType ( String ): 标准型加速器的计费类型。取值： 
            - PREPAY：包年包月（预付费）。 
            - POSTPAY：按量付费（后付费）。 
        BillingType ( String ): 对于按量付费加速器（ChargeType 为POSTPAY）的具体计费标准： 
            - PayByTrafficDaily：按日流量后付费。 
            - PayByTrafficMonthly：按月流量后付费。 
            - PayByBandwidthMonthly：按月95峰值带宽后付费。 
            对于包年包月加速器（ChargeType 为PREPAY），该值始终为 ByBandwidthPrePay。 
        BillingSpec ( String ): 标准型加速器规格。取值： 
            - small：小型。 
            - middle：中型。 
            - large：大型。 
        Bandwidth ( Integer ): 加速器的实际带宽上限。单位：Mb。 
            - 如果是按量付费的加速器，或未绑定带宽包的包年包月加速器，则为与加速器规格匹配的带宽上限。 
            - 如果是绑定了带宽包的包年包月加速器，则为带宽包的带宽规格。 
        ConnectionNum ( Integer ): 与加速器规格匹配的最大并发连接数。 
        RegionNum ( Integer ): 与加速器规格匹配的最多可添加的加速区域数量。 
        BandwidthPackageIds ( Array of String ): 绑定的公网带宽包的ID列表。 
        CrossDomainBandwidthIds ( Array of String ): 绑定的跨域带宽包ID列表。 
        RenewType ( Integer ): 标准型加速器的续费类型，取值： 
            - 0：该加速器的计费类型是后付费。 
            - 1：该加速器的计费类型是预付费，续费类型是手动续费。 
            - 2：该加速器的计费类型是预付费，续费类型是自动续费。 
        RegionCount ( Integer ): 该加速器下的加速区域数量。 
        ListenerCount ( Integer ): 该加速器下的监听器数量。 
        CreateTime ( Integer ): 标准型加速器的创建时间，用 Unix 时间戳表示。 
        CreateTimeStr ( String ): 标准型加速器的创建时间，用字符串表示。 
        ExpiredTime ( Integer ): 过期时间，用 Unix 时间戳表示。仅包年包月加速器（ChargeType 为 PREPAY）包含此字段。 
        BillingSpecEffectiveTime ( Integer ): 计费生效时间，用 Unix 时间戳表示。 
        ProjectName ( String ): 加速器所属项目。 
        ResourceTags ( Array of ResourceTags ): 加速器上添加的标签列表。 
        WANBandwidthPackages ( Array of WANBandwidthPackages ): 公网带宽包详情列表。 
        IPSets ( Array of IPSets ): IPSet列表 
       "字段"： ResourceTags
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Key ( String ): 标签名称。 
        Value ( String ): 与标签名称对应的值。 
       "字段"： WANBandwidthPackages
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorIDs ( Array of String ): 加速器ID。 
        AccountID ( String ): 用户ID。 
        Bandwidth ( Integer ): 公网带宽包的带宽规格，单位 Mb。 
        BeginTime ( Integer ): 公网带宽包开始时间，用 Unix 时间戳表示。 
        BillingType ( String ): 固定返回 ByBandwidthPrePay。 
        ChargeType ( String ): 固定返回 PREPAY。 
        CreateTime ( Integer ): 公网带宽包创建时间，用 Unix 时间戳表示。 
        ExpiredTime ( Integer ): 公网带宽包到期时间，用 Unix 时间戳表示。 
        ID ( String ): 公网带宽包 ID。 
        RenewType ( Integer ): 跨域带宽包续费方式，取值： 
            - 0：表示该跨域带宽包为后付费，不涉及自动续费。 
            - 1：手动续费。 
            - 2：自动续费，自动续费时长为1个月。 
        State ( String ): 公网带宽包状态，支持取值： 
            - bound：已绑定 
            - expired：已过期 
            - unbound：未绑定 
            - deploy：配置中 
        BandwidthType ( String ): 公网带宽类型。取值： 
            - Standard：标准公网带宽包 
            - Premium：精品公网带宽包 
        ProjectName ( String ): 公网带宽包关联的项目名。 
        ResourceTags ( Array of ResourceTags ): 公网带宽包关联的标签列表 
       "字段"： IPSets
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 加速器ID 
        IPSetId ( String ): IPSetID 
        IPVersion ( String ): IP版本 
        AccelerateRegion ( String ): 加速区域 
        State ( String ): 状态 
        IPAddressList ( Object of IPAddressList ): IP列表 
        IspType ( String ):  
       "字段"： IPAddressList
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        IPV4s ( Array of IPV4s ): IPv4列表 
        IPV6s ( Array of IPV6s ): IPv6列表 
       "字段"： IPV4s
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        ISP ( String ):  
        ISPName ( String ):  
        Addr ( String ):  
       "字段"： IPV6s
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        ISP ( String ):  
        ISPName ( String ):  
        Addr ( String ):  
    """,
    "list_bandwidth_packages": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 否  加速器ID 
             AccountId ( String ): 否  账号ID 
             AgentId ( String ): 否   
             BandwidthPackageId ( String ): 否  带宽包ID 
             BandwidthType ( String ): 是  带宽类型 
             Domain ( String ): 否  域名 
             Isp ( String ): 否  运营商 
             OrderType ( String ): 否  排序类型 
             PageNumber ( Integer ): 是  页码 
             PageSize ( Integer ): 是  页大小 
             State ( String ): 否  状态 
             States ( Array of String ): 否  状态列表 
             ProjectName ( String ): 否  项目名 
             ResourceTagFilter ( Object of ResourceTagFilter ): 否  标签过滤器 
            "字段"： ResourceTagFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             FilterType ( String ): 否   
             ResourceTags ( Array of ResourceTags ): 否   
            "字段"： ResourceTags
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Key ( String ): 是  标签名称，支持大/小写字母、数字和中文组成，支持"+-=@/._"等特殊字符，长度不超过 128 个字符，不允许以volc开头。 
             Value ( String ): 是  标签名称对应的值，由大/小写字母、数字和中文组成，支持"+-=@/._"等特殊字符，长度不超过 256个字符。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        CrossDomainBandwidthPackages ( Array of CrossDomainBandwidthPackages ): 跨境带宽包列表 
        PageNumber ( Integer ): 页码 
        PageSize ( Integer ): 页大小 
        TotalCount ( Integer ): 总数 
        WANBandwidthPackages ( Array of WANBandwidthPackages ): 公网带宽包列表 
       "字段"： CrossDomainBandwidthPackages
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 加速器ID 
        AccountID ( String ): 账户ID 
        ActivatedTime ( Integer ): 生效时间 
        Bandwidth ( Integer ): 带宽 
        BillingType ( String ): 计费类型 
        ChargeType ( String ): 计费方式 PREPAY:预付费 POSTPAY:后付费 
        CreateTime ( Integer ): 创建时间 
        CrossDomainBandwidthLines ( Array of CrossDomainBandwidthLines ): 线路列表 
        Desc ( String ): 描述 
        EndpointA ( String ): 终端节点A 
        EndpointB ( String ): 终端节点B 
        ExpiredTime ( Integer ): 过期时间 
        Id ( String ): 带宽包ID 
        IsAllowShared ( Boolean ): 是否允许共享 
        Isp ( String ): 运营商 
        RenewType ( Integer ): 是否自动续费 
        SharedQuotaRemain ( Integer ): 共享带宽剩余配额 
        State ( String ): 带宽包状态 
        ProjectName ( String ): 项目名 
        ResourceTags ( Array of ResourceTags ): 标签列表 
       "字段"： WANBandwidthPackages
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorIDs ( Array of String ):  
        AccountID ( String ):  
        Bandwidth ( Integer ):  
        BeginTime ( Integer ):  
        BillingType ( String ):  
        ChargeType ( String ):  
        CreateTime ( Integer ):  
        ExpiredTime ( Integer ):  
        ID ( String ):  
        RenewType ( Integer ):  
        State ( String ):  
        BandwidthType ( String ):  
        ProjectName ( String ): 项目名 
        ResourceTags ( Array of ResourceTags ): 标签列表 
       "字段"： CrossDomainBandwidthLines
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Bandwidth ( Integer ): 带宽 
        EndpointA ( String ): 终端节点A 
        EndpointB ( String ): 终端节点B 
        Id ( String ): 线路ID 
        Name ( String ): 线路名 
       "字段"： ResourceTags
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Key ( String ): 标签名称，支持大/小写字母、数字和中文组成，支持"+-=@/._"等特殊字符，长度不超过 128 个字符，不允许以volc开头。 
        Value ( String ): 标签名称对应的值，由大/小写字母、数字和中文组成，支持"+-=@/._"等特殊字符，长度不超过 256个字符。 
    """,
    "list_basic_accelerate_i_ps": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 是  基础型加速器ID。 
             IPSetId ( String ): 是  加速区域ID。 
             PageSize ( Integer ): 是  分页中显示的最大条目数。 
             PageNum ( Integer ): 是  返回分页的页码。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AccelerateIPs ( Array of AccelerateIPs ): 加速IP列表。 
        TotalCount ( Integer ): 查询到的总条目数。 
        PageSize ( Integer ): 分页中显示的最大条目数。 
        PageNum ( Integer ): 返回分页的页码。 
       "字段"： AccelerateIPs
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AccelerateIPAddress ( String ): 加速IP的地址。 
        AccelerateIPId ( String ): 加速IP的ID。 
        AcceleratorId ( String ): 基础型加速器ID。 
        BindingMode ( String ): 绑定模式，即加速IP与终端节点的绑定模式。取值： 
            - Standard：标准模式，您的终端节点为边缘计算节点或ENI时，可以选择该模式。该模式下，一个加速IP可以关联一个终端节点。 
            - All-Port：全端口模式，您的终端节点为自定义 IP 时，请选择该模式。该模式下，一个加速IP可以关联一个终端节点。 
            - Shared：共享模式，您的终端节点为边缘计算节点或ENI时，可以选择该模式。该模式下，一个加速IP可以关联多个终端节点。一个终端节点也可以关联多个加速IP。 
        EdgeNodeAlias ( String ): 终端节点所属边缘计算节点中文名称。 
        EdgeNodeName ( String ): ECS或ENI所属的边缘节点名称，终端节点Type为ECS或ENI时存在。 
        Endpoints ( Array of Endpoints ): 加速IP所绑定的终端节点组列表。 
        IPSetId ( String ): 加速区域ID。 
        ISP ( String ): 提供加速IP的运营商。具体支持的取值如下： 
            - ChinaUnicom：中国联通。 
            - ChinaMobile：中国移动。 
            - ChinaTelecom：中国电信。 
            - BGP：BGP专线。 
        State ( String ): 加速区域的状态。 
            - active：运行中 
            - deploying：配置中 
       "字段"： Endpoints
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        EndpointId ( String ): 终端节点ID。 
        Type ( String ): 终端节点的类型。 
            - 公网类型终端节点组（EndpointType为public）取值： 
            	- ECS：边缘计算节点。 
            	- ENI：弹性网卡实例。 
            	- IP：IPv4类型的自定义源站 IP 。 
            - 私网类型终端节点组（EndpointType为private）取值： 
            	- EDX_IP：EDX私网IP。 
        EndpointAddress ( String ): 与您选择的终端节点类型对应的终端节点地址。具体如下 
            - ECS：边缘计算实节点的ID。 
            - ENI：弹性网卡实例的ID。 
            - IP：自定义源站 IP 的公网 IPv4 地址。 
            - EDX_IP：EDX私网IP的地址。 
        InternalIPs ( Array of String ): 终端节点私网IP列表，当绑定模式为标准模式时存在。 
        PrivateInstanceID ( String ): 私有实例ID，终端节点组类型为私网时存在。 
    """,
    "list_basic_accelerators": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 否  基础型加速器ID。 
             State ( String ): 否  查询处于何种状态的基础型加速器。 
                   - active：运行中。 
                   - inactive：待配置。 
                   - deploying：配置中。 
                   - overdue：欠费中。 
                   - expired：已过期。 
             Name ( String ): 否  基础型加速器的名称。 
             WithBandwidthPackage ( Boolean ): 否  是否绑定了带宽包。 
             ChargeType ( String ): 否  基础型加速器的计费类型。取值： 
                   - PREPAY：包年包月。 
                   - POSTPAY：按量付费。 
             PageSize ( Integer ): 否  分页中显示的最大条目数。 
             PageNum ( Integer ): 否  返回分页的页码。 
             IPSetRegion ( String ): 否  加速区域 
                   - CN_South：华南 
                   - AP1：亚太1 
                   仅对申请该功能的客户开放： 
                   - CN_North：华北 
                   - CN_East：华东 
                   - CN_NorthEast：东北 
                   - CN_Central：华中 
                   - CN_NorthWest：西北 
                   - CN_SouthWest：西南 
             EndPointGroupRegion ( String ): 否  终端节点组区域。取值： 
                   - CN_North：华北 
                   - CN_East：华东 
                   - CN_South：华南 
                   - CN_NorthEast：东北 
                   - CN_Central：华中 
                   - CN_NorthWest：西北 
                   - CN_SouthWest：西南 
                   - AP1：亚太1 
             ProjectName ( String ): 否  加速器所属项目。 
             ResourceTagFilter ( Object of ResourceTagFilter ): 否  指定关联的资源标签。可以调用 ListResourceTags 查看资源标签列表。 
            "字段"： ResourceTagFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             FilterType ( String ): 否  当您指定了多个资源标签时，该参数指定标签组合的逻辑： 
                   - and：同时具有所有指定标签 
                   - or：具有任一指定标签 
             ResourceTags ( Array of ResourceTags ): 否  指定的资源标签的集合，每个对象为一个名值对格式的标签。 
            "字段"： ResourceTags
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Key ( String ): 是  标签名称。 
             Value ( String ): 是  和标签名称对应的值。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Accelerators ( Array of Accelerators ): 基础型加速器列表。 
        TotalCount ( Integer ): 查询到的总条目数。 
        PageSize ( Integer ): 分页中显示的最大条目数。 
        PageNum ( Integer ): 返回分页的页码。 
       "字段"： Accelerators
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 基础型加速器ID。 
        AccountID ( String ): 您的火山引擎账号ID。 
        AccountName ( String ): 您的火山引擎账号名称。 
        Name ( String ): 加速器名称。 
        State ( String ): 基础型加速器的状态，取值： 
            - active：运行中； 
            - inactive：待配置； 
            - deploying：配置中； 
            - overdue：欠费中； 
            - expired：已过期。 
        BillingType ( String ): 对于按量付费加速器（ChargeType 为POSTPAY）的具体计费标准： 
            - PayByTrafficDaily：按日流量后付费。 
            - PayByTrafficMonthly：按月流量后付费。 
            - PayByBandwidthMonthly：按月95峰值带宽后付费。 
            对于包年包月加速器（ChargeType 为PREPAY），该值始终为 ByBandwidthPrePay。 
        RenewType ( Integer ): 基础型加速器的续费类型，取值： 
            - 0：该加速器的计费类型是后付费。 
            - 1：该加速器的计费类型是预付费，续费类型是手动续费。 
            - 2：该加速器的计费类型是预付费，续费类型是自动续费。 
        ChargeType ( String ): 基础型加速器的计费类型。取值： 
            - PREPAY：包年包月。 
            - POSTPAY：按量付费。 
        CrossDomainBandwidthIds ( Array of String ): 绑定的跨域带宽包ID列表。 
        BandwidthPackageIds ( Array of String ): 绑定的公网带宽包的ID列表。 
        BandwidthPackageVolume ( Integer ): 带宽包的带宽规格。单位：Mb。 
        EndPointGroups ( Array of EndPointGroups ): 终端节点组列表。 
        IPSets ( Array of IPSets ): 加速区域列表。 
        CreateTime ( Integer ): 基础型加速器的创建时间，用 Unix 时间戳表示。 
        CreateTimeStr ( String ): 加速器的创建时间，用字符串表示。 
        ExpiredTime ( Integer ): 过期时间，用 Unix 时间戳表示。仅包年包月加速器（ChargeType 为 PREPAY）包含此字段。 
        BeginTime ( Integer ): 计费生效时间，用 Unix 时间戳表示。 
        ProjectName ( String ): 加速器所属项目。 
        ResourceTags ( Array of ResourceTags ): 指定的资源标签的集合，每个对象为一个名值对格式的标签。 
       "字段"： EndPointGroups
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        EndPointGroupId ( String ): 终端节点组ID 
        Region ( String ): 终端节点组区域。 
            - CN_North：华北 
            - CN_East：华东 
            - CN_South：华南 
            - CN_NorthEast：东北 
            - CN_Central：华中 
            - CN_NorthWest：西北 
            - CN_SouthWest：西南 
            - AP1：亚太1 
       "字段"： IPSets
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        IPSetId ( String ): 加速区域ID。 
        Region ( String ): 加速区域所在的区域： 
            - CN_South：华南 
            - CN_North：华北 
            - CN_East：华东 
            - CN_NorthEast：东北 
            - CN_Central：华中 
            - CN_NorthWest：西北 
            - CN_SouthWest：西南 
            - AP1：亚太1 
       "字段"： ResourceTags
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Key ( String ): 标签名称。 
        Value ( String ): 和标签名称对应的值。 
    """,
    "list_basic_endpoint_groups": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 是  基础型加速器ID。 
             PageSize ( Integer ): 否  分页中显示的最大条目数。 
             PageNum ( Integer ): 否  返回分页的页码。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        EndpointGroups ( Array of EndpointGroups ): 终端节点组列表。每个对象为一个终端节点组的详情。 
        TotalCount ( Integer ): 查询到的总条目数。 
        PageSize ( Integer ): 分页中显示的最大条目数。 
        PageNum ( Integer ): 返回分页的页码。 
       "字段"： EndpointGroups
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        EndpointGroupId ( String ): 终端节点组ID。 
        AcceleratorId ( String ): 基础型加速器ID。 
        Name ( String ): 终端节点组名称。 
        State ( String ): 终端节点组的状态。取值： 
            - active：运行中 
            - deploying：配置中 
        Region ( String ): 终端节点组所在区域。 
            - CN_North：华北 
            - CN_East：华东 
            - CN_South：华南 
            - CN_NorthEast：东北 
            - CN_Central：华中 
            - CN_NorthWest：西北 
            - CN_SouthWest：西南 
            - AP1：亚太1 
        EndpointType ( String ): 终端节点类型。同一终端节点组的终端节点类型相同。取值： 
            - public：公网类型 
            - private：私网类型 
        ExistBoundEndpoint ( Boolean ): 终端节点组是否包含已绑定到加速IP的终端节点。 
            - true：包含已绑定加速IP的终端节点。 
            - false：组内所有终端节点均未绑定加速IP。 
        Endpoints ( Array of Endpoints ): 终端节点列表。 
       "字段"： Endpoints
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        EndpointId ( String ): 终端节点ID。 
        Type ( String ): 终端节点的类型。 
            - 公网类型终端节点组（EndpointType为public）取值： 
            	- ECS：边缘计算节点。 
            	- ENI：弹性网卡实例。 
            	- IP：IPv4类型的自定义源站 IP 。 
            - 私网类型终端节点组（EndpointType为private）取值： 
            	- EDX_IP：EDX私网IP。 
        EndpointAddress ( String ): 终端节点的地址，与您选择的类型有关。具体如下 
            - ECS：边缘计算实节点的ID。 
            - ENI：弹性网卡实例的ID。 
            - IP：自定义源站 IP 的公网 IPv4 地址。 
            - EDX_IP：EDX私网IP的地址。 
        EdgeNodeName ( String ): ECS或ENI所属的边缘节点名称，终端节点Type为ECS或ENI时存在。 
        PrivateInstanceID ( String ): 私有实例ID，终端节点组类型为私网时存在。 
    """,
    "list_basic_endpoints": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 是  基础型加速器ID。 
             EndpointGroupId ( String ): 是  终端节点组ID 
             PageSize ( Integer ): 否  分页中显示的最大条目数。 
             PageNum ( Integer ): 否  返回分页的页码。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Endpoints ( Array of Endpoints ): 终端节点列表。 
        TotalCount ( Integer ): 查询到的总条目数。 
        PageSize ( Integer ): 分页中显示的最大条目数。 
        PageNum ( Integer ): 返回分页的页码。 
       "字段"： Endpoints
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 加速器ID 
        EndpointGroupId ( String ): 终端节点组ID。 
        EdgeNodeName ( String ): 终端节点所属边缘计算节点名称。 
        EdgeNodeAlias ( String ): 终端节点所属边缘计算节点中文名称。 
        EndpointAddress ( String ): 与您选择的终端节点类型对应的终端节点地址。具体如下 
            - ECS：边缘计算实节点的ID。 
            - ENI：弹性网卡实例的ID。 
            - IP：自定义源站 IP 的公网 IPv4 地址。 
            - EDX_IP：EDX私网IP的地址。 
        EndpointId ( String ): 终端节点ID。 
        Type ( String ): 终端节点的类型。 
            - 公网类型终端节点组（EndpointType为public）取值： 
            	- ECS：边缘计算节点。 
            	- ENI：弹性网卡实例。 
            	- IP：IPv4类型的自定义源站 IP 。 
            - 私网类型终端节点组（EndpointType为private）取值： 
            	- EDX_IP：EDX私网IP。 
        AccelerateIPs ( Array of AccelerateIPs ): 终端节点绑定的加速IP列表。 
       "字段"： AccelerateIPs
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AccelerateIP ( String ): 加速IP地址。 
        ISP ( String ): 加速IP运营商。 
            - ChinaMobile：中国移动。 
            - ChinaUnicom：中国联通。 
            - ChinaTelecom：中国电信。 
            - BGP：BGP 
        State ( String ): 终端节点与加速IP的绑定状态，取值： 
            - active：已绑定 
            - inactive：待绑定 
    """,
    "list_basic_ip_sets": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 是  加速器ID 
             PageSize ( Integer ): 否  分页中显示的最大条目数。 
             PageNum ( Integer ): 否  返回分页的页码。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        IPSets ( Array of IPSets ): 加速区域列表。 
        TotalCount ( Integer ): 查询到的总条目数。 
        PageSize ( Integer ): 分页中显示的最大条目数。 
        PageNum ( Integer ): 页码 
       "字段"： IPSets
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        IPSetId ( String ): 加速区域ID。 
        AcceleratorId ( String ): 基础型加速器ID。 
        Region ( String ): 加速区域所在的区域： 
            - CN_South：华南 
            - CN_North：华北 
            - CN_East：华东 
            - CN_NorthEast：东北 
            - CN_Central：华中 
            - CN_NorthWest：西北 
            - CN_SouthWest：西南 
            - AP1：亚太1 
        IPVersion ( String ): 加速区域支持的 IP 协议版本： 
            - IPv4：表示加速器支持客户端使用 IPv4 地址进行访问。 
            - IPv4/IPv6：表示加速器支持客户端使用 IPv4 和 IPv6 地址进行访问。 
        State ( String ): 加速区域的状态。 
            - active：运行中 
            - deploying：配置中 
        ExistBoundIP ( Boolean ): 是否已绑定加速IP。 
        AccelerateIPs ( Array of String ): 加速IP的ID列表。 
    """,
    "list_endpoint_groups": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 否  加速器ID。ListenerId 与 AcceleratorId 两者至少需要指定一个。 
             ListenerId ( String ): 否  监听器 ID。ListenerId 与 AcceleratorId 两者至少需要指定一个。 
             PageSize ( Integer ): 否  分页中显示的最大条目数。 
             PageNum ( Integer ): 否  返回分页的页码。 
             Role ( String ): 否  选择查询主终端节点组还是备终端节点组： 
                   - main：主终端节点组（默认） 
                   - backup：备终端节点组 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        EndpointGroups ( Array of EndpointGroups ): 终端节点组列表。每个对象为一个终端节点组的详情。 
        PageNum ( Integer ): 返回分页的页码。 
        PageSize ( Integer ): 分页中显示的最大条目数。 
        TotalCount ( Integer ): 查询到的总条目数。 
       "字段"： EndpointGroups
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 加速器 ID。 
        Region ( String ): 终端节点组区域。 
            - CN_North：华北 
            - CN_East：华东 
            - CN_South：华南 
            - CN_NorthEast：东北 
            - CN_Central：华中 
            - CN_NorthWest：西北 
            - CN_SouthWest：西南 
            - AP1：亚太1 
        HealthCheckStatus ( String ): 该终端节点组的健康检查状态。 
            - detecting：探测中 
            - disable：未开启 
            - available：可用 
            - unavailable：不可用 
            - normal：正常 
            - abnormal：异常 
            - partiallyAbnormal：部分异常 
        HealthyConfig ( Object of HealthyConfig ): 健康检查的配置信息。 
        TrafficPercentage ( Integer ): 分配到该终端节点组的流量权重，即本终端节点组接入的流量在所有终端节点组接入流量的比例。 
            - 一个监听默认可以关联2个默认终端节点组，如果需要创建更多默认终端节点组，请联系客服经理。 
            - 每个终端节点组的流量调配取值范围：1~100。 
        ListenerId ( String ): 监听器 ID。 
        EndpointGroupId ( String ): 终端节点组ID。 
        Name ( String ): 终端节点组名称。 
        State ( String ): 终端节点组状态： 
            - active：运行中 
            - deleting： 删除中 
            - deploying：配置中 
        EndpointConfigurations ( Array of EndpointConfigurations ): 终端节点组包含的各终端节点的配置。 
        IsVolcSource ( Boolean ): 后端应用是否为托管在火山引擎的服务。 
        KeepClientIP ( Boolean ): 是否开启基于Proxy Protocol的保持客户端源IP功能。 
            - true：启用了保持客户端源IP功能。 
            - false：未启用此功能。 
        KeepClientIPMethod ( String ): Proxy Protocol 协议版本。取值： 
            - ProxyProtocolV1：仅支持TCP协议。通过在报文Payload开头添加Proxy Protocol v1报头（ASCII码格式）传递客户端源IP。 
            - ProxyProtocolV2：通过在报文Payload开头添加 Proxy Protocol v2报头（二进制格式）传递客户端源IP。 
        EndpointType ( String ): 终端节点类型，支持取值： 
            - public：公网 
            - private：私网 
        SourceIP ( Array of SourceIP ): 表示私网回源IP网段集合，仅在终端节点为私网类型时存在。 
        Role ( String ): 该终端节点组为主终端节点组还是备终端节点组： 
            - main：主终端节点组 
            - backup：备终端节点组 
       "字段"： HealthyConfig
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        HealthCheckEnable ( Boolean ): 是否开启健康检查： 
            - true：开启了健康检查功能。 
            - false：未开启健康检查功能。 
        HealthCheckProtocol ( String ): 健康检查协议，当前仅支持 TCP 协议。 
        HealthCheckPort ( Integer ): 健康检查端口，端口输入范围为1~65535。默认为80端口。 
        HealthResponseTimeOut ( Integer ): 健康检查超时时间，即等待健康检查响应的时间上限。 
            - 如果后端服务器在指定时间内没有正确响应，则判定本次健康检查异常。 
            - 默认响应超时时间为2秒，可设置的超时时间范围为1～50秒。 
        HealthCheckInterval ( Integer ): 健康检查间隔时间，即发起健康检查请求的时间间隔，单位为秒。 
            - 默认间隔为2秒，指每2秒对终端节点进行一次健康检查。 
            - 请合理设置检测间隔，以免健康检查请求对终端节点造成过多负担。可设置的检测间隔范围为1～50秒。 
        HealthyThreshold ( Integer ): 健康阈值，即连续健康检查请求成功的次数，系统以此来判断终端节点是否健康。 
            - 健康阈值默认为3次，指连续3次健康检查请求成功，才能判定终端节点状态健康。 
            - 允许设置的健康阈值为2～10次。 
       "字段"： EndpointConfigurations
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Type ( String ): 终端节点组内的终端节点类型，取值如下： 
            - IP：自定义IP。 
            - Domain：自定义域名。 
            - EDX_IP：私网 IP。 
        Endpoint ( String ): 与终端节点类型相对应的终端节点的值。例如：Type 为 IP 时，终端节点的 Endpoint 值则是一个 IP 地址。 
        Weight ( Integer ): 终端节点的权重。 
            - 终端节点权重决定了终端节点组内每个终端节点接收的流量比例。 
            - 您可以为每个终端节点设置 1 到 100 之间的权重值。 
            - 系统会计算终端节点组内所有终端节点权重的总和。然后，根据其权重与总权重的比例，将流量转发到每个终端节点。 
            - 如果某个终端节点健康检查失败，流量将按比例分配到该终端节点组中其余健康的终端节点。 
        PrivateInstanceID ( String ): 私网终端节点所在的私有实例IP，仅在终端节点类型为私网时存在。 
       "字段"： SourceIP
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        IPRange ( String ): 私网回源IP网段。 
        IPRangeId ( String ): 私网回源IP网段ID。 
    """,
    "list_listeners": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 是  加速器 ID。 
             PageSize ( Integer ): 否  每个分页显示的最大条目数。默认值：10。 
             PageNum ( Integer ): 否  需要返回分页的序号。1 表示第一个分页。默认值：1。 
             State ( String ): 否  基于监听器状态的筛选。仅返回指定状态的监听器。取值： 
                   - active：运行中 
                   - deleting：删除中 
                   - deploying：配置中 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Listeners ( Array of Listeners ): 监听器列表。 
        PageNum ( Integer ): 返回分页的页码。 
        PageSize ( Integer ): 分页中显示的最大条目数。 
        TotalCount ( Integer ): 查询到的总条目数。 
       "字段"： Listeners
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 加速器 ID。 
        AccountID ( String ): 当前用户账号 ID。 
        ListenerId ( String ): 监听器 ID。 
        Name ( String ): 监听器名称。 
        CreateTime ( Integer ): 监听器创建时间，以 UNIX 时间戳格式表示。 
        State ( String ): 监听器状态。取值： 
            - active：运行中 
            - deleting：删除中 
            - deploying：配置中 
        Protocol ( String ): 监听协议。取值： 
            - TCP 
            - UDP 
        PortRanges ( Array of PortRanges ): 监听器端口范围集合。每个端口范围由一个起始端口和一个结束端口定义。 
        EndpointGroupIds ( Array of String ): 主终端节点组 ID 的列表。 
            终端节点组详情，可以调用 DescribeEndpointGroup 获取。 
        BackupEndpointGroupIds ( Array of String ): 备终端节点组 ID 的列表。 
            终端节点组详情，可以调用 DescribeEndpointGroup 获取。 
        EnableAffinity ( Boolean ): 启用客户端亲和性 
        DisableIsolateTCPNullConn ( Boolean ): 禁用隔离TCP空连接 
        DisablePreConnect ( Boolean ): 禁用预连接 
        FixedSourceReturn ( Object of FixedSourceReturn ): 固定转发 IP 相关配置。 
        IPAccess ( Object of IPAccess ): 基于源 IP 地址的访问控制相关配置。 
       "字段"： PortRanges
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        FromPort ( Integer ): 起始端口。 
        ToPort ( Integer ): 结束端口。如果指定单个端口，则起始端口和结束端口相同。 
       "字段"： FixedSourceReturn
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否启用固定转发 IP。 取值： 
            - true：启用。 
            - false：不启用。 
        GroupID ( Integer ): 固定转发集群 ID。 
        Cidrs ( Array of String ): 固定转发 IP 开启后，出口 IP 网段的列表。 
       "字段"： IPAccess
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否启用基于源 IP 地址的访问控制。默认不启用。取值： 
            - true：启用。 
            - false：不启用。 
        FilterType ( String ): 表明访问控制是基于黑名单还是白名单。当 Enable 字段为 true 时，此选项必填。取值： 
            - WhiteList：白名单列表，仅允许列表中的 IP 地址访问监听器。 
            - BlackList：黑名单列表，仅阻止列表中的 IP 地址访问监听器。 
        FilterList ( Array of String ): 白名单或黑名单中的 IP 地址集合。单个值为一个 IP 地址和网段，最多输入 100 个值。当 Enable 字段为 true 时，此选项必填。 
    """,
}
