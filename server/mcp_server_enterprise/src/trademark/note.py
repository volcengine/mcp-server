note = {
    "get_applicant": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             ApplicantID ( String ): 是  商标申请人的 id 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Reason ( String ): 失败原因 
        Status ( String ): 申请人状态 
        UserID ( String ): 火山子账号 
        Address ( String ): 申请人证件地址 
        Contact ( Object of Contact ): 联系人信息 
        Country ( String ): 国家 
        Document ( Object of Document ): 申请人材料 
        IDNumber ( String ): 身份证ID 
        Postcode ( String ): 申请人邮政编码 
        Province ( String ): 省份 
        AccountID ( String ): 火山账号 
        EnAddress ( String ): 申请人英文证件地址 
        CreditCode ( String ): 统一社会信用代码 
        ApplicantID ( String ): 申请人ID 
        ApplicantName ( String ): 申请人名称 
        ApplicantType ( String ): 申请人类型 
        EnApplicantName ( String ): 申请人英文名称 
       "字段"： Contact
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Email ( String ): 联系人邮箱 
        Phone ( String ): 联系人电话 
        ContactAddr ( String ): 联系人住址 
        ContactName ( String ): 联系人姓名 
        ContactPostcode ( String ): 联系人邮政编码 
       "字段"： Document
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        POAImg ( String ): 委托书图片 
        IDCardImg ( String ): 个人身份证或护照图片 
        POAReuseImg ( String ): 委托书复用声明图片 
        PersonEvidenceImg ( String ): 个人中英文证明图片 
        BusinessLicenseImg ( String ): 营业执照图片 
        BusinessEvidenceImg ( String ): 企业中英文证明图片 
    """,
    "get_trademark": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             TrademarkID ( String ): 是  商标ID 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        UserID ( String ): 火山子账号 
        AccountID ( String ): 火山账号 
        Applicant ( Object of TrademarkApplicant ): 申请人信息 
        Trademark ( Object of TrademarkInfo ): 商标信息 
       "字段"： TrademarkApplicant
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Reason ( String ): 失败原因 
        Status ( String ): 商标申请人状态 
        Address ( String ): 申请人证件地址 
        Contact ( Object of TrademarkContact ): 联系人信息 
        Country ( String ): 国家或地区 
        Document ( Object of TrademarkApplicantDocument ): 申请人文档材料 
        IDNumber ( String ): 申请人身份ID 
        Postcode ( String ): 证件地址邮政编码 
        Province ( String ): 省份 
        EnAddress ( String ): 申请人证件英文地址 
        CreditCode ( String ): 统一社会信用代码 
        ApplicantID ( String ): 申请人ID 
        ApplicantName ( String ): 申请人名称 
        ApplicantType ( String ): 申请人类型 
        EnApplicantName ( String ): 申请人英文名称 
       "字段"： TrademarkInfo
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Name ( String ): 商标名称 
        Risk ( Object of Risk ): 风险评估 
        Price ( Float ): 商标价格 
        Holder ( String ): 障碍商标申请人 
        POAImg ( String ): 委托书图片 
        Reason ( String ): 失败原因 
        Status ( String ): 商标状态 
        ClassID ( String ): 商标类别 
        Comment ( String ): 备注 
        POAType ( Integer ): 商标委托书使用类型 
             0 未使用 
             1 使用申请人模板 
             2 单次上传使用 
        Pattern ( String ): 商标图样 
        Portrait ( String ): 肖像姓名授权书 
        ClassInfo ( Array of String ): 商标类别内容 
        CreateTime ( String ): 需求提交时间 
        FilingDate ( String ): 递交商标局日期 
        UpdateTime ( String ): 更新时间 
        Description ( String ): 商标说明 
        PatternMode ( String ): 商标图样模式 
        ProgressBar ( Array of ProgressBar ): 商标申请流程进度条 
        TrademarkID ( String ): 商标ID 
        StatusExpired ( Integer ): 商标状态是否过期 
        TrademarkType ( String ): 商标类型 
        ProgressContent ( Array of ProgressContent ): 商标申请流程进展内容 
        RequirementType ( String ): 需求类型 
        RegistrationNumber ( String ): 商标注册号 
       "字段"： TrademarkContact
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Email ( String ): 联系人邮箱 
        Phone ( String ): 联系人手机 
        ContactAddr ( String ): 联系人地址 
        ContactName ( String ): 联系人名称 
        ContactPostcode ( String ): 联系人邮编 
       "字段"： TrademarkApplicantDocument
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        POAImg ( String ): 商标委托书图片 
        IDCardImg ( String ): 个人身份证或护照图片 
        POAReuseImg ( String ): 商标委托书复用声明图片 
        PersonEvidenceImg ( String ): 个人中英文证明图片 
        BusinessLicenseImg ( String ): 营业执照图片 
        BusinessEvidenceImg ( String ): 企业中英文证明图片 
       "字段"： Risk
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        End ( String ): 风险评估结束内容 
        Class ( Array of RiskCLass ): 风险类别 
        Start ( String ): 风险评估开始内容 
       "字段"： ProgressBar
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Done ( Boolean ): 进度是否已完成 
        Progress ( String ): 进度环节 
        TimeSpent ( String ): 用时 
       "字段"： ProgressContent
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Time ( String ): 发生时间 
        Content ( String ): 进展内容 
       "字段"： RiskCLass
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        ClassID ( String ): 商标类别id 
        ClassName ( String ): 商标类别名称 
        RegistrationNumber ( String ): 商标注册号 
    """,
    "list_applicants": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             ApplicantType ( String ): 否  商标申请人的类型，默认获取所有类型的申请人，Business 企业, Individual 个体工商, Person 个人 
             ApplicantName ( String ): 否  商标申请人名称 
             Status ( String ): 否  申请人状态，多个状态用英文逗号,隔开，LackOfMaterials 待补充材料,Ready 待使用,CreateFailed 创建失败 
             Country ( String ): 否  国家或地区，支持模糊搜索 
             PageNumber ( Integer ): 否  页码 
             PageSize ( Integer ): 否  每页内容条数 
             OrderBy ( Integer ): 否  排序，默认按 id 降序展示，1降序 2升序 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        TotalSize ( Integer ): 申请人总数 
        Applicants ( Array of ApplicantResult ): 申请人列表 
       "字段"： ApplicantResult
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Reason ( String ): 失败原因 
        Status ( String ): 申请人状态 
        UserID ( String ): 火山子账号 
        Address ( String ): 申请人证件地址 
        Contact ( Object of Contact ): 联系人信息 
        Country ( String ): 国家 
        Document ( Object of Document ): 申请人材料 
        IDNumber ( String ): 身份证ID 
        Postcode ( String ): 申请人邮政编码 
        Province ( String ): 省份 
        AccountID ( String ): 火山账号 
        EnAddress ( String ): 申请人英文证件地址 
        CreditCode ( String ): 统一社会信用代码 
        ApplicantID ( String ): 申请人ID 
        ApplicantName ( String ): 申请人名称 
        ApplicantType ( String ): 申请人类型 
        EnApplicantName ( String ): 申请人英文名称 
       "字段"： Contact
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Email ( String ): 联系人邮箱 
        Phone ( String ): 联系人电话 
        ContactAddr ( String ): 联系人住址 
        ContactName ( String ): 联系人姓名 
        ContactPostcode ( String ): 联系人邮政编码 
       "字段"： Document
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        POAImg ( String ): 委托书图片 
        IDCardImg ( String ): 个人身份证或护照图片 
        POAReuseImg ( String ): 委托书复用声明图片 
        PersonEvidenceImg ( String ): 个人中英文证明图片 
        BusinessLicenseImg ( String ): 营业执照图片 
        BusinessEvidenceImg ( String ): 企业中英文证明图片 
    """,
    "get_requirement": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             RequirementID ( String ): 是  商标需求的 id 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Info ( String ): 需求信息 
        Phone ( String ): 联系方式 
        Status ( String ): 需求状态 
        UserID ( String ): 火山子账号 
        AccountID ( String ): 火山账号 
        CreateTime ( String ): 创建时间 
        UpdateTime ( String ): 更新时间 
        Description ( String ): 需求描述 
        TrademarkIDs ( Array of String ): 商标 id 列表 
        RequirementID ( String ): 需求ID 
        RequirementType ( String ): 需求类型 
    """,
    "list_requirements": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             RequirementTypes ( String ): 否  需求类型，多个类型用逗号,分隔，ConsultativeReg,商标顾问注册 WorrySavingReg,商标省心注册 ReviewOfTrademarkRefusal,商标驳回复审 NonUseCancellation,商标撤三申请 TrademarkChange,商标变更申请 TrademarkAssignment,商标转让申请 TrademarkOppositionResponse,商标异议答辩 TrademarkWithdrawal,商标撤回申请 TrademarkOpposition,商标异议申请 TrademarkInvalidation,商标无效宣告 TrademarkRenewal,商标续展申请 TrademarkLicenseRecordal,商标许可备案 NonUseCancellationResponse,商标撤三答辩 TrademarkInvalidationResponse,商标无效宣告答辩 TrademarkGracePeriod,商标宽展申请 TrademarkRegistrationCertificate,补发商标注册证 RegistrationRejectReview,商标不予注册复审 
             Status ( String ): 否  需求状态，多个状态用逗号,分隔，PendingResponse,待响应 Communicating,沟通中 PendingConfirm,待确认 PendingPay,待支付 Paid,已支付 Closed,已关闭 Invalid,已失效 
             RequirementID ( String ): 否  需求ID 
             Info ( String ): 否  需求信息 
             PageNumber ( Integer ): 否  页码 
             PageSize ( Integer ): 否  每页内容条数 
             SortBy ( String ): 否  按字段排序 
             SortOrder ( String ): 否  排序顺序 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        TotalSize ( Integer ): 需求个数 
        Requirements ( Array of Requirement ): 需求列表 
       "字段"： Requirement
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Info ( String ): 需求信息 
        Phone ( String ): 联系方式 
        Status ( String ): 需求状态 
        UserID ( String ): 火山子账号 
        AccountID ( String ): 火山账号 
        CreateTime ( String ): 创建时间 
        UpdateTime ( String ): 更新时间 
        Description ( String ): 需求描述 
        TrademarkIDs ( Array of String ): 商标 id 列表 
        RequirementID ( String ): 需求ID 
        RequirementType ( String ): 需求类型 
    """,
    "list_trademarks": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             RequirementTypes ( String ): 否  需求类型，多个类型用逗号,隔开，IntelligentReg 商标智能注册,ConsultativeReg 商标顾问注册,WorrySavingReg 商标省心注册,ReviewOfTrademarkRefusal 商标驳回复审,NonUseCancellation 商标撤三,TrademarkAssignment 商标转让,TrademarkChange 商标变更,TrademarkLicenseRecordal 商标许可备案,TrademarkRegistrationCertificate 补发商标注册证,TrademarkWithdrawal 商标撤回申请,TrademarkGracePeriod 商标宽展申请,TrademarkOpposition 商标异议申请,TrademarkInvalidation 商标无效宣告,NonUseCancellationResponse 商标撤三答辩,TrademarkOppositionResponse 商标异议答辩,TrademarkInvalidationResponse 商标无效宣告答辩,RegistrationRejectReview 商标不予注册复审,TrademarkRenewal 商标续展申请 
             ClassIDs ( String ): 否  商标类别，多个类别用逗号,隔开 
             Status ( String ): 否  商标状态，多个状态用逗号,隔开，商标状态，多个状态用逗号,隔开，LackOfMaterials,待补充材料 AutoTermination,自动终止 PendingReview,待审核 ReviewFailure,审核失败 PendingSubmitToOffice,待提交商标局 SubmittedToOffice,已提交到商标局 PendingCorrection,待补正 CorrectionReviewing,补正审核中 CorrectionReviewFailure,补正审核失败 CorrectionSubmitted,补正已提交 CorrectionExpired,补正已过期 AcceptanceSent,已发受理通知 NotAccepted,申请不予受理 ApplyForPendingEvidenceSameDay,同日申请待补证据 ApplyForPendingNegotiatedSameDay,同日申请待协商 ApplyForPendingDrawnSameDay,同日申请待抽签 DrawnSuccessDecisionSent,已发抽签决定-已中签 DrawnFailureDecisionSent,已发抽签决定-未中签 NoticeOfReviewOpinionSent,已发注册审查意见书 PartRejected,部分驳回 AllRejected,全部驳回 NoticeOfJudgeOpinionSent,已发驳回复审评审意见书 NoticeOfReviewOnRefusalDecisionSent,已发驳回复审决定书 NoticeOfPreliminaryExaminationSent,初审公告 Opposed,被异议 NotRegisteredBecauseOfObjection,因异议不予注册 ApproveRegistration,准予注册 Registered,已注册 NonUsed,被撤三 NonUsedFailure,被撤三-维持注册 NonUsedSuccess,被撤三-撤销注册 DeclaredInvalid,被无效宣告 DeclaredInvalidFailure,被无效-维持注册 DeclaredInvalidSuccess,被无效-商标无效 NoticeOfRegistrationCertificate,领取注册证通知 UserClosed,用户关闭 Closed,已关闭 ApplicationWithdrawn,已撤回申请 AssignmentCorrection,已发转让补正 AssignmentSuccess,转让成功 AssignmentFailure,转让失败 
             TrademarkIDs ( String ): 否  商标ID列表，多个id用逗号,分隔 
             TrademarkName ( String ): 否  商标名称 
             Comment ( String ): 否  备注 
             RegistrationNumber ( String ): 否  商标注册号 
             ApplicantName ( String ): 否  申请人 
             PageNumber ( Integer ): 否  页码 
             PageSize ( Integer ): 否  每页内容条数 
             SortBy ( String ): 否  按字段排序 
             SortOrder ( String ): 否  排序顺序 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        TotalSize ( Integer ): 商标个数 
        Trademarks ( Array of TrademarkResult ): 商标列表 
       "字段"： TrademarkResult
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Name ( String ): 商标名称 
        Risk ( Object of Risk ): 风险 
        Price ( Float ): 价格 
        Holder ( String ): 障碍商标申请人 
        Reason ( String ): 失败原因 
        Status ( String ): 商标状态 
        UserID ( String ): 火山子账户 
        ClassID ( String ): 商标类别 
        Comment ( String ): 备注 
        Pattern ( String ): 商标图样 
        AccountID ( String ): 火山账户 
        ClassInfo ( Array of String ): 商标类别内容 
        CreateTime ( String ): 需求提交时间 
        FilingDate ( String ): 递交商标局日期 
        UpdateTime ( String ): 更新时间 
        TrademarkID ( String ): 商标ID 
        ApplicantName ( String ): 申请人名称 
        StatusExpired ( Integer ): 商标状态是否过期 
        TrademarkType ( String ): 商标类型 
        RequirementType ( String ): 需求类型 
        RegistrationNumber ( String ): 申请号 
       "字段"： Risk
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        End ( String ): 风险评估结束内容 
        Class ( Array of RiskCLass ): 风险类别 
        Start ( String ): 风险评估开始内容 
       "字段"： RiskCLass
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        ClassID ( String ): 商标类别id 
        ClassName ( String ): 商标类别名称 
        RegistrationNumber ( String ): 商标注册号 
    """,
    "search_trademark_info": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             ClassID ( String ): 是  商标类别id 
             RegistrationNumber ( String ): 是  注册号 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Agent ( String ): 代理机构 
        Remark ( String ): 备注 
        Status ( String ): 商标状态 
        ClassID ( String ): 商标类别id 
        EndTime ( String ): 专用权日期-终止日期 
        Pattern ( String ): 商标图样 
        Progress ( Object of SearchTrademarkProgress ): 进度 
        StatusZH ( String ): 商标状态中文 
        ClassInfo ( String ): 商品服务id 
        ClassName ( String ): 商标类别名称 
        PreAnnNum ( String ): 初审公告期号 
        RegAnnNum ( String ): 注册公告期号 
        StartTime ( String ): 专用权日期-起始日期 
        FilingDate ( String ): 申请日期 
        PreAnnDate ( String ): 初审公告日期 
        RegAnnDate ( String ): 注册公告日期 
        ApplicantAddr ( String ): 申请人地址 
        ApplicantName ( String ): 申请人 
        ClassInfoName ( String ): 商品服务名称 
        TrademarkName ( String ): 商标名称 
        TrademarkType ( String ): 商标类型 
        RegistrationDate ( String ): 注册日期 
        RegistrationNumber ( String ): 注册号 
       "字段"： SearchTrademarkProgress
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        End ( String ): 终止进度 
        Reg ( String ): 已注册进度 
        Filing ( String ): 商标申请进度 
        PreAnn ( String ): 初审公告进度 
    """,
    "search_trademark": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
        body: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             SortBy ( String ): 否  综合排序，或 申请日期 排序，如果为空，则默认综合排序 
             Status ( String ): 否  商标状态 
                    Registered 已注册 
                    PreExamined 已初审 
                    Ended 已销亡 
                    Reviewing 待审中 
             ClassID ( String ): 否  商标类别，多个分类用逗号,分隔 
             PageSize ( Integer ): 否  每页内容条数 
             SortOrder ( String ): 否  排序，Desc降序 Asc升序，当按申请日期排序时此字段起作用，综合排序无需传递此字段 
             PageNumber ( Integer ): 否  页码 
             ApplicantName ( String ): 否  申请人 
             TrademarkName ( String ): 否  商标名称 
             RegistrationNumber ( String ): 否  注册号 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Classes ( Array of SearchTrademarkClassInfo ): 商标类别信息 
        Statuses ( Array of SearchTrademarkStatusInfo ): 商标状态信息 
        TotalSize ( Integer ): 商标个数 
        Trademarks ( Array of SearchTrademarkData ): 商标列表 
        Unregistered ( Array of UnregisteredClass ): 未注册的商标类别 
       "字段"： SearchTrademarkClassInfo
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Count ( Integer ): 数量 
        ClassID ( String ): 商标类别id 
        ClassName ( String ): 商标类别名称 
       "字段"： SearchTrademarkStatusInfo
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Count ( Integer ): 数量 
        Status ( String ): 商标状态 
        StatusZH ( String ): 商标状态中文 
       "字段"： SearchTrademarkData
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Uniq ( String ): 唯一标识 
        Agent ( String ): 代理机构 
        Status ( String ): 商标状态 
        ClassID ( String ): 商标类别id 
        Pattern ( String ): 商标图样 
        StatusZH ( String ): 商标状态中文 
        ClassName ( String ): 商标类别名称 
        PreAnnNum ( String ): 初审公告期号 
        RegAnnNum ( String ): 注册公告期号 
        FilingDate ( String ): 申请日期 
        PreAnnDate ( String ): 初审公告日期 
        RegAnnDate ( String ): 注册公告日期 
        ApplicantName ( String ): 申请人 
        TrademarkName ( String ): 商标名称 
        TrademarkType ( String ): 商标类型 
        RegistrationDate ( String ): 注册日期 
        RegistrationNumber ( String ): 注册号 
       "字段"： UnregisteredClass
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        ClassID ( String ): 商标类别id 
        ClassName ( String ): 商标类别名称 
    """,
    "list_barrier_trademarks": r""" 
    Args: 
        params: A JSON structure
             参数 ( 类型 ): 是否必选  描述 
             ---- ( ---- ): ----  ---- 
             TrademarkIDs ( String ): 否  商标ID列表，多个id用逗号,分隔 
             TrademarkName ( String ): 否  商标名称 
             RegistrationNumber ( String ): 否  商标注册号 
             ApplicantName ( String ): 否  需求申请人 
             Holder ( String ): 否  障碍商标申请人 
             RequirementTypes ( String ): 否  需求类型，多个类型用逗号,隔开，NonUseCancellation,撤三申请 
             ClassIDs ( String ): 否  商标类别id 
             Status ( String ): 否  申请状态，多个状态用逗号,隔开，PendingSubmitToOffice,待提交商标局 SubmittedToOffice,已提交商标局 AcceptanceSent,已发受理通知 NotAccepted,申请不予受理 NonUseSuccess,撤三成功 NonUseFailure,撤三失败 Closed,已关闭 
             PageNumber ( Integer ): 否  页码 
             PageSize ( Integer ): 否  每页内容条数 
             SortBy ( String ): 否  按字段排序 
             SortOrder ( String ): 否  排序顺序 
   Returns: 
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        TotalSize ( Integer ): 商标个数 
        Trademarks ( Array of TrademarkResult ): 商标列表 
       "字段"： TrademarkResult
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        Name ( String ): 商标名称 
        Risk ( Object of Risk ): 风险 
        Price ( Float ): 价格 
        Holder ( String ): 障碍商标申请人 
        Reason ( String ): 失败原因 
        Status ( String ): 商标状态 
        UserID ( String ): 火山子账户 
        ClassID ( String ): 商标类别 
        Comment ( String ): 备注 
        Pattern ( String ): 商标图样 
        AccountID ( String ): 火山账户 
        ClassInfo ( Array of String ): 商标类别内容 
        CreateTime ( String ): 需求提交时间 
        FilingDate ( String ): 递交商标局日期 
        UpdateTime ( String ): 更新时间 
        TrademarkID ( String ): 商标ID 
        ApplicantName ( String ): 申请人名称 
        StatusExpired ( Integer ): 商标状态是否过期 
        TrademarkType ( String ): 商标类型 
        RequirementType ( String ): 需求类型 
        RegistrationNumber ( String ): 申请号 
       "字段"： Risk
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        End ( String ): 风险评估结束内容 
        Class ( Array of RiskCLass ): 风险类别 
        Start ( String ): 风险评估开始内容 
       "字段"： RiskCLass
        参数 ( 类型 ): 描述 
        ---- ( ---- ): ---- 
        ClassID ( String ): 商标类别id 
        ClassName ( String ): 商标类别名称 
        RegistrationNumber ( String ): 商标注册号 
    """,
}
