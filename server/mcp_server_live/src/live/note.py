note = {
    "describe_live_stream_count_data": r""" 
    Args: 
        body: A JSON structure
             DomainList ( Array of String ): 否  直播流使用的域名列表，默认为空，表示查询所有全部域名下的峰值流数。您可以调用 ListDomainDetail 接口或在视频直播控制台的域名管理页面，查看直播流使用的域名。 
             StreamType ( Array of String ): 否  流类型，缺省情况下表示全部类型，支持的流类型取值如下。 
                   - push：推流； 
                   - relay-source：回源流； 
                   - transcode：转码流。 
             ISPList ( Array of String ): 否  提供网络接入服务的运营商标识符，缺省情况下表示所有运营商，支持的运营商如下所示。 
                   - unicom：联通； 
                   - railcom：铁通； 
                   - telecom：电信； 
                   - mobile：移动； 
                   - cernet：教育网； 
                   - tianwei：天威； 
                   - alibaba：阿里巴巴； 
                   - tencent：腾讯； 
                   - drpeng：鹏博士； 
                   - btvn：广电； 
                   - huashu：华数。 
                   - 当流类型 StreamType 为推流 push 时支持使用运营商对查询数据进行筛选。 
                   - 您也可以通过 DescribeLiveISPData 接口获取运营商对应的标识符。 
             UserRegionList ( Array of UserRegionList ): 否  客户端 IP 所属区域的列表，缺省情况下表示所有区域。 
                   当流类型 StreamType 为推流 push 时支持使用客户端 IP 所属的区域对查询数据进行筛选。 
             Aggregation ( Integer ): 否  聚合的时间粒度，单位为秒，支持的时间粒度如下所示。 
                   - 60：1 分钟； 
                   - 300：（默认值）5 分钟； 
                   - 3600：1 小时。 
             DetailField ( Array of String ): 否  数据拆分的维度，默认为空表示不按维度进行数据拆分，支持的维度如下所示。 
                   - Domain：域名； 
                   - ISP：运营商。 
             StartTime ( String ): 是  查询的开始时间，RFC3339 格式的时间戳，精度为秒。 
                   历史查询最大时间范围为 366 天，单次查询最大时间跨度与数据拆分维度和数据聚合时间粒度有关，详细如下。 
                   - 当不进行维度拆分或只使用一个维度拆分数据时： 
                   	- 数据以 60 秒聚合时，单次查询最大时间跨度为 24 小时； 
                   	- 数据以 300 秒聚合时，单次查询最大时间跨度为 31 天； 
                   	- 数据以 3600 秒聚合时，单次查询最大时间跨度为 31 天。 
                   - 当使用两个或两个以上维度拆分数据时： 
                   	- 数据以 60 秒聚合时，单次查询最大时间跨度为 3 小时； 
                   	- 数据以 300 秒聚合时，单次查询最大时间跨度为 24 小时； 
                   	- 数据以 3600 秒聚合时，单次查询最大时间跨度为 7 天。 
             EndTime ( String ): 是  查询的结束时间，RFC3339 格式的时间戳，精度为秒。 
            "字段"： UserRegionList
             Area ( String ): 否  区域信息的大区标识符，如何获取请参见查询区域标识符。 
             Country ( String ): 否  区域信息的国家标识符，如何获取请参见查询区域标识符。如果按国家筛选，需要同时传入 Area 和 Country。 
             Province ( String ): 否  区域信息的省份标识符，国外暂不支持该参数，如何获取请参见查询区域标识符。如果按省筛选，需要同时传入 Area、Country 和 Province。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        DomainList ( Array of String ): ["push.example.com","push2.example.com"] 
        StartTime ( String ): 2021-08-16T00:00:00+08:00 
        EndTime ( String ): 2021-08-16T00:01:59+08:00 
        Aggregation ( Integer ): 60 
        DetailField ( Array of String ): ["Domain"] 
        StreamType ( Array of String ): ["push"] 
        PeakCount ( Integer ): 100 
        TotalStreamDataList ( Array of TotalStreamDataList ): - 
        StreamDetailDataList ( Array of StreamDetailDataList ): - 
        ISPList ( Array of String ): ["telecom"] 
        UserRegionList ( Array of UserRegionList ): - 
       "字段"： TotalStreamDataList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        TimeStamp ( String ): 2021-08-16T00:00:00+08:00 
        PeakCount ( Integer ): 100 
       "字段"： StreamDetailDataList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Domain ( String ): push.example.com 
        TotalStreamDataList ( Array of TotalStreamDataList ): - 
       "字段"： UserRegionList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Area ( String ): CN 
        Country ( String ): CN 
        Province ( String ): beijing 
    """,
    "describe_live_batch_stream_traffic_data": r""" 
    Args: 
        body: A JSON structure
             DomainList ( Array of String ): 否  域名列表，默认为空，表示查询所有域名下的流量数据。您可以调用 ListDomainDetail 接口或在视频直播控制台的域名管理页面，获取待查询的域名。 
             ProtocolList ( Array of String ): 否  推拉流协议，缺省情况下表示所有协议类型，支持的协议如下所示。 
                   - HTTP-FLV：基于 HTTP 协议的推拉流协议，使用 FLV 格式传输视频格式。 
                   - HTTP-HLS：基于 HTTP 协议的推拉流协议，使用 TS 格式传输视频格式。 
                   - RTMP：Real Time Message Protocol，实时信息传输协议。 
                   - RTM：Real Time Media，超低延时直播协议。 
                   - SRT：Secure Reliable Transport，安全可靠传输协议。 
                   - QUIC：Quick UDP Internet Connections，一种基于 UDP 的全新的低延时互联网传输协议。 
                   - 如果查询推拉流协议为 QUIC，不能同时查询其他协议。 
                   - 缺省情况下，查询的总流量数据为实际产生的上下行流量。 
                   - 如果传入单个协议进行查询，并对各协议的流量求和，结果将大于实际总流量。 
             ISPList ( Array of String ): 否  提供网络接入服务的运营商标识符，缺省情况下表示所有运营商，支持的运营商如下所示。 
                   - unicom：联通； 
                   - railcom：铁通； 
                   - telecom：电信； 
                   - mobile：移动； 
                   - cernet：教育网； 
                   - tianwei：天威； 
                   - alibaba：阿里巴巴； 
                   - tencent：腾讯； 
                   - drpeng：鹏博士； 
                   - btvn：广电； 
                   - huashu：华数。 
                   您也可以通过 DescribeLiveISPData 接口获取运营商对应的标识符。 
             RegionList ( Array of RegionList ): 否  CDN 节点 IP 所属区域的列表，缺省情况下表示所有区域。 
                   参数 RegionList和UserRegionList 不支持同时传入。 
             UserRegionList ( Array of RegionList ): 否  客户端 IP 所属区域的列表，缺省情况下表示所有区域。 
                   参数 RegionList和UserRegionList 不支持同时传入。 
             StartTime ( String ): 是  查询的开始时间，RFC3339 格式的时间戳，精度为秒。 
                   单次查询最大时间跨度为 24 小时，查询历史数据的时间范围为 366 天。 
             EndTime ( String ): 是  查询的结束时间，RFC3339 格式的时间戳，精度为秒。 
             PageNum ( Integer ): 否  查询数据的页码，默认值为 1，表示查询第一页的数据。 
             PageSize ( Integer ): 否  每页显示的数据条数，默认值为 1000，取值范围为 [100,1000]。 
            "字段"： RegionList
             Area ( String ): 否  区域信息中的大区标识符，如何获取请参见查询区域标识符。 
             Country ( String ): 否  区域信息中的国家标识符，如何获取请参见查询区域标识符。如果按国家筛选，需要同时传入 Area 和 Country。 
             Province ( String ): 否  区域信息中的省份标识符，国外暂不支持该参数，如何获取请参见查询区域标识符。如果按省筛选，需要同时传入 Area、Country 和 Province。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        DomainList ( Array of String ): ["push.example.com", "push2.example.com"] 
        ProtocolList ( Array of String ): ["RTMP"] 
        ISPList ( Array of String ): ["telecom"] 
        RegionList ( Array of RegionList ): - 
        UserRegionList ( Array of RegionListResponse ): - 
        StartTime ( String ): 2022-11-10T00:00:00+08:00 
        EndTime ( String ): 2022-11-11T00:00:00+08:00 
        TotalUpTraffic ( Float ): 40 
        TotalDownTraffic ( Float ): 40 
        StreamInfoList ( Array of StreamInfoList ): - 
        Pagination ( Object of Pagination ): - 
       "字段"： RegionList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Area ( String ): CN 
        Country ( String ): CN 
        Province ( String ): beijing 
       "字段"： RegionListResponse
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Area ( String ): CN 
        Country ( String ): CN 
        Province ( String ): beijing 
       "字段"： StreamInfoList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Domain ( String ): push.example.com 
        App ( String ): live 
        Stream ( String ): example_stream 
        UpTraffic ( Float ): 20 
        DownTraffic ( Float ): 20 
       "字段"： Pagination
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        PageNum ( Integer ): 1 
        PageSize ( Integer ): 1000 
        TotalCount ( Integer ): 2 
    """,
    "describe_live_source_traffic_data": r""" 
    Args: 
        body: A JSON structure
             DomainList ( Array of String ): 否  拉流域名列表，默认为空，表示查询所有域名的回源流量带宽监控数据。您可以调用 ListDomainDetail 接口或在视频直播控制台的域名管理页面，获取待查询的拉流域名。 
                   DomainList 和 Domain 传且仅传一个。 
             Domain ( String ): 否  拉流域名，您可以调用 ListDomainDetail 接口或在视频直播控制台的域名管理页面，获取待查询的拉流域名。 
                   查询流粒度数据时，需同时指定 Domain 、App 和 Stream 来指定回源流。 
             App ( String ): 否  回源流的应用名称，查询流粒度数据时必传，且需同时传入 Domain 和 Stream。支持由大小写字母（A - Z、a - z）、数字（0 - 9）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 30 个字符。 
                   查询流粒度数据时，需同时指定 Domain 、App 和 Stream 来指定回源流。 
             Stream ( String ): 否  回源流的流名称，查询流粒度数据时必传，且需同时传入 Domain 和 App。支持由大小写字母（A - Z、a - z）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 100 个字符。 
                   查询流粒度数据时，需同时指定 Domain 、App 和 Stream 来指定回源流。 
             ISPList ( Array of String ): 否  提供网络接入服务的运营商标识符，缺省情况下表示所有运营商，支持的运营商如下所示。 
                   - unicom：联通； 
                   - railcom：铁通； 
                   - telecom：电信； 
                   - mobile：移动； 
                   - cernet：教育网； 
                   - tianwei：天威； 
                   - alibaba：阿里巴巴； 
                   - tencent：腾讯； 
                   - drpeng：鹏博士； 
                   - btvn：广电； 
                   - huashu：华数。 
                   您也可以通过 DescribeLiveISPData 接口获取运营商对应的标识符。 
             UserRegionList ( Array of UserRegionList ): 否  客户端 IP 所属区域的列表，缺省情况下表示所有区域。 
             Aggregation ( Integer ): 否  数据聚合的时间粒度，单位为秒，支持的时间粒度如下所示。 
                   - 60：1 分钟。 
                   - 300：（默认值）5 分钟。 
                   - 3600：1 小时。 
             DetailField ( Array of String ): 否  数据拆分的维度，默认为空表示不按维度进行数据拆分，支持的维度如下所示。 
                   - Domain：域名； 
                   - ISP：运营商。 
                   配置数据拆分的维度时，对应的维度参数传入多个值时才会返回按此维度拆分的数据。例如，配置按 Domain 进行数据拆分时， DomainList 传入多个 Domain 值时，才会返回按 Domain 拆分的数据。 
             StartTime ( String ): 是  查询的开始时间，RFC3339 格式的时间戳，精度为秒。 
                   历史查询最大时间范围为 366 天，单次查询最大时间跨度与数据拆分维度和数据聚合时间粒度有关，详细如下。 
                   - 当不进行维度拆分或只使用一个维度拆分数据时： 
                   	- 数据以 60 秒聚合时，单次查询最大时间跨度为 24 小时； 
                   	- 数据以 300 秒聚合时，单次查询最大时间跨度为 31 天； 
                   	- 数据以 3600 秒聚合时，单次查询最大时间跨度为 31 天。 
                   - 当使用两个或两个以上维度拆分数据时： 
                   	- 数据以 60 秒聚合时，单次查询最大时间跨度为 3 小时； 
                   	- 数据以 300 秒聚合时，单次查询最大时间跨度为 24 小时； 
                   	- 数据以 3600 秒聚合时，单次查询最大时间跨度为 7 天。 
             EndTime ( String ): 是  查询的结束时间，RFC3339 格式的时间戳，精度为秒。 
            "字段"： UserRegionList
             Area ( String ): 否  区域信息中的大区标识符，如何获取请参见查询区域标识符。 
             Country ( String ): 否  区域信息中的国家标识符，如何获取请参见查询区域标识符。如果按国家筛选，需要同时传入 Area 和 Country。 
             Province ( String ): 否  区域信息中的省份标识符，国外暂不支持该参数，如何获取请参见查询区域标识符。如果按省筛选，需要同时传入 Area、Country 和 Province。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        DomainList ( Array of String ): ["push.example.com", "push2.example.com"] 
        Domain ( String ): push.example.com 
        App ( String ): live 
        Stream ( String ): example_stream 
        ISPList ( Array of String ): ["telecom"] 
        UserRegionList ( Array of UserRegionList ): - 
        DetailField ( Array of String ): ["Domain"] 
        StartTime ( String ): 2021-04-13T00:00:00+08:00 
        EndTime ( String ): 2021-04-14T00:00:00+08:00 
        Aggregation ( Integer ): 300 
        TotalTraffic ( Float ): 20 
        PeakBandwidth ( Float ): 10 
        TrafficDataList ( Array of TrafficDataList ): - 
        TrafficDetailDataList ( Array of TrafficDetailDataList ): - 
       "字段"： UserRegionList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Area ( String ): CN 
        Country ( String ): CN 
        Province ( String ): beijing 
       "字段"： TrafficDataList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        TimeStamp ( String ): 2022-04-13T00:00:00+08:00 
        Traffic ( Float ): 20 
        Bandwidth ( Float ): 10 
       "字段"： TrafficDetailDataList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Domain ( String ): push.example.com 
        ISP ( String ): telecom 
        TotalTraffic ( Float ): 20 
        PeakBandwidth ( Float ): 10 
        TrafficDataList ( Array of TrafficDataList ): - 
    """,
    "describe_live_stream_session_data": r""" 
    Args: 
        body: A JSON structure
             DomainList ( Array of String ): 否  拉流域名列表，默认为空，表示查询所有域名的请求数和在线人数。您可以调用 ListDomainDetail 接口或在视频直播控制台的域名管理页面，获取待查询的拉流域名。 
                   DomainList 和 Domain 传且仅传一个。 
             Domain ( String ): 否  拉流域名，您可以调用 ListDomainDetail 接口或在视频直播控制台的域名管理页面，获取待查询的拉流域名。 
                   查询流粒度的请求数和在线人数数据时，需同时指定 Domain 、App 和 Stream 来指定直播流。 
             App ( String ): 否  应用名称，取值与直播流地址中的 AppName 字段取值相同。支持由大小写字母（A - Z、a - z）、数字（0 - 9）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 30 个字符。 
                   查询流粒度的请求数和在线人数数据时，需同时指定 Domain 、App 和 Stream 来指定直播流。 
             Stream ( String ): 否  流名称，取值与直播流地址中的 StreamName 字段取值相同。支持由大小写字母（A - Z、a - z）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 100 个字符。 
                   查询流粒度的请求数和在线人数数据时，需同时指定 Domain 、App 和 Stream 来指定直播流。 
             ProtocolList ( Array of String ): 否  推拉流协议，缺省情况下表示所有协议类型，支持的协议如下所示。 
                   - HTTP-FLV：基于 HTTP 协议的推拉流协议，使用 FLV 格式传输视频格式。 
                   - HTTP-HLS：基于 HTTP 协议的推拉流协议，使用 TS 格式传输视频格式。 
                   - RTMP：Real Time Message Protocol，实时信息传输协议。 
                   - RTM：Real Time Media，超低延时直播协议。 
                   - SRT：Secure Reliable Transport，安全可靠传输协议。 
                   - QUIC：Quick UDP Internet Connections，一种基于 UDP 的全新的低延时互联网传输协议。 
                   如果查询推拉流协议为 QUIC，不能同时查询其他协议。 
             ISPList ( Array of String ): 否  提供网络接入服务的运营商标识符，缺省情况下表示所有运营商，支持的运营商如下所示。 
                   - unicom：联通； 
                   - railcom：铁通； 
                   - telecom：电信； 
                   - mobile：移动； 
                   - cernet：教育网； 
                   - tianwei：天威； 
                   - alibaba：阿里巴巴； 
                   - tencent：腾讯； 
                   - drpeng：鹏博士； 
                   - btvn：广电； 
                   - huashu：华数。 
                   您也可以通过 DescribeLiveISPData 接口获取运营商对应的标识符。 
             RegionList ( Array of RegionList ): 否  CDN 节点 IP 所属区域的列表，缺省情况下表示所有区域。 
             Aggregation ( Integer ): 否  数据聚合的时间粒度，单位为秒，支持的时间粒度如下所示。 
                   - 60：1 分钟。 
                   - 300：（默认值）5 分钟。 
                   - 3600：1 小时。 
             DetailField ( Array of String ): 否  数据拆分的维度，默认为空表示不按维度进行数据拆分，支持的维度如下所示。 
                   - Domain：域名； 
                   - ISP：运营商； 
                   - Protocol：推拉流协议。 
                   配置数据拆分的维度时，对应的维度参数传入多个值时才会返回按此维度拆分的数据。例如，配置按 Domain 进行数据拆分时， DomainList 传入多个 Domain 值时，才会返回按 Domain 拆分的数据。 
             OnlineUserType ( String ): 否  在线人数统计方式，取值及含义如下所示： 
                   - Online（默认值）：以 1 分钟瞬时连接的 session 数作为 1 分钟粒度的在线人数数量； 
                   - Viewer：以 1 分钟内的 session 链接总数作为 1 分钟粒度的在线人数数量； 
                   - ClientIP：以 1 分钟内的进行拉流请求的客户端 IP 总数作为 1 分钟粒度的在线人数数量。 
             StartTime ( String ): 是  查询的开始时间，RFC3339 格式的时间戳，精度为秒。 
                   历史查询最大时间范围为 366 天，单次查询最大时间跨度与数据拆分维度和数据聚合时间粒度有关，详细如下。 
                   - 当不进行维度拆分或只使用一个维度拆分数据时： 
                   	- 数据以 60 秒聚合时，单次查询最大时间跨度为 24 小时； 
                   	- 数据以 300 秒聚合时，单次查询最大时间跨度为 31 天； 
                   	- 数据以 3600 秒聚合时，单次查询最大时间跨度为 31 天。 
                   - 当使用两个或两个以上维度拆分数据时： 
                   	- 数据以 60 秒聚合时，单次查询最大时间跨度为 3 小时； 
                   	- 数据以 300 秒聚合时，单次查询最大时间跨度为 24 小时； 
                   	- 数据以 3600 秒聚合时，单次查询最大时间跨度为 7 天。 
             EndTime ( String ): 是  查询的结束时间，RFC3339 格式的时间戳，精度为秒。 
            "字段"： RegionList
             Area ( String ): 否  区域信息中的大区标识符，如何获取请参见查询区域标识符。 
             Country ( String ): 否  区域信息中的国家标识符，如何获取请参见查询区域标识符。如果按国家筛选，需要同时传入 Area 和 Country。 
             Province ( String ): 否  区域信息中的省份标识符，国外暂不支持该参数，如何获取请参见查询区域标识符。如果按省筛选，需要同时传入 Area、Country 和 Province。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        DomainList ( Array of String ): ["pull.example.com"] 
        Domain ( String ): pull.example.com 
        App ( String ): live 
        Stream ( String ): example_stream 
        ProtocolList ( Array of String ): ["HTTP-FLV", "RTMP"] 
        ISPList ( Array of String ): ["telecom"] 
        RegionList ( Array of RegionList ): - 
        StartTime ( String ): 2021-04-13T00:00:00+08:00 
        EndTime ( String ): 2021-04-14T00:00:00+08:00 
        Aggregation ( Integer ): 300 
        DetailField ( Array of String ): ["Domain"] 
        TotalRequest ( Integer ): 20 
        PeakOnlineUser ( Integer ): 20 
        SessionDataList ( Array of SessionDataList ): - 
        SessionDetailDataList ( Array of SessionDetailDataList ): - 
       "字段"： RegionList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Area ( String ): CN 
        Country ( String ): CN 
        Province ( String ): beijing 
       "字段"： SessionDataList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        TimeStamp ( String ): 2022-04-13T00:00:00+08:00 
        Request ( Integer ): 10 
        OnlineUser ( Integer ): 20 
       "字段"： SessionDetailDataList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Domain ( String ): pull.example.com 
        Protocol ( String ): HTTP-FLV 
        ISP ( String ): telecom 
        TotalRequest ( Integer ): 20 
        PeakOnlineUser ( Integer ): 20 
        SessionDataList ( Array of SessionDataList ): - 
    """,
    "describe_live_play_status_code_data": r""" 
    Args: 
        body: A JSON structure
             DomainList ( Array of String ): 否  域名列表，默认为空时表示查询所有域名下产生的请求状态码占比数据。您可以调用 ListDomainDetail 接口或在视频直播控制台的域名管理页面，获取待查询请求状态码占比数据的域名。 
             ISPList ( Array of String ): 否  提供网络接入服务的运营商标识符，缺省情况下表示所有运营商，支持的运营商如下所示。 
                   - unicom：联通； 
                   - railcom：铁通； 
                   - telecom：电信； 
                   - mobile：移动； 
                   - cernet：教育网； 
                   - tianwei：天威； 
                   - alibaba：阿里巴巴； 
                   - tencent：腾讯； 
                   - drpeng：鹏博士； 
                   - btvn：广电； 
                   - huashu：华数。 
                   您也可以通过 DescribeLiveISPData 接口获取运营商对应的标识符。 
             RegionList ( Array of Region ): 否  CDN 节点 IP 所属区域的列表，缺省情况下表示所有区域。 
                   参数 RegionList和UserRegionList 不支持同时传入。 
             UserRegionList ( Array of Region ): 否  客户端 IP 所属区域的列表，缺省情况下表示所有区域。 
                   参数 RegionList和UserRegionList 不支持同时传入。 
             StartTime ( String ): 是  查询的开始时间，RFC3339 格式的时间戳，精度为秒。 
             EndTime ( String ): 是  查询的结束时间，RFC3339 格式的时间戳，精度为秒。 
             Aggregation ( Integer ): 否  聚合的时间粒度，单位为秒，支持的时间粒度如下所示。 
                   - 60：（默认值）1 分钟。时间粒度为 1 分钟时，单次查询最大时间跨度为 24 小时，历史查询时间范围为 366 天； 
                   - 300：5 分钟。时间粒度为 5 分钟时，单次查询最大时间跨度为 31 天，历史查询时间范围为 366 天； 
                   - 3600：1 小时。时间粒度为 1 小时时，单次查询最大时间跨度为 93 天，历史查询时间范围为 366 天。 
             DetailField ( Array of String ): 否  数据拆分的维度，默认为空表示不按维度进行数据拆分，支持的维度如下所示。 
                   - Domain：域名； 
                   - ISP：运营商。 
                   配置数据拆分的维度时，对应的维度参数传入多个值时才会返回按此维度拆分的数据。例如，配置按 Domain 进行数据拆分时， DomainList 传入多个 Domain 值时，才会返回按 Domain 拆分的数据。 
             Type ( String ): 否  请求类型，取值及含义如下所示。 
                   - Access：（默认值）推流请求和拉流请求； 
                   - Source：回源请求。 
            "字段"： Region
             Area ( String ): 否  区域信息中的大区标识符，如何获取请参见查询区域标识符。 
             Country ( String ): 否  区域信息中的国家标识符，如何获取请参见查询区域标识符。如果按国家筛选，需要同时传入 Area 和 Country。 
             Province ( String ): 否  区域信息中的省份标识符，国外暂不支持该参数，如何获取请参见查询区域标识符。如果按省筛选，需要同时传入 Area、Country 和 Province。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        DomainList ( Array of String ): ["push.example.com", "pull.example.com"] 
        ISPList ( Array of String ): ["telecom"] 
        RegionList ( Array of Region ): - 
        UserRegionList ( Array of Region ): - 
        StartTime ( String ): 2021-04-13T00:00:00+08:00 
        EndTime ( String ): 2021-04-14T00:00:00+08:00 
        Aggregation ( Integer ): 300 
        DetailField ( Array of String ): ["Domain"] 
        StatusSummaryDataList ( Array of StatusSummaryData ): - 
        StatusDataList ( Array of StatusData ): - 
        StatusDetailDataList ( Array of StatusDetailData ): - 
        Type ( String ): Access 
       "字段"： Region
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Area ( String ): CN 
        Country ( String ): CN 
        Province ( String ): beijing 
       "字段"： StatusSummaryData
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        StatusCode ( Integer ): 400 
        Value ( Integer ): 67 
        Percent ( Float ): 67 
       "字段"： StatusData
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        TimeStamp ( String ): 2021-08-16T00:00:00+08:00 
        StatusSummaryDataList ( Array of StatusSummaryData ): - 
       "字段"： StatusDetailData
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Domain ( String ): pull.example.com 
        ISP ( String ): unicom 
        StatusDataList ( Array of StatusData ): - 
    """,
    "describe_live_push_stream_metrics": r""" 
    Args: 
        body: A JSON structure
             Domain ( String ): 是  推流域名，您可以调用 ListDomainDetail 接口或在视频直播控制台的域名管理页面，查看直播流使用的推流域名。 
             App ( String ): 是  应用名称，取值与直播流地址中 AppName 字段取值相同。支持由大小写字母（A - Z、a - z）、数字（0 - 9）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 30 个字符。 
             Stream ( String ): 是  流名称，取值与直播流地址中 StreamName 字段取值相同。支持由大小写字母（A - Z、a - z）、数字（0 - 9）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 100 个字符。 
             StartTime ( String ): 是  查询的开始时间，RFC3339 格式的时间戳，精度为秒。 
                   单次查询最大时间跨度为 1 天，历史查询最大时间范围为 366 天。 
             EndTime ( String ): 是  查询的结束时间，RFC3339 格式的时间戳，精度为秒。 
             Aggregation ( Integer ): 否  数据聚合的时间粒度，单位为秒，支持的时间粒度如下所示。 
                   - 5：5 秒； 
                   - 30：（默认值）30 秒。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Domain ( String ): example.com 
        App ( String ): example_app 
        Stream ( String ): example_stream 
        StartTime ( String ): 2021-08-16T00:00:00+08:00 
        EndTime ( String ): 2021-08-16T00:00:00+08:00 
        Aggregation ( Integer ): 5 
        MetricList ( Array of MetricList ): - 
       "字段"： MetricList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        TimeStamp ( String ): 2022-04-13T00:00:00+08:00 
        Bitrate ( Float ): 20 
        Framerate ( Float ): 20 
        AudioFramerate ( Float ): 20 
        AudioBitrate ( Float ): 20 
        AudioPts ( Double ): 9558439 
        VideoPts ( Double ): 9558430 
        PtsDelta ( Float ): 9 
        AudioFrameGap ( Float ): 20 
        VideoFrameGap ( Float ): 20 
    """,
    "describe_live_source_stream_metrics": r""" 
    Args: 
        body: A JSON structure
             Domain ( String ): 是  拉流域名，您可以调用 ListDomainDetail 接口或在视频直播控制台的域名管理页面，查看回源流使用的拉流域名。 
             App ( String ): 是  应用名称，取值与直播流地址中 AppName 字段取值相同。支持由大小写字母（A - Z、a - z）、数字（0 - 9）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 30 个字符。 
             Stream ( String ): 是  流名称，取值与直播流地址中 StreamName 字段取值相同。支持由大小写字母（A - Z、a - z）、数字（0 - 9）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 100 个字符。 
             StartTime ( String ): 是  查询的开始时间，RFC3339 格式的时间戳，精度为秒。 
                   单次查询最大时间跨度为 1 天，历史查询最大时间范围为 366 天。 
             EndTime ( String ): 是  查询的结束时间，RFC3339 格式的时间戳，精度为秒。 
             Aggregation ( Integer ): 否  数据聚合的时间粒度，单位为秒，当前接口默认且仅支持按 30 秒进行数据聚合。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Domain ( String ): pull.example.com 
        App ( String ): live 
        Stream ( String ): example_stream 
        StartTime ( String ): 2021-08-16T00:00:00+08:00 
        EndTime ( String ): 2021-08-16T00:01:59+08:00 
        Aggregation ( Integer ): 30 
        MetricList ( Array of MetricList ): - 
       "字段"： MetricList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        TimeStamp ( String ): 2022-04-13T00:00:00+08:00 
        Bitrate ( Float ): 20 
        Framerate ( Float ): 20 
        AudioFramerate ( Float ): 20 
        AudioBitrate ( Float ): 20 
        AudioPts ( Double ): 1651831909 
        VideoPts ( Double ): 1651831910 
        PtsDelta ( Float ): 1 
        AudioFrameGap ( Float ): 20 
        VideoFrameGap ( Float ): 20 
    """,
    "describe_live_batch_stream_transcode_data": r""" 
    Args: 
        body: A JSON structure
             DomainList ( Array of String ): 否  域名列表，默认为空表示全部域名。您可以调用 ListDomainDetail 接口或在视频直播控制台的域名管理页面，获取直播流使用的域名信息。 
             StartTime ( String ): 是  查询的开始时间，RFC3339 格式的时间戳，精度为秒。 
                   查询历史数据的时间范围为 366 天。 
             EndTime ( String ): 是  查询的结束时间，RFC3339 格式的时间戳，精度为秒。 
             PageSize ( Integer ): 否  每页显示的数据条数，默认值为 1000，取值范围为 [100,1000]。 
             PageNum ( Integer ): 否  查询数据的页码，默认值为 1，表示查询第一页的数据。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        DomainList ( Array of String ): ["pull.example.com", "pull2.example.com"] 
        StartTime ( String ): 2022-11-10T00:00:00+08:00 
        EndTime ( String ): 2022-11-11T00:00:00+08:00 
        TotalDuration ( Float ): 40.1 
        StreamInfoList ( Array of StreamInfoList ): - 
        Pagination ( Object of Pagination ): - 
       "字段"： StreamInfoList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Domain ( String ): pull.example.com 
        App ( String ): live 
        Stream ( String ): example_stream 
        Resolution ( String ): 720P 
        Duration ( Float ): 20.1 
        VCodec ( String ): Normal_H264 
        Coderate ( Integer ): 2000 
       "字段"： Pagination
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        PageNum ( Integer ): 1 
        PageSize ( Integer ): 100 
        TotalCount ( Integer ): 2 
    """,
    "describe_live_batch_push_stream_metrics": r""" 
    Args: 
        body: A JSON structure
             Domain ( String ): 是  推流域名，您可以调用 ListDomainDetail 接口或在视频直播控制台的域名管理页面，查看直播流使用的推流域名。 
             App ( String ): 否  应用名称，取值与直播流地址中的 AppName 字段取值相同，查询流粒度数据时必传，且需同时传入 Stream。支持由大小写字母（A - Z、a - z）、数字（0 - 9）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 30 个字符。 
                   查询流粒度的监控数据时，需同时指定 App 和 Stream 来指定直播流。 
             Stream ( String ): 否  流名称，预置与直播流地址中的 StreamName 字段取值相同，查询流粒度数据时必传，且需同时传入 Stream。支持由大小写字母（A - Z、a - z）、数字（0 - 9）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 100 个字符。 
                   查询流粒度的监控数据时，需同时指定 App 和 Stream 来指定直播流。 
             AggType ( String ): 否  数据聚合时间粒度内，动态指标的聚合算法，取值及含义如下所示。 
                   - max：（默认值）计算聚合时间粒度内的最大值； 
                   - avg：计算聚合时间粒度内的平均值。 
             StartTime ( String ): 是  查询的开始时间，RFC3339 格式的时间戳，精度为秒。 
                   单次查询最大时间跨度为 1 天，历史查询最大时间范围为 366 天。 
             EndTime ( String ): 是  查询的结束时间，RFC3339 格式的时间戳，精度为秒。 
             Aggregation ( Integer ): 否  数据聚合的时间粒度，单位为秒，支持的时间粒度如下所示。 
                   - 5：5 秒； 
                   - 30：30 秒； 
                   - 60：（默认值）1 分钟。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Domain ( String ): push.example.com 
        App ( String ): live 
        Stream ( String ): example_stream 
        AggType ( String ): max 
        StartTime ( String ): 2021-08-16T00:00:00+08:00 
        EndTime ( String ): 2021-08-16T00:01:59+08:00 
        Aggregation ( Integer ): 5 
        StreamMetricList ( Array of StreamMetricList ): - 
       "字段"： StreamMetricList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Domain ( String ): push.example.com 
        App ( String ): live 
        Stream ( String ): example_stream 
        SessionID ( String ): 1961227fe2ab4da7a3f28 
        MetricList ( Array of MetricList ): - 
       "字段"： MetricList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        TimeStamp ( String ): 2022-04-13T00:00:00+08:00 
        Bitrate ( Float ): 20 
        Framerate ( Float ): 20 
        AudioFramerate ( Float ): 20 
        AudioBitrate ( Float ): 20 
        AudioPts ( Double ): 9558439 
        VideoPts ( Double ): 9558438 
        PtsDelta ( Float ): 1 
        AudioFrameGap ( Float ): 20 
        VideoFrameGap ( Float ): 20 
        StreamBeginTime ( Long ): 1723726121000 
        FirstFrameTime ( Integer ): 10 
        ClientIp ( String ): 127.0.0.1 
        ServerIp ( String ): 127.0.0.1 
        Resolution ( String ): 1280x720 
        ACodec ( String ): AAC 
        VCodec ( String ): H264 
    """,
    "describe_live_batch_source_stream_metrics": r""" 
    Args: 
        body: A JSON structure
             Domain ( String ): 是  拉流域名，您可以调用 ListDomainDetail 接口或在视频直播控制台的域名管理页面，查看回源流使用的拉流域名。 
             App ( String ): 否  应用名称，取值与直播流地址中的 AppName 字段取值相同，查询流粒度数据时必传，且需同时传入 Stream。支持由大小写字母（A - Z、a - z）、数字（0 - 9）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 30 个字符。 
                   查询流粒度的监控数据时，需同时指定 App 和 Stream 来指定回源流。 
             Stream ( String ): 否  流名称，预置与直播流地址中的 StreamName 字段取值相同，查询流粒度数据时必传，且需同时传入 Stream。支持由大小写字母（A - Z、a - z）、数字（0 - 9）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 100 个字符。 
                   查询流粒度的监控数据时，需同时指定 App 和 Stream 来指定回源流。 
             StartTime ( String ): 是  查询的开始时间，RFC3339 格式的时间戳，精度为秒。 
                   单次查询最大时间跨度为 1 天，历史查询最大时间范围为 366 天。 
             EndTime ( String ): 是  查询的结束时间，RFC3339 格式的时间戳，精度为秒。 
             Aggregation ( Integer ): 否  数据聚合的时间粒度，单位为秒，支持的时间粒度如下所示。 
                   - 30：30 秒； 
                   - 60：（默认值）1 分钟。 
             AggType ( String ): 否  数据聚合时间粒度内，动态指标的聚合算法，取值及含义如下所示。 
                   - max：（默认值）计算聚合时间粒度内的最大值； 
                   - avg：计算聚合时间粒度内的平均值。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Domain ( String ): pull.example.com 
        App ( String ): live 
        Stream ( String ): example_stream 
        StartTime ( String ): 2021-04-13T00:00:00+08:00 
        EndTime ( String ): 2021-04-14T00:00:00+08:00 
        Aggregation ( Integer ): 30 
        StreamMetricList ( Array of StreamMetricList ): - 
        AggType ( String ): max 
       "字段"： StreamMetricList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Domain ( String ): pull.example.com 
        App ( String ): live 
        Stream ( String ): example_stream 
        MetricList ( Array of MetricList ): - 
       "字段"： MetricList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        TimeStamp ( String ): 2022-04-13T00:00:00+08:00 
        Bitrate ( Float ): 20 
        Framerate ( Float ): 20 
        AudioFramerate ( Float ): 20 
        AudioBitrate ( Float ): 20 
        AudioPts ( Double ): 1651831909 
        VideoPts ( Double ): 1651831910 
        PtsDelta ( Float ): 1 
        AudioFrameGap ( Float ): 20 
        VideoFrameGap ( Float ): 20 
    """,
    "describe_ip_info": r""" 
    Args: 
        body: A JSON structure
             Ips ( Array of String ): 是  待查询的 IP 地址列表。支持 IPv4 和 IPv6 地址，一次最多查询 50 个 IP 地址。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        List ( Array of LiveIpInfo ): - 
       "字段"： LiveIpInfo
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Ip ( String ): 186.199.*.1 
        LiveCdnIp ( Boolean ): false 
        Location ( String ): 中国 
        Province ( String ): 河北 
        City ( String ): 廊坊 
        Isp ( String ): telecom 
    """,
    "generate_play_url": r""" 
    Args: 
        body: A JSON structure
             Domain ( String ): 是  拉流域名。您可以调用 ListDomainDetail 接口或在视频直播控制台的域名管理页面，查看直播流使用的拉流域名。 
             App ( String ): 是  应用名称，取值与直播流地址中 AppName 字段取值相同。支持由大小写字母（A - Z、a - z）、数字（0 - 9）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 30 个字符。 
             Stream ( String ): 是  流名称，取值与直播流地址中 StreamName 字段取值相同。支持由大小写字母（A - Z、a - z）、数字（0 - 9）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 100 个字符。 
             Type ( String ): 否  CDN 类型，默认值为 fcdn，支持如下取值。 
                   - fcdn：火山引擎流媒体直播 CDN； 
                   - 3rd：第三方 CDN。 
             Suffix ( String ): 否  转码流后缀，默认为空，表示生成源流的拉流地址。配置不为空时表示生成转码流的拉流地址，可通过调用 ListVhostTransCodePreset 接口查询对应流的转码流后缀。 
             ValidDuration ( Integer ): 否  拉流地址的有效时长，单位为秒，超过有效时长后需要重新生成。取值范围为正整数，缺省值为 604800，即 7 天。 
                   如果同时设置 ValidDuration 和 ExpiredTime，以 ExpiredTime 的时间为准。 
             ExpiredTime ( String ): 否  拉流地址的过期时间，RFC3339 格式的 UTC 时间，精度为秒，过期后需要重新生成。缺省情况下表示当前时间往后的 7 天。 
                   如果同时设置 ValidDuration 和 ExpiredTime，以 ExpiredTime 的时间为准。 
             StreamType ( String ): 是  生成地址类型，取值如下： 
                   - source：生成源流地址。 
                   - transcode: 生成转码流地址。 
                   - abr: 生成 ABR 地址。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        URLList ( Array of URLList ): - 
       "字段"： URLList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        URL ( String ): http://pull.example.com/live/example_stream.sdp 
        Type ( String ): pull 
        CDN ( String ): fcdn 
        Protocol ( String ): hls 
        SubStreamURL ( Array of SubStreamURL ): - 
       "字段"： SubStreamURL
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Suffix ( String ): _ld 
        Tag ( String ): LL-HLS 
    """,
    "generate_push_url": r""" 
    Args: 
        body: A JSON structure
             Vhost ( String ): 是  域名空间，即推流域名所属的域名空间。您可以调用 ListDomainDetail 接口或在视频直播控制台的域名管理页面，查看推流域名所属的域名空间。 
             Domain ( String ): 否  推流域名，默认为空，表示生成域名空间下所有推流域名的推流地址。您可以调用 ListDomainDetail 接口或在视频直播控制台的域名管理页面，查看需要的推流域名。 
             App ( String ): 是  应用名称，取值与直播流地址中 AppName 字段取值相同。支持由大小写字母（A - Z、a - z）、数字（0 - 9）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 30 个字符。 
             Stream ( String ): 是  流名称，取值与直播流地址中 StreamName 字段取值相同。支持由大小写字母（A - Z、a - z）、数字（0 - 9）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 100 个字符。 
             ValidDuration ( Integer ): 否  推流地址的有效时长，单位为秒，超过有效时长后需要重新生成。取值范围为正整数，默认值为 604800，即 7 天。 
                   如果同时设置 ValidDuration 和 ExpiredTime，以 ExpiredTime 的时间为准。 
             ExpiredTime ( String ): 否  推流地址的过期时间，RFC3339 格式的时间字符串，精度为秒，过期后需要重新生成。缺省情况下表示当前时间往后的 7 天。 
                   如果同时设置 ValidDuration 和 ExpiredTime，以 ExpiredTime 的时间为准。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        PushURLList ( Array of String ): ["rtmp://push.example.com/live/example_stream"] 
        PushURLListDetail ( Array of PushURLListDetail ): - 
        TsOverSrtURLList ( Array of String ): ["srt://push.example.com:9000?streamid=#!::h=push.example.com,r=live/example_stream,m=publish"] 
        RtmpOverSrtURLList ( Array of String ): ["rtmp://push.example.com:1999/live/example_stream"] 
        RtmURLList ( Array of String ): ["http://push.example.com/live/example_stream.sdp"] 
        WebTransportURLList ( Array of String ): ["https://push.example.com/live/example_stream"] 
       "字段"： PushURLListDetail
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        URL ( String ): rtmp://live.push.example.com/live/example_stream 
        DomainApp ( String ): rtmp://push.example.com/live/ 
        StreamSign ( String ): example_stream 
    """,
    "describe_domain": r""" 
    Args: 
        body: A JSON structure
             DomainList ( Array of String ): 是  待查询域名信息的域名列表。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        DomainList ( Array of DomainList ): - 
       "字段"： DomainList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Vhost ( String ): push.example.com 
        Domain ( String ): push.example.com 
        Status ( Integer ): 0 
        Type ( String ): push 
        Region ( String ): cn 
        CNAME ( String ): push.example.com.bytefcdn.com 
        CnameCheck ( Integer ): 0 
        DomainCheck ( Integer ): 0 
        ICPCheck ( Integer ): 0 
        CreateTime ( String ): 2006-01-02T15:04:05Z 
        CertDomain ( String ): *.example.com 
        HTTP2 ( Boolean ): false 
        ChainID ( String ): 21614 
        PushDomain ( String ): push.example.com 
    """,
    "list_domain_detail": r""" 
    Args: 
        body: A JSON structure
             PageNum ( Integer ): 是  查询数据的页码，取值为 1 时表示查询第一页的数据，取值范围为 [1,1000]。 
             PageSize ( Integer ): 是  每页显示的数据条数，取值为 10 时表示每页展示 10 条域名信息，取值范围为 [1, 1000]。 
             VhostList ( Array of String ): 否  域名空间列表，缺省情况下表示查询全部域名空间下的域名。 
             DomainStatusList ( Array of Integer ): 否  域名状态列表，缺省情况下表示查询全部状态的域名。支持的取值如下所示。 
                   - 0：正常； 
                   - 1：审核中； 
                   - 2：禁用，禁止使用，此时 domain 不生效； 
                   - 3：删除； 
                   - 4：审核被驳回。审核不通过，需要重新创建并审核； 
                   - 5：欠费关停； 
                   - 6：域名未备案被封禁。 
             DomainTypeList ( Array of String ): 否  域名类型列表，缺省情况下表示全部类型的域名。支持的取值如下所示。 
                   - push：推流域名； 
                   - pull-flv：拉流域名。 
             DomainRegionList ( Array of String ): 否  域名加速区域列表，缺省情况下表示查看全部。支持的取值如下所示。 
                   - cn：中国内地； 
                   - cn-global：全球加速； 
                   - cn-oversea：海外及港澳台。 
             DomainNameList ( Array of String ): 否  域名名称列表，缺省情况下表示全部。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        DomainList ( Array of DomainList ): - 
        Total ( Integer ): 2 
       "字段"： DomainList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        CNAME ( String ): push.example.com.bytefcdn.com 
        Vhost ( String ): push.example.com 
        Domain ( String ): push.example.com 
        Status ( Integer ): 0 
        Type ( String ): pull 
        Region ( String ): cn 
        CnameCheck ( Integer ): 0 
        DomainCheck ( Integer ): 0 
        ICPCheck ( Integer ): 1 
        CreateTime ( String ): 2006-01-02T15:04:05Z 
        CertDomain ( String ): *.example.com 
        HTTP2 ( Boolean ): false 
        ChainID ( String ): 21614 
        PushDomain ( String ): push.example.com 
        ProjectName ( String ): default 
        Tags ( Array of Tags ): - 
       "字段"： Tags
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Key ( String ): key1 
        Value ( String ): value1 
        Category ( String ): Custom 
    """,
    "describe_live_isp_data": r""" 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        ISPList ( Array of ISPList ): - 
       "字段"： ISPList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Code ( String ): unicom 
        Name ( String ): 联通 
    """,
    "describe_live_region_data": r""" 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Areas ( Array of Areas ): - 
       "字段"： Areas
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Code ( String ): CN 
        Name ( String ): 中国 
        Countries ( Array of Countries ): - 
       "字段"： Countries
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Code ( String ): CN 
        Name ( String ): 中国 
        Provinces ( Array of Provinces ): - 
       "字段"： Provinces
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Code ( String ): beijing 
        Name ( String ): 北京 
    """,
    "describe_live_push_stream_info_data": r""" 
    Args: 
        body: A JSON structure
             DomainList ( Array of String ): 否  直播推流使用的域名列表，缺省为空，表示当前账号下所有域名。您可以调用 ListDomainDetail 接口或在视频直播控制台的域名管理页面，查看直播推流使用的域名。 
             App ( String ): 否  应用名称，取值与直播流地址中 AppName 字段取值相同，默认为空，表示查询所有应用名称。支持由大小写字母（A - Z、a - z）、数字（0 - 9）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 30 个字符。 
             Stream ( String ): 否  流名称，取值与直播流地址中 StreamName 字段取值相同，默认为空表示查询所有流名称。支持由大小写字母（A - Z、a - z）、数字（0 - 9）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 100 个字符。 
             StartTime ( String ): 是  查询的开始时间，RFC3339 格式的时间戳，精度为秒。 
                   支持查询最近 93 天以内的推流数据。 
             EndTime ( String ): 是  查询的结束时间，RFC3339 格式的时间戳，精度为秒。 
                   支持查询最近 93 天以内的推流数据。 
             PageNum ( Integer ): 否  查询数据的页码，默认为 1，表示查询第一页的数据，取值范围为正整数。 
             PageSize ( Integer ): 否  每页显示的数据条数，默认为 20，取值范围为 [1,1000]。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        DomainList ( Array of String ): ["push.example.com"] 
        App ( String ): live 
        Stream ( String ): example_stream 
        StartTime ( String ): 2021-04-13T00:00:00+08:00 
        EndTime ( String ): 2021-04-14T00:00:00+08:00 
        PushStreamInfoDataList ( Array of PushStreamInfoDataList ): - 
        Pagination ( Object of Pagination ): - 
       "字段"： PushStreamInfoDataList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        App ( String ): example_app 
        Stream ( String ): example_stream 
        StartTime ( String ): 2021-04-13T00:00:00+08:00 
        EndTime ( String ): 2021-04-14T00:00:00+08:00 
        Duration ( Integer ): 100 
        IP ( String ): 127.0.0.1 
        StreamBreakReason ( String ): 对端主动断开链接 
       "字段"： Pagination
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        PageCur ( Integer ): 1 
        PageSize ( Integer ): 100 
        TotalCount ( Integer ): 1000 
    """,
    "describe_live_transcode_info_data": r""" 
    Args: 
        body: A JSON structure
             DomainList ( Array of String ): 否  域名列表，默认为空，表示查询您视频直播产品下所有域名的转码用量数据。您可以调用 ListDomainDetail 接口或在视频直播控制台的域名管理页面，获取待查询的域名。 
             App ( String ): 否  应用名称，取值与直播流地址中 AppName 字段取值相同。支持由大小写字母（A - Z、a - z）、数字（0 - 9）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 30 个字符。 
                   查询流粒度数据时，需同时传入 App 和 Stream。 
             Stream ( String ): 否  流名称，取值与直播流地址中 StreamName 字段取值相同。支持由大小写字母（A - Z、a - z）、数字（0 - 9）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 100 个字符。 
                   查询流粒度数据时，需同时传入 App 和 Stream。 
             StartTime ( String ): 是  查询的开始时间，RFC3339 格式的时间戳，精度为秒。 
                   历史查询最大时间范围为 366 天。 
             EndTime ( String ): 是  查询的结束时间，RFC3339 格式的时间戳，精度为秒。 
             TranscodeType ( Array of String ): 否  视频编码格式，默认为空表示不指定视频编码格式，支持的取值和含义如下所示。 
                   - Normal_H264：H.264 标准转码； 
                   - Normal_H265：H.265 标准转码； 
                   - Normal_H266：H.266 标准转码； 
                   - ByteHD_H264：H.264 极智超清； 
                   - ByteHD_H265：H.265 极智超清； 
                   - ByteHD_H266：H.266 极智超清； 
                   - ByteQE：画质增强； 
                   - Audio：纯音频流。 
             Resolution ( Array of String ): 否  转码分辨率档位，默认为空表示不指定转码分辨率档位。以 720P 为例，表示转码配置的长边 x 短边计算而出的面积大于 480P（640 × 480）且小于等于 720P 档位（1280 x 720）。支持的取值和含义如下所示。 
                   - 480P：640 × 480； 
                   - 720P：1280 × 720； 
                   - 1080P：1920 × 1088； 
                   - 2K：2560 × 1440； 
                   - 4K：4096 × 2160； 
                   - 8K：> 4096 x 2160； 
                   - 0P：纯音频转码。 
             PageNum ( Integer ): 否  查询数据的页码，默认为 1，表示查询第一页的数据。 
             PageSize ( Integer ): 否  每页显示的数据条数。默认为 20，最大值为 100000。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        DomainList ( Array of String ): ["push.example.com","push2.example.com"] 
        App ( String ): live 
        Stream ( String ): example_stream 
        Resolution ( Array of String ): ["720P","1080P"] 
        StartTime ( String ): 2021-04-13T00:00:00+08:00 
        EndTime ( String ): 2021-04-14T00:00:00+08:00 
        TranscodeInfoDataList ( Array of TranscodeInfoDataList ): - 
        Pagination ( Object of Pagination ): - 
        TranscodeType ( Array of String ): ["Normal_H264","ByteHD_H265"] 
       "字段"： TranscodeInfoDataList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        TaskID ( String ): assf1**adasdn 
        Stream ( String ): test_stream 
        TranscodeSuffix ( String ): hd 
        TranscodeType ( String ): Normal_H264 
        Resolution ( String ): 720P 
        StartTime ( String ): 2022-03-07T00:00:00+08:00 
        EndTime ( String ): 2022-03-08T00:00:00+08:00 
        Duration ( Float ): 1.4475713543666666 
       "字段"： Pagination
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        PageCur ( Integer ): 1 
        PageSize ( Integer ): 100 
        TotalCount ( Integer ): 1000 
    """,
    "describe_live_batch_stream_session_data": r""" 
    Args: 
        body: A JSON structure
             DomainList ( Array of String ): 否  拉流域名列表，默认为空，表示查询所有域名的请求数和在线人数。您可以调用 ListDomainDetail 接口或在视频直播控制台的域名管理页面，获取待查询的拉流域名。 
             ProtocolList ( Array of String ): 否  推拉流协议，缺省情况下表示所有协议类型，支持的协议如下所示。 
                   - HTTP-FLV：基于 HTTP 协议的推拉流协议，使用 FLV 格式传输视频格式。 
                   - HTTP-HLS：基于 HTTP 协议的推拉流协议，使用 TS 格式传输视频格式。 
                   - RTMP：Real Time Message Protocol，实时信息传输协议。 
                   - RTM：Real Time Media，超低延时直播协议。 
                   - SRT：Secure Reliable Transport，安全可靠传输协议。 
                   - QUIC：Quick UDP Internet Connections，一种基于 UDP 的全新的低延时互联网传输协议。 
                   - 如果查询推拉流协议为 QUIC，不能同时查询其他协议。 
                   - 缺省情况下，查询的总流量数据为实际产生的上下行流量。 
                   - 如果传入单个协议进行查询，并对各协议的流量求和，结果将大于实际总流量。 
             ISPList ( Array of String ): 否  提供网络接入服务的运营商标识符，缺省情况下表示所有运营商，支持的运营商如下所示。 
                   - unicom：联通； 
                   - railcom：铁通； 
                   - telecom：电信； 
                   - mobile：移动； 
                   - cernet：教育网； 
                   - tianwei：天威； 
                   - alibaba：阿里巴巴； 
                   - tencent：腾讯； 
                   - drpeng：鹏博士； 
                   - btvn：广电； 
                   - huashu：华数。 
                   您也可以通过 DescribeLiveISPData 接口获取运营商对应的标识符。 
             RegionList ( Array of RegionList ): 否  CDN 节点 IP 所属区域的列表，缺省情况下表示所有区域。 
             StartTime ( String ): 是  查询的开始时间，RFC3339 格式的时间戳，精度为秒。 
                   单次查询最大时间跨度为 24 小时，查询历史数据的时间范围为 366 天。 
             EndTime ( String ): 是  查询的结束时间，RFC3339 格式的时间戳，精度为秒。 
             PageNum ( Integer ): 否  查询数据的页码，默认值为 1，表示查询第一页的数据。 
             PageSize ( Integer ): 否  每页显示的数据条数，默认值为 1000，取值范围为 [100,1000]。 
             OnlineUserType ( String ): 否  在线人数统计方式，取值及含义如下所示： 
                   - Online：以 1 分钟瞬时连接的 session 数作为 1 分钟粒度的在线人数数量； 
                   - Viewer（默认值）：以 1 分钟内的 session 链接总数作为 1 分钟粒度的在线人数数量。 
            "字段"： RegionList
             Area ( String ): 否  区域信息中的大区标识符，如何获取请参见查询区域标识符。 
             Country ( String ): 否  区域信息中的国家标识符，如何获取请参见查询区域标识符。如果按国家筛选，需要同时传入 Area 和 Country。 
             Province ( String ): 否  区域信息中的省份标识符，国外暂不支持该参数，如何获取请参见查询区域标识符。如果按省筛选，需要同时传入 Area、Country 和 Province。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        DomainList ( Array of String ): ["example.com", "example2.com"] 
        ProtocolList ( Array of String ): ["RTMP"] 
        ISPList ( Array of String ): ["telecom"] 
        RegionList ( Array of RegionList ): - 
        StartTime ( String ): 2022-11-10T00:00:00+08:00 
        EndTime ( String ): 2022-11-11T00:00:00+08:00 
        TotalRequest ( Integer ): 20 
        PeakOnlineUser ( Integer ): 20 
        StreamInfoList ( Array of StreamInfoList ): - 
        Pagination ( Object of Pagination ): - 
       "字段"： RegionList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Area ( String ): CN 
        Country ( String ): CN 
        Province ( String ): beijing 
       "字段"： StreamInfoList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Domain ( String ): example.com 
        App ( String ): example_app 
        Stream ( String ): example_stream 
        TotalRequest ( Integer ): 20 
        PeakOnlineUser ( Integer ): 20 
       "字段"： Pagination
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        PageNum ( Integer ): 1 
        PageSize ( Integer ): 1000 
        TotalCount ( Integer ): 2 
    """,
    "describe_live_top_play_data": r""" 
    Args: 
        body: A JSON structure
             StartTime ( String ): 是  查询的开始时间，RFC3339 格式的时间戳，精度为秒。 
                   - 单次查询最大时间跨度为 31 天。 
                   - 历史查询时间范围是 366 天。 
                   - 带宽和流量数据按照整小时进行聚合。在此建议您，查询开始时间和查询结束时间应涵盖您所要查询的时间段的整点小时。 
             EndTime ( String ): 是  查询的结束时间，RFC3339 格式的时间戳，精度为秒。 
             QueryType ( String ): 否  查询类型，取值及含义如下所示。  
                   - Domain ：查询 TOPN 域名的的流量带宽信息。 
                   - Stream（默认值）：查询 TOPN 直播流的流量带宽信息。 
             VhostList ( Array of String ): 否  域名空间列表，默认为空，表示所有域名空间。您可以调用 ListDomainDetail 接口或在视频直播控制台的域名管理页面，获取待查询的域名空间信息。 
             DomainList ( Array of String ): 否  域名列表，默认为空，表示所有域名。您可以调用 ListDomainDetail 接口或在视频直播控制台的域名管理页面，获取待查询的域名信息。 
             SortBy ( String ): 否  TOPN 结果的排序指标，取值及含义如下所示。  
                   - PeakBandwidth（默认值）：以峰值带宽值降序展示查询结果。  
                   - AvgBandwidth：以平均带宽值降序展示查询结果。 
                   - TotalTraffic：以流量加值降序展示查询结果。 
             PageSize ( String ): 否  每页显示的数据条数，默认值为 10，取值范围为  [1,1000]。 
             PageNum ( String ): 否  查询数据的页码，默认值为 1，表示查询第一页的数据。  
                   PageSize 为 10，PageNum 为 1 时，表示查询 TOP 10 的数据。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        StartTime ( String ): 2024-11-16T00:00:00+08:00 
        EndTime ( String ): 2024-11-20T00:00:00+08:00 
        QueryType ( String ): Stream 
        VhostList ( Array of String ): ["push.example.com"] 
        DomainList ( Array of String ): ["push.example.com"] 
        SortBy ( String ): PeakBandwidth 
        DataItemList ( Array of DataItemList ): - 
        Pagination ( Object of Pagination ): - 
       "字段"： DataItemList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Domain ( String ): push.example.com 
        App ( String ): live 
        Stream ( String ): example_stream 
        PeakBandwidth ( Float ): 1000 
        AvgBandwidth ( Float ): 1000 
        TotalTraffic ( Float ): 20000 
       "字段"： Pagination
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        PageSize ( String ): 10 
        PageNum ( String ): 1 
        TotalCount ( String ): 20 
    """,
    "describe_live_edge_stat_data": r""" 
    Args: 
        body: A JSON structure
             DomainList ( Array of String ): 否  域名列表，默认为空，表示您添加到视频直播中的所有域名。您可以调用 ListDomainDetail 接口或在视频直播控制台的域名管理页面，获取待查询的域名。 
             AppList ( Array of String ): 否  直播流地址中的 AppName 字段列表，默认为空表示所有 AppName。每个 AppName 支持由大小写字母（A - Z、a - z）、数字（0 - 9）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 30 个字符。 
             StreamList ( Array of String ): 否  直播流地址中的 StreamName 字段列表，默认为空表示所有 StreamName。每个 StreamName 支持由大小写字母（A - Z、a - z）、数字（0 - 9）、下划线（_）、短横线（-）和句点（.）组成，长度为 1 到 100 个字符。 
             ProtocolList ( Array of String ): 否  推拉流协议，缺省情况下表示所有协议类型，支持的协议如下所示。 
                   - HTTP-FLV：基于 HTTP 协议的推拉流协议，使用 FLV 格式传输视频格式。 
                   - HTTP-HLS：基于 HTTP 协议的推拉流协议，使用 TS 格式传输视频格式。 
                   - RTMP：Real Time Message Protocol，实时信息传输协议。 
                   - RTM：Real Time Media，超低延时直播协议。 
                   - SRT：Secure Reliable Transport，安全可靠传输协议。 
                   - QUIC：Quick UDP Internet Connections，一种基于 UDP 的全新的低延时互联网传输协议。 
                   如果查询推拉流协议为 QUIC，不能同时查询其他协议。 
             ISPList ( Array of String ): 否  提供网络接入服务的运营商标识符，缺省情况下表示所有运营商，支持的运营商如下所示。 
                   - unicom：联通； 
                   - railcom：铁通； 
                   - telecom：电信； 
                   - mobile：移动； 
                   - cernet：教育网； 
                   - tianwei：天威； 
                   - alibaba：阿里巴巴； 
                   - tencent：腾讯； 
                   - drpeng：鹏博士； 
                   - btvn：广电； 
                   - huashu：华数。 
                   您也可以通过 DescribeLiveISPData 接口获取运营商对应的标识符。 
             RegionList ( Array of Region ): 否  CDN 节点 IP 所属区域的列表，缺省情况下表示所有区域。 
                   参数 RegionList和UserRegionList 不支持同时传入。 
             UserRegionList ( Array of Region ): 否  客户端 IP 所属区域的列表，缺省情况下表示所有区域。 
                   参数 RegionList和UserRegionList 不支持同时传入。 
             DetailField ( Array of String ): 否  数据拆分的维度，缺省情况下不进行数据拆分，支持的维度如下所示。 
                   - Domain：域名； 
                   - Protocol：推拉流协议； 
                   - ISP：运营商； 
                   - Area：CDN 节点 IP 所属大区。 
                   - Country：CDN 节点 IP 所属国家。 
                   - Province：CDN 节点 IP 所属省份。 
                   - UserArea：客户端 IP 所属大区。 
                   - UserCountry：客户端 IP 所属国家。 
                   - UserProvince：客户端 IP 所属省份。 
                   中国（Country 或 UserCountry 为 CN）以外区域无 Province 字段，如果按 Province 或 UserProvince 字段拆分数据时，默认只返回 Country 为 CN 时的数据。 
             Aggregation ( Integer ): 否  数据聚合的时间粒度，单位为秒，支持以下取值。 
                   - 60：1 分钟。 
                   - 300：（默认值）5 分钟。 
                   - 3600：1 小时。 
             StartTime ( String ): 是  查询的开始时间，RFC3339 格式的时间戳，精度为秒。 
                   历史查询最大时间范围为 366 天，单次查询最大时间跨度与数据拆分维度和数据聚合时间粒度有关，详细如下。 
                   - 当不进行维度拆分或只使用一个维度拆分数据时： 
                   	- 数据以 60 秒聚合时，单次查询最大时间跨度为 24 小时； 
                   	- 数据以 300 秒聚合时，单次查询最大时间跨度为 31 天； 
                   	- 数据以 3600 秒聚合时，单次查询最大时间跨度为 31 天。 
                   - 当使用两个或两个以上维度拆分数据时： 
                   	- 数据以 60 秒聚合时，单次查询最大时间跨度为 3 小时； 
                   	- 数据以 300 秒聚合时，单次查询最大时间跨度为 24 小时； 
                   	- 数据以 3600 秒聚合时，单次查询最大时间跨度为 7 天。 
             EndTime ( String ): 是  查询的结束时间，RFC3339 格式的时间戳，精度为秒。 
            "字段"： Region
             Area ( String ): 否  区域信息中的大区标识符，如何获取请参见查询区域标识符。 
             Country ( String ): 否  区域信息中的国家标识符，如何获取请参见查询区域标识符。如果按国家筛选，需要同时传入 Area 和 Country。 
             Province ( String ): 否  区域信息中的省份标识符，国外暂不支持该参数，如何获取请参见查询区域标识符。如果按省筛选，需要同时传入 Area、Country 和 Province。 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        DomainList ( Array of String ): ["push.example.com","pull.example.com"] 
        AppList ( Array of String ): ["live","livevod"] 
        StreamList ( Array of String ): ["stream001","stream002"] 
        ProtocolList ( Array of String ): ["HTTP-FLV", "RTMP"] 
        ISPList ( Array of String ): ["unicom",telecom"] 
        RegionList ( Array of Region ): - 
        UserRegionList ( Array of Region ): - 
        DetailField ( Array of String ): [Domain] 
        Aggregation ( Integer ): 300 
        StartTime ( String ): 2024-12-12T00:00:00+08:00 
        EndTime ( String ): 2024-12-12T01:00:00+08:00 
        PeakUpBandwidth ( Float ): 10 
        PeakDownBandwidth ( Float ): 10 
        TotalUpTraffic ( Float ): 20 
        TotalDownTraffic ( Float ): 20 
        TotalRequest ( Float ): 5 
        EdgeStatDataList ( Array of EdgeStatDataList ): - 
        EdgeStatDetailDataList ( Array of EdgeStatDetailDataList ): - 
       "字段"： Region
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Area ( String ): CN 
        Country ( String ): CN 
        Province ( String ): beijing 
       "字段"： EdgeStatDataList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        TimeStamp ( String ): 2024-12-12T00:00:00+08:00 
        UpTraffic ( Float ): 20 
        DownTraffic ( Float ): 20 
        UpBandwidth ( Float ): 10 
        DownBandwidth ( Float ): 10 
        Request ( Float ): 5 
       "字段"： EdgeStatDetailDataList
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        Domain ( String ): push。example.com 
        Protocol ( String ): HTTP-FLV 
        ISP ( String ): telecom 
        Area ( String ): CN 
        Country ( String ): CN 
        Province ( String ): beijing 
        UserArea ( String ): CN 
        UserCountry ( String ): CN 
        UserProvince ( String ): beijing 
        PeakUpBandwidth ( Float ): 10 
        PeakDownBandwidth ( Float ): 10 
        TotalUpTraffic ( Float ): 20 
        TotalDownTraffic ( Float ): 20 
        TotalRequest ( Float ): 5 
        EdgeStatDataList ( Array of EdgeStatDataList ): - 
    """,
}
