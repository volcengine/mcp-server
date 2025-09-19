note = {
    "list_domain_config": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Domains ( Array of String ): 否  待查询的加速域名列表。匹配规则为模糊匹配。当域名匹配到其中任一个关键字时，就会返回对应数据。如域名列表["abc.com","abc.cn"]，关键词为abc，由于dabc.com 包含 abc.com，dabc.cn 包含 abc.cn，所以 dabc.com、dabc.cn会匹配到，返回对应数据。但是 abcd.com、abcd.cn不会匹配到。 
             HTTPs ( Boolean ): 否  过滤参数，查询的域名是否开启了 HTTPS 功能 
             Keyword ( String ): 否  过滤参数，查询的域名是否包含该关键字，可以用来模糊匹配加速域名。 
             OriginType ( Array of String ): 否  过滤参数，查询的域名的源站所属类型，支持参数范围： 
                   - IP：IP 源站 
                   - Domain：域名源站 
                   - IP_Domain：同时包含 IP 和域名源站 
                   - TOS：TOS 源站 
                   - ALB：ALB 源站 
                   - GA：GA 源站 
             PageNumber ( Integer ): 否  分页参数，页码，大于0小于100000，不输入时默认为1。 
             PageSize ( Integer ): 否  分页参数，页大小，大于0小于10000，不输入或输入为0时默认为查询所有域名。 
             ProjectName ( Array of String ): 否  过滤参数，查询的域名所在的项目列表范围 
             Scope ( Array of String ): 否  过滤参数，加速区域。取值： 
                   - domestic：中国大陆。 
                   - overseas：中国大陆以外区域。 
                   - global：全球。 
             Status ( Array of String ): 否  过滤参数，查询的域名当前所处的范围，取值范围如下： 
                   - Stop：已停止 
                   - Deploy：部署中 
                   - Started：运行中 
             TimeSortOrder ( String ): 否  设置返回的域名列表按照创建时间排序规则，默认后创建的域名排序靠前（降序），支持参数范围： 
                   - descending：创建时间降序 
                   - ascending：创建时间升序 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        DomainConfigs ( Array of DomainConfigs ): 返回的域名详细信息。 
        Total ( Integer ): 对应筛选条件下的域名总数。 
       "字段"： DomainConfigs
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Domain ( String ): 待查询的加速域名列表，匹配规则为模糊匹配，当域名匹配到其中任一个关键字时，就会返回对应数据。如域名列表[abc.com,abc.cn] ，关键词为abc，由于dabc.com 包含 abc.com，dabc.cn 包含 abc.cn，所以 dabc.com、dabc.cn会匹配到，返回对应数据。但是 abcd.com、abcd.cn不会匹配到。 
        ProjectName ( String ): 当前域名所归属的项目。 
        StrategyType ( String ): 回源策略，支持取值： 
            - wrr：加权轮询。 
            - optimum：按照健康度选择最优源站。 
        Scope ( String ): 加速区域（访问用户所在的区域），当前仅对白名单用户开放。详细信息，请见修改基础配置。取值： 
            - domestic（默认值）：中国大陆。 
            - overseas：中国大陆以外区域。 
            - global：全球。 
        Cname ( String ): 全站加速为加速域名生成的 CNAME。 
        IsCNAMEResolved ( Boolean ): 加速域名是否被成功解析到全站加速提供的 CNAME，取值： 
            - true：已解析。 
            - false：未解析。 
            对于每个加速域名，您需要在您对应的 DNS 服务提供商处添加一条与加速域名同名的 CNAME 记录，将其值指向全站加速为您创建的 CNAME。具体操作请参考配置CNAME解析。全站加速如果能够将您的加速域名解析到对应的 CNAME 时，此选项会被设为 true。 
        RecordFiling ( String ): 当前域名备案状态，取值： 
            - success：域名备案状态有效。 
            - fail：域名备案状态失效。 
            - recovery：域名备案状态从有效转为失效。 
        UserName ( String ): 加速域名所属的用户 ID 。 
        Status ( String ): 加速域名的状态，取值： 
            - Started：运行中。 
            - Deploy：部署中。 
            - Stop：已停止。 
        CreateTime ( String ): 创建加速域名的时间。时间格式遵循 RFC 3339 规范。 
        UpdateTime ( String ): 最近更新加速域名的时间。时间格式遵循 RFC 3339 规范。 
        Origin ( Object of Origin ): 源站配置。 
        Https ( Object of Https ): HTTPS 加速配置。 
        EnableFailOver ( Boolean ): 是否开启主备容灾功能，默认不启用，支持取值： 
            - true：启用。 
            - false：不启用。 
        IPv6Switch ( Boolean ): 是否开启 IPv6 功能，客户端和边缘节点通过 IPv6 协议通信。默认不启用，支持取值： 
            - true：启用。 
            - false：不启用。 
        Cache ( Object of Cache ): 缓存配置。 
        UrlRedirect ( Object of UrlRedirect ): URL 重定向相关配置。当客户端请求资源的 URL 和全站加速节点上缓存的 URL 不一致时，您可以进行 URL 重定向。 
        IpAccess ( Object of IpAccess ): Ip 访问黑/白名单。为了解决恶意 IP 盗刷、攻击等问题，需要对访问来源进行限制，您可以在全站加速控制台配置 IP 黑白名单。 
        UserAgentAccess ( Object of UserAgentAccess ): 基于客户端 UserAgent 的访问黑/白名单。如果您希望通过对用户 HTTP 请求头中的 User-Agent 字段进行规则判断，从而基于客户端类型进行过滤，您可以配置 User-Agent 黑白名单。 
        RefererAccess ( Object of RefererAccess ): 基于 Referer 访问黑/白名单。为了防止网站资源被盗用，您可以配置 Referer 防盗链。 
        UrlAccess ( Object of UrlAccess ): URL 鉴权。为了保护站点资源，避免资源被恶意下载盗用，您还可以通过配置 URL 鉴权，达到防止资源被非法下载盗用、提升内容安全性的目的。 
        WebSocket ( Object of WebSocket ): WebSockect 相关配置。当您处于服务端主动推送数据信息到客户端、实时通讯性要求高的业务场景时，可以选择开启 WebSocket 服务。 
        GzipCompress ( Object of GzipCompress ): Gzip 压缩。开启 Gzip 压缩后，全站加速在返回内容时会对资源进行 Gzip 压缩，缩减静态内容尺寸，从而缩短传输时间。 
        BrCompress ( Object of BrCompress ): Brotli 压缩。开启 Brotli 压缩后，全站加速在返回内容时会对资源进行 Brotli，缩减静态内容尺寸，从而缩短传输时间。当客户端和全站加速同时都支持 Gzip 压缩和 Brotli 压缩时，Brotli 压缩会被优先采用。 
        StaticOptimization ( Object of StaticOptimization ): 页面性能优化。HTTP/2 协议多路复用场景下，通过调整缓冲区策略，控制静态资源请求优先级，实现静态页面加载性能优化。 
        PreConnect ( Object of PreConnect ): 预连接。开启后预连接后，DCDN服务主动与源站建立连接，维护连接池，提高回源连接复用率，缩短访问链路耗时。 
            预连接不会向源站发送 HTTP 请求，不会引起额外的请求数费用。开启后可能对源站造成 5～20Mbps 带宽增长，建议评估源站带宽容量后再开启。 
        RTTOptimize ( Object of RTTOptimize ): 回源链路择优。开启回源链路择优后，DCDN服务会选择最优的RTT链路回源，缩短访问链路耗时。 
        ResourceTags ( Array of ResourceTags ): 绑定在该域名上的资源标签（Tag）信息。 
        ServiceType ( String ): 该加速域名关联的加速场景，取值： 
            - ai：AI 加速 
            - upload：上传加速 
            - page：页面加速 
            - api：API 加速 
            - other：其他 
        UploadOptimize ( Object of UploadOptimize ): 上传协议优化。开启上传协议优化后，全站加速通过自研协议栈优化策略，提升文件接收和传输性能。 
       "字段"： Origin
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Origins ( Array of Origins ): 主源站列表，全站加速允许源站列表同时包含 IP 源站和域名源站。 
        OriginSni ( Object of OriginSni ): 在回源协议为 HTTPS 时有效。对于源站单 IP 多域名的场景，边缘节点在建立安全连接时候，需要向源站发送 SNI 来指定需要访问的域名（以便核对服务器端证书）。此配置允许您设置回源时发送的 SNI。 
        OriginRange ( Object of OriginRange ): Range 回源相关配置。对于支持 Range 传输的源站，可以开启此能力，仅仅向源站请求客户端请求的部分文件。该功能可以提高大文件分发效率。 
        OriginType ( String ): 主源站类型，支持参数： 
            - IP：IP 源站。 
            - Domain：域名源站。 
            - IP_Domain：同时包含 IP 源站和域名源站。 
            - TOS：对象存储源站。 
            - ALB：负载均衡 ALB 源站 
            - GA：全球加速源站。 
        OriginProtocolType ( String ): 回源协议，支持参数： 
            - http：忽略客户端的请求方式，边缘节点会强制采用 HTTP 回源。 
            - https：忽略客户端的请求方式，边缘节点会强制 HTTPS 回源。 
            - follow：边缘节点的回源方式与客户端的请求协议保持一致。 
        RequestHeader ( Object of RequestHeader ): 回源请求头相关配置。全站加速回源时，会透传用户的请求头。该配置允许您自定义回源请求头设置，比如删除、添加、修改已有请求头的值。 
        ResponseHeader ( Object of ResponseHeader ): HTTP 响应头相关配置。当用户请求资源时，全站加速会对返回的响应头进行自定义的修改，影响客户程序（如浏览器）的响应行为。 
        TosPrivateAccess ( Boolean ): OriginType 为 TOS 时，您可以设置源站是否被允许访问私有 bucket。您需要先授权 DCDN 访问该私有 Bucket 的权限后，才可开启此配置。支持取值： 
            - true：启用。 
            - false：不启用。 
        BackupOrigins ( Array of BackupOrigins ): 备源站列表，全站加速允许源站列表同时包括 IP 源站与域名源站，开启主备容灾时该选项有效。最多配置 50 条记录。源站类型为对象存储时，不支持备源站设置。 
        BackupOriginType ( String ): 备源站类型，开启主备容灾时必填，支持参数： 
            - IP：IP 源站。 
            - Domain：域名源站。 
            - IP_Domain：同时包含 IP 源站和域名源站。 
        ResponseTimeout ( Integer ): 回源超时时间，单位为秒，最大值为900。默认值为10。 
        OriginHost ( Object of OriginHost ): 自定义回源访问的具体站点域名。源站获取资源的站点与加速域名的站点不一致时，您可以通过配置回源 HOST 指明资源所在站点。 
        ConditionalOrigins ( Array of ConditionalOrigins ): 条件源站配置。 
        FollowRedirect ( Object of FollowRedirect ): 回源重定向跟随配置。 
        GAOriginProbe ( Object of GAOriginProbe ): OriginType 为 GA 时，GA源站探测配置信息。 
        OriginIPv6 ( Object of OriginIPv6 ): IPv6回源配置。 
            - 您成功添加一个加速域名后，全站加速默认的回源方式是仅使用 IPv4 协议访问源站。 
            - 源站类型全部为 IP 地址时，至少有一个源站支持 IPv4 协议。 
            - 您必须开启 IPv6回源 功能后，选择一个回源方式，全站加速按照您配置的回源方式使用 IPv6 协议访问源站。 
        PrivateBucketAuth ( Object of PrivateBucketAuth ): 表示访问第三方云厂商的对象存储私有存储桶的权限设置。该对象仅当 OriginType是 TOS 时有效。该配置指定了全站加速在回源第三方私有存储桶时提交的认证身份配置（如 AccessKey ID 及 AccessKey Secret） 
       "字段"： Https
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        EnableHttps ( Boolean ): 是否启用 HTTPS，默认根据证书的绑定自动打开，如果绑定证书时不想启用 HTTPS，需要将该参数设置为 false。取值： 
            - true：启用。 
            - false：不启用。 
        Http2 ( Boolean ): 是否启用 HTTP2，默认不启用，开启前需要先开启 HTTPS 设置。取值： 
            - true：启用。 
            - false：不启用。 
        Hsts ( Object of Hsts ): HSTS 配置。开启前需要先开启 HTTPS 设置。开启后，全站加速响应增加 Strict-Transport-Security 头部，减少被劫持的风险。 
        TlsVersions ( Object of TlsVersions ): TlS 版本配置。支持选择 TLS V1.0-V1.3 版本。 
        CertBind ( Object of CertBind ): HTTPS 证书配置（服务器证书），绑定证书的情况下，HTTPS、HSTS、ForceRedirect等功能才能开启。 
        ForceRedirect ( Object of ForceRedirect ): 强制跳转配置。开启前请先配置 HTTPS 证书，将客户端到全站加速的请求方式强制重定向为 HTTP 或 HTTPS，默认通过返回状态码 301 跳转。 
        QUICSwitch ( Boolean ): 是否开启 QUIC，开启前需要先开启 HTTPS 设置，开启后支持客户端以 QUIC 协议访问服务，开启 QUIC前，请确认域名已完成证书配置。默认不启用，支持取值： 
            - true：启用。 
            - false：不启用。 
        HTTPSClientCert ( Object of HTTPSClientCert ): 边缘双向认证的相关配置。在启用了 HTTPS 之后，允许边缘节点与客户端建立安全通信的时候，启用双向认证（同时认证客户端证书）以获得更高的安全性。 
            此功能仅向特定用户开放，如需使用该功能，请 提交工单。 
        OCSPStapling ( Boolean ): OCSP Stapling 配置，启用该配置后，可提高客户端 TLS 握手效率，节省了在 TLS 握手阶段客户端通过OCSP验证证书的时间。 
       "字段"： Cache
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否启用缓存功能，默认不启用，支持取值： 
            - true：启用。 
            - false：不启用。 
        AdaptCache ( Boolean ): 是否启用自适应缓存功能，默认不启用，支持取值： 
            - true：启用。 
            - false：不启用。 
            	自适应缓存只有当您没有配置自定义规则或者当用户请求未能匹配任何自定义规则时生效。 
        CacheRules ( Array of CacheRules ): - 缓存规则配置，启用缓存功能且未开启自适应缓存时必选。 
            - 指您可以设置源站静态内容在边缘节点的缓存过期时间。这样可以设定边缘节点缓存的内容在多长时间后过期。过期后，节点需要重新回源获取该内容。 
        CacheKeyRules ( Array of CacheKeyRules ): 缓存键配置规则。指示边缘节点在缓存静态内容时，是否会去除请求 URL 中的参数。 
            - 缓存键规则定义了全站加速生成和匹配缓存键的方法。 
            - 当请求 URL 中的查询参数不影响文件内容的获取时，建议您将缓存键规则中的参数规则设置为忽略全部。这样可提高请求的命中率，减少边缘节点的回源次数。 
            - 全站加速默认有一条根目录缓存键规则，您不能修改规则类型和内容。 
        StatusCodeCacheRule ( Object of StatusCodeCacheRule ): 状态码缓存配置。 
            为了减轻源站处理请求的压力，您可以配置状态码缓存规则。这样边缘节点可以缓存特定的响应状态码，避免每次都返回源站获取相同的响应状态码。配置状态码缓存规则只在您配置了静态缓存规则时才会生效，未配置静态缓存规则时，状态码缓存规则不生效。 
       "字段"： UrlRedirect
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否启用 URL 重定向功能，默认不启用，取值： 
            - true：启用。 
            - false：不启用。 
        Rules ( Array of Rules ): URL 重定向相关配置。当 Enable 字段为 true 时，此选项必填。 
       "字段"： IpAccess
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否启用 IP 黑/白名单功能，默认不启用。取值： 
            - true：启用。 
            - false：不启用。 
        FilterType ( String ): 表示过滤行为为黑名单或白名单，当 Enable 字段为 true 时，此选项必填。取值： 
            - WhiteList：白名单列表，只有添加在白名单内的 IP 能访问加速域名下的资源。 
            - BlackList：黑名单列表，添加在黑名单内的 IP 无法访问加速域名下的资源。 
        FilterList ( Array of String ): IP 列表，支持配置 IP 地址和网段输入，多个 IP 通过换行分隔，最多输入100个。当 Enable 字段为 true 时，此选项必填。 
       "字段"： UserAgentAccess
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否启用 UserAgent 黑/白名单，默认不启用，取值：  
             - true：启用。  
             - false：不启用。 
        FilterType ( String ): 表示过滤行为为黑名单或白名单，当 Enable 字段为 true 时，此选项必填。选项： 
            - WhiteList：白名单列表，只有 HTTP 请求中的 User-Agent 字段匹配到白名单内的字段，用户才可以访问当前请求的资源。 
            - BlackList：黑名单列表，如果 HTTP 请求中的 User-Agent 字段匹配到黑名单内的字段，那么用户无法访问当前请求的资源。 
        FilterList ( Array of String ): UA 列表，当 Enable 字段为 true 时，此选项必填，支持通配符号“*”，多个字段通过换行分隔，最多输入100个。 
       "字段"： RefererAccess
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否启用 Referer 黑/白名单，默认不启用，取值： 
            - true：启用。 
            - false：不启用。 
        FilterType ( String ): 表示过滤行为为黑名单或白名单，当 Enable 字段为 true 时，此选项必填。选项： 
            - WhiteList：白名单列表，只有 HTTP 请求中的 Referer 内容匹配到白名单内容，用户才可以访问当前请求的资源。 
            - BlackList：黑名单列表，如果 HTTP 请求中的 Referer 内容匹配到黑名单内容，那么用户无法访问当前请求的资源。 
        AllowNone ( Boolean ): 是否允许 Referer 字段为空，默认不允许，即便当 Enable 字段为 true 时，本字段也可不填。取值： 
            - true：允许。 
            - false：不允许。 
        FilterList ( Array of String ): 具体 Referer 列表，当 Enable 字段为 true 时，此选项必填。具体规则： 
            - 支持泛域名和通配符号“*”，多个字段通过换行分隔，最多输入100个。 
            - 参数不应该带前缀（http://）或（https://）。 
            - 允许Filename配置，如允许您使用 referer 为 http://x.com，则 http://x.com/Filename 也符合规则。 
            - 前缀通配泛域名，如（*.b.baidu.com）需要加（.），则允许 referer 为 （http://[xx].b.baidu.com）。 
            - 后缀通配泛域名，如（b.baidu.com.*），需要加（.），则允许 referer 为（http://b.baidu.com.[xx]）。 
            - 当（）作为通配符时，不能满足泛域名的格式，此时将被认为是正则匹配。如（.a.com）会被当作泛域名，（a.*b.com）则会用正则表达式的规则匹配，可以匹配上（a.cab.com.）。 
            - 开启白名单时，则默认白名单列表中存在此加速域名。 
       "字段"： UrlAccess
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否开启 URL 鉴权，默认不启用，取值： 
            - true：启用。 
            - false：不启用。 
        GenType ( String ): 鉴权类型，从系统内置的签名公式里选一种，当 Enable 字段为 true 时，此选项生效。详见++配置 URL 鉴权++，取值： 
            - TypeA 
            - TypeB 
            - TypeC 
            - TypeD 
        GenKey ( String ): 鉴权密钥，支持6-40位大/小写字母、数字。当 Enable 字段为 true 时，此选项必填。 
        GenTTL ( Integer ): URL 有效时间，单位为秒，范围为：0~31536000。当 Enable 字段为 true 时，此选项生效。 
       "字段"： WebSocket
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否开启 WebSocket 协议，默认不启用，取值： 
            - true：启用。 
            - false：不启用。 
        Timeout ( Integer ): 超时时间，单位为秒。取值范围 [1，900]。当 Enable 字段为 true 时，此选项必填。 
       "字段"： GzipCompress
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否开启 Gzip 压缩配置，默认不启用，取值： 
            - true：启用。 
            - false：不启用。 
       "字段"： BrCompress
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否开启 Brotli 压缩配置，默认不启用，支持取值： 
            - true：启用。 
            - false：不启用。 
       "字段"： StaticOptimization
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        H2Priority ( Boolean ): 是否开启页面性能优化，默认不启用，支持取值： 
            - true：启用。 
            - false：不启用。 
       "字段"： PreConnect
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否开启预连接配置，默认不启用，取值： 
            - true：启用。 
            - false：不启用。 
       "字段"： RTTOptimize
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否开启回源链路择优，开启前需要先开启预连接，默认不启用，支持取值： 
            - true：启用。 
            - false：不启用。 
       "字段"： ResourceTags
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Key ( String ): 标签名称，支持大/小写字母、数字和中文组成，支持 +-=@/._ 等特殊字符，长度不超过 128 个字符，不允许以 volc 开头。 
        Value ( String ): 标签名称对应的值，由大/小写字母、数字和中文组成，支持"+-=@/._"等特殊字符，长度不超过 256 个字符。 
       "字段"： UploadOptimize
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否开启 上传协议优化配置，默认不启用，取值： 
            - true：启用。 
            - false：不启用。 
       "字段"： Origins
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Name ( String ): 源站地址，需要与您设置的源站类型一致（如：IP 或域名）。 
        Weight ( Integer ): 权重，您可为源站设置权重，有效范围为 0 - 100。且所有源站的权重之和不为0。 
        Port ( Integer ): 源站服务的端口。如：80、443。 
            不填时系统会自动根据回源协议选择默认值。 
            - 回源协议为 HTTP 时：回源端口为80。 
            - 回源协议为 HTTPS 时：回源端口为443。 
        Type ( String ): 当您的回源地址同时存在IP类型和域名类型时（OriginType 为 IP_Domain），该值表示源站地址的类型。 
       "字段"： OriginSni
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否启用回源 SNI，默认不启用，支持取值： 
            - true：启用。 
            - false：不启用。 
        SniInfo ( String ): SNI 域名。当 Enable 字段为 true 时，此选项生效。对于单 IP 多域名的场景，当回源协议为 HTTPS 时，需要指定回源 SNI 来指定具体访问的域名。 
       "字段"： OriginRange
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否启用 Range 回源，默认不启用，支持取值： 
            - true：启用。 
            - false：不启用。 
       "字段"： RequestHeader
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否启用，默认不启用，支持取值： 
            - true：启用。 
            - false：不启用。 
        HeaderInfo ( Array of HeaderInfo ): 回源请求头相关配置。当 Enable 为 true 时，此选项生效。全站加速回源时，会透传用户的请求头。并且遵循您自定义回源请求头设置，比如删除、添加、修改已有请求头的值。 
       "字段"： ResponseHeader
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否启用，默认不启用，支持取值： 
            - true：启用。 
            - false：不启用。 
        HeaderInfo ( Array of HeaderInfo ): 当Enable字段为true时，此选项有效。比如删除、添加、修改已有请求头的值，比如删除、添加、修改已有响应头字段。 
       "字段"： BackupOrigins
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Name ( String ): 源站地址，需要与您设置的源站类型一致（如：IP 或域名）。 
        Weight ( Integer ): 权重，您可为源站设置权重，有效范围为 0 - 100。且所有源站的权重之和不为0。 
        Port ( Integer ): 源站服务的端口。如：80、443。 
            不填时系统会自动根据回源协议选择默认值。 
            - 回源协议为 HTTP 时：回源端口为80。 
            - 回源协议为 HTTPS 时：回源端口为443。 
        Type ( String ): 当您的回源地址同时存在IP类型和域名类型时（BackupOriginType 为 IP_Domain），该值表示源站地址的类型。 
        Strategy ( String ): 当源站为域名时，您可自定义单源站策略。不填默认为轮询 
       "字段"： OriginHost
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否启用回源Host，默认不启用，但是源站类型为 TOS 时，默认启用。支持取值： 
            - true：启用。 
            - false：不启用。 
        HostInfo ( String ): Host 地址 。当Enable字段为true时，此选项生效。源站获取资源的站点与加速域名的站点不一致，您可以通过配置回源 HOST 指明资源所在站点。源站类型为 TOS 时，Host 地址默认为回源地址。 
       "字段"： ConditionalOrigins
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Name ( String ): 条件回源的主源站名称，同域名下需要不能重复，长度不能超过50。 
            条件源站名称标识着一组源站，修改时，需要携带该标识。 
        Origins ( Array of Origins ): 主源站列表，全站加速支持 IP 与域名源站混填，最多配置50条记录。 
        BackupOrigins ( Array of BackupOrigins ): 备源站列表，全站加速支持 IP 与域名源站混填，开启主备容灾时必填。最多配置50条记录。源站类型为对象存储时，不支持备源站设置。 
        MatchingRuleGroup ( Object of MatchingRuleGroup ): 匹配条件组。 
       "字段"： FollowRedirect
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 跟随重定向功能开关，默认不启用，支持取值： 
            - true：启用。 
            - false：不启用。 
        MaxTries ( Integer ): 重定向最大跟随次数，取值范围为1～5。 
       "字段"： GAOriginProbe
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 仅在OriginType 为 GA 时生效。表示是否开启 GA 源站健康度探测配置，支持取值： 
            - true：开启 
            - false：不开启。 
        Host ( String ): 全球加速向源站发起探测请求时用的域名（GA 源站 URL 的域名部分）。不能填写特殊符号。 
        Url ( String ): 当Enable字段为true时，此选项生效。表示 GA 源站用来健康度检查的目标 URL 路径（不包含域名部分），不能填写特殊符号，必须使用/开头。 
       "字段"： OriginIPv6
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 回源 IPv6 开关，默认不开启，取值： 
            - true：开启。 
            - false：不开启。 
        Strategy ( String ): 当Enable字段为true时，此选项生效。表示回源 IPv6 策略，取值： 
            - ipv6_first：IPv6优先，边缘节点优先使用 IPv6 协议访问 IPv6 源站。如果没有 IPv6 源站，则访问 IPv4 源站。 
            - ipv4_first：IPv4优先，边缘节点优先使用 IPv4 协议访问 IPv4 源站。如果没有 IPv4 源站，则访问 IPv6 源站。 
            - ipv4v6_lb：IPv4和IPv6负载均衡模式，边缘节点以轮询的方式访问源站（IPv4 源站、IPv6 源站）。如果 IPv4 源站、IPv6 源站设置了权重，那么边缘节点会按照权重的比例访问源站。 
            - followclient：跟随客户端协议模式。边缘节点使用的 IP 协议与客户端请求使用的 IP 协议相同。 
            	- 客户端请求使用 IPv6 协议，边缘节点优先使用 IPv6 协议访问 IPv6 源站。如果没有 IPv6 源站，则访问 IPv4 源站。 
            	- 客户端请求使用 IPv4 协议，边缘节点优先使用 IPv4 协议访问 IPv4 源站。如果没有 IPv4 源站，则访问 IPv6 源站。 
       "字段"： PrivateBucketAuth
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Switch ( Boolean ): 是否开启第三方云厂商的私有存储桶的访问验证请求。 
            - true: 表示对象存储服务是第三方云厂商的。 
            - false（默认值）: 表示对象存储服务不是第三方云厂商的。 
            	该参数的默认值是false。 
        AuthType ( String ): 表示对象存储源站所在的云厂商。当Switch为true，该参数生效。 
            该参数有以下取值: 
            - cos: 腾讯云。 
            - oss: 阿里云。 
            - aws: AWS。 
            - obs: 华为云。 
        TosAuthInformation ( Object of TosAuthInformation ): 表示访问第三方云厂商所需要的密钥。当TosPrivateAccess是true时,该参数为必填。 
       "字段"： Hsts
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否启用 HSTS，默认不启用。启用 HSTS 前，必须先启用 HTTPS。开启后，全站加速响应增加 Strict-Transport-Security 头部，在用户第一次成功建立 HTTPS 访问后，减少后续被被劫持的风险。取值： 
            - true：启用。 
            - false：不启用。 
            为保证 HSTS 功能的成功生效，要求客户端支持 HSTS 机制，同时客户端应该完成过一次 HTTPS 请求。因此，开启 HSTS 时系统将同时为您开启强制跳转功能，将 HTTP 请求重定向为 HTTPS 请求。后续在您指定的时间内，客户端对所有的请求都会只使用 HTTPS 协议。 
        IncludeSubDomain ( Boolean ): 是否包含该域名的子域名。默认不包含。EnableHttps 为 true 时生效。取值： 
            - true：包含。HSTS 启用对该域名的子域名同样生效。 
            - false：不包含。HSTS 启用对该域名的子域名不生效。 
        MaxAge ( Integer ): 开启 HSTS 功能后，您可以指定 HSTS 的过期时间。如果客户端成功完成了一次 HTTPS 请求，客户端会记住响应头中的 Strict-Transport-Security 字段。在您指定时间内，对接下来的全部请求，客户端都会强制使用 HTTPS 协议。单位：秒。支持取值：0-63072000。 
       "字段"： TlsVersions
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否启用 TLS 协议版本强制要求，默认不启用，取值： 
            - true：启用。 
            - false：不启用。 
        TlsVersion ( Array of String ): TLS 版本，输入版本需要连续，支持TLSv1、TLSv1.1、TLSv1.2、TLSv1.3。当 Enable 字段为 true 时，此选项生效。 
       "字段"： CertBind
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        CertSource ( String ): 证书托管位置。取值： 
            - volc：证书托管在火山引擎证书中心。如果您的证书还未在证书中心，您需要先将证书上传到证书中心。 
            - self：证书托管在 DCDN。（该功能仅对白名单用户开放。如需使用，请提交工单。） 
        CertId ( String ): 用于验证客户端证书的 CA 证书 ID。 
        CertName ( String ): 证书名称。 
        DeployStatus ( String ): 证书部署的状态，支持取值： 
            - Deployed：部署成功。 
            - Waiting：未部署。 
            - Deploying： 部署中。 
        DomainId ( String ): 绑定的加速域名 ID。 
        DomainName ( String ): 绑定的加速域名名称。 
        Expire ( String ): 证书过期时间。 
       "字段"： ForceRedirect
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否启用强制跳转，默认不启用，支持取值： 
            - true：启用。 
            - false：不启用。 
        RedirectType ( String ): 强制跳转访问协议类型，当 Enable 字段为 true 时，此选项必填。支持取值： 
            - http：访问协议强制跳转为 HTTP 协议。 
            - https：访问协议强制跳转为 HTTPS 协议。 
        RedirectCode ( Integer ): 强制跳转使用的状态码，默认使用 301。取值：301，302，307，308。 
            对于 301 和 302 状态码，即使原用户请求使用的方法不是 GET，某些早期浏览器可能会使用 GET 方法发送重定向请求。 
       "字段"： HTTPSClientCert
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否开启边缘双向认证。默认不开启。取值： 
            - true：表示边缘双向认证已启用。 
            - false：表示边缘双向认证已禁用。 
        CertBindClient ( Object of CertBindClient ): 客户端验证的证书配置。当 Enable 为 true 时，此选项生效。 
       "字段"： CacheRules
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Type ( String ): 缓存规则类型。您可以按照文件后缀、目录、文件全路径、首页、全路径正则表达式等方式来指定源站返回的数据内容，并对这部分数据设置缓存过期时间。取值： 
            - file：按文件名后缀匹配缓存。 
            - dir：按目录匹配缓存。 
            - all：按文件全路径匹配缓存。 
            - index：按首页匹配缓存。 
            - pcre：按全路径正则表达式匹配缓存。 
        Contents ( String ): 缓存规则内容主体，不同的缓存类型对应的缓存规则不同，详见配置缓存规则文档。 
            如果您开启了自适应缓存功能、同时设置了缓存规则，当源站返回的静态内容同时匹配自适应缓存规则、缓存规则时，那么边缘节点会优先按照缓存规则来缓存静态内容。更多关于不同缓存规则优先级的问题，请参见缓存规则的优先级。 
        Policy ( String ): 缓存策略，取值： 
            - default：默认策略，表示本规则优先遵循源站不缓存的响应头信息（Cache-Control:no-store 和 Cache-Control:private），然后再遵循全站加速的缓存配置规则。 
            - force：强制缓存，表示本规则完全遵循全站加速的缓存配置，忽略源站不缓存响应头信息（Cache-Control:no-store 和 Cache-Control:private）的情况。 
            - origin：源站优先，表示本规则优先遵循源站响应头信息（Cache-Control 以及 Expires）进行缓存和不缓存判断，再遵循全站加速的缓存策略。 
        CacheTime ( Float ): 缓存的过期时间的取值。 
            当达到设置的过期时间时，边缘节点上缓存的静态内容失效。此时客户端向边缘节点请求这一内容时，全站加速会在源站获取最新内容并按照规则将内容缓存在边缘节点中。 
            - 图片类型、应用下载类型等不经常更新的静态内容：建议您将缓存时间设置成30天以上。 
            - JS、CSS等频繁更新的静态内容：建议您根据实际需求设定缓存时间。 
            - PHP、JSP、ASP等动态内容：建议您将缓存时间设置成0秒，即边缘节点回源获取这些内容。 
        CacheTimeUnit ( String ): 缓存时间单位，取值： 
            - second：秒。 
            - minute：分。 
            - hour：小时。 
            - day：天。 
            - month：月。 
            - year：年。 
        IgnoreCase ( Boolean ): 表示全站加速在使用该规则匹配用户请求 URL 时是否忽略大小写，默认不忽略，取值： 
            - true：忽略。 
            - false：不忽略。 
        ParamsReserveList ( String ): 缓存参数列表，缓存键参数规则ParamsFilterType为part和excl时必选，不同参数用分号 ; 相隔。 
        IgnoreSetCookie ( Boolean ): 当源站返回Set-Cookie头部时，节点是否缓存该头部及body，默认为false。 
            - true：遵循用户自定义的节点缓存规则，命中后删除set-cookie头部 
            - false：关闭，遵循用户自定义的节点缓存规则 
            	建议用户开启该功能，不缓存set-cookie头部。 
       "字段"： CacheKeyRules
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Type ( String ): 缓存键规则类型，支持取值： 
            - file：文件名后缀。 
            - dir：目录。 
            - all：文件全路径。 
            - index：首页。 
            - pcre：全路径正则表达式。 
        Contents ( String ): 缓存键规则主体，不同的缓存键类型对应的缓存键规则不同，详见配置缓存键文档。 
        ParamsFilterType ( String ): 生成缓存键时URL中“?”之后的参数的缓存规则，默认保留全部，支持取值： 
            - ignore：忽略全部参数（过滤）。 
            - reserve：保留所有参数（不过滤）。 
            - part：保留部分参数。 
            - excl：去除部分参数。 
        IgnoreCase ( Boolean ): 表示配置的规则在匹配请求 URL 及生成缓存键时，是否忽略大小写，默认不忽略。取值： 
            - true：忽略。 
            - false：不忽略。 
        ParamsReserveList ( String ): 参数规则 ParamsFilterType 为 part（保留部分参数）或 excl（去除部分参数）时生效。表示缓存规则中需要排除或者需要保留的具体参数列表，以分号相隔。 
       "字段"： StatusCodeCacheRule
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Enable ( Boolean ): 是否启用状态码缓存功能，默认不启用，支持取值： 
            - true：启用。 
            - false：不启用。 
        Rules ( Array of Rules ): 状态码缓存规则。当 Enable 字段为 true 时，此选项生效。 
       "字段"： Rules
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Match ( String ): 待改写的 URL，当 Enable 字段为 true 时，此选项必填。具体规则如下： 
            - 以正斜线“/”开头的 URL 路径，不含 http:// 头及域名。 
            - 支持 PCRE 正则表达式，不包含前后“/”。 
        Replacement ( String ): 目标 URL，当 Enable 字段为 true 时，此选项必填。具体规则如下： 
            - 以正斜线“/”开头的 URL，不含 http:// 头及域名。 
       "字段"： HeaderInfo
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        HeaderMode ( Integer ): - 0：ADD，添加请求头。 
            - 1：SET，设置已有的请求头。 
            - 2：DELETE，删除对应的请求头。 
        HeaderName ( String ): RequestHeader 字段名称，具体规则如下： 
            - 名称不能重复。自定义请求头字段名称长度默认为 1 - 100 个字符，由数字 0 - 9、字符 a - z、A - Z，及特殊符 - 组成，连字符 - 不能出现在名称的头部或者尾部。不能使用 x-bd、x-tt 作为开头。 
            - RequestHeader 不能为 x-real-ip 或 x-forwarded-for（大小写模糊匹配）。 
        HeaderValue ( String ): RequestHeader 的值。当修改请求头的方式为 DELETE 时不生效，具体规则如下： 
            - 取值长度为1 - 1000个字符，不支持中文。 
            - 在变量模式下，HeaderValue只能在固定范围内填写：["uri", "request_uri", "http_host", "args", "msec", "scheme", "args_string", "host", "client_ip", "remote_addr", "remote_port"]。 
        HeaderValueType ( String ): RequestHeader填写HeaderValue中的值类型，支持取值： 
            - v：变量，此模式下，HeaderValue只能在固定范围内填写：["uri", "request_uri", "http_host", "args", "msec", "scheme", "args_string", "host", "client_ip", "remote_addr", "remote_port"]。 
            - s或空值：表征字符固定值。 
       "字段"： MatchingRuleGroup
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Logic ( String ): 匹配条件间的关系，非必填，支持and(与关系)和or(或关系)，默认为and，在填写CriteriaGroup有效。 
        Criteria ( Object of Criteria ): 匹配到该回源配置的详细条件配置，和CriteriaGroup互斥，二者只能填写一个GriteriaGroup设置多条规则，Criteria设置单条规则。 
        CriteriaGroup ( Array of String ): 匹配到该回源配置的嵌套条件配置，和Criteria互斥，二者只能填写一个。 
       "字段"： TosAuthInformation
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        AccessKeyId ( String ): 表示云厂商账号的 AccessKey ID 
        AccessKeySecret ( String ): 表示云厂商账号的 AccessKey Secret 
       "字段"： CertBindClient
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        CertSource ( String ): 证书托管的位置。取值： 
            - self：证书托管在 DCDN 上。目前边缘双向认证只支持托管在 DCDN 中的 CA 证书。 
        CertId ( String ): 在 DCDN 上托管的证书 ID。 
        CertName ( String ): 证书名称。 
        DomainName ( String ): 绑定的加速域名名称。 
        DomainId ( String ): 绑定的加速域名 ID。 
        DeployStatus ( String ): 证书部署的状态,支持取值： 
            - Deployed：部署成功。 
            - Waiting：未部署。 
            - Deploying： 部署中。 
        Expire ( String ): 证书过期时间。 
       "字段"： Criteria
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        ArgType ( String ): 匹配类型，支持以下配置： 
            - path: 访问URL。 
            - header:请求Header。 
            - protocol_type：协议类型。 
            - query：请求 URL 中的查询字符串（URL 参数）。 
            - file_suf：文件后缀。 
            - file_name：文件名称。 
            - cookie:请求携带的Cookie。 
            - client_ip：客户端ip。 
            - client_loc_province：客户端ip地理位置(支持选择国内省份)。 
            - client_loc_country：客户端ip地理位置(支持选择国家)。 
            - client_ip_version：客户端ip版本。 
            - client_isp：客户端网络运行商。 
        MatchType ( String ): 匹配规则，必填，取值范围为:a(等于),n_a(不等于), c(包含任意一个),n_c(不包含任意一个),r(正则匹配到任意一个),e(存在)，n_e(不存在),gt(大于)，gte(大于等于)，lt(小于)，lte(小于等于) 
        IgnoreCase ( Boolean ): 匹配时是否忽略大小写，默认不忽略，支持取值： 
            - true：忽略。 
            - false：不忽略。 
            	只有在ArgType为path、header、protocol_type、query、file_suf、file_name、cookie时生效。 
        Name ( String ): 需要匹配的名称，具体填写限制参考ArgType字段，长度不能超过200。 
        Values ( Array of String ): 需要匹配的值列表，长度不能超过200。 
    """,
    "describe_dcdn_region_and_isp": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Area ( String ): 是  客户端所在区域，默认为China，支持参数： 
                   - China：中国大陆。 
                   - Global：全球。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Regions ( Array of Regions ): 地域信息。 
        Isps ( Array of Isps ): 运营商信息。 
        UniError ( Object of UniError ):  
       "字段"： Regions
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Code ( String ): 运营商/地域缩写 
        Name ( String ): 运营商/地域名称。 
       "字段"： Isps
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Code ( String ): 运营商/地域缩写 
        Name ( String ): 运营商/地域名称。 
       "字段"： UniError
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Code ( String ):  
        MsgCN ( String ):  
        MsgEN ( String ):  
        RespCode ( Integer ):  
    """,
    "describe_domain_isp_data": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             StartTime ( String ): 是  查询起始时间。 
             EndTime ( String ): 是  查询结束时间，结束时间大于起始时间。 
             Domain ( String ): 是  指定查询加速域名，仅支持单个域名。 
             ProjectName ( Array of String ): 否  指定查询域名所属的项目，为空代表查询当前用户所有项目。 
             Area ( String ): 否   
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        DomainName ( String ): 查询域名。 
        StartTime ( String ): 查询起始时间。 
        EndTime ( String ): 查询结束时间。 
        Values ( Array of Values ): 具体运营商分布统计数据信息。 
       "字段"： Values
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Isp ( String ): 运营商中文名。 
        IspEname ( String ): 运营商英文名。 
        Bandwidth ( Float ): 带宽峰值。 
        Traffic ( Float ): 流量。 
        TrafficProportion ( Float ): 总流量占比，例如返回90即为90%。 
        Request ( Float ): 请求数。 
        RequestProportion ( Float ): 访问数占比，例如返回90即为90%。 
        AvgResponseTime ( Float ): 平均响应时间。 
    """,
    "describe_domain_pv_data": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             StartTime ( String ): 是  查询起始时间。 
             EndTime ( String ): 是  查询结束时间。 
             Domain ( String ): 否  指定需查询的加速域名，为空代表查询当前账号下所有加速域名。需要指定完整加速域名，不支持域名部分匹配。 
             ProjectName ( Array of String ): 否  指定需查询的加速域名所属项目，为空代表查询当前用户所有项目。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        DomainName ( String ): 域名。 
        StartTime ( String ): 查询起始时间。 
        EndTime ( String ): 查询结束时间。 
        DataInterval ( Integer ): 采样时间间隔。单位：秒。当前仅支持 3600（1小时一个采样样本）。 
        Results ( Array of Results ): 加速域名的PV样本数据。集合中每个对象对应一个加速域名在某小时内的PV值。 
       "字段"： Results
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Domain ( String ): 样本对应的加速域名。 
        TimeStamp ( String ): 样本时间段（小时）的开始时间点。 
        Value ( Integer ): PV值。 
    """,
    "describe_realtime_data": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             StartTime ( String ): 是  查询起始时间。您可以查询到7天以内的数据。查询时间跨度（StartTime和EndTime之间时长）不能超过24小时。 
             EndTime ( String ): 是  查询结束时间，结束时间大于起始时间。 
             Domains ( Array of String ): 否  指定域名列表，为空时表示查询当前用户所有域名。 
             ProjectName ( Array of String ): 否  指定域名所属的项目，为空时表示查询当前用户所有项目。 
             Metrics ( Array of String ): 是  指定返回的监控指标，支持取值： 
                   - all：全部指标。 
                   - traffic：流量，单位为 byte。 
                   - bandwidth：峰值带宽，单位为 bps。 
                   - request：请求数。 
                   - QPS：峰值QPS。 
                   - RequestHitRate：请求数命中率。 
                   - TrafficHitRate：流量命中率。 
                   - 2xx：返回 2xx 状态码的请求数。返回结果会提供 2xx 状态码总请求数以及单个 2xx 状态码的总请求数。 
                   - 3xx：返回 3xx 状态码的请求数。返回结果会提供 3xx 状态码总请求数以及单个 3xx 状态码的总请求数。 
                   - 4xx：返回 4xx 状态码的请求数。返回结果会提供 4xx 状态码总请求数以及单个 4xx 状态码的总请求数。 
                   - 5xx：返回 5xx 状态码的请求数。返回结果会提供 5xx 状态码总请求数以及单个 5xx 状态码的总请求数。 
             IspNameEn ( Array of String ): 否  指定运营商，为空时表示查询所有运营商，支持取值： 
                   - unicom：联通 
                   - telecom：电信 
                   - mobile：移动 
                   - guangdian：广电 
                   - edu：教育网 
                   - tietong：铁通 
                   - pengboshi：鹏博士 
                   - other：其他运营商 
             AcceleratingRegion ( String ): 否  指定加速区域，为空时表示查询所有区域，支持取值： 
                   - CHN：中国内地 
                   - EU（仅对开通此功能的客户可见）：欧洲 
                   - NA（仅对开通此功能的客户可见）：北美 
                   - SA（仅对开通此功能的客户可见）：南美 
                   - ME（仅对开通此功能的客户可见）：中东 
                   - AP1（仅对开通此功能的客户可见）：亚太1 
                   - AP2（仅对开通此功能的客户可见）：亚太2 
                   - AP3（仅对开通此功能的客户可见）：亚太3 
             AcceleratingScope ( String ): 否  指定加速区域范围，为空时表示查询全球范围，支持取值： 
                   - mainland：中国内地。 
                   - overseas：海外（中国内地以外区域） 
             Area ( String ): 否  指定客户端所在区域，为空时表示查询所有区域，支持取值： 
                   - China：中国大陆 
                   - Global：全球 
             Region ( Array of String ): 否  指定客户端所在详细区域，为空时表示查询所有区域。当 Area 为 China 或 Global 时，Region 支持的区域详见下方表格。 
             Protocol ( Array of String ): 否  指定客户端请求应用层和传输层协议查询，为空时表示查询所有协议，支持取值： 
                   - ALL：全部协议 
                   - HTTP：HTTP协议 
                   - HTTPS：HTTPS协议 
                   - QUIC：QUIC协议 
                   - WS：WebSocket协议 
             Type ( String ): 否  指定访问请求类型，不填时表示查询所有类型（相当于all）。支持取值： 
                   - all：所有类型。 
                   - dynamic：仅查询动态请求对应指标。 
                   - static：仅查询静态请求对应指标。 
             IPVersion ( String ): 否  指定IP协议类型查询。不填时表示查询所有类型，支持取值： 
                   - all：所有类型。 
                   - ipv4：通过 IPv4 访问DCDN的请求 
                   - ipv6：通过 IPv6 访问DCDN的请求 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        DomainCount ( Integer ): 查询域名中有效域名的数量。 
        StartTime ( String ): 查询起始时间。 
        EndTime ( String ): 查询结束时间。 
        Metrics ( Array of String ): 回显查询时选择展示的统计指标。 
        Results ( Array of Results ): 以一分钟为颗粒度的样本集合，集合中每个对象对应一分钟时长的统计数据。 
       "字段"： Results
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        TimeStamp ( String ): 当前一分钟样本的起始时间。 
        RealTimeResults ( Array of RealTimeResults ): 当前一分钟样本的详细数据。 
       "字段"： RealTimeResults
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        DomainName ( String ): 当前数据所对应的域名。 
        DetailInfo ( Array of DetailInfo ): 请求中Metrics字段指定的各个统计指标的数据集合，集合中每个对象为一个名值对。 
       "字段"： DetailInfo
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Name ( String ): 统计指标名称。 
        Value ( Float ): 统计指标的值。 
    """,
    "describe_domain_uv_data": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             StartTime ( String ): 是  查询起始时间。 
             EndTime ( String ): 是  查询结束时间。 
             Domain ( String ): 否  指定需查询的加速域名，为空代表查询当前账号下所有加速域名。需要指定完整加速域名，不支持域名部分匹配。 
             ProjectName ( Array of String ): 否  指定查询域名所属的项目，为空代表查询当前用户所有项目。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        DomainName ( String ): 回显请求中查询的加速域名。 
        StartTime ( String ): 查询起始时间。 
        EndTime ( String ): 查询结束时间。 
        DataInterval ( Integer ): 采样时间间隔。单位：秒。当前仅支持 3600（1小时一个采样样本）。 
        Results ( Array of Results ): 加速域名的UV样本数据。集合中每个对象对应一个加速域名在某小时内的UV值。 
       "字段"： Results
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Domain ( String ): 样本对应的加速域名。 
        TimeStamp ( String ): 样本时间段（小时）的开始时间点。 
        Value ( Integer ): UV值。 
    """,
    "describe_origin_statistics_detail": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             StartTime ( String ): 是  查询起始时间。 
             EndTime ( String ): 是  查询结束时间。 
             ProjectName ( Array of String ): 否  指定查询域名所属的项目，为空代表查询当前用户所有项目。 
             Domain ( String ): 是  域名。 
             PageNum ( Integer ): 否  页码，默认1，从 1 开始计数，可取 >= 1的任意整数。 
             PageSize ( Integer ): 否  每页条数，默认20，取值范围 1 ~ 1000 。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        FileLists ( Array of FileLists ): 日志详情列表。 
        FilesCount ( Integer ): 日志总数据条数。 
        PageNum ( Integer ): 指定的页码。 
        PageSize ( Integer ): 指定的每页条数。 
       "字段"： FileLists
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        DomainName ( String ): 域名。 
        StartTime ( String ): 日志起始时间。 
        EndTime ( String ): 日志结束时间。 
        FilePath ( String ): 日志下载地址。 
        FileSize ( Float ): 日志包大小，单位为 byte 。 
        FileName ( String ): 日志包名称。 
    """,
    "describe_origin_realtime_data": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             StartTime ( String ): 是  查询起始时间。您可以查询到7天以内的数据。查询时间跨度（StartTime和EndTime之间时长）不能超过24小时。 
             EndTime ( String ): 是  查询结束时间，结束时间大于起始时间。 
             Domains ( Array of String ): 否  指定域名列表，为空时表示查询当前用户所有域名。 
             Metrics ( Array of String ): 是  指定返回的监控指标，支持取值： 
                   - all：全部指标。 
                   - traffic：流量，单位为 byte。 
                   - bandwidth：峰值带宽，单位为 bps。 
                   - request：请求数。 
                   - QPS：峰值QPS。 
                   - 2xx：返回 2xx 状态码的请求数。返回结果会提供 2xx 状态码总请求数以及单个 2xx 状态码的总请求数。 
                   - 3xx：返回 3xx 状态码的请求数。返回结果会提供 3xx 状态码总请求数以及单个 3xx 状态码的总请求数。 
                   - 4xx：返回 4xx 状态码的请求数。返回结果会提供 4xx 状态码总请求数以及单个 4xx 状态码的总请求数。 
                   - 5xx：返回 5xx 状态码的请求数。返回结果会提供 5xx 状态码总请求数以及单个 5xx 状态码的总请求数。 
             Protocol ( Array of String ): 否  指定回源请求的应用层协议，为空时表示查询所有协议，支持取值： 
                   - ALL：所有协议 
                   - HTTP 
                   - HTTPS 
             Type ( String ): 否  指定访问请求类型，不填时表示查询所有类型（相当于all）。支持取值： 
                   - all：所有类型。 
                   - dynamic：仅查询动态请求对应指标。 
                   - static：仅查询静态请求对应指标。 
             IPVersion ( String ): 否  指定IP协议类型查询。不填时表示查询所有类型，支持取值： 
                   - all：所有类型。 
                   - ipv4：通过 IPv4 访问DCDN的请求 
                   - ipv6：通过 IPv6 访问DCDN的请求 
             ProjectName ( Array of String ): 否  指定域名所属的项目，为空时表示查询当前用户所有项目。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        DomainCount ( Integer ): 查询域名中有效域名的数量。 
        StartTime ( String ): 查询起始时间。 
        EndTime ( String ): 查询结束时间。 
        Metrics ( Array of String ): 回显查询时选择展示的统计指标。 
        Results ( Array of Results ): 以一分钟为颗粒度的样本集合，集合中每个对象对应一分钟时长的统计数据。 
       "字段"： Results
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        TimeStamp ( String ): 当前一分钟样本的起始时间。 
        RealTimeResults ( Array of RealTimeResults ): 当前一分钟样本的详细数据。 
       "字段"： RealTimeResults
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        DomainName ( String ): 当前数据所对应的域名。 
        DetailInfo ( Array of DetailInfo ): 请求中Metrics字段指定的各个统计指标的数据集合，集合中每个对象为一个名值对。 
       "字段"： DetailInfo
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Name ( String ): 统计指标名称。 
        Value ( Float ): 统计指标的值。 
    """,
    "describe_origin_statistics": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             StartTime ( String ): 是  查询起始时间。您可以查询过去90天内的数据。查询时间跨度（StartTime和EndTime之间时长）不能超过31天。基于您指定的时间跨度，您可以选择数据样本的时间粒度（Interval 参数）会相应不同。 
             EndTime ( String ): 是  查询结束时间，结束时间大于起始时间。 
             Metrics ( Array of String ): 是  指定返回的监控指标，支持取值： 
                   - all：全部指标。 
                   - traffic：流量，单位为 byte。 
                   - bandwidth：峰值带宽，单位为 bps。 
                   - request：请求数。 
                   - QPS：峰值QPS。 
                   - 2xx：返回 2xx 状态码的请求数。返回结果会提供 2xx 状态码总请求数以及单个 2xx 状态码的总请求数。 
                   - 3xx：返回 3xx 状态码的请求数。返回结果会提供 3xx 状态码总请求数以及单个 3xx 状态码的总请求数。 
                   - 4xx：返回 4xx 状态码的请求数。返回结果会提供 4xx 状态码总请求数以及单个 4xx 状态码的总请求数。 
                   - 5xx：返回 5xx 状态码的请求数。返回结果会提供 5xx 状态码总请求数以及单个 5xx 状态码的总请求数。 
             Domains ( Array of String ): 否  指定查询域名列表。为空时代表查询当前用户所有域名。 
             Interval ( Integer ): 否  时间粒度，单位为秒 。支持取值： 
                   - 查询时间段跨度 3 天以内（不含3）：支持 300、3600、 86400。不传该参数时，默认值为300。 
                   - 查询时间段跨度 3 - 31 天（不含31）： 支持 3600 和 86400。不传该参数时，默认值为 3600。 
                   - 查询时间段跨度 31 天： 支持 86400。不传该参数，默认值为 86400。 
             Protocol ( Array of String ): 否  指定客户端请求应用层和传输层协议查询，为空时表示查询所有协议，支持取值： 
                   - ALL：全部协议 
                   - HTTP：HTTP协议 
                   - HTTPS：HTTPS协议 
                   - QUIC：QUIC协议 
                   - WS：WebSocket协议 
             Type ( String ): 否  指定访问请求类型，为空时表示查询所有类型（相当于all）。支持取值： 
                   - all：所有类型。 
                   - dynamic：仅查询动态请求对应指标。 
                   - static：仅查询静态请求对应指标。 
             IPVersion ( String ): 否  指定IP协议类型查询。为空时表示查询所有类型，支持取值： 
                   - all：所有类型。 
                   - ipv4：通过 IPv4 访问DCDN的请求 
                   - ipv6：通过 IPv6 访问DCDN的请求 
             ProjectName ( Array of String ): 否  指定域名所属的项目，为空时表示查询当前用户所有项目。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        DomainCount ( Integer ): 查询域名中有效域名的数量。 
        StartTime ( String ): 查询起始时间。 
        EndTime ( String ): 查询结束时间。 
        Metrics ( Array of String ): 回显查询时选择展示的统计指标。 
        Results ( Array of Results ): 查询数据明细。 
       "字段"： Results
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        TimeStamp ( String ): 当前样本时间段的开始时间点。 
        DetailInfo ( Array of DetailInfo ): 当前样本时间段的详细数据。 
       "字段"： DetailInfo
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Name ( String ): 统计指标名称。 
        Value ( Float ): 统计指标的值。 
    """,
    "describe_top_domains": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             StartTime ( String ): 是  查询起始时间。 
             EndTime ( String ): 是  查询结束时间。 
             Sort ( String ): 是  指定排序指标，可指定值： 
                   - traffic：流量。 
                   - bandwidth：峰值带宽。 
                   - request: 请求数。 
                   - QPS: 峰值 QPS 。 
                   - 2xx: 2xx状态码数量 。 
                   - 3xx: 3xx状态码数量 。 
                   - 4xx:4xx状态码数量 。 
                   - 5xx: 5xx状态码数量 。 
             Domains ( Array of String ): 否  指定查询域名列表。为空代表查询当前用户所有域名。 
             Limit ( Integer ): 否  域名获取数量限制，默认为20，取值支持1~100 。 
             ProjectName ( Array of String ): 否  指定查询域名所属的项目，为空代表查询当前用户所有项目。 
             IspNameEn ( Array of String ): 否  指定运营商，为空时表示查询所有运营商，支持取值： 
                   - unicom：联通 
                   - telecom：电信 
                   - mobile：移动 
                   - guangdian：广电 
                   - edu：教育网 
                   - tietong：铁通 
                   - pengboshi：鹏博士 
                   - other：其他运营商 
             ServiceType ( String ): 否  指定加速域名关联的加速场景，支持取值： 
                   - ai：AI 加速 
                   - upload：上传加速 
                   - page：页面加速 
                   - api：API 加速 
                   - other：其他 
             AcceleratingRegion ( String ): 否  加速区域，不填表示查询所有区域，支持的参数如下所示 
                   - CHN：中国内地 
                   - EU（仅对开通此功能的客户可见）：欧洲 
                   - NA（仅对开通此功能的客户可见）：北美 
                   - SA（仅对开通此功能的客户可见）：南美 
                   - ME（仅对开通此功能的客户可见）：中东 
                   - AP1（仅对开通此功能的客户可见）：亚太1 
                   - AP2（仅对开通此功能的客户可见）：亚太2 
                   - AP3（仅对开通此功能的客户可见）：亚太3 
             AcceleratingScope ( String ): 否  指定加速区域范围，为空时表示查询全球范围，支持取值： 
                   - mainland：中国内地。 
                   - overseas：海外（中国内地以外区域） 
             Area ( String ): 否  客户端所在区域，不填表示查询所有区域，支持参数： 
                   - China：中国大陆； 
                   - Global：全球。 
             Region ( Array of String ): 否  指定区域，为空时表示查询所有区域。当 Area 为 China 或 Global 时，Region 支持的区域详见下方表格。 
             Protocol ( Array of String ): 否  指定客户端请求应用层和传输层协议查询，为空时表示查询所有协议，支持参数： 
                   - ALL：全部协议； 
                   - HTTP：HTTP协议； 
                   - HTTPS：HTTPS协议； 
                   - QUIC：QUIC协议； 
                   - WS：WebSocket协议。 
             Type ( String ): 否  指定访问类型，不填时表示查询所有类型（相当于all），支持参数： 
                   - all：所有类型。 
                   - dynamic：指定查询动态对应指标。 
                   - static：指定查询静态对应指标。 
             IPVersion ( String ): 否  指定ip类型查询，不填时表示查询所有类型，支持参数： 
                   - all：所有类型； 
                   - ipv4：IPv4 类型； 
                   - ipv6：IPv6 类型。 
             Metrics ( Array of String ): 否  指定返回的监控指标，支持取值： 
                   - all：全部指标。 
                   - traffic：流量，单位为 byte。 
                   - bandwidth：峰值带宽，单位为 bps。 
                   - request：请求数。 
                   - QPS：峰值QPS。 
                   - 2xx：返回 2xx 状态码的请求数。返回结果会提供 2xx 状态码总请求数以及单个 2xx 状态码的总请求数。 
                   - 3xx：返回 3xx 状态码的请求数。返回结果会提供 3xx 状态码总请求数以及单个 3xx 状态码的总请求数。 
                   - 4xx：返回 4xx 状态码的请求数。返回结果会提供 4xx 状态码总请求数以及单个 4xx 状态码的总请求数。 
                   - 5xx：返回 5xx 状态码的请求数。返回结果会提供 5xx 状态码总请求数以及单个 5xx 状态码的总请求数。 
             ResourceTagFilter ( Object of ResourceTagFilter ): 否  指定加速域名关联的资源标签。可以调用 ListResourceTags 查看资源标签列表。 
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
        DomainCount ( Integer ): 查询域名中有效域名的数量。 
        StartTime ( String ): 查询起始时间。 
        EndTime ( String ): 查询结束时间。 
        TopDomains ( Array of TopDomains ): 域名排名列表。 
       "字段"： TopDomains
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        DomainName ( String ): 域名。 
        Rank ( Float ): 查询到的域名对应的排名。 
        Request ( Float ): 请求数。 
        Traffic ( Float ): 流量。 
        Bandwidth ( Float ): 带宽峰值。 
        QPS ( Float ): 峰值 QPS 。 
        StatusCode2xx ( Float ): 2xx状态码数量。 
        StatusCode3xx ( Float ): 3xx状态码数量。 
        StatusCode4xx ( Float ): 4xx状态码数量。 
        StatusCode5xx ( Float ): 5xx状态码数量。 
        StatusCode2xxRatio ( Float ): 2xx状态码占比，小于等于1。 
        StatusCode3xxRatio ( Float ): 3xx状态码占比，小于等于1。 
        StatusCode4xxRatio ( Float ): 4xx状态码占比，小于等于1。 
        StatusCode5xxRatio ( Float ): 5xx状态码占比，小于等于1。 
        StatusCode1xx ( Float ): 1xx状态码数量。 
        StatusCode1xxRatio ( Float ): 1xx状态码占比，小于等于1。 
    """,
    "describe_top_i_ps": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             StartTime ( String ): 是  查询起始时间。 
             EndTime ( String ): 是  查询结束时间。 
             Sort ( String ): 是  指定排序指标。取值： 
                   - traffic：流量。 
                   - bandwidth：峰值带宽。 
                   - request: 请求数。 
                   - QPS: 峰值 QPS 。 
             Limit ( Integer ): 否  域名获取数量限制，默认为20，取值支持1~100 。 
             ProjectName ( Array of String ): 否  指定查询域名所属的项目，为空代表查询当前用户所有项目。 
             Domain ( String ): 否  指定查询域名，不填默认全选。需要指定完整加速域名，不支持域名部分匹配。 
             StatusCode ( Array of String ): 否  指定查询状态码：2xx、3xx、4xx、5xx。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        IP ( String ): 客户端 IP 地址。 
        Rank ( Float ): 排名。 
        Request ( Float ): 请求数。 
        Traffic ( Float ): 流量。单位：byte。 
        Bandwidth ( Float ): 带宽峰值。单位：bps。 
        QPS ( Float ): 峰值 QPS 。 
    """,
    "describe_top_referers": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             StartTime ( String ): 是  查询起始时间。 
             EndTime ( String ): 是  查询结束时间。 
             Sort ( String ): 是  指定排序指标。取值： 
                   - traffic：流量。 
                   - bandwidth：峰值带宽。 
                   - request: 请求数。 
                   - QPS: 峰值 QPS 。 
             Limit ( Integer ): 否  域名获取数量限制，默认为20，取值支持1~100 。 
             ProjectName ( Array of String ): 否  指定查询域名所属的项目，为空代表查询当前用户所有项目。 
             Domain ( String ): 否  指定查询域名，不填默认全选。需要指定完整加速域名，不支持域名部分匹配。 
             StatusCode ( Array of String ): 否  指定查询状态码：2xx、3xx、4xx、5xx。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Referer ( String ): HTTP referer。 
        Rank ( Float ): 排名。 
        Request ( Float ): 请求数。 
        Traffic ( Float ): 流量。单位：byte。 
        Bandwidth ( Float ): 带宽峰值。单位：bps。 
        QPS ( Float ): 峰值 QPS 。 
    """,
    "describe_top_urls": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             StartTime ( String ): 是  查询起始时间。 
             EndTime ( String ): 是  查询结束时间。 
             Sort ( String ): 是  指定排序指标。取值： 
                   - traffic：流量。 
                   - bandwidth：峰值带宽。 
                   - request: 请求数。 
                   - QPS: 峰值 QPS 。 
             Limit ( Integer ): 否  域名获取数量限制，默认为20，取值 1~100。 
             ProjectName ( Array of String ): 否  指定查询域名所属的项目，为空代表查询当前用户所有项目。 
             Domain ( String ): 否  指定查询域名，不填默认全选。需要指定完整加速域名，不支持域名部分匹配。 
             StatusCode ( Array of String ): 否  指定查询状态码：2xx、3xx、4xx、5xx。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        URL ( String ): URL。 
        Rank ( Float ): 排名。 
        Request ( Float ): 请求数。 
        Traffic ( Float ): 流量。 
        Bandwidth ( Float ): 峰值带宽。 
        QPS ( Float ): 峰值 QPS 。 
    """,
    "list_cert": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             MatchDomain ( String ): 否  查询某个域名绑定的证书。通过输入的加速域名，查询与该加速域名绑定的证书信息。 
             PageNumber ( Integer ): 否  分页页号，最大 10000，最小 1。默认为 1。 
             PageSize ( Integer ): 否  分页每页记录数，最大100，不填默认为20。 
             CertStatus ( String ): 否  筛选不同状态的证书，支持： 
                   - Expired：已过期 
                   - Expiring：即将过期，距离真正过期时间少于30天时展示的状态 
                   - Running：运行中 
             BoundStatus ( String ): 否  基于证书是否绑定了加速域名，进行证书的筛选。支持： 
                   - unbound：查询在全站加速服务上，未与加速域名相绑定的证书。 
                   - bound：查询在全站加速服务上，已与加速域名相绑定的证书。 
             ProjectName ( Array of String ): 否  证书所在的项目列表，最多允许填写一个。 
             ContainDomain ( Boolean ): 否  是否包含DCDN的域名绑定关系，开启后可能会增加该接口的访问时间。 
             BindDomain ( String ): 否  过滤绑定在某域名上的证书，模糊匹配。 
             CertId ( String ): 否  证书 ID。 
             CertName ( String ): 否  证书的描述性名称。 
             CertSource ( String ): 否  证书托管位置，支持取值： 
                   - volc：证书中心托管证书 
                   - self：DCDN托管证书 
                   默认查询证书中心托管证书 
             CertUsage ( String ): 否  查询的证书用途，为空时默认查询服务器证书，支持取值： 
                   - server：服务器证书 
                   - ca： CA 证书 
             ExpireSortOrder ( String ): 否  按证书过期时间排序，默认不排序，支持取值： 
                   - ascending：升序 
                   - descending：降序 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        CertList ( Array of CertList ): 与加速域名绑定的证书信息列表。 
        PageNumber ( Integer ): 当前页号。 
        PageSize ( Integer ): 当前页大小。 
        Total ( Integer ): 证书数量。 
       "字段"： CertList
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        CertSource ( String ): 证书的托管位置，具体来源如下： 
            - volc：证书在火山证书中心上托管。 
            - self：证书在DCDN上托管。 
        CertId ( String ): 证书的 ID 。 
        CertName ( String ): 证书的名称。 
        Expire ( String ): 证书的过期时间。 
        Domain ( Array of String ): 证书绑定的域名。 
        CertStatus ( String ): 证书状态，支持如下取值： 
            - Expired: 已过期。 
            - Expiring: 即将过期，距离真正过期时间少于30天。 
            - Running: 运行中。 
        IsCA ( Boolean ): 是否是CA证书 
        KeyType ( String ): 密钥算法。该参数有以下取值： 
            - rsa：RSA算法 
            - ecc：ECC算法 
            - SM2：SM2（国密）算法 
        MatchDomain ( Array of String ): 该证书能匹配上的域名 
    """,
    "list_cert_bind": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             SearchKey ( String ): 否  筛选绑定关系的参数，当证书名称、证书ID、域名名称包含该参数时，才会返回绑定关系信息。 
             ProjectName ( Array of String ): 否  筛选域名的项目，不填时默认不对项目进行筛选。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        BindList ( Array of BindList ): 证书绑定关系列表。 
       "字段"： BindList
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        CertSource ( String ): 证书来源，支持参数： 
            - volc：在火山证书中心上托管的证书。 
            - self：在DCDN上托管的证书。 
        CertId ( String ): 在火山证书中心上托管的证书 ID。 
        CertName ( String ): 证书名称。 
        DomainName ( String ): 绑定的加速域名名称。 
        DomainId ( String ): 绑定的加速域名 ID。 
        DeployStatus ( String ): 证书部署的状态,支持取值： 
            - Deployed：部署成功。 
            - Waiting：未部署。 
            - Deploying： 部署中。 
        Expire ( String ): 过期时间。 
    """,
    "describe_domain_region_data": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             StartTime ( String ): 是  查询起始时间。 
             EndTime ( String ): 是  查询结束时间。结束时间必须大于起始时间。StartTime及EndTime定义的查询的时间段不能超过 31 天。 
             Domain ( String ): 是  指定查询加速域名。仅支持单个域名。 
             ProjectName ( Array of String ): 否  指定查询域名所属的项目。为空代表查询当前用户所有项目。 
             Area ( String ): 否  客户端所在区域。不填表示查询全球区域，支持取值： 
                   - China：仅中国内地 
                   - Global：全球 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        DomainName ( String ): 查询域名。 
        StartTime ( String ): 查询起始时间。 
        EndTime ( String ): 查询结束时间。 
        Values ( Array of Values ): 具体区域分布统计数据。 
       "字段"： Values
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Region ( String ): 区域中文名。如果您查询的是“仅中国内地”区域，结果精确到省份颗粒度。如果您查询的是“全球”区域，结果精确到国家/地区颗粒度。 
        RegionEname ( String ): 区域英文缩写代号。例如，新加坡为SGP，辽宁为LN。 
        Bandwidth ( Float ): 带宽峰值。单位：bps 
        Traffic ( Float ): 流量。单位：byte 
        TrafficProportion ( Float ): 该区域流量占本次查询结果总量的百分比，例如返回90即为90%。 
        Request ( Float ): 请求数。 
        RequestProportion ( Float ): 该区域请求数占本次查询结果总量的百分比，例如返回90即为90%。 
        AvgResponseTime ( Float ): 平均响应时间。单位：毫秒 
    """,
    "describe_statistics": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             StartTime ( String ): 是  查询起始时间。您可以查询过去90天内的数据。查询时间跨度（StartTime和EndTime之间时长）不能超过31天。基于您指定的时间跨度，您可以选择数据样本的时间粒度（Interval 参数）会相应不同。 
             EndTime ( String ): 是  查询结束时间，结束时间大于起始时间。 
             Metrics ( Array of String ): 否  指定返回的监控指标，支持取值： 
                   - all：全部指标。 
                   - traffic：流量，单位为 byte。 
                   - bandwidth：峰值带宽，单位为 bps。 
                   - request：请求数。 
                   - QPS：峰值QPS。 
                   - RequestHitRate：请求数命中率。 
                   - TrafficHitRate：流量命中率。 
                   - 2xx：返回 2xx 状态码的请求数。返回结果会提供 2xx 状态码总请求数以及单个 2xx 状态码的总请求数。 
                   - 3xx：返回 3xx 状态码的请求数。返回结果会提供 3xx 状态码总请求数以及单个 3xx 状态码的总请求数。 
                   - 4xx：返回 4xx 状态码的请求数。返回结果会提供 4xx 状态码总请求数以及单个 4xx 状态码的总请求数。 
                   - 5xx：返回 5xx 状态码的请求数。返回结果会提供 5xx 状态码总请求数以及单个 5xx 状态码的总请求数。 
             Domains ( Array of String ): 是  指定查询域名列表。为空时代表查询当前用户所有域名。 
             Interval ( Integer ): 否  时间样本粒度，单位为秒 。支持取值： 
                   - 查询时间段跨度 3 天以内（不含3）：支持 300、3600、 86400。不传该参数时，默认值为300。 
                   - 查询时间段跨度 3 - 31 天（不含31）： 支持 3600 和 86400。不传该参数时，默认值为 3600。 
                   - 查询时间段跨度 31 天： 支持 86400。不传该参数，默认值为 86400。 
             Protocol ( Array of String ): 否  指定客户端请求应用层和传输层协议查询，为空时表示查询所有协议，支持取值： 
                   - ALL：全部协议 
                   - HTTP：HTTP协议 
                   - HTTPS：HTTPS协议 
                   - QUIC：QUIC协议 
                   - WS：WebSocket协议 
             Area ( String ): 否  客户端所在区域，不填表示查询所有区域，支持参数： 
                   - China：中国大陆； 
                   - Global：全球。 
             Region ( Array of String ): 否  指定客户端所在详细区域，为空时表示查询所有区域。当 Area 为 China 或 Global 时，Region 支持的区域详见下方表格。 
             ProjectName ( Array of String ): 否  指定域名所属的项目，为空时表示查询当前用户所有项目。 
             IspNameEn ( Array of String ): 否  指定运营商，为空时表示查询所有运营商，支持的运营商如下所示。 
                   - unicom：中国联通； 
                   - telecom：中国电信； 
                   - mobile：中国移动； 
                   - guangdian：广电； 
                   - edu：教育网； 
                   - tietong：铁通； 
                   - pengboshi：鹏博士； 
                   - other：其他运营商。 
             AcceleratingRegion ( String ): 否  指定加速区域，为空时表示查询所有区域，支持取值： 
                   - CHN：中国内地 
                   - EU（仅对开通此功能的客户可见）：欧洲 
                   - NA（仅对开通此功能的客户可见）：北美 
                   - SA（仅对开通此功能的客户可见）：南美 
                   - ME（仅对开通此功能的客户可见）：中东 
                   - AP1（仅对开通此功能的客户可见）：亚太1 
                   - AP2（仅对开通此功能的客户可见）：亚太2 
                   - AP3（仅对开通此功能的客户可见）：亚太3 
             AcceleratingScope ( String ): 否  指定加速区域范围，为空时表示查询全球范围，支持取值： 
                   - mainland：中国内地。 
                   - overseas：海外（中国内地以外区域） 
             Type ( String ): 否  指定访问请求类型，为空时表示查询所有类型（相当于all）。支持取值： 
                   - all：所有类型。 
                   - dynamic：仅查询动态请求对应指标。 
                   - static：仅查询静态请求对应指标。 
             IPVersion ( String ): 否  指定IP协议类型查询。不填时表示查询所有类型，支持取值： 
                   - all：所有类型。 
                   - ipv4：通过 IPv4 访问DCDN的请求 
                   - ipv6：通过 IPv6 访问DCDN的请求 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        DomainCount ( Integer ): 查询域名中有效域名的数量。 
        StartTime ( String ): 查询起始时间。 
        EndTime ( String ): 查询结束时间。 
        Metrics ( Array of String ): 回显查询时选择展示的统计指标。 
        Results ( Array of Results ): 统计指标的明细。基于请求中Interval参数指定的时间样本粒度，以时间序列结构展示。 
       "字段"： Results
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        TimeStamp ( String ): 当前样本时间段起始时间，以字符串格式呈现。 
        DetailInfo ( Array of DetailInfo ): 当前样本时间段的详细数据。 
       "字段"： DetailInfo
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Name ( String ): 统计指标名称。 
        Value ( Float ): 标签名称对应的值。 
    """,
}
