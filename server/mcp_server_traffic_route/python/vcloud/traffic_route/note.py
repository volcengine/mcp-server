note = {
    "list_zones": r""" 
    Args: 
        body: A JSON structure
            key ( String ): 否  搜索关键词。 
            searchMode ( String ): 否  如果值为 like，则为模糊匹配；如果值为 exact，则为精确匹配。 
    """,
    "create_zone": r""" 
    Args: 
        body: A JSON structure
            zoneName ( String ): 是  域名。 
    """,
    "create_record": r""" 
    Args: 
        body: A JSON structure
            ZID ( String ): 是  关联的域名 ID。
            Host ( String ): 是  主机名。
            Type ( String ): 是  解析记录类型。
            Value ( String ): 是  解析记录值。
            TTL ( Long ): 否  生存时间，单位为秒。默认值为 600。
            Weight ( Float ): 否  权重。默认值为 1。
    """,
    "list_records": r""" 
        body: A JSON structure
            ZID ( String ): 是  关联的域名 ID。
    """,
}
