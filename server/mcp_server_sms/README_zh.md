# 火山引擎短信 MCP App

面向支持 MCP Apps 的客户端：模型查询资源并打开可预填页面，客户在页面核对后提交。服务支持 MCP 2026-07-28、stdio 和无状态 Streamable HTTP，不加载或依赖 Skill。

当前尚未对外开放，本轮统一替换原 API 型工具面，不保留旧工具别名、兼容模式或直接模型写入路径。没有 MCP Apps 的客户端可继续只读查询；业务办理使用支持表单的客户端或短信控制台。

## 模型可见：17 个工具

| 用途 | 工具 |
| --- | --- |
| 账号、材料要求和资质 | `get_account_information`、`get_qualification_requirements`、`list_qualifications` |
| 消息组、签名、引流和运营商报备 | `query_sms_resources` |
| 普通模板及二级绑定详情 | `list_templates`、`list_second_templates` |
| 发送记录和统计 | `list_send_logs`、`get_send_statistics` |
| 群发任务查询和 CSV 示例 | `query_batch_tasks`、`get_batch_csv_template` |
| 打开业务页面 | `open_sms_service_onboarding`、`open_qualification_form`、`open_signature_form`、`open_traffic_form`、`open_template_form`、`open_batch_task_form` |

全部查询和开表工具都声明 `readOnlyHint=true`。开表不会申请、发码、发送短信或启动群发。自然语言单发先调用 `preview_sms_send`，向客户展示掩码号码和渲染正文；客户明确确认后，把未变化的请求和返回的 `confirmation` 交给 `send_sms`。提交前会重新核对模板和账号范围，参数或资源变化后必须重新预览。多个号码、定时发送和逐号码变量统一使用群发页面。`prefill` 只接受可编辑草稿，不接受业务提交 `request`、校验票据、确认标记或幂等键。用户已经提供的信息可预填，未知项留空。

已有群发任务通过 `open_batch_task_form({"task":{"subAccount":"消息组 ID","taskId":"任务 ID"}})` 打开管理页；`task` 与新建用的 `prefill` 互斥。查询和打开旧任务不会重建一条任务。

`query_sms_resources` 的 `request.action` 与 `request.params` 使用对应类型：

- 消息组：`GetSubAccountListForAgent`、`GetSubAccountDetail`。
- 签名与群发模板：`ListSignaturesForAgent`、`ListBatchTemplatesForAgent`。
- 引流：`GetTobTrafficDrivingLinkListForAgent`、`GetTobTrafficDrivingPhoneListForAgent`、`ListRelationTemplateForAgent`、`CheckTrafficDrivingExist`。
- 运营商报备：`ListThirdTemplate`、`AgentGetSignatureTemplateReportStatus`。
- 群发正文预检：`ValidateBatchTaskContentForAgent`，只用于模板明确声明的任务级正文。

`query_batch_tasks` 选择 `GetBatchTaskDetail`（`subAccount/taskId`）或 `GetBatchTaskList`（`subAccount/taskName/signature/templateId/pageIndex/pageSize`）。列表未出现任务不能代替按 ID 查询。

签名表单通过 `query_sms_resources` 调用 `GetApplySignatureBind`，一次取得已审核通过的资质候选数组；可选 `purpose` 为 1（自用）、2（他用），不传或 0 不限制用途。只消费 `id/purpose/materialName/businessCertificateName`，不分页、不逐条补查。客户确认后直接调用 `ApplySmsSignatureV2`，资质归属及审核状态由短信接口校验。`list_qualifications` 继续用于完整资质列表查询。

## 页面内部：22 个工具

| 用途 | 工具 |
| --- | --- |
| 文件上传 | `prepare_material_upload`、`complete_material_upload`、`prepare_recipients_upload`、`complete_recipients_upload` |
| 服务开通 | `get_sms_service_onboarding`、`submit_sms_service_onboarding` |
| 资质核验 | `recognize_qualification_document`、`check_qualification_enterprise`、`check_qualification_person`、`send_verification_code`、`verify_code` |
| 申请与引流录入 | `submit_qualification`、`submit_signature`、`submit_template`、`preview_traffic_resource`、`submit_traffic_resources` |
| 发送和群发管理 | `preview_sms_send`、`send_sms`、`send_batch_test_sms`、`create_batch_task`、`start_batch_task`、`cancel_batch_task` |

这些工具声明 `visibility=["app"]`，由遵循规范的宿主从模型工具列表中排除。可见性不是鉴权：每次调用仍校验客户凭据，最终资源权限由短信/IAM 执行。

OCR、企业和人员核验详细结果固定放在 `_meta["sms/form"]`，没有改成模型可见的开关。元数据仍经宿主管理，不代表端到端加密；生产接入需核对宿主日志和留存策略。

## 页面流程

七种表单共用 `ui://sms/forms.html`，React/Arco 样式由本包维护，不依赖原短信 Skill 的运行环境。

- 资质、签名和引流保留现有填写、上传、核验及确认步骤，支持宿主预填。
- 模板申请覆盖正文、用途、变量类型、签名、消息组、引流组合和短链选项。正文占位符与变量定义必须一致，动态业务规则和最终审核仍由短信服务判断。
- 普通发送支持 1–200 个国内号码，使用同一组变量。页面根据已选模板展示实际正文，普通发送和群发试发在确认后直接调用发送接口，模板有效性及发送参数由短信接口校验；保留号码及变量原文，不静默去重或拆单。每个收件人内容不同时使用 CSV 群发。
- 引流录入使用上游原生响应展示受理结果，成功后不逐条补查资源 ID；需要资源 ID 时使用资源查询工具。
- 群发新建页面一次确认完成创建任务与确认发送：先创建，再对同一任务调用启动接口；受理后不再要求二次确认。两个内部工具仍独立调用，不把创建本身视为发送。已有任务从管理页读取最新身份、状态与正文后由客户确认启动或取消；业务结果未知时不自动重试。
- 页面中的提交、发送或取消就是客户对所展示操作的确认。模型读取结果并回查，不在点击后再追加一轮会话确认。受理、审核、报备、任务结束与最终送达分别说明。

## 文件传输与私密数据

群发查询只返回任务摘要，不返回存储 Key、下载链接或内部扩展字段。

原文件不进入 App 工具调用参数。页面先传文件元信息取得本次上传请求，HTTPS 直传原字节到受信 ImageX/TOS，再通过 MCP 确认。短信 AK/SK 和 ImageX STS 留在服务端，页面只获得单文件上传能力。

CSV 直传后只保留签名引用，在核对群发任务时通过 `complete_recipients_upload` 一次完成名单统计和可选引流检查。MCP 通过 `GetFilePublicTosURL` 校验账号文件归属，回读有大小上限的原始流，拒绝压缩响应并核对 SHA-256，按页面已加载的 CSV 列定义检查表头、号码和重复数量。模板正文与列定义在同一次核对中复用，不再次查询；可选引流检查仍按实际正文查询报备资源。相同文件和模板的完整检查结果可在当前页面及凭证有效期内复用；未完整覆盖或发现缺失资源时重新检查。创建任务仍由短信后端校验实际文件。当前账号/网关无权限时明确失败，不跳过校验。

单文件最大 10 MiB。每实例最多同时持有两个 CSV 回读/校验缓冲，槽位覆盖后续引流消费期。材料直传前由页面检查大小，服务端校验申报元信息，实际存储侧限制由 ImageX 负责。上传确认按当前凭据签名，材料 10 分钟、CSV 1 小时有效；凭据刷新后重新上传。

上传失败保留已填内容，允许客户手动重选，不自动重传，也不会提交业务申请。普通聊天附件不会自动变成材料引用，较大文件应在表单选择；包内文件上限不代表宿主工具参数容量。

CSP 仅声明配置的 ImageX 上传域名和 TOS 桶的完整域名 `https://batch-sms-bucket.tos-cn-beijing.volces.com`，不加载外部 JS/CSS。使用完整域名，避免宿主将通配符 `*` 转义为 `%2A` 后导致浏览器拒绝连接。真实客户端需核实 CSP 支持与存储 CORS。服务没有 `/files` 路由、本机文件访问、调用方任意下载地址、持久化上传状态或服务端草稿。

## 结果与观测

查询失败不等于没有资源；请求受理不等于审核通过或送达。MCP 每次物理 API 请求只调用一次，不自行重试。

短信后端错误码、错误原文、RequestId 和 HTTP 状态直接透传，完整原始响应保存在 `error.backend_response`。MCP 不按错误码或 HTTP 状态推断业务最终结果，也不将后端错误改写成“结果未知”；后续处理由宿主 Agent 判断。未收到后端响应时返回实际网络异常类型及信息。表单直接展示错误原文，汇总流程同时保留各次调用的原始错误。

工具及物理 API 调用输出成对 start/end 日志与 OpenTelemetry 事件，携带关联 ID、耗时、公开错误码和请求编号，不记录文件、短信正文、号码或凭据。页面上传日志也不含文件名、URL 或授权头。观测失败不改变业务结果。

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
mcp-server-sms --transport streamable-http --host 0.0.0.0 --port 8000 \
  --public-url https://sms-mcp.example.com
```

客户端连接 `/mcp`。部署平台提供 HTTPS 和访问策略，每个请求通过 `Authorization: <Base64 JSON>` 或 `Authorization: Bearer <Base64 JSON>` 传递短信凭据：

```json
{"AccessKeyId":"<access-key>","SecretAccessKey":"<secret-key>","SessionToken":"<optional-session-token>"}
```

这沿用仓库已有的凭据传递方式，**不是 OAuth access token，Base64 也不是加密**。由客户端或可信网关在模型之外构造请求头，不得写入访问日志。每次短信请求独立执行官方 V4 签名，由短信/IAM 校验权限；HTTP 缺少凭据时不会使用进程默认账号。

不创建 OAuth 登录应用，不保存用户身份。MCP SDK 校验 `Host` 以及请求中提供的 `Origin`。将 `--public-url` 设为服务的 HTTPS 来源，可以放行其域名和同源请求。每个额外的可信网页来源可单独传入一次 `--allowed-origin https://app.example.com`。浏览器跨域接入时，部署入口还需处理 CORS 预检和响应头。不带 `Origin` 的客户端可凭有效凭据和允许的 `Host` 接入。无需协议会话或共享存储，多副本可以独立处理请求。云端平台的实际请求头、上传链路及表单宿主仍需联调确认。

通过统一 MCP 网关接入时，OAuth 登录和授权在网关完成，网关向本服务转发该客户的 STS 凭据。普通 OAuth access token 不能直接发给本服务，也不能用部署账号的 AK/SK 代替不同客户的凭据。

HTTP 连接池随 MCP 服务启动和关闭，凭据和签名头仍逐请求生成，不保留不同调用者之间的响应 Cookie。连接复用不引入业务状态或数据库。

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
