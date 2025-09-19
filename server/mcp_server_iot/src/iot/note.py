note = {
    "call_service": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             DeviceName ( String ): 是  设备名称 
             ElementIdentifier ( String ): 是  功能标示ID 
             InstanceID ( String ): 是  实例ID 
             ModuleKey ( String ): 是  模块标示 
             Params ( JSON Map ): 否  输入参数 
             ProductKey ( String ): 是  产品标示 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        OutputData ( JSON Map ): 服务调用输出参数 
        TraceID ( String ): 一次服务调用唯一ID 
    """,
    "get_all_last_device_property_value": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             DeviceName ( String ): 是  设备名称 
             InstanceID ( String ): 是  实例ID 
             ProductKey ( String ): 是  设备产品标识 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        PropertyValues ( Array of PropertyValues ): 属性值 
       "字段"： PropertyValues
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Module ( String ): 物模型模块 
        PropertyValues ( Array of PropertyValues ): 属性列表 
    """,
    "get_custom_topic_list": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             InstanceID ( String ): 是  实例ID 
             ProductKey ( String ): 是  产品标识 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        CustomTopics ( Array of CustomTopics ): 自动义topic列表 
       "字段"： CustomTopics
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Description ( String ): 描述 长度限制小于128个字符 
        OperateType ( String ): 设备操作权限，Publish-发布，Subscribe-订阅，All-发布和订阅 
        TopicSuffix ( String ): 主题后缀，topic默认前缀是 sys/{ProductKey}/{DeviceName}/custom/，Topic长度不超过64个字节，支持英文字母、数字、_、+、#、/，其中+和#仅设备操作权限为订阅时支持，/和+不能连续出现，#只能出现一次且只能在末尾，不能以/开头或结尾 
    """,
    "get_device_detail": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             DeviceName ( String ): 是  设备名称 
             InstanceID ( String ): 是  实例ID 
             ProductKey ( String ): 是  设备产品标识 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AccountID ( Long ): 账户ID 
        ActivateTime ( String ): 激活时间 
        BatchCreateRecordID ( String ): 批次记录ID 
        ConnectTime ( String ): 最近连接时间 
        ConnectType ( String ): 连接类型，支持 Direct/Proxy 直连/代理 
        CreateTime ( String ): 创建时间 
        DisconnectTime ( String ): 最近断开连接时间 
        ExtraName ( String ): 备注名称，支持中文、英文字母、数字、和特殊字符_-@()，长度限制 0~32个字符 
        GenerateType ( String ): 设备类型，自动创建/用户导入/网关创建, Create/Import/Gateway 
        ID ( String ): 设备ID 
        IP ( String ): 设备IP 
        LLMUsage ( Object of LLMUsage ):  
        Name ( String ): 设备名称 
        NodeType ( String ): 节点类型，直连设备-Device、网关设备-Gateway、网关子设备-SubDevice 
        OTAModuleVersion ( JSON Map ): 固件版本，key为OTA模块名称，value为固件版本号 
        ProductKey ( String ): 产品标示 
        ProductName ( String ): 产品名称 
        Secret ( String ): 设备密钥 
        Status ( String ): 设备状态，Online/Offline/NeverConnected/Disable，在线/离线/未激活/禁用 
        UpdateTime ( String ): 最近修改时间时间 
       "字段"： LLMUsage
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Character ( Integer ):  
        Duration ( Double ):  
        Request ( Integer ):  
        Status ( String ):  
        TokenTotal ( Integer ):  
    """,
    "get_device_event_record_list": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             DeviceName ( String ): 是  设备名称 
             EndTime ( Long ): 否  结束时间时间，单位为秒 
             EventType ( String ): 否  事件类型(只有事件有)，信息、报警、故障;Info/Alert/Error 
             Identifier ( String ): 否  功能标示 
             InstanceID ( String ): 是  实例ID 
             ModuleKey ( String ): 否  模块标示 
             Name ( String ): 否  功能名称，模糊匹配 
             Page ( Long ): 否  页码，默认为1 
             ProductKey ( String ): 是  产品标示 
             Size ( Long ): 否  每页条数，默认为10 
             StartTime ( Long ): 否  开始时间,单位为秒 
             Status ( String ): 否  调用状态(只有服务有)，调用中/调用完成；Calling/Done 
             TraceID ( String ): 否  追踪ID 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        List ( Array of List ): 调用记录 
        Page ( Long ): 页码，默认为1 
        Size ( Long ): 每页条数，默认为10 
        Total ( Long ): 总条数 
       "字段"： List
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        CreateTime ( String ): 创建时间，事件上报场景中，为事件上报事件 
        DeviceName ( String ): 设备名称 
        EventType ( String ): 事件类型(只有事件有)，信息、报警、故障;Info/Alert/Error 
        ID ( String ): 调用记录ID 
        Identifier ( String ): 功能标示 
        ModuleKey ( String ): 模块标示 
        Name ( String ): 功能名称 
        OutputData ( JSON Map ): 输出参数 
        ProductKey ( String ): 产品标示 
        TraceID ( String ): 追踪ID 
        UpdateTime ( String ): 更新时间 
    """,
    "get_device_list": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             BatchCreateRecordID ( String ): 否  批次ID 
             HasSetGeoLocation ( Boolean ): 否  过滤平台上设置过地理位置的设备 
             InstanceID ( String ): 是  实例ID 
             Name ( String ): 否  设备名称，支持模糊查询 
             OTAModule ( String ): 否  OTA模块名称 
             OTAModuleVersion ( String ): 否  固件版本号，支持多选，用逗号分隔 
             Page ( Long ): 否  页码，默认为1 
             ProductKey ( String ): 否  产品标示 
             Size ( Long ): 否  每页条数，默认为10 
             Status ( String ): 否  状态，Online/Offline/NeverConnected/Disable，在线/离线/未激活/禁用 
             Tags ( Array of Tags ): 否  标签列表，多个标签之间是与的关系 
            "字段"： Tags
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Key ( String ): 是  标签key 
             Value ( String ): 是  标签值 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        List ( Array of List ): 当前页设备列表 
        Page ( Long ): 页码，默认为1 
        Size ( Long ): 每页条数，默认为10 
        Total ( Long ): 总条数 
       "字段"： List
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AccountID ( Long ): 账户ID 
        ActivateTime ( String ): 激活时间 
        BatchCreateRecordID ( String ): 批次记录ID 
        ConnectTime ( String ): 最近连接时间 
        ConnectType ( String ): 连接类型，支持 Direct/Proxy 直连/代理 
        CreateTime ( String ): 创建时间 
        DisconnectTime ( String ): 最近断开连接时间 
        ExtraName ( String ): 备注名称，支持中文、英文字母、数字、和特殊字符_-@()，长度限制 0~32个字符 
        GenerateType ( String ): 设备类型，自动创建/用户导入/网关创建, Create/Import/Gateway 
        ID ( String ): 设备ID 
        IP ( String ): 设备IP 
        LLMUsage ( Object of LLMUsage ):  
        Name ( String ): 设备名称 
        NodeType ( String ): 节点类型，直连设备-Device、网关设备-Gateway、网关子设备-SubDevice 
        OTAModuleVersion ( JSON Map ): 固件版本，key为OTA模块名称，value为固件版本号 
        ProductKey ( String ): 产品标示 
        ProductName ( String ): 产品名称 
        Secret ( String ): 设备密钥 
        Status ( String ): 设备状态，Online/Offline/NeverConnected/Disable，在线/离线/未激活/禁用 
        UpdateTime ( String ): 最近修改时间时间 
       "字段"： LLMUsage
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Character ( Integer ):  
        Duration ( Double ):  
        Request ( Integer ):  
        Status ( String ):  
        TokenTotal ( Integer ):  
    """,
    "get_device_overview": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             InstanceID ( String ): 是  实例ID 
             ProductKey ( String ): 否  产品标识 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Active ( Long ): 活跃设备数（当天有属性或者事件上报） 
        Disable ( Long ): 禁用设备数 
        NeverConnected ( Long ): 未激活设备数 
        Offline ( Long ): 离线设备数 
        Online ( Long ): 在线设备数 
        Total ( Long ): 总设备数 
    """,
    "get_device_status": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             DeviceName ( String ): 是  设备名称 
             InstanceID ( String ): 是  实例ID 
             ProductKey ( String ): 是  设备产品标识 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Status ( String ): 设备状态 Online-在线 Offline-离线 NeverConnected-未激活 Disable-禁用 
    """,
    "get_device_service_call_record_list": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             DeviceName ( String ): 是  设备名称 
             EndTime ( Long ): 否  结束时间时间，单位为秒 
             Identifier ( String ): 否  功能标示 
             InstanceID ( String ): 是  实例ID 
             ModuleKey ( String ): 否  模块标示 
             Name ( String ): 否  功能名称，模糊匹配 
             Page ( Long ): 否  页码，默认为1 
             ProductKey ( String ): 是  产品标示 
             Size ( Long ): 否  每页条数，默认为10 
             StartTime ( Long ): 否  开始时间,单位为秒 
             Status ( String ): 否  调用状态(只有服务有)，调用中/调用完成；Calling/Done 
             TraceID ( String ): 否  追踪ID 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        List ( Array of List ): 调用记录 
        Page ( Long ): 页码，默认为1 
        Size ( Long ): 每页条数，默认为10 
        Total ( Long ): 总条数 
       "字段"： List
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        CallType ( String ): 同步/异步;sync/async 
        CreateTime ( String ): 创建时间，事件上报场景中，为事件上报事件 
        DeviceName ( String ): 设备名称 
        ID ( String ): 调用记录ID 
        Identifier ( String ): 功能标示 
        InputData ( JSON Map ): 输入参数 
        ModuleKey ( String ): 模块标示 
        Name ( String ): 功能名称 
        OutputData ( JSON Map ): 输出参数 
        ProductKey ( String ): 产品标示 
        Status ( String ): 调用状态，调用中/调用完成；Calling/Done 
        TraceID ( String ): 追踪ID 
        UpdateTime ( String ): 更新时间 
    """,
    "get_instance_detail": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             InstanceID ( String ): 是  实例ID 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AutoRenew ( Boolean ):  
        BeginTime ( String ): 实例生效时间 
        CreateTime ( String ): 创建时间 
        Description ( String ): 描述信息 
        EndTime ( String ): 到期时间 
        Favor ( String ): 是否被用户收藏 favor:收藏 / not_favor:未收藏 
        ID ( String ): 实例ID 
        InstanceGroupID ( String ): 实例组ID 
        InstanceGroupName ( String ): 实例组名称 
        IsPublicInstance ( Boolean ): 是否是公共实例, 公共实例-true 企业实例-false 
        LLMType ( String ): 端智能实例类型 
        Name ( String ): 实例名称 
        Quota ( Object of Quota ): 实例Quota 
        Status ( String ): 实例状态 Pending-创建中 Running-运行中 Expiring-到期关停中 Expired-到期关停 Modifying-升级中 CreateFailed-创建失败 Reclaiming-回收中 Reclaimed-已回收 Terminating-退订中 Terminated-已退订 
        Tags ( JSON Map ): 实例标签 
        Type ( String ): 实例类型 Standard-标准型 / Exculsive-独占型 
        UpdateTime ( String ): 更新时间 
       "字段"： Quota
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        DeviceNum ( Long ): 实例内最大设备数 
        LogRetainTime ( Long ): 日志保留时间（单位：天） 
        MessageTPS ( Long ): 消息上下行TPS 
        OnlineDeviceNum ( Long ): 实例内最大在线设备数 
        PropertyRetainTime ( Long ): 属性保留时间（单位：天） 
        RuleEngineTPS ( Long ): 规则引擎TPS 
    """,
    "get_instance_endpoints": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             InstanceID ( String ): 是  公共实例ID 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        CloudAPIEndpoint ( Object of CloudAPIEndpoint ):  
        DeviceAPIEndpoint ( Object of DeviceAPIEndpoint ):  
        MQTTAccessDetail ( Object of MQTTAccessDetail ):  
       "字段"： CloudAPIEndpoint
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Endpoint ( String ): endpoint 
       "字段"： DeviceAPIEndpoint
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Endpoint ( String ): endpoint 
       "字段"： MQTTAccessDetail
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Endpoint ( String ): endpoint 
        Port ( Long ): 端口号 
        TLSPort ( Long ): tls端口号 
    """,
    "get_instance_list": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Favor ( String ): 否  是否被用户收藏 favor:收藏 / not_favor:未收藏 
             InstanceGroupID ( String ): 否  实例组ID 
             InstanceID ( String ): 否  实例ID 
             IsPublicInstance ( Boolean ): 否  是否是公共实例 
             Name ( String ): 否  实例名称 
             Page ( Long ): 否  第几页 
             Size ( Long ): 否  每页大小 
             Status ( String ): 否  实例状态 Pending-创建中 Running-运行中 Expiring-到期关停中 Expired-到期关停 Modifying-升级中 CreateFailed-创建失败 Reclaiming-回收中 Reclaimed-已回收 Terminating-退订中 Terminated-已退订 
             Tags ( JSON Map ): 否  每页大小 
             Type ( String ): 否  实例类型 Standard-标准型 / Exculsive-独占型 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        List ( Array of List ): 实例列表 
        Page ( Long ): 第几页 
        Size ( Long ): 每页大小 
        Total ( Long ): 总数 
       "字段"： List
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AutoRenew ( Boolean ):  
        BeginTime ( String ): 实例生效时间 
        CreateTime ( String ): 创建时间 
        Description ( String ): 描述信息 
        EndTime ( String ): 到期时间 
        Favor ( String ): 是否被用户收藏 favor:收藏 / not_favor:未收藏 
        ID ( String ): 实例ID 
        InstanceGroupID ( String ): 实例组ID 
        InstanceGroupName ( String ): 实例组名称 
        IsPublicInstance ( Boolean ): 是否是公共实例, 公共实例-true 企业实例-false 
        LLMType ( String ): 端智能实例类型 
        Name ( String ): 实例名称 
        Quota ( Object of Quota ): 实例Quota 
        Status ( String ): 实例状态 Pending-创建中 Running-运行中 Expiring-到期关停中 Expired-到期关停 Modifying-升级中 CreateFailed-创建失败 Reclaiming-回收中 Reclaimed-已回收 Terminating-退订中 Terminated-已退订 
        Tags ( JSON Map ): 实例标签 
        Type ( String ): 实例类型 Standard-标准型 / Exculsive-独占型 
        UpdateTime ( String ): 更新时间 
       "字段"： Quota
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        DeviceNum ( Long ): 实例内最大设备数 
        LogRetainTime ( Long ): 日志保留时间（单位：天） 
        MessageTPS ( Long ): 消息上下行TPS 
        OnlineDeviceNum ( Long ): 实例内最大在线设备数 
        PropertyRetainTime ( Long ): 属性保留时间（单位：天） 
        RuleEngineTPS ( Long ): 规则引擎TPS 
    """,
    "get_last_device_property_value": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             DeviceName ( String ): 是  设备名称 
             Identifiers ( Array of String ): 否  属性ID，不传则查询整个模块下所有的属性值 
             InstanceID ( String ): 是  实例ID 
             ModuleKey ( String ): 是  模块标示 
             ProductKey ( String ): 是  产品标示 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        PropertyValues ( Array of PropertyValues ): 属性值 
       "字段"： PropertyValues
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Identifier ( String ): 属性 
        Time ( Long ): 上报时间戳，单位毫秒 
        Value ( Object of Value ): 值 
    """,
    "get_product_list": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             CategoryKey ( String ): 否  所属品类Key 
             InstanceID ( String ): 是  实例ID 
             IsStandard ( Boolean ): 否  是否是标准品类，true-标准品类，false-自定义 
             Name ( String ): 否  名称,支持模糊匹配 
             Page ( Long ): 否  页码，默认为1 
             ProductKey ( String ): 否  产品标识 
             Size ( Long ): 否  每页条数，默认为10 
             Tags ( Array of Tags ): 否  标签列表，多个标签之间是与的关系 
            "字段"： Tags
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Key ( String ): 是  标签key 
             Value ( String ): 是  标签值 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        List ( Array of List ): 当前页产品列表 
        Page ( Long ): 页码，默认为1 
        Size ( Long ): 每页条数，默认为10 
        Total ( Long ): 总条数 
       "字段"： List
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        CategoryID ( String ): 品类ID 
        CategoryKey ( String ): 所属品类Key 
        CategoryName ( String ): 所属品类名称 
        Description ( String ): 产品描述 长度限制小于128个字符 
        DeviceNodeType ( String ): 节点类型，直连设备-Device、网关设备-Gateway、网关子设备-SubDevice 
        ID ( String ): 产品唯一标示，productKey 
        InstanceID ( String ): 实例ID 
        IsStandard ( Boolean ): 是否是标准品类，true-标准品类，false-自定义 
        Name ( String ): 名称，支持中文、英文字母、数字、和特殊字符_-@()，长度限制不超过32个字符 
        NetConnectType ( String ): 连网方式，Wi-Fi、蜂窝(2G/3G/4G/5G)、以太网、LoRaWAN;Wi-Fi/Cellular/Ethernet/LoRaWAN 
        SupportDynamicRegister ( Boolean ): 是否支持动态注册 
        ThingmodelDataType ( String ): 数据格式，标准数据格式、自定义，暂时只支持标准数据格式；Standard/Custom 
        UpdateTime ( String ): 最近更新时间 
    """,
    "get_product_detail": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             InstanceID ( String ): 是  实例ID 
             ProductKey ( String ): 是  产品标识 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AccountID ( Long ): 账户ID 
        CategoryID ( String ): 品类ID 
        CategoryKey ( String ): 所属品类Key 
        CategoryName ( String ): 所属品类名称 
        CreateTime ( String ): 创建时间 
        Description ( String ): 产品描述 长度限制小于128个字符 
        DeviceNodeType ( String ): 节点类型，直连设备-Device、网关设备-Gateway、网关子设备-SubDevice 
        ID ( String ): 产品唯一标示，productKey 
        InstanceID ( String ): 实例ID 
        IsStandard ( Boolean ): 是否是标准品类，true-标准品类，false-自定义 
        Name ( String ): 名称，支持中文、英文字母、数字、和特殊字符_-@()，长度限制不超过32个字符 
        NetConnectType ( String ): 连网方式，Wi-Fi、蜂窝(2G/3G/4G/5G)、以太网、LoRaWAN;Wi-Fi/Cellular/Ethernet/LoRaWAN 
        Secret ( String ): 产品密钥，productSecret 
        SupportDynamicRegister ( Boolean ): 是否支持动态注册 
        ThingmodelDataType ( String ): 数据格式，标准数据格式、自定义，暂时只支持标准数据格式；Standard/Custom 
        UpdateTime ( String ): 最近更新时间 
    """,
    "get_property_values_by_time": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             AggregateType ( String ): 否  AggregateType 聚合方式，支持Mean平均值/Sum求和/Max最大值/Min最小值/First第一个值/Last最后一个值，默认为Mean 
             DeviceName ( String ): 是  设备名称 
             EndTime ( Long ): 否  结束时间时间，默认为当前时间，单位为毫秒 
             Identifier ( String ): 是  属性标示 
             InstanceID ( String ): 是  实例ID 
             ModuleKey ( String ): 是  模块标示 
             NeedAggregate ( Boolean ): 是  是否需要数据聚合，列表展示场景下全部为false，非数值数据全部为false，只有类型为数值，且展示形式为图表时该字段可以为true 
             ProductKey ( String ): 是  产品标示 
             Size ( Long ): 否  每页条数，默认为20，建议数值类为60，其他类型20，最大允许1000；若选择聚合，则每隔(endTime - startTime) / size ms聚合一次 
             StartTime ( Long ): 否  开始时间,默认为当前时间-1小时，单位为毫秒 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        NextTime ( Long ): 下次查询的起始时间 
        OriginalTotal ( Long ): 原始数据总数，即数据未经聚合时的总数 
        Points ( Array of Points ): 数据点 
        SupportNext ( Boolean ): 是否支持翻页，当没有多余数值或数值型数据以图表展示的情况下，该值为false 
       "字段"： Points
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Time ( Long ): 上报时间戳，单位毫秒 
        Value ( Object of Value ): 值 
    """,
    "get_thing_model": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             InstanceID ( String ): 是  实例ID 
             ProductKey ( String ): 是  产品标识 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        ThingModel ( Array of ThingModel ): 产品物模型列表 
       "字段"： ThingModel
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Description ( String ): 模块描述 
        Events ( Array of Events ): 事件 
        Key ( String ): 唯一标示，支持英文大小写字母、数字和下划线，不超过 32 个字符 
        Name ( String ): 模块名称，默认名称为"默认模块"，支持中文、英文字母、数字和下划线，长度限制 4～32 个字符，中文算 1 个字符 
        Properties ( Array of Properties ): 属性 
        Services ( Array of Services ): 服务 
       "字段"： Events
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Description ( String ): 描述 长度限制小于128个字符 
        Identifier ( String ): 标识符 支持英文大小写字母、数字和下划线，不超过 32 个字符，不支持修改 
        Name ( String ): 名称 长度限制1-32个字符 
        OutputData ( Array of OutputData ): 输出参数 
        Required ( Boolean ): 是否必选，对于标准品类，有些功能是必须拥有的 
        Type ( String ): 事件类型，信息、报警、故障;Info/Alert/Error 
       "字段"： Properties
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AccessMode ( String ): 只读-r 读写-rw 
        Description ( String ): 描述 长度限制小于128个字符 
        Identifier ( String ): 标识符 支持英文大小写字母、数字和下划线，不超过 32 个字符，不支持修改 
        IsOptional ( Boolean ): 是否可选，仅对事件和服务生效，属性默认为可选，true则为可选参数，设备进行事件上报/服务调用时可以忽略此参数值；否则为必选参数，设备事件上报/服务调用时若缺少此参数，则物模型数据校验不通过 
        ModuleKey ( String ): 模块标示 
        Name ( String ): 名称 支持中文、英文字母、数字和下划线，长度限制 4～32 个字符，中文算 1 个字符 
        Required ( Boolean ): 是否必选，对于标准品类，有些功能是必须拥有的 
        ThingmodelDataType ( Object of ThingmodelDataType ):  
       "字段"： Services
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        CallType ( String ): 调用类型，同步/异步;Sync/Async 
        Description ( String ): 描述 长度限制小于128个字符 
        Identifier ( String ): 标识符 支持英文大小写字母、数字和下划线，不超过 32 个字符，不支持修改 
        InputData ( Array of InputData ): 输入参数 
        Name ( String ): 名称 长度限制1-32个字符 
        OutputData ( Array of OutputData ): 输出参数 
        Required ( Boolean ): 是否必选，对于标准品类，有些功能是必须拥有的 
       "字段"： OutputData
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Identifier ( String ): 标识符 支持英文大小写字母、数字和下划线，不超过 32 个字符，不支持修改 
        IsOptional ( Boolean ): 是否可选，仅对事件和服务生效，属性默认为可选，true则为可选参数，设备进行事件上报/服务调用时可以忽略此参数值；否则为必选参数，设备事件上报/服务调用时若缺少此参数，则物模型数据校验不通过 
        Name ( String ): 名称 支持中文、英文字母、数字和下划线，长度限制 4～32 个字符，中文算 1 个字符 
        ThingmodelDataType ( Object of ThingmodelDataType ):  
       "字段"： ThingmodelDataType
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        ThingmodelSpecification ( Object of ThingmodelSpecification ):  
        Type ( String ): 数据类型，支持int、float、double、enum、bool、text、date、struct、array 
       "字段"： InputData
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Identifier ( String ): 标识符 支持英文大小写字母、数字和下划线，不超过 32 个字符，不支持修改 
        IsOptional ( Boolean ): 是否可选，仅对事件和服务生效，属性默认为可选，true则为可选参数，设备进行事件上报/服务调用时可以忽略此参数值；否则为必选参数，设备事件上报/服务调用时若缺少此参数，则物模型数据校验不通过 
        Name ( String ): 名称 支持中文、英文字母、数字和下划线，长度限制 4～32 个字符，中文算 1 个字符 
        ThingmodelDataType ( Object of ThingmodelDataType ):  
       "字段"： ThingmodelSpecification
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        EnumMap ( Object of EnumMap ): 枚举k-v对 (map[int]string) 
        ItemDataType ( String ): 数据类型，支持int、float、double、enum、bool、text、date、struct、array 
        Length ( Long ): 文本长度 
        Max ( Double ): 最大值 
        Min ( Double ): 最小值 
        Size ( Long ): 元素个数 
        Step ( Double ): 步长 
        StructSpec ( Array of StructSpec ): 参数列表(只支持int、float、double、enum、bool、text、date) 
        Unit ( String ): 单位 
        UnitName ( String ): 单位名称 
       "字段"： StructSpec
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Identifier ( String ): 标识符 支持英文大小写字母、数字和下划线，不超过 32 个字符 
        Name ( String ): 名称 支持中文、英文字母、数字和下划线，长度限制 4～32 个字符，中文算 1 个字符 
        ThingmodelDataType ( Object of ThingmodelDataType ):  
    """,
    "set_property": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             DeviceName ( String ): 是  设备名称 
             InstanceID ( String ): 是  实例ID 
             Params ( JSON Map ): 是  属性值，最外层key为ModuleKey，内层key为功能的identifier，value为参数的值 
             ProductKey ( String ): 是  产品标示 
    """,
}
