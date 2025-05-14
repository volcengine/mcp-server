note = {
    "describe_cdn_config": r""" 
    Args: 
        body: A JSON structure
             Domain ( String ): 是  表示一个加速域名。您一次只能查询一个加速域名的配置详情。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        DomainConfig ( Object of DomainConfig ):  
       "字段"： DomainConfig
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        ServiceType ( String ): web 
        Cname ( String ): www.example.com.volcgslb.com 
        CreateTime ( Long ): 1636612244 
        Domain ( String ): www.example.com 
        HTTPS ( Object of HTTPS ):  
        LockStatus ( String ): `on` 
        Project ( String ): default 
        ServiceRegion ( String ): outside_chinese_mainland 
        Status ( String ): offline 
        UpdateTime ( Long ): 1639621409 
        ResourceTags ( Array of ResourceTags ):  
       "字段"： HTTPS
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Switch ( Boolean ): true 
        CertInfo ( Object of CertInfo ):  
        CertInfoList ( Array of CertInfoList ):  
        CertCheck ( Object of CertCheck ):  
       "字段"： ResourceTags
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Key ( String ):  
        Value ( String ):  
       "字段"： CertInfo
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        CertId ( String ): cert-eb5d99026753499a8a34d2a4f0a08d92 
        CertName ( String ): www.example.com 
        Desc ( String ): Comment 
        EffectiveTime ( Long ): 1655856000 
        ExpireTime ( Long ): 1687478399 
        Source ( String ): volc_cert_center 
        EncryType ( String ): inter_cert 
       "字段"： CertInfoList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        CertId ( String ): cert-602fc4eb6cbf4b9351b54bedf2bc5dc5 
        CertName ( String ): www.example.com 
        Desc ( String ): Comment 
        EffectiveTime ( Long ): 1655856000 
        ExpireTime ( Long ): 1687478399 
        Source ( String ): volc_cert_center 
        EncryType ( String ): inter_cert 
       "字段"： CertCheck
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        CertInfoList ( Array of CertInfoList ):  
        Switch ( Boolean ): true 
    """,
    "list_cdn_domains": r""" 
    Args: 
        body: A JSON structure
             Domain ( String ): 否  表示一个字符串，用来对域名进行过滤，获取包含该字符串的域名。 
             ServiceType ( String ): 否  表示一个业务类型，用来对域名进行过滤，获取该业务类型的域名。该参数有以下取值： 
                   - download：表示文件下载。 
                   - web：表示网页。 
                   - video：表示音视频点播。 
             ResourceTags ( Array of String ): 否  表示一个标签列表，用于对域名进行过滤，获取带有列表中任意标签的域名。列表中最多可以包含 10 个标签，每个标签的格式是 key:value。参见右边该参数的示例。 
             Status ( String ): 否  表示一个域名状态，用来对域名进行过滤，获取该状态下的域名。该参数有以下取值： 
                   - online：表示 "正常运行"。 
                   - configuring：表示 "配置中"。 
                   - offline：表示 "已下线"。 
             Project ( String ): 否  表示一个项目，获取归属该项目的域名。 
             OriginProtocol ( String ): 否  表示一个协议，获取回源请求使用该协议的域名。该参数有以下取值： 
                   - http：表示 HTTP 协议。 
                   - https：表示 HTTPS 协议。 
                   - followclient：表示用户请求使用的协议。 
             IPv6 ( Boolean ): 否  表示根据是否启用了 IPv6 特性来过滤域名。该参数有以下取值： 
                   * true: 表示 IPv6 已启用。 
                   * false: 表示 IPv6 未启用。 
             HTTPS ( Boolean ): 否  表示根据是否启用了 HTTPS 特性来过滤域名。该参数有以下取值： 
                   * true: 表示 HTTPS 已启用。 
                   * false: 表示 HTTPS 未启用。 
             PrimaryOrigin ( String ): 否  表示一个主源站，以获取主源站配置中包含该主源站的那些域名。该参数值可以是一个 IP 地址，也可以是一个域名。 
             PageNum ( Long ): 否  表示一个页码，用以获取该页面上域名列表。该参数的默认值为 1。 
                   CDN 对符合过滤条件的域名进行分页。您可以根据响应参数 Total 和请求参数 PageSize 计算该 API 返回的页数。 
             PageSize ( Long ): 否  表示每页包含的域名数量。该参数的取值范围是 1-100，默认值是 10。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        PageNum ( Long ): 1 
        PageSize ( Long ): 10 
        Total ( Long ): 100 
        Data ( Array of Data ):  
       "字段"： Data
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Domain ( String ): www.example.com 
        ServiceType ( String ): web 
        Status ( String ): online 
        Cname ( String ): www.example.com.volcgslb.com 
        ServiceRegion ( String ): domestic 
        CreateTime ( Long ): 1625587200 
        UpdateTime ( Long ): 1601371409 
        Project ( String ): default 
        OriginProtocol ( String ): http 
        IPv6 ( Boolean ):  
        HTTPS ( Boolean ): true 
        PrimaryOrigin ( Array of String ): 1.2.3.4,2.3.4.5 
        BackupOrigin ( Array of String ): 1.2.3.4,2.3.4.5 
        ResourceTags ( Array of ResourceTags ):  
        CacheShared ( String ): target_host 
        CacheSharedTargetHost ( String ): www.test.com 
        IsConflictDomain ( Boolean ): false 
        DomainLock ( Object of DomainLock ):  
       "字段"： ResourceTags
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Key ( String ): userKey 
        Value ( String ): userValue 
       "字段"： DomainLock
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Remark ( String ): 域名锁定，不允许自助配置操作，域名下线 
        Status ( String ): on 
    """,
    "describe_origin_top_statistical_data": r""" 
    Args: 
        body: A JSON structure
             Domain ( String ): 是  指定一个域名进行数据统计。 
             EndTime ( Long ): 是  指定一个结束时间。时间格式是 Unix 时间戳，精度是秒。 
             Item ( String ): 是  指定一个统计对象。该参数的可用值如下： 
                   * url：表示对回源请求 URL 进行统计。 
             Metric ( String ): 是  指定一个统计指标。基于该指标的统计数据，对 Item 进行排序。您可以指定以下指标： 
                   * flux：表示回源请求所产生的流量。单位是 Byte。 
                   * pv：表示回源请求数。 
                   * status_2xx：表示在回源请求的响应状态码中，范围在 200-299 内的状态码数量。 
                   * status_3xx：表示范围在 300-399 内的状态码数量。 
                   * status_4xx：表示范围在 400-499 内的状态码数量。 
                   * status_5xx：表示范围在 500-599 内的状态码数量。 
             StartTime ( Long ): 是  指定一个开始时间。时间格式是 Unix 时间戳，精度是秒。StartTime 必须早于或者等于 EndTime。 
                   您必须同时指定 StartTime 和 EndTime，或者都不指定。如果您不指定这两个参数，该页面展示最近 24 小时的数据。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Domain ( String ): www.example.com 
        Item ( String ): url 
        Metric ( String ): flux 
        TopDataDetails ( Array of TopDataDetails ):  
       "字段"： TopDataDetails
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        ItemKey ( String ): https://www.example.com/birds/chickadee.png 
        Value ( Double ): 2341 
    """,
    "describe_district_data": r""" 
    Args: 
        body: A JSON structure
             Metric ( String ): 是  表示一个指标。该参数有以下取值： 
                   - traffic：表示 CDN 向用户传输的数据量，单位是 bytes。 
                   - bandwidth：表示基于 CDN 向用户传输的数据量而计算的带宽，单位是 bps。 
                   - requests：表示 CDN 收到的用户请求数量。 
                   - qps：表示 CDN 收到的用户请求的 QPS。 
                   - response_time：表示 CDN 响应用户请求所耗费的平均时间，单位是毫秒（ms）。 
                   - avg_speed：表示 CDN 向用户传输数据时的平均速度，单位是 Bps。 
                   - status_all：在 CDN 对用户请求的响应中，该参数表示以下各类别的状态码数量： 
                   	- 所有状态码的数量。 
                   	- 2xx 状态码的数量。 
                   	- 3xx 状态码的数量。 
                   	- 4xx 状态码的数量。 
                   	- 5xx 状态码的数量。 
                   	- 每个状态码的数量。 
                   - status_2xx：表示 2xx 状态码的数量以及该类别下每个状态码的数量。 
                   - status_3xx：表示 3xx 状态码的数量以及该类别下每个状态码的数量。 
                   - status_4xx：表示 4xx 状态码的数量以及该类别下每个状态码的数量。 
                   - status_5xx：表示 5xx 状态码的数量以及该类别下每个状态码的数量。 
                   关于每个指标的详情以及统计方式，参见 指标的定义以及统计方式。 
             StartTime ( Long ): 是  表示统计时间段的开始时间，格式是 Unix 时间戳，精度是秒。StartTime 必须早于或者等于 EndTime。同时，StartTime 与 EndTime 所表示的统计时间段不能超过 31 天。 
             EndTime ( Long ): 是  表示统计时间段的结束时间，格式是 Unix 时间戳，精度是秒。 
             Interval ( String ): 否  表示一个时间粒度。该 API 基于 Interval 将 StartTime 和 EndTime 所表示的统计时间段拆分成一系列的时间区间，然后对每个时间区间统计 Metric 数据。 
                   关于 Interval参数是如何用来拆分统计时间段，参考 统计时间段说明。  
                   该参数有以下取值： 
                   - 1min：表示时间粒度是 1 分钟。 
                   - 5min：表示时间粒度是 5 分钟。 
                   - hour：表示时间粒度是 1 小时。 
                   - day：表示时间粒度是 1 天。 
                   您可以指定的时间粒度受 StartTime 和 EndTime 所表示的时间范围的影响。 
                   - 如果时间范围 <= 1 天，您可以指定的时间粒度有 1min、5min、hour。 
                   - 如果 1 天 < 时间范围 <= 3 天，您可以指定的时间粒度有 5min、hour、day。 
                   - 如果 3 天 < 时间范围 <= 31 天，您可以指定的时间粒度有 hour、day。 
                   该参数的默认值是 5min。如果默认值不匹配时间范围，API 请求会失败。 
             Project ( String ): 否  表示一个项目。 
                   * 如果您指定了 Domain，该 API 对所有您指定的加速域名统计 Metric 数据。 
                   * 如果您指定了 Project ，但未指定 Domain，该 API 对您指定的项目统计 Metric 数据。参见 项目数据是如何统计的。 
                   * 如果您既未指定 Project ，也未指定 Domain，该 API 对所有加速域名统计 Metric 数据。 
             Domain ( String ): 否  表示一个或多个加速域名，用于对用户请求进行过滤。该 API 对您指定的每个加速域名统计 Metric 数据。您最多可以指定 50 个加速域名。多个加速域名之间使用逗号（,）分隔。如果不指定 Domain，表示不使用该参数对请求进行过滤。 
                   如果您指定了 Project，您指定的加速域名必须是属于该 Project 的。 
                   当子用户调用该 API 时，请留意以下说明： 
                   - 子用户只能指定其有权限访问的加速域名。子用户可以调用 ListCdnDomains 获取其有权限访问的加速域名。 
                   - 如果不指定该参数，表示所有该子用户有权限访问的那些加速域名。 
             Location ( String ): 否  表示国家和地区的代码，用于对用户请求进行过滤。您可以指定一个或者多个代码，CDN 对来自这些国家和地区的用户请求统计 Metric 数据。多个国家和地区代码之间使用逗号（,）分隔。您最多可以指定 30 个国家和地区。 
                   * 如果您指定了 Location，就不能指定 Province，反之亦然。 
                   * 如果您不指定 Location，表示不使用该参数对请求进行过滤。 
                   您可以调用 DescribeCdnRegionAndIsp 获取代码与国家和地区的对应表。 
             Province ( String ): 否  表示中国省级行政区的代码，用于对用户请求进行过滤。您可以指定一个或者多个代码，CDN 对来自这些省级行政区的用户请求统计 Metric 数据。多个代码之间使用逗号（,）分隔。您最多可以指定 10 个代码。 
                   如果您不指定 Province，表示不使用该参数对请求进行过滤。 
                   您可以调用 DescribeCdnRegionAndIsp 获取代码与中国省级行政区的对应表。 
             Isp ( String ): 否  表示请求所使用的中国网络运营商的代码，用于对用户请求进行过滤。例如，CT 表示中国电信。您可以指定一个或者多个代码，CDN 对使用这些网络运营商的用户请求统计 Metric 数据。多个代码之间使用逗号（,）分隔。您最多可以指定 5 个代码。 
                   - 当 Location 是 CHN 或者您指定了 Province 时，您才能指定 Isp。 
                   - 当您不指定 Isp 时，表示不使用该参数对请求进行过滤。 
                   您可以调用 DescribeCdnRegionAndIsp 获取代码与网络运营商的对应表。 
             Protocol ( String ): 否  表示请求使用的一个应用层协议，用于对用户请求进行过滤。该参数的可用值如下： 
                   - http：表示 HTTP 协议。 
                   - https：表示 HTTPS 协议。 
                   - quic：表示 QUIC 协议。 
                   如果不指定 Protocol，表示不使用该参数对请求进行过滤。 
             IpVersion ( String ): 否  表示请求使用的一个网络层协议，用于对用户请求进行过滤。该参数的可用值如下： 
                   - IPv4：表示 IPv4 协议。 
                   - IPv6：表示 IPv6 协议。 
                   如果不指定 IpVersion，表示不使用该参数对请求进行过滤。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        MetricDataList ( Array of MetricDataList ):  
       "字段"： MetricDataList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Metric ( String ): traffic 
        Values ( Array of Values ):  
       "字段"： Values
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        TimeStamp ( Long ): 1710273600 
        Value ( Double ): 4567 
    """,
    "describe_district_ranking": r""" 
    Args: 
        body: A JSON structure
             Item ( String ): 是  表示一个分组条件，用于对 Metric 数据进行汇总。该参数有以下取值： 
                   - location：表示用户请求来自的国家和地区。 
                   - province：表示用户请求来自的中国省级行政区。 
                   - isp：表示用户请求使用的中国网络运营商。 
                   当 Item 是 province 或 isp 时，Metric 数据是基于来自中国的请求而统计的。 
             Metric ( String ): 是  表示一个指标。该参数有以下取值： 
                   - traffic：表示内容分发网络向用户传输的数据量，单位是 bytes。 
                   - bandwidth：表示基于内容分发网络向用户传输的数据量而计算的带宽峰值，单位是 bps。 
                   - requests：表示内容分发网络收到的用户请求数量。 
                   关于每个指标的详情以及统计方式，参见 指标的定义以及统计方式。 
             StartTime ( Long ): 是  表示统计时间段的开始时间，格式是 Unix 时间戳，精度是秒。StartTime 必须早于或者等于 EndTime。同时，StartTime 和 EndTime 所表示的统计时间段不能超过 31 天。 
             EndTime ( Long ): 是  表示统计时间段的结束时间，格式是 Unix 时间戳，精度是秒。 
             Interval ( String ): 否  表示一个时间粒度。该 API 基于 Interval 将 StartTime 和 EndTime 所表示的统计时间段拆分成一系列的时间区间，然后对每个时间区间统计 Metric 的数据。 
                   关于 Interval 参数是如何用来拆分统计时间段，参考 统计时间段说明。 
                   该参数有以下取值： 
                   - 1min：表示时间粒度是 1 分钟。 
                   - 5min：表示时间粒度是 5 分钟。 
                   您可以指定的时间粒度受 StartTime 和 EndTime 所表示的时间范围的影响。 
                   - 如果时间范围 <= 1 天，您可以指定的时间粒度有 1min、5min。 
                   - 如果 1 天 < 时间范围 <= 31 天，您可以指定的时间粒度只能是 5min。 
                   该参数的默认值是 5min。如果默认值不匹配时间范围，API 请求会失败。 
             Project ( String ): 否  表示一个项目。 
                   * 如果您指定了 Domain，该 API 对所有您指定的加速域名统计 Metric 数据。 
                   * 如果您指定了 Project ，但未指定 Domain，该 API 对您指定的项目统计 Metric 数据。参见 项目数据是如何统计的。 
                   * 如果您既未指定 Project ，也未指定 Domain，该 API 对所有加速域名统计 Metric 数据。 
             Domain ( String ): 否  表示一个或多个加速域名，用于对用户请求进行过滤。该 API 对您指定的每个加速域名统计 Metric 数据。您最多可以指定 50 个加速域名。多个加速域名之间使用逗号（,）分隔。如果不指定 Domain，表示不使用该参数对请求进行过滤。 
                   如果您指定了 Project，您指定的加速域名必须是属于该 Project 的。 
                   当子用户调用该 API 时，请留意以下说明： 
                   - 子用户只能指定其有权限访问的加速域名。子用户可以调用 ListCdnDomains 获取其有权限访问的加速域名。 
                   - 如果不指定该参数，表示所有该子用户有权限访问的那些加速域名。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Item ( String ): location 
        TopDataDetails ( Array of TopDataDetails ):  
       "字段"： TopDataDetails
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Metric ( String ): traffic 
        ValueDetails ( Array of ValueDetails ):  
       "字段"： ValueDetails
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        ItemKey ( String ): CHN 
        Ratio ( Double ): 0.9527 
        Timestamp ( Long ): 1710419700 
        Value ( Double ): 95270 
    """,
    "describe_edge_status_code_ranking": r""" 
    Args: 
        body: A JSON structure
             Item ( String ): 是  表示一个分组条件。当前，该参数值只能是 domain，表示按 Domain 对 Metric 数据进行汇总。 
             Metric ( String ): 是  对于 CDN 对用户请求的响应，该参数表示以下某个类别的状态码数量： 
                   - status_2xx：表示 2xx 状态码数量。 
                   - status_3xx：表示 3xx 状态码数量。 
                   - status_4xx：表示 4xx 状态码数量。 
                   - status_5xx：表示 5xx 状态码数量。 
             StartTime ( Long ): 是  表示统计时间段的开始时间，格式是 Unix 时间戳，精度是秒。StartTime 必须早于或者等于 EndTime。同时，StartTime 和 EndTime 所表示的统计时间段不能超过 31 天。 
             EndTime ( Long ): 是  表示统计时间段的结束时间，格式是 Unix 时间戳，精度是秒。 
             Interval ( String ): 否  表示一个时间粒度。该 API 基于 Interval 将 StartTime 和 EndTime 所表示的统计时间段拆分成一系列的时间区间，然后对每个时间区间统计 Metric 的数据。 
                   关于 Interval 参数是如何用来拆分统计时间段，参考 统计时间段说明。 
                   该参数有以下取值： 
                   - 1min：表示时间粒度是 1 分钟。 
                   - 5min：表示时间粒度是 5 分钟。 
                   您可以指定的时间粒度受 StartTime 和 EndTime 所表示的时间范围的影响。 
                   - 如果时间范围 <= 1 天，您可以指定的时间粒度有 1min、5min。 
                   - 如果 1 天 < 时间范围 <= 31 天，您可以指定的时间粒度有 5min。 
                   该参数的默认值是 5min。如果默认值不匹配时间范围，API 请求会失败。 
             Project ( String ): 否  表示一个项目。 
                   * 如果您指定了 Domain，该 API 对所有您指定的加速域名统计 Metric 数据。 
                   * 如果您指定了 Project ，但未指定 Domain，该 API 对您指定的项目统计 Metric 数据。参见 项目数据是如何统计的。 
                   * 如果您既未指定 Project ，也未指定 Domain，该 API 对所有加速域名统计 Metric 数据。 
             Domain ( String ): 否  表示一个或多个加速域名，用于对用户请求进行过滤。该 API 对您指定的每个加速域名统计 Metric 数据。您最多可以指定 50 个加速域名。多个加速域名之间使用逗号（,）分隔。如果不指定 Domain，表示不使用该参数对请求进行过滤。 
                   如果您指定了 Project，您指定的加速域名必须是属于该 Project 的。 
                   当子用户调用该 API 时，请留意以下说明： 
                   - 子用户只能指定其有权限访问的加速域名。子用户可以调用 ListCdnDomains 获取其有权限访问的加速域名。 
                   - 如果不指定该参数，表示所有该子用户有权限访问的那些加速域名。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Item ( String ): domain 
        Metric ( String ): status_4xx 
        TopDataDetails ( Array of TopDataDetails ):  
       "字段"： TopDataDetails
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        ItemKey ( String ): www.example.com 
        Status2xx ( Double ): 45678 
        Status2xxRatio ( Double ): 0.47 
        Status3xx ( Double ): 0 
        Status3xxRatio ( Double ): 0 
        Status4xx ( Double ): 3 
        Status4xxRatio ( Double ): 0.0001 
        Status5xx ( Double ): 0 
        Status5xxRatio ( Double ): 0 
    """,
    "describe_district_summary": r""" 
    Args: 
        body: A JSON structure
             Metric ( String ): 是  表示一个统计指标。该参数有以下取值： 
                   - traffic：表示 CDN 向用户传输的数据量，单位是 bytes。 
                   - bandwidth：表示基于 CDN 向用户传输的数据量而计算的带宽峰值，单位是 bps。 
                   - requests：表示 CDN 收到的用户请求数量。 
                   - qps：表示 CDN 收到的用户请求的 QPS 峰值。 
                   - response_time：表示 CDN 响应用户请求所耗费的平均时间，单位是毫秒（ms）。 
                   - avg_speed：表示 CDN 向用户传输数据时的平均速度，单位是 Bps。 
                   - status_all：在 CDN 对用户请求的响应中，该参数表示以下类别的状态码数量： 
                   	- 所有状态码的数量。 
                   	- 2xx 状态码的数量。 
                   	- 3xx 状态码的数量。 
                   	- 4xx 状态码的数量。 
                   	- 5xx 状态码的数量。 
                   	- 每个状态码的数量。 
                   - status_2xx：表示 2xx 状态码的数量以及该类别下每个状态码的数量。 
                   - status_3xx：表示 3xx 状态码的数量以及该类别下每个状态码的数量。 
                   - status_4xx：表示 4xx 状态码的数量以及该类别下每个状态码的数量。 
                   - status_5xx：表示 5xx 状态码的数量以及该类别下每个状态码的数量。 
                   关于每个指标的详情以及统计方式，参见 指标的定义以及统计方式。 
             StartTime ( Long ): 是  表示统计时间段的开始时间，格式是 Unix 时间戳，精度是秒。StartTime 必须早于或者等于 EndTime。同时，StartTime 与 EndTime 所表示的统计时间段不能超过 31 天。 
             EndTime ( Long ): 是  表示统计时间段的结束时间，格式是 Unix 时间戳，精度是秒。 
             Interval ( String ): 否  表示一个时间粒度。该 API 基于 Interval 将 StartTime 和 EndTime 所表示的统计时间段拆分成一系列的时间区间，然后对每个时间区间统计 Metric 数据。 
                   关于 Interval 参数是如何用来拆分统计时间段，参考 统计时间段说明。 
                   该参数有以下取值： 
                   - 1min：表示时间粒度是 1 分钟。 
                   - 5min：表示时间粒度是 5 分钟。 
                   您可以指定的时间粒度受 StartTime 和 EndTime 所表示的时间范围的影响。 
                   - 如果时间范围 <= 1 天，您可以指定的时间粒度有 1min、5min。 
                   - 如果 1 天 < 时间范围 <= 31 天，您可以指定的时间粒度只能是 5min。 
                   该参数的默认值是 5min。如果默认值不匹配时间范围，API 请求会失败。 
             Project ( String ): 否  表示一个项目。 
                   * 如果您指定了 Domain，该 API 对所有您指定的加速域名统计 Metric 数据。 
                   * 如果您指定了 Project ，但未指定 Domain，该 API 对您指定的项目统计 Metric 数据。参见 项目数据是如何统计的。 
                   * 如果您既未指定 Project ，也未指定 Domain，该 API 对所有加速域名统计 Metric 数据。 
             Domain ( String ): 否  表示一个或多个加速域名，用于对用户请求进行过滤。该 API 对您指定的每个加速域名统计 Metric 数据。您最多可以指定 50 个加速域名。多个加速域名之间使用逗号（,）分隔。如果不指定 Domain，表示不使用该参数对请求进行过滤。 
                   如果您指定了 Project，您指定的加速域名必须是属于该 Project 的。 
                   当子用户调用该 API 时，请留意以下说明： 
                   - 子用户只能指定其有权限访问的加速域名。子用户可以调用 ListCdnDomains 获取其有权限访问的加速域名。 
                   - 如果不指定该参数，表示所有该子用户有权限访问的那些加速域名。 
             Location ( String ): 否  表示国家和地区的代码，用于对用户请求进行过滤。您可以指定一个或者多个代码，CDN 对来自这些国家和地区的用户请求统计 Metric 数据。多个国家和地区代码之间使用逗号（,）分隔。您最多可以指定 30 个国家和地区。 
                   * 如果您指定了 Location，就不能指定 Province，反之亦然。 
                   * 如果您不指定 Location，表示不使用该参数对请求进行过滤。 
                   您可以调用 DescribeCdnRegionAndIsp 获取代码与国家和地区的对应表。 
             Province ( String ): 否  表示中国省级行政区的代码，用于对用户请求进行过滤。您可以指定一个或者多个代码，CDN 对来自这些省级行政区的用户请求统计 Metric 数据。多个代码之间使用逗号（,）分隔。您最多可以指定 10 个代码。 
                   如果您不指定 Province，表示不使用该参数对请求进行过滤。 
                   您可以调用 DescribeCdnRegionAndIsp 获取代码与中国省级行政区的对应表。 
             Isp ( String ): 否  表示请求所使用的中国网络运营商的代码，用于对用户请求进行过滤。例如，CT 表示中国电信。您可以指定一个或者多个代码，CDN 对使用这些网络运营商的用户请求统计 Metric 数据。多个代码之间使用逗号（,）分隔。您最多可以指定 5 个代码。 
                   - 当 Location 是 CHN 或者您指定了 Province 时，您才能指定 Isp。 
                   - 当您不指定 Isp 时，表示不使用该参数对请求进行过滤。 
                   您可以调用 DescribeCdnRegionAndIsp 获取代码与网络运营商的对应表。 
             Protocol ( String ): 否  表示请求使用的一个应用层协议，用于对用户请求进行过滤。该参数的可用值如下： 
                   - http：表示 HTTP 协议。 
                   - https：表示 HTTPS 协议。 
                   - quic：表示 QUIC 协议。 
                   如果不指定 Protocol，表示不使用该参数对请求进行过滤。 
             IpVersion ( String ): 否  表示请求使用的一个网络层协议，用于对用户请求进行过滤。该参数的可用值如下： 
                   - IPv4：表示 IPv4 协议。 
                   - IPv6：表示 IPv6 协议。 
                   如果不指定 IpVersion，表示不使用该参数对请求进行过滤。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        MetricDataList ( Array of MetricDataList ):  
       "字段"： MetricDataList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Metric ( String ): traffic 
        Value ( Double ): 3475788 
    """,
    "describe_origin_data": r""" 
    Args: 
        body: A JSON structure
             Metric ( String ): 是  表示一个指标。该参数有以下取值： 
                   - traffic：表示源站向内容分发网络传输的数据量，单位是 bytes。 
                   - bandwidth：表示基于源站向内容分发网络传输的数据量而计算的带宽，单位是 bps。 
                   - requests：表示回源请求数量。 
                   - qps：表示回源请求的 QPS。 
                   - status_all：在内容分发网络收到的源站响应中，该参数表示以下类别的状态码数量： 
                   	- 所有状态码的数量。 
                   	- 所有 2xx 状态码的数量。 
                   	- 所有 3xx 状态码的数量。 
                   	- 所有 4xx 状态码的数量。 
                   	- 所有 5xx 状态码的数量。 
                   	- 每个状态码的数量。 
                   - status_2xx：表示所有 2xx 状态码的数量以及该类别下每个状态码的数量。 
                   - status_3xx：表示所有 3xx 状态码的数量以及该类别下每个状态码的数量。 
                   - status_4xx：表示所有 4xx 状态码的数量以及该类别下每个状态码的数量。 
                   - status_5xx：表示所有 5xx 状态码的数量以及该类别下每个状态码的数量。 
                   关于每个指标的详情以及统计方式，参见 指标的定义以及统计方式。 
             StartTime ( Long ): 是  表示统计时间段的开始时间，格式是 Unix 时间戳，精度是秒。StartTime 必须早于或者等于 EndTime。同时，StartTime 与 EndTime 所表示的统计时间段不能超过 31 天。 
             EndTime ( Long ): 是  表示统计时间段的结束时间，格式是 Unix 时间戳，精度是秒。 
             Interval ( String ): 否  表示一个时间粒度。该 API 基于 Interval 将 StartTime 和 EndTime 所表示的统计时间段拆分成一系列的时间区间，然后对每个时间区间统计 Metric 数据。 
                   关于 Interva参数是如何用来拆分统计时间段，参考 统计时间段说明。  
                   该参数有以下取值： 
                   - 1min：表示时间粒度是 1 分钟。 
                   - 5min：表示时间粒度是 5 分钟。 
                   - hour：表示时间粒度是 1 小时。 
                   - day：表示时间粒度是 1 天。 
                   您可以指定的时间粒度受 StartTime 和 EndTime 所表示的时间范围的影响。 
                   - 如果时间范围 <= 1 天，您可以指定的时间粒度有 1min、5min、hour。 
                   - 如果 1 天 < 时间范围 <= 3 天，您可以指定的时间粒度有 5min、hour、day。 
                   - 如果 3 天 < 时间范围 <= 31 天，您可以指定的时间粒度有 hour、day。 
                   该参数的默认值是 5min。如果默认值不匹配时间范围，API 请求会失败。 
             Project ( String ): 否  表示一个项目。 
                   * 如果您指定了 Domain，该 API 对所有您指定的加速域名统计 Metric 数据。 
                   * 如果您指定了 Project ，但未指定 Domain，该 API 对您指定的项目统计 Metric 数据。参见 项目数据是如何统计的。 
                   * 如果您既未指定 Project ，也未指定 Domain，该 API 对所有加速域名统计 Metric 数据。 
             Domain ( String ): 否  表示一个或多个加速域名，用于对用户请求进行过滤。该 API 对您指定的每个加速域名统计 Metric 数据。您最多可以指定 50 个加速域名。多个加速域名之间使用逗号（,）分隔。如果不指定 Domain，表示不使用该参数对请求进行过滤。 
                   如果您指定了 Project，您指定的加速域名必须是属于该 Project 的。 
                   当子用户调用该 API 时，请留意以下说明： 
                   - 子用户只能指定其有权限访问的加速域名。子用户可以调用 ListCdnDomains 获取其有权限访问的加速域名。 
                   - 如果不指定该参数，表示所有该子用户有权限访问的那些加速域名。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        MetricDataList ( Array of MetricDataList ):  
       "字段"： MetricDataList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Metric ( String ): traffic 
        Values ( Array of Values ):  
       "字段"： Values
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        TimeStamp ( Long ): 1710273600 
        Value ( Double ): 4568 
    """,
    "describe_edge_ranking": r""" 
    Args: 
        body: A JSON structure
             Item ( String ): 是  表示一个分组条件，用于对 Metric 数据进行汇总。该参数有以下取值： 
                   - domain：表示按加速域名统计指标数据。 
                   - billingRegion：表示按计费区域统计指标数据。 
                   - project：表示按项目统计指标数据。在这个情况下，您不能指定 Domain。参见 项目数据是如何统计的。 
             Metric ( String ): 是  表示一个指标。该参数有以下取值： 
                   - traffic：表示 CDN 向用户传输的数据量，单位是 bytes。 
                   - bandwidth：表示基于 CDN 向用户传输的数据量而计算的带宽峰值，单位是 bps。 
                   - requests：表示 CDN 收到的用户请求数量。 
                   关于每个指标的详情以及统计方式，参见 指标的定义以及统计方式。 
             BillingRegion ( String ): 否  表示一个或多个计费区域，用于对用户请求进行过滤。该 API 对来自这些计费区域的用户请求统计 Metric 数据。多个计费区域之间使用逗号（,）分隔。该参数有以下取值： 
                   - CHN：表示中国内地。 
                   - EU：表示欧洲区。 
                   - NA：表示北美区。 
                   - SA：表示南美区。 
                   - MEA：表示中东区和非洲区。 
                   - AP1：表示亚太一区。 
                   - AP2：表示亚太二区。 
                   - AP3：表示亚太三区。 
                   如果不指定 BillingRegion，表示不使用该参数对请求进行过滤。 
             StartTime ( Long ): 是  表示统计时间段的开始时间，格式是 Unix 时间戳，精度是秒。StartTime 必须早于或者等于 EndTime。同时，StartTime 和 EndTime 所表示的统计时间段不能超过 31 天。 
             EndTime ( Long ): 是  表示统计时间段的结束时间，格式是 Unix 时间戳，精度是秒。 
             Interval ( String ): 否  表示一个时间粒度。该 API 基于 Interval 将 StartTime 和 EndTime 所表示的统计时间段拆分成一系列的时间区间，然后对每个时间区间统计 Metric 的数据。 
                   关于 Interval 参数是如何用来拆分统计时间段，参考 统计时间段说明。 
                   该参数有以下取值： 
                   - 1min：表示时间粒度是 1 分钟。 
                   - 5min：表示时间粒度是 5 分钟。 
                   您可以指定的时间粒度受 StartTime 和 EndTime 所表示的时间范围的影响。 
                   - 如果时间范围 <= 1 天，您可以指定的时间粒度有 1min、5min。 
                   - 如果 1 天 < 时间范围 <= 31 天，您可以指定的时间粒度有 5min。 
                   该参数的默认值是 5min。如果默认值不匹配时间范围，API 请求会失败。 
             Project ( String ): 否  表示一个项目。如果不指定 Project，表示所有项目。 
                   对于 Project 和 Domain： 
                   - 当您指定 Project，不指定 Domain 时，CDN 按 Item 统计指定项目的 Metric 数据。参见 项目数据是如何统计的。 
                   - 其他情况下，CDN 按 Item 统计指定加速域名的 Metric 数据。 
                   参见 Item、Project、Domain 的配置组合。 
             Domain ( String ): 否  表示一个或多个加速域名，用于对用户请求进行过滤。您最多可以指定 50 个加速域名。多个域名之间使用逗号（,）分隔。如果不指定 Domain，表示所有加速域名。关于 Domain 参数的额外描述，参见 Project 参数。 
                   当子用户调用该 API 时，请留意以下说明： 
                   - 子用户只能指定其有权限访问的加速域名。子用户可以调用 ListCdnDomains 获取其有权限访问的加速域名。 
                   - 如果不指定该参数，表示所有该子用户有权限访问的那些加速域名。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Item ( String ): domain 
        TopDataDetails ( Array of TopDataDetails ):  
       "字段"： TopDataDetails
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Metric ( String ): requests 
        ValueDetails ( Array of ValueDetails ):  
       "字段"： ValueDetails
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        ItemKey ( String ): www.example.com 
        Ratio ( Double ): 0.978 
        Timestamp ( Long ): 1710419700 
        Value ( Double ): 456 
    """,
    "describe_edge_data": r""" 
    Args: 
        body: A JSON structure
             Metric ( String ): 是  表示一个指标。该参数有以下取值： 
                   - traffic：表示 CDN 向用户传输的数据量，单位是 bytes。 
                   - bandwidth：表示基于 CDN 向用户传输的数据量而计算的带宽，单位是 bps。 
                   - requests：表示 CDN 收到的用户请求数量。 
                   - qps：表示 CDN 收到的用户请求的 QPS。 
                   - traffic_hitrate：表示 CDN 的流量命中率，以数值形式显示。例如，0.9999 表示 99.99%。 
                   - response_time：表示 CDN 响应用户请求所耗费的平均时间，单位是毫秒（ms）。 
                   - avg_speed：表示 CDN 向用户传输数据时的平均速度，单位是 Bps。 
                   - status_all：在 CDN 对用户请求的响应中，该参数表示以下类别的状态码数量： 
                   	- 所有状态码的数量。 
                   	- 2xx 状态码的数量。 
                   	- 3xx 状态码的数量。 
                   	- 4xx 状态码的数量。 
                   	- 5xx 状态码的数量。 
                   	- 每个状态码的数量。 
                   - status_2xx：表示 2xx 状态码的数量以及该类别下每个状态码的数量。 
                   - status_3xx：表示 3xx 状态码的数量以及该类别下每个状态码的数量。 
                   - status_4xx：表示 4xx 状态码的数量以及该类别下每个状态码的数量。 
                   - status_5xx：表示 5xx 状态码的数量以及该类别下每个状态码的数量。 
                   关于每个指标的详情以及统计方式，参见 指标的定义以及统计方式。 
             StartTime ( Long ): 是  表示统计时间段的开始时间，格式是 Unix 时间戳，精度是秒。StartTime 必须早于或者等于 EndTime。同时，StartTime 与 EndTime 所表示的统计时间段不能超过 31 天。 
             EndTime ( Long ): 是  表示统计时间段的结束时间，格式是 Unix 时间戳，精度是秒。 
             Interval ( String ): 否  表示一个时间粒度。该 API 会基于 Interval 将 StartTime 和 EndTime 所表示的统计时间段拆分成一系列的时间区间，然后对每个时间区间统计 Metric 数据。 
                   关于 Interval 参数是如何用来拆分统计时间段，参考 统计时间段说明。 
                   该参数有以下取值： 
                   - 1min：表示时间粒度是 1 分钟。 
                   - 5min：表示时间粒度是 5 分钟。 
                   - hour：表示时间粒度是 1 小时。 
                   - day：表示时间粒度是 1 天。 
                   您可以指定的时间粒度受 StartTime 和 EndTime 所表示的时间范围的影响。 
                   - 如果时间范围 <= 1 天，您可以指定的时间粒度有 1min、5min、hour。 
                   - 如果 1 天 < 时间范围 <= 3 天，您可以指定的时间粒度有 5min、hour、day。 
                   - 如果 3 天 < 时间范围 <= 31 天，您可以指定的时间粒度有 hour、day。 
                   该参数的默认值是 5min。如果默认值不匹配时间范围，API 请求会失败。 
             Project ( String ): 否  表示一个项目。 
                   * 如果您指定了 Domain，该 API 对所有您指定的加速域名统计 Metric 数据。 
                   * 如果您指定了 Project ，但未指定 Domain，该 API 对您指定的项目统计 Metric 数据。参见 项目数据是如何统计的。 
                   * 如果您既未指定 Project ，也未指定 Domain，该 API 对所有加速域名统计 Metric 数据。 
             Domain ( String ): 否  表示一个或多个加速域名，用于对用户请求进行过滤。该 API 对您指定的每个加速域名统计 Metric 数据。您最多可以指定 50 个加速域名。多个加速域名之间使用逗号（,）分隔。如果不指定 Domain，表示不使用该参数对请求进行过滤。 
                   如果您指定了 Project，您指定的加速域名必须是属于该 Project 的。 
                   当子用户调用该 API 时，请留意以下说明： 
                   - 子用户只能指定其有权限访问的加速域名。子用户可以调用 ListCdnDomains 获取其有权限访问的加速域名。 
                   - 如果不指定该参数，表示所有该子用户有权限访问的那些加速域名。 
             BillingRegion ( String ): 否  表示一个或多个计费区域，用于对用户请求进行过滤。该 API 对来自这些计费区域的用户请求统计 Metric 数据。多个计费区域之间使用逗号（,）分隔。该参数有以下取值： 
                   - CHN：表示中国内地。 
                   - EU：表示欧洲区。 
                   - NA：表示北美区。 
                   - SA：表示南美区。 
                   - MEA：表示中东区和非洲区。 
                   - AP1：表示亚太一区。 
                   - AP2：表示亚太二区。 
                   - AP3：表示亚太三区。 
                   如果不指定 BillingRegion，表示不使用该参数对请求进行过滤。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        MetricDataList ( Array of MetricDataList ):  
       "字段"： MetricDataList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Metric ( String ): traffic 
        Values ( Array of Values ):  
       "字段"： Values
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        TimeStamp ( Long ): 1710273600 
        Value ( Double ): 4567 
    """,
    "describe_edge_summary": r""" 
    Args: 
        body: A JSON structure
             Metric ( String ): 是  表示一个指标。该参数有以下取值： 
                   - traffic：表示内容分发网络向用户传输的数据量，单位是 bytes。 
                   - bandwidth：表示基于内容分发网络向用户传输的数据量而计算的带宽峰值，单位是 bps。 
                   - requests：表示内容分发网络收到的用户请求数量。 
                   - qps：表示内容分发网络收到的用户请求的 QPS 峰值。 
                   - traffic_hitrate：表示内容分发网络的流量命中率，以数值形式显示。例如，0.9999 表示 99.99%。 
                   - response_time：表示内容分发网络响应用户请求所耗费的平均时间，单位是毫秒（ms）。 
                   - avg_speed：表示内容分发网络向用户传输数据时的平均速度，单位是 Bps。 
                   - status_all：在内容分发网络对用户请求的响应中，该参数表示以下类别的状态码数量： 
                   	- 所有状态码的数量。 
                   	- 2xx 状态码的数量。 
                   	- 3xx 状态码的数量。 
                   	- 4xx 状态码的数量。 
                   	- 5xx 状态码的数量。 
                   	- 每个状态码的数量。 
                   - status_2xx：表示 2xx 状态码的数量以及该类别下每个状态码的数量。 
                   - status_3xx：表示 3xx 状态码的数量以及该类别下每个状态码的数量。 
                   - status_4xx：表示 4xx 状态码的数量以及该类别下每个状态码的数量。 
                   - status_5xx：表示 5xx 状态码的数量以及该类别下每个状态码的数量。 
                   关于每个指标的详情以及统计方式，参见 指标的定义以及统计方式。 
             StartTime ( Long ): 是  表示统计时间段的开始时间，格式是 Unix 时间戳，精度是秒。StartTime 必须早于或者等于 EndTime。同时，StartTime 与 EndTime 所表示的统计时间段不能超过 31 天。 
             EndTime ( Long ): 是  表示统计时间段的结束时间，格式是 Unix 时间戳，精度是秒。 
             Interval ( String ): 否  表示一个时间粒度。该 API 基于 Interval 将 StartTime 和 EndTime 所表示的统计时间段拆分成一系列的时间区间，然后对每个时间区间统计 Metric 数据。 
                   关于 Interval 参数是如何用来拆分统计时间段，参考 统计时间段说明。 
                   该参数有以下取值： 
                   - 1min：表示时间粒度是 1 分钟。 
                   - 5min：表示时间粒度是 5 分钟。 
                   您可以指定的时间粒度受 StartTime 和 EndTime 所表示的时间范围的影响。 
                   - 如果时间范围 <= 1 天，您可以指定的时间粒度有 1min、5min。 
                   - 如果 1 天 < 时间范围 <= 31 天，您可以指定的时间粒度只能是 5min。 
                   该参数的默认值是 5min。如果默认值不匹配时间范围，API 请求会失败。 
             Project ( String ): 否  表示一个项目。 
                   * 如果您指定了 Domain，该 API 对所有您指定的加速域名统计 Metric 数据。 
                   * 如果您指定了 Project ，但未指定 Domain，该 API 对您指定的项目统计 Metric 数据。参见 项目数据是如何统计的。 
                   * 如果您既未指定 Project ，也未指定 Domain，该 API 对所有加速域名统计 Metric 数据。 
             Domain ( String ): 否  表示一个或多个加速域名，用于对用户请求进行过滤。该 API 对您指定的每个加速域名统计 Metric 数据。您最多可以指定 50 个加速域名。多个加速域名之间使用逗号（,）分隔。如果不指定 Domain，表示不使用该参数对请求进行过滤。 
                   如果您指定了 Project，您指定的加速域名必须是属于该 Project 的。 
                   当子用户调用该 API 时，请留意以下说明： 
                   - 子用户只能指定其有权限访问的加速域名。子用户可以调用 ListCdnDomains 获取其有权限访问的加速域名。 
                   - 如果不指定该参数，表示所有该子用户有权限访问的那些加速域名。 
             BillingRegion ( String ): 否  表示一个或多个计费区域，用于对用户请求进行过滤。该 API 对来自这些计费区域的用户请求统计 Metric 数据。多个计费区域之间使用逗号（,）分隔。该参数有以下取值： 
                   - CHN：表示中国内地。 
                   - EU：表示欧洲区。 
                   - NA：表示北美区。 
                   - SA：表示南美区。 
                   - MEA：表示中东区和非洲区。 
                   - AP1：表示亚太一区。 
                   - AP2：表示亚太二区。 
                   - AP3：表示亚太三区。 
                   如果不指定 BillingRegion，表示不使用该参数对请求进行过滤。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        MetricDataList ( Array of MetricDataList ):  
       "字段"： MetricDataList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Metric ( String ): traffic 
        Value ( Double ): 3475788 
    """,
    "describe_origin_ranking": r""" 
    Args: 
        body: A JSON structure
             Item ( String ): 是  表示一个分组条件，用于对 Metric 数据进行汇总。该参数有以下取值： 
                   - domain：表示按加速域名统计指标数据。 
                   - project：表示按项目统计指标数据。在这个情况下，您不能指定 Domain。参见 项目数据是如何统计的。 
             Metric ( String ): 是  表示一个指标。该参数有以下取值： 
                   - traffic：表示源站向 CDN 传输的数据量，单位是 bytes。 
                   - bandwidth：表示基于源站向 CDN 传输的数据量而计算的带宽峰值，单位是 bps。 
                   - requests：表示回源请求的数量。 
                   关于每个指标的详情以及统计方式，参见 指标的定义以及统计方式。 
             StartTime ( Long ): 是  表示统计时间段的开始时间，格式是 Unix 时间戳，精度是秒。StartTime 必须早于或者等于 EndTime。同时，StartTime 和 EndTime 所表示的统计时间段不能超过 31 天。 
             EndTime ( Long ): 是  表示统计时间段的结束时间，格式是 Unix 时间戳，精度是秒。 
             Interval ( String ): 否  表示一个时间粒度。该 API 基于 Interval 将 StartTime 和 EndTime 所表示的统计时间段拆分成一系列的时间区间，然后对每个时间区间统计 Metric 的数据。 
                   关于 Interval 参数是如何用来拆分统计时间段，参考 统计时间段说明。 
                   该参数有以下取值： 
                   - 1min：表示时间粒度是 1 分钟。 
                   - 5min：表示时间粒度是 5 分钟。 
                   您可以指定的时间粒度受 StartTime 和 EndTime 所表示的时间范围的影响。 
                   - 如果时间范围 <= 1 天，您可以指定的时间粒度有 1min、5min。 
                   - 如果 1 天 < 时间范围 <= 31 天，您可以指定的时间粒度只能是 5min。 
                   该参数的默认值是 5min。如果默认值不匹配时间范围，API 请求会失败。 
             Project ( String ): 否  表示一个项目。如果不指定 Project，表示所有项目。 
                   对于 Project 和 Domain： 
                   - 当您指定 Project，不指定 Domain 时，CDN 按 Item 统计指定项目的 Metric 数据。参见 项目数据是如何统计的。 
                   - 其他情况下，CDN 按 Item 统计指定加速域名的 Metric 数据。 
             Domain ( String ): 否  表示一个或多个加速域名，用于对回源请求进行过滤。您最多可以指定 50 个加速域名。多个加速域名之间使用逗号（,）分隔。如果不指定 Domain，表示所有加速域名。关于 Domain 参数的额外描述，参见 Project 参数。 
                   当子用户调用该 API 时，请留意以下说明： 
                   - 子用户只能指定其有权限访问的加速域名。子用户可以调用 ListCdnDomains 获取其有权限访问的加速域名。 
                   - 如果不指定该参数，表示所有该子用户有权限访问的那些加速域名。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Item ( String ): domain 
        TopDataDetails ( Array of TopDataDetails ):  
       "字段"： TopDataDetails
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Metric ( String ): traffic 
        ValueDetails ( Array of ValueDetails ):  
       "字段"： ValueDetails
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        ItemKey ( String ): www.example.com 
        Ratio ( Double ): 0.867 
        Timestamp ( Long ): 1710419700 
        Value ( Double ): 457 
    """,
    "describe_statistical_ranking": r""" 
    Args: 
        body: A JSON structure
             Item ( String ): 是  表示一个热门对象的类型作为分组和排序条件。 该 API 按 Item 对 Metric 数据进行汇总并对这些汇总数据进行排序。该参数有以下取值： 
                   - region：表示请求客户端所在的国家或地区。 
                   - url：表示请求 URL 中的路径。 
                   - referer：表示请求中的 Referer 域名。 
                   - ua：表示请求中的 User-Agent 字符串。 
                   - clientip：表示客户端的 IP 地址。 
                   - 当 Item 是 ua 时，您还需要指定 UaType 作为一个补充分组条件。 
                   - 当 Item 是 region 时，您还需要指定 Area 作为一个补充分组条件。 
             Metric ( String ): 是  表示一个指标。该参数的可用值受 Item 的影响。 
                   - 当 Item 是 referer、ua 或 clientip 时，该参数有以下取值： 
                   	- traffic：表示内容分发网络向用户传输的数据量，单位是 bytes。 
                   	- requests：表示内容分发网络收到的用户请求的数量。 
                   - 当 Item 是 url 时，该参数有以下取值： 
                   	- traffic 
                   	- requests 
                   	- status_2xx：在内容分发网络对用户请求的响应中，该参数表示 2xx 状态码的数量。 
                   	- status_3xx：表示 3xx 状态码的数量。 
                   	- status_4xx：表示 4xx 状态码的数量。 
                   	- status_5xx：表示 5xx 状态码的数量。 
                   - 当 Item 是 region 时，该参数有以下取值。 
                   	- clientip：表示独立客户端 IP 地址的数量。 
                   	当 Item 是 region 时，该参数有默认值 clientip，并且可以不指定。 
             StartTime ( Long ): 是  表示统计时间段的开始时间，格式是 Unix 时间戳，精度是秒。StartTime 必须早于或者等于 EndTime。同时，StartTime 和 EndTime 所表示的统计时间段不能超过 31 天。 
                   * StartTime 和 EndTime 指定了统计时间段。但是实际统计时间段的开始时间和结束时间都是小时级别的。 
                     例子：StartTime 表示的时间是 15:07，EndTime 表示的时间是 15:21，那么实际的统计时间段是 [15:00,16:00）。 
                     需要留意的是，如果 EndTime 正好是整点，则实际的统计时间段还要再往后延长 1 小时。假设 StartTime 表示的时间是 15:07，EndTime 表示的时间是 16:00，那么实际的统计时间段是 [15:00,17:00)。 
             EndTime ( Long ): 是  表示统计时间段的结束时间，格式是 Unix 时间戳，精度是秒。 
             Domain ( String ): 是  表示一个加速域名，用于对用户请求进行过滤。 
                   当子用户调用该 API 时，请留意以下说明： 
                   - 子用户只能指定一个其有权限访问的加速域名。子用户可以调用 ListCdnDomains 获取其有权限访问的加速域名。 
             UaType ( String ): 否  表示 User-Agent 字符串中的一个对象类型。当 Item 是 ua 时，该参数必须指定，作为一个补充分组条件。当 Item 不是 ua 时，该参数无效。 
                   该参数有以下取值： 
                   - browser：表示 User-Agent 字符串中的浏览器类型。 
                   - system：表示 User-Agent 字符串中的操作系统类型。 
                   - equipment：表示 User-Agent 字符串中客户端设备的类型。 
             Area ( String ): 否  表示一个地域类型。该参数仅当 Item 是 region 时有效，作为一个补充分组条件，用于获取客户端 IP 地址数量的地区分布。该参数有以下取值： 
                   - Global：表示全球国家和地区。 
                   - China：表示中国省级行政区。 
                   * 如果您不指定 Metric，Area 可以不被指定。 
                   	* 如果不指定 Area，该 API 将返回按国家、地区、中国省级行政区域分布的独立客户端 IP 地址数量。 
                   * 如果您指定了 Metric，Area 必须指定。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Item ( String ): region 
        Metric ( String ): traffic 
        RankingDataList ( Array of RankingDataList ):  
        UaType ( String ): system 
       "字段"： RankingDataList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        ItemKey ( String ): GS 
        ItemKeyCN ( String ): 甘肃 
        Value ( Double ): 777 
    """,
    "describe_origin_status_code_ranking": r""" 
    Args: 
        body: A JSON structure
             Item ( String ): 是  表示一个分组条件。当前，该参数值只能是 domain，表示按 Domain 对 Metric 数据进行汇总。 
             Metric ( String ): 是  对于 CDN 收到的源站响应，该参数表示以下某个类别的状态码数量： 
                   - status_2xx：表示 2xx 状态码数量。 
                   - status_3xx：表示 3xx 状态码数量。 
                   - status_4xx：表示 4xx 状态码数量。 
                   - status_5xx：表示 5xx 状态码数量。 
             StartTime ( Long ): 是  表示统计时间段的开始时间，格式是 Unix 时间戳，精度是秒。StartTime 必须早于或者等于 EndTime。同时，StartTime 和 EndTime 所表示的统计时间段不能超过 31 天。 
             EndTime ( Long ): 是  表示统计时间段的结束时间，格式是 Unix 时间戳，精度是秒。 
             Interval ( String ): 否  表示一个时间粒度。该 API 基于 Interval 将 StartTime 和 EndTime 所表示的统计时间段拆分成一系列的时间区间，然后对每个时间区间统计 Metric 的数据。 
                   关于 Interval 参数是如何用来拆分统计时间段，参考 统计时间段说明。 
                   该参数有以下取值： 
                   - 1min：表示时间粒度是 1 分钟。 
                   - 5min：表示时间粒度是 5 分钟。 
                   您可以指定的时间粒度受 StartTime 和 EndTime 所表示的时间范围的影响。 
                   - 如果时间范围 <= 1 天，您可以指定的时间粒度有 1min、5min。 
                   - 如果 1 天 < 时间范围 <= 31 天，您可以指定的时间粒度只能是 5min。 
                   该参数的默认值是 5min。如果默认值不匹配时间范围，API 请求会失败。 
             Project ( String ): 否  表示一个项目。 
                   * 如果您指定了 Domain，该 API 对所有您指定的加速域名统计 Metric 数据。 
                   * 如果您指定了 Project ，但未指定 Domain，该 API 对您指定的项目统计 Metric 数据。参见 项目数据是如何统计的。 
                   * 如果您既未指定 Project ，也未指定 Domain，该 API 对所有加速域名统计 Metric 数据。 
             Domain ( String ): 否  表示一个或多个加速域名，用于对用户请求进行过滤。该 API 对您指定的每个加速域名统计 Metric 数据。您最多可以指定 50 个加速域名。多个加速域名之间使用逗号（,）分隔。如果不指定 Domain，表示不使用该参数对请求进行过滤。 
                   如果您指定了 Project，您指定的加速域名必须是属于该 Project 的。 
                   当子用户调用该 API 时，请留意以下说明： 
                   - 子用户只能指定其有权限访问的加速域名。子用户可以调用 ListCdnDomains 获取其有权限访问的加速域名。 
                   - 如果不指定该参数，表示所有该子用户有权限访问的那些加速域名。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Item ( String ): domain 
        Metric ( String ): status_4xx 
        TopDataDetails ( Array of TopDataDetails ):  
       "字段"： TopDataDetails
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        ItemKey ( String ): www.example.com 
        Status2xx ( Double ): 45678 
        Status2xxRatio ( Double ): 0.47 
        Status3xx ( Double ): 0 
        Status3xxRatio ( Double ): 0 
        Status4xx ( Double ): 3 
        Status4xxRatio ( Double ): 0.0001 
        Status5xx ( Double ): 0 
        Status5xxRatio ( Double ): 0 
    """,
    "describe_user_data": r""" 
    Args: 
        body: A JSON structure
             StartTime ( Long ): 是  表示统计时间段的开始时间，格式是 Unix 时间戳，精度是秒。StartTime 必须早于或者等于 EndTime。同时，StartTime 与 EndTime 所表示的统计时间段不能超过 31 天。 
             EndTime ( Long ): 是  表示统计时间段的结束时间，格式是 Unix 时间戳，精度是秒。 
             Interval ( String ): 是  表示一个时间粒度。该 API 基于 Interval 将 StartTime 和 EndTime 所表示的统计时间段拆分成一系列的时间区间，然后对每个时间区间统计独立客户端 IP 地址的数量。 
                   关于 Interva参数是如何用来拆分统计时间段，参考 统计时间段说明。  
                   该参数有以下取值： 
                   - hour：表示时间粒度是 1 小时。 
                   - day：表示时间粒度是 1 天。 
             Domain ( String ): 是  表示一个加速域名，用于对用户请求进行过滤。 
                   当子账号调用该 API 时，请留意以下说明： 
                   - 子账号可以指定的加速域名是该子账号有权限访问的那些加速域名。子账号可以调用 ListCdnDomains 获取其有权限访问的加速域名。 
             IpVersion ( String ): 否  表示请求使用的一个网络层协议，用于对用户请求进行过滤。该参数的可用值如下： 
                   - IPv4：表示 IPv4 协议。 
                   - IPv6：表示 IPv6 协议。 
                   如果不指定 IpVersion，表示不使用该参数对请求进行过滤。 
             Location ( String ): 否  表示一个国家或地区的代码，用于对用户请求进行过滤。CDN 对来自这些国家和地区的用户请求统计客户端 IP 地址的数量。 
                   * 如果您指定了 Location，就不能指定 Province，反之亦然。 
                   * 如果您不指定 Location，表示不使用该参数对请求进行过滤。 
                   您可以调用 DescribeCdnRegionAndIsp 获取代码与国家和地区的对应表。 
             Province ( String ): 否  表示一个中国省级行政区的代码，用于对用户请求进行过滤。CDN 对来自这些省级行政区的用户请求统计客户端 IP 地址的数量。 
                   如果您不指定 Province，表示不使用该参数对请求进行过滤。 
                   您可以调用 DescribeCdnRegionAndIsp 获取代码与中国省级行政区的对应表。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        MetricDataList ( Array of MetricDataList ):  
       "字段"： MetricDataList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        TimeStamp ( Long ): 1710950400 
        Value ( Double ): 42 
    """,
    "describe_origin_summary": r""" 
    Args: 
        body: A JSON structure
             Metric ( String ): 是  表示一个指标。该参数有以下取值： 
                   - traffic：表示源站向内容分发网络传输的数据量，单位是 bytes。 
                   - bandwidth：表示基于源站向内容分发网络传输的数据量而计算的带宽峰值，单位是 bps。 
                   - requests：表示回源请求的数量。 
                   - qps：表示回源请求的 QPS 峰值。 
                   - status_all：在内容分发网络收到的源站响应中，该参数表示以下类别的状态码数量： 
                   	- 所有状态码的数量。 
                   	- 所有 2xx 状态码的数量。 
                   	- 所有 3xx 状态码的数量。 
                   	- 所有 4xx 状态码的数量。 
                   	- 所有 5xx 状态码的数量。 
                   	- 每个状态码的数量。 
                   - status_2xx：表示所有 2xx 状态码的数量以及该类别下每个状态码的数量。 
                   - status_3xx：表示所有 3xx 状态码的数量以及该类别下每个状态码的数量。 
                   - status_4xx：表示所有 4xx 状态码的数量以及该类别下每个状态码的数量。 
                   - status_5xx：表示所有 5xx 状态码的数量以及该类别下每个状态码的数量。 
                   关于每个指标的详情以及统计方式，参见 指标的定义以及统计方式。 
             StartTime ( Long ): 是  表示统计时间段的开始时间，格式是 Unix 时间戳，精度是秒。StartTime 必须早于或者等于 EndTime。同时，StartTime 与 EndTime 所表示的统计时间段不能超过 31 天。 
             EndTime ( Long ): 是  表示统计时间段的结束时间，格式是 Unix 时间戳，精度是秒。 
             Interval ( String ): 否  表示一个时间粒度。该 API 基于 Interval 将 StartTime 和 EndTime 所表示的统计时间段拆分成一系列的时间区间，然后对每个时间区间统计 Metric 数据。 
                   关于 Interval 参数是如何用来拆分统计时间段，参考 统计时间段说明。 
                   该参数有以下取值： 
                   - 1min：表示时间粒度是 1 分钟。 
                   - 5min：表示时间粒度是 5 分钟。 
                   您可以指定的时间粒度受 StartTime 和 EndTime 所表示的时间范围的影响。 
                   - 如果时间范围 <= 1 天，您可以指定的时间粒度有 1min、5min。 
                   - 如果 1 天 < 时间范围 <= 31 天，您可以指定的时间粒度只能是 5min。 
                   该参数的默认值是 5min。如果默认值不匹配时间范围，API 请求会失败。 
             Project ( String ): 否  表示一个项目。 
                   * 如果您指定了 Domain，该 API 对所有您指定的加速域名统计 Metric 数据。 
                   * 如果您指定了 Project ，但未指定 Domain，该 API 对您指定的项目统计 Metric 数据。参见 项目数据是如何统计的。 
                   * 如果您既未指定 Project ，也未指定 Domain，该 API 对所有加速域名统计 Metric 数据。 
             Domain ( String ): 否  表示一个或多个加速域名，用于对用户请求进行过滤。该 API 对您指定的每个加速域名统计 Metric 数据。您最多可以指定 50 个加速域名。多个加速域名之间使用逗号（,）分隔。如果不指定 Domain，表示不使用该参数对请求进行过滤。 
                   如果您指定了 Project，您指定的加速域名必须是属于该 Project 的。 
                   当子用户调用该 API 时，请留意以下说明： 
                   - 子用户只能指定其有权限访问的加速域名。子用户可以调用 ListCdnDomains 获取其有权限访问的加速域名。 
                   - 如果不指定该参数，表示所有该子用户有权限访问的那些加速域名。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        MetricDataList ( Array of MetricDataList ):  
       "字段"： MetricDataList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Metric ( String ): bandwidth 
        Value ( Double ): 3475788 
    """,
}
