note = {
    "create_namespace": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Registry ( String ): 是  指定的镜像仓库实例名称。通过 ListRegistries 或在 镜像仓库控制台 的 实例列表 页面获取。 
             Name ( String ): 是  命名空间名称。支持小写英文、数字、英文句号（.）、短划线（-）、下划线（_），标点符号不能出现在首位或末位，也不能连续输入。长度限制为 2～90 个字符。 
                   - 标准版实例：同一个镜像仓库实例下，名称必须唯一。 
                   - 体验版实例：同一地域下，所有火山引擎账号范围内的命名空间名称需要保持唯一。如果您设置的命名空间名称已被占用，请尝试其他名称或者 购买标准版实例 。 
             ClientToken ( String ): 否  用于保证请求幂等性的字符串。该字符串由调用方传入，需保证不同请求之间唯一。ClientToken 对大小写敏感，且最大值不超过 64 个 ASCII 字符。 
             Project ( String ): 否  命名空间所属项目的名称。参数值大小写敏感，不得超过 64 个字符。参数为空时，命名空间关联默认的 default 项目。 
             RepositoryDefaultAccessLevel ( String ): 否  命名空间下新建 OCI 制品仓库的默认公开属性，默认 Private。公开属性支持后续变更。 
                   - Public：公开，不需要访问密钥，支持直接访问。 
                   - Private：私有，需要输入访问密钥后才能够访问。 
    """,
    "get_authorization_token": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Registry ( String ): 是  镜像仓库实例的名称。在 镜像仓库控制台 的 实例列表 页面，获取实例名称。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Token ( String ): 临时访问密钥。 
        Username ( String ): 登录镜像仓库实例的用户名。 
        ExpireTime ( String ): 临时访问密钥的过期时间，RFC3339 格式的 UTC+0 时间。 
    """,
    "list_domains": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Registry ( String ): 是  要查询域名的镜像仓库实例名称。 
             PageSize ( Long ): 否  单页展示的域名信息数量，默认为 10 个，取值范围为 [1,100] 的整数。 
             PageNumber ( Long ): 否  开始显示返回结果的页码，从 1 开始，默认为 1，取值范围为 [1,2147483647] 的整数。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Registry ( String ): 镜像仓库实例名称。 
        TotalCount ( Long ): 域名总数。 
        PageNumber ( Long ): 当前页码。 
        PageSize ( Long ): 单页显示的域名信息条数。 
        Items ( Array of Domain ): 镜像仓库实例域名列表。 
       "字段"： Domain
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Domain ( String ): 镜像仓库域名： 
            - 体验版实例域名： 
            	- 存量实例：cr-cn-beijing.volces.com 
            	- 升级后的实例：[实例名]-[地域].cr.volces.com 
            - 其他版本实例域名：[实例名]-[地域].cr.volces.com 
        Type ( String ): 域名类型： 
            - System ：系统提供的域名。 
            - Volcengine：火山引擎域名。 
            - ThirdParty：第三方域名。 
        CreateTime ( String ): 域名创建的时间，使用 RFC 3339 格式。 
        Default ( Boolean ): 该域名是否为镜像仓库系统域名。 
            - true：默认域名。 
            - false：不是默认域名。 
    """,
    "list_tags": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Registry ( String ): 是  指定 OCI 制品仓库所属的镜像仓库实例名称。在 镜像仓库控制台 的 实例列表 页面，获取实例名称。 
             Namespace ( String ): 是  指定 OCI 制品仓库所属的命名空间名称。在 镜像仓库控制台 目标实例的 命名空间 页面，获取命名空间名称。 
             Repository ( String ): 是  指定 OCI 制品仓库名称。在 镜像仓库控制台 目标实例的 OCI制品仓库 页面，获取 OCI 制品仓库名称。 
             Filter ( Object of TagFilter ): 否  查询 OCI 制品版本的过滤条件。 
             PageSize ( Long ): 否  单页展示的 OCI 制品版本数量，默认为 10 个，取值范围为 [1,100] 的整数。 
             PageNumber ( Long ): 否  开始显示返回结果的页码，从 1 开始，默认为 1。取值范围为 [1,2147483647] 的整数。 
             SortBy ( String ): 否  搜索制品版本的排序条件 
            "字段"： TagFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Names ( Array of String ): 否  指定 Tag，支持精确匹配和模糊匹配，模糊匹配仅支持使用 * 号作为通配符，最多 20 个。 
             Types ( Array of String ): 否  OCI 制品 Tag 类型，取值如下： 
                   - Image：该 Tag 对应一个容器镜像。 
                   - Chart：该 Tag 对应一个 Helm Chart。 
                   单次可填写一个或多个Tag 类型。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Registry ( String ): 指定 OCI 制品仓库所属的镜像仓库实例名称。 
        TotalCount ( Long ): 查询到的 OCI 制品版本总数。 
        Namespace ( String ): 指定 OCI 制品仓库所属的命名空间名称。 
        Repository ( String ): 指定 OCI 制品仓库名称。 
        Items ( Array of Tag ): OCI 制品版本列表。详细信息，请参见 Tag。 
        PageNumber ( Long ): 当前页码。 
        PageSize ( Long ): 单页显示的 OCI 制品版本信息条数。 
       "字段"： Tag
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Name ( String ): OCI 制品版本（Tag）名称。 
        Type ( String ): OCI 制品 Tag 类型： 
            - Image：该 Tag 对应一个容器镜像。 
            - Chart：该 Tag 对应一个 Helm Chart。 
        Digest ( String ): OCI 制品摘要，SHA256 值。 
        PushTime ( String ): OCI 制品最近一次推送的时间。RFC3339 格式的 UTC+0 时间。 
        Size ( Long ): OCI 制品大小，单位为 Byte。 
        ImageAttributes ( Array of ImageAttribute ): Tag 类型为 Image 时的相关属性。 
        ChartAttribute ( Object of ChartAttribute ): Tag 类型为 Chart 时的相关属性。 
        PullTime ( String ): OCI 制品最近一次拉取的时间（按照客户端调用oci v2 Get manifests接口时间计算）。RFC3339 格式的 UTC+0 时间。 
       "字段"： ImageAttribute
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Author ( String ): 镜像的创建者，即上传该镜像到镜像仓库的火山引擎账号。 
        Architecture ( String ): 镜像架构。 
        Os ( String ): 镜像支持的操作系统。 
        Digest ( String ): 镜像摘要，SHA256 值。 
        Size ( Long ): 镜像大小 
       "字段"： ChartAttribute
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        ApiVersion ( String ): Helm 版本。 
        Name ( String ): Helm Chart 名称。 
    """,
    "create_repository": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Registry ( String ): 是  指定命名空间所属的镜像仓库实例名称。在 镜像仓库控制台 的 实例列表 页面，获取实例名称。 
             Namespace ( String ): 是  目标命名空间名称。在 镜像仓库控制台 目标实例的 命名空间 页面，获取命名空间名称。 
             Name ( String ): 是  OCI 制品仓库名称。同一个命名空间下，名称必须唯一。支持小写英文、数字、分隔符（分隔符可输入一个.或/、一个或多个-、一个或两个_，且分隔符不能出现在首位或末位，不能连续出现），长度限制为 1～128 个字符。 
             Description ( String ): 否  OCI 制品仓库描述信息。长度不超过 300 个字符。 
             AccessLevel ( String ): 否  OCI 制品仓库的类型。 
                   - Public：拥有全读写权限的子用户可推送或拉取镜像，其他用户可匿名拉取镜像。 
                   - Private：拥有全读写权限的子用户可推送或拉取镜像 ，拥有只读权限的子用户可拉取镜像。 
                   默认值为 Private。 
             ClientToken ( String ): 否  用于保证请求幂等性的字符串。该字符串由调用方传入，需保证不同请求之间唯一。ClientToken 对大小写敏感，且最大值不超过 64 个 ASCII 字符。 
    """,
    "list_repositories": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Registry ( String ): 是  指定镜像仓库实例名称。在 镜像仓库控制台 的 实例列表 页面，获取实例名称。 
             Filter ( Object of RepositoryFilter ): 否  查询 OCI 制品的过滤条件。 
             PageSize ( Long ): 否  单页展示的 OCI 制品仓库数量，默认为 10 个，取值范围为 [1,100] 的整数。 
             PageNumber ( Long ): 否  开始显示返回结果的页码，从 1 开始，默认为 1，取值范围为 [1,2147483647] 的整数。 
            "字段"： RepositoryFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Namespaces ( Array of String ): 否  指定 OCI 制品仓库所属的命名空间。在 镜像仓库控制台 目标实例的 命名空间 页面，获取命名空间名称。 
                   支持精确匹配和模糊匹配，模糊匹配仅支持使用星号（*）作为通配符。单次最多填写 20 个命名空间名称。 
             Names ( Array of String ): 否  指定 OCI 制品仓库名称。在 镜像仓库控制台 目标实例的 OCI制品仓库 页面，获取 OCI 制品仓库名称。 
                   支持精确匹配和模糊匹配，模糊匹配仅支持使用星号（*）作为通配符。单次最多填写 20 个 OCI 制品仓库名称。 
             AccessLevels ( Array of String ): 否  访问等级，取值如下： 
                   - Private：私有类型 OCI 制品仓库，只能被有权限的用户访问。 
                   - Public：公有类型 OCI 制品仓库，可以被所有用户访问。 
                   单次可填写一个或多个访问等级。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Registry ( String ): 镜像仓库实例 
        TotalCount ( Long ): 镜像实例总数 
        Items ( Array of Repository ): OCI 制品仓库列表。详细信息，请参见 Repository。 
        PageSize ( Long ): 单页显示的 OCI 制品仓库信息条数。 
        PageNumber ( Long ): 当前页码。 
       "字段"： Repository
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Namespace ( String ): 命名空间名称。 
        Name ( String ): OCI 制品仓库名称。 
        AccessLevel ( String ): 访问等级： 
            - Private：私有类型 OCI 制品仓库，访问时需要访问密钥。 
            - Public：公有类型 OCI 制品仓库，支持通过访问地址直接访问。 
        Description ( String ): 镜像仓库描述，描述长度为 0~300 个 UTF-8 字符。 
        CreateTime ( String ): 创建 OCI 制品仓库的时间。RFC3339 格式的 UTC+0 时间。 
        UpdateTime ( String ): 最近一次更新 OCI 制品仓库的时间。RFC3339 格式的 UTC+0 时间。 
    """,
    "list_namespaces": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Registry ( String ): 是  指定的镜像仓库实例名称。在 镜像仓库控制台 的 实例列表 页面，获取实例名称。 
             Filter ( Object of NamespaceFilter ): 否  待查询命名空间的过滤条件。 
             PageSize ( Long ): 否  单页展示的命名空间数量，默认为 10 个，取值范围为 [1,100] 的整数。 
             PageNumber ( Long ): 否  开始显示返回结果的页码，从 1 开始，默认为 1，取值范围为 [1,2147483647] 的整数。 
            "字段"： NamespaceFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Names ( Array of String ): 否  指定命名空间名称。在 镜像仓库控制台 目标实例的 命名空间 页面，获取命名空间名称。 
                   支持精确匹配和模糊匹配，模糊匹配仅支持使用星号（*）作为通配符。单次最多填写 20 个命名空间名称。 
             Projects ( Array of String ): 否  筛选用户所属的项目，让 inProject 为 true 时读取这个参数进行筛选 
             InProject ( Boolean ): 否  筛选 namespace 是否在项目中，如设定为 true，则返回项目中的 namespace，Projects 参数生效 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Registry ( String ): 指定镜像仓库实例名称。 
        TotalCount ( Long ): 查询到的命名空间数量。 
        PageNumber ( Long ): 当前页码。 
        PageSize ( Long ): 单页显示的命名空间信息条数。 
        Items ( Array of Namespace ): 命名空间列表，详情请参见 Namespace。 
       "字段"： Namespace
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Name ( String ): 命名空间名称。 
        Project ( String ): Namespace 所属项目的名称。该参数为空时，表示创建的 Namespace 不属于任何项目。 
        CreateTime ( String ): 创建命名空间的时间。RFC3339 格式的 UTC+0 时间。 
        RepositoryDefaultAccessLevel ( String ): 命名空间下 OCI 制品仓库的默认公开属性。 
            - Public：公开，不需要访问密钥，支持直接访问。 
            - Private：私有，需要输入访问密钥后才能够访问。 
    """,
    "create_registry": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Name ( String ): 是  标准版实例名称，同一个地域下，名称必须唯一。支持小写英文字母、数字、短划线（-）且数字不能在首位，短划线（-）不能在首位或末位，长度限制为 3～30 个字符。 
             Type ( String ): 否  不填写默认创建标准版实例。 
                   - Enterprise：标准版 
                   - Micro：小微版 
             Project ( String ): 否  填写实例需要关联的项目。一个实例仅支持关联一个项目。 
             ResourceTags ( Array of ResourceTag ): 否  支持通过键值对，自定义实例的标签。支持在 分账账单 中基于实例标签查看账单信息，详情说明参见 分账账单。 
             ClientToken ( String ): 否  用于保证请求幂等性的字符串。该字符串由调用方传入，需保证不同请求之间唯一。ClientToken 对大小写敏感，且最大值不超过 64 个 ASCII 字符。 
             ProxyCacheEnabled ( Boolean ): 否  是否为远端代理仓。 
             ProxyCache ( Object of ProxyCacheSpec ): 否  远端代理仓配置，创建远端代理仓时必填。 
            "字段"： ResourceTag
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Key ( String ): 是  标签的 Key 值。 
             Value ( String ): 是  标签的 Value 值列表。 
            "字段"： ProxyCacheSpec
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Type ( String ): 是  远端代理仓支持的类型。 
                   - DockerHub：Docker Hub 类型的远端代理仓，支持在大陆地区拉取 Docker Hub 中镜像。 
                   - DockerRegistry：通用类型的远端代理仓，可以支持多云场景中主备仓需求。 
             Endpoint ( String ): 否  源镜像的访问地址。 
                   - DockerHub 类型：访问地址固定为 https://hub.docker.com。 
                   - DockerHub 以外的类型：需要指定具体的访问地址。 
             Password ( String ): 否  访问源镜像所需的用户名或者 SecretAccessKey。 
             Username ( String ): 否  访问源镜像所需的密码或者 AccessKeyID。 
             SkipSSLVerify ( Boolean ): 否  是否忽略 SSL 证书验证。 
    """,
    "list_registries": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Filter ( Object of RegistryFilter ): 否  待查询镜像仓库实例的过滤条件。 
             ResourceTagFilters ( Array of ResourceTagFilter ): 否  查询镜像仓库实例标签的过滤条件。 
             PageSize ( Long ): 否  单页展示的镜像仓库实例数量，默认为 10 个，取值范围为 [1,100] 的整数。 
             PageNumber ( Long ): 否  开始显示返回结果的页码，从 1 开始，默认为 1，取值范围为 [1,2147483647] 的整数。 
            "字段"： RegistryFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Names ( Array of String ): 否  指定镜像仓库实例或远端代理仓名称。在 镜像仓库控制台 的 实例列表 或 远端代理 页面，获取实例或远端代理仓的名称。 
                   支持精确匹配和模糊匹配，模糊匹配仅支持使用星号（*）作为通配符。单次最多填写 20 个实例或远端代理仓名称。 
             Types ( Array of String ): 否  镜像仓库实例类型。取值如下： 
                   - Basic：基础版实例。 
                   - Trial：体验版实例。 
                   - Enterprise：标准版实例。 
                   - Micro：小微版实例。 
                   可填写一个或多个实例类型。 
             Projects ( Array of String ): 否  关联的项目名称。 
             Statuses ( Array of StatusFilter ): 否  镜像仓库实例的状态，单次调用最多可填写 10 个 StatusFilter 组合。 
            "字段"： ResourceTagFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Key ( String ): 是  标签的 Key 值。 
             Values ( Array of String ): 是  标签的 Value 值。 
            "字段"： StatusFilter
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             Phase ( String ): 否  实例状态（Status）由 Phase 和 Conditions 组成。 
                   - Creating, [ Progressing ] ：创建中。 
                   - Running, [ Ok ] ：运行中。 
                   - Running, [ Degraded ] ：运行中。 
                   - Stopped, [ Balance ] ： 欠费关停。 
                   - Stopped, [ Released ] ：待回收。 
                   - Stopped, [ Released, Balance ] ：欠费关停。 
                   - Starting, [ Progressing ] ：启动中。 
                   - Deleting, [ Progressing ] ：销毁中。 
                   - Failed, [ Unknown ] ：异常。 
             Condition ( String ): 否  实例状态（Status）由 Phase 和 Conditions 组成。 
                   Creating, [ Progressing ] ：创建中。 
                   Running, [ Ok ] ：运行中。 
                   Running, [ Degraded ] ：运行中。 
                   Stopped, [ Balance ] ： 欠费关停。 
                   Stopped, [ Released ] ：待回收。 
                   Stopped, [ Released, Balance ] ：欠费关停。 
                   Starting, [ Progressing ] ：启动中。 
                   Deleting, [ Progressing ] ：销毁中。 
                   Failed, [ Unknown ] ：异常。 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        TotalCount ( Long ): 查询到的镜像仓库实例数量。 
        PageNumber ( Long ): 当前页码。 
        PageSize ( Long ): 单页显示的镜像仓库实例信息条数。 
        Items ( Array of Registry ): 镜像仓库实例列表。 
       "字段"： Registry
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Name ( String ): 镜像仓库实例名称。 
        Type ( String ): 镜像仓库实例类型，参数值说明如下： 
            - Basic：基础版实例。仅部分历史版本用户支持使用，不支持在控制台查看。 
            - Trial：体验版实例。 
            - Enterprise：标准版实例。 
            - Micro：小微版实例。 
        ChargeType ( String ): 镜像仓库实例的付费类型，目前仅支持 PostCharge 按量付费模式。 
        Status ( Object of RegistryStatus ): 镜像仓库实例状态，由 Phase 和 Conditions 组成。 
            合法的 Phase 和 Conditions 组合如下所示： 
            - {Creating, [Progressing]}：创建中 
            - {Running, [Ok]}：运行中 
            - {Running, [Degraded]}：运行中 
            - {Stopped, [Balance]}：欠费关停 
            - {Stopped, [Released]}：待回收 
            - {Stopped, [Released, Balance]}：欠费关停 
            - {Starting, [Progressing]}：启动中 
            - {Deleting, [Progressing]}：销毁中 
            - {Failed, [Unknown]}：异常 
        Project ( String ): 填写实例需要关联的项目。一个实例仅支持关联一个项目。 
        ResourceTags ( Array of ResourceTag ): 支持通过键值对，自定义实例的标签。支持在 分账账单 中基于实例标签查看账单信息，详情说明参见 分账账单。 
        CreateTime ( String ): 创建镜像仓库实例的时间。RFC3339 格式的 UTC+0 时间。 
        ExpireTime ( String ): 实例或远端代理仓到期时间。仅计费类型为 HybridCharge 混合计费时存在返回值。 
        RenewType ( String ): 实例或远端代理仓到期时间。仅计费类型为 HybridCharge 混合计费时存在返回值。 
        ProxyCache ( Object of ProxyCache ): 远端代理仓配置说明。 
        ProxyCacheEnabled ( Boolean ): 是否为远端代理仓。 
       "字段"： RegistryStatus
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Phase ( String ): 镜像仓库实例状态，参数值如下： 
            - Creating 
            - Running 
            - Stopped 
            - Starting 
            - Deleting 
            - Failed 
        Conditions ( Array of String ): 镜像仓库实例进入当前状态下的条件、即进入该状态的原因等，可以有多个原因。参数值如下： 
            - Ok 
            - Progressing 
            - Degraded 
            - Balance 
            - Released 
            - Unknown 
       "字段"： ResourceTag
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Key ( String ): 标签的 Key 值。 
        Value ( String ): 标签的 Value 值列表。 
       "字段"： ProxyCache
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Type ( String ): 远端代理仓支持的类型。 
            - DockerHub：Docker Hub 类型的远端代理仓，支持在大陆地区拉取 Docker Hub 中镜像。 
            - DockerRegistry：通用类型的远端代理仓，可以支持多云场景中主备仓需求。 
    """,
}
