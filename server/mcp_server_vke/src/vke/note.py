# coding=utf-8
note = {
    "create_cluster": r"""
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Region: (String) 是  集群所属的地域，常见的地域代号示例如下，默认为 cn-beijing：
                   - cn-beijing：华北2（北京）
                   - cn-beijing2：华北3（北京）
                   - cn-datong：华北4（大同）
                   - cn-wulanchabu：华北5（乌兰察布）
                   - cn-shanghai：华东2（上海）
                   - cn-guangzhou：华南1（广州）
                   - cn-hongkong：中国香港
                   - ap-southeast-1：亚太东南（柔佛）
                   - ap-southeast-3：亚太东南（雅加达）
             ClientToken ( String ): 否  用于保证请求幂等性的字符串。该字符串由调用方传入，需保证不同请求之间唯一。ClientToken 对大小写敏感，且最大值不超过 64 个 ASCII 字符。 
             Name ( String ): 是  集群名称。 
                   - 同一个地域下，名称必须唯一。 
                   - 支持大小写英文字母、汉字、数字、短划线（-），长度限制为 2～64 个字符。 
             Description ( String ): 否  集群描述。长度限制为 300 个字符以内。 
             DeleteProtectionEnabled ( Boolean ): 否  集群删除保护，取值： 
                   - false：（默认值）关闭删除保护。 
                   - true：开启删除保护，不允许直接删除集群。 
                   	创建集群后，可以通过调用 UpdateClusterConfig 接口，更改集群的 DeleteProtectionEnabled 配置，再次进行删除；也可以在调用 DeleteCluster 时，配置 Force 参数，选择强制删除集群。 
             ClusterConfig ( Object of ClusterConfigRequest ): 否  集群控制面及节点的网络配置。 
             PodsConfig ( Object of PodsConfigRequest ): 否  集群的容器（Pod）网络配置。 
             ServicesConfig ( Object of ServicesConfigRequest ): 否  集群的服务（Service）网络配置。 
             Tags ( Array of Tag ): 否  自定义的资源标签，用于从不同维度对具有相同特征的集群进行分类、搜索和聚合，能够灵活管理集群。 
                   - Tags 中各个 Key 不可重复。 
                   - 资源已有相同 Tags.Key 的情况下，重复绑定 Tags.Key 不会报错，会更新为最新的 Tags.Value。 
                   - 单个资源最多支持绑定 50 个 Tags。 
                   - Tags 中的 Key、Value 不允许在最前或最后输入空格。 
             KubernetesVersion ( String ): 否  集群的 Kubernetes 版本，格式为x.xx。创建集群时，系统自动匹配该 Kubernetes 版本对应的最新 VKE 版本。 
                   容器服务已发布的 Kubernetes 版本，请参见 Kubernetes 版本发布记录。 
             LoggingConfig ( Object of ClusterLoggingConfigRequest ): 否  集群的日志配置信息。 
             ProjectName ( String ): 否  集群所属项目名称，一个集群只能归属于一个项目。 
                   - 只能包含英文字母、数字、下划线（_）、英文句点（.）和中划线（-）。 
                   - 长度限制在 64 个字符以内。 
                   - 默认值：default。 
             ConnectorConfig ( Object of ClusterConnectorConfigRequest ): 否  注册集群的配置 
             SourceRegion ( String ): 否  集群源地域 
            "字段"： ClusterConfigRequest
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             SubnetIds ( Array of String ): 否  集群控制面在私有网络（VPC）内通信的子网 ID。 
                   可以调用 私有网络API 获取子网 ID。 
                   - 创建集群时，请确保所有指定的 SubnetIds（包括但不限于本参数）属于同一个私有网络。 
                   - 建议您尽量选择不同可用区下的子网来提高集群控制面的高可用性。 
                   - 最多可选择 3 个可用区的子网，每个可用区最多允许添加 2 个子网。 
                   - 子网可用 IP 数至少为 1。 
             ApiServerPublicAccessEnabled ( Boolean ): 否  集群 API Server 公网访问配置，取值： 
                   - false：（默认值）关闭 
                   - true：开启 
             ApiServerPublicAccessConfig ( Object of PublicAccessConfigRequest ): 否  集群 API Server 公网访问配置信息。 
                   ApiServerPublicAccessEnabled=true时才生效。 
             ResourcePublicAccessDefaultEnabled ( Boolean ): 否  节点公网访问配置，取值： 
                   - false：（默认值）不开启公网访问。已有 NAT 网关和规则不受影响。 
                   - true：开启公网访问。开启后，自动为集群专有网络创建 NAT 网关并配置相应规则。 
                   集群创建完成后暂不支持修改该参数，请合理配置。 
            "字段"： PublicAccessConfigRequest
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             PublicAccessNetworkConfig ( Object of EipConfigRequest ): 否  公网访问网络配置。 
                   ApiServerPublicAccessEnabled=true时才需要填写，否则忽略。 
                   集群创建完成后暂不支持修改该参数，请合理配置。 
            "字段"： EipConfigRequest
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             BillingType ( Integer ): 否  公网 IP 的计费类型，取值： 
                   - 3：（默认值）按量计费-按实际流量计费，即指定带宽上限后，将按照实际使用的出公网流量计费，与使用时长无关。 
                   - 2：按量计费-按带宽上限计费，即指定带宽上限后，将按照使用时长计费，与实际流量无关。 
             Bandwidth ( Integer ): 否  公网 IP 的带宽峰值，单位为 Mbps，取值： 
                   - BillingType=2时：取值范围 1 ~ 500，默认值 10。 
                   - BillingType=3时：取值范围 1 ~ 200，默认值 10。 
             Isp ( String ): 否  公网 IP 的线路类型，取值： 
                   BGP：BGP（多线）。 
            "字段"： PodsConfigRequest
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             PodNetworkMode ( String ): 是  容器（Pod）网络模型（CNI），取值： 
                   - Flannel：Flannel 网络模型，独立的 Underlay 容器网络方案，配合私有网络（VPC）的全局路由能力，实现集群高性能的网络体验。 
                   - VpcCniShared：VPC-CNI 网络模型，基于私有网络的弹性网卡 ENI 实现的 Underlay 容器网络方案，具有较高的网络通信性能。 
                   集群创建完成后暂不支持修改该参数，请合理配置。 
             FlannelConfig ( Object of FlannelConfigRequest ): 否  Flannel 网络配置。 
                   PodNetworkMode=Flannel时才能配置，但非必选。 
             VpcCniConfig ( Object of VpcCniConfigRequest ): 否  PC-CNI 网络配置。 
                   PodNetworkMode=VpcCniShared时才能配置，但非必选。 
            "字段"： FlannelConfigRequest
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             PodCidrs ( Array of String ): 是  Flannel 容器网络模型对应的 Pod CIDR。 
                   PodNetworkMode=Flannel时才能配置，但非必选。 
                   - 集群内 Pod 数量受该 CIDR 的 IP 数量限制，集群创建完成后不支持修改，请合理规划 Pod CIDR。 
                   - 不能与以下网段冲突： 
                   	- 同一个集群的 ClusterConfig.SubnetIds 对应的私有网络网段。 
                   	- 同一个集群的 ServiceConfig.ServiceCidrsv4 对应的网段。 
                   	- 同一个私有网络内所有集群的 ServiceConfig.ServiceCidrsv4 对应的网段。 
                   	- 同一个私有网络内不同集群的 FlannelConfig.PodCidrs（本参数）。 
             MaxPodsPerNode ( Integer ): 否  Flannel 模型容器网络的单节点 Pod 实例数量上限，取值： 
                   - 64（默认值） 
                   - 16 
                   - 32 
                   - 128 
                   - 256 
            "字段"： VpcCniConfigRequest
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             SubnetIds ( Array of String ): 是  VPC-CNI 容器网络模型对应的 Pod 子网 ID 列表。 
                   PodNetworkMode=VpcCniShared时才需填写，否则忽略。 
                   可以调用 私有网络API 获取子网 ID。 
                   创建集群时，请确保所有指定的 SubnetIds（包括但不限于本参数）属于同一个私有网络。 
            "字段"： ServicesConfigRequest
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             ServiceCidrsv4 ( Array of String ): 是  集群内服务使用的 CIDR。 
                   - 不能与同一个私有网络内所有集群的 FlannelConfig.PodCidrs.SubnetIds 或 ClusterConfig.SubnetIds 网段冲突。 
                   - 当前仅支持传入一个数组元素，指定多个值时，仅第一个值生效。 
            "字段"： Tag
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Key ( String ): 是  标签键。 
                   - 不能以任何大小写形式的volc:开头。 
                   - 只能包含语言字符、数字、空格和特殊符号_.:/=+-@。 
                   - 长度限制为 1～128 个字符。 
             Value ( String ): 否  标签值，可以为空。 
                   - 只能包含语言字符、数字、空格和特殊符号_.:/=+-@。 
                   - 长度不超过 256 个字符。 
            "字段"： ClusterLoggingConfigRequest
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             LogSetups ( Array of LogSetupRequest ): 否  集群的日志选项信息。 
                   - 空数组代表不开启任何日志。 
                   - 首次开启日志时，日志主题（Log Topic）自动生成。 
                   - 多个日志选项时，LogType 不允许重复。 
             LogProjectId ( String ): 否  集群的日志项目（Log Project）ID。 
                   - 不可以空字符串。 
                   - 创建集群时，若 LogProjectId 不传参数值，表示由系统自动创建新的日志项目。 
                   - 系统自动创建日志项目，按照k8s-log-{clusterId}-{6位随机字符}格式自动生成项目名称。 
                   - 如果 LogSetups.Enabled 字段取值为 false，则不会自动创建日志项目。 
                   - 更新集群配置时，若 LogProjectId 已指定日志项目，则不可更新为空。 
                   - 更新集群配置时，若集群不存在任何日志配置，此时只传了 LogProjectId 且LogSetups 为空时，LogProjectId 将会被忽略。 
                   - 更新 LogProjectId 会为处于开启状态的日志创建新的主题。 
            "字段"： LogSetupRequest
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             LogType ( String ): 是  当前开启的日志类型，取值： 
                   - Audit：集群审计日志 
                   - KubeApiServer：kube-apiserver 组件日志 
                   - KubeScheduler：kube-scheduler 组件日志 
                   - KubeControllerManager：kube-controller-manager 组件日志 
             LogTtl ( Integer ): 否  日志在日志服务中的保存时间，超过指定的日志存储时长后，此日志主题中的过期日志会被自动清除。 
                   - 取值范围：1～3650 
                   - 单位：天 
                   - 默认值：30 天 
                   	指定为 3650 天表示永久存储。 
             Enabled ( Boolean ): 否  是否开启该日志选项，取值： 
                   - false：（默认值）不开启 
                   - true：开启 
                   - 更新集群配置时，若 LogType 为 Audit，则更改 Enabled 会重启 Apiserver。 
                   - 更新集群配置时，若 Enabled 由 false 更换为 true，则会创建新的日志主题。 
            "字段"： ClusterConnectorConfigRequest
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Type ( String ): 是  注册集群的链接类型，取值： 
                       - Direct：直连模式，基于目标集群的KubeConfig的直连模式进行注册并管理； 
                       - Agent：代理模式，基于Agent的方式进行注册并管理 
             Provider ( String ): 是  注册集群的提供商，可选值：VeStack  Vke  Ack  Tke  Cce  Self(失效)  （Kubernetes/None） 
             TargetKubeConfig ( String ): 否  导入集群的对端集群的KubeConfig，需要BASE64编码，长度：0-20480, 只有Type=Direct时才有效，否则会被忽略 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Id ( String ): 集群 ID。 
    """,
    "list_clusters": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Region: (String) 是  集群所属的地域，常见的地域代号示例如下，默认为 cn-beijing：
                   - cn-beijing：华北2（北京）
                   - cn-beijing2：华北3（北京）
                   - cn-datong：华北4（大同）
                   - cn-wulanchabu：华北5（乌兰察布）
                   - cn-shanghai：华东2（上海）
                   - cn-guangzhou：华南1（广州）
                   - cn-hongkong：中国香港
                   - ap-southeast-1：亚太东南（柔佛）
                   - ap-southeast-3：亚太东南（雅加达） 
             Filter ( Object of ListClustersFilter ): 否  待查询集群的筛选条件。 
             Tags ( Array of ListTagFilter ): 否  基于标签查询集群列表。 
                   - Tags 中各个 Key 不可重复。 
                   - Tags 中的 Key、Value 不允许在最前或最后输入空格。 
                   - 单次最多支持 10 个标签。 
             PageNumber ( Integer ): 否  分页查询时的起始页码，从 1 开始，默认为 1。 
             PageSize ( Integer ): 否  分页查询时每页显示的记录数，取值： 
                   - 最小值：1 
                   - 最大值：100 
                   - 默认值：10 
             ProjectName ( String ): 否  项目名称，即按照集群所属的项目筛选查询集群。 
            "字段"： ListClustersFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Ids ( Array of String ): 否  集群 ID 列表。 
                   单次最多填写 100 个 ID。 
                   此参数为空数组时，筛选您本账号下公共参数中指定地域的所有集群。 
             Name ( String ): 否  集群名称。 
             DeleteProtectionEnabled ( Boolean ): 否  集群删除保护，取值： 
                   - true：开启 
                   - false：关闭 
             PodsConfig.PodNetworkMode ( String ): 否  容器（Pod）网络模型（CNI），取值： 
                   - Flannel：Flannel 网络模型，独立的 Underlay 容器网络方案，配合 VPC 的全局路由能力，实现集群高性能的网络体验。 
                   - VpcCniShared：VPC-CNI 网络模型，基于私有网络的弹性网卡 ENI 实现的 Underlay 容器网络方案，具有较高的网络通信性能。 
             Statuses ( Array of ClusterStatusFilter ): 否  需要筛选的集群状态数组。 
                   数组各个元素间是逻辑「或」关系。单次最多填写 15 个状态数组元素。 
             CreateClientToken ( String ): 否  创建集群成功时的 ClientToken。 
                   ClientToken 是保证请求幂等性的字符串。该字符串由调用方传入。 
             UpdateClientToken ( String ): 否  最后一次更新集群成功时的 ClientToken。 
                   ClientToken 是保证请求幂等性的字符串。该字符串由调用方传入。 
            "字段"： ClusterStatusFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Phase ( String ): 否  集群的状态，取值： 
                   - Creating 
                   - Running 
                   - Updating 
                   - Deleting 
                   - Stopped 
                   - Failed 
                   Phase 和 Conditions.Type 两者至少有一个参数必填，否则为无效数组元素。合法的 Phase 和 Conditions.Type 组合，请参见 资源状态说明。 
             Conditions.Type ( String ): 否  集群当前主状态下的状态条件，即进入该主状态的原因，可以有多个原因，取值： 
                   - Progressing 
                   - Ok 
                   - Balance 
                   - CreateError 
                   - ResourceCleanupFailed 
                   - Unknown 
                   Phase 和 Conditions.Type 两者至少有一个参数必填，否则为无效数组元素。合法的 Phase 和 Conditions.Type 组合，请参见 资源状态说明。 
            "字段"： ListTagFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Key ( String ): 是  标签键。 
                   - 不能以任何大小写形式的volc:开头。 
                   - 只能包含语言字符、数字、空格和特殊符号_.:/=+-@。 
                   - 长度限制为 1～128 个字符。 
             Value ( String ): 否  标签值，可以为空。 
                   - 只能包含语言字符、数字、空格和特殊符号_.:/=+-@。 
                   - 长度不超过 256 个字符。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Items ( Array of ClusterResponse ): 集群的详细信息列表。 
        PageNumber ( Integer ): 当前页码。 
        PageSize ( Integer ): 每页显示的集群数。 
        TotalCount ( Integer ): 符合条件的集群总数。 
       "字段"： ClusterResponse
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Id ( String ): 集群 ID。 
        CreateClientToken ( String ): 创建成功时的 ClientToken。 ClientToken 是保证请求幂等性的字符串。该字符串由调用方传入。 
        UpdateClientToken ( String ): 最后一次更新成功时 ClientToken。 ClientToken 是保证请求幂等性的字符串。该字符串由调用方传入。 
        CreateTime ( String ): 集群创建时间。 
            标准 RFC3339 格式的 UTC+0 时间。 
        UpdateTime ( String ): 集群最近一次更新的时间。 
            标准 RFC3339 格式的 UTC+0 时间。 
        KubernetesVersion ( String ): 集群对应的 Kubernetes 版本信息。 
        Name ( String ): 集群名称。 
        Description ( String ): 集群描述信息。 
        Status ( Object of ClusterStatus ): 集群状态。 
        DeleteProtectionEnabled ( Boolean ): 集群删除保护，参数值说明： 
            - true：已开启删除保护。 
            - false：已关闭删除保护。 
        ClusterConfig ( Object of ClusterConfigResponse ): 集群控制面及部分节点的网络配置。 
        PodsConfig ( Object of PodsConfigResponse ): Pod 的网络配置。 
        ServicesConfig ( Object of ServicesConfigResponse ): 服务的网络配置。 
        NodeStatistics ( Object of NodeStatistics ): 集群中各主状态下对应的节点数量统计。 
        Tags ( Array of TagResponse ): 集群绑定的标签信息。 
        LoggingConfig ( Object of ClusterLoggingConfigResponse ): 集群的日志配置信息。 
        ProjectName ( String ): 集群所属的项目。 
       "字段"： ClusterStatus
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Phase ( String ): 集群的状态。参数值有： 
            - Creating 
            - Running 
            - Updating 
            - Deleting 
            - Stopped 
            - Failed 
            合法的 Phase 和 Conditions.Type 组合请参见 资源状态说明。 
        Conditions ( Array of ClusterStatusCondition ): 集群当前主状态下的状态条件，即进入该主状态的原因。 
       "字段"： ClusterStatusCondition
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Type ( String ): 集群当前主状态下的状态条件，即进入该主状态的原因，可以有多个原因，参数值有： 
            - Progressing 
            - Ok 
            - Balance 
            - CreateError 
            - ResourceCleanupFailed 
            - Unknown 
            合法的 Phase 和 Conditions.Type 组合请参见 资源状态说明。 
       "字段"： ClusterConfigResponse
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        VpcId ( String ): 集群控制面及部分节点的网络所在的私有网络（VPC）ID。 
        SubnetIds ( Array of String ): 集群控制面在私有网络内通信的子网 ID。 
        SecurityGroupIds ( Array of String ): 集群控制面及节点使用的的安全组。 
        ApiServerPublicAccessEnabled ( Boolean ): 集群 API Server 公网访问配置，参数值说明： 
            - false：未开启 
            - true：已开启 
        ApiServerPublicAccessConfig ( Object of PublicAccessConfigResponse ): 集群 API Server 公网访问配置信息。 
            ApiServerPublicAccessEnable=true时才返回的参数。 
        ResourcePublicAccessDefaultEnabled ( Boolean ): 节点公网访问配置，参数值说明： 
            - false：未开启 
            - true：已开启 
        ApiServerEndpoints ( Object of ClusterApiServerEndpointsResponse ): 集群 API Server 访问的 Endpoint 信息。 
       "字段"： PublicAccessConfigResponse
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        PublicAccessNetworkConfig ( Object of EipConfigResponse ): 公网访问网络配置。 
            ApiServerPublicAccessEnable=true时才返回的参数。 
        AccessSourceIpsv4 ( Array of String ): IPv4 的公网访问白名单。 
            空值代表放通所有网络段（0.0.0.0/0）。 
       "字段"： EipConfigResponse
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        BillingType ( Integer ): 公网 IP 的计费类型： 
            - 2：按量计费-按带宽上限 
            - 3：按量计费-按实际流量 
        Bandwidth ( Integer ): 公网 IP 的带宽峰值，单位：Mbps。 
        Isp ( String ): 公网 IP 的线路类型，参数值说明： BGP：BGP（多线）。 
       "字段"： ClusterApiServerEndpointsResponse
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        PublicIp ( Object of Endpoint ): 集群 API Server 私网的 Endpoint 地址。 
        PrivateIp ( Object of Endpoint ): 集群 API Server 公网的 Endpoint 地址。 
       "字段"： Endpoint
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Ipv4 ( String ): Endpoint 的 IPv4 地址。 
       "字段"： PodsConfigResponse
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        PodNetworkMode ( String ): 容器（Pod）网络模型（CNI），参数值说明： 
            - Flannel：Flannel 网络模型，独立的 Underlay 容器网络模型。 
            - VpcCniShared：VPC-CNI 网络模型，基于私有网络的弹性网卡 ENI 实现的 Underlay 容器网络模型。 
        FlannelConfig ( Object of FlannelConfigResponse ): Flannel 网络配置。 
        VpcCniConfig ( Object of VpcCniConfigResponse ): VPC-CNI 网络配置。 
       "字段"： FlannelConfigResponse
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        PodCidrs ( Array of String ): Flannel 容器网络的 Pod CIDR。 
        MaxPodsPerNode ( Integer ): Flannel 容器网络的单节点 Pod 实例数量上限。 
       "字段"： VpcCniConfigResponse
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        SubnetIds ( Array of String ): VPC-CNI 容器网络模型对应的 Pod 子网 ID 列表。 
       "字段"： ServicesConfigResponse
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        ServiceCidrsv4 ( Array of String ): Kubernetes 服务（Service）暴露的 IPv4 私有网络地址。 
       "字段"： NodeStatistics
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        TotalCount ( Integer ): 节点总数量。 
        CreatingCount ( Integer ): Phase=Creating的节点总数量。 
        RunningCount ( Integer ): Phase=Running的节点总数量。 
        UpdatingCount ( Integer ): Phase=Updating的节点总数量。 
        DeletingCount ( Integer ): Phase=Deleting的节点总数量。 
        FailedCount ( Integer ): Phase=Failed的节点总数量。 
       "字段"： TagResponse
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Key ( String ): 标签键。 
        Value ( String ): 标签值。 
        Type ( String ): 标签类型，参数值说明： 
            - System：  系统标签。 
            - Custom：用户自定义标签。 
       "字段"： ClusterLoggingConfigResponse
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        LogSetups ( Array of LogSetupResponse ): 集群的日志选项信息。 
        LogProjectId ( String ): 集群的日志项目（Log Project）ID。 如果为空，表示集群的日志项目未被创建。 
       "字段"： LogSetupResponse
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        LogType ( String ): 当前开启的日志类型，参数值说明： 
            - Audit：集群审计日志 
            - KubeApiServer：kube-apiserver 组件日志 
            - KubeScheduler：kube-scheduler 组件日志 
            - KubeControllerManager：kube-controller-manager 组件日志 
        LogTtl ( Integer ): 日志在日志服务中的保存时间，单位为天。 3650 天表示永久存储。 
        LogTopicId ( String ): 采集目标的TLS日志主题ID。 如果为空，表示对应日志的主题未被创建。 
        Enabled ( Boolean ): 是否开启该日志选项，参数值说明： 
            - true：已开启 
            - false：未开启 
    """,
    "list_kubeconfigs": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Region: (String) 是  集群所属的地域，常见的地域代号示例如下，默认为 cn-beijing：
                   - cn-beijing：华北2（北京）
                   - cn-beijing2：华北3（北京）
                   - cn-datong：华北4（大同）
                   - cn-wulanchabu：华北5（乌兰察布）
                   - cn-shanghai：华东2（上海）
                   - cn-guangzhou：华南1（广州）
                   - cn-hongkong：中国香港
                   - ap-southeast-1：亚太东南（柔佛）
                   - ap-southeast-3：亚太东南（雅加达）
             PageNumber ( Integer ): 否  分页查询时的起始页码，从 1 开始，默认为 1。 
             PageSize ( Integer ): 否  分页查询时每页显示的记录数，取值： 
                   - 最小值：1 
                   - 最大值：100 
                   - 默认值：10 
             Filter ( Object of ListKubeconfigsFilter ): 否  待查询 Kubeconfig 的筛选条件。 
            "字段"： ListKubeconfigsFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             ClusterIds ( Array of String ): 否  集群 ID。 
                   可以调用 ListClusters 接口，获取集群 ID。 
                   - 单次最多填写 100 个集群 ID。 
                   - 此参数为空数组时，基于账号下指定地域的所有集群进行筛选。 
             Ids ( Array of String ): 否  Kubeconfig ID。 
                   在 容器服务控制台 的 集群 页面，单击目标集群名称后，在集群的 基本信息 页面 连接信息 页签获取 Kubeconfig ID，也可以查看调用 CreateKubeconfig 接口后保存的 Kubeconfig ID 信息。 
             UserIds ( Array of Long ): 否  用户 ID。 
                   可以调用 获取用户详情 接口，获取用户 ID。 
                   - 若不传入用户 ID，则由系统判断接口调用者的权限并返回对应的 Kubeconfig 信息： 
                   	- 调用者具有火山引擎账号（主账号）权限：返回火山引擎账号及其下子用户的所有 Kubeconfig 信息。 
                   	- 调用者具有子用户权限：仅返回该子用户下的 Kubeconfig 信息。 
                   - 单次最多填写 20 个用户 ID。 
             RoleIds ( Array of Long ): 否  角色 ID。 
                   可以调用 获取角色详情 接口，获取角色 ID。 
                   - 若不传入角色 ID，则由系统判断接口调用者的权限并返回对应的 Kubeconfig 信息： 
                   	- 调用者具有火山引擎账号（主账号）权限：返回火山引擎账号及其下角色的所有 Kubeconfig 信息。 
                   	- 调用者具有角色权限：仅返回该角色下的 Kubeconfig 信息。 
                   - 单次最多填写 20 个角色 ID。 
             Types ( Array of String ): 否  集群 Kubeconfig 文件类型，取值： 
                   - Private：私网访问类型的 Kubeconfig 文件。 
                   - Public：公网访问类型的 Kubeconfig 文件。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Items ( Array of KubeconfigResponse ): Kubeconfig 的详细信息列表。 
        PageNumber ( Integer ): 当前页码。 
        PageSize ( Integer ): 每页显示的 Kubeconfig 信息条数。 
        TotalCount ( Integer ): 符合条件的 Kubeconfig 总数。 
       "字段"： KubeconfigResponse
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Id ( String ): Kubeconfig ID。 
        UserId ( Long ): 用户 ID。 
        ClusterId ( String ): 集群 ID。 
        Type ( String ): 集群 Kubeconfig 文件类型，参数值有： 
            - Private：私网访问类型的 Kubeconfig 文件。 
            - Public：公网访问类型的 Kubeconfig 文件。 
        CreateTime ( String ): Kubeconfig 生成时间。 
            标准 RFC3339 格式的 UTC+0 时间。 
        ExpireTime ( String ): Kubeconfig 到期时间。 
            标准 RFC3339 格式的 UTC+0 时间。 
        Kubeconfig ( String ): Kubeconfig 文本。以 Base64 编码返回。 
            如果Type=Public但ClusterIds中指定的集群的ClusterConfig.ApiServerPublicAccessEnabled=false，则此处返回为空。 
        RoleId ( Long ): 角色 ID。 
    """,
    "create_kubeconfig": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Region: (String) 是  集群所属的地域，常见的地域代号示例如下，默认为 cn-beijing：
                   - cn-beijing：华北2（北京）
                   - cn-beijing2：华北3（北京）
                   - cn-datong：华北4（大同）
                   - cn-wulanchabu：华北5（乌兰察布）
                   - cn-shanghai：华东2（上海）
                   - cn-guangzhou：华南1（广州）
                   - cn-hongkong：中国香港
                   - ap-southeast-1：亚太东南（柔佛）
                   - ap-southeast-3：亚太东南（雅加达）
             ClusterId ( String ): 是  集群 ID。 
                   可以调用 ListClusters 接口，获取集群 ID。 
                   集群必须处于{Running,Ok]}或{Updating,[Progressing]}状态。可调用 [ListClusters] 接口获取集群当前的状态。 
             Type ( String ): 是  集群 Kubeconfig 文件类型，取值： 
                   - Private：私网访问类型的 Kubeconfig。 
                   - Public：公网访问类型的 Kubeconfig。 
             ValidDuration ( Integer ): 否  Kubeconfig 文件有效期。 
                   - 取值范围：1～867240。 
                   - 单位：小时。 
                   - 默认值：26280（3年）。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Id ( String ): Kubeconfig ID。 
            建议您妥善保存 Kubeconfig ID 信息，以备后续使用。 
    """,
    "list_supported_resource_types": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Region: (String) 是  集群所属的地域，常见的地域代号示例如下，默认为 cn-beijing：
                   - cn-beijing：华北2（北京）
                   - cn-beijing2：华北3（北京）
                   - cn-datong：华北4（大同）
                   - cn-wulanchabu：华北5（乌兰察布）
                   - cn-shanghai：华东2（上海）
                   - cn-guangzhou：华南1（广州）
                   - cn-hongkong：中国香港
                   - ap-southeast-1：亚太东南（柔佛）
                   - ap-southeast-3：亚太东南（雅加达）
             Filter ( Object of SupportedResourceTypesFilter ): 否  要是查询的资源类型筛选条件。 
             PageNumber ( Integer ): 否  分页查询时的起始页码，从 1 开始，默认为 1。 
             PageSize ( Integer ): 否  分页查询时每页显示的记录数，取值： 
                   - 最小值：1 
                   - 最大值：100 
                   - 默认值：10 
            "字段"： SupportedResourceTypesFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             ZoneIds ( Array of String ): 否  可用区 ID 列表。 
                   请参见 地域和可用区，获取可用区 ID（ZoneID）。 
                   不传参数值时返回指定 Region 下所有可用区下的资源信息。 
             ResourceTypes ( Array of String ): 否  返回的资源类型，目前支持两种资源类型： 
                   - Ecs：云服务器（ECS）资源。 
                   - Zone：可用区类型资源。 
                   不传参数值时，返回容器服务支持的所有资源类型。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Items ( Array of SupportedResourceTypeResponse ): 支持的资源类型及规格的列表。 
        PageNumber ( Integer ): 当前页码。 
        PageSize ( Integer ): 每页显示的数据条数。 
        TotalCount ( Integer ): 符合条件的数据总数。 
       "字段"： SupportedResourceTypeResponse
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        ResourceScope ( String ): 资源所属范围，参数值说明： 
            - Zone：可用区。 
            - Region：地域。 
        ZoneId ( String ): 资源所支持的具体可用区 ID。 
        ResourceType ( String ): 资源类型，参数值说明： 
            - Ecs：云服务器（ECS）资源。 
            - Zone：可用区资源。 
        ResourceSpecifications ( Array of String ): 资源的对应规格列表。 
            当前仅支持云服务器类型的资源。云服务器规格说明，请参见 DescribeInstanceTypes 接口中的 InstanceTypeId 参数说明。 
    """,
    "list_supported_addons": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Region: (String) 是  集群所属的地域，常见的地域代号示例如下，默认为 cn-beijing：
                   - cn-beijing：华北2（北京）
                   - cn-beijing2：华北3（北京）
                   - cn-datong：华北4（大同）
                   - cn-wulanchabu：华北5（乌兰察布）
                   - cn-shanghai：华东2（上海）
                   - cn-guangzhou：华南1（广州）
                   - cn-hongkong：中国香港
                   - ap-southeast-1：亚太东南（柔佛）
                   - ap-southeast-3：亚太东南（雅加达）
             Filter ( Object of ListSupportedAddonsFilter ): 否  查询组件的过滤条件。 
            "字段"： ListSupportedAddonsFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Name ( String ): 否  待查询组件的名称。 
             PodNetworkModes ( Array of String ): 否  组件支持的容器（Pod）网络模型（CNI），取值： 
                   - Flannel：Flannel 网络模型，独立的 Underlay 容器网络方案，配合私有网络（VPC）的全局路由能力，实现集群高性能的网络体验。 
                   - VpcCniShared：VPC-CNI 网络模型，基于私有网络的弹性网卡 ENI 实现的 Underlay 容器网络方案，具有较高的网络通信性能。 
             DeployModes ( Array of String ): 否  支持的部署模式，取值： 
                   - Unmanaged：获取非托管模式部署的组件。 
                   - Managed：获取托管模式部署的组件。 
                   - 为空：获取全部部署模式的组件。 
             DeployNodeTypes ( Array of String ): 否  部署节点类型。仅DeployMode=Unmanaged时，才需要指定。取值： 
                   - Node：获取以节点（云服务器）方式部署的组件。 
                   - VirtualNode：获取以虚拟节点（弹性容器实例）方式部署的组件。 
                   - 为空：获取全部部署节点类型的组件。 
             Necessaries ( Array of String ): 否  组件的安装必要性，取值： 
                   - Required：系统必装 
                   - Recommended：推荐安装 
                   - OnDemand：可选安装 
             Categories ( Array of String ): 否  组件的分类，取值： 
                   - Storage：存储 
                   - Network：网络 
                   - Monitor：监控 
                   - Scheduler：调度 
                   - Dns：DNS 
                   - Security：安全 
                   - Gpu：GPU 
                   - Image：镜像 
             Versions.Compatibilities.KubernetesVersions ( Array of String ): 否  组件支持的 Kubernetes 版本。容器服务发布 Kubernetes 版本，请参见 Kubernetes 版本发布记录。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Items ( Array of SupportedAddon ): 容器服务支持的组件的详细信息。 
        TotalCount ( Integer ): 容器服务支持的组件总数。 
       "字段"： SupportedAddon
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Name ( String ): 组件名称。 
        Versions ( Array of AddonVersion ): 组件支持的版本。 
        PodNetworkModes ( Array of String ): 组件的容器（Pod）网络模型（CNI），参数值有： 
            - Flannel：Flannel 网络模型，独立的 Underlay 容器网络模型。 
            - VpcCniShared：VPC-CNI 网络模型，基于私有网络的弹性网卡 ENI 实现的 Underlay 容器网络模型。 
        DeployMode ( String ): 组件部署模式，参数值有： 
            - Unmanaged：非托管模式部署。 
            - Managed：托管模式部署。 
        DeployNodeTypes ( Array of String ): 部署节点的类型，参数值有： 
            - Node：以节点方（云服务器）式部署。 
            - VirtualNode：以虚拟节点（弹性容器实例）方式部署。 
            	仅DeployModes=Unmanaged时，才返回该参数。 
        Necessary ( String ): 组件的安装必要性，参数值有： 
            - Required：系统必装 
            - Recommended：推荐安装 
            - OnDemand：可选安装 
        Categories ( Array of String ): 组件的分类，参数值有： 
            - Network：网络 
            - Monitor：监控 
            - Scheduler：调度 
            - Dns：DNS 
            - Security：安全 
            - Gpu：GPU 
            - Image：镜像 
            - 为空：返回空数组，表示该组件没有分类。 
       "字段"： AddonVersion
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        CompatibleVersions ( Array of String ): 可以兼容升级到当前版本的低版本列表。 
    """,
    "create_addon": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Region: (String) 是  集群所属的地域，常见的地域代号示例如下，默认为 cn-beijing：
                   - cn-beijing：华北2（北京）
                   - cn-beijing2：华北3（北京）
                   - cn-datong：华北4（大同）
                   - cn-wulanchabu：华北5（乌兰察布）
                   - cn-shanghai：华东2（上海）
                   - cn-guangzhou：华南1（广州）
                   - cn-hongkong：中国香港
                   - ap-southeast-1：亚太东南（柔佛）
                   - ap-southeast-3：亚太东南（雅加达）
             ClusterId ( String ): 是  待安装组件的集群 ID。 
                   可以调用 ListClusters 接口，获取集群 ID。 
                   待安装组件的集群必须处于{Running,*]}状态。可调用 [ListClusters] 接口获取集群当前的状态。 
             Name ( String ): 是  待安装组件的名称。 
                   容器服务当前支持的组件名称，请调用 ListSupportedAddons获取。 
                   可以调用 ListSupportedAddons接口，获取待安装组件的版本。 
             DeployMode ( String ): 否  部署模式，取值： 
                   * Unmanaged：非托管模式部署。 
                   * Managed：托管模式部署。 
                      可以调用 ListSupportedAddons 接口，获取待安装组件的托管模式。 
                   若不传入参数值，当组件支持托管时，此处系统默认为 Managed；当组件不支持托管时，此处系统默认为 Unmanaged。 
             DeployNodeType ( String ): 否  部署节点类型。仅DeployModes=Unmanaged时，才需要指定该参数。取值： 
                   * Node：以节点（云服务器）方式部署。 
                   * VirtualNode：以虚拟节点（弹性容器实例）方式部署。 
                   若目标当前集群已安装了 vci-virtual-kubelet 组件，则此处默认值为 VirtualNode，否则默认值为 Node。 
                   请调用 ListAddons 接口，获取当前集群已安装的组件。 
             Config ( String ): 否  组件配置。详细配置说明，请参见下方 组件配置信息。 
                   仅 组件配置信息 中列出的组件需要配置该参数。其余组件无需配置。 
             Version ( String ): 否  待更新组件的版本。 
                   可以调用 [ListSupportedAddons] 接口获取组件版本。 
             ClientToken ( String ): 否  用于保证请求幂等性的字符串。该字符串由调用方传入，需保证不同请求之间唯一。ClientToken 对大小写敏感，且最大值不超过 64 个 ASCII 字符。 
    """,
    "update_addon_config": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Region: (String) 是  集群所属的地域，常见的地域代号示例如下，默认为 cn-beijing：
                   - cn-beijing：华北2（北京）
                   - cn-beijing2：华北3（北京）
                   - cn-datong：华北4（大同）
                   - cn-wulanchabu：华北5（乌兰察布）
                   - cn-shanghai：华东2（上海）
                   - cn-guangzhou：华南1（广州）
                   - cn-hongkong：中国香港
                   - ap-southeast-1：亚太东南（柔佛）
                   - ap-southeast-3：亚太东南（雅加达）
             ClusterId ( String ): 是  待更新组件所属集群的 ID。 
                   可以调用 ListClusters 接口，获取集群 ID。 
                   集群必须处于{Running,*]}状态。可调用 [ListClusters] 接口获取集群当前的状态。 
             Name ( String ): 是  待更新组件的名称。 
                   可以调用 ListAddons 接口获取组件名称。 
                   - 仅个别组件支持更新组件配置信息，包括：cr-credential-controller、apmplus-opentelemetry-collector、cluster-autoscaler、ingress-nginx、p2p-accelerator。 
                   - 组件必须处于{Running, ]}或除{Failed, [ResourceCleanupFailed]}、{Failed, [ClusterNotRunning]}以外的{Failed, []}状态。可调用 [ListAddons] 接口获取组件当前状态。 
             Config ( String ): 否  组件配置。 
                   详细说明，请参见 组件配置信息。 
             Version ( String ): 否  待更新组件的版本。 
                   可以调用 [ListSupportedAddons] 接口获取组件版本。 
             ClientToken ( String ): 否  用于保证请求幂等性的字符串。该字符串由调用方传入，需保证不同请求之间唯一。ClientToken 对大小写敏感，且最大值不超过 64 个 ASCII 字符。 
    """,
    "list_addons": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Region: (String) 是  集群所属的地域，常见的地域代号示例如下，默认为 cn-beijing：
                   - cn-beijing：华北2（北京）
                   - cn-beijing2：华北3（北京）
                   - cn-datong：华北4（大同）
                   - cn-wulanchabu：华北5（乌兰察布）
                   - cn-shanghai：华东2（上海）
                   - cn-guangzhou：华南1（广州）
                   - cn-hongkong：中国香港
                   - ap-southeast-1：亚太东南（柔佛）
                   - ap-southeast-3：亚太东南（雅加达）
             Filter ( Object of ListAddonsFilter ): 否  待查询组件的筛选条件。 
             PageNumber ( Integer ): 否  分页查询时的起始页码，从 1 开始，默认为 1。 
             PageSize ( Integer ): 否  分页查询时每页显示的记录数，取值： 
                   - 最小值：1 
                   - 最大值：100 
                   - 默认值：10 
            "字段"： ListAddonsFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             ClusterIds ( Array of String ): 否  集群 ID 列表。 
                   可以调用 ListClusters 接口，获取集群 ID。单次最多填写 100 个集群 ID。 
                   此参数为空数组时，基于账号下指定地域的所有集群进行筛选。 
             Names ( Array of String ): 否  组件名称列表。 
                   可以调用 ListSupportedAddons 接口，获取集群组件名称。单次最多填写 100 个组件名称。 
                   此参数为空数组时，基于指定集群下的所有组件进行筛选。 
             DeployModes ( Array of String ): 否  支持的部署模式，取值： 
                   - Unmanaged：查询非托管模式部署的组件。 
                   - Managed：查询托管模式部署的组件。 
                   - 为空：查询全部部署模式的组件。 
             DeployNodeTypes ( Array of String ): 否  部署节点类型。仅DeployMode=Unmanaged时，才需要指定。取值： 
                   - Node：查询以节点（云服务器）方式部署的组件。 
                   - VirtualNode：查询以虚拟节点（弹性容器实例）方式部署的组件。 
                   - 为空：查询全部部署节点类型的组件。 
             Statuses ( Array of AddonStatusFilter ): 否  组件状态。 
                   单次最多填写 15 个数组元素。传入多个状态时，状态间是逻辑「或」关系。 
             CreateClientToken ( String ): 否  创建成功时的 ClientToken。 ClientToken 是保证请求幂等性的字符串。该字符串由调用方传入。 
             UpdateClientToken ( String ): 否  按更新幂等token过滤，精确查询 
                   最后一次更新成功时 ClientToken。 ClientToken 是保证请求幂等性的字符串。该字符串由调用方传入。 
            "字段"： AddonStatusFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Phase ( String ): 否  组件的状态，取值： 
                   - Running 
                   - Failed 
                   - Creating 
                   - Deleting 
                   - Updating 
                   Phase 和 Conditions.Type 两者至少有一个参数必填，否则为无效数组元素。合法的 Phase 和 Conditions.Type 组合请参见 资源状态说明。 
             Conditions.Type ( String ): 否  组件当前主状态下的状态条件，即进入该主状态的原因，可以有多个原因，取值： 
                   - Unknown 
                   - ClusterNotRunning 
                   - CrashLoopBackOff 
                   - ImagePullBackOff 
                   - SchedulingFailed 
                   - NameConflict 
                   - ResourceCleanupFailed 
                   - ClusterVersionUpgrading 
                   - Ok 
                   - Degraded 
                   - Progressing 
                   Phase 和 Conditions.Type 两者至少有一个参数必填，否则为无效数组元素。合法的 Phase 和 Conditions.Type 组合请参见 资源状态说明。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Items ( Array of Addon ): 组件列表。 
        PageNumber ( Integer ): 当前页码。 
        PageSize ( Integer ): 每页显示的组件数。 
        TotalCount ( Integer ): 符合条件的组件总数。 
       "字段"： Addon
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        ClusterId ( String ): 组件所在集群 ID。 
        Name ( String ): 组件名称。 
        DeployMode ( String ): 组件部署模式，参数值有： 
            - Unmanaged：非托管模式部署。 
            - Managed：托管模式部署。 
        DeployNodeType ( String ): 部署节点的类型，参数值有： 
            - Node：以节点方式部署。 
            - VirtualNode：以虚拟节点方式部署。 
            	仅DeployModes=Unmanaged时，才返回该参数。 
        Config ( String ): 组件配置。详细的参数说明，请参见 组件配置信息。 
        CreateTime ( String ): 安装组件的时间。 
            标准 RFC3339 格式的 UTC+0 时间。 
        UpdateTime ( String ): 更新组件的时间。 
            标准 RFC3339 格式的 UTC+0 时间。 
        Status ( Object of AddonStatus ): 组件状态。 
        CreateClientToken ( String ): 创建成功时的 ClientToken。 
        UpdateClientToken ( String ): 最后一次更新成功时的 ClientToken。 
       "字段"： AddonStatus
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Phase ( String ): 组件的状态，参数值有： 
            - Running 
            - Failed 
            - Creating 
            - Deleting 
            - Updating 
            合法的 Phase 和 Conditions.Type 组合说明，请参见 资源状态说明。 
        Conditions ( Array of AddonCondition ): 组件当前主状态下的状态条件，即进入该主状态的原因。 
            合法的 Phase 和 Conditions.Type 组合说明，请参见 资源状态说明。 
       "字段"： AddonCondition
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Type ( String ): 组件当前主状态下的状态条件，即进入该主状态的原因，可以有多个原因，参数值有： 
            - Progressing 
            - ClusterVersionUpgrading 
            - Unknown 
            - Degraded 
            - NameConflict 
            - ClusterNotRunning 
            - CrashLoopBackOff 
            - SchedulingFailed 
            - ResourceCleanupFailed 
    """,
    "update_addon_version": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Region: (String) 是  集群所属的地域，常见的地域代号示例如下，默认为 cn-beijing：
                   - cn-beijing：华北2（北京）
                   - cn-beijing2：华北3（北京）
                   - cn-datong：华北4（大同）
                   - cn-wulanchabu：华北5（乌兰察布）
                   - cn-shanghai：华东2（上海）
                   - cn-guangzhou：华南1（广州）
                   - cn-hongkong：中国香港
                   - ap-southeast-1：亚太东南（柔佛）
                   - ap-southeast-3：亚太东南（雅加达）
             ClusterId ( String ): 是  待更新组件所属集群的 ID。 
                   可以调用 ListClusters 接口，获取集群 ID。 
                   集群必须处于{Running,Ok]}或{Updating, [Progressing]}状态。可调用 [ListClusters] 接口获取集群当前的状态。 
             Name ( String ): 是  待更新组件的名称。 
                   可以调用 ListAddons 接口获取组件名称。 
                   组件必须处于{Running, *]}状态。可调用 [ListAddons] 接口获取组件当前状态。 
                   可以调用 ListSupportedAddons 接口，获取组件的可升级版本。 
             ClientToken ( String ): 否  用于保证请求幂等性的字符串。该字符串由调用方传入，需保证不同请求之间唯一。ClientToken 对大小写敏感，且最大值不超过 64 个 ASCII 字符。 
    """,
    "create_node_pool": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Region: (String) 是  集群所属的地域，常见的地域代号示例如下，默认为 cn-beijing：
                   - cn-beijing：华北2（北京）
                   - cn-beijing2：华北3（北京）
                   - cn-datong：华北4（大同）
                   - cn-wulanchabu：华北5（乌兰察布）
                   - cn-shanghai：华东2（上海）
                   - cn-guangzhou：华南1（广州）
                   - cn-hongkong：中国香港
                   - ap-southeast-1：亚太东南（柔佛）
                   - ap-southeast-3：亚太东南（雅加达）
             ClientToken ( String ): 否  用于保证请求幂等性的字符串。该字符串由调用方传入，需保证不同请求之间唯一。ClientToken 对大小写敏感，且最大值不超过 64 个 ASCII 字符。 
             ClusterId ( String ): 是  节点池所在集群的 ID。 
                   可以调用 ListClusters 接口，获取集群 ID。 
                   集群必须处于{Running,Ok]}或{Updating,[Progressing]}状态。可调用 [ListClusters] 接口获取集群当前的状态。 
             Name ( String ): 是  节点池名称。 
                   - 同一个集群下，节点池名称必须唯一。 
                   - 支持大小写英文字母、汉字、数字、短划线（-），长度限制为 2～64 个字符。 
                   不能使用默认节点池保留名：vke-default-nodepool。 
             KubernetesConfig ( Object of NodePoolKubernetesConfigRequest ): 否  节点池 Kubernetes 相关配置。 
             NodeConfig ( Object of NodePoolNodeConfigRequest ): 是  节点池中云服务器（ECS）实例配置。 
             AutoScaling ( Object of NodePoolAutoScalingRequest ): 否  节点池伸缩策略配置。 
             Tags ( Array of Tag ): 否  自定义的资源标签，用于从不同维度对具有相同特征的节点池进行分类、搜索和聚合，能够灵活管理节点池。 
                   - Tags 中各个 Key 不可重复。 
                   - 资源已有相同 Tags.Key 的情况下，重复绑定 Tags.Key 不会报错，会更新为最新的 Tags.Value。 
                   - 单个资源最多支持绑定 50 个 Tags。 
                   - Tags 中的 Key、Value 不允许在最前或最后输入空格。 
            "字段"： NodePoolKubernetesConfigRequest
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Labels ( Array of Label ): 否  节点池/节点的 Kubernetes 标签（Labels）信息。最多可传入 20 个标签。 
                   节点池会统一管理节点的标签配置信息，因此标签信息会同步到节点池内的所有节点上。当标签发生变更时，会覆盖原有的标签配置信息。 
             Taints ( Array of Taint ): 否  节点池/节点的 Kubernetes 污点（Taints）信息。最多可传入 20 个污点。 
                   节点池会统一管理节点的污点配置信息，因此污点信息会同步到节点池内的所有节点上。当污点发生变更时，会覆盖原有的污点配置信息。 
             Cordon ( Boolean ): 否  封锁节点配置，取值： 
                   - false：（默认值）不封锁 
                   - true：封锁 
                   更新节点池（UpdateNodePoolConfig）时，若不传入参数值，则保持原有参数配置。 
             NamePrefix ( String ): 否  Kubernetes 中节点对象的元数据名称前缀。默认不启用，若设置表示启用，并将影响 Kubernetes Node Manifest 文件中展示的metadata.name前缀信息。前缀校验规则如下： 
                   - 支持英文小写字母、数字、中划线(-)和半角句号(.)。 
                   - 只能以英文小写字母或者数字开头。 
                   - 长度限制为 1~48 个字符。 
             KubeletConfig ( Object of NodePoolKubeletConfig ): 否  节点池中节点的 kubelet 自定义参数配置，用于调整节点行为。 
             AutoSyncDisabled ( Boolean ): 否  是否禁用自动同步标签污点到存量节点的功能，取值： 
                   - true：禁用，即关闭自动同步。 
                   - false：（默认值）不禁用，即开启自动同步。 
            "字段"： Label
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Key ( String ): 是  标签键，要求如下，更多规则，请参见 Kubernetes 标签规则。 
                   有效的标签键有两个段：和，用斜杠（/）分隔。 
                   - 是必须的，支持英文大小写字母、数字、短划线（-）、下划线（_）、英文句号（ .），以字母或数字开头和结尾，长度不超过 63 个字符。 
                   - 是可选的。如果指定，则必须是 DNS 子域：由英文句号（.）分隔的一系列 DNS 标签，长度不超过 253 个字符。 
                   - 和总长度不超过 82 个字符。 
             Value ( String ): 否  标签值，要求如下，更多规则，请参见 Kubernetes 标签规则。 
                   - 长度不超过 63 个字符（可以为空）。 
                   - 支持以英文大小写字母、数字开头和结尾。 
                   - 支持特殊字符：短划线（-）、下划线（_）、英文句号（.）。 
            "字段"： Taint
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Effect ( String ): 否  污点效果，取值： 
                   - NoSchedule：（默认值）不调度。 
                   - NoExecute：驱逐没有容忍污点的 Pod。 
                   - PreferNoSchedule：尽量避免调度。 
             Key ( String ): 是  污点键，要求如下，更多规则，请参见 Kubernetes 标签规则。 
                   有效的污点键有两个段：和，用斜杠（/）分隔。 
                   - 是必须的，支持英文大小写字母、数字、短划线（-）、下划线（_）、英文句号（ .），以字母或数字开头和结尾，长度不超过 63 个字符。 
                   - 是可选的。如果指定，则必须是 DNS 子域：由英文句号（.）分隔的一系列 DNS 标签，长度不超过 253 个字符。 
                   - 和总长度不超过 82 个字符。 
             Value ( String ): 否  污点值，要求如下，更多规则，请参见 Kubernetes 标签规则。 
                   - 长度不超过 63 个字符（可以为空）。 
                   - 支持以英文大小写字母、数字开头和结尾。 
                   - 支持特殊字符：短划线（-）、下划线（_）、英文句号（.）。 
            "字段"： NodePoolKubeletConfig
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             FeatureGates ( Object of FeatureGates ): 否  特性门控，即描述 Kubernetes 特性的一组键值对。 
                   该特性门控仅支持在 Kubernetes v1.26 及以下版本的集群中使用。 
             TopologyManagerScope ( String ): 否  拓扑管理策略的资源粒度，取值： 
                   - container：表示资源对齐粒度为容器级。 
             TopologyManagerPolicy ( String ): 否  拓扑管理策略，取值： 
                   - none：（默认）禁用拓扑管理策略。 
                   - restricted：kubelet 仅接受在所请求资源上实现最佳 NUMA（Non-Uniform Memory Access，非一致存储访问结构）的 Pod。 
                   - best-effort：kubelet 会优先选择在 CPU 和设备资源上实现 NUMA 的 Pod。 
                   - single-numa-node：kubelet 仅允许在同一个节点的 CPU 和设备资源上实现 NUMA 的 Pod。 
             KubeApiQps ( Integer ): 否  与 APIServer 通信的每秒查询个数。 
                   - 整数形式，取值范围为 1～50。 
                   - 默认值为 5。 
             KubeApiBurst ( Integer ): 否  每秒发送到 APIServer 的突发请求数量上限。 
                   - 整数形式，取值范围为 1～100。 
                   - 默认值为 10。 
                   该值必须大于等于KubeApiQps参数的值。 
             EvictionHard ( Array of EvictionHard ): 否  触发 Pod 驱逐操作的一组硬性门限。详细参数解释，请参见 官方文档。 
                   如果希望显式地禁用，可以在任意资源上将其阈值设置为 0% 或 100%。 
                   默认值如下： 
                   - memory.available: "100Mi" 
                   - nodefs.available: "10%" 
                   - nodefs.inodesFree: "5%" 
                   - imagefs.available: "15%" 
             RegistryPullQps ( Integer ): 否  集群从镜像仓库拉取镜像的 QPS 阈值。 
                   - 整数形式，取值范围为 1～50。 
                   - 默认值为 2。 
             RegistryBurst ( Integer ): 否  集群从镜像仓库拉取镜像的突发阈值。 
                   - 整数形式，取值范围为 1～100。 
                   - 默认值为 5。 
                   仅当RegistryPullQps大于 0 时需要配置，且取值必须大于等于RegistryPullQps参数的值。 
             SerializeImagePulls ( Boolean ): 否  是否串行拉取镜像，取值： 
                   - true：串行拉取镜像。 
                   - false：（默认）并行拉取镜像，能够提高 Pod 启动速度。 
            "字段"： FeatureGates
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             QoSResourceManager ( Boolean ): 否  是否启用 QoS 资源管理器，用于支持微拓扑调度。取值： 
                   - true：启用 QoS 资源管理器。 
                   - false：（默认）不启用 QoS 资源管理器。 
            "字段"： EvictionHard
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Key ( String ): 是  硬性门限名称。取值： 
                   - memory.available 
                   - nodefs.available 
                   - nodefs.inodesFree 
                   - imagefs.available 
             Value ( String ): 是  硬性门限值。 
            "字段"： NodePoolNodeConfigRequest
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             InstanceTypeIds ( Array of String ): 是  节点对应的 ECS 实例规格 ID 列表。 
                   调用 ListSupportedResourceTypes 接口查询集群实例所支持的资源类型和范围。 
                   当前仅支持传入一个数组元素。 
             SubnetIds ( Array of String ): 是  节点网络所属的子网 ID 列表。 
                   可以调用 私有网络 API 获取子网 ID。 
                   - 必须与集群处于同一个私有网络内。 
                   - 单个节点池最多支持关联 8 个子网 ID。 
             ImageId ( String ): 否  节点对应的 ECS 实例使用的镜像 ID。 
                   不同的镜像类型对应的镜像 ID 也不同，详细说明，请参见 容器服务支持的公共镜像。 
                   若不传该参数，容器服务将根据您所选的 ECS 实例规格，默认分配与该规格对应的 veLinux-VKE 镜像 ID。 
             SystemVolume ( Object of SystemVolume ): 否  节点的系统盘配置。 
                   调用 ECS 的 DescribeInstanceTypes 接口获取 ECS 实例规格族与云盘规格的匹配关系。 
             DataVolumes ( Array of DataVolume ): 否  节点的数据盘配置。 
                   调用云服务的 DescribeInstanceTypes 接口获取 ECS 实例规格族与云盘规格的匹配关系。 
             InitializeScript ( String ): 否  创建并初始化节点后执行的自定义脚本。 
                   支持 Shell 格式，Base64 编码后长度不超过 1 KB。 
             Security ( Object of NodeSecurityRequest ): 是  节点安全配置。 
             AdditionalContainerStorageEnabled ( Boolean ): 否  配置节点的第一块数据盘并格式化挂载容器和镜像存储目录/var/lib/containerd，取值： 
                   - false：（默认值）关闭 
                   - true：开启 
                   - 至少配置一块数据盘，否则将导致节点池创建失败。 
                   - 该方式将自动格式化第一块数据盘并创建文件系统。 
             InstanceChargeType ( String ): 否  ECS 实例计费类型，取值： 
                   - PostPaid：（默认值）按量计费 
                   - PrePaid：包年包月 
             Period ( Integer ): 否  ECS 实例购买时长。取值如下，单位为月： 
                   1、2、3、4、5、6、7、8、9、12、24、36 
                   仅当InstanceChargeType=PrePaid时才需要填写且为必选参数。 
             AutoRenew ( Boolean ): 否  ECS 实例到期是否自动续费，取值范围： 
                   - true：（默认值）自动续费 
                   - false：不自动续费 
                   	仅当InstanceChargeType=PrePaid时才需要填写，否则忽略。 
             AutoRenewPeriod ( Integer ): 否  ECS 实例每次自动续费时长。取值如下，单位为月： 
                   1（默认值）、2、3、6、12 
                   仅当AutoRenew=true时才需要填写，否则忽略。 
             NamePrefix ( String ): 否  节点名称前缀。取值为空字符串时表示不启用节点命名前缀，默认不启用。前缀校验规则如下： 
                   - 支持英文大小写字母、数字和中划线(-)。 
                   - 只能以英文字母开头，英文字母或数字结尾。 
                   - 不能连续使用中划线(-)。 
                   - 长度限制为 2～51 个字符。 
             Tags ( Array of Tag ): 否  节点对应 ECS 实例绑定的标签信息，用于搜索、管理 ECS 实例。 
                   - Tags 中各个 Key 不可重复。 
                   - 资源已有相同 Tags.Key 的情况下，重复绑定 Tags.Key 不会报错，会更新为最新的 Tags.Value。 
                   - 单个资源最多支持绑定 20 个 ECS 实例标签。 
                   - Tags 中的 Key、Value 不允许在最前或最后输入空格。 
             HpcClusterIds ( Array of String ): 否  高性能计算集群 ID。 
                   当创建 高性能计算 GPU 型 规格的节点池时，需要指定高性能计算集群 ID。在 云服务器控制台 的 实例与镜像 > 高性能计算集群 页面获取 ID。 
                   - 当前仅支持传入一个高性能计算集群 ID。更多介绍，请参见 高性能计算集群概述。 
                   - 请确保指定的高性能计算集群与 SubnetIds 中指定的子网同属一个可用区。 
             ProjectName ( String ): 否  节点池中扩容出来的 ECS 所属的项目名称，一个 ECS 只能归属于一个项目。 
                   - 只能包含英文字母、数字、下划线（_）、英文句点（.）和中划线（-）。 
                   - 长度限制在 64 个字符以内。 
                   - 默认值：default。 
            "字段"： SystemVolume
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Type ( String ): 否  云盘类型： 
                   - ESSD_PL0：（默认值）性能级别为 PL0 的极速型 SSD 云盘。 
                   - ESSD_FlexPL：性能级别为 PL1 的极速型 SSD 云盘。 
                   更新节点池时，该参数为必填参数，无默认值。 
             Size ( Integer ): 否  云盘容量，单位 GiB，取值说明： 
                   - 默认值：40 
                   - 极速型 SSD（ESSD_PL0，ESSD_FlexPL): 40~2048 
                   更新节点池时，该参数为必填参数，无默认值。 
            "字段"： DataVolume
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Type ( String ): 否  磁盘类型： 
                   - ESSD_PL0：（默认值）性能级别为 PL0 的极速型 SSD 云盘。 
                   - ESSD_FlexPL：性能级别为 PL1 的极速型 SSD 云盘。 
                   更新节点池时，该参数为必填参数，无默认值。 
             Size ( Integer ): 否  磁盘容量，单位 GiB，数据云盘数值范围： 
                   - 默认值：20 
                   - 极速型 SSD（ESSD_PL0，ESSD_FlexPL）：20～32768 
                   更新节点池时，该参数为必填参数，无默认值。 
             MountPoint ( String ): 否  磁盘格式化后的目标挂载目录，取值要求如下： 
                   - 必须以/开头。 
                   - 长度限制为 1～255 个字符。 
                   - 不同数据盘的挂载目录不允许重复。 
            "字段"： NodeSecurityRequest
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             SecurityGroupIds ( Array of String ): 否  节点网络所在的安全组 ID 列表。 
                   调用私有网络的 DescribeSecurityGroups 接口，获取安全组 ID。 
                   - 必须与集群处于同一个私有网络内。 
                   - 取值为空时，默认使用 集群节点默认安全组（命名格式为-common）。默认安全组相关说明，请参见 安全组设置。 
                   - 单个节点池最多支持关联 5 个安全组（含集群节点默认安全组）。 
             SecurityStrategies ( Array of String ): 否  节点的安全策略，取值： 
                   - 取值为空：表示节点不开启安全加固。 
                   - Hids：主机安全加固。 
             Login ( Object of NodeLoginRequest ): 是  节点的访问方式配置。 
                   支持密码方式或密钥对方式。同时传入时，优先使用密钥对。 
            "字段"： NodeLoginRequest
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Password ( String ): 否  Root 用户登录密码，使用 Base64 编码格式。 
                   请遵循云服务器对于实例密码的要求规范： 
                   - 长度为 8～30 个字符 
                   - 不能以/和$6$开头 
                   - 支持以下几项字符，且至少包含三项 
                   	- 小写字母a~z 
                   	- 大写字母A~Z 
                   	- 数字0~9 
                   	- 特殊字符`( )  ~ ! @ # $ % ^ & * _ - + =  { } [ ] : ; '  , . ? /`` 
             SshKeyPairName ( String ): 否  SSH 密钥对名称。请确保该密钥对已在云服务器中创建或托管。 
            "字段"： Tag
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Key ( String ): 是  标签键。 
                   - 不能以任何大小写形式的volc:开头。 
                   - 只能包含语言字符、数字、空格和特殊符号_.:/=+-@。 
                   - 长度限制为 1～128 个字符。 
             Value ( String ): 否  标签值，可以为空。 
                   - 只能包含语言字符、数字、空格和特殊符号_.:/=+-@。 
                   - 长度不超过 256 个字符。 
            "字段"： NodePoolAutoScalingRequest
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Enabled ( Boolean ): 否  配置节点池弹性伸缩功能开关，取值： 
                   - false：（默认值）关闭。 
                   - true：开启。 
             MaxReplicas ( Integer ): 否  配置节点池的最大节点数，取值说明： 
                   - 默认值：10 
                   - 取值范围：1~2000 
                   仅在节点池开启弹性伸缩功能后，对该节点池生效。 
             MinReplicas ( Integer ): 否  配置节点池的最小节点数，取值说明： 
                   - 默认值：0 
                   - 最小值：0 
                   - 最大值：小于 MaxReplicas 参数的值 
                   仅在节点池开启弹性伸缩功能后，对该节点池生效。 
             DesiredReplicas ( Integer ): 否  配置节点池的期望节点数，取值说明： 
                   - 默认值：0 
                   - 取值范围：0~2000 
                   节点池开启弹性伸缩功能时，DesiredReplicas 需大于等于 MinReplicas 参数的值，小于等于 MaxReplicas 参数的值。 
             Priority ( Integer ): 否  优先级，取值说明： 
                   - 默认值：10 
                   - 取值范围：0~100 
                   仅针对节点池开启弹性伸缩功能且扩容算法为priority时生效。 
             SubnetPolicy ( String ): 否  节点池的多子网调度策略，用于在 Worker 节点扩容时按照子网优先级顺序进行调度。取值： 
                   - ZoneBalance：（默认值）可用区均衡策略，节点扩容时，新增的节点会分散到多个可用区的子网下，且保证各个可用区中的节点数相对均衡。 
                   - Priority：子网优先级策略，按照子网列表的先后顺序调度。如果优先级最高的子网可以创建成功，则总在该子网下新增节点。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Id ( String ): 节点池 ID。 
    """,
    "list_node_pools": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Region: (String) 是  集群所属的地域，常见的地域代号示例如下，默认为 cn-beijing：
                   - cn-beijing：华北2（北京）
                   - cn-beijing2：华北3（北京）
                   - cn-datong：华北4（大同）
                   - cn-wulanchabu：华北5（乌兰察布）
                   - cn-shanghai：华东2（上海）
                   - cn-guangzhou：华南1（广州）
                   - cn-hongkong：中国香港
                   - ap-southeast-1：亚太东南（柔佛）
                   - ap-southeast-3：亚太东南（雅加达）
             Filter ( Object of ListNodePoolsFilter ): 否  待查询节点池的筛选条件。 
             Tags ( Array of ListTagFilter ): 否  基于标签查询节点池列表。 
                   - Tags 中各个 Key 不可重复。 
                   - Tags 中的 Key、Value 不允许在最前或最后输入空格。 
                   - 单次最多支持 10 个标签。 
             PageNumber ( Integer ): 否  分页查询时的起始页码，从 1 开始，默认为 1。 
             PageSize ( Integer ): 否  分页查询时每页显示的记录数，取值： 
                   - 最小值：1 
                   - 最大值：100 
                   - 默认值：10 
            "字段"： ListNodePoolsFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             ClusterIds ( Array of String ): 否  集群 ID。 
                   可以调用 ListClusters 接口，获取集群 ID。单次最多填写 100 个集群 ID。 
                   此参数为空数组时，基于账号下指定地域的所有集群进行筛选。 
             Ids ( Array of String ): 否  节点池 ID 列表。 
                   单次最多填写 100 个节点池 ID。 
             Name ( String ): 否  节点池名称。 
                   支持模糊匹配。 
                   此参数为空时，返回指定集群内所有的节点池信息。 
             AutoScaling.Enabled ( Boolean ): 否  节点池弹性伸缩配置信息，取值： 
                   - true：开启弹性伸缩。 
                   - false：关闭弹性伸缩。 
             Statuses ( Array of NodePoolStatusFilter ): 否  节点池状态。 
                   单次最多填写 15 个数组元素。传入多个状态时，状态间是逻辑 或 关系。 
             CreateClientToken ( String ): 否  创建成功时的 ClientToken。 
                   ClientToken 是保证请求幂等性的字符串。该字符串由调用方传入。 
             UpdateClientToken ( String ): 否  最后一次更新成功时 ClientToken。 
                   ClientToken 是保证请求幂等性的字符串。该字符串由调用方传入。 
            "字段"： NodePoolStatusFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Phase ( String ): 否  节点池的状态，取值： 
                   - Creating 
                   - Running 
                   - Updating 
                   - Deleting 
                   - Failed 
                   - Scaling 
                   Phase 和 Conditions.Type 两者至少有一个参数必填，否则为无效数组元素。合法的 Phase 和 Conditions.Type 组合请参见 资源状态说明。 
             Conditions.Type ( String ): 否  节点池当前主状态下的状态条件，即进入该主状态的原因，可以有多个原因，取值： 
                   - Progressing 
                   - Ok 
                   - ResourceCleanupFailed 
                   - Unknown 
                   - ClusterNotRunning 
                   Phase 和 Conditions.Type 两者至少有一个参数必填，否则为无效数组元素。合法的 Phase 和 Conditions.Type 组合请参见 资源状态说明。 
            "字段"： ListTagFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Key ( String ): 是  标签键。 
                   - 不能以任何大小写形式的volc:开头。 
                   - 只能包含语言字符、数字、空格和特殊符号_.:/=+-@。 
                   - 长度限制为 1～128 个字符。 
             Value ( String ): 否  标签值，可以为空。 
                   - 只能包含语言字符、数字、空格和特殊符号_.:/=+-@。 
                   - 长度不超过 256 个字符。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Items ( Array of NodePool ): 节点池列表。 
        TotalCount ( Integer ): 符合条件的节点池总数。 
        PageNumber ( Integer ): 当前页码。 
        PageSize ( Integer ): 每页显示的节点池数。 
       "字段"： NodePool
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Id ( String ): 节点池 ID。 
        CreateClientToken ( String ): 创建成功时的 ClientToken。 
            ClientToken 是保证请求幂等性的字符串。该字符串由调用方传入。 
        UpdateClientToken ( String ): 最后一次更新成功时的 ClientToken。 
            ClientToken 是保证请求幂等性的字符串。该字符串由调用方传入。 
        ClusterId ( String ): 集群 ID。 
        Name ( String ): 节点池名称。 
        KubernetesConfig ( Object of NodePoolKubernetesConfigResponse ): 节点池 Kubernetes 配置。 
        NodeConfig ( Object of NodePoolNodeConfigResponse ): 节点池中云服务器实例配置。 
        AutoScaling ( Object of NodePoolAutoScalingResponse ): 节点池伸缩策略配置。 
        CreateTime ( String ): 创建节点池的时间。 
            标准 RFC3339 格式的 UTC+0 时间。 
        UpdateTime ( String ): 更新节点池的时间。 
            标准 RFC3339 格式的 UTC+0 时间。 
        Status ( Object of NodePoolStatus ): 节点池状态。 
        NodeStatistics ( Object of NodeStatistics ): 节点池中的节点统计。 
        Tags ( Array of TagResponse ): 节点池绑定的标签信息。 
       "字段"： NodePoolKubernetesConfigResponse
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Labels ( Array of Label ): 节点池/节点的 Kubernetes 标签（Labels）信息。 
        Taints ( Array of Taint ): 节点池/节点的 Kubernetes 污点（Taints）信息。 
        Cordon ( Boolean ): 封锁节点配置，参数值说明： 
            - false：不封锁。 
            - true：封锁。 
        NamePrefix ( String ): Kubernetes 中节点对象的元数据名称前缀。 
        KubeletConfig ( Object of NodePoolKubeletConfig ): 节点的 kubelet 自定义参数配置。 
        AutoSyncDisabled ( Boolean ): 是否禁用自动同步标签污点到存量节点的功能，参数值说明： 
            - true：禁用，即关闭自动同步。 
            - false：不禁用，即开启自动同步。 
       "字段"： Label
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Key ( String ): 标签键。 
        Value ( String ): 标签值。 
       "字段"： Taint
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Effect ( String ): 污点效果，参数值说明： 
            - NoSchedule：不调度。 
            - NoExecute：驱逐没有容忍污点的 Pod。 
            - PreferNoSchedule：尽量避免调度。 
        Key ( String ): 污点键。 
        Value ( String ): 污点值。 
       "字段"： NodePoolKubeletConfig
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        FeatureGates ( Object of FeatureGates ): 特性门控，即描述 Kubernetes 特性的一组键值对。 
            该特性门控仅支持在 Kubernetes v1.26 及以下版本的集群中使用。 
        TopologyManagerScope ( String ): 拓扑管理策略的资源粒度，取值： 
            - container：表示资源对齐粒度为容器级。 
        TopologyManagerPolicy ( String ): 拓扑管理策略，取值： 
            - none：（默认）禁用拓扑管理策略。 
            - restricted：kubelet 仅接受在所请求资源上实现最佳 NUMA（Non-Uniform Memory Access，非一致存储访问结构）的 Pod。 
            - best-effort：kubelet 会优先选择在 CPU 和设备资源上实现 NUMA 的 Pod。 
            - single-numa-node：kubelet 仅允许在同一个节点的 CPU 和设备资源上实现 NUMA 的 Pod。 
        KubeApiQps ( Integer ): 与 APIServer 通信的每秒查询个数。 
            - 整数形式，取值范围为 1～50。 
            - 默认值为 5。 
        KubeApiBurst ( Integer ): 每秒发送到 APIServer 的突发请求数量上限。 
            - 整数形式，取值范围为 1～100。 
            - 默认值为 10。 
            该值必须大于等于KubeApiQps参数的值。 
        EvictionHard ( Array of EvictionHard ): 触发 Pod 驱逐操作的一组硬性门限。详细参数解释，请参见 官方文档。 
            如果希望显式地禁用，可以在任意资源上将其阈值设置为 0% 或 100%。 
            默认值如下： 
            - memory.available: "100Mi" 
            - nodefs.available: "10%" 
            - nodefs.inodesFree: "5%" 
            - imagefs.available: "15%" 
        RegistryPullQps ( Integer ): 集群从镜像仓库拉取镜像的 QPS 阈值。 
            - 整数形式，取值范围为 1～50。 
            - 默认值为 2。 
        RegistryBurst ( Integer ): 集群从镜像仓库拉取镜像的突发阈值。 
            - 整数形式，取值范围为 1～100。 
            - 默认值为 5。 
            仅当RegistryPullQps大于 0 时需要配置，且取值必须大于等于RegistryPullQps参数的值。 
        SerializeImagePulls ( Boolean ): 是否串行拉取镜像，取值： 
            - true：串行拉取镜像。 
            - false：（默认）并行拉取镜像，能够提高 Pod 启动速度。 
       "字段"： FeatureGates
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        QoSResourceManager ( Boolean ): 是否启用 QoS 资源管理器，用于支持微拓扑调度。取值： 
            - true：启用 QoS 资源管理器。 
            - false：（默认）不启用 QoS 资源管理器。 
       "字段"： EvictionHard
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Key ( String ): 硬性门限名称。取值： 
            - memory.available 
            - nodefs.available 
            - nodefs.inodesFree 
            - imagefs.available 
        Value ( String ): 硬性门限值。 
       "字段"： NodePoolNodeConfigResponse
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        InstanceTypeIds ( Array of String ): 节点对应的云服务器实例规格 ID 列表。 
            规格详细说明，请参见 实例规格清单。 
        SubnetIds ( Array of String ): 节点网络所属的子网 ID 列表。 
        ImageId ( String ): 节点对应云服务器所使用的镜像 ID。 
        SystemVolume ( Object of SystemVolume ): 节点的系统盘配置。 
        DataVolumes ( Array of DataVolume ): 节点的数据盘配置。 
        InitializeScript ( String ): 创建并初始化节点后执行的自定义脚本。 
            Base64 编码后的 Shell 格式脚本。 
        Security ( Object of NodeSecurityResponse ): 节点安全配置。 
        AdditionalContainerStorageEnabled ( Boolean ): 节点的第一块数据盘是否已配置并格式化挂载作为容器镜像和日志的存储目录，参数值说明： 
            - false：未配置并格式化。 
            - true：已配置并格式化。 
        InstanceChargeType ( String ): 云服务器实例计费类型，参数值说明： 
            - PostPaid：按量计费 
            - PrePaid：包年包月 
        Period ( Integer ): 云服务器实例购买时长，单位为月。 
            仅当InstanceChargeType=PrePaid时才返回的参数。 
        AutoRenew ( Boolean ): 云服务器实例到期是否自动续费，参数值说明： 
            - true：自动续费 
            - false：不自动续费 
            	仅当InstanceChargeType=PrePaid时才返回的参数。 
        AutoRenewPeriod ( Integer ): 云服务器实例每次自动续费时长，单位为月。 
            仅当AutoRenew=true时才返回的参数。 
        NamePrefix ( String ): 节点名称前缀，为空字符串或 nil 时表示未开启节点名称前缀策略。 
        HpcClusterIds ( Array of String ): 高性能计算集群 ID。 
            当节点池配置为高性能计算 GPU 型规格节点时，返回高性能计算集群 ID。 
        Tags ( Array of Tag ): 节点对应 ECS 实例绑定的标签信息。 
        ProjectName ( String ): 节点池内 ECS 所属项目。 
       "字段"： SystemVolume
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Type ( String ): 云盘类型： 
            - ESSD_PL0：性能级别为 PL0 的极速型 SSD 云盘。 
            - ESSD_FlexPL：性能级别为 PL1 的极速型 SSD 云盘。 
        Size ( Integer ): 云盘容量，单位 GiB。 
       "字段"： DataVolume
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Type ( String ): 磁盘类型： 
            - ESSD_PL0：性能级别为 PL0 的极速型 SSD 云盘。 
            - ESSD_FlexPL：性能级别为 PL1 的极速型 SSD 云盘。 
        Size ( Integer ): 磁盘容量，单位 GiB。 
        MountPoint ( String ): 磁盘格式化后的目标挂载目录。 
       "字段"： NodeSecurityResponse
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        SecurityGroupIds ( Array of String ): 节点网络所在的安全组 ID 列表。 
        SecurityStrategyEnabled ( Boolean ): 节点是否启用了安全加固配置，参数值说明： 
            - true：已开启 
            - false：未开启 
        SecurityStrategies ( Array of String ): 节点的安全策略，参数值说明： 
            Hids：主机安全加固。 
        Login ( Object of NodeLoginResponse ): 节点的访问方式配置。 
       "字段"： NodeLoginResponse
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Type ( String ): 节点的访问登录方式，参数值说明： 
            - Password：密码登录。 
            - SshKeyPair：SSH 密钥对登录。 
        SshKeyPairName ( String ): SSH 密钥对名称。 
       "字段"： Tag
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Key ( String ): 标签键。 
        Value ( String ): 标签值。 
       "字段"： NodePoolAutoScalingResponse
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enabled ( Boolean ): 配置节点池弹性伸缩功能开关，参数值说明： 
            - false：关闭。 
            - true：开启。 
        MaxReplicas ( Integer ): 配置节点池的最大节点数。 
        MinReplicas ( Integer ): 配置节点池的最小节点数。 
        DesiredReplicas ( Integer ): 配置节点池的期望节点数。 
        Priority ( Integer ): 优先级。 
            仅针对节点池开启弹性伸缩功能且扩容算法为priority时，优先级才会生效。 
        SubnetPolicy ( String ): 节点池的多子网调度策略，参数值说明： 
            - ZoneBalance：可用区均衡策略。 
            - Priority：子网优先级策略。 
       "字段"： NodePoolStatus
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Phase ( String ): 节点池的状态，参数值有： 
            - Creating 
            - Running 
            - Updating 
            - Deleting 
            - Failed 
            - Scaling 
            合法的 Phase 和 Conditions.Type 组合说明，请参见 资源状态说明。 
        Conditions ( Array of NodePoolStatusCondition ): 节点池当前主状态下的状态条件，即进入该主状态的原因。 
       "字段"： NodePoolStatusCondition
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Type ( String ): 节点池当前主状态下的状态条件，即进入该主状态的原因，可以有多个原因，参数值有： 
            - Progressing 
            - Ok 
            - ResourceCleanupFailed 
            - Unknown 
            - ClusterNotRunning 
       "字段"： NodeStatistics
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        TotalCount ( Integer ): 节点总数量。 
        CreatingCount ( Integer ): Phase=Creating的节点总数量。 
        RunningCount ( Integer ): Phase=Running的节点总数量。 
        UpdatingCount ( Integer ): Phase=Updating的节点总数量。 
        DeletingCount ( Integer ): Phase=Deleting的节点总数量。 
        FailedCount ( Integer ): Phase=Failed的节点总数量。 
       "字段"： TagResponse
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Key ( String ): 标签键。 
        Value ( String ): 标签值。 
        Type ( String ): 标签类型，参数值说明： 
            - System：  系统标签。 
            - Custom：用户自定义标签。 
    """,
    "create_default_node_pool": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Region: (String) 是  集群所属的地域，常见的地域代号示例如下，默认为 cn-beijing：
                   - cn-beijing：华北2（北京）
                   - cn-beijing2：华北3（北京）
                   - cn-datong：华北4（大同）
                   - cn-wulanchabu：华北5（乌兰察布）
                   - cn-shanghai：华东2（上海）
                   - cn-guangzhou：华南1（广州）
                   - cn-hongkong：中国香港
                   - ap-southeast-1：亚太东南（柔佛）
                   - ap-southeast-3：亚太东南（雅加达）
             ClientToken ( String ): 否  用于保证请求幂等性的字符串。该字符串由调用方传入，需保证不同请求之间唯一。ClientToken 对大小写敏感，且最大值不超过 64 个 ASCII 字符。 
             ClusterId ( String ): 是  默认节点池所在集群的 ID。 
                   可以调用 ListClusters 接口，获取集群 ID。 
                   集群必须处于{Running,Ok]}或{Updating,[Progressing]}状态。可调用 [ListClusters] 接口获取集群当前的状态。 
             KubernetesConfig ( Object of NodePoolKubernetesConfigRequest ): 否  默认节点池 Kubernetes 配置。 
             NodeConfig ( Object of DefaultNodePoolNodeConfigRequest ): 是  默认节点池中云服务器（ECS）实例配置。 
             Tags ( Array of Tag ): 否  默认节点池标签信息，用于从不同维度对具有相同特征的节点池进行分类、搜索和聚合，能够灵活管理节点池。 
                   - Tags 中各个 Key 不可重复。 
                   - 资源已有相同 Tags.Key 的情况下，重复绑定 Tags.Key 不会报错，会更新为最新的 Tags.Value。 
                   - 单个资源最多支持绑定50个 Tags。 
                   - Tags 中的 Key、Value 不允许在最前或最后输入空格。 
            "字段"： NodePoolKubernetesConfigRequest
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Labels ( Array of Label ): 否  节点池/节点的 Kubernetes 标签（Labels）信息。最多可传入 20 个标签。 
                   节点池会统一管理节点的标签配置信息，因此标签信息会同步到节点池内的所有节点上。当标签发生变更时，会覆盖原有的标签配置信息。 
             Taints ( Array of Taint ): 否  节点池/节点的 Kubernetes 污点（Taints）信息。最多可传入 20 个污点。 
                   节点池会统一管理节点的污点配置信息，因此污点信息会同步到节点池内的所有节点上。当污点发生变更时，会覆盖原有的污点配置信息。 
             Cordon ( Boolean ): 否  封锁节点配置，取值： 
                   - false：（默认值）不封锁 
                   - true：封锁 
                   更新节点池（UpdateNodePoolConfig）时，若不传入参数值，则保持原有参数配置。 
             NamePrefix ( String ): 否  Kubernetes 中节点对象的元数据名称前缀。默认不启用，若设置表示启用，并将影响 Kubernetes Node Manifest 文件中展示的metadata.name前缀信息。前缀校验规则如下： 
                   - 支持英文小写字母、数字、中划线(-)和半角句号(.)。 
                   - 只能以英文小写字母或者数字开头。 
                   - 长度限制为 1~48 个字符。 
             KubeletConfig ( Object of NodePoolKubeletConfig ): 否  节点池中节点的 kubelet 自定义参数配置，用于调整节点行为。 
             AutoSyncDisabled ( Boolean ): 否  是否禁用自动同步标签污点到存量节点的功能，取值： 
                   - true：禁用，即关闭自动同步。 
                   - false：（默认值）不禁用，即开启自动同步。 
            "字段"： Label
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Key ( String ): 是  标签键，要求如下，更多规则，请参见 Kubernetes 标签规则。 
                   有效的标签键有两个段：和，用斜杠（/）分隔。 
                   - 是必须的，支持英文大小写字母、数字、短划线（-）、下划线（_）、英文句号（ .），以字母或数字开头和结尾，长度不超过 63 个字符。 
                   - 是可选的。如果指定，则必须是 DNS 子域：由英文句号（.）分隔的一系列 DNS 标签，长度不超过 253 个字符。 
                   - 和总长度不超过 82 个字符。 
             Value ( String ): 否  标签值，要求如下，更多规则，请参见 Kubernetes 标签规则。 
                   - 长度不超过 63 个字符（可以为空）。 
                   - 支持以英文大小写字母、数字开头和结尾。 
                   - 支持特殊字符：短划线（-）、下划线（_）、英文句号（.）。 
            "字段"： Taint
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Effect ( String ): 否  污点效果，取值： 
                   - NoSchedule：（默认值）不调度。 
                   - NoExecute：驱逐没有容忍污点的 Pod。 
                   - PreferNoSchedule：尽量避免调度。 
             Key ( String ): 是  污点键，要求如下，更多规则，请参见 Kubernetes 标签规则。 
                   有效的污点键有两个段：和，用斜杠（/）分隔。 
                   - 是必须的，支持英文大小写字母、数字、短划线（-）、下划线（_）、英文句号（ .），以字母或数字开头和结尾，长度不超过 63 个字符。 
                   - 是可选的。如果指定，则必须是 DNS 子域：由英文句号（.）分隔的一系列 DNS 标签，长度不超过 253 个字符。 
                   - 和总长度不超过 82 个字符。 
             Value ( String ): 否  污点值，要求如下，更多规则，请参见 Kubernetes 标签规则。 
                   - 长度不超过 63 个字符（可以为空）。 
                   - 支持以英文大小写字母、数字开头和结尾。 
                   - 支持特殊字符：短划线（-）、下划线（_）、英文句号（.）。 
            "字段"： NodePoolKubeletConfig
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             FeatureGates ( Object of FeatureGates ): 否  特性门控，即描述 Kubernetes 特性的一组键值对。 
                   该特性门控仅支持在 Kubernetes v1.26 及以下版本的集群中使用。 
             TopologyManagerScope ( String ): 否  拓扑管理策略的资源粒度，取值： 
                   - container：表示资源对齐粒度为容器级。 
             TopologyManagerPolicy ( String ): 否  拓扑管理策略，取值： 
                   - none：（默认）禁用拓扑管理策略。 
                   - restricted：kubelet 仅接受在所请求资源上实现最佳 NUMA（Non-Uniform Memory Access，非一致存储访问结构）的 Pod。 
                   - best-effort：kubelet 会优先选择在 CPU 和设备资源上实现 NUMA 的 Pod。 
                   - single-numa-node：kubelet 仅允许在同一个节点的 CPU 和设备资源上实现 NUMA 的 Pod。 
             KubeApiQps ( Integer ): 否  与 APIServer 通信的每秒查询个数。 
                   - 整数形式，取值范围为 1～50。 
                   - 默认值为 5。 
             KubeApiBurst ( Integer ): 否  每秒发送到 APIServer 的突发请求数量上限。 
                   - 整数形式，取值范围为 1～100。 
                   - 默认值为 10。 
                   该值必须大于等于KubeApiQps参数的值。 
             EvictionHard ( Array of EvictionHard ): 否  触发 Pod 驱逐操作的一组硬性门限。详细参数解释，请参见 官方文档。 
                   如果希望显式地禁用，可以在任意资源上将其阈值设置为 0% 或 100%。 
                   默认值如下： 
                   - memory.available: "100Mi" 
                   - nodefs.available: "10%" 
                   - nodefs.inodesFree: "5%" 
                   - imagefs.available: "15%" 
             RegistryPullQps ( Integer ): 否  集群从镜像仓库拉取镜像的 QPS 阈值。 
                   - 整数形式，取值范围为 1～50。 
                   - 默认值为 2。 
             RegistryBurst ( Integer ): 否  集群从镜像仓库拉取镜像的突发阈值。 
                   - 整数形式，取值范围为 1～100。 
                   - 默认值为 5。 
                   仅当RegistryPullQps大于 0 时需要配置，且取值必须大于等于RegistryPullQps参数的值。 
             SerializeImagePulls ( Boolean ): 否  是否串行拉取镜像，取值： 
                   - true：串行拉取镜像。 
                   - false：（默认）并行拉取镜像，能够提高 Pod 启动速度。 
            "字段"： FeatureGates
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             QoSResourceManager ( Boolean ): 否  是否启用 QoS 资源管理器，用于支持微拓扑调度。取值： 
                   - true：启用 QoS 资源管理器。 
                   - false：（默认）不启用 QoS 资源管理器。 
            "字段"： EvictionHard
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Key ( String ): 是  硬性门限名称。取值： 
                   - memory.available 
                   - nodefs.available 
                   - nodefs.inodesFree 
                   - imagefs.available 
             Value ( String ): 是  硬性门限值。 
            "字段"： DefaultNodePoolNodeConfigRequest
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             InitializeScript ( String ): 否  创建并初始化节点后执行的自定义脚本。 支持 Shell 格式，Base64 编码后长度不超过 1 KB。 
             Security ( Object of NodeSecurityRequest ): 是  节点安全配置。 
             NamePrefix ( String ): 否  节点名称前缀。取值为空字符串时表示不启用节点命名前缀，默认不启用。前缀校验规则如下： 
                   - 支持英文大小写字母、数字和中划线(-)。 
                   - 只能以英文字母开头，英文字母或数字结尾。 
                   - 不能连续使用中划线(-)。 
                   - 长度限制为 2～51 个字符。 
             Tags ( Array of Tag ): 否  节点对应 ECS 实例绑定的标签信息，用于搜索、管理 ECS 实例。 
                   - Tags 中各个 Key 不可重复。 
                   - 资源已有相同 Tags.Key 的情况下，重复绑定 Tags.Key 不会报错，会更新为最新的 Tags.Value。 
                   - 单个资源最多支持绑定 20 个 ECS 实例标签。 
                   - Tags 中的 Key、Value 不允许在最前或最后输入空格。 
            "字段"： NodeSecurityRequest
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             SecurityGroupIds ( Array of String ): 否  节点网络所在的安全组 ID 列表。 
                   调用私有网络的 DescribeSecurityGroups 接口，获取安全组 ID。 
                   - 必须与集群处于同一个私有网络内。 
                   - 取值为空时，默认使用 集群节点默认安全组（命名格式为-common）。默认安全组相关说明，请参见 安全组设置。 
                   - 单个节点池最多支持关联 5 个安全组（含集群节点默认安全组）。 
             SecurityStrategies ( Array of String ): 否  节点的安全策略，取值： 
                   - 取值为空：表示节点不开启安全加固。 
                   - Hids：主机安全加固。 
             Login ( Object of NodeLoginRequest ): 是  节点的访问方式配置。 
                   支持密码方式或密钥对方式。同时传入时，优先使用密钥对。 
            "字段"： NodeLoginRequest
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Password ( String ): 否  Root 用户登录密码，使用 Base64 编码格式。 
                   请遵循云服务器对于实例密码的要求规范： 
                   - 长度为 8～30 个字符 
                   - 不能以/和$6$开头 
                   - 支持以下几项字符，且至少包含三项 
                   	- 小写字母a~z 
                   	- 大写字母A~Z 
                   	- 数字0~9 
                   	- 特殊字符`( )  ~ ! @ # $ % ^ & * _ - + =  { } [ ] : ; '  , . ? /`` 
             SshKeyPairName ( String ): 否  SSH 密钥对名称。请确保该密钥对已在云服务器中创建或托管。 
            "字段"： Tag
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Key ( String ): 是  标签键。 
                   - 不能以任何大小写形式的volc:开头。 
                   - 只能包含语言字符、数字、空格和特殊符号_.:/=+-@。 
                   - 长度限制为 1～128 个字符。 
             Value ( String ): 否  标签值，可以为空。 
                   - 只能包含语言字符、数字、空格和特殊符号_.:/=+-@。 
                   - 长度不超过 256 个字符。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Id ( String ): 默认节点池 ID。 
    """,
    "create_nodes": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Region: (String) 是  集群所属的地域，常见的地域代号示例如下，默认为 cn-beijing：
                   - cn-beijing：华北2（北京）
                   - cn-beijing2：华北3（北京）
                   - cn-datong：华北4（大同）
                   - cn-wulanchabu：华北5（乌兰察布）
                   - cn-shanghai：华东2（上海）
                   - cn-guangzhou：华南1（广州）
                   - cn-hongkong：中国香港
                   - ap-southeast-1：亚太东南（柔佛）
                   - ap-southeast-3：亚太东南（雅加达）
             ClientToken ( String ): 否  用于保证请求幂等性的字符串。该字符串由调用方传入，需保证不同请求之间唯一。ClientToken 对大小写敏感，且最大值不超过 64 个 ASCII 字符。 
             ClusterId ( String ): 是  集群的 ID。 
                   可以调用 ListClusters 接口，获取集群 ID。 
                   集群必须处于{Running,*]} 或 {Updating,[Progressing]}状态。可调用 [ListClusters] 接口获取集群当前的状态。 
             NodePoolId ( String ): 否  节点池 ID。 
                   * 不传入参数值：表示将已有 ECS 实例添加到默认节点池。 
                   * 传入参数值：表示将已有 ECS 实例添加到自定义节点池。可调用 ListNodePools 接口，获取目标自定义节点池 ID。 
                   若此处填写 自定义节点池 ID，则待添加的节点将应用自定义节点池上的 Kubernetes 配置和节点配置（包括 ECS 实例标签、标签、污点、封锁节点配置、项目、节点名称前缀等），因此 InitializeScript、KubernetesConfig、ImageId 参数配置将无效，上述参数仅在默认节点池中添加已有节点时有效。 
             InstanceIds ( Array of String ): 是  要添加到集群的 ECS 实例 ID。单次调用最多支持填写 100 个 ECS 实例 ID。 
                   调用 DescribeInstances 接口，获取 ECS 实例 ID。该 ECS 实例须满足以下条件： 
                   * 与集群在同一个私有网络内。 
                   * 未被其他集群使用。 
                   * 实例状态必须处于 运行中（Running）。 
                   * 添加的节点数量不能超过集群所支持的最大节点数上限。 
                   * 请勿重复添加同一个 ECS 实例。 
                   ECS 实例作为节点添加进集群实例的过程中，VKE 会重置 ECS 实例的操作系统，该实例系统盘的历史数据会被清除。 
             KeepInstanceName ( Boolean ): 否  是否保留原 ECS 实例名称，取值： 
                   * false：（默认值）不保留原 ECS 实例名称，由容器服务自动为其命名。 
                   * true：保留原 ECS 实例名称。 
             AdditionalContainerStorageEnabled ( Boolean ): 否  选择配置节点的数据盘并格式化挂载作为容器镜像和日志的存储目录，取值： 
                   * false：（默认值）关闭。 
                      * 默认节点池：表示不挂载数据盘。 
                      * 自定义节点池：使用节点池的数据盘配置进行挂载，被添加到节点池的 ECS 实例数据盘必须包含目标节点池指定了挂载的数据盘（含本地盘），且盘类型和大小完全一致。 
                   * true: 开启。此时必须同时配置 ContainerStoragePath 参数。节点通过 ContainerStoragePath参数中的配置进行挂载，而忽略节点池的数据盘配置，对被添加到节点池的 ECS 实例数据盘无特殊要求。 
             ContainerStoragePath ( String ): 否  使用该数据盘设备挂载容器和镜像存储目录/var/lib/containerd。 
                   仅当AdditionalContainerStorageEnabled=true时有效，且不能为空。 
                   须满足以下条件，否则将初始化失败： 
                   * 仅支持已挂载数据盘的 ECS 实例。 
                   * 指定数据盘设备名时，请确保该数据盘设备存在，否则会初始化失败。 
                   * 指定数据盘分区或逻辑卷名时，请确保该分区或逻辑卷存在，且为 ext4 文件系统。 
                   * 指定数据盘设备时，将自动格式化后直接挂载，请注意提前备份数据。 
                   * 指定数据盘分区或逻辑卷名时，不需要格式化。 
             ImageId ( String ): 否  节点对应的 ECS 实例使用的镜像 ID。 
                   不同的镜像类型对应的镜像 ID 也不同，详细说明，请参见 容器服务支持的公共镜像。 
                   若不传该参数，容器服务将根据您所选的 ECS 实例规格，默认分配与该规格对应的 veLinux-VKE 镜像 ID。 
             InitializeScript ( String ): 否  创建 ECS 节点并完成 Kubernetes 组件部署后执行的脚本。支持 Shell 格式，Base64 编码后长度不超过 1 KB。 
                   * 为空时，节点继承使用默认节点池配置的初始化脚本NodeConfig.InitializeScript。 
                   * 自定义填写脚本内容后，使用自定义的脚本，忽略默认节点池配置的初始化脚本。 
             KubernetesConfig ( Object of KubernetesConfigRequest ): 否  节点 Kubernetes 相关配置。 
                   * 为空时，节点继承使用默认节点池的 Kubernetes 配置KubernetesConfig.Labels/Taints/Cordon。 
                   * 自定义填写配置后，使用自定义配置内容，忽略默认节点池的 Kubernetes 配置。 
            "字段"： KubernetesConfigRequest
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Labels ( Array of Label ): 否  节点池/节点的 Kubernetes 标签（Labels）信息。最多可传入 20 个标签。 
                   节点池会统一管理节点的标签配置信息，因此标签信息会同步到节点池内的所有节点上。当标签发生变更时，会覆盖原有的标签配置信息。 
             Taints ( Array of Taint ): 否  节点池/节点的 Kubernetes 污点（Taints）信息。最多可传入 20 个污点。 
                   节点池会统一管理节点的污点配置信息，因此污点信息会同步到节点池内的所有节点上。当污点发生变更时，会覆盖原有的污点配置信息。 
             Cordon ( Boolean ): 否  封锁节点配置，取值： 
                   - false：（默认值）不封锁 
                   - true：封锁 
                   更新节点池（UpdateNodePoolConfig）时，若不传入参数值，则保持原有参数配置。 
            "字段"： Label
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Key ( String ): 是  标签键，要求如下，更多规则，请参见 Kubernetes 标签规则。 
                   有效的标签键有两个段：和，用斜杠（/）分隔。 
                   - 是必须的，支持英文大小写字母、数字、短划线（-）、下划线（_）、英文句号（ .），以字母或数字开头和结尾，长度不超过 63 个字符。 
                   - 是可选的。如果指定，则必须是 DNS 子域：由英文句号（.）分隔的一系列 DNS 标签，长度不超过 253 个字符。 
                   - 和总长度不超过 82 个字符。 
             Value ( String ): 否  标签值，要求如下，更多规则，请参见 Kubernetes 标签规则。 
                   - 长度不超过 63 个字符（可以为空）。 
                   - 支持以英文大小写字母、数字开头和结尾。 
                   - 支持特殊字符：短划线（-）、下划线（_）、英文句号（.）。 
            "字段"： Taint
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Effect ( String ): 否  污点效果，取值： 
                   - NoSchedule：（默认值）不调度。 
                   - NoExecute：驱逐没有容忍污点的 Pod。 
                   - PreferNoSchedule：尽量避免调度。 
             Key ( String ): 是  污点键，要求如下，更多规则，请参见 Kubernetes 标签规则。 
                   有效的污点键有两个段：和，用斜杠（/）分隔。 
                   - 是必须的，支持英文大小写字母、数字、短划线（-）、下划线（_）、英文句号（ .），以字母或数字开头和结尾，长度不超过 63 个字符。 
                   - 是可选的。如果指定，则必须是 DNS 子域：由英文句号（.）分隔的一系列 DNS 标签，长度不超过 253 个字符。 
                   - 和总长度不超过 82 个字符。 
             Value ( String ): 否  污点值，要求如下，更多规则，请参见 Kubernetes 标签规则。 
                   - 长度不超过 63 个字符（可以为空）。 
                   - 支持以英文大小写字母、数字开头和结尾。 
                   - 支持特殊字符：短划线（-）、下划线（_）、英文句号（.）。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Ids ( Array of String ): 节点 ID 列表。 
    """,
    "list_nodes": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Region: (String) 是  集群所属的地域，常见的地域代号示例如下，默认为 cn-beijing：
                   - cn-beijing：华北2（北京）
                   - cn-beijing2：华北3（北京）
                   - cn-datong：华北4（大同）
                   - cn-wulanchabu：华北5（乌兰察布）
                   - cn-shanghai：华东2（上海）
                   - cn-guangzhou：华南1（广州）
                   - cn-hongkong：中国香港
                   - ap-southeast-1：亚太东南（柔佛）
                   - ap-southeast-3：亚太东南（雅加达）
             Filter ( Object of ListNodesFilter ): 否  待查询节点的筛选条件。 
             PageNumber ( Integer ): 否  分页查询时的起始页码，从 1 开始，默认为 1。 
             PageSize ( Integer ): 否  分页查询时每页显示的记录数，取值： 
                   - 最小值：1 
                   - 最大值：100 
                   - 默认值：10 
            "字段"： ListNodesFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             ClusterIds ( Array of String ): 否  集群 ID 列表。 
                   可以调用 ListClusters 接口，获取集群 ID。单次最多填写 100 个集群 ID。 
                   此参数为空数组时，筛选基于账号下指定地域的所有集群。 
             Ids ( Array of String ): 否  节点 ID 列表。 
                   单次调用最多填写 100 个节点 ID。 
             Name ( String ): 否  节点名称。 
                   支持模糊匹配。 
             NodePoolIds ( Array of String ): 否  节点池 ID 列表。 
                   可以调用 ListNodePools 接口，获取节点池 ID。单次调用最多填写 100 个节点池 ID。 
             ZoneIds ( Array of String ): 否  可用区 ID 列表。容器服务的可用区列表，请参见 地域和可用区。 
             Statuses ( Array of NodeStatusFilter ): 否  节点状态。 
                   单次调用最多填写 15 个数组元素。传入多个状态时，状态间是逻辑「或」关系。 
             CreateClientToken ( String ): 否  创建成功时的 ClientToken。 
                   用于保证请求幂等性的字符串。该字符串由调用方传入，需保证不同请求之间唯一。ClientToken 对大小写敏感，且最大值不超过 64 个 ASCII 字符。 
            "字段"： NodeStatusFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Phase ( String ): 否  节点的状态，取值： 
                   - Creating 
                   - Running 
                   - Deleting 
                   - Failed 
                   - Updating 
                   Phase 和 Conditions.Type 两者至少有一个参数必填，否则为无效数组元素。合法的 Phase 和 Conditions.Type 组合请参见 资源状态说明。 
             Conditions.Type ( String ): 否  节点池当前主状态下的状态条件，即进入该主状态的原因，可以有多个原因，取值： 
                   - Progressing 
                   - Ok 
                   - Unschedulable 
                   - InitilizeFailed 
                   - NotReady 
                   - Balance 
                   - ResourceCleanupFailed 
                   - Unknown 
                   Phase 和 Conditions.Type 两者至少有一个参数必填，否则为无效数组元素。合法的 Phase 和 Conditions.Type 组合请参见 资源状态说明。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Items ( Array of Node ): 节点列表。 
        PageNumber ( Integer ): 当前页码。 
        PageSize ( Integer ): 每页显示的节点数。 
        TotalCount ( Integer ): 符合条件的节点总数。 
       "字段"： Node
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Id ( String ): 节点 ID。 
        Name ( String ): 节点名称。 
        ClusterId ( String ): 集群 ID。 
        InstanceId ( String ): 节点对应的云服务器实例 ID。 
        NodePoolId ( String ): 节点池 ID。 
        ZoneId ( String ): 可用区 ID。 
        Roles ( Array of String ): 节点角色，参数值说明： 
            Worker：Worker节点 
        CreateClientToken ( String ): 创建成功时的 ClientToken。 
            ClientToken 是保证请求幂等性的字符串。该字符串由调用方传入。 
        CreateTime ( String ): 创建时间。 
            标准 RFC3339 格式的 UTC+0 时间。 
        UpdateTime ( String ): 更新时间。 
            标准 RFC3339 格式的 UTC+0 时间。 
        Status ( Object of NodeStatus ): 节点状态。 
        IsVirtual ( Boolean ): 是否为虚拟节点，参数值说明： 
            - false：否 
            - true：是 
        AdditionalContainerStorageEnabled ( Boolean ): 是否已配置节点的数据盘作为容器镜像和日志的存储目录，参数值说明： 
            - false：未配置 
            - true：已配置 
        ContainerStoragePath ( String ): 用于作为容器镜像和日志存储目录的数据盘设备名称。 
        ImageId ( String ): 节点对应的云服务器实例使用的镜像 ID。 
        InitializeScript ( String ): 创建 ECS 节点并完成 Kubernetes 组件部署后执行的脚本。 
        KubernetesConfig ( Object of KubernetesConfigResponse ): 节点初始化时使用的 Kubernetes 相关配置。 
            其中，创建节点后添加的 Label（标签）、Taints（污点）不会通过该 OpenAPI 返回，您需要 连接集群 后使用 Kubernetes API 获取。Kubernetes API 相关信息，请参见 官方文档。 
       "字段"： NodeStatus
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Phase ( String ): 节点的状态，参数值有： 
            - Creating 
            - Running 
            - Deleting 
            - Failed 
            - Updating 
            合法的 Phase 和 Conditions.Type 组合说明，请参见 资源状态说明。 
        Conditions ( Array of NodeStatusCondition ): 节点当前主状态下的状态条件，即进入该主状态的原因。 
            合法的 Phase 和 Conditions.Type 组合说明，请参见 资源状态说明。 
       "字段"： NodeStatusCondition
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Type ( String ): 节点当前主状态下的状态条件，即进入该主状态的原因，可以有多个原因，参数值有： 
            - Progressing 
            - Ok 
            - Unschedulable 
            - InitilizeFailed 
            - NotReady 
            - Balance 
            - ResourceCleanupFailed 
            - Unknown 
       "字段"： KubernetesConfigResponse
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Labels ( Array of Label ): 节点池/节点的 Kubernetes 标签（Labels）信息。 
        Taints ( Array of Taint ): 节点池/节点的 Kubernetes 污点（Taints）信息。 
        Cordon ( Boolean ): 封锁节点配置，参数值说明： 
            - false：不封锁。 
            - true：封锁。 
       "字段"： Label
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Key ( String ): 标签键。 
        Value ( String ): 标签值。 
       "字段"： Taint
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Effect ( String ): 污点效果，参数值说明： 
            - NoSchedule：不调度。 
            - NoExecute：驱逐没有容忍污点的 Pod。 
            - PreferNoSchedule：尽量避免调度。 
        Key ( String ): 污点键。 
        Value ( String ): 污点值。 
    """,
    "list_k8s_resources": r"""
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Region: (String) 是  集群所属的地域，常见的地域代号示例如下，默认为 cn-beijing：
                   - cn-beijing：华北2（北京）
                   - cn-beijing2：华北3（北京）
                   - cn-datong：华北4（大同）
                   - cn-wulanchabu：华北5（乌兰察布）
                   - cn-shanghai：华东2（上海）
                   - cn-guangzhou：华南1（广州）
                   - cn-hongkong：中国香港
                   - ap-southeast-1：亚太东南（柔佛）
                   - ap-southeast-3：亚太东南（雅加达）
             ClusterId ( String ): 是  集群 ID。
             ApiVersion ( String ): 是  API 版本，常见的有：
                 - v1
                 - apps/v1
                 - batch/v1
                 - authentication.k8s.io/v1
                 - events.k8s.io/v1
                 - networking.k8s.io/v1
                 - discovery.k8s.io/v1
                 - coordination.k8s.io/v1
                 - scheduling.k8s.io/v1
                 - storage.k8s.io/v1
             Kind ( String ): 是  资源类型，常见的有：
                 - ClusterRole
                 - ClusterRoleBinding
                 - ComponentStatus
                 - ConfigMap
                 - CronJob
                 - DaemonSet
                 - Deployment
                 - Endpoint
                 - EndpointSlice
                 - Event
                 - Ingress
                 - Job
                 - LimitRange
                 - Namespace
                 - Node
                 - PersistentVolume
                 - PersistentVolumeClaim
                 - PersistentVolumeSnapshot
                 - Pod
                 - PodDisruptionBudget
                 - ReplicationController
                 - ResourceQuota
                 - Role
                 - RoleBinding
                 - Secret
                 - Service
                 - ServiceAccount
                 - StatefulSet
                 - StorageClass
                 - VolumeAttachment
             Namespace ( String ): 否  资源所在的命名空间，当不指定时，默认查询所有命名空间的资源。
             LabelSelectors ( String ): 否  标签选择器。 
             FieldSelectors ( String ): 否  字段选择器。
             Limit ( Integer ): 否  分页查询时，每页返回的资源数量，默认 500。
    Returns: 
        反序列化后的资源数据（JSON 格式）
    """,
    "manage_k8s_resources": r"""
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Region: (String) 是  集群所属的地域，常见的地域代号示例如下，默认为 cn-beijing：
                   - cn-beijing：华北2（北京）
                   - cn-beijing2：华北3（北京）
                   - cn-datong：华北4（大同）
                   - cn-wulanchabu：华北5（乌兰察布）
                   - cn-shanghai：华东2（上海）
                   - cn-guangzhou：华南1（广州）
                   - cn-hongkong：中国香港
                   - ap-southeast-1：亚太东南（柔佛）
                   - ap-southeast-3：亚太东南（雅加达）
             ClusterId ( String ): 是  集群 ID。
             ApiVersion ( String ): 是  API 版本，常见的有：
                 - v1
                 - apps/v1
                 - batch/v1
                 - authentication.k8s.io/v1
                 - events.k8s.io/v1
                 - networking.k8s.io/v1
                 - discovery.k8s.io/v1
                 - coordination.k8s.io/v1
                 - scheduling.k8s.io/v1
                 - storage.k8s.io/v1
             Kind ( String ): 是  资源类型，常见的有：
                 - ClusterRole
                 - ClusterRoleBinding
                 - ComponentStatus
                 - ConfigMap
                 - CronJob
                 - DaemonSet
                 - Deployment
                 - Endpoint
                 - EndpointSlice
                 - Event
                 - Ingress
                 - Job
                 - LimitRange
                 - Namespace
                 - Node
                 - PersistentVolume
                 - PersistentVolumeClaim
                 - PersistentVolumeSnapshot
                 - Pod
                 - PodDisruptionBudget
                 - ReplicationController
                 - ResourceQuota
                 - Role
                 - RoleBinding
                 - Secret
                 - Service
                 - ServiceAccount
                 - StatefulSet
                 - StorageClass
                 - VolumeAttachment
             Method ( String ): 是  操作方法，参数值说明：
                 - POST：创建资源。
                 - PUT：更新资源。
                 - DELETE：删除资源。
                 - PATCH：部分更新资源。
             Namespace ( String ): 否  资源所在的命名空间。
             Name ( String ): 否  资源名称, 仅在 Method 为 PUT、PATCH、DELETE 时必填。
             Body ( JSON ): 否  资源的 JSON 数据, 仅在 Method 为 POST、PUT、PATCH 时必填。
    Returns: 
        反序列化后的资源数据（JSON 格式） 
    """,
    "apply_yaml": r"""
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Region: (String) 是  集群所属的地域，常见的地域代号示例如下，默认为 cn-beijing：
                   - cn-beijing：华北2（北京）
                   - cn-beijing2：华北3（北京）
                   - cn-datong：华北4（大同）
                   - cn-wulanchabu：华北5（乌兰察布）
                   - cn-shanghai：华东2（上海）
                   - cn-guangzhou：华南1（广州）
                   - cn-hongkong：中国香港
                   - ap-southeast-1：亚太东南（柔佛）
                   - ap-southeast-3：亚太东南（雅加达）
             ClusterId ( String ): 是  集群 ID。
             Content ( String ): 是  资源的 YAML 数据。
             Force ( Boolean ): 否  是否强制更新资源，默认 False。
    Returns: 
        反序列化后的资源数据（JSON 格式） 
    """,
    "list_virtual_nodes": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
       body: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Filter ( Object of VirtualNodesFilter ): 否  待查询虚拟节点的筛选条件。 
            PageNumber ( Integer ): 否  分页查询时的起始页码，从 1 开始，默认为 1。 
            PageSize ( Integer ): 否  分页查询时每页显示的记录数，取值： 
                  - 最小值：1 
                  - 最大值：100 
                  - 默认值：10 
           "字段"： VirtualNodesFilter
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Ids ( Array of String ): 否  虚拟节点 ID 列表。 
                  单次最多填写 10 个虚拟节点 ID。 
            Name ( String ): 否  虚拟节点名称，支持模糊匹配。 
                  此参数为空时，返回指定地域内所有的虚拟节点信息。 
            Statuses ( Array of VirtualNodeStatusFilterRequest ): 否  虚拟节点的状态。 
                  单次最多填写 15 个数组元素。传入多个状态时，状态间是逻辑 或 关系。 
           "字段"： VirtualNodeStatusFilterRequest
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Phase ( String ): 否  虚拟节点的状态，枚举值如下： 
                      - Creating：创建中 
                      - Running：运行中 
                      - Deleting：删除中 
                      - Failed：异常 
            Conditions.Type ( String ): 否  虚拟节点当前主状态下的状态条件，即进入该主状态的原因，可以有多个原因，取值： 
                      - Progressing：处理中 
                      - Ok：正常 
                      - Unavailable：异常 
                      - CreateFailed：创建失败 
                      - Unknown：未知错误 
    """,
    "create_virtual_node": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
       body: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            ClientToken ( String ): 否  用于保证请求幂等性的字符串。该字符串由调用方传入，需保证不同请求之间唯一。ClientToken 对大小写敏感，且最大值不超过 64 个 ASCII 字符。 
            Name ( String ): 否  虚拟节点的名称。 
                  - 同一私有网络（VPC）下，虚拟节点名称必须唯一。 
                  - 支持大小写英文字母、数字、短划线（-），长度限制为 2～64 个字符 
                  - 该名称仅是虚拟节点的显示名称，不等于 Kubernetes 中的node.name。 
                  - 若不设置，系统以vci-vnode-格式命名虚拟节点的名称。 
            Kubeconfig ( String ): 是  虚拟节点要连接的目标 Kubernetes 集群的 Kubeconfig。 
                  需要对 Kubeconfig 进行 Base 64 编码后传入。Base 64 编码相关注意事项，请参见 FAQ。 
            VirtualNodeConfig ( Object of VirtualNodeConfig ): 是  虚拟节点的节点配置信息。 
            KubernetesConfig ( Object of VirtualNodeKubernetesConfigRequest ): 否  虚拟节点的 Kubernetes 配置信息。 
           "字段"： VirtualNodeConfig
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            VpcId ( String ): 是  VPC ID, 需确保 VPC 与目标用户 k8s 集群网络联通 
            SubnetIds ( Array of String ): 是  VPC 内子网 ID 信息，用于 vk 组件部署，所有 subnet 需属于同一 az，最对 5 个 
            SecurityGroupIds ( Array of String ): 是  VPC 内安全组 ID 信息，vnode ENI 和 VCI 会默认加入该组 
           "字段"： VirtualNodeKubernetesConfigRequest
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Labels ( Array of Label ): 否  虚拟节点的 Kubernetes 标签（Labels）信息。 
            Taints ( Array of Taint ): 否  虚拟节点的 Kubernetes 污点（Taints）信息。 
            ClusterDns ( Array of String ): 否  DNS 服务器的 IP 地址数组。如果 VCI Pod 中设置了dnsPolicy=ClusterFirst，则使用该配置值为容器提供 DNS 服务。 
            ClusterDomain ( String ): 否  集群的域名。配置后，除了主机的搜索域外，还会配置这里指定的域名到所有容器。 
           "字段"： Label
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Key ( String ): 是  标签键，要求如下，更多规则，请参见 Kubernetes 标签规则。 
                  有效的标签键有两个段：和，用斜杠（/）分隔。 
                  * 是必须的，支持英文大小写字母、数字、短划线（-）、下划线（_）、英文句号（ .），以字母或数字开头和结尾，长度不超过 63 个字符。 
                  * 是可选的。如果指定，则必须是 DNS 子域：由英文句号（.）分隔的一系列 DNS 标签，长度不超过 253 个字符。 
                  * 和总长度不超过 82 个字符。 
            Value ( String ): 否  标签值，要求如下，更多规则，请参见 Kubernetes 标签规则。 
                  * 长度不超过 63 个字符（可以为空）。 
                  * 支持以英文大小写字母、数字开头和结尾。 
                  * 支持特殊字符：短划线（-）、下划线（_）、英文句号（.）。 
           "字段"： Taint
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            Key ( String ): 是  污点键 
            Value ( String ): 否  污点值 
            Effect ( String ): 否  污点效果，取值： 
                      - NoSchedule（默认值）：一定不能被调度 
                      - PreferNoSchedule：尽量不要调度 
                      - NoExecute：不仅不会调度，还会驱逐Node上已有的Pod 
    """,
}
