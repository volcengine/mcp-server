note = {
    "check_fee": r""" 
    Args: 
        params: A JSON structure
             domain ( String ): 是  域名, 例如: baidu.com 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        domain ( String ):  
        domain_type ( String ):  
        is_limit_domain ( Boolean ):  
        new_price ( String ):  
        notice_info ( String ):  
        price_type ( String ):  
        renew_price ( String ):  
        restore_price ( String ):  
        status ( String ):  
        zone ( String ):  
    """,
    "get_domain": r""" 
    Args: 
        params: A JSON structure
             domain ( String ): 否  域名 
             instance_no ( String ): 否  域名绑定的费用实例ID 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        account_id ( String ):  
        address ( String ):  
        address_zh ( String ):  
        city ( String ):  
        city_zh ( String ):  
        country_code ( String ):  
        created_at ( Integer ):  
        domain ( String ):  
        domain_name_audit_status ( String ):  
        email ( String ):  
        expired_time ( Integer ):  
        instance_no ( String ):  
        is_auto_renew ( Boolean ):  
        is_transfer_prohibited ( Boolean ):  
        is_update_prohibited ( Boolean ):  
        ns_list ( String ):  
        post_code ( String ):  
        register_time ( Integer ):  
        registrant ( String ):  
        registrant_fn ( String ):  
        registrant_fn_zh ( String ):  
        registrant_ln ( String ):  
        registrant_ln_zh ( String ):  
        registrant_zh ( String ):  
        state ( String ):  
        state_zh ( String ):  
        status ( String ):  
        status_notice ( String ):  
        template_tag ( String ):  
        updated_at ( Integer ):  
        user_id ( String ):  
        verify_status ( String ):  
        zone ( String ):  
    """,
    "get_async_task": r""" 
    Args: 
        params: A JSON structure
             task_no ( String ): 是  异步任务id 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        account_id ( String ):  
        annotation ( String ):  
        created_at ( Integer ):  
        instance_no ( String ):  
        price ( String ):  
        resource ( String ):  
        retry_count ( Integer ):  
        status ( String ):  
        task_no ( String ):  
        task_type ( String ):  
        updated_at ( Integer ):  
        user_id ( String ):  
    """,
    "get_template": r""" 
    Args: 
        params: A JSON structure
             tag ( String ): 是  模板tag 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        address ( String ):  
        address_zh ( String ):  
        city ( String ):  
        city_zh ( String ):  
        country_code ( String ):  
        created_at ( Integer ):  
        email ( String ):  
        id_code ( String ):  
        id_type ( String ):  
        post_code ( String ):  
        registrant ( String ):  
        registrant_fn ( String ):  
        registrant_fn_zh ( String ):  
        registrant_ln ( String ):  
        registrant_ln_zh ( String ):  
        registrant_zh ( String ):  
        registration_type ( String ):  
        state ( String ):  
        state_zh ( String ):  
        status ( String ):  
        status_notice ( String ): 身份信息与证件不符 
        tag ( String ):  
        tel_area_code ( String ):  
        tel_country_code ( String ):  
        tel_extension ( String ):  
        tel_number ( String ):  
        updated_at ( Integer ):  
    """,
    "list_domains": r""" 
    Args: 
        params: A JSON structure
             domain ( String ): 否  域名 
             status ( String ): 否  域名状态 多个状态逗号隔开.(normal正常 registrant_change过户中 expired已过期 redemption赎回期 wasted已废弃 transfer_out已转出 redeeming赎回中 registrant_changing持有人信息修改中) 
             verify_status ( String ): 否  实名状态 多个状态逗号隔开 (not_validation未实名 pending_validation实名中 verification_success实名成功 verification_failed实名失败) 
             expired_after ( Integer ): 否  将在{days}过期的域名 
             is_auto_renew ( Boolean ): 否  是否自动续费 
             domain_name_audit_status ( String ): 否  命名审核状态 多个状态逗号隔开 (auditing命名审核中 audit_pass命名审核通过 audit_unPass命名审核未通过) 
             order_by ( String ): 否  按{x}排序(register_time/expired_time) 
             asc_or_desc ( String ): 否  升序or降序(ASC/DESC) 
             page_number ( Integer ): 否  分页-页码 
             page_size ( Integer ): 否  分页-每页大小 最大50,默认10个 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        domain_info_list ( Array of DomainInfo ):  
        total ( Integer ):  
       "字段"： DomainInfo
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        zone ( String ):  
        domain ( String ):  
        status ( String ):  
        ns_list ( String ):  
        user_id ( String ):  
        account_id ( String ):  
        created_at ( Integer ):  
        updated_at ( Integer ):  
        instance_no ( String ):  
        expired_time ( Integer ):  
        template_tag ( String ):  
        is_auto_renew ( Boolean ):  
        register_time ( Integer ):  
        status_notice ( String ):  
        verify_status ( String ):  
        is_update_prohibited ( Boolean ):  
        is_transfer_prohibited ( Boolean ):  
        domain_name_audit_status ( String ):  
    """,
    "list_templates": r""" 
    Args: 
        params: A JSON structure
             registrant_zh ( String ): 否  持有人名称(中文), 模糊搜索 
             registration_type ( String ): 否  注册类型.(C企业 P个人) 
             tag ( String ): 否  模板tag 
             status ( String ): 否  模板状态 多个状态逗号隔开 (not_validation未实名 pending_validation实名中 verification_success实名成功 verification_failed实名失败) 
             page_number ( Integer ): 否  分页-页码 
             page_size ( Integer ): 否  分页-每页大小 最大50,默认10个 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        template_info_list ( Array of TemplateInfo ):  
        total ( Integer ):  
       "字段"： TemplateInfo
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        tag ( String ):  
        city ( String ):  
        email ( String ):  
        state ( String ):  
        status ( String ):  
        address ( String ):  
        city_zh ( String ):  
        id_code ( String ):  
        id_type ( String ):  
        state_zh ( String ):  
        post_code ( String ):  
        address_zh ( String ):  
        created_at ( Integer ):  
        registrant ( String ):  
        tel_number ( String ):  
        updated_at ( Integer ):  
        country_code ( String ):  
        registrant_fn ( String ):  
        registrant_ln ( String ):  
        registrant_zh ( String ):  
        status_notice ( String ): 身份信息与证件不符 
        tel_area_code ( String ):  
        tel_extension ( String ):  
        registrant_fn_zh ( String ):  
        registrant_ln_zh ( String ):  
        tel_country_code ( String ):  
        registration_type ( String ):  
    """,
    "register_domain": r""" 
    Args: 
        body: A JSON structure
             domain ( String ): 是  域名 
             template_tag ( String ): 是  模板tag 
             period ( Integer ): 否  注册年限，默认1年，不能超过10年，使用资源包时只能注册1年 
             ns_list ( Array of String ): 否  ns列表，如果为空默认使用火山的ns，提供的ns必须已经在注册商注册过 
             is_auto_renew ( Boolean ): 否  是否开启自动续费，开启后会在域名过期前7天尝试自动续费 
             package_id ( String ): 否  资源包ID，如果使用资源包需要提供购买资源包ID 
   Returns: 
        参数 ( 类型 ): 示例值 
        ---- ( ---- ): ---- 
        task_no ( String ):  
    """,
}
