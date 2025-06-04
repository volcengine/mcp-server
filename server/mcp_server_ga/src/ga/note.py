note = {
    "describe_accelerator": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 是  加速器ID 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 加速器ID 
        CreateTime ( Integer ): 创建时间 
        CrossDomainBandwidthIds ( Array of String ): 跨域带宽包ID列表 
        BillingType ( String ): 计费类型 
        Bandwidth ( Integer ): 带宽大小 
        ConnectionNum ( Integer ): 连接数 
        RegionNum ( Integer ): 区域数 
        BillingSpec ( String ): 计费规格 
        TunnelIdsL3 ( Array of String ): 三层Tunnel ID列表 
        ConfDoneTunnelIdsL3 ( Array of String ): 配置完成的三层Tunnel ID列表 
        ExpiredTime ( Integer ): 过期时间 
        SchedTunnelL3 ( String ): 调度中Tunnel 
        FullPortSwitch ( Boolean ): 是否全端口模式 
        OriginSwitch ( Boolean ): 回源开关 
        CDBOriginSwitch ( Boolean ): CDB回源开关 
        BTForbidden ( Object of BTForbidden ): BT封禁 
        BillingSpecEffectiveTime ( Integer ): 计费规格生效时间 
        ResourceType ( String ): 三层加速器类型 
        VPCInfo ( Object of VPCInfo ): VPC信息 
        ChargeType ( String ): 计费类型 PREPAY:预付费 POSTPAY:后付费 
        BandwidthPackageIds ( Array of String ): 带宽包ID列表 
        Name ( String ): 名称 
        RenewType ( Integer ): 是否自动续费 
        BeginTime ( Integer ): 开始时间 
        WANBandwidthPackages ( Array of WANBandwidthPackages ): 公网带宽包列表 
        RegionCount ( Integer ): 区域数 
        State ( String ): 状态 
        CNAME ( String ): CNAME 
        ListenerCount ( Integer ): 监听数 
        AccountID ( String ): 账号ID 
        AccelerateType ( String ):  
        CreateTimeStr ( String ): 创建时间字符串 
        ProjectName ( String ): 项目名 
        ResourceTags ( Array of ResourceTags ): 标签列表 
       "字段"： BTForbidden
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        BTForbiddenKeyWord ( Array of String ):  
        BTForbiddenSwitch ( Boolean ):  
       "字段"： VPCInfo
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        VpcID ( Array of String ):  
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
       "字段"： ResourceTags
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Key ( String ): 标签名称，支持大/小写字母、数字和中文组成，支持"+-=@/._"等特殊字符，长度不超过 128 个字符，不允许以volc开头。 
        Value ( String ): 标签名称对应的值，由大/小写字母、数字和中文组成，支持"+-=@/._"等特殊字符，长度不超过 256个字符。 
    """,
    "describe_basic_accelerator": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 是  加速器ID 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 加速器ID 
        AccountID ( String ): 账号ID 
        AccountName ( String ): 账号名称 
        BandwidthPackageIds ( Array of String ): 公网带宽包ID列表 
        BandwidthPackageVolume ( Integer ): 带宽包大小 
        BeginTime ( Integer ): 计费开始时间 
        BillingType ( String ): 计费类型 
        ChargeType ( String ): 付费模式 PREPAY:预付费 POSTPAY:后付费 
        CreateTime ( Integer ): 创建时间 
        CreateTimeStr ( String ): 创建时间字符串 
        CrossDomainBandwidthIds ( Array of String ): 跨境带宽包ID列表 
        EndPointGroups ( Array of EndPointGroups ): 终端节点组列表 
        ExpiredTime ( Integer ): 过期时间 
        IPSets ( Array of IPSets ): IPSet列表 
        Mode ( String ): 模式 
        Name ( String ): 加速器名称 
        ProjectName ( String ): 项目名 
        RenewType ( Integer ): 是否自动续费 
        ResourceTags ( Array of ResourceTags ): 标签列表 
        State ( String ): 状态 
       "字段"： EndPointGroups
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        EndPointGroupId ( String ): 终端节点组ID 
        Region ( String ): 区域 
       "字段"： IPSets
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        IPSetId ( String ): 加速区域ID 
        Region ( String ): 区域 
       "字段"： ResourceTags
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Key ( String ): 标签名称，支持大/小写字母、数字和中文组成，支持"+-=@/._"等特殊字符，长度不超过 128 个字符，不允许以volc开头。 
        Value ( String ): 标签名称对应的值，由大/小写字母、数字和中文组成，支持"+-=@/._"等特殊字符，长度不超过 256个字符。 
    """,
    "describe_basic_endpoint_group": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 是  加速器ID 
             EndpointGroupId ( String ): 是  终端节点组ID 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 加速器ID 
        EndpointGroupId ( String ): 终端节点组ID 
        EndpointType ( String ): 终端节点类型 
        Endpoints ( Array of Endpoints ): 终端节点列表 
        ExistBoundEndpoint ( Boolean ): 是否存在绑定的终端节点 
        Name ( String ): 终端节点组名称 
        Region ( String ): 区域 
        State ( String ): 终端节点组状态 
       "字段"： Endpoints
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        EndpointId ( String ): 终端节点ID 
        Type ( String ): 终端节点类型 
        EndpointAddress ( String ): 终端节点地址 
        EdgeNodeName ( String ): 边缘节点名称 
        PrivateInstanceID ( String ): 私有实例ID 
    """,
    "describe_basic_ip_set": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 是  加速器ID 
             IPSetId ( String ): 是  IPSetID 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AccelerateIPs ( Array of String ): 加速IP列表 
        AcceleratorId ( String ): 加速器ID 
        ExistBoundIP ( Boolean ): 是否存在绑定IP 
        IPSetId ( String ): IPSet ID 
        IPVersion ( String ): IP版本 
        Region ( String ): 区域 
        State ( String ): 状态 
    """,
    "describe_endpoint_group": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             ListenerId ( String ): 是  监听器ID 
             EndpointGroupId ( String ): 是  终端节点组ID 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 加速器ID 
        Region ( String ): 区域 
        HealthCheckStatus ( String ): 健康检查状态 
        HealthyConfig ( Object of HealthyConfig ): 健康检查配置 
        TrafficPercentage ( Integer ): 流量百分比 
        ListenerId ( String ): 监听器ID 
        EndpointGroupId ( String ): 终端节点组ID 
        Name ( String ): 名称 
        State ( String ): 状态 
        EndpointConfigurations ( Array of EndpointConfigurations ): 配置列表 
        IsVolcSource ( Boolean ): 火山源站 
        KeepClientIP ( Boolean ): 保持客户端源IP 
        KeepClientIPMethod ( String ): 保持客户端源IP方法 
        EndpointType ( String ):  
        SourceIP ( Array of SourceIP ):  
        Role ( String ):  
       "字段"： HealthyConfig
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        HealthCheckEnable ( Boolean ): 是否开启健康检查 
        HealthCheckProtocol ( String ): 健康检查协议 
        HealthCheckPort ( Integer ): 健康检查端口 
        HealthResponseTimeOut ( Integer ): 健康检查超时时间 
        HealthCheckInterval ( Integer ): 健康检查间隔时间 
        HealthyThreshold ( Integer ): 健康阈值 
       "字段"： EndpointConfigurations
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Type ( String ): 终端节点类型 
        Endpoint ( String ): 终端节点 
        Weight ( Integer ): 权重 
        PrivateInstanceID ( String ):  
        LineName ( String ):  
       "字段"： SourceIP
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        IPRange ( String ):  
        IPRangeId ( String ):  
    """,
    "describe_ip_set": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 是  加速器ID 
             IPSetId ( String ): 是  IPSet ID 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        IPSet ( Object of IPSet ): IPSet信息 
       "字段"： IPSet
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
    "describe_statistics": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             InputIdType ( String ): 是  查询ID类型，支持参数：AcceleratorId,ListenerId 
             InputId ( Array of String ): 是  查询ID列表 
             Interval ( Integer ): 是  查询时间粒度，单位：秒，支持参数：60,300 
             StartTime ( String ): 是  查询起始时间 
             EndTime ( String ): 是  查询结束时间 
             Metrics ( Array of String ): 否  查询指标列表 
             Region ( Array of String ): 否  查询区域列表 
             GroupByListener ( Boolean ): 否  按指定监听器聚合 
             GroupByRegion ( Boolean ): 否  按指定加速区域聚合 
             RegionType ( String ): 否  加速区域 
             GroupByAccelerator ( Boolean ): 否  按指定加速器聚合 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Results ( Array of Results ): 查询结果列表 
        TotalStatisticResults ( Array of TotalStatisticResults ): 汇总数据 
       "字段"： Results
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        StatisticsResults ( Array of StatisticsResults ): 统计结果 
        TimeStamp ( String ): 时间戳 
        TimeStampInt ( Integer ):  
       "字段"： TotalStatisticResults
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 加速器ID 
        ListenerId ( String ): 监听器ID 
        MaxBandwidth ( Float ): 最大带宽 
        MaxBandwidth95 ( Float ): 最大95带宽 
        MaxConnectionNum ( Float ): 最大连接数 
        Region ( String ): 区域 
        TotalTraffic ( Float ): 总流量 
       "字段"： StatisticsResults
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 加速器ID 
        DetailInfo ( Array of DetailInfo ): 明细数据列表 
        ListenerId ( String ): 监听器ID 
        Region ( String ): 区域 
       "字段"： DetailInfo
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Name ( String ): 在请求时选择的 Metrics 中的字段。 
        Value ( Float ): 对应该字段的值。 
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
    "list_accelerators": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 否  加速器ID 
             State ( String ): 否  状态 
             PageSize ( Integer ): 否  页大小 
             PageNum ( Integer ): 否  页码 
             Name ( String ): 否  名称 
             Filters ( Array of Filters ): 否  过滤条件 
             WithBandwidthPackage ( Boolean ): 否  携带带宽包信息 
             ChargeType ( String ): 否  付费方式 PREPAY:预付费 POSTPAY:后付费 
             BillingSpec ( String ): 否  计费类型 
             ProjectName ( String ): 否  项目名 
             ResourceTagFilter ( Object of ResourceTagFilter ): 否  标签过滤器 
            "字段"： Filters
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Name ( String ): 否  条件名 
             Values ( Array of String ): 否  条件值 
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
        Accelerators ( Array of Accelerators ): 加速器列表 
        PageNum ( Integer ): 页码 
        PageSize ( Integer ): 页大小 
        TotalCount ( Integer ): 总数 
       "字段"： Accelerators
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 加速器ID 
        CreateTime ( Integer ): 创建时间 
        CrossDomainBandwidthIds ( Array of String ): 跨域带宽包ID列表 
        BillingType ( String ): 计费类型 
        Bandwidth ( Integer ): 带宽大小 
        ConnectionNum ( Integer ): 连接数 
        RegionNum ( Integer ): 区域数 
        BillingSpec ( String ): 计费规格 
        TunnelIdsL3 ( Array of String ): 三层Tunnel ID列表 
        ConfDoneTunnelIdsL3 ( Array of String ): 配置完成的三层Tunnel ID列表 
        ExpiredTime ( Integer ): 过期时间 
        SchedTunnelL3 ( String ): 调度中Tunnel 
        FullPortSwitch ( Boolean ): 是否全端口模式 
        OriginSwitch ( Boolean ): 回源开关 
        CDBOriginSwitch ( Boolean ): CDB回源开关 
        BTForbidden ( Object of BTForbidden ): BT封禁 
        BillingSpecEffectiveTime ( Integer ): 计费规格生效时间 
        ResourceType ( String ): 三层加速器类型 
        VPCInfo ( Object of VPCInfo ): VPC信息 
        ChargeType ( String ): 计费类型 PREPAY:预付费 POSTPAY:后付费 
        BandwidthPackageIds ( Array of String ): 带宽包ID列表 
        Name ( String ): 名称 
        RenewType ( Integer ): 是否自动续费 
        BeginTime ( Integer ): 开始时间 
        WANBandwidthPackages ( Array of WANBandwidthPackages ): 公网带宽包列表 
        RegionCount ( Integer ): 区域数 
        State ( String ): 状态 
        CNAME ( String ): CNAME 
        ListenerCount ( Integer ): 监听数 
        AccountID ( String ): 账号ID 
        AccelerateType ( String ):  
        CreateTimeStr ( String ): 创建时间字符串 
        ProjectName ( String ): 项目名 
        ResourceTags ( Array of ResourceTags ): 标签列表 
       "字段"： BTForbidden
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        BTForbiddenKeyWord ( Array of String ):  
        BTForbiddenSwitch ( Boolean ):  
       "字段"： VPCInfo
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        VpcID ( Array of String ):  
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
       "字段"： ResourceTags
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Key ( String ): 标签名称，支持大/小写字母、数字和中文组成，支持"+-=@/._"等特殊字符，长度不超过 128 个字符，不允许以volc开头。 
        Value ( String ): 标签名称对应的值，由大/小写字母、数字和中文组成，支持"+-=@/._"等特殊字符，长度不超过 256个字符。 
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
             AcceleratorId ( String ): 是  加速器ID 
             IPSetId ( String ): 是  IPSet ID 
             PageSize ( Integer ): 是  页大小 
             PageNum ( Integer ): 是  页码 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AccelerateIPs ( Array of AccelerateIPs ): 加速器IP列表 
        TotalCount ( Integer ): 总数 
        PageSize ( Integer ): 页大小 
        PageNum ( Integer ): 页码 
       "字段"： AccelerateIPs
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AccelerateIPAddress ( String ): 加速IP地址 
        AccelerateIPId ( String ): 加速IP ID 
        AcceleratorId ( String ): 加速器 ID 
        BindingMode ( String ): 绑定模式 
        EdgeNodeAlias ( String ): 加速IP所属边缘节点名称 
        EdgeNodeName ( String ): 加速IP所属边缘节点 
        Endpoints ( Array of Endpoints ): 加速IP绑定终端节点组列表 
        IPSetId ( String ): 加速区域ID 
        ISP ( String ): 加速IP所属运营商 
        State ( String ): 状态 
        Mode ( String ): 绑定模式 
       "字段"： Endpoints
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        EndpointAddress ( String ): 终端节点地址 
        EndpointId ( String ): 终端节点ID 
        Type ( String ): 终端节点类型 
        InternalIPs ( Array of String ):  
        PrivateInstanceID ( String ):  
    """,
    "list_basic_accelerators": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 否  加速器ID 
             State ( String ): 否  状态 
             Name ( String ): 否  名称 
             WithBandwidthPackage ( Boolean ): 否  是否有带宽包 
             ChargeType ( String ): 否  计费类型 PREPAY:预付费 POSTPAY:后付费 
             PageSize ( Integer ): 否  页大小 
             PageNum ( Integer ): 否  页码 
             IPSetRegion ( String ): 否  IPSet区域 
             EndPointGroupRegion ( String ): 否  终端节点组区域 
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
        Accelerators ( Array of Accelerators ): 加速器列表 
        TotalCount ( Integer ): 总数 
        PageSize ( Integer ): 页大小 
        PageNum ( Integer ): 页码 
       "字段"： Accelerators
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 加速器ID 
        CrossDomainBandwidthIds ( Array of String ): 跨境带宽包ID列表 
        BandwidthPackageIds ( Array of String ): 公网带宽包ID列表 
        EndPointGroups ( Array of EndPointGroups ): 终端节点组列表 
        IPSets ( Array of IPSets ): IPSet列表 
        CreateTime ( Integer ): 创建时间 
        ExpiredTime ( Integer ): 过期时间 
        BeginTime ( Integer ): 计费开始时间 
        BandwidthPackageVolume ( Integer ): 带宽包大小 
        Name ( String ): 加速器名称 
        Mode ( String ): 模式 
        State ( String ): 状态 
        BillingType ( String ): 计费类型 
        RenewType ( Integer ): 是否自动续费 
        ChargeType ( String ): 付费模式 PREPAY:预付费 POSTPAY:后付费 
        AccountID ( String ): 账号ID 
        AccountName ( String ): 账号名称 
        CreateTimeStr ( String ): 创建时间字符串 
        ProjectName ( String ): 项目名 
        ResourceTags ( Array of ResourceTags ): 标签列表 
       "字段"： EndPointGroups
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        EndPointGroupId ( String ): 终端节点组ID 
        Region ( String ): 区域 
       "字段"： IPSets
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        IPSetId ( String ): 加速区域ID 
        Region ( String ): 区域 
       "字段"： ResourceTags
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Key ( String ): 标签名称，支持大/小写字母、数字和中文组成，支持"+-=@/._"等特殊字符，长度不超过 128 个字符，不允许以volc开头。 
        Value ( String ): 标签名称对应的值，由大/小写字母、数字和中文组成，支持"+-=@/._"等特殊字符，长度不超过 256个字符。 
    """,
    "list_basic_endpoint_groups": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 是  加速器ID 
             PageSize ( Integer ): 是  页大小 
             PageNum ( Integer ): 是  页码 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        EndpointGroups ( Array of EndpointGroups ): 终端节点组列表 
        TotalCount ( Integer ): 总数 
        PageSize ( Integer ): 页大小 
        PageNum ( Integer ): 页码 
       "字段"： EndpointGroups
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        EndpointGroupId ( String ): 终端节点组ID 
        AcceleratorId ( String ): 加速器ID 
        Name ( String ): 终端节点组名称 
        State ( String ): 终端节点组状态 
        Region ( String ): 区域 
        Endpoints ( Array of Endpoints ): 终端节点列表 
        ExistBoundEndpoint ( Boolean ): 是否存在绑定的终端节点 
        EndpointType ( String ): 终端节点类型 
       "字段"： Endpoints
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        EndpointId ( String ): 终端节点ID 
        Type ( String ): 终端节点类型 
        EndpointAddress ( String ): 终端节点地址 
        EdgeNodeName ( String ): 边缘节点名称 
        PrivateInstanceID ( String ): 私有实例ID 
    """,
    "list_basic_endpoints": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AcceleratorId ( String ): 是  加速器ID 
             EndpointGroupId ( String ): 否  终端节点组ID 
             PageSize ( Integer ): 是  页大小 
             PageNum ( Integer ): 是  页码 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Endpoints ( Array of Endpoints ): 终端节点列表 
        TotalCount ( Integer ): 总数 
        PageSize ( Integer ): 页大小 
        PageNum ( Integer ): 页码 
       "字段"： Endpoints
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AccelerateIPs ( Array of AccelerateIPs ): 终端节点绑定加速器IP列表 
        AcceleratorId ( String ): 加速器ID 
        EdgeNodeAlias ( String ): 终端节点所属边缘节点名称 
        EndpointAddress ( String ):  
        EndpointGroupId ( String ): 终端节点组ID 
        EndpointId ( String ): 终端节点ID 
        Type ( String ): 终端节点类型 
        AddressInstanceID ( String ):  
        EdgeNodeName ( String ): 终端节点所属边缘节点 
        PrivateInstanceID ( String ):  
        VpcID ( String ):  
        VpcRouteTableID ( String ):  
        VpcRouteTableName ( String ):  
       "字段"： AccelerateIPs
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AccelerateIP ( String ): 加速IP地址 
        AccelerateIPId ( String ): 加速IP ID 
        ISP ( String ): 加速IP运营商 
        State ( String ): 绑定状态 
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
             PageSize ( Integer ): 是  页大小 
             PageNum ( Integer ): 是  页码 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        IPSets ( Array of IPSets ): IPSet列表 
        TotalCount ( Integer ): 总数 
        PageSize ( Integer ): 页大小 
        PageNum ( Integer ): 页码 
       "字段"： IPSets
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        IPSetId ( String ): IPSet ID 
        AcceleratorId ( String ): 加速器ID 
        Region ( String ): 区域 
        IPVersion ( String ): IP版本 
        State ( String ): 状态 
        ExistBoundIP ( Boolean ): 是否存在绑定IP 
        AccelerateIPs ( Array of String ): 加速IP列表 
    """,
    "list_endpoint_groups": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             ListenerId ( String ): 是  监听器ID 
             PageSize ( Integer ): 否  页大小 
             PageNum ( Integer ): 否  页码 
             AcceleratorId ( String ): 否  加速器ID 
             Role ( String ): 否   
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        EndpointGroups ( Array of EndpointGroups ): 终端节点组列表 
        PageNum ( Integer ): 页码 
        PageSize ( Integer ): 页大小 
        TotalCount ( Integer ): 总数 
       "字段"： EndpointGroups
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AcceleratorId ( String ): 加速器ID 
        Region ( String ): 区域 
        HealthCheckStatus ( String ): 健康检查状态 
        HealthyConfig ( Object of HealthyConfig ): 健康检查配置 
        TrafficPercentage ( Integer ): 流量百分比 
        ListenerId ( String ): 监听器ID 
        EndpointGroupId ( String ): 终端节点组ID 
        Name ( String ): 名称 
        State ( String ): 状态 
        EndpointConfigurations ( Array of EndpointConfigurations ): 配置列表 
        IsVolcSource ( Boolean ): 火山源站 
        KeepClientIP ( Boolean ): 保持客户端源IP 
        KeepClientIPMethod ( String ): 保持客户端源IP方法 
        EndpointType ( String ):  
        SourceIP ( Array of SourceIP ):  
        Role ( String ):  
       "字段"： HealthyConfig
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        HealthCheckEnable ( Boolean ): 是否开启健康检查 
        HealthCheckProtocol ( String ): 健康检查协议 
        HealthCheckPort ( Integer ): 健康检查端口 
        HealthResponseTimeOut ( Integer ): 健康检查超时时间 
        HealthCheckInterval ( Integer ): 健康检查间隔时间 
        HealthyThreshold ( Integer ): 健康阈值 
       "字段"： EndpointConfigurations
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Type ( String ): 终端节点类型 
        Endpoint ( String ): 终端节点 
        Weight ( Integer ): 权重 
        PrivateInstanceID ( String ):  
        LineName ( String ):  
       "字段"： SourceIP
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        IPRange ( String ):  
        IPRangeId ( String ):  
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
        PageNum ( Integer ): 页码 
        PageSize ( Integer ): 返回分页的序号。 
        TotalCount ( Integer ): 总条目数，即为该加速器上所有监听器的数量。 
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
