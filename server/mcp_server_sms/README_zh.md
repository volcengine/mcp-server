# 火山引擎短信 MCP Server

[English](README.md)

独立的短信 API 适配服务，支持 **MCP 2026-07-28**、stdio、**Stateless Streamable HTTP** 和标准 **MCP Apps**。业务工具接收完整参数并调用对应接口；打开表单不执行写入，文件上传在服务端完成授权、上传及确认。

不依赖 Skill，不在服务端保存业务草稿或预览，不提供本机文件路径服务及通用 `prepare/execute` 流程；不需要 SQLite、PostgreSQL 或 Redis。五类表单在宿主沙箱内保存当前填写内容，客户端负责用户确认，现有短信服务负责业务校验、申请、任务与发送记录。

## 工具与接口

| 工具 | 短信 Action |
| --- | --- |
| `list_message_groups` | `ListSubAccountForAgent` |
| `get_message_group` | `GetSubAccountDetail` |
| `get_account_information` | `ListAllSmsProduct` |
| `get_qualification_requirements` | `GetAccountIdentRankForAgent` |
| `list_qualifications` | `GetSignatureIdentificationList` |
| `recognize_qualification_document` | `GetOCRLicenseForAgent` |
| `check_qualification_enterprise` | `ThreeElementEnterpriseCheckForAgent` |
| `check_qualification_person` | `ThreeElementPersonCheckForAgent` |
| `send_verification_code` | `SendSmsVerifyCodeByMobile` |
| `verify_code` | `CheckSmsVerifyCodeByMobile` |
| `apply_qualification` | `ApplySignatureIdentificationForAgent` |
| `list_signatures` | `ListSignatureForAgent` |
| `apply_signature` | `ApplySmsSignatureV2` |
| `list_templates` | `ListSmsTemplateForAgent` |
| `list_second_templates` | `ListSecondTemplate` |
| `apply_template` | `ApplySmsTemplateV2ForAgent` |
| `send_sms` | `SendSmsForAgent` |
| `list_send_logs` | `ListSmsSendLogForAgent` |
| `get_send_statistics` | `GetTotalSendCountStatV4ForAgent` |
| `get_batch_upload_url` | `GetUploadTosURL` |
| `get_batch_csv_template` | `TemplateUploadDemoForAgent` |
| `create_batch_task` | `SetBatchTaskForAgent` |
| `get_batch_task` | `GetBatchTaskDetail` |
| `list_batch_tasks` | `GetBatchTaskList` |
| `start_batch_task` | `ConsentBatchTask` |
| `cancel_batch_task` | `DeleteBatchTask` |
| `query_sms_resources` | 下表中的 10 项补充查询 |
| `manage_sms_service` | `ConfirmProtocolDocument`、`ActivateSmsProductInOneStep` |
| `open_sms_service_onboarding`、`get_sms_service_onboarding`、`submit_sms_service_onboarding` | 开通表单、`ListAllSmsProduct`、按确认执行协议签署或开通 |
| `register_traffic_resource`、`preview_traffic_resource` | 引流格式校验、录入及可选回查 |
| `send_batch_test_sms`、`check_batch_traffic_resources`（仅 App 可见） | 校验群发模板后单条试发、按实际正文核对引流 |
| `upload_sms_file`（仅 App 可见） | 内部材料授权及上传，或 CSV 模板校验与上传 |

共 **36 个工具、40 项业务 Action**，上传组件另在内部调用 `GetMUploadParam`。群发目录和 CSV 示例接口支持普通模板及特殊通知模板。验证码群发和国际短信不在范围内。三个聚合工具使用 `request.action` 和对应类型的 `request.params`。

| `query_sms_resources` 的 action | 用途 |
| --- | --- |
| `GetSubAccountListForAgent` | 分页查询消息组，支持项目、名称、启用状态筛选 |
| `ListSignaturesForAgent` | 按消息组、类型、行业、审核状态查询签名 |
| `ListBatchTemplatesForAgent` | 查询群发模板目录，保留 `TaskFields`、`BatchOnly` |
| `GetTobTrafficDrivingLinkListForAgent` | 查询引流链接、短链及备案信息 |
| `GetTobTrafficDrivingPhoneListForAgent` | 查询引流号码及所属企业 |
| `ListRelationTemplateForAgent` | 按签名、号码或链接查询关联模板 |
| `CheckTrafficDrivingExist` | 检查实际正文中的引流资源 |
| `ListThirdTemplate` | 查询组合模板报备 |
| `AgentGetSignatureTemplateReportStatus` | 查询签名与模板的三网报备状态 |
| `ValidateBatchTaskContentForAgent` | 预检特殊通知任务正文 |

例如，查询群发模板时，工具参数为：

```json
{
  "request": {
    "action": "ListBatchTemplatesForAgent",
    "params": {"SubAccounts": ["<消息组 ID>"], "Page": 1, "PageSize": 20}
  }
}
```

`RE:0001` 表示未开通。支持 MCP Apps 时，用 `open_sms_service_onboarding` 让客户核对协议及计费后确认。直接调用 `manage_sms_service` 时，先通过 `get_account_information` 核实协议和商品状态，获授权后按实际协议 ID 调用 `ConfirmProtocolDocument`。签署结果的 `fail` 为空后，首次开通或重新开通再调用 `ActivateSmsProductInOneStep`，参数为 `{"product":["sms"]}`，最后回查账号状态。

`register_traffic_resource` 的参数为 `{"request":{"action":"<上述两种录入 Action 之一>","params":{"data":[...]}}}`。每次最多 10 个链接或 100 个号码；完整字段和必填约束见 `tools/list`。链接、路径、查询参数、号码均按原文传递，个人证件信息通过客户端私密渠道输入。

服务端会核对协议签署结果完整覆盖本次协议且成功、失败清单不重叠，开通结果恰好对应本次商品。缺失或不匹配返回 `outcome_unknown`；合法的部分签署失败或开通业务失败保留原值，供客户端核对。

直接发送沿用调用方提供的签名、模板和号码。已有模板 ID 交给发送接口校验。

## 资质与文件

资质申请接收完整企业、经办人、责任人、可选法人信息、材料引用和上游校验票据。`ticket` 是短信校验接口返回的业务凭据，由客户端保管并在申请时传回，不是 MCP 的草稿 ID。上游要求、票据有效性和审核结果由短信服务判断。

验证码接口所需的应用 ID、场景、模板和通道来自已有业务配置，MCP 不硬编码某个内部应用或自动选择。客户端应通过私密渠道提供个人材料和验证码；OCR 默认 `private=true`，完整识别字段只放在 `_meta["sms/form"]` 供私密页面核对，普通内容只返回操作状态。客户明确同意识别结果进入模型上下文时才显式使用 `private=false`；此时姓名、证件号等会进入模型可见的 `content` 和 `structuredContent`。

MCP Apps 表单可以选择并上传材料，服务端通过当前客户的凭据取得材料上传授权，再完成 ImageX 上传。材料上传仅允许当前 ImageX 服务的官方区域/加速域名及官方列出的历史上传主机，其他主机在发送文件和上传授权前拒绝；CSV 仍按自身 TOS 地址策略校验。也可以继续使用已有短信材料渠道的引用。MCP 不读取本机路径、不下载调用方指定的 URL、不持久保存文件，也不提供额外的 `/files` 接口；普通聊天附件不会自动转换成材料引用。

签名申请支持 `appIcp.appIcpFileList`、`trademark.trademarkFileList`、`uploadFileList` 以及消息组绑定。`GetMUploadParam` 不作为模型可调用工具暴露，其结果整体禁止从普通 API 结果返回；临时凭据仅供服务端上传组件消费。

群发 CSV：调用 `get_batch_upload_url`，客户端使用短期签名 URL 直接上传原文件，再把返回的 `file` 对象 Key 作为 `fileUrl` 传入 `create_batch_task`。创建与启动是短信业务本身的两个操作，必须分别调用。

## MCP Apps 表单

不传 `request` 调用以下工具，只打开对应表单；传完整 `request` 仍按原工具语义直接调用短信 API，必须事先取得用户授权：

| 工具 | 表单能力 |
| --- | --- |
| `apply_qualification` | 企业、人员和材料校验，企业信息未通过自动核验时由客户确认转人工审核 |
| `apply_signature` | 唯一可用资质和消息组自动预选，公司名回填，项目和证明材料，名称风险单独确认 |
| `register_traffic_resource` | 预览时校验格式、协议和重复项，确认录入后回查资源 ID |
| `create_batch_task` | 单条试发及回执、按 CSV 逐行检查引流、创建后单独确认启动或取消 |
| `open_sms_service_onboarding` | 查看国内短信商品、协议与计费，确认开通或更新协议，刷新实际状态 |

例如 `tools/call` 的参数为 `{"name":"apply_signature","arguments":{}}`。五个开表工具均通过 `_meta.ui.resourceUri` 绑定 `ui://sms/forms.html`，`resources/read` 返回 MIME 为 `text/html;profile=mcp-app` 的自包含 HTML。Python 使用官方 `Apps` 扩展，页面使用官方 `@modelcontextprotocol/ext-apps`。

宿主 Agent 把已核实的字段传给 `prefill`，未知字段可以省略。打开后客户可修改或补齐，再核对提交。
`prefill` 与 `request` 互斥；准确的字段和类型见 `tools/list`。例如
`{"name":"create_batch_task","arguments":{"prefill":{"name":"双十一活动通知","subAccount":"group-id","signature":"示例签名","templateId":"template-id"}}}`。

| 表单 | 可预填内容 |
| --- | --- |
| 资质 | 用途、名称、`businessInfo`、经办人、责任人、法人信息、人员关系和营业证件、人员证件、委托书、其他材料。证件图片在 `personCertificate` 中按 `front`、`back` 或法人其他证件的 `document` 提供。 |
| 签名 | 签名内容、来源、资质 ID、消息组范围和组 ID、项目名称、说明、APP 备案、商标信息和各类证明附件。 |
| 引流 | `kind` 为 `link` 或 `phone`；`data` 中填写对应行的链接、协议、备案或号码、类型、归属信息。 |
| 群发 | 任务名称 `name`、消息组、签名、模板、任务级正文、`checkTraffic`、`scheduled`、`sendTime`（Unix 秒，页面显示北京时间）及 `recipientsFile`。模板声明了正文输入项时才使用任务级正文。 |

签名和群发的下拉项按当前账号资源核对。群发可只预填签名或模板，补齐上游选项后再核对和选中。
个人信息和文件须由宿主通过获授权的私密渠道传递；预填值只在工具结果的 `_meta["sms/form"].prefill` 中交给视图，普通结果不回显。
附件形如 `{"name":"proof.png","data":"<原文件的 Base64>"}`，同一次开表的附件合计最多 10 MB；宿主不具备私密文件传递能力时由客户在表单内选择。
页面先显示待上传文件，用户点击上传后才走原材料或 CSV 校验上传流程。预填不接受验证码、校验票据、已上传文件 Key、勾选确认或任务幂等键。

表单配色、布局和样式文件复用 byted-sms-sender 1.4.6 的 React/Arco 页面；源码复制在本包 `ui/` 中，Skill 不做修改，构建及运行不依赖 Skill 路径。宿主宽窄尺寸、深色模式在独立样式中适配。JS/CSS 已内联，CSP 不声明外部连接或静态源，页面不直接请求业务 API。

- 上传仅通过宿主代理调用 `upload_sms_file`，文件引用放入 `_meta["sms/form"]`，普通结果只含操作状态；OCR 默认使用该通道；企业/人员校验可显式传入 `private=true`。`_meta` 仍由宿主管理，生产接入需核实宿主的数据展示、留存及日志策略，不能将其当作端到端加密或独立权限边界。
- `upload_sms_file` 声明 `visibility=["app"]`；宿主按标准过滤模型工具列表。该标记不替代短信/IAM 鉴权，所有业务请求仍使用本次调用者的凭据。
- 单文件最大 **10 MiB**，每实例同时处理最多 **2** 个上传，满载时明确拒绝且不排队解码。资质图片支持 JPG/JPEG/PNG；签名材料按类别支持图片、PDF、ZIP、DOC/DOCX。CSV 按对应模板的表头校验，保留原文件，重复号码只计数不改写。更大的文件继续走现有上传渠道；宿主及网关实际请求体上限需联调确认。
- `form_config.json` 是前后端共同的上传限制和短信材料/验证场景配置；其中是既有短信业务标识，不能填写客户 AK/SK 或 Token。
- 用户核对并勾选后才提交；重复点击受控，未知写结果锁定重试。群发创建后重新查询任务；启动前核对任务身份、状态和正文，另行确认实际发送及费用。历史恢复只展示返回结果，不重放写操作。
- 客户确认转人工审核后，服务端重新核验企业信息，并在符合条件时使用上游人工审核票据。人员、材料和手机号核验仍以账号要求为准。
- CSV 引流检查逐行渲染短信正文，向查询接口提交去重后的正文，在限定时间内最多检查 100 种不同正文。确认页显示覆盖数量、缺失资源和待核对的行。
- 开通表单在提交前重新核对当前账号及协议清单。协议更新只签待更新项，首次开通或重新开通需完整签署后再发起开通，最终以账号状态为准。同一 MCP 实例会锁定同一访问凭据的未决提交，直到查到明确结果。
- 原有工具继续接受完整参数。表单填写内容和确认状态保留在当前宿主视图内。

开发及预览见 [ui/README.md](ui/README.md)。标准接口参考 [MCP Apps](https://modelcontextprotocol.io/extensions/apps/overview)。

## 0.2.0 参数迁移

原有 26 个工具名保留，以下输入与结果契约有变化，客户端需要同步更新：

- `apply_template` 改用 `ApplySmsTemplateV2ForAgent`。每个 `templateParams` 项必须明确给出 `paramType`（1 普通、2 链接、3 号码、4 Path、5 超级变量），不再默认为普通变量。`templateTrafficDriving` 使用二维数组，每项提供 `name`、`paramType` 及资源 `id` 或 `content`。
- `create_batch_task` 改用 `SetBatchTaskForAgent`：必填 `subAccount/name/signature/templateId/fileUrl/scheduled/sendTime/idempotencyKey`；特殊通知按模板的 `TaskFields` 提供 `content`，先做正文预检。移除旧的 `templateName/channelType/extra` 输入，由短信服务解析模板。立即发送传 `scheduled=false, sendTime=0`，定时发送传 Unix 秒。客户端为同一已确认任务保留稳定的 `idempotencyKey`。请求等待上限为 60 秒，只有返回有效 `taskId/totalCount/dupCount` 才确认创建受理；计数为 0 有效。
- `get_batch_csv_template` 改用 `TemplateUploadDemoForAgent`，不再接受 `force_update`；CSV 内容从结果的 `value` 读取，兼容 JSON 和原始 CSV 响应。不自行构造列名。
- `get_send_statistics` 改用 V4：支持项目、消息组、类型/签名/模板数组、标准错误码、拆分口径与分组开关，固定查询国内短信。旧的单个类型/签名/模板输入仍可用，按 API 数组字段发送。
- `list_send_logs` 可以省略消息组，查询当前主账户；模型结果移除完整 `mobile/content`，保留回执状态与错误码。资源查询同时移除人员证件、材料引用等私密字段，其他未知业务字段保留。

Schema 由同一套类型模型生成并内联，使用标准 `oneOf/anyOf`，不包含 `$ref/$defs/definitions`。表单复用原样式并改用 AppBridge；不保留 localhost 接口。Plugin 元数据、OAuth 网关配置和上架仍需单独办理。API 失败和参数校验失败提供结构化 `isError` 结果，表单不解析错误文案判断写入是否完成。

## 本地运行

需要 Python 3.11 或以上版本。配置 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY` 及可选 `VOLCENGINE_SESSION_TOKEN`，再运行：

```bash
uv sync --extra test
uv run mcp-server-sms --transport stdio
```

凭据放在客户端进程环境中，不放入工具参数、聊天或仓库。无需配置数据库、流程有效期、本地身份或材料目录。

也可构建本版 wheel 后指定安装包运行：

```bash
uv build
uvx --from ./dist/mcp_server_sms-0.2.0-py3-none-any.whl mcp-server-sms --transport stdio
```

功能取决于实际安装版本；仓库代码更新不等于线上函数已更新。

## 云端运行

```bash
mcp-server-sms --transport streamable-http --host 0.0.0.0 --port 8000
```

客户端连接 `/mcp`。部署平台提供 HTTPS 和访问策略，每个请求通过 `Authorization: <Base64 JSON>` 或 `Authorization: Bearer <Base64 JSON>` 传递短信凭据：

```json
{"AccessKeyId":"<access-key>","SecretAccessKey":"<secret-key>","SessionToken":"<optional-session-token>"}
```

这沿用仓库已有的凭据传递方式，**不是 OAuth access token，Base64 也不是加密**。由客户端或可信网关在模型之外构造请求头，不得写入访问日志。每次短信请求独立执行官方 V4 签名，由短信/IAM 校验权限；HTTP 缺少凭据时不会使用进程默认账号。

不创建 OAuth 登录应用，不保存用户身份。MCP SDK 根据 `--host` 应用默认传输校验。旧命令可继续传入 `--public-url` 以兼容启动参数。无需协议会话或共享存储，多副本可以独立处理请求。云端平台的实际请求头、上传链路及表单宿主仍需联调确认。

通过统一 MCP 网关接入时，OAuth 登录和授权在网关完成，网关向本服务转发该客户的 STS 凭据。普通 OAuth access token 不能直接发给本服务，也不能用部署账号的 AK/SK 代替不同客户的凭据。

HTTP 连接池随 MCP 服务启动和关闭，凭据和签名头仍逐请求生成，不保留不同调用者之间的响应 Cookie。连接复用不引入业务状态或数据库。

## 执行语义

- 写工具直接产生业务操作，客户端必须先取得用户授权；工具注解不是授权证明。
- 发送接口成功只表示受理，需按 Message ID 查询送达回执。空列表不是失败证据。
- 资质、签名和模板申请成功不等于审核通过，分别查询其状态。
- 不自动重试任何 API 调用。写请求超时或响应不足以确认结果时返回 `outcome_unknown`，不能盲目重发；不承诺跨请求去重或“恰好一次”。
- 非结构化的 HTTP 400/401/403/404/405/413/415/422/429 响应按明确拒绝处理；其他非结构化状态、服务端异常和损坏或缺少关键结果的成功响应，仍保留未知写结果。API 响应错误携带 `http_status`，不回显响应正文。
- 上传接口顶层 `url` 保持完整原文，包括参与签名的凭证参数；其他字段仍按规则脱敏。完整 URL 是短期授权信息，不要修改后上传，也不要写入日志。
- 接口调用成功也可能返回校验未通过，例如验证码的 `status` 非零、正文预检 `Approved=false` 或协议签署 `fail` 非空；保留上游字段，调用方应检查业务结果。报备成功不代表送达，任务列表可能不含状态 2，已知任务 ID 时直接查详情。
- 错误保留公开错误码和 RequestId，不回显请求正文、验证码、凭据或原始服务端错误文本；字段按上述隐私契约过滤，其他业务值不改写。申请、开通与引流录入的 `1999/SY:0500` 等不确定错误不应自动重试。

工具调用和短信 API 调用分别记录 start/end，包含关联 ID、Action、耗时、结果分类、错误码与 RequestId。日志写 stderr，OpenTelemetry 使用宿主配置的 tracer provider，不配置 exporter 时不外发。两种观测失败均不改变业务结果；不会记录参数、正文、号码或鉴权头。部署平台还需约束自身访问日志。

## 验证和发布

```bash
cd ui
npm ci
npm test
npm run build
cd ..
uv run ruff check src tests
uv run pytest -q
uv build
uv run python -m twine check dist/*
```

测试覆盖实际 MCP 协议边界、参数映射、凭据隔离、未知写结果、CSV、Schema、隐私过滤、观测故障、UI 资源和交互确认；上游 HTTP 使用替身，不会真的发送短信或提交申请。Python 测试校验 UI 源文件指纹与打包 HTML 一致，避免修改前端后漏构建。Node.js 只用于开发构建，部署 wheel 不需要 Node.js。实际写操作验收需要客户单独授权，本地通过不代表网关 OAuth、ImageX/TOS 实际上传、云端部署或豆包客户端已完成联调。

请求字段参照[官方短信 SDK](https://github.com/volcengine/volcengine-python-sdk/tree/3b116781c5b8bb648f215b29587f2ec74d9e5d02/volcenginesdkvolcsms)，请求签名使用[官方 Python SDK](https://github.com/volcengine/volc-sdk-python)。资质扩展 Action 按现有短信服务契约接入，需确认部署账号的接口可用性。

源码版本为 0.2.0。复用仓库现有 PR 构建检查和合入后的 PyPI 发布流程，发布权限由维护者提供；包发布、veFaaS 升级和 ATS/Plugin 上架是分别执行的操作。许可证为 Apache-2.0。
