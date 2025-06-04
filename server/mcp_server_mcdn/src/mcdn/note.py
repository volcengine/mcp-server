note = {
    "list_cloud_accounts": r""" 
    Args: 
        body: A JSON structure
             Vendor ( String ): 否  指定一个云服务商，查询属于该云服务商的账号。该参数有以下取值： 
                   - builtin：内置加速 
                   - aliyun：阿里云 
                   - tencent：腾讯云 
                   - ksyun：金山云 
                   - huawei：华为云 
                   - volcengine：火山引擎 
                   - wangsu：网宿科技 
                   - qiniu：七牛云 
                   - ucloud：UCloud 
                   - akamai：Akamai 
                   - baishan：白山云 
                   - aws：AWS 
                   - baidu：百度智能云 
                   - jingdong：京东云 
                   - gcp：Google Cloud 
                   - chinamobile：中国移动 
                   - ctcdn：天翼云CDN+ 
                   - azure：Azure 
                   - cloudflare：Cloudflare 
             Pagination ( Object of PagingOption ): 否  对查询结果进行分页并返回特定页码上的云服务商账号。 
             ReadOnly ( Boolean ): 否  是否只返回开启了只读访问模式的云服务商账号。默认值：false。 
             Name ( String ): 否  指定一个云服务商账号的名称，查询该账号的信息。 
             SyncStatus ( String ): 否  指定一个同步状态，查询最近一次域名同步结果为特定状态的云服务商账号。该参数有以下取值： 
                   - Successful：同步成功 
                   - Failed：同步失败 
                   - Syncing：正在同步 
             SortBy ( Array of String ): 否  设置返回的云服务商账号的排序方式。该参数有以下取值： 
                   - CreatedAt：按创建时间进行升序排序 
                   - UpdatedAt：按最新一次更新时间进行升序排序 
                   - LastSyncAt：按最近一次域名同步时间进行升序排序 
                   - -CreatedAt（默认）：按创建时间进行降序排序 
                   - -UpdatedAt：按最新一次更新时间进行降序排序 
                   - -LastSyncAt：按最近一次域名同步时间进行降序排序 
                   支持设置多个排序方式，不同排序方式的优先级由设置的顺序决定。例如，["-CreatedAt", "UpdatedAt"]表示优先按照创建时间进行降序排序，其次按照更新时间进行升序排序。 
             VendorType ( String ): 否  要查询的账号的类型。该参数有以下取值： 
                   - Vendor（默认）：查询您添加到多云CDN的第三方云服务商账号。 
                   - BuiltIn：查询内置加速服务所属账号。 
                   - All：查询所有账号，包含第三方云服务商账号和内置加速服务所属账号。 
            "字段"： PagingOption
             PageSize ( Long ): 是  每页包含云服务商账号的数量。最大值：100。 
             PageNum ( Long ): 是  云服务商账号所在页码。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        CloudAccounts ( Array of CloudAccountForList ):  
        Pagination ( Object of PagingResult ):  
       "字段"： CloudAccountForList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Id ( String ): 655372daa21faa599668** 
        Name ( String ): volctest 
        Vendor ( String ): volcengine 
        SyncStatus ( String ): Successful 
        CreatedAt ( Long ): 1665628799 
        UpdatedAt ( Long ): 1665628799 
        Extra ( Object of CloudAccountExtra ):  
        StatSettings ( Object of CloudAccountStatSettings ):  
        ContentSettings ( Object of CloudAccountContentSettings ):  
        DomainSettings ( Object of CloudAccountDomainSettings ):  
        SubProducts ( Array of String ): cdn 
        SelfHostProxyEndpoint ( String ): http://.com:3888 
        LastSyncAt ( Long ): 1708496441 
        ReadOnly ( Boolean ): true 
        CloudAccountVendorPermission ( String ): Ok 
        TopAccountId ( String ): 210023XXXX 
        PermissionState ( Object of CloudAccountVendorPermissionState ):  
        SyncStatusState ( Object of CloudAccountSyncStatusState ):  
       "字段"： PagingResult
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        PageSize ( Long ): 10 
        PageNum ( Long ): 1 
        Total ( Long ): 1 
       "字段"： CloudAccountExtra
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        ProductId ( String ): 6zz3aln** 
        AkamaiEndpoint ( String ): akab-jln56zz3a2excugg-e6g6th53rn5c**.luna.akamaiapis.net 
        AccessToken ( String ): - 
        GcpType ( String ): - 
        RefreshToken ( String ): - 
        TenantId ( String ): - 
        WangsuAkSkEnabled ( Boolean ): true 
       "字段"： CloudAccountStatSettings
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Aws ( Object of AwsStatSetting ):  
        OfflineDataSetting ( Object of OfflineDataSetting ):  
       "字段"： CloudAccountContentSettings
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Aws ( Object of AwsContentSetting ):  
       "字段"： CloudAccountDomainSettings
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        UCloud ( Object of UCloudDomainSettings ):  
       "字段"： CloudAccountVendorPermissionState
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        ListApiStatus ( String ): Ok 
       "字段"： CloudAccountSyncStatusState
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        DomainSyncStatusState ( Object of SyncStatusState ):  
        StatSyncStatusState ( Object of SyncStatusState ):  
       "字段"： AwsStatSetting
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Enabled ( Boolean ): true 
        Endpoint ( String ): https://hmrfda**.execute-api.us-east-1.amazonaws.com/prod/metric 
        ApiKey ( String ): q3mxsbRw982dwEHsL50ld9VzdGdVjj757N1V** 
       "字段"： OfflineDataSetting
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Enabled ( Boolean ): true 
        SubProducts ( Array of String ): cdn 
       "字段"： AwsContentSetting
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Preload ( Object of AwsPreloadContentSetting ):  
       "字段"： UCloudDomainSettings
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        ProjectId ( String ): ln56zz3** 
       "字段"： SyncStatusState
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        SyncStatus ( String ): Successful 
        LastSyncAt ( Long ): 1708676776 
       "字段"： AwsPreloadContentSetting
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Enabled ( Boolean ): true 
        SubmitEndpoint ( String ): https://8tdrp1**.execute-api.ap-southeast-1.amazonaws.com/prod/ 
        QueryEndpoint ( String ): https://ovqy95**.execute-api.ap-southeast-1.amazonaws.com/prod/ 
        ApiKey ( String ): q3mxsbRw982dwEHsL50ld9VzdGdVjj757N1V** 
    """,
    "list_cdn_domains": r""" 
    Args: 
        body: A JSON structure
             Name ( String ): 否  指定一个加速域名，查询与该域名模糊匹配的加速域名的信息。 
             CdnType ( Array of String ): 否  指定一个或多个业务类型，查询具有该业务类型属性的加速域名。该参数有以下取值： 
                   - Download：大文件下载加速 
                   - Video：音视频点播加速 
                   - Web：网页/小文件加速 
                   - Dynamic：动态与静态内容混合加速 
                   - Live：直播加速 
                   - Default：未配置 
             Vendor ( Array of String ): 否  指定一个或多个云服务商，查询属于指定云服务商的加速域名。该参数有以下取值： 
                   - builtin：内置加速 
                   - aliyun：阿里云 
                   - tencent：腾讯云 
                   - ksyun：金山云 
                   - huawei：华为云 
                   - volcengine：火山引擎 
                   - wangsu：网宿科技 
                   - qiniu：七牛云 
                   - ucloud：UCloud 
                   - akamai：Akamai 
                   - baishan：白山云 
                   - aws：AWS 
                   - baidu：百度智能云 
                   - jingdong：京东云 
                   - gcp：Google Cloud 
                   - chinamobile：中国移动 
                   - ctcdn：天翼云CDN+ 
                   - azure：Azure 
                   - cloudflare：Cloudflare 
             Status ( Array of String ): 否  指定一个或多个状态，查询处于指定状态的加速域名。该参数有以下取值： 
                   - Deleting：删除中 
                   - Deploying：部署中 
                   - DeployingFailed：部署失败 
                   - Locked：已封禁 
                   - Locking：封禁中 
                   - Offline：已停用 
                   - Online：已启用 
                   - ReviewFailed：审核失败 
                   - Reviewing：审核中 
                   - Stopping：停用中 
             Region ( Array of String ): 否  指定一个或多个加速区域，查询具有该加速区域属性的加速域名。该参数有以下取值： 
                   - Domestic：中国内地 
                   - Global：全球 
                   - OverSea：全球（不含中国内地） 
             CloudAccountId ( String ): 否  指定一个云服务商账号的 ID，查询通过该账号同步的加速域名。 
                   账号 ID 是多云CDN为云服务商账号生成的唯一 ID。只用于多云CDN平台。您可以调用 ListCloudAccounts 接口查询所有云服务商账号的 ID。 
             ExactName ( String ): 否  指定一个加速域名，查询与该域名精确匹配的加速域名的信息。 
             Pagination ( Object of PagingOption ): 否  对查询结果进行分页并返回特定页码上的加速域名。 
             BizNodeIds ( Array of String ): 否  指定一个或多个多云CDN业务节点的 ID，查询属于指定业务的加速域名。 
                   “业务”是多云CDN用来对资源进行分组和权限管理的工具。更多信息，请参见权限管理。 
             TagFilters ( Array of Tag ): 否  指定一个或多个标签，查询与指定标签关联的加速域名。多个标签之间使用“逻辑与”方式连接（即与所有标签都匹配才算满足条件）。 
             ScheduleCreated ( Boolean ): 否  是否只查询开启多云流量调度的域名。默认值为 false。 
            "字段"： PagingOption
             PageSize ( Long ): 是  指定每页包含加速域名的数量。取值范围：1~100。 
             PageNum ( Long ): 是  指定要返回的页码。 
            "字段"： Tag
             Key ( String ): 是  标签 Key。 
             Value ( String ): 是  标签 Value。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Domains ( Array of Domain ):  
        Pagination ( Object of PagingResult ):  
       "字段"： Domain
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Id ( String ): 654a20acbd82bac3e2c6** 
        Name ( String ): www.example.com 
        Cname ( String ): www.example.com.volcgslb.com 
        Status ( String ): Online 
        CdnType ( String ): Web 
        Vendor ( String ): volcengine 
        Region ( String ): Domestic 
        TopAccountId ( String ): 210023XXXX 
        CloudAccountId ( String ): 6596badbd262c2b7220b** 
        CloudAccountName ( String ): volctest 
        Tags ( Array of Tag ):  
        SubProduct ( String ): cdn 
        BizNodeId ( String ): 65098b4f78287dcda3be** 
        BizNodeName ( String ): 未分组 
        BizNodePath ( String ): /未分组 
        SyncedAt ( String ): 2024-01-11T17:26:02+08:00 
        ScheduleCreated ( Boolean ): true 
        VendorId ( String ): aeadf2de79d04f6794704922190c** 
        CreatedAt ( String ): 2022-08-02T10:28:13Z 
        UpdatedAt ( String ): 2024-01-10T18:30:29Z 
        ImportedAt ( String ): 2023-11-07T19:33:58+08:00 
        Certificates ( Array of Certificate ):  
        Networks ( Array of Network ):  
       "字段"： PagingResult
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        PageSize ( Long ): 10 
        PageNum ( Long ): 1 
        Total ( Long ): 2 
       "字段"： Tag
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Key ( String ): biz 
        Value ( String ): web 
       "字段"： Certificate
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Id ( String ): mcdntest 
        Name ( String ): mcdntest 
        StartTime ( String ): 2023-06-30T08:00:00+08:00 
        ExpireTime ( String ): 2024-06-30T07:59:59+08:00 
        FingerprintSha1 ( String ): fe357a975e25f1a536c56c77f852399b423b8727 
        FingerprintSha256 ( String ): 5b9566783da171972c46c74a35d5aa50f13fd40290c69b5a383fb5b061c72f1a 
        CommonName ( String ): *.example.com 
        SubjectAlternativeNames ( Array of String ): *.example.com,example.com 
        region ( String ): - 
        Status ( String ): Ok 
        SyncDetail ( Object of SyncDetail ):  
        VolcIds ( Array of String ): cert-0dc7e5dfbf954bf2952ea98746fd** 
        VolcIdsSyncDetail ( Object of SyncDetail ):  
       "字段"： Network
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Type ( String ): Cname 
        Value ( String ): www.example.com.volcgslb.com 
       "字段"： SyncDetail
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        SyncedAt ( String ): 2024-03-04T19:02:10+08:00 
    """,
    "describe_cdn_domain_config": r""" 
    Args: 
        params: A JSON structure
             DomainName ( String ): 否  @ignoredeprecated, 域名名称。 
             Vendor ( String ): 否  @ignoredeprecated, 云厂商名称。 
             DomainId ( String ): 否  域名Id 
             NormalizeOptions ( Array of String ): 否  @ignore响应格式化选项 
             DomainVersion ( String ): 否  请求的域名配置版本 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Domain ( Object of DomainDetailConfig ):  
        Components ( Array of Resource ):  
        FieldAnnotations ( JSON Map ):  
        DomainVersion ( String ):  
       "字段"： DomainDetailConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Id ( String ):  
        Name ( String ):  
        Tags ( Array of Tag ):  
        Cname ( String ):  
        Region ( String ):  
        Status ( String ):  
        Vendor ( String ):  
        CdnType ( String ):  
        Origins ( Array of OriginEndpoint ):  
        SslHsts ( Object of SslHstsConfig ):  
        CacheTtl ( Object of CacheTtlConfig ):  
        Compress ( Object of CompressConfig ):  
        Networks ( Array of Network ):  
        SyncedAt ( String ):  
        VendorId ( String ):  
        BizNodeId ( String ):  
        CreatedAt ( String ):  
        Schedules ( Array of String ):  
        SslAccess ( Object of SslAccessConfig ):  
        UpdatedAt ( String ):  
        ErrorPages ( Array of ErrorPageRule ):  
        ImportedAt ( String ):  
        OriginHost ( Object of OriginHostConfig ):  
        OriginPath ( String ):  
        ScheduleId ( String ):  
        SubProduct ( String ):  
        SyncStatus ( String ):  
        BizNodeName ( String ):  
        BizNodePath ( String ):  
        DnsSchedule ( Object of DnsSchedule ):  
        ProtocolSsl ( Object of ProtocolSslConfig ):  
        VolcProject ( String ):  
        Certificates ( Array of Certificate ):  
        IpAccessRule ( Object of IpAccessRule ):  
        OriginSslSni ( Object of OriginSslSniConfig ):  
        ProtocolIpv6 ( Object of ProtocolIpv6Config ):  
        ProtocolQuic ( Object of ProtocolQuicConfig ):  
        TopAccountId ( String ):  
        UaAccessRule ( Object of UaAccessRule ):  
        CacheKeyQuery ( Object of CacheKeyQueryConfig ):  
        ProtocolHttp2 ( Object of ProtocolHttp2Config ):  
        VendorCdnType ( String ):  
        CloudAccountId ( String ):  
        ConditionRules ( Array of ConditionRule ):  
        OriginHttpPort ( Long ):  
        OriginProtocol ( String ):  
        SslCertificate ( Object of SslServerCertificateConfig ):  
        OriginHttpsPort ( Long ):  
        OriginTimeoutMs ( Long ):  
        ScheduleCreated ( Boolean ):  
        SslOcspStapling ( Object of SslOcspStaplingConfig ):  
        CloudAccountName ( String ):  
        ConfigSyncDetail ( Object of SyncDetail ):  
        OriginLoadBalance ( Object of OriginLoadBalanceConfig ):  
        ProtocolWebSocket ( Object of ProtocolWebSocketConfig ):  
        RefererAccessRule ( Object of RefererAccessRule ):  
        OriginRangeRequest ( Object of OriginRangeRequestConfig ):  
        RequestUrlRewrites ( Array of RequestUrlRewriteRule ):  
        ResponseHeaderCors ( Object of ResponseHeaderCorsConfig ):  
        ErrorCodeCacheRules ( Array of ErrorCodeCacheRule ):  
        OriginReadTimeoutMs ( Long ):  
        OriginSendTimeoutMs ( Long ):  
        OriginFollowRedirect ( Object of OriginFollowRedirectConfig ):  
        RequestHeaderRewrites ( Array of HeaderRewriteRule ):  
        OriginConnectTimeoutMs ( Long ):  
        OriginRequestArgFilter ( Object of ArgFilterConfig ):  
        ResponseHeaderRewrites ( Array of HeaderRewriteRule ):  
        OriginRequestArgRewrites ( Array of ArgRewriteRule ):  
        OriginRequestUrlRewrites ( Array of UrlRewriteRule ):  
        OriginRequestHeaderFilter ( Object of OriginRequestHeaderConfig ):  
        OriginRequestHeaderRewrites ( Array of HeaderRewriteRule ):  
        OriginResponseHeaderRewrites ( Array of HeaderRewriteRule ):  
       "字段"： Resource
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Id ( String ):  
        Name ( String ):  
        Type ( String ):  
        Attributes ( Object of ResourceAttribute ):  
       "字段"： FieldAnnotations
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Error ( String ):  
        Comment ( String ):  
        Capability ( String ):  
       "字段"： Tag
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Key ( String ): biz 
        Value ( String ): web 
       "字段"： OriginEndpoint
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Host ( Object of OriginHostConfig ):  
        Path ( String ):  
        Type ( String ):  
        AwsS3 ( Object of OriginAwsS3Config ):  
        JDOss ( Object of OriginJDOssConfig ):  
        SslSni ( Object of OriginSslSniConfig ):  
        Weight ( Long ):  
        Address ( String ):  
        VolcTos ( Object of OriginVolcTosConfig ):  
        BaiduBos ( Object of OriginBaiduBosConfig ):  
        HttpPort ( Long ):  
        Priority ( Long ):  
        Protocol ( String ):  
        AliyunOss ( Object of OriginAliyunOssConfig ):  
        HttpsPort ( Long ):  
        HuaweiObs ( Object of OriginHuaweiObsConfig ):  
        QiniuKodo ( Object of OriginQiniuKodoConfig ):  
        TimeoutMs ( Long ):  
        TencentCos ( Object of OriginTencentCosConfig ):  
        ReadTimeoutMs ( Long ):  
        SendTimeoutMs ( Long ):  
        ConnectTimeoutMs ( Long ):  
       "字段"： SslHstsConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Mode ( String ):  
        MaxAge ( Long ):  
        IncludeSubDomains ( String ):  
       "字段"： CacheTtlConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        MaxTtl ( Long ):  
        MinTtl ( Long ):  
        DefaultTtl ( Long ):  
       "字段"： CompressConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Mode ( String ):  
        MaxSize ( Long ):  
        MinSize ( Long ):  
        Algorithms ( Array of String ):  
       "字段"： Network
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Type ( String ): Cname 
        Value ( String ): www.example.com.volcgslb.com 
       "字段"： SslAccessConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Mode ( String ):  
        RedirectCode ( String ):  
       "字段"： ErrorPageRule
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        ErrorCode ( String ):  
        ResponseCode ( String ):  
        ResponsePage ( String ):  
       "字段"： OriginHostConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Mode ( String ):  
        HeaderHost ( String ):  
       "字段"： DnsSchedule
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Id ( String ):  
        Cname ( String ):  
        Status ( String ):  
        IsEnabledStatus ( Boolean ):  
       "字段"： ProtocolSslConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Mode ( String ):  
        ProtocolVersions ( Array of String ):  
       "字段"： Certificate
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Id ( String ): mcdntest 
        Name ( String ): mcdntest 
        StartTime ( String ): 2023-06-30T08:00:00+08:00 
        ExpireTime ( String ): 2024-06-30T07:59:59+08:00 
        FingerprintSha1 ( String ): fe357a975e25f1a536c56c77f852399b423b8727 
        FingerprintSha256 ( String ): 5b9566783da171972c46c74a35d5aa50f13fd40290c69b5a383fb5b061c72f1a 
        CommonName ( String ): *.example.com 
        SubjectAlternativeNames ( Array of String ): *.example.com,example.com 
        region ( String ): - 
        Status ( String ): Ok 
        SyncDetail ( Object of SyncDetail ):  
        VolcIds ( Array of String ): cert-0dc7e5dfbf954bf2952ea98746fd** 
        VolcIdsSyncDetail ( Object of SyncDetail ):  
       "字段"： IpAccessRule
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Values ( Array of String ):  
        ReturnCode ( String ):  
        MatchOperator ( String ):  
        RedirectLocation ( String ):  
       "字段"： OriginSslSniConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Mode ( String ):  
        ServerName ( String ):  
       "字段"： ProtocolIpv6Config
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Mode ( String ):  
       "字段"： ProtocolQuicConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Mode ( String ):  
       "字段"： UaAccessRule
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Values ( Array of String ):  
        AllowEmpty ( String ):  
        ReturnCode ( String ):  
        MatchOperator ( String ):  
        RedirectLocation ( String ):  
       "字段"： CacheKeyQueryConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Keys ( Array of String ):  
        Mode ( String ):  
        Reorder ( String ):  
        IgnoreCase ( String ):  
       "字段"： ProtocolHttp2Config
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Mode ( String ):  
       "字段"： ConditionRule
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Configs ( Object of CdnConfig ):  
        Conditions ( Array of Condition ):  
       "字段"： SslServerCertificateConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Id ( String ):  
        Name ( String ):  
       "字段"： SslOcspStaplingConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Mode ( String ):  
       "字段"： SyncDetail
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        SyncedAt ( String ): 2024-03-04T19:02:10+08:00 
       "字段"： OriginLoadBalanceConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Mode ( String ):  
       "字段"： ProtocolWebSocketConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Mode ( String ):  
       "字段"： RefererAccessRule
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Values ( Array of String ):  
        AllowEmpty ( String ):  
        ReturnCode ( String ):  
        CheckScheme ( String ):  
        MatchOperator ( String ):  
        RedirectLocation ( String ):  
        IncludeSubDomains ( String ):  
       "字段"： OriginRangeRequestConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Mode ( String ):  
       "字段"： RequestUrlRewriteRule
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Break ( String ):  
        Field ( String ):  
        DstHost ( String ):  
        DstValue ( String ):  
        SrcValue ( String ):  
        MatchMode ( String ):  
        DstProtocol ( String ):  
        MatchOption ( Object of UrlMatchOption ):  
        RedirectCode ( String ):  
       "字段"： ResponseHeaderCorsConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        AccessControlMaxAge ( Long ):  
        AccessControlAllowHeaders ( Array of String ):  
        AccessControlAllowMethods ( Array of String ):  
        AccessControlAllowOrigins ( Array of String ):  
        AccessControlExposeHeaders ( Array of String ):  
        AccessControlAllowCredentials ( String ):  
       "字段"： ErrorCodeCacheRule
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        MaxTtl ( Long ):  
        MinTtl ( Long ):  
        ErrorCode ( String ):  
        DefaultTtl ( Long ):  
       "字段"： OriginFollowRedirectConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Mode ( String ):  
        MaxTries ( Long ):  
        FollowCodes ( Array of String ):  
       "字段"： HeaderRewriteRule
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Field ( String ):  
        DstValue ( String ):  
        SrcValue ( String ):  
        MatchOption ( Object of RewriteMatchOption ):  
       "字段"： ArgFilterConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Keys ( Array of String ):  
        Mode ( String ):  
       "字段"： ArgRewriteRule
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Field ( String ):  
        DstValue ( String ):  
        SrcValue ( String ):  
       "字段"： UrlRewriteRule
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Break ( String ):  
        Field ( String ):  
        DstValue ( String ):  
        SrcValue ( String ):  
        MatchMode ( String ):  
        MatchOption ( Object of UrlMatchOption ):  
       "字段"： OriginRequestHeaderConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Mode ( String ):  
        Headers ( Array of String ):  
       "字段"： ResourceAttribute
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Value ( File ):  
        References ( Array of Reference ):  
       "字段"： OriginAwsS3Config
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        AccessKey ( String ):  
        SecretKey ( String ):  
        AccessIdentity ( String ):  
       "字段"： OriginJDOssConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        AccessKey ( String ):  
        SecretKey ( String ):  
        PrivateAccess ( String ):  
       "字段"： OriginVolcTosConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        AccessKey ( String ):  
        SecretKey ( String ):  
        PrivateAccess ( String ):  
       "字段"： OriginBaiduBosConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        AccessKey ( String ):  
        SecretKey ( String ):  
        PrivateAccess ( String ):  
       "字段"： OriginAliyunOssConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        AccessKey ( String ):  
        SecretKey ( String ):  
        PrivateAccess ( String ):  
       "字段"： OriginHuaweiObsConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        AccessKey ( String ):  
        SecretKey ( String ):  
        PrivateAccess ( String ):  
       "字段"： OriginQiniuKodoConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        AccessKey ( String ):  
        SecretKey ( String ):  
        PrivateAccess ( String ):  
       "字段"： OriginTencentCosConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        AccessKey ( String ):  
        SecretKey ( String ):  
        PrivateAccess ( String ):  
       "字段"： CdnConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Origins ( Array of OriginEndpoint ):  
        SslHsts ( Object of SslHstsConfig ):  
        CacheTtl ( Object of CacheTtlConfig ):  
        Compress ( Object of CompressConfig ):  
        SslAccess ( Object of SslAccessConfig ):  
        ErrorPages ( Array of ErrorPageRule ):  
        OriginHost ( Object of OriginHostConfig ):  
        OriginPath ( String ):  
        ProtocolSsl ( Object of ProtocolSslConfig ):  
        IpAccessRule ( Object of IpAccessRule ):  
        OriginSslSni ( Object of OriginSslSniConfig ):  
        ProtocolIpv6 ( Object of ProtocolIpv6Config ):  
        ProtocolQuic ( Object of ProtocolQuicConfig ):  
        UaAccessRule ( Object of UaAccessRule ):  
        CacheKeyQuery ( Object of CacheKeyQueryConfig ):  
        ProtocolHttp2 ( Object of ProtocolHttp2Config ):  
        OriginHttpPort ( Long ):  
        OriginProtocol ( String ):  
        SslCertificate ( Object of SslServerCertificateConfig ):  
        OriginHttpsPort ( Long ):  
        OriginTimeoutMs ( Long ):  
        SslOcspStapling ( Object of SslOcspStaplingConfig ):  
        OriginLoadBalance ( Object of OriginLoadBalanceConfig ):  
        ProtocolWebSocket ( Object of ProtocolWebSocketConfig ):  
        RefererAccessRule ( Object of RefererAccessRule ):  
        OriginRangeRequest ( Object of OriginRangeRequestConfig ):  
        RequestUrlRewrites ( Array of RequestUrlRewriteRule ):  
        ResponseHeaderCors ( Object of ResponseHeaderCorsConfig ):  
        ErrorCodeCacheRules ( Array of ErrorCodeCacheRule ):  
        OriginReadTimeoutMs ( Long ):  
        OriginSendTimeoutMs ( Long ):  
        OriginFollowRedirect ( Object of OriginFollowRedirectConfig ):  
        RequestHeaderRewrites ( Array of HeaderRewriteRule ):  
        OriginConnectTimeoutMs ( Long ):  
        OriginRequestArgFilter ( Object of ArgFilterConfig ):  
        ResponseHeaderRewrites ( Array of HeaderRewriteRule ):  
        OriginRequestArgRewrites ( Array of ArgRewriteRule ):  
        OriginRequestUrlRewrites ( Array of UrlRewriteRule ):  
        OriginRequestHeaderFilter ( Object of OriginRequestHeaderConfig ):  
        OriginRequestHeaderRewrites ( Array of HeaderRewriteRule ):  
        OriginResponseHeaderRewrites ( Array of HeaderRewriteRule ):  
       "字段"： Condition
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Or ( Array of Condition ):  
        Field ( String ):  
        Values ( Array of String ):  
        Operator ( String ):  
        FieldType ( String ):  
        MatchMode ( String ):  
        MatchOption ( Object of MatchOption ):  
       "字段"： UrlMatchOption
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        MatchPart ( String ):  
        IgnoreCase ( String ):  
       "字段"： RewriteMatchOption
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        MatchMultiple ( String ):  
       "字段"： Reference
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        RefPath ( String ):  
        FieldPath ( String ):  
        RefStateId ( String ):  
       "字段"： MatchOption
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        IgnoreCase ( String ):  
    """,
    "describe_cdn_access_log": r""" 
    Args: 
        body: A JSON structure
             StartTime ( Long ): 是  指定一个时间段的起点，查询时间段内（包含起点）的日志。使用时间戳表示，单位为秒。 
                   不同云服务商平台允许查询的日志时间范围不同。若您设置的时间起点不符合云服务商平台的要求（超出最长可查询时间），那么日志查询请求会失败。更多信息，请参见日志查询限制。 
             EndTime ( Long ): 是  指定一个时间段的终点，查询时间段内（不包含终点）的数据。使用时间戳表示，单位为秒。 
                   不同云服务商平台允许查询的日志时间跨度不同。若您设置的时间段不符合云服务商平台的要求（超出允许的时间跨度），那么日志查询请求会失败。更多信息，请参见日志查询限制。 
             Domain ( String ): 否  指定要查询的加速域名。 
                   - Domain 和 DomainId 不允许同时为空，否则日志查询请求会失败。 
                   - 如果您指定了 Domain，则必须同时指定 Vendor 和 SubProduct。 
             Vendor ( String ): 否  指定一个云服务商，向该云服务商平台发起日志查询请求。 
                   如果您指定了 Domain，则必须同时指定 Vendor 和 SubProduct。 
                   该参数有以下取值： 
                   - builtin：内置加速 
                   - aliyun：阿里云 
                   - tencent：腾讯云 
                   - ksyun：金山云 
                   - huawei：华为云 
                   - volcengine：火山引擎 
                   - wangsu：网宿科技 
                   - qiniu：七牛云 
                   - ucloud：UCloud 
                   - akamai：Akamai 
                   - baishan：白山云 
                   - aws：AWS 
                   - baidu：百度智能云 
                   - jingdong：京东云 
                   - gcp：Google Cloud 
                   - chinamobile：中国移动 
                   - ctcdn：天翼云CDN+ 
                   - azure：Azure 
                   - cloudflare：Cloudflare 
             DomainId ( String ): 否  指定要查询的加速域名的 ID。 
                   - 您可以调用 ListCdnDomains 接口查询所有加速域名的 ID。 
                   - 如果您指定了 DomainId，则不能指定 Domain、Vendor 和 SubProduct。 
             SubProduct ( String ): 否  指定一个产品类型。 
                   如果您指定了 Domain，则必须同时指定 Vendor 和 SubProduct。 
                   该参数有以下取值： 
                   - cdn（默认）：内容分发网络（CDN） 
                   - ucdn：UCloud UCDN 
                   - cloudfront：AWS CloudFront 
                   - amd：Akamai AMD 
                   - dsa：Akamai DSA 
                   - media_cdn：Google Cloud Media CDN 
                   - dcdn：全站加速（DCDN） 
                   - ecdn：腾讯云 ECDN 
                   - edgeone：腾讯云 EdgeOne 
             Pagination ( Object of PagingOption ): 否  对查询结果进行分页并返回特定页码上的访问日志。 
            "字段"： PagingOption
             PageSize ( Long ): 是  指定每页包含访问日志的数量。默认值是 10，最大值是 100。 
             PageNum ( Long ): 是  指定要返回的页码。默认值为 1。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Logs ( Array of AccessLogElement ):  
        Pagination ( Object of PagingResult ):  
       "字段"： AccessLogElement
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Domain ( String ): www.example.com 
        LogInfos ( Array of LogInfo ):  
       "字段"： PagingResult
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        PageSize ( Long ): 1 
        PageNum ( Long ): 1 
        Total ( Long ): 168 
       "字段"： LogInfo
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Url ( String ): cdnlog-sh-public.oss-cn-shanghai.aliyuncs.com/v1.l1cache/200027584/www.example.com/2024_10_05/www.example.com_2024_10_05_000000_010000.gz?Expires=1729318755&OSSAccessKeyId=LTAIviCc6zy8x3xa&Signature=**TdX9Xzj5rxDW%2BwLuAH8%3D 
        Size ( Long ): 176774 
        FileName ( String ): www.example.com_2024_10_05_000000_010000.gz 
        StartTime ( Long ): 1728057600 
        EndTime ( Long ): 1728061200 
    """,
    "describe_cdn_region_and_isp": r""" 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Isps ( Array of NamePair ):  
        Countries ( Array of Country ):  
       "字段"： NamePair
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        CnName ( String ): 电信 
        EnName ( String ): TELECOM 
       "字段"： Country
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        NamePair ( Object of NamePair ):  
        Regions ( Array of NamePair ):  
    """,
    "describe_cdn_data_offline": r""" 
    Args: 
        body: A JSON structure
             StartTime ( Long ): 是  指定一个时间段的起点，查询该时间段内（包含起点）的数据。使用时间戳表示，单位为秒。 
                   时间段按照您设置的 Interval 值向前规整。示例：假设 Interval 为 5 分钟（对应秒级时间戳 300），那么 1644163200 和 1644163499 都会规整为 1644163200。 
             EndTime ( Long ): 是  指定一个时间段的终点，查询该时间段内（不包含终点）的数据。使用时间戳表示，单位为秒。 
                   时间段按照您设置的 Interval 值向前规整。示例：假设 Interval 为 5 分钟（对应秒级时间戳 300），那么 1644163200 和 1644163499 都会规整为 1644163200。 
             Metric ( String ): 是  指定一个要查询的指标。该参数有以下取值： 
                   - flux：流量（byte） 
                   - bandwidth：带宽（bps） 
                   - request: 请求数 
                   - status_all：2xx、3xx、4xx、5xx 状态码的汇总数量 
                   - status_2xx：2xx 状态码的汇总数量和某个具体 2xx 状态码（如 200、201 等）的数量 
                   - status_3xx：3xx 状态码的汇总数量和某个具体 3xx 状态码（如 301、302 等）的数量 
                   - status_4xx：4xx 状态码的汇总数量和某个具体 4xx 状态码（如 400、404 等）的数量 
                   - status_5xx：5xx 状态码的汇总数量和某个具体 5xx 状态码（如 500、502 等）的数量 
                   - hitrate: 流量命中率（ %，保留两位小数） 
                   - request_hitrate：请求命中率（ %，保留两位小数） 
             Interval ( String ): 是  指定返回数据的时间间隔。该参数有以下取值： 
                   - 1min：每 1 分钟返回一个数据。查询的时间段必须在 1 天内，才支持该取值。 
                   - 5min：每 5 分钟返回一个数据。查询的时间段必须在 31 天内，才支持该取值。 
                   - hour：每 1 小时返回一个数据。查询的时间段必须在 90 天内，才支持该取值。 
                   - day：每 1 天返回一个数据。查询的时间段至少为 2 天，且最多为 90 天，才支持该取值。 
             Vendors ( Array of String ): 否  指定一个或多个云服务商，查询对应云服务商的数据。多个云服务商间使用半角逗号（,）分隔。默认返回所有云服务商的数据。该参数有以下取值： 
                   - builtin：内置加速 
                   - aliyun：阿里云 
                   - tencent：腾讯云 
                   - ksyun：金山云 
                   - huawei：华为云 
                   - volcengine：火山引擎 
                   - wangsu：网宿科技 
                   - qiniu：七牛云 
                   - ucloud：UCloud 
                   - akamai：Akamai 
                   - baishan：白山云 
                   - aws：AWS 
                   - baidu：百度智能云 
                   - jingdong：京东云 
                   - gcp：Google Cloud 
                   - chinamobile：中国移动 
                   - ctcdn：天翼云CDN+ 
                   - azure：Azure 
                   - cloudflare：Cloudflare 
             CloudAccountIds ( Array of String ): 否  指定一个或多个云服务商的账号 ID，查询对应云服务商账号的数据。多个账号 ID 间使用半角逗号（,）分隔。默认返回所有账号的数据。 
                   账号 ID 是您将云服务商账号添加到多云CDN后，多云CDN为账号分配的唯一 ID。您可以调用 ListCloudAccounts 接口获取所有云服务商账号 ID。 
             SubProducts ( Array of String ): 否  指定一个或多个产品类型，查询对应产品的数据。多个产品类型间使用半角逗号（,）分隔。默认返回云服务商下所有支持的产品的数据。该参数有以下取值： 
                   - cdn：内容分发网络（CDN） 
                   - ucdn：UCloud UCDN 
                   - cloudfront：AWS CloudFront 
                   - amd：Akamai AMD 
                   - dsa：Akamai DSA 
                   - media_cdn：Google Cloud Media CDN 
                   - dcdn：全站加速（DCDN） 
                   - ecdn：腾讯云 ECDN 
                   - edgeone：腾讯云 EdgeOne 
             CdnTypes ( Array of String ): 否  指定一个或多个业务类型，查询对应业务类型的数据。多个业务类型间使用半角逗号（,）分隔。默认返回云服务商下所有业务类型的数据。该参数有以下取值： 
                   - Web：网页/小文件加速 
                   - Video：音视频点播加速 
                   - Download：大文件下载加速 
                   - Dynamic：动态加速 
                   - Hybrid：混合加速 
                   - Live：直播加速 
                   - Default：未配置 
             Domains ( Array of String ): 否  指定一个或多个加速域名，查询对应加速域名的数据。多个加速域名间使用半角逗号（,）分隔。最多允许设置 50 个加速域名。默认返回所有加速域名的数据。 
                   您可以调用 ListCdnDomains 接口获取所有加速域名。 
             DomainIds ( Array of String ): 否  指定一个或多个加速域名的 ID，查询对应加速域名的数据。多个加速域名 ID 间使用半角逗号（,）分隔。最多允许设置 50 个加速域名 ID。默认返回所有加速域名的数据。 
                   加速域名 ID 是多云CDN为（从云服务商平台同步的）加速域名分配的唯一标识符。加速域名 ID 在“云服务商/云产品/域名”维度是唯一的。您可以调用 ListCdnDomains 接口获取所有加速域名的 ID。 
             GroupBy ( String ): 否  指定一种返回数据的分组方式。默认返回汇总数据，即不对数据进行分组。该参数有以下取值： 
                   - vendor：按云服务商对数据分组 
                   - cloud_account_id：按云服务商账号对数据分组 
                   - sub_product：按子产品类型对数据分组 
                   - cdn_type：按业务类型对数据分组 
                   - domain：按域名对数据分组（仅在 Domains 不为空时支持该取值） 
                   - domain_id：按域名 ID 对数据分组（仅在 DomainIds 不为空时支持该取值） 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Resources ( Array of ResourceStatData ):  
       "字段"： ResourceStatData
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Name ( String ): total 
        Metrics ( Array of MetricStatData ):  
       "字段"： MetricStatData
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Metric ( String ): flux 
        Values ( Array of TimeSeriesData ):  
       "字段"： TimeSeriesData
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Timestamp ( Long ): 1704038400 
        Value ( Double ): 41914513357 
    """,
    "describe_cdn_origin_data_offline": r""" 
    Args: 
        body: A JSON structure
             StartTime ( Long ): 是  指定一个时间段的起点，查询该时间段内（包含起点）的数据。使用时间戳表示，单位为秒。 
                   时间段按照您设置的 Interval 值向前规整。示例：假设 Interval 为 5 分钟（对应秒级时间戳 300），那么 1644163200 和 1644163499 都会规整为 1644163200。 
             EndTime ( Long ): 是  指定一个时间段的终点，查询该时间段内（不包含终点）的数据。使用时间戳表示，单位为秒。 
                   时间段按照您设置的 Interval 值向前规整。示例：假设 Interval 为 5 分钟（对应秒级时间戳 300），那么 1644163200 和 1644163499 都会规整为 1644163200。 
             Metric ( String ): 是  指定一个要查询的指标。该参数有以下取值： 
                   - flux：流量（byte） 
                   - bandwidth：带宽（bps） 
                   - request: 请求数 
                   - status_all：2xx、3xx、4xx、5xx 状态码的汇总数量 
                   - status_2xx：2xx 状态码的汇总数量和某个具体 2xx 状态码（如 200、201 等）的数量 
                   - status_3xx：3xx 状态码的汇总数量和某个具体 3xx 状态码（如 301、302 等）的数量 
                   - status_4xx：4xx 状态码的汇总数量和某个具体 4xx 状态码（如 400、404 等）的数量 
                   - status_5xx：5xx 状态码的汇总数量和某个具体 5xx 状态码（如 500、502 等）的数量 
             Interval ( String ): 是  指定返回数据的时间间隔。该参数有以下取值： 
                   - 1min：每 1 分钟返回一个数据。查询的时间段必须在 1 天内，才支持该取值。 
                   - 5min：每 5 分钟返回一个数据。查询的时间段必须在 31 天内，才支持该取值。 
                   - hour：每 1 小时返回一个数据。查询的时间段必须在 90 天内，才支持该取值。 
                   - day：每 1 天返回一个数据。查询的时间段至少为 2 天，且最多为 90 天，才支持该取值。 
             Vendors ( Array of String ): 否  指定一个或多个云服务商，查询对应云服务商的数据。多个云服务商间使用半角逗号（,）分隔。默认返回所有云服务商的数据。该参数有以下取值： 
                   - builtin：内置加速 
                   - aliyun：阿里云 
                   - tencent：腾讯云 
                   - ksyun：金山云 
                   - huawei：华为云 
                   - volcengine：火山引擎 
                   - wangsu：网宿科技 
                   - qiniu：七牛云 
                   - ucloud：UCloud 
                   - akamai：Akamai 
                   - baishan：白山云 
                   - aws：AWS 
                   - baidu：百度智能云 
                   - jingdong：京东云 
                   - gcp：Google Cloud 
                   - chinamobile：中国移动 
                   - ctcdn：天翼云CDN+ 
                   - azure：Azure 
                   - cloudflare：Cloudflare 
             CloudAccountIds ( Array of String ): 否  指定一个或多个云服务商的账号 ID，查询对应云服务商账号的数据。多个账号 ID 间使用半角逗号（,）分隔。默认返回所有账号的数据。 
                   账号 ID 是您将云服务商账号添加到多云CDN后，多云CDN为账号分配的唯一 ID。您可以调用 ListCloudAccounts 接口获取所有云服务商账号 ID。 
             SubProducts ( Array of String ): 否  指定一个或多个子产品类型，查询对应子产品的数据。多个子产品类型间使用半角逗号（,）分隔。默认返回云服务商下所有子产品的数据。该参数有以下取值： 
                   - cdn：内容分发网络（CDN） 
                   - ucdn：UCloud UCDN 
                   - cloudfront：AWS CloudFront 
                   - amd：Akamai AMD 
                   - dsa：Akamai DSA 
                   - media_cdn：Google Cloud Media CDN 
                   - dcdn：全站加速（DCDN） 
                   - ecdn：腾讯云 ECDN 
                   - edgeone：腾讯云 EdgeOne 
             CdnTypes ( Array of String ): 否  指定一个或多个业务类型，查询对应业务类型的数据。多个业务类型间使用半角逗号（,）分隔。默认返回云服务商下所有业务类型的数据。该参数有以下取值： 
                   - Web：网页/小文件加速 
                   - Video：音视频点播加速 
                   - Download：大文件下载加速 
                   - Dynamic：动态加速 
                   - Hybrid：混合加速 
                   - Live：直播加速 
                   - Default：未配置 
             Domains ( Array of String ): 否  指定一个或多个域名，查询对应域名的数据。多个域名间使用半角逗号（,）分隔。最多允许设置 50 个域名。默认返回所有域名的数据。 
                   您可以调用 ListCdnDomains 接口获取所有域名。 
             DomainIds ( Array of String ): 否  指定一个或多个域名的 ID，查询对应域名的数据。多个域名 ID 间使用半角逗号（,）分隔。最多允许设置 50 个域名 ID。默认返回所有域名的数据。 
                   加速域名 ID 是多云CDN为（从云服务商平台同步的）加速域名分配的唯一标识符。加速域名 ID 在“云服务商/云产品/域名”维度是唯一的。您可以调用 ListCdnDomains 接口获取所有域名的 ID。 
             GroupBy ( String ): 否  指定一种返回数据的分组方式。默认返回汇总数据，即不对数据进行分组。该参数有以下取值： 
                   - vendor：按云服务商对数据分组 
                   - cloud_account_id：按云服务商账号对数据分组 
                   - sub_product：按子产品类型对数据分组 
                   - cdn_type：按业务类型对数据分组 
                   - domain：按域名对数据分组（仅在 Domains 不为空时支持该取值） 
                   - domain_id：按域名 ID 对数据分组（仅在 DomainIds 不为空时支持该取值） 
             IsTrimLatestData ( Boolean ): 否  是否剔除最新的数据点不完整的数据。默认值为 false。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Resources ( Array of ResourceStatData ):  
       "字段"： ResourceStatData
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Name ( String ): total 
        Metrics ( Array of MetricStatData ):  
       "字段"： MetricStatData
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Metric ( String ): flux 
        Values ( Array of TimeSeriesData ):  
       "字段"： TimeSeriesData
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Timestamp ( Long ): 1704038400 
        Value ( Double ): 41914513357 
    """,
}
