note = {
    "get_domain_config": r""" 
   Args: 
       params: A JSON structure
            DomainName ( String ): 是  域名，您可以通过调用 GetServiceDomains 获取当前服务下所有域名。 
            ServiceId ( String ): 是  服务 ID。 
                  - 您可以在veImageX 控制台 服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
    """,
    "get_image_audit_tasks": r""" 
   Args: 
       params: A JSON structure
            Region ( String ): 否  任务地区。仅支持默认取值 cn，表示国内。 
            Type ( String ): 否  审核场景，缺省情况下查询全部场景的任务。取值如下所示： 
                  - UrlFile：上传 txt 审核文件处理场景 
                  - Url：上传审核图片 URL 处理场景 
                  - Upload：图片上传场景 
            AuditAbility ( String ): 否  审核能力，缺省情况下查询全部审核类型的任务。取值如下所示： 
                  - 0：基础审核能力 
                  - 1：智能审核能力 
            Status ( String ): 否  审核状态，缺省情况下查询全部状态的任务。取值如下所示： 
                  - Running：审核中 
                  - Suspend：已暂停 
                  - Done：已完成 
                  - Failed：审核失败 
                  - Cancel：已取消 
            TaskType ( String ): 是  审核任务类型，当前仅支持取值为 audit。 
            Limit ( String ): 否  分页条数。取值范围为 (0,100]，默认值为 100。 
            Offset ( String ): 否  分页偏移量，默认为 0。取值为 1 时，表示跳过第一条数据，从第二条数据取值。 
       body: A JSON structure
            Name ( String ): 是  任务名称 
            Desc ( String ): 否  任务描述 
            Type ( Integer ): 是  任务类型。取值1表示在线提交URL，取值2表示在线提交URI，取值3表示在线访问触发，取值4表示SDK URL触发 
            ServiceId ( String ): 是  服务ID 
            SampleRate ( Float ): 否  采样率。取值范围(0,1] 
            Tpl ( String ): 否  模板 
            Domain ( Array of String ): 否  域名列表 
            ResUri ( String ): 否  URL/URI zip包的TOS URI。在线提交类任务必填，上传至ServiceId对应的存储下 
            EvalPerStage ( Boolean ): 否  是否模拟模板每阶段输出。仅当Type=2时有效 
    """,
    "get_image_audit_result": r""" 
   Args: 
       params: A JSON structure
            TaskId ( String ): 否  任务 ID，您可通过调用 查询所有审核任务 获取所需的任务 ID。 
            Type ( String ): 否  审核场景，缺省情况下查询全部场景的任务。取值如下所示： 
                  - UrlFile：上传 txt 审核文件处理场景 
                  - Url：上传审核图片 URL 处理场景 
                  - Upload：图片上传场景 
            Problem ( String ): 否  问题类型，取值根据审核类型的不同其取值不同。缺省情况下返回全部类型任务。 
                  - 基础安全审核 
                  	- govern：涉政		 
                  	- porn ：涉黄		 
                  	- illegal：违法违规	 
                  	- terror：涉暴 
                  - 智能安全审核 
                  	- 图像风险识别 
                  		- porn ：涉黄，主要适用于通用色情、色情动作、性行为、性暗示、性分泌物、色情动漫、色情裸露等涉黄场景的风险识别	 
                  		- sensitive1 ：涉敏1，具体指涉及暴恐风险		 
                  		- sensitive2：涉敏2，具体值涉及政治内容风险		 
                  		- forbidden：违禁，主要适用于打架斗殴、爆炸、劣迹艺人等场景的风险识别 
                  		- uncomfortable：引人不适，主要适用于恶心、恐怖、尸体、血腥等引人不适场景的风险识别		 
                  		- qrcode：二维码，主要适用于识别常见二维码（QQ、微信、其他二维码等） 
                  		- badpicture：不良画面，主要适用于自我伤害、丧葬、不当车播、吸烟/纹身/竖中指等不良社会风气的风险识别		 
                  		- sexy：性感低俗，主要适用于舌吻、穿衣性行为、擦边裸露等多种性感低俗场景的风险识别 
                  		- age：年龄，主要适用于图中人物对应的年龄段识别		 
                  		- underage：未成年相关，主要适用于儿童色情、儿童邪典等风险识别	 
                  		- quality：图片质量，主要适用于图片模糊、纯色边框、纯色屏等风险识别 
                  	- 图文风险识别 
                  		- ad：广告，综合图像及文字内容智能识别广告 
                  		- defraud：诈骗，综合图像及文字内容智能识别诈骗 
                  		- charillegal：文字违规，图片上存在涉黄、涉敏、违禁等违规文字 
            ImageType ( String ): 否  图片类型，缺省情况下返回全部类型任务。取值如下所示： 
                  - problem：问题图片 
                  - frozen：冻结图片 
                  - fail：审核失败图片 
            AuditSuggestion ( String ): 否  审核建议，缺省情况下返回全部任务。取值如下所示： 
                  - nopass：建议不通过 
                  - recheck：建议复审 
            Limit ( String ): 否  分页条数。取值范围为 (0,100]，默认值为 10。 
            Marker ( String ): 否  上一次查询返回的位置标记，作为本次列举的起点信息。默认值为 0。 
    """,
    "describe_image_x_domain_bandwidth_data": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。为空时表示不筛选，支持查询多个服务，使用逗号分隔不同的服务。 
                  - 您可以在 veImageX 控制台服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考 GetAllImageServices。 
            DomainNames ( String ): 否  域名。为空时表示不筛选，支持查询多个域名，不同的域名使用逗号分隔。 
                  您可以通过调用 GetServiceDomains 获取服务下所有域名信息。 
            BillingRegion ( String ): 否  过滤计费区域。不传表示不过滤，传入多个用英文逗号分隔。支持取值如下： 
                  - CHN：中国内地 
                  - AP1：亚太一区 
                  - AP2：亚太二区 
                  - AP3：亚太三区 
                  - EU：欧洲 
                  - ME：中东和非洲 
                  - SA：南美 
                  - NA：北美 
                  - OTHER：其他 
            GroupBy ( String ): 否  需要分组查询的参数。不传表示不拆分维度，传入多个用英文逗号分隔。支持取值如下： 
                  - ServiceId：服务 ID 
                  - DomainName ：域名 
            StartTime ( String ): 是  取数据起始时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近一年历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2010-11-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( Integer ): 否  查询数据的时间粒度。单位为秒。缺省时查询 StartTime 和 EndTime 时间段全部数据，此时单次查询最大时间跨度为 93 天。支持取值如下： 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_domain_traffic_data": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。为空时表示不筛选，支持查询多个服务，使用逗号分隔不同的服务。 
                  - 您可以在 veImageX 控制台服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考 GetAllImageServices。 
            DomainNames ( String ): 否  域名。为空时表示不筛选，支持查询多个域名，不同的域名使用逗号分隔。 
                  您可以通过调用 GetServiceDomains 获取服务下所有域名信息。 
            BillingRegion ( String ): 否  过滤计费区域。不传表示不过滤。传入多个用英文逗号分隔。支持取值如下： 
                  - CHN：中国内地 
                  - AP1：亚太一区 
                  - AP2：亚太二区 
                  - AP3：亚太三区 
                  - EU：欧洲 
                  - ME：中东和非洲 
                  - SA：南美 
                  - NA：北美 
                  - OTHER：其他 
            GroupBy ( String ): 否  需要分组查询的参数。不传表示不拆分维度，传入多个用英文逗号分隔。支持取值如下： 
                  - ServiceId：服务 ID 
                  - DomainName ：域名 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近一年历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2010-11-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒。缺省时查询 StartTime 和 EndTime 时间段全部数据，此时单次查询最大时间跨度为 93 天。支持取值如下： 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_bucket_usage": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。为空时表示不筛选，支持查询多个服务，使用逗号分隔不同的服务。 
                  - 您可以在 veImageX 控制台服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考 GetAllImageServices。 
            BucketNames ( String ): 否  Bucket 名称。支持同时查询多个 BucketName，不同的 BucketNmae 使用逗号分隔。 
                  您可以通过调用 GetAllImageServices 获取所需的 Bucket 名称。 
            GroupBy ( String ): 否  需要分组查询的参数，多个数据用逗号分隔。支持取值如下： 
                  - ServiceId：服务 ID 
                  - BucketName：Bucket 名称 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm。例如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近一年历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2010-11-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm。例如2019-06-02T00:00:00+08:00。 
    """,
    "describe_image_x_request_cnt_usage": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。为空时表示不筛选，支持查询多个服务，使用英文逗号分隔不同的服务。 
                  - 您可以在 veImageX 控制台服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考 GetAllImageServices。 
            AdvFeats ( String ): 否  组件名称。为空时表示不筛选，支持查询多个AdvFeat，不同的AdvFeat使用英文逗号分隔。 
                  您可通过调用 GetImageAddOnConf 查看Key返回值。 
            Templates ( String ): 否  模版。为空时表示不筛选，支持查询多个模板，不同的模板使用英文逗号分隔。 
                  您可通过调用 GetAllImageTemplates 获取服务下全部模版信息。 
            GroupBy ( String ): 否  维度拆分的维度值。不传表示不拆分维度，只能传入单个参数。支持取值如下： 
                  - ServiceId 
                  - AdvFeat 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近一年历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2010-11-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒。缺省时查询 StartTime 和 EndTime 时间段全部数据，此时单次查询最大时间跨度为 93 天。支持取值如下： 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_base_op_usage": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。为空时表示不筛选，支持查询多个服务，使用逗号分隔不同的服务。 
                  - 您可以在 veImageX 控制台服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考 GetAllImageServices。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近一年历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2010-11-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒。缺省时查询 StartTime 和 EndTime 时间段全部数据，此时单次查询最大时间跨度为 93 天。支持取值如下： 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_compress_usage": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。为空时表示不筛选，支持查询多个服务，使用逗号分隔不同的服务。 
                  - 您可以在 veImageX 控制台服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考 GetAllImageServices。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近一年历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2010-11-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒。缺省时查询 StartTime 和 EndTime 时间段全部数据，此时单次查询最大时间跨度为 93 天。支持取值如下： 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "get_image_transcode_queues": r""" 
   Args: 
       params: A JSON structure
            Region ( String ): 否  队列所在地区。默认当前地区。ToB取值枚举：cn、va、sg。 
            SearchPtn ( String ): 否  返回队列名称或队列描述中包含该值的队列。不传返回所有队列 
            Limit ( Integer ): 是  分页条数，取值范围为(0,100]。 
            Offset ( Integer ): 否  分页偏移量，默认为 0。取值为 1 时，表示跳过第一条数据，从第二条数据取值。 
       body: A JSON structure
            TaskId ( String ): 是  待更新的任务ID 
            Status ( String ): 是  更新后的任务状态。取值枚举：Running、Suspend、Done 
    """,
    "describe_image_x_summary": r""" 
   Args: 
       params: A JSON structure
            Timestamp ( String ): 是  数据查询时间段，即Timestamp所在月份的 1 日 0 时起至传入时间Timestamp的时间范围。 
                  格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            ServiceIds ( String ): 否  限制查询的服务 ID，传入多个时用英文逗号分割。缺省情况下表示不限制服务 ID。 
                  - 您可以在 veImageX 控制台服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考 GetAllImageServices。 
    """,
    "describe_image_xcdn_top_request_data": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。传入多个时用“,”作为分割符，缺省情况下表示不限制服务 ID。 
                  - 您可以在 veImageX 控制台服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
            DomainNames ( String ): 否  域名。传入多个时用“,”作为分割符，缺省情况下表示不限制域名。您可以通过调用获取服务下全部域名获取所需的域名。 
            IPVersion ( String ): 否  网络协议。缺省情况下则表示不限制网络协议，取值如下所示： 
                  - IPv4 
                  - IPv6 
                  KeyType取值为Domain时，IPVersion的取值无效。 
            Country ( String ): 否  数据访问区域。仅在KeyType取值为Region或Isp时生效，取值如下所示： 
                  - China：中国。 
                  - Other：中国境外的区域。 
            KeyType ( String ): 是  排序指标。取值如下所示： 
                  - URL：生成的图片访问 URL 
                  - UserAgent：用户代理 
                  - Refer：请求 Refer 
                  - ClientIP：客户端 IP 
                  - Region：访问区域 
                  - Domain：域名 
                  - Isp：运营商 
            ValueType ( String ): 是  排序依据，即获取按ValueType值排序的KeyType列表。取值如下所示： 
                  - Traffic：按流量排序 
                  - RequestCnt：按请求次数排序 
                  当KeyType取值为Domain时，ValueType仅支持取值为Traffic，即按照流量排序获取域名列表。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Limit ( String ): 否  每页查询数据量，默认为0，即返回所有数据。 
            Offset ( String ): 否  分页偏移量，默认取值为0 。取值为10时，表示跳过前 10 条数据，从第 11 条数据开始取值。 
    """,
    "get_service_domains": r""" 
   Args: 
       params: A JSON structure
            ServiceId ( String ): 是  服务 ID。 
                  - 您可以在veImageX 控制台 服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
    """,
    "get_image_x_query_dims": r""" 
   Args: 
       params: A JSON structure
            Source ( String ): 是  数据来源。 
                  * upload：上传 1.0 数据。 
                  * cdn：下行网络数据。 
                  * client：客户端数据。 
                  * sensible：感知数据。 
                  * uploadv2：上传 2.0 数据。 
                  * exceed：大图监控数据。 
            Appid ( String ): 否  应用 ID。默认为空，匹配账号下所有的 App ID。 
                  您可以通过调用获取应用列表的方式获取所需的 AppID。 
            OS ( String ): 否  需要匹配的系统类型。取值如下所示： 
                  - 不传或传空字符串：Android+iOS。 
                  - iOS：iOS。 
                  - Android：Android。 
                  - WEB：web+小程序。 
                  - Web：web，仅当Source为upload或uploadv2时可传。 
                  - Imp：小程序，仅当Source为upload或uploadv2时可传。 
    """,
    "get_image_x_query_vals": r""" 
   Args: 
       params: A JSON structure
            Dim ( String ): 是  自定义维度名称。 
                  您可以通过调用获取自定义维度列表获取所需的维度名称。 
            Source ( String ): 是  数据来源。 
                  * upload：上传 1.0 数据。 
                  * cdn：下行网络数据。 
                  * client：客户端数据。 
                  * sensible：感知数据。 
                  * uploadv2：上传 2.0 数据。 
                  * exceed：大图监控数据。 
            Appid ( String ): 否  应用 ID。默认为空，匹配中账号下所有的 App ID。 
                  您可以通过调用获取应用列表的方式获取所需的 AppID。 
            OS ( String ): 否  需要匹配的系统类型。取值如下所示： 
                  - 不传或传空字符串：Android+iOS。 
                  - iOS：iOS。 
                  - Android：Android。 
                  - WEB：web+小程序。 
                  - Web：web，仅当Source为upload或uploadv2时可传。 
                  - Imp：小程序，仅当Source为upload或uploadv2时可传。 
            Keyword ( String ): 否  需要过滤的关键词（包含），不传则不过滤关键词。 
    """,
    "get_image_x_query_apps": r""" 
   Args: 
       params: A JSON structure
            Source ( String ): 否  数据来源，账号下近 60 天内有数据上报的应用 ID，缺省情况下返回账号对应的全部应用 ID。 
                  * upload：上传 1.0 数据。 
                  * cdn：下行网络数据。 
                  * client：客户端数据。 
                  * sensible：感知数据。 
                  * uploadv2：上传 2.0 数据。 
                  * exceed：大图监控数据。 
    """,
    "get_image_transcode_details": r""" 
   Args: 
       params: A JSON structure
            QueueId ( String ): 是  任务队列ID 
            Region ( String ): 否  队列所在地区。默认当前地区。ToB取值枚举：cn、va、sg。 
            StartTime ( Float ): 是  任务提交的起始Unix时间戳 
            EndTime ( Float ): 是  任务提交的截止Unix时间戳 
            Status ( String ): 否  执行状态，取值枚举：Pending、Running、Success、Fail。多个使用逗号分隔 
            SearchPtn ( String ): 否  返回图片url或uri中包含该值的任务 
            Limit ( Float ): 是  分页条数，取值范围(0, 100] 
            Offset ( Float ): 否  分页偏移 
    """,
    "describe_image_x_screenshot_usage": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  为空时表示不筛选，支持查询多个 Service，不同的 Service 使用逗号（,）分隔。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位：秒。支持300,600,1200,1800,3600,86400,604800。缺省时查询StartTime和EndTime时间段全部数据。 
    """,
    "describe_image_x_video_clip_duration_usage": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  为空时表示不筛选，支持查询多个 Service，不同的 Service 使用逗号（,）分隔。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位：秒。支持300,600,1200,1800,3600,86400,604800。缺省时查询StartTime和EndTime时间段全部数据。 
    """,
    "describe_image_x_edge_request": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。为空时表示不筛选，支持查询多个服务，使用逗号分隔不同的服务。 
                  - 您可以在 veImageX 控制台服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考 GetAllImageServices。 
            DomainNames ( String ): 否  域名。为空时表示不筛选，支持查询多个域名，不同的域名使用逗号分隔。 
                  您可以通过调用 GetServiceDomains 获取服务下所有域名信息。 
            Regions ( String ): 否  区域。传入多个时用英文逗号作为分割符，缺省情况下表示查询所有区域。取值如下所示： 
                  - 中国大陆 
                  - 亚太一区 
                  - 亚太二区 
                  - 亚太三区 
                  - 欧洲区 
                  - 北美区 
                  - 南美区 
                  - 中东区 
            UserCountry ( String ): 否  客户端国家。传入多个时用英文逗号作为分割符，缺省情况下表示不过滤。可调用获取边缘分发地区列表获取 IP 解析后的客户端国家。取值如下所示： 
                  - 海外，除中国外全部国家。 
                  - 具体国家取值，如中国、美国。 
            UserProvince ( String ): 否  客户端省份。传入多个用英文逗号分割。缺省情况下表示不过滤。可调用获取边缘分发地区列表获取 IP 解析后的客户端省份。 
            Protocols ( String ): 否  过滤网络协议。传入多个用英文逗号分割。缺省情况下表示不过滤。取值如下所示： 
                  - HTTP 
                  - HTTPS 
            Isp ( String ): 否  过滤运营商。传入多个用英文逗号分割，缺省情况下表示不过滤。取值如下所示： 
                  - 电信 
                  - 联通 
                  - 移动 
                  - 鹏博士 
                  - 教育网 
                  - 广电网 
                  - 其它 
            DataTypes ( String ): 是  状态码。传入多个时用英文逗号分隔。支持以下取值： 
                  - req_cnt：返回所有状态码数据 
                  - 2xx：返回 2xx 状态码汇总数据 
                  - 3xx：返回 3xx 状态码汇总数据 
                  - 4xx：返回 4xx 状态码汇总数据 
                  - 5xx：返回 5xx 状态码汇总数据。 
            GroupBy ( String ): 否  需要分组查询的参数。传入多个用英文逗号分割。支持以下取值： 
                  - DomainName：域名 
                  - DataType：状态码 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近 93 天的历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2011-08-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒，缺省时查询StartTime和EndTime时间段全部数据，此时单次查询最大时间跨度为 93 天。支持以下取值： 
                  - 60：单次查询最大时间跨度为 6 小时 
                  - 120：单次查询最大时间跨度为 6 小时 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
            DetailedCode ( Boolean ): 否  是否拆分状态码。取值如下所示： 
                  - true：拆分 
                  - false：（默认）不拆分 
    """,
    "describe_image_x_hit_rate_traffic_data": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  限制查询的服务 ID，传入多个时用英文逗号分割。缺省情况下表示不限制服务 ID。 
                  - 您可以在 veImageX 控制台服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考 GetAllImageServices。 
            DomainNames ( String ): 否  限制查询的域名，传入多个时用英文逗号分割。缺省情况下表示不限制域名。 
                  您可以通过调用 GetServiceDomains 获取服务下所有域名信息。 
            GroupBy ( String ): 否  需要分组查询的参数。仅支持取值DomainName。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm。例如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近 93 天的历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2011-08-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm。例如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度，单位为秒。缺省时查询StartTime和EndTime时间段全部数据，此时单次查询最大时间跨度为 93 天。支持以下取值： 
                  - 60：单次查询最大时间跨度为 6 小时 
                  - 120：单次查询最大时间跨度为 6 小时 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_hit_rate_request_data": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  限制查询的服务 ID，传入多个时用英文逗号分割。缺省情况下表示不限制服务 ID。 
                  - 您可以在 veImageX 控制台服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考 GetAllImageServices。 
            DomainNames ( String ): 否  限制查询的域名，传入多个时用英文逗号分割。缺省情况下表示不限制域名。 
                  您可以通过调用 GetServiceDomains 获取服务下所有域名信息。 
            GroupBy ( String ): 否  需要分组查询的参数。仅支持取值DomainName。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm。例如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近 93 天的历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2011-08-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm。例如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度，单位为秒。缺省时查询StartTime和EndTime时间段全部数据，此时单次查询最大时间跨度为 93 天。支持以下取值： 
                  - 60：单次查询最大时间跨度为 6 小时 
                  - 120：单次查询最大时间跨度为 6 小时 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "get_audit_entrys_count": r""" 
   Args: 
       params: A JSON structure
            TaskId ( String ): 否   
    """,
    "get_image_x_query_regions": r""" 
   Args: 
       params: A JSON structure
            Source ( String ): 是  数据来源。 
                  * upload：上传 1.0 数据。 
                  * cdn：下行网络数据。 
                  * client：客户端数据。 
                  * uploadv2：上传 2.0 数据。 
            Appid ( String ): 否  应用 ID。默认为空，匹配账号下所有的 App ID。 
                  您可以通过调用获取应用列表的方式获取所需的 Appid。 
            OS ( String ): 否  需要匹配的系统类型。取值如下所示： 
                  - 不传或传空字符串：Android+iOS。 
                  - iOS：iOS。 
                  - Android：Android。 
                  - WEB：web+小程序。 
                  - Web：web，仅当Source为upload或uploadv2时可传。 
                  - Imp：小程序，仅当Source为upload或uploadv2时可传。 
    """,
    "describe_image_x_service_quality": r""" 
   Args: 
       params: A JSON structure
            Region ( String ): 否  获取指定地区的数据。默认为空，表示获取国内数据。 
                  * cn：国内。 
                  * va：美东。 
                  * sg：新加坡。 
    """,
    "describe_image_x_edge_request_bandwidth": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。为空时表示不筛选，支持查询多个服务，使用逗号分隔不同的服务。 
                  - 您可以在 veImageX 控制台服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考 GetAllImageServices。 
            DomainNames ( String ): 否  域名。为空时表示不筛选，支持查询多个域名，不同的域名使用逗号分隔。 
                  您可以通过调用 GetServiceDomains 获取服务下所有域名信息。 
            Regions ( String ): 否  区域。传入多个时用英文逗号作为分割符，缺省情况下表示查询所有区域。取值如下所示： 
                  - 中国大陆 
                  - 亚太一区 
                  - 亚太二区 
                  - 亚太三区 
                  - 欧洲区 
                  - 北美区 
                  - 南美区 
                  - 中东区 
            UserCountry ( String ): 否  客户端国家。传入多个时用英文逗号作为分割符，缺省情况下表示不过滤。可调用获取边缘分发地区列表获取 IP 解析后的客户端国家。取值如下所示： 
                  - 海外，除中国外全部国家。 
                  - 具体国家取值，如中国、美国。 
            UserProvince ( String ): 否  客户端省份。传入多个用英文逗号分割。缺省情况下表示不过滤。可调用获取边缘分发地区列表获取 IP 解析后的客户端省份。 
            Protocols ( String ): 否  过滤网络协议。传入多个用英文逗号分割。缺省情况下表示不过滤。取值如下所示： 
                  - HTTP 
                  - HTTPS 
            Isp ( String ): 否  过滤运营商。传入多个用英文逗号分割，缺省情况下表示不过滤。取值如下所示： 
                  - 电信 
                  - 联通 
                  - 移动 
                  - 鹏博士 
                  - 教育网 
                  - 广电网 
                  - 其它 
            GroupBy ( String ): 否  分组依据，仅支持取值DomainName。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近 93 天的历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2011-08-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒，缺省时查询StartTime和EndTime时间段全部数据，此时单次查询最大时间跨度为 93 天。支持以下取值： 
                  - 60：单次查询最大时间跨度为 6 小时 
                  - 120：单次查询最大时间跨度为 6 小时 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_edge_request_traffic": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。为空时表示不筛选，支持查询多个服务，使用逗号分隔不同的服务。 
                  - 您可以在 veImageX 控制台服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考 GetAllImageServices。 
            DomainNames ( String ): 否  域名。为空时表示不筛选，支持查询多个域名，不同的域名使用逗号分隔。 
                  您可以通过调用 GetServiceDomains 获取服务下所有域名信息。 
            Regions ( String ): 否  区域。传入多个时用英文逗号作为分割符，缺省情况下表示查询所有区域。取值如下所示： 
                  - 中国大陆 
                  - 亚太一区 
                  - 亚太二区 
                  - 亚太三区 
                  - 欧洲区 
                  - 北美区 
                  - 南美区 
                  - 中东区 
            UserCountry ( String ): 否  客户端国家。传入多个时用英文逗号作为分割符，缺省情况下表示不过滤。可调用获取边缘分发地区列表获取 IP 解析后的客户端国家。取值如下所示： 
                  - 海外，除中国外全部国家。 
                  - 具体国家取值，如中国、美国。 
            UserProvince ( String ): 否  客户端省份。传入多个用英文逗号分割。缺省情况下表示不过滤。可调用获取边缘分发地区列表获取 IP 解析后的客户端省份。 
            Protocols ( String ): 否  过滤网络协议。传入多个用英文逗号分割。缺省情况下表示不过滤。取值如下所示： 
                  - HTTP 
                  - HTTPS 
            Isp ( String ): 否  过滤运营商。传入多个用英文逗号分割，缺省情况下表示不过滤。取值如下所示： 
                  - 电信 
                  - 联通 
                  - 移动 
                  - 鹏博士 
                  - 教育网 
                  - 广电网 
                  - 其它 
            GroupBy ( String ): 否  分组依据，仅支持取值DomainName。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近 93 天的历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2011-08-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒，缺省时查询StartTime和EndTime时间段全部数据，此时单次查询最大时间跨度为 93 天。支持以下取值： 
                  - 60：单次查询最大时间跨度为 6 小时 
                  - 120：单次查询最大时间跨度为 6 小时 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_edge_request_regions": r""" 
   Args: 
       params: A JSON structure
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm。例如2019-06-02T00:00:00+08:00。起始时间与结束时间间隔小于等于 90 天。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm。例如2019-06-02T00:00:00+08:00。起始时间与结束时间间隔小于等于 90 天。 
    """,
    "get_url_fetch_task": r""" 
   Args: 
       params: A JSON structure
            Id ( String ): 是  异步任务 ID，您可通过调用 FetchImageUrl接口获取该 ID。 
            ServiceId ( String ): 是  服务 ID。 
                  - 您可以在 veImageX 控制台 服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
    """,
    "get_image_erase_models": r""" 
   Args: 
       params: A JSON structure
            Type ( Integer ): 否  模型。默认取值为0。 
                  * 0：自动检测并擦除模型列表。 
                  * 1：指定区域擦除模型列表。 
    """,
    "get_dedup_task_status": r""" 
   Args: 
       params: A JSON structure
            TaskId ( String ): 是  任务 ID，您可以通过调用使用图片去重获取结果值接口获取异步去重TaskId返回值。 
    """,
    "apply_image_upload": r""" 
   Args: 
       params: A JSON structure
            ServiceId ( String ): 是  服务 ID。 
                  - 您可以在 veImageX 控制台 服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
            SessionKey ( String ): 否  一次上传会话 Key。 
                  本接口上一次请求的SessionKey，可在重试时带上，作为服务端的再次选路时的一个参考。 
            UploadNum ( Integer ): 否  上传文件的数量，将决定下发的 StoreUri 的数量，取值范围为[1,10]，默认为 1。 
            StoreKeys ( Array of String ): 否  上传文件的存储 Key。默认使用随机生成的字符串作为存储 Key。 
                  * 数组长度和UploadNum保持一致。 
                  * 存储 Key 详细命名规范请参看 veImageX 存储 Key 通用字符规则。 
            Prefix ( String ): 否  指定的上传文件路径。 
                  * 指定Prefix时，下发的存储 Key 为：Prefix/{随机Key}{FileExtension}，其中Prefix + FileExtension最大长度限制为 145 个字节。 
                  * 不支持以/开头或结尾，不支持/连续出现。 
                  仅当未指定StoreKeys时生效。 
            FileExtension ( String ): 否  文件扩展名(如：.java, .txt, .go 等)，最大长度限制为 8 个字节。 
                  仅当未指定StoreKeys时生效。 
            Overwrite ( Boolean ): 否  是否开启重名文件覆盖上传，取值如下所示： 
                  - true：开启 
                  - false：（默认）关闭 
                  在指定 Overwrite 为 true 前，请确保您指定的 ServiceId 对应服务已开启了覆盖上传能力。 
    """,
    "get_image_upload_files": r""" 
   Args: 
       params: A JSON structure
            ServiceId ( String ): 是  服务 ID。 
                  - 您可以在 veImageX 控制台 服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
            Limit ( Integer ): 否  获取文件个数，最大值为 100。 
            Marker ( Long ): 否  分页标志。 
    """,
    "get_image_migrate_tasks": r""" 
   Args: 
       params: A JSON structure
            Region ( String ): 否  任务地区（即任务目标服务的地区），缺省时将返回国内列表。取值如下所示： 
                  - cn：国内 
                  - va：美东 
                  - sg：新加坡 
            TaskId ( String ): 否  任务 ID。 
            ServiceId ( String ): 否  迁移的目标服务 ID。 
            Offset ( Long ): 否  分页偏移量。默认值为 0，表示从最新一个开始获取。 
            Limit ( Integer ): 否  分页条数。默认值为 10，最大值为 1000。 
            TaskNamePtn ( String ): 否  返回任务名称中包含该值的迁移任务信息。 
            Status ( String ): 否  任务状态，填入多个时使用半角逗号分隔。取值如下所示： 
                  - Initial：创建中 
                  - Running：运行中 
                  - Done：全部迁移完成 
                  - Partial：部分迁移完成 
                  - Failed：迁移失败 
                  - Terminated：中止 
    """,
    "get_image_service": r""" 
   Args: 
       params: A JSON structure
            ServiceId ( String ): 是  服务 ID。 
                  - 您可以在 veImageX 控制台 服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
    """,
    "get_image_style_detail": r""" 
   Args: 
       params: A JSON structure
            StyleId ( String ): 是  样式 ID。 
    """,
    "get_templates_from_bin": r""" 
   Args: 
       params: A JSON structure
            ServiceId ( String ): 是  服务 ID 
                  - 您可以在 veImageX 控制台 服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
            TemplateNamePattern ( String ): 否  仅返回模板名称包含该字符串的图片模板，不填或者为空则返回所有模板。 
            Offset ( Integer ): 否  分页偏移。默认 0。取值为1，表示跳过第一条数据，从第二条数据开始取值。 
            Limit ( Integer ): 否  分页获取条数，默认 10。 
            Asc ( String ): 否  是否按照模板创建时间升序查询，支持取值：true、false，默认为false。 
    """,
    "describe_image_x_multi_compress_usage": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。为空时表示不筛选，支持查询多个服务，不同的服务使用逗号分隔。 
                  * 您可以在veImageX 控制台 服务管理页面，在创建好的图片服务中获取服务 ID。 
                  * 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近 93 天的历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2011-08-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒，缺省时查询StartTime和EndTime时间段全部数据，此时单次查询最大时间跨度为 93 天。支持以下取值： 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "get_compress_task_info": r""" 
   Args: 
       params: A JSON structure
            TaskId ( String ): 是  异步任务 ID 
            ServiceId ( String ): 是  服务 ID。 
                  - 您可以在veImageX 控制台 服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
    """,
    "describe_image_x_billing_request_cnt_usage": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。为空时表示不筛选，支持查询多个服务，不同的服务使用逗号分隔。 
                  * 您可以在veImageX 控制台 服务管理页面，在创建好的图片服务中获取服务 ID。 
                  * 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
            AdvFeats ( String ): 否  组件名称。为空时表示不筛选，支持查询多个AdvFeat，不同的AdvFeat使用逗号分隔。 
                  您可通过调用 GetImageAddOnConf 查看Key返回值。 
            GroupBy ( String ): 是  固定值，仅支持AdvFeat即附加组件。 
            StartTime ( String ): 是  获取数据起始时间点。 
                  日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近一年历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2010-11-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。 
                  日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒。缺省时查询 StartTime 和 EndTime 时间段全部数据，此时单次查询最大时间跨度为 93 天。支持取值如下： 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "get_image_ai_generate_task": r""" 
   Args: 
       params: A JSON structure
            TaskId ( String ): 是  AIGC 任务 ID，您可通过调用创建 AIGC 异步任务获取。 
            ServiceId ( String ): 是  服务 ID。 
                  - 您可以在veImageX 控制台 服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
    """,
    "get_image_all_domain_cert": r""" 
    """,
    "get_cert_info": r""" 
   Args: 
       params: A JSON structure
            CertID ( String ): 是  证书 ID，您可以通过调用获取账号下全部证书获取账号下所有证书信息。 
    """,
    "download_cert": r""" 
   Args: 
       params: A JSON structure
            CertID ( String ): 是  证书 ID，您可以通过调用 获取账号下全部证书 获取账号下所有证书信息。 
    """,
    "get_all_certs": r""" 
    """,
    "get_resource_url": r""" 
   Args: 
       params: A JSON structure
            ServiceId ( String ): 是  资源所在的服务 ID。 
                  - 您可以在 veImageX 控制台 服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
            Domain ( String ): 是  域名。您可以通过调用 OpenAPI 获取服务下所有域名获取。 
            URI ( String ): 是  文件存储 Uri。您可以通过调用 OpenAPI 获取服务下的上传文件获取。 
            Tpl ( String ): 否  模板名称，缺省情况下表示无模板处理图片。您可以通过调用 OpenAPI 获取服务下所有图片模板获取。 
            Proto ( String ): 否  协议，默认为 http，隐私图片使用 https，公开图片支持取值 http 以及 https。 
            Format ( String ): 否  创建模板时设置的图片输出格式，默认为 image，支持取值有： 
                  - image：表示输出原格式； 
                  - 静图格式：png、jpeg、heic、avif、webp; 
                  - 动图格式：awebp、heif、avis。 
            Timestamp ( Integer ): 否  过期时长，最大限制为 1 年，默认为 1800s。 
                  仅当开启 URL 鉴权配置后，Timestamp 配置生效。 
    """,
    "export_failed_migrate_task": r""" 
   Args: 
       params: A JSON structure
            Region ( String ): 是  任务地区（即任务目标服务的地区），默认空，返回国内任务。 
                  - cn：国内 
                  - va：美东 
                  - sg：新加坡 
            TaskId ( String ): 是  任务 ID，请参考CreateImageMigrateTask获取返回的任务 ID。 
    """,
    "get_image_monitor_rules": r""" 
   Args: 
       params: A JSON structure
            Limit ( Integer ): 否  分页条数。默认值为 10，取值范围为（0，100]。 
            Offset ( Integer ): 否  分页偏移量。默认值为 0，表示从最新一个开始获取。 
            AppId ( String ): 否   
            NamePtn ( String ): 否  告警名称，以正则表达式进行筛选匹配。缺省时默认获取所有报警规则。 
            RuleId ( String ): 否  报警规则 ID，按照指定 ID 返回对应报警规则。缺省时默认获取所有报警规则。 
    """,
    "get_image_template": r""" 
   Args: 
       params: A JSON structure
            ServiceId ( String ): 是  服务 ID。 
                  - 您可以在 veImageX 控制台 服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
            TemplateName ( String ): 是  模板名称。 
                  * 您可以通过调用获取服务下所有模板获取所需的模板名称。 
    """,
    "get_all_image_templates": r""" 
   Args: 
       params: A JSON structure
            ServiceId ( String ): 是  服务ID 
                  - 您可以在 veImageX 控制台 服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
            TemplateNamePattern ( String ): 否  支持的字符正则集合为[a-zA-Z0-9_-]。指定时返回模板名称包含该字符串的图片模板，不填或者为空则返回所有模板。 
            Offset ( Integer ): 否  分页偏移量，默认 0。取值为 1 时，表示跳过第一条数据，从第二条数据取值。 
            Limit ( Integer ): 否  分页获取条数，默认 10。 
            Asc ( String ): 否  是否按照模板创建时间升序查询，默认为false。 
                  * 取值为true时，表示按升序查询。 
                  * 取值为false时，表示降序查询。 
    """,
    "get_image_storage_files": r""" 
   Args: 
       params: A JSON structure
            ServiceId ( String ): 是  服务 ID。 
                  - 您可以在veImageX 控制台 服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
            Marker ( String ): 否  上一次列举返回的位置标记，作为本次列举的起点信息。默认值为空。 
            Limit ( Long ): 否  一次查询列出的文件信息条目数，取值范围为[1,1000]。默认值为 10。 
            Prefix ( String ): 否  指定需要查询文件的前缀，只有资源名匹配该前缀的文件会被列出。缺省时将返回所有文件信息。 
                  例如，一个存储服务中有三个文件，分别为 Example/imagex.png、Example/mov/a.avis 和 Example/mov/b.avis。若指定 Prefix 取值 Example/且指定 Delimiter 取值 /：则返回 Example/imagex.png，并在 CommonPrefix 里返回 Example/mov/。 
            Delimiter ( String ): 否  指定目录分隔符，默认值为空。所有文件名字包含指定的前缀，第一次出现 Delimiter 字符之间的文件作为一组元素（即 CommonPrefixe）。 
    """,
    "get_image_analyze_tasks": r""" 
   Args: 
       params: A JSON structure
            Region ( String ): 否  任务地区。默认为 cn，表示国内。 
            SearchPtn ( String ): 否  返回任务名称或描述中包含该值的任务。 
            Limit ( Integer ): 否  分页条数。取值范围为 (0,100]，默认值为 100。 
            Offset ( Integer ): 否  分页偏移量，默认为 0。取值为 1 时，表示跳过第一条数据，从第二条数据取值。 
       body: A JSON structure
            Name ( String ): 是  任务名称 
            Desc ( String ): 否  任务描述 
            Type ( Integer ): 是  任务类型。取值1表示在线提交URL，取值2表示在线提交URI，取值3表示在线访问触发，取值4表示SDK URL触发 
            ServiceId ( String ): 是  服务ID 
            SampleRate ( Float ): 否  采样率。取值范围(0,1] 
            Tpl ( String ): 否  模板 
            Domain ( Array of String ): 否  域名列表 
            ResUri ( String ): 否  URL/URI zip包的TOS URI。在线提交类任务必填，上传至ServiceId对应的存储下 
            EvalPerStage ( Boolean ): 否  是否模拟模板每阶段输出。仅当Type=2时有效 
    """,
    "get_image_analyze_result": r""" 
   Args: 
       params: A JSON structure
            TaskId ( String ): 是  任务 ID，您可以通过调用 GetImageAnalyzeTasks 获取指定地区全部离线评估任务 ID。 
            StartTime ( Long ): 是  任务运行开始时间，Unix 时间戳。 
            EndTime ( Long ): 是  任务运行结束时间，Unix 时间戳。 
            RunId ( String ): 否  任务执行 ID 
            Limit ( Integer ): 否  分页条数。默认值为 10。 
            Offset ( Integer ): 否  分页偏移量，默认为 0。取值为 1 时，表示跳过第一条数据，从第二条数据取值。 
            File ( String ): 否  文件名 
    """,
    "get_image_audit_result": r""" 
   Args: 
       params: A JSON structure
            TaskId ( String ): 是  任务 ID，您可通过调用 查询所有审核任务 获取所需的任务 ID。 
            Type ( String ): 否  审核场景，缺省情况下查询全部场景的任务。取值如下所示： 
                  - UrlFile：上传 txt 审核文件处理场景 
                  - Url：上传审核图片 URL 处理场景 
                  - Upload：图片上传场景 
            Problem ( String ): 否  问题类型，取值根据审核类型的不同其取值不同。缺省情况下返回全部类型任务。 
                  - 基础安全审核 
                  	- govern：涉政 
                  	- porn ：涉黄 
                  	- illegal：违法违规 
                  	- terror：涉暴 
                  - 智能安全审核 
                  	- 图像风险识别 
                  		- porn ：涉黄，主要适用于通用色情、色情动作、性行为、性暗示、性分泌物、色情动漫、色情裸露等涉黄场景的风险识别 
                  		- sensitive1 ：涉敏1，具体指涉及暴恐风险 
                  		- sensitive2：涉敏2，具体值涉及政治内容风险 
                  		- forbidden：违禁，主要适用于打架斗殴、爆炸、劣迹艺人等场景的风险识别 
                  		- uncomfortable：引人不适，主要适用于恶心、恐怖、尸体、血腥等引人不适场景的风险识别 
                  		- qrcode：二维码，主要适用于识别常见二维码（QQ、微信、其他二维码等） 
                  		- badpicture：不良画面，主要适用于自我伤害、丧葬、不当车播、吸烟/纹身/竖中指等不良社会风气的风险识别 
                  		- sexy：性感低俗，主要适用于舌吻、穿衣性行为、擦边裸露等多种性感低俗场景的风险识别 
                  		- age：年龄，主要适用于图中人物对应的年龄段识别 
                  		- underage：未成年相关，主要适用于儿童色情、儿童邪典等风险识别 
                  		- quality：图片质量，主要适用于图片模糊、纯色边框、纯色屏等风险识别 
                  	- 图文风险识别 
                  		- ad：广告，综合图像及文字内容智能识别广告 
                  		- defraud：诈骗，综合图像及文字内容智能识别诈骗 
                  		- charillegal：文字违规，图片上存在涉黄、涉敏、违禁等违规文字 
            ImageType ( String ): 否  图片类型，缺省情况下返回全部类型任务。取值如下所示： 
                  - problem：问题图片 
                  - frozen：冻结图片 
                  - fail：审核失败图片 
            AuditSuggestion ( String ): 否  审核建议，缺省情况下返回全部任务。取值如下所示： 
                  - nopass：建议不通过 
                  - recheck：建议复审 
            Limit ( Integer ): 否  分页条数。取值范围为 (0,100]，默认值为 10。 
            Marker ( Integer ): 否  上一次查询返回的位置标记，作为本次列举的起点信息。默认值为 0。 
    """,
    "get_image_audit_tasks": r""" 
   Args: 
       params: A JSON structure
            Region ( String ): 否  任务地区。仅支持默认取值 cn，表示国内。 
            Type ( String ): 否  审核场景，缺省情况下查询全部场景的任务。取值如下所示： 
                  - UrlFile：上传 txt 审核文件处理场景 
                  - Url：上传审核图片 URL 处理场景 
                  - Upload：图片上传场景 
            AuditAbility ( Integer ): 否  审核能力，缺省情况下查询全部审核类型的任务。取值如下所示： 
                  - 0：基础审核能力 
                  - 1：智能审核能力 
            Status ( String ): 否  审核状态，缺省情况下查询全部状态的任务。取值如下所示： 
                  - Running：审核中 
                  - Suspend：已暂停 
                  - Done：已完成 
                  - Failed：审核失败 
                  - Cancel：已取消 
            TaskType ( String ): 是  审核任务类型，当前仅支持取值为 audit。 
            Limit ( Integer ): 否  分页条数。取值范围为 (0,100]，默认值为 100。 
            Offset ( Integer ): 否  分页偏移量，默认为 0。取值为 1 时，表示跳过第一条数据，从第二条数据取值。 
    """,
    "get_audit_entrys_count": r""" 
   Args: 
       params: A JSON structure
            TaskId ( String ): 否  任务 ID，您可通过调用 查询所有审核任务 获取所需的任务 ID。 
    """,
    "get_image_transcode_queues": r""" 
   Args: 
       params: A JSON structure
            Region ( String ): 否  队列所在地区。默认当前地区。ToB取值枚举：cn、va、sg。 
            SearchPtn ( String ): 否  返回队列名称或队列描述中包含该值的队列。默认为空，不传则返回所有队列。 
            Limit ( Integer ): 是  分页条数，取值范围为(0,100]。 
            Offset ( Integer ): 否  分页偏移量，默认为 0。取值为 1 时，表示跳过第一条数据，从第二条数据取值。 
       body: A JSON structure
            TaskId ( String ): 是  待更新的任务ID 
            Status ( String ): 是  更新后的任务状态。取值枚举：Running、Suspend、Done 
    """,
    "get_image_transcode_details": r""" 
   Args: 
       params: A JSON structure
            QueueId ( String ): 是  队列 ID，您可通过调用GetImageTranscodeQueues获取该账号下全部任务队列 ID。 
            TaskId ( String ): 否  任务 ID，缺省情况下查询指定队列下所有任务详情。您可通过调用 GetImageTranscodeTasks获取指定队列的全部任务 ID。 
            Region ( String ): 否  队列所在地区。默认当前地区为 cn。 
            StartTime ( Long ): 是  任务提交的起始 Unix 时间戳 
                  StartTime与EndTime时间间隔最大不超过 7 天。 
            EndTime ( Long ): 是  任务提交的截止 Unix 时间戳 
                  StartTime与EndTime时间间隔最大不超过 7 天。 
            Status ( String ): 否  执行状态，填入多个时使用英文逗号分隔。取值如下所示： 
                  - Pending：排队中 
                  - Running：执行中 
                  - Success：执行成功 
                  - Fail：执行失败 
            SearchPtn ( String ): 否  返回图片 url 或 uri 中包含该值的任务。默认为空，不传则返回所有任务。 
            Limit ( Long ): 是  分页条数，取值范围为(0, 100]。 
            Offset ( Long ): 否  分页偏移量，默认为 0。取值为 1 时，表示跳过第一条数据，从第二条数据取值。 
    """,
    "get_image_settings": r""" 
   Args: 
       params: A JSON structure
            AppId ( String ): 是  应用 ID，您可以通过调用获取应用列表的方式获取所需的 AppId。 
            Category ( String ): 否  所属组件，缺省情况下表示获取基础配置列表。 
                  - 取值为HEIF时，表示获取 HEIF 解码库下配置列表； 
                  - 取值为SR时，表示获取客户端下配置列表。 
    """,
    "get_image_setting_rules": r""" 
   Args: 
       params: A JSON structure
            AppId ( String ): 是  应用 ID，您可以通过调用获取应用列表的方式获取所需的 AppId。 
            SettingId ( String ): 是  配置项 ID，您可以通过调用获取配置项列表的方式获取所需的配置项 ID。 
    """,
    "get_image_setting_rule_history": r""" 
   Args: 
       params: A JSON structure
            AppId ( String ): 是  应用 ID，您可以通过调用获取应用列表的方式获取所需的 AppId。 
            SettingId ( String ): 是  配置项 ID，您可以通过调用获取配置项列表的方式获取所需的配置项 ID。 
            Offset ( Integer ): 否  分页偏移量，用于控制分页查询返回结果的起始位置，以便对数据进行分页展示和浏览。默认值为 0。 
                  例如，指定分页条数 Limit = 10，分页偏移量 Offset = 10，表示从查询结果的第 11 条记录开始返回数据，共展示 10 条数据。 
            Limit ( Integer ): 否  分页查询时，显示的每页数据的最大条数。取值范围为 [1,100]，默认值为 10。 
    """,
    "get_image_add_on_tag": r""" 
   Args: 
       params: A JSON structure
            Key ( String ): 是  组件标签 key。取值固定为功能属性，返回相关标签值。 
            Type ( String ): 否  组件类型，默认获取所有类型的标签信息。取值如下所示： 
                  - AI：智能处理类型 
                  - Other：其他增值类型 
    """,
    "get_image_service_subscription": r""" 
   Args: 
       params: A JSON structure
            AddOnType ( String ): 否  附加组件类型，取值AI获取服务端智能处理开通情况。默认返回ImageX服务开通情况 
            AddOnId ( String ): 否  附加组件ID，获取指定附加组件的开通情况。默认返回ImageX服务开通情况 
            AddOnKey ( String ): 否  附加组件英文标识，获取指定附加组件的开通情况。默认返回ImageX服务开通情况。 
    """,
    "get_image_auth_key": r""" 
   Args: 
       params: A JSON structure
            ServiceId ( String ): 是  服务 ID。 
                  - 您可以在 veImageX 控制台服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
    """,
    "get_image_styles": r""" 
   Args: 
       params: A JSON structure
            Type ( String ): 是  样式类型。取值 user 表示用户样式。 
            SearchPtn ( String ): 否  需要返回的样式列表标识。 
                  * 返回的样式名称、样式 ID 包含了该值的样式列表。 
                  * 返回的样式宽度或样式高度为该值的样式列表。 
            Limit ( Integer ): 否  分页返回条数，取值范围为[0,100]，默认 10 条。 
            Offset ( Integer ): 否  分页偏移，默认 0，取值为 1 时，表示跳过一条数据，从第二条数据取值。 
    """,
    "get_image_fonts": r""" 
    """,
    "get_image_elements": r""" 
   Args: 
       params: A JSON structure
            Type ( String ): 是  要素类型，取值如下所示： 
                  * image：图片要素； 
                  * background：背景要素； 
                  * mask：蒙版要素。 
            SearchPtn ( String ): 否  返回图片 URI 中包含该值的要素列表。 
            Limit ( Integer ): 否  分页返回条数。默认 10，最大限制为 100。 
            Offset ( Integer ): 否  分页偏移，默认 0，取值为 1 时，表示跳过一条数据，从第二条数据取值。 
    """,
    "get_image_background_colors": r""" 
    """,
    "describe_image_x_summary": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。支持查询多个服务，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有服务。您可以在 veImageX 控制台的服务管理模块或者调用 GetAllImageServices 接口获取服务 ID。 
            Timestamp ( String ): 是  数据查询时间段，即Timestamp所在月份的 1 日 0 时起至传入时间Timestamp的时间范围。 
                  格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
    """,
    "describe_image_x_domain_traffic_data": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。支持查询多个服务，传入多个时用英文逗号“,”分割，缺省时表示查询所有服务。您可以在 veImageX 控制台的服务管理模块或者调用 GetAllImageServices 接口获取服务 ID。 
            DomainNames ( String ): 否  域名。支持查询多个域名，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有域名。您可以通过调用 GetServiceDomains 获取服务下所有域名信息。 
            BillingRegion ( String ): 否  计费区域。支持查询多个区域，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有区域。取值如下所示： 
                  - CHN：中国内地 
                  - AP1：亚太一区 
                  - AP2：亚太二区 
                  - AP3：亚太三区 
                  - EU：欧洲 
                  - ME：中东和非洲 
                  - SA：南美 
                  - NA：北美 
                  - OTHER：其他 
            GroupBy ( String ): 否  需要分组查询的参数。不传表示不拆分维度，传入多个用英文逗号分隔。取值如下所示： 
                  - ServiceId：服务 ID 
                  - DomainName ：域名 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近一年历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2010-11-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒。缺省时查询 StartTime 和 EndTime 时间段全部数据，此时单次查询最大时间跨度为 93 天。取值如下所示： 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_domain_bandwidth_data": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。支持查询多个服务，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有服务。您可以在 veImageX 控制台的服务管理模块或者调用 GetAllImageServices 接口获取服务 ID。 
            DomainNames ( String ): 否  域名。支持查询多个域名，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有域名。您可以通过调用 GetServiceDomains 获取服务下所有域名信息。 
            BillingRegion ( String ): 否  计费区域。支持查询多个区域，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有区域。取值如下所示： 
                  - CHN：中国内地 
                  - AP1：亚太一区 
                  - AP2：亚太二区 
                  - AP3：亚太三区 
                  - EU：欧洲 
                  - ME：中东和非洲 
                  - SA：南美 
                  - NA：北美 
                  - OTHER：其他 
            GroupBy ( String ): 否  需要分组查询的参数。不传表示不拆分维度，传入多个用英文逗号分隔。取值如下所示： 
                  - ServiceId：服务 ID 
                  - DomainName ：域名 
            StartTime ( String ): 是  取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近一年历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2010-11-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( Integer ): 否  查询数据的时间粒度。单位为秒。缺省时查询 StartTime 和 EndTime 时间段全部数据，此时单次查询最大时间跨度为 93 天。取值如下所示： 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_bucket_usage": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。为空时表示不筛选，支持查询多个服务，使用逗号分隔不同的服务。 
                  - 您可以在 veImageX 控制台服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考 GetAllImageServices。 
            BucketNames ( String ): 否  Bucket 名称。支持同时查询多个 BucketName，不同的 BucketNmae 使用逗号分隔。 
                  您可以通过调用 GetAllImageServices 获取所需的 Bucket 名称。 
            GroupBy ( String ): 否  需要分组查询的参数，多个数据用逗号分隔。支持取值如下： 
                  - ServiceId：服务 ID 
                  - BucketName：Bucket 名称 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm。例如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近一年历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2010-11-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm。例如2019-06-02T00:00:00+08:00。 
    """,
    "describe_image_x_billing_request_cnt_usage": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。支持查询多个服务，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有服务。您可以在 veImageX 控制台的服务管理模块或者调用 GetAllImageServices 接口获取服务 ID。 
            AdvFeats ( String ): 否  组件名称。支持查询多个组件，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有组件。您可通过调用 GetImageAddOnConf 查看Key返回值。 
            GroupBy ( String ): 是  固定值，仅支持AdvFeat即附加组件。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近一年历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2010-11-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒。缺省时查询 StartTime 和 EndTime 时间段全部数据，此时单次查询最大时间跨度为 93 天。支持取值如下： 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_request_cnt_usage": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。支持查询多个服务，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有服务。您可以在 veImageX 控制台的服务管理模块或者调用 GetAllImageServices 接口获取服务 ID。 
            AdvFeats ( String ): 否  组件名称。支持查询多个组件，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有组件。您可通过调用 GetImageAddOnConf 查看Key返回值。 
            Templates ( String ): 否  图片处理模板。支持查询多个模板，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有模板。您可通过调用 GetAllImageTemplates 获取服务下全部模版信息。 
            GroupBy ( String ): 否  维度拆分的维度值。不传表示不拆分维度，只能传入单个参数。支持取值如下： 
                  - ServiceId：服务 
                  - AdvFeat：组件 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近一年历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2010-11-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒。缺省时查询 StartTime 和 EndTime 时间段全部数据，此时单次查询最大时间跨度为 93 天。取值如下所示： 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_base_op_usage": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。支持查询多个服务，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有服务。您可以在 veImageX 控制台的服务管理模块或者调用 GetAllImageServices 接口获取服务 ID。 
            GroupBy ( String ): 否  需要分组查询的参数，当前仅支持取值 ServiceId，表示按服务 ID 进行分组。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近一年历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2010-11-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒。缺省时查询 StartTime 和 EndTime 时间段全部数据，此时单次查询最大时间跨度为 93 天。取值如下所示： 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_compress_usage": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。支持查询多个服务，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有服务。您可以在 veImageX 控制台的服务管理模块或者调用 GetAllImageServices 接口获取服务 ID。 
            GroupBy ( String ): 否  需要分组查询的参数，当前仅支持取值 ServiceId，表示按服务 ID 进行分组。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近一年历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2010-11-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒。缺省时查询 StartTime 和 EndTime 时间段全部数据，此时单次查询最大时间跨度为 93 天。取值如下所示： 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_screenshot_usage": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。支持查询多个服务，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有服务。您可以在 veImageX 控制台的服务管理模块或者调用 GetAllImageServices 接口获取服务 ID。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近一年历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2010-11-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒。缺省时查询 StartTime 和 EndTime 时间段全部数据，此时单次查询最大时间跨度为 93 天。取值如下所示： 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_video_clip_duration_usage": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。支持查询多个服务，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有服务。您可以在 veImageX 控制台的服务管理模块或者调用 GetAllImageServices 接口获取服务 ID。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近一年历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2010-11-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒。缺省时查询 StartTime 和 EndTime 时间段全部数据，此时单次查询最大时间跨度为 93 天。取值如下所示： 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_multi_compress_usage": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。支持查询多个服务，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有服务。您可以在 veImageX 控制台的服务管理模块或者调用 GetAllImageServices 接口获取服务 ID。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近 93 天的历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2011-08-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒，缺省时查询StartTime和EndTime时间段全部数据，此时单次查询最大时间跨度为 93 天。取值如下所示： 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_edge_request": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。支持查询多个服务，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有服务。您可以在 veImageX 控制台的服务管理模块或者调用 GetAllImageServices 接口获取服务 ID。 
            DomainNames ( String ): 否  域名。支持查询多个域名，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有域名。您可以通过调用 GetServiceDomains 获取服务下所有域名信息。 
            Regions ( String ): 否  计费区域。支持查询多个区域，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有区域。取值如下所示： 
                  - 中国大陆 
                  - 亚太一区 
                  - 亚太二区 
                  - 亚太三区 
                  - 欧洲区 
                  - 北美区 
                  - 南美区 
                  - 中东区 
            UserCountry ( String ): 否  客户端国家。支持查询多个国家，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有国家。您可通过调用 DescribeImageXEdgeRequestRegions 获取 IP 解析后的客户端国家。取值如下所示： 
                  - 海外，除中国外全部国家。 
                  - 具体国家取值，如中国、美国。 
            UserProvince ( String ): 否  客户端省份。支持查询多个省份，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有省份。可调用 DescribeImageXEdgeRequestRegions 获取 IP 解析后的客户端省份。 
            Protocols ( String ): 否  过滤网络协议。传入多个用英文逗号分割，缺省情况下表示不过滤。取值如下所示： 
                  - HTTP 
                  - HTTPS 
            Isp ( String ): 否  过滤运营商。传入多个用英文逗号分割，缺省情况下表示不过滤。取值如下所示： 
                  - 电信 
                  - 联通 
                  - 移动 
                  - 鹏博士 
                  - 教育网 
                  - 广电网 
                  - 其它 
            DataTypes ( String ): 是  状态码，传入多个时用英文逗号分隔。取值如下所示： 
                  - req_cnt：返回所有状态码数据 
                  - 2xx：返回 2xx 状态码汇总数据 
                  - 3xx：返回 3xx 状态码汇总数据 
                  - 4xx：返回 4xx 状态码汇总数据 
                  - 5xx：返回 5xx 状态码汇总数据。 
            GroupBy ( String ): 否  需要分组查询的参数，传入多个用英文逗号分割。取值如下所示： 
                  - DomainName：域名 
                  - DataType：状态码 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近 93 天的历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2011-08-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒，缺省时查询StartTime和EndTime时间段全部数据，此时单次查询最大时间跨度为 93 天。支持以下取值： 
                  - 60：单次查询最大时间跨度为 6 小时 
                  - 120：单次查询最大时间跨度为 6 小时 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
            DetailedCode ( Boolean ): 否  是否拆分状态码，取值如下所示： 
                  - true：拆分 
                  - false：（默认）不拆分 
    """,
    "describe_image_x_edge_request_bandwidth": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。支持查询多个服务，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有服务。您可以在 veImageX 控制台的服务管理模块或者调用 GetAllImageServices 接口获取服务 ID。 
            DomainNames ( String ): 否  域名。支持查询多个域名，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有域名。您可以通过调用 GetServiceDomains 获取服务下所有域名信息。 
            Regions ( String ): 否  计费区域。支持查询多个区域，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有区域。取值如下所示： 
                  - 中国大陆 
                  - 亚太一区 
                  - 亚太二区 
                  - 亚太三区 
                  - 欧洲区 
                  - 北美区 
                  - 南美区 
                  - 中东区 
            UserCountry ( String ): 否  客户端国家。传入多个时用英文逗号作为分割符，缺省情况下表示不过滤。可调用 DescribeImageXEdgeRequestRegions 获取 IP 解析后的客户端国家。取值如下所示： 
                  - 海外，除中国外全部国家。 
                  - 具体国家取值，如中国、美国。 
            UserProvince ( String ): 否  客户端省份。传入多个用英文逗号分割，缺省情况下表示不过滤。可调用 DescribeImageXEdgeRequestRegions 获取 IP 解析后的客户端省份。 
            Protocols ( String ): 否  过滤网络协议。传入多个用英文逗号分割，缺省情况下表示不过滤。取值如下所示： 
                  - HTTP 
                  - HTTPS 
            Isp ( String ): 否  过滤运营商。传入多个用英文逗号分割，缺省情况下表示不过滤。取值如下所示： 
                  - 电信 
                  - 联通 
                  - 移动 
                  - 鹏博士 
                  - 教育网 
                  - 广电网 
                  - 其它 
            GroupBy ( String ): 否  分组依据，取值仅支持DomainName。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近 93 天的历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2011-08-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒，缺省时查询StartTime和EndTime时间段全部数据，此时单次查询最大时间跨度为 93 天。取值如下所示： 
                  - 60：单次查询最大时间跨度为 6 小时 
                  - 120：单次查询最大时间跨度为 6 小时 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_edge_request_traffic": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。支持查询多个服务，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有服务。您可以在 veImageX 控制台的服务管理模块或者调用 GetAllImageServices 接口获取服务 ID。 
            DomainNames ( String ): 否  域名。支持查询多个域名，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有域名。您可以通过调用 GetServiceDomains 获取服务下所有域名信息。 
            Regions ( String ): 否  区域。支持查询多个区域，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有区域。取值如下所示： 
                  - 中国大陆 
                  - 亚太一区 
                  - 亚太二区 
                  - 亚太三区 
                  - 欧洲区 
                  - 北美区 
                  - 南美区 
                  - 中东区 
            UserCountry ( String ): 否  客户端国家。传入多个时用英文逗号作为分割符，缺省情况下表示不过滤。您可以通过调用 DescribeImageXEdgeRequestRegions 获取 IP 解析后的客户端国家。取值如下所示： 
                  - 海外，除中国外全部国家。 
                  - 具体国家取值，如中国、美国。 
            UserProvince ( String ): 否  客户端省份。传入多个用英文逗号分割，缺省情况下表示不过滤。可调用 DescribeImageXEdgeRequestRegions 获取 IP 解析后的客户端省份。 
            Protocols ( String ): 否  过滤网络协议。传入多个用英文逗号分割，缺省情况下表示不过滤。取值如下所示： 
                  - HTTP 
                  - HTTPS 
            Isp ( String ): 否  过滤运营商。传入多个用英文逗号分割，缺省情况下表示不过滤。取值如下所示： 
                  - 电信 
                  - 联通 
                  - 移动 
                  - 鹏博士 
                  - 教育网 
                  - 广电网 
                  - 其它 
            GroupBy ( String ): 否  分组依据，取值仅支持DomainName。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近 93 天的历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2011-08-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒，缺省时查询StartTime和EndTime时间段全部数据，此时单次查询最大时间跨度为 93 天。取值如下所示： 
                  - 60：单次查询最大时间跨度为 6 小时 
                  - 120：单次查询最大时间跨度为 6 小时 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_edge_request_regions": r""" 
   Args: 
       params: A JSON structure
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm。例如2019-06-02T00:00:00+08:00。起始时间与结束时间间隔小于等于 90 天。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm。例如2019-06-02T00:00:00+08:00。起始时间与结束时间间隔小于等于 90 天。 
    """,
    "describe_image_x_server_qps_usage": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。支持查询多个服务，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有服务。您可以在 veImageX 控制台的服务管理模块或者调用 GetAllImageServices 接口获取服务 ID。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近 93 天的历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2011-08-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒。缺省时查询StartTime和EndTime时间段全部数据，此时单次查询最大时间跨度为 93 天。取值如下所示： 
                  - 1: 单次查询最大时间跨度为 6 小时 
                  - 60：单次查询最大时间跨度为 6 小时 
                  - 120：单次查询最大时间跨度为 6 小时 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_hit_rate_traffic_data": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。支持查询多个服务，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有服务。您可以在 veImageX 控制台的服务管理模块或者调用 GetAllImageServices 接口获取服务 ID。 
            DomainNames ( String ): 否  域名。支持查询多个域名，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有域名。您可以通过调用 GetServiceDomains 获取服务下所有域名信息。 
            GroupBy ( String ): 否  需要分组查询的参数。取值仅支持DomainName。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm。例如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近 93 天的历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2011-08-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm。例如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度，单位为秒。缺省时查询StartTime和EndTime时间段全部数据，此时单次查询最大时间跨度为 93 天。支持以下取值： 
                  - 60：单次查询最大时间跨度为 6 小时 
                  - 120：单次查询最大时间跨度为 6 小时 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_hit_rate_request_data": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。支持查询多个服务，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有服务。您可以在 veImageX 控制台的服务管理模块或者调用 GetAllImageServices 接口获取服务 ID。 
            DomainNames ( String ): 否  域名。支持查询多个域名，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有域名。您可以通过调用 GetServiceDomains 获取服务下所有域名信息。 
            GroupBy ( String ): 否  需要分组查询的参数。取值仅支持DomainName。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm。例如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近 93 天的历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2011-08-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm。例如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度，单位为秒。缺省时查询StartTime和EndTime时间段全部数据，此时单次查询最大时间跨度为 93 天。支持以下取值： 
                  - 60：单次查询最大时间跨度为 6 小时 
                  - 120：单次查询最大时间跨度为 6 小时 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_xcdn_top_request_data": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。支持查询多个服务，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有服务。您可以在 veImageX 控制台的服务管理模块或者调用 GetAllImageServices 接口获取服务 ID。 
            DomainNames ( String ): 否  域名。支持查询多个域名，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有域名。您可以通过调用 GetServiceDomains 获取所需的域名。 
            IPVersion ( String ): 否  网络协议。缺省情况下则表示不限制网络协议，取值如下所示： 
                  - IPv4 
                  - IPv6 
                  KeyType取值为Domain时，IPVersion的取值无效。 
            Country ( String ): 否  数据访问区域。仅在KeyType取值为Region或Isp时生效，取值如下所示： 
                  - China：中国。 
                  - Other：中国境外的区域。 
            KeyType ( String ): 是  排序依据，取值如下所示： 
                  - URL：生成的图片访问 URL 
                  - UserAgent：用户代理 
                  - Refer：请求 Refer 
                  - ClientIP：客户端 IP 
                  - Region：访问区域 
                  - Domain：域名 
                  - Isp：运营商 
            ValueType ( String ): 是  排序依据，即获取按ValueType值排序的KeyType列表。取值如下所示： 
                  - Traffic：按流量排序 
                  - RequestCnt：按请求次数排序 
                  当KeyType取值为Domain时，仅支持将ValueType取值为Traffic，即按照流量排序获取域名列表。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如 2019-06-02T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如 2019-06-02T00:00:00+08:00。 
            Limit ( String ): 否  每页查询数据量，默认为0，即返回所有数据。 
            Offset ( String ): 否  分页偏移量，默认取值为0 。取值为10时，表示跳过前 10 条数据，从第 11 条数据开始取值。 
    """,
    "describe_image_x_service_quality": r""" 
   Args: 
       params: A JSON structure
            Region ( String ): 否  获取指定地区的数据。默认为空，表示获取国内数据。 
                  * cn：国内。 
                  * sg：新加坡。 
    """,
    "get_image_x_query_apps": r""" 
   Args: 
       params: A JSON structure
            Source ( String ): 否  数据来源，账号下近 60 天内有数据上报的应用 ID，缺省情况下返回账号对应的全部应用 ID。取值如下所示： 
                  * upload：上传 1.0 数据。 
                  * cdn：下行网络数据。 
                  * client：客户端数据。 
                  * sensible：感知数据。 
                  * uploadv2：上传 2.0 数据。 
                  * exceed：大图监控数据。 
    """,
    "get_image_x_query_regions": r""" 
   Args: 
       params: A JSON structure
            Source ( String ): 是  数据来源，取值如下所示： 
                  * upload：上传 1.0 数据。 
                  * cdn：下行网络数据。 
                  * client：客户端数据。 
                  * uploadv2：上传 2.0 数据。 
            Appid ( String ): 否  应用 ID。默认为空，匹配账号下所有的 AppID。 
                  您可以通过调用获取应用列表的方式获取所需的应用 ID。 
            OS ( String ): 否  需要匹配的系统类型。取值如下所示： 
                  - 不传或传空字符串：Android+iOS。 
                  - iOS：iOS。 
                  - Android：Android。 
                  - WEB：web+小程序。 
                  - Web：web，仅当Source为upload或uploadv2时可传。 
                  - Imp：小程序，仅当Source为upload或uploadv2时可传。 
    """,
    "get_image_x_query_dims": r""" 
   Args: 
       params: A JSON structure
            Source ( String ): 是  数据来源，取值如下所示： 
                  * upload：上传 1.0 数据。 
                  * cdn：下行网络数据。 
                  * client：客户端数据。 
                  * sensible：感知数据。 
                  * uploadv2：上传 2.0 数据。 
                  * exceed：大图监控数据，包含大图样本量和大图明细。 
                  * exceed_all：大图分布数据。 
            Appid ( String ): 否  应用 ID。默认为空，匹配账号下所有的 AppID。 
                  您可以通过调用获取应用列表的方式获取所需的 AppID。 
            OS ( String ): 否  需要匹配的系统类型。取值如下所示： 
                  - 不传或传空字符串：Android+iOS。 
                  - iOS：iOS。 
                  - Android：Android。 
                  - WEB：web+小程序。 
                  - Web：web，仅当Source为upload或uploadv2时可传。 
                  - Imp：小程序，仅当Source为upload或uploadv2时可传。 
    """,
    "get_image_x_query_vals": r""" 
   Args: 
       params: A JSON structure
            Dim ( String ): 是  自定义维度名称。 
                  您可以通过调用获取自定义维度列表获取所需的维度名称。 
            Source ( String ): 是  数据来源。 
                  * upload：上传 1.0 数据。 
                  * cdn：下行网络数据。 
                  * client：客户端数据。 
                  * sensible：感知数据。 
                  * uploadv2：上传 2.0 数据。 
                  * exceed：大图监控数据，包含大图样本量和大图明细。 
                  * exceed_all：大图分布数据。 
            Appid ( String ): 否  应用 ID。默认为空，匹配中账号下所有的 AppID。 
                  您可以通过调用获取应用列表的方式获取所需的 AppID。 
            OS ( String ): 否  需要匹配的系统类型。取值如下所示： 
                  - 不传或传空字符串：Android+iOS。 
                  - iOS：iOS。 
                  - Android：Android。 
                  - WEB：web+小程序。 
                  - Web：web，仅当Source为upload或uploadv2时可传。 
                  - Imp：小程序，仅当Source为upload或uploadv2时可传。 
            Keyword ( String ): 否  需要过滤的关键词（包含），不传则不过滤关键词。 
    """,
    "get_image_upload_file": r""" 
   Args: 
       params: A JSON structure
            ServiceId ( String ): 是  服务 ID。 
                  - 您可以在veImageX 控制台 服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
            StoreUri ( String ): 是  文件 Uri。 
                  - 您可以在 veImageX 控制台 资源管理页面，在已上传文件的名称列获取资源 Uri。 
                  - 您也可以通过 OpenAPI 的方式获取Uri，具体请参考 GetImageUploadFiles。 
    """,
    "preview_image_upload_file": r""" 
   Args: 
       params: A JSON structure
            ServiceId ( String ): 是  服务 ID。 
                  - 您可以在 veImageX 控制台 服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
            StoreUri ( String ): 是  文件存储 URI。 
                  - 您可以在 veImageX 控制台 资源管理页面，在已上传文件的名称列获取。 
                  - 您也可以通过 OpenAPI 的方式获取，具体请参考获取服务下的上传文件。 
    """,
    "get_image_update_files": r""" 
   Args: 
       params: A JSON structure
            ServiceId ( String ): 是  需要查询的服务 ID。 
                  - 您可以在 veImageX 控制台 服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
            Type ( Integer ): 否  获取类型，取值如下所示： 
                  - 0：获取刷新 URL 列表 
                  - 1：获取禁用 URL 列表 
            UrlPattern ( String ): 否  URL 格式，若指定 URL 格式则仅返回 URL 中包含该字符串的 URL 列表。默认为空，缺省情况下返回所有 URL 列表。 
            Offset ( Integer ): 否  分页偏移量，用于控制分页查询返回结果的起始位置，以便对数据进行分页展示和浏览。默认值为 0。 
                  例如，指定分页条数 Limit = 10，分页偏移量 Offset = 10，表示从查询结果的第 11 条记录开始返回数据，共展示 10 条数据。 
            Limit ( Integer ): 否  分页查询时，显示的每页数据的最大条数。最大值为 100。 
    """,
    "get_image_erase_models": r""" 
   Args: 
       params: A JSON structure
            Type ( Integer ): 否  模型。默认取值为0。 
                  * 0：自动检测并擦除模型列表。 
                  * 1：指定区域擦除模型列表。 
    """,
    "get_response_header_validate_keys": r""" 
    """,
    "describe_image_x_domain_bandwidth_ninety_five_data": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。支持查询多个服务，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有服务。您可以在 veImageX 控制台的服务管理模块或者调用 GetAllImageServices 接口获取服务 ID。 
            DomainNames ( String ): 否  域名。支持查询多个域名，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有域名。您可以通过调用 GetServiceDomains 获取服务下所有域名信息。 
            BillingRegion ( String ): 否  计费区域。支持查询多个区域，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有区域。取值如下所示： 
                  - CHN：中国内地 
                  - AP1：亚太一区 
                  - AP2：亚太二区 
                  - AP3：亚太三区 
                  - EU：欧洲 
                  - ME：中东和非洲 
                  - SA：南美 
                  - NA：北美 
                  - OTHER：其他 
            StartTime ( String ): 是  取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近一年历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2010-11-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
    """,
    "get_batch_task_info": r""" 
   Args: 
       params: A JSON structure
            TaskId ( String ): 是  异步任务 ID，传入 CreateBatchProcessTask 获取的异步任务 ID。 
            ServiceId ( String ): 是  服务 ID。 
                  - 您可以在 veImageX 控制台 服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
    """,
    "get_all_image_services": r""" 
   Args: 
       params: A JSON structure
            SearchPtn ( String ): 否  筛选服务的参数，当该值为空时返回所有服务，指定后返回服务名或者 ID 中包含该字符串的服务。 
    """,
    "describe_image_x_bucket_retrieval_usage": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。为空时表示不筛选，支持查询多个服务，使用逗号分隔不同的服务。 
                  - 您可以在 veImageX 控制台服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考 GetAllImageServices。 
            BucketNames ( String ): 否  Bucket 名称。支持同时查询多个 BucketName，不同的 BucketNmae 使用逗号分隔。 
                  您可以通过调用 GetAllImageServices 获取所需的 Bucket 名称。 
            GroupBy ( String ): 否  需要分组查询的参数，多个数据用逗号分隔。支持取值如下： 
                  - ServiceId：服务 ID 
                  - BucketName：Bucket 名称 
                  - StorageType：存储类型 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm。例如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近一年历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2010-11-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm。例如2019-06-02T00:00:00+08:00。 
            IsRetrieval ( Boolean ): 否  是否查询数据取回量。 
                  - true：查询取回量。 
                  - false：查询存储量。 
    """,
    "get_image_migrate_tasks": r""" 
   Args: 
       params: A JSON structure
            Region ( String ): 否  任务地区（即任务目标服务的地区），缺省时将返回国内列表。取值如下所示： 
                  - cn：国内 
                  - sg：新加坡 
            TaskId ( String ): 否  任务 ID。 
            ServiceId ( String ): 否  迁移的目标服务 ID。 
            Offset ( Long ): 否  分页偏移量，用于控制分页查询返回结果的起始位置，以便对数据进行分页展示和浏览。默认值为 0。 
                  例如，指定分页条数 Limit = 10，分页偏移量 Offset = 10，表示从查询结果的第 11 条记录开始返回数据，共展示 10 条数据。 
            Limit ( Integer ): 否  分页查询时，显示的每页数据的最大条数。默认值为 10，最大值为 1000。 
            TaskNamePtn ( String ): 否  返回任务名称中包含该值的迁移任务信息。 
            Status ( String ): 否  任务状态，填入多个时使用英文逗号分隔。取值如下所示： 
                  - Initial：创建中 
                  - Running：运行中 
                  - Done：全部迁移完成 
                  - Partial：部分迁移完成 
                  - Failed：迁移失败 
                  - Terminated：中止 
    """,
    "export_failed_migrate_task": r""" 
   Args: 
       params: A JSON structure
            Region ( String ): 是  任务地区（即任务目标服务的地区），默认空，返回国内任务。 
                  - cn：国内 
                  - sg：新加坡 
            TaskId ( String ): 是  任务 ID，请参考CreateImageMigrateTask获取返回的任务 ID。 
    """,
    "describe_image_x_source_request": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。为空时表示不筛选，支持查询多个服务，使用逗号分隔不同的服务。 
                  - 您可以在 veImageX 控制台服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考 GetAllImageServices。 
            DomainNames ( String ): 否  域名。为空时表示不筛选，支持查询多个域名，不同的域名使用逗号分隔。 
                  您可以通过调用 GetServiceDomains 获取服务下所有域名信息。 
            Regions ( String ): 否  区域。传入多个时用英文逗号作为分割符，缺省情况下表示查询所有区域。取值如下所示： 
                  - 中国大陆 
                  - 亚太一区 
                  - 亚太二区 
                  - 亚太三区 
                  - 欧洲区 
                  - 北美区 
                  - 南美区 
                  - 中东区 
            UserCountry ( String ): 否  客户端国家。传入多个时用英文逗号作为分割符，缺省情况下表示不过滤。可调用 DescribeImageXEdgeRequestRegions 获取 IP 解析后的客户端国家。取值如下所示： 
                  - 海外，除中国外全部国家。 
                  - 具体国家取值，如中国、美国。 
            UserProvince ( String ): 否  客户端省份。传入多个用英文逗号分割。缺省情况下表示不过滤。可调用 DescribeImageXEdgeRequestRegions 获取 IP 解析后的客户端省份。 
            Protocols ( String ): 否  过滤网络协议。传入多个用英文逗号分割。缺省情况下表示不过滤。取值如下所示： 
                  - HTTP 
                  - HTTPS 
            Isp ( String ): 否  过滤运营商。传入多个用英文逗号分割，缺省情况下表示不过滤。取值如下所示： 
                  - 电信 
                  - 联通 
                  - 移动 
                  - 鹏博士 
                  - 教育网 
                  - 广电网 
                  - 其它 
            DataTypes ( String ): 是  状态码。传入多个时用英文逗号分隔。支持以下取值： 
                  - req_cnt：返回所有状态码数据 
                  - 2xx：返回 2xx 状态码汇总数据 
                  - 3xx：返回 3xx 状态码汇总数据 
                  - 4xx：返回 4xx 状态码汇总数据 
                  - 5xx：返回 5xx 状态码汇总数据。 
            GroupBy ( String ): 否  需要分组查询的参数。传入多个用英文逗号分割。支持以下取值： 
                  - DomainName：域名 
                  - DataType：状态码 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近 93 天的历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2011-08-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒，缺省时查询StartTime和EndTime时间段全部数据，此时单次查询最大时间跨度为 93 天。支持以下取值： 
                  - 60：单次查询最大时间跨度为 6 小时 
                  - 120：单次查询最大时间跨度为 6 小时 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
            DetailedCode ( Boolean ): 否  是否拆分状态码。取值如下所示： 
                  - true：拆分 
                  - false：（默认）不拆分 
    """,
    "describe_image_x_source_request_bandwidth": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。为空时表示不筛选，支持查询多个服务，使用逗号分隔不同的服务。 
                  - 您可以在 veImageX 控制台服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考 GetAllImageServices。 
            DomainNames ( String ): 否  域名。为空时表示不筛选，支持查询多个域名，不同的域名使用逗号分隔。 
                  您可以通过调用 GetServiceDomains 获取服务下所有域名信息。 
            Regions ( String ): 否  区域。传入多个时用英文逗号作为分割符，缺省情况下表示查询所有区域。取值如下所示： 
                  - 中国大陆 
                  - 亚太一区 
                  - 亚太二区 
                  - 亚太三区 
                  - 欧洲区 
                  - 北美区 
                  - 南美区 
                  - 中东区 
            UserCountry ( String ): 否  客户端国家。传入多个时用英文逗号作为分割符，缺省情况下表示不过滤。可调用 DescribeImageXEdgeRequestRegions 获取 IP 解析后的客户端国家。取值如下所示： 
                  - 海外，除中国外全部国家。 
                  - 具体国家取值，如中国、美国。 
            UserProvince ( String ): 否  客户端省份。传入多个用英文逗号分割。缺省情况下表示不过滤。可调用 DescribeImageXEdgeRequestRegions 获取 IP 解析后的客户端省份。 
            Protocols ( String ): 否  过滤网络协议。传入多个用英文逗号分割。缺省情况下表示不过滤。取值如下所示： 
                  - HTTP 
                  - HTTPS 
            Isp ( String ): 否  过滤运营商。传入多个用英文逗号分割，缺省情况下表示不过滤。取值如下所示： 
                  - 电信 
                  - 联通 
                  - 移动 
                  - 鹏博士 
                  - 教育网 
                  - 广电网 
                  - 其它 
            GroupBy ( String ): 否  分组依据，仅支持取值DomainName。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近 93 天的历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2011-08-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒，缺省时查询StartTime和EndTime时间段全部数据，此时单次查询最大时间跨度为 93 天。支持以下取值： 
                  - 60：单次查询最大时间跨度为 6 小时 
                  - 120：单次查询最大时间跨度为 6 小时 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_source_request_traffic": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。为空时表示不筛选，支持查询多个服务，使用逗号分隔不同的服务。 
                  - 您可以在 veImageX 控制台服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考 GetAllImageServices。 
            DomainNames ( String ): 否  域名。为空时表示不筛选，支持查询多个域名，不同的域名使用逗号分隔。 
                  您可以通过调用 GetServiceDomains 获取服务下所有域名信息。 
            Regions ( String ): 否  区域。传入多个时用英文逗号作为分割符，缺省情况下表示查询所有区域。取值如下所示： 
                  - 中国大陆 
                  - 亚太一区 
                  - 亚太二区 
                  - 亚太三区 
                  - 欧洲区 
                  - 北美区 
                  - 南美区 
                  - 中东区 
            UserCountry ( String ): 否  客户端国家。传入多个时用英文逗号作为分割符，缺省情况下表示不过滤。可调用 DescribeImageXEdgeRequestRegions 获取 IP 解析后的客户端国家。取值如下所示： 
                  - 海外，除中国外全部国家。 
                  - 具体国家取值，如中国、美国。 
            UserProvince ( String ): 否  客户端省份。传入多个用英文逗号分割。缺省情况下表示不过滤。可调用 DescribeImageXEdgeRequestRegions 获取 IP 解析后的客户端省份。 
            Protocols ( String ): 否  过滤网络协议。传入多个用英文逗号分割。缺省情况下表示不过滤。取值如下所示： 
                  - HTTP 
                  - HTTPS 
            Isp ( String ): 否  过滤运营商。传入多个用英文逗号分割，缺省情况下表示不过滤。取值如下所示： 
                  - 电信 
                  - 联通 
                  - 移动 
                  - 鹏博士 
                  - 教育网 
                  - 广电网 
                  - 其它 
            GroupBy ( String ): 否  分组依据，仅支持取值DomainName。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近 93 天的历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2011-08-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照ISO8601表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒，缺省时查询StartTime和EndTime时间段全部数据，此时单次查询最大时间跨度为 93 天。支持以下取值： 
                  - 60：单次查询最大时间跨度为 6 小时 
                  - 120：单次查询最大时间跨度为 6 小时 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_x_cube_usage": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。支持查询多个服务，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有服务。您可以在 veImageX 控制台的服务管理模块或者调用 GetAllImageServices 接口获取服务 ID。 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近一年历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2010-11-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒。缺省时查询 StartTime 和 EndTime 时间段全部数据，此时单次查询最大时间跨度为 93 天。取值如下所示： 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "describe_image_xai_request_cnt_usage": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。支持查询多个服务，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有服务。您可以在 veImageX 控制台的服务管理模块或者调用 GetAllImageServices 接口获取服务 ID。 
            AdvFeats ( String ): 否  组件名称。支持查询多个组件，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有组件。您可通过调用 GetImageAddOnConf 查看Key返回值。 
            Templates ( String ): 否  图片处理模板。支持查询多个模板，传入多个时用英文逗号“,”分割，缺省情况下表示查询所有模板。您可通过调用 GetAllImageTemplates 获取服务下全部模版信息。 
            EnableBillingRate ( Boolean ): 否  是否叠加计费倍率。默认为false。 
            GroupBy ( String ): 否  维度拆分的维度值。不传表示不拆分维度，只能传入单个参数。支持取值如下： 
                  - ServiceId：服务 
                  - AdvFeat：组件 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近一年历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2010-11-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm，比如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 否  查询数据的时间粒度。单位为秒。缺省时查询 StartTime 和 EndTime 时间段全部数据，此时单次查询最大时间跨度为 93 天。取值如下所示： 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 600：单次查询最大时间跨度为 31 天 
                  - 1200：单次查询最大时间跨度为 31 天 
                  - 1800：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
                  - 604800：单次查询最大时间跨度为 93 天 
    """,
    "apply_vpc_upload_info": r""" 
   Args: 
       params: A JSON structure
            ServiceId ( String ): 是  服务 ID。 
                  - 您可以在 veImageX 控制台 服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
            StoreKey ( String ): 否  上传文件的存储 Key。默认使用随机生成的字符串作为存储 Key。 
                  存储 Key 详细命名规范请参看 veImageX 存储 Key 通用字符规则。 
            Prefix ( String ): 否  指定的上传文件路径。指定 Prefix 时，下发的存储 Key 为：Prefix/{随机Key}.{FileExtension}，拼接形成的存储 Key 需满足 veImageX 存储 Key 通用字符规则。 
                  仅当未指定 StoreKeys 时生效。 
            FileExtension ( String ): 否  文件扩展名，最大长度限制为 8 个字节。 
                  仅当未指定 StoreKeys 时生效。 
            ContentType ( String ): 否  上传文件的 Content-Type 值。 
                  需确保指定值在服务维度的白名单内，否则无法成功上传，参看上传 Content-Type 限制。 
            StorageClass ( String ): 否  存储类型。 
                  - STANDARD：标准存储 
                  - IA：低频存储 
                  - ARCHIVE_FR：归档闪回存储 
                  - ARCHIVE：归档存储 
                  - COLD_ARCHIVE：冷归档存储 
            FileSize ( Long ): 否  文件大小。 
            PartSize ( Long ): 否  分片大小，单位为字节，默认值为 200 MB。 
                  当 FileSize 大于 PartSize 时，下发分片上传的 URL。 
            Overwrite ( Boolean ): 否  是否开启重名文件覆盖上传，取值如下所示： 
                  - true：开启 
                  - false：（默认）关闭 
                  在指定 Overwrite 为 true 前，请确保您指定的 ServiceId 对应服务已开启了覆盖上传能力。 
    """,
    "get_image_ai_details": r""" 
   Args: 
       params: A JSON structure
            QueueId ( String ): 是  队列 ID，通过 CreateImageAITask 接口返回。 
            TaskId ( String ): 是  任务 ID，通过 CreateImageAITask 接口返回，缺省时查询指定队列下全部的任务。 
            StartTime ( Long ): 是  查询的起始 Unix 时间戳，StartTime 与 EndTime 时间间隔最大不超过 7 天。 
            EndTime ( Long ): 是  查询的结束 Unix 时间戳，StartTime 与 EndTime 时间间隔最大不超过 7 天。 
            Status ( String ): 否  执行状态，填入多个时使用英文逗号分隔。取值如下所示： 
                  - Pending：排队中 
                  - Running：执行中 
                  - Success：执行成功 
                  - Fail：执行失败 
            SearchPtn ( String ): 否  返回图片 URL 或 URI 中包含该值的任务。默认为空，不传则返回所有任务。 
            Limit ( Long ): 是  分页条数，取值范围为 (0, 100]。 
            Offset ( Long ): 否  分页偏移量，默认为 0。取值为 1 时，表示跳过第一条数据，从第二条数据取值。 
            ServiceId ( String ): 是  服务 ID。若 DataType 取值 uri，则提交的图片 URI 列表需在该服务内。 
                  - 您可以在 veImageX 控制台服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
    """,
    "get_image_ai_tasks": r""" 
   Args: 
       params: A JSON structure
            ServiceId ( String ): 是  服务 ID。 
                  - 您可以在 veImageX 控制台 服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考获取所有服务信息。 
            QueueId ( String ): 是  队列 ID，通过 CreateImageAITask 接口返回。 
            TaskId ( String ): 否  任务 ID，通过 CreateImageAITask 接口返回，缺省时查询指定队列下全部的任务。 
            Marker ( String ): 否  上一次查询返回的位置标记，作为本次查询的起点信息，默认值为空。 
            Limit ( Long ): 否  单次查询列出的任务的个数，取值范围为 (0,1000]，默认值为 1000。 
            Status ( String ): 否  指定查询的任务状态，缺省时将查询全部状态的任务。取值如下所示： 
                  - Running：任务运行中 
                  - Suspend：任务中断 
                  - Done：任务已完成 
                  - Cancel：任务取消 
                  - Failed：任务失败 
            StartTime ( Long ): 是  查询的起始 Unix 时间戳，StartTime 与 EndTime 时间间隔最大不超过 7 天。 
            EndTime ( Long ): 是  查询的结束 Unix 时间戳，StartTime 与 EndTime 时间间隔最大不超过 7 天。 
    """,
    "describe_image_x_storage_usage": r""" 
   Args: 
       params: A JSON structure
            ServiceIds ( String ): 否  服务 ID。为空时表示不筛选，支持查询多个服务，使用逗号分隔不同的服务。 
                  - 您可以在 veImageX 控制台服务管理页面，在创建好的图片服务中获取服务 ID。 
                  - 您也可以通过 OpenAPI 的方式获取服务 ID，具体请参考 GetAllImageServices。 
            BucketNames ( String ): 否  Bucket 名称。支持同时查询多个 BucketName，不同的 BucketNmae 使用逗号分隔。 
                  您可以通过调用 GetAllImageServices 获取所需的 Bucket 名称。 
            GroupBy ( String ): 否  需要分组查询的参数，多个数据用逗号分隔。支持取值如下： 
                  - ServiceId：服务 ID 
                  - BucketName：Bucket 名称 
                  - StorageType：存储类型 
            StartTime ( String ): 是  获取数据起始时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm。例如2019-06-02T00:00:00+08:00。 
                  由于仅支持查询近一年历史数据，则若此刻时间为2011-11-21T16:14:00+08:00，那么您可输入最早的开始时间为2010-11-21T00:00:00+08:00。 
            EndTime ( String ): 是  获取数据结束时间点。日期格式按照 ISO8601 表示法，格式为：YYYY-MM-DDThh:mm:ss±hh:mm。例如2019-06-02T00:00:00+08:00。 
            Interval ( String ): 是  查询数据的时间粒度。单位为秒，缺省时查询StartTime和EndTime时间段全部数据，此时单次查询最大时间跨度为 93 天。支持以下取值： 
                  - 300：单次查询最大时间跨度为 31 天 
                  - 3600：单次查询最大时间跨度为 93 天 
                  - 86400：单次查询最大时间跨度为 93 天 
            IsRetrieval ( Boolean ): 否  是否查询数据取回量。 
                  - true：查询取回量。 
                  - false：查询存储量。 
    """,
}
