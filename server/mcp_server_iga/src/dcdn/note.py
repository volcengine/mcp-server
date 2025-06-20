note = {
    "list_domain_config": r""" 
   Args: 
       body: A JSON structure
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
    """,
    "describe_dcdn_region_and_isp": r""" 
   Args: 
       body: A JSON structure
            Area ( String ): 是  客户端所在区域，默认为China，支持参数： 
                  - China：中国大陆。 
                  - Global：全球。 
    """,
    "describe_domain_isp_data": r""" 
   Args: 
       body: A JSON structure
            StartTime ( String ): 是  查询起始时间。时间格式：2021-01-01 00:00:00。 
            EndTime ( String ): 是  查询结束时间，结束时间大于起始时间。时间格式：2021-01-01 23:59:59。 
            Domain ( String ): 是  指定查询加速域名，仅支持单个域名。 
            ProjectName ( Array of String ): 否  指定查询域名所属的项目，为空代表查询当前用户所有项目。 
            Area ( String ): 否   
    """,
    "describe_domain_pv_data": r""" 
   Args: 
       body: A JSON structure
            StartTime ( String ): 是  查询起始时间。时间格式：2021-01-01 00:00:00。 
            EndTime ( String ): 是  查询结束时间。时间格式：2021-01-01 23:59:59。 
            Domain ( String ): 是  域名名称。 
            ProjectName ( Array of String ): 否  指定查询域名所属的项目，为空代表查询当前用户所有项目。 
    """,
    "describe_domain_uv_data": r""" 
   Args: 
       body: A JSON structure
            StartTime ( String ): 是  查询起始时间。时间格式：2021-01-01 23:59:59。 
            EndTime ( String ): 是  查询结束时间。时间格式：2021-01-01 00:00:00。 
            Domain ( String ): 是  域名名称。 
            ProjectName ( Array of String ): 否  指定查询域名所属的项目，为空代表查询当前用户所有项目。 
    """,
    "describe_origin_statistics_detail": r""" 
   Args: 
       body: A JSON structure
            StartTime ( String ): 是  查询起始时间。 
            EndTime ( String ): 是  查询结束时间。 
            ProjectName ( Array of String ): 否  指定查询域名所属的项目，为空代表查询当前用户所有项目。 
            Domain ( String ): 是  域名。 
            PageNum ( Integer ): 否  页码，默认1，从 1 开始计数，可取 >= 1的任意整数。 
            PageSize ( Integer ): 否  每页条数，默认20，取值范围 1 ~ 1000 。 
    """,
    "describe_origin_statistics": r""" 
   Args: 
       body: A JSON structure
            StartTime ( String ): 是  查询起始时间。时间格式：2021-01-01 00:00:00。 
            EndTime ( String ): 是  查询结束时间，结束时间大于起始时间。时间格式：2021-01-01 23:59:59。 
            Domains ( Array of String ): 是  指定查询域名列表，为空代表查询当前用户所有域名。 
            Metrics ( Array of String ): 否  指定查询指标，支持取值： 
                  - all：全部指标。 
                  - traffic：流量，单位为 byte 。 
                  - bandwidth：峰值带宽，单位为 bps 。 
                  - request: 请求数，单位为次 。 
                  - QPS: 峰值QPS，单位为次/s 。 
                  - 2xx：返回 2xx 状态码汇总或者 2 开头状态码数据，单位为个 。 
                  - 3xx：返回 3xx 状态码汇总或者 3 开头状态码数据，单位为个 。 
                  - 4xx：返回 4xx 状态码汇总或者 4 开头状态码数据，单位为个 。 
                  - 5xx：返回 5xx 状态码汇总或者 5 开头状态码数据，单位为个 。 
            Interval ( Integer ): 否  时间粒度，单位为秒 ，支持参数： 
                  - 3 天以内（不含3）：支持 300、3600、 86400，不传该参数时，默认值为300。 
                  - 3 - 31 天（不含31）： 支持 3600 和 86400，不传该参数时，默认值为3600。 
                  - 31 天及以上： 支持 86400，不传该参数，默认值为 86400。 
            Protocol ( Array of String ): 否  指定客户端请求应用层和传输层协议查询，为空时表示查询所有协议，支持参数： 
                  - ALL 
                  - HTTP 
                  - HTTPS 
                  - QUIC 
                  - WebSocket 
            Type ( String ): 否  指定访问类型，不填时表示查询所有类型，返回总和（相当于all），支持参数： 
                  - all：所有类型。 
                  - dynamic：指定查询动态对应指标。 
                  - static：指定查询静态对应指标。 
            IPVersion ( String ): 否  指定ip类型查询，不填时表示查询所有类型，支持参数： 
                  - all：所有类型。 
                  - ipv4 
                  - ipv6 
            ProjectName ( Array of String ): 否  指定查询域名所属的项目，为空代表查询当前用户所有项目。 
    """,
    "describe_top_domains": r""" 
   Args: 
       body: A JSON structure
            AcceleratingRegion ( String ): 否   
            AcceleratingScope ( String ): 否   
            Area ( String ): 否   
            Domains ( Array of String ): 否   
            EndTime ( String ): 否   
            IPVersion ( String ): 否   
            IspNameEn ( Array of String ): 否   
            Limit ( Integer ): 否   
            Metrics ( Array of String ): 否   
            ProjectName ( Array of String ): 否   
            Protocol ( Array of String ): 否   
            Region ( Array of String ): 否   
            ResourceTagFilter ( Object of ResourceTagFilter ): 否   
            Sort ( String ): 否   
            StartTime ( String ): 否   
            Type ( String ): 否   
            ServiceType ( String ): 否   
           "字段"： ResourceTagFilter
            FilterType ( String ): 否   
            ResourceTags ( Array of ResourceTags ): 否   
           "字段"： ResourceTags
            Key ( String ): 是  标签名称，支持大/小写字母、数字和中文组成，支持"+-=@/._"等特殊字符，长度不超过 128 个字符，不允许以volc开头。 
            Value ( String ): 是  标签名称对应的值，由大/小写字母、数字和中文组成，支持"+-=@/._"等特殊字符，长度不超过 256个字符。 
    """,
    "describe_top_i_ps": r""" 
   Args: 
       body: A JSON structure
            StartTime ( String ): 是  查询起始时间。时间格式：2021-01-01 00:00:00。 
            EndTime ( String ): 是  查询结束时间。时间格式：2021-01-01 23:59:59。 
            Sort ( String ): 是  指定排序指标，可指定值： 
                  - traffic：流量。 
                  - bandwidth：峰值带宽。 
                  - request: 请求数。 
                  - QPS: 峰值 QPS 。 
            Limit ( Integer ): 否  域名获取数量限制，默认为20，取值支持1~100 。 
            ProjectName ( Array of String ): 否  指定查询域名所属的项目，为空代表查询当前用户所有项目。 
            Domain ( String ): 否  指定查询域名，不填默认全选。 
            StatusCode ( Array of String ): 否  指定查询状态码，2xx,3xx,4xx,5xx。 
    """,
    "describe_top_referers": r""" 
   Args: 
       body: A JSON structure
            StartTime ( String ): 是  查询起始时间。时间格式：2021-01-01 00:00:00。 
            EndTime ( String ): 是  查询结束时间。时间格式：2021-01-01 23:59:59。 
            Sort ( String ): 是  指定排序指标，可指定值： 
                  - traffic：流量。 
                  - bandwidth：峰值带宽。 
                  - request: 请求数。 
                  - QPS: 峰值 QPS 。 
            Limit ( Integer ): 否  域名获取数量限制，默认为20，取值支持1~100 。 
            ProjectName ( Array of String ): 否  指定查询域名所属的项目，为空代表查询当前用户所有项目。 
            Domain ( String ): 否  指定查询域名，不填默认全选。 
            StatusCode ( Array of String ): 否  指定查询状态码，2xx,3xx,4xx,5xx。 
    """,
    "describe_top_urls": r""" 
   Args: 
       body: A JSON structure
            StartTime ( String ): 是  查询起始时间。时间格式：2021-01-01 00:00:00。 
            EndTime ( String ): 是  查询结束时间。时间格式：2021-01-01 23:59:59。 
            Sort ( String ): 是  指定排序指标，可指定值： 
                  - traffic：流量。 
                  - bandwidth：峰值带宽。 
                  - request: 请求数。 
                  - QPS: 峰值 QPS 。 
            Limit ( Integer ): 否  域名获取数量限制，默认为20，取值支持1~100 。 
            ProjectName ( Array of String ): 否  指定查询域名所属的项目，为空代表查询当前用户所有项目。 
            Domain ( String ): 否  指定查询域名，不填默认全选。 
            StatusCode ( Array of String ): 否  指定查询状态码，2xx,3xx,4xx,5xx。 
    """,
    "list_cert": r""" 
   Args: 
       body: A JSON structure
            MatchDomain ( String ): 否  查询某个域名绑定的证书。通过输入的加速域名，查询与该加速域名绑定的证书信息。 
            PageNumber ( Integer ): 否  分页页号，最大10000，最小1，不填默认为1。 
            PageSize ( Integer ): 否  分页页号，分页页大小，最大100，不填默认为20。 
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
            CertId ( String ): 否  证书ID 
            CertName ( String ): 否  证书备注名称 
            CertSource ( String ): 否  证书源类型，支持以下两种： 
                  - volc：证书中心托管证书 
                  - self：DCDN托管证书 
                  默认查询火山证书中心托管证书 
            CertUsage ( String ): 否  查询的证书用途，为空时默认查询服务端证书，支持：'server' 'ca'。 
            ExpireSortOrder ( String ): 否  证书过期时间排序，默认不排序，支持： 
                  - ascending 
                  - descending 
    """,
    "list_cert_bind": r""" 
   Args: 
       body: A JSON structure
            SearchKey ( String ): 否  筛选绑定关系的参数，当证书名称、证书ID、域名名称包含该参数时，才会返回绑定关系信息。 
            ProjectName ( Array of String ): 否  筛选域名的项目，不填时默认不对项目进行筛选。 
    """,
    "describe_domain_region_data": r""" 
   Args: 
       body: A JSON structure
            StartTime ( String ): 是  查询起始时间。 
            EndTime ( String ): 是  查询结束时间。结束时间必须大于起始时间。StartTime及EndTime定义的查询的时间段不能超过 31 天。 
            Domain ( String ): 是  指定查询加速域名。仅支持单个域名。 
            ProjectName ( Array of String ): 否  指定查询域名所属的项目。为空代表查询当前用户所有项目。 
            Area ( String ): 否  客户端所在区域。不填表示查询全球区域，支持取值： 
                  - China：仅中国内地 
                  - Global：全球 
    """,
}
