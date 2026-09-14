# 火山引擎短信 MCP Server

[English](README.md)

通过独立 MCP 工具完成国内短信的资质、签名、模板申请、发送及结果查询。沿用现有短信 OpenAPI，不改动 SMS 后端。业务规则来自官方 Skill `master@c7c49836dff727ca7a2ab297dc9d1ad62c5aec15`（1.4.4）。

支持 MCP **2026-07-28**、stdio 和无状态 Streamable HTTP，使用 MCP Python SDK 2.x。包版本为 **0.1.0**；包、MCP 协议和短信 API 的版本分别管理。

## 工具范围

| 场景 | 工具 |
| --- | --- |
| 开通检查与消息组 | `list_message_groups`、`get_message_group` |
| 资质规则与草稿 | `get_qualification_requirements`、`create_qualification_draft`、`update_qualification_base`、`get_qualification_draft`、`cancel_qualification_draft` |
| 材料与信息 | `import_input_file`、`upload_qualification_document`、`recognize_qualification_document`、`export_qualification_review`、`update_qualification_information`、`set_qualification_responsible`、`clear_qualification_legal` |
| 资质校验与申请 | `check_qualification_information`、`prepare_qualification_verification_code`、`verify_qualification_code`、`prepare_qualification_application`、`list_qualifications` |
| 签名与模板 | `list_signatures`、`list_templates`、`get_template`、`match_template`、`prepare_signature`、`prepare_template` |
| 发送与回执 | `prepare_send`、`get_send_status`、`analyze_delivery` |
| 普通群发 | `get_batch_csv_template`、`check_batch_file`、`prepare_batch_task`、`get_batch_task`、`list_batch_tasks`、`prepare_batch_launch`、`prepare_batch_cancel` |
| 执行与核对 | `execute_sms_operation`、`get_sms_operation_result` |

普通群发支持国内通知和营销短信、CSV 文件、立即或定时发送。不支持验证码群发、特殊通知群发、国际及港澳台短信。

当前发送流程使用客户已审核的签名和模板，暂不支持 `SPT_` 公共模板。不能把公共模板套用到客户模板的校验流程。

Server 不提供 HTML 页面、MCP App、浏览器登录或本地表单。材料收集、私密展示和客户确认由宿主或已有业务页面负责；工具不会自动生成这些界面。

发送前可用 `get_template(template_id, signature, sub_account)` 获取选定模板的正文和变量。`contentRedacted=true` 表示正文经过脱敏或截断，不应当作完整原文展示。模板详情查询不发送短信，发送前仍须生成当前预览。

## 资质申请流程

1. 查询消息组。只有 `RE:0001` 表示未开通；客户在[短信控制台](https://console.volcengine.com/sms)自行阅读协议并开通。
2. 调用 `get_qualification_requirements` 获取账号材料规则及 `privateInputSchemas`。调用 `create_qualification_draft(name, purpose)` 创建短期草稿；不创建线上申请、不要求 HTTPS 网页地址。
3. 宿主通过下述文件渠道提供图片。`upload_qualification_document` 将图片上传到既有短信材料服务并关联草稿。营业证件指定证件类型，居民身份证指定类型 `0` 和 `front`/`back`；其他法人证件和补充材料使用从 `0` 开始的连续 `index`，`replace=true` 表示从本次文件开始替换该组旧附件。
4. `recognize_qualification_document` 识别已上传的营业证件或身份证正反面，返回 `reviewFileId`。宿主取得该文件供客户私密核对；OCR 不自动保存为已确认信息。客户确认的字段由宿主按 `privateInputSchemas` 生成 `qualification_data` 文件，再调用 `update_qualification_information` 保存。材料名称、用途由草稿基本信息单独管理，不被 OCR 覆盖。
5. 用 `check_qualification_information` 校验企业、经办人及必要的法人/责任人信息。`set_qualification_responsible` 明确是否与经办人相同；相同时复用。法人补充材料可选；`clear_qualification_legal` 可移除已填写的法人补充材料，营业证件上的法人姓名仍保留。
6. 账号要求手机号验证时，先 `prepare_qualification_verification_code` 展示脱敏号码；客户确认后通过 `execute_sms_operation` 发码。宿主私密接收验证码并提供 `verification_code` 文件，由 `verify_qualification_code` 校验。验证码服务端暂存副本在调用后清除；源文件由宿主管理。
7. 材料与校验齐备后调用 `prepare_qualification_application`，向客户展示当前预览。客户确认后使用 `execute_sms_operation(operation_id)` 提交；申请、发送和验证码发送均不能自动确认。
8. `get_qualification_draft` 获取提交结果，成功后通过 `list_qualifications` 查询审核状态及原因。取消仅清除未提交的草稿，不撤销线上申请或结果未知的请求。

信息或材料变化会使已有预览失效。校验票据、上传凭证和图片地址不返回模型。企业未通过自动校验时按既有业务规则进入人工审核；经办人及独立责任人的必要校验必须通过。

## 文件输入与私密核对

工具参数只接收文件引用，不接收图片 Base64、验证码原文或原始个人字段。宿主须实现不进入模型上下文的材料渠道，不能假设普通聊天附件会自动、安全地传给 Server。

| 文件 kind | 内容与限制 |
| --- | --- |
| `qualification_image` | JPEG 或 PNG，每张 1 字节至 2 MB |
| `qualification_data` | UTF-8 JSON 对象，最多 64 KB；字段规范由资质要求工具返回 |
| `verification_code` | `{"code":"1234"}` 格式的 JSON 对象，四位数字，最多 1 KB |
| `batch_csv` | UTF-8 CSV，最多 50 MB；号码及变量随后按所选模板校验 |

**stdio：** 管理员显式配置 `SMS_MCP_INPUT_ROOT`。宿主将客户提供的文件放入该目录，调用 `import_input_file(relative_path, kind, content_type)` 得到 `fileId`。只允许目录内普通文件，拒绝绝对路径、目录穿越和符号链接。`export_qualification_review` 可将私密 OCR JSON 写入该目录内一个尚不存在的文件，供客户核对。宿主不能把核对文件读入模型对话。

**HTTP：** 宿主使用与 MCP 相同的访问令牌，在模型之外调用 `POST /files?kind=...`，请求体为原始文件字节，`Content-Type` 与内容一致。返回 `fileId`、类型、大小、指纹及有效期。宿主通过 `GET /files/{fileId}` 私密读取 OCR 核对数据；文件只允许原用户访问。HTTP 模式禁止通过 MCP 工具读取服务器的本地材料目录。

这两个 HTTP 文件接口属于宿主集成接口，不是 MCP 文件上传标准。是否支持这条私密文件通道，须按 TraeWork、豆包工作等实际宿主分别验收。

普通群发使用同一文件渠道：导入 `batch_csv` → `check_batch_file` → `prepare_batch_task` → 客户确认后执行创建 → `prepare_batch_launch` → 再次确认并执行启动。任务创建、任务处理完成与每个号码送达分别判断。

## 运行配置

必填公共配置：

| 变量 | 用途 |
| --- | --- |
| `SMS_MCP_DATABASE_URL` | SQLAlchemy URL；单机可用 SQLite，多副本使用同一个 PostgreSQL |
| `SMS_MCP_ENCRYPTION_KEY` | Fernet 密钥，加密草稿、文件和执行结果；副本之间共享 |
| `SMS_MCP_FLOW_TTL` | 文件、草稿和预览有效期，默认 1800 秒，至少 60 秒 |
| `SMS_MCP_OPERATION_TTL` | 执行去重记录有效期，默认 86400 秒，不得短于草稿有效期 |

stdio 配置 `SMS_MCP_LOCAL_SUBJECT` 作为本地记录所有者，并通过 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、可选 `VOLCENGINE_SESSION_TOKEN` 指定短信凭据。`SMS_MCP_INPUT_ROOT` 仅在需要导入或导出文件时配置，必须为绝对目录路径。

包正式发布后可运行：

```bash
uvx --from 'mcp-server-sms==0.1.0' mcp-server-sms --transport stdio
```

开发版可用当前源码或明确的 wheel 路径安装，无需等待合码或 PyPI 发布。不要将本机文件路径直接复制到云端配置。

HTTP 另外需要：

| 变量 | 用途 |
| --- | --- |
| `SMS_MCP_PUBLIC_URL` | 对外 HTTPS origin；服务挂载在域名根路径 |
| `SMS_MCP_OIDC_ISSUER` | 部署平台提供的现有令牌签发方，支持标准 discovery/JWKS |
| `SMS_MCP_TOKEN_AUDIENCE` | MCP 访问令牌的 audience |

```bash
mcp-server-sms --transport streamable-http --host 0.0.0.0 --port 8000
```

客户端连接 `/mcp`，每次请求独立鉴权，不依赖 initialize 或 Mcp-Session-Id。部署方负责 HTTPS、现有授权服务和数据库，本包不创建云资源或身份应用。

- `Authorization: Bearer <MCP access token>`：验证签名、issuer、audience、有效期和 `sub`，只允许 RS256 或 ES256。
- `X-Volcengine-Credentials`：由可信客户端或网关注入 Base64 JSON `{AccessKeyId, SecretAccessKey, SessionToken?}`，用于本次短信调用，不得记录或向模型暴露。文件接口只需 MCP token，不需要短信凭据。Base64 仅编码，网络传输必须使用 HTTPS。

这仍需对接具体托管平台的授权约定；未验证的平台不能声称开箱即用。HTTP 不回退到进程默认短信账号。不再需要网页登录 client ID、client secret、会话签名密钥或浏览器回调地址。

参考 [.env.example](.env.example) 提供配置。实际密钥用部署平台的 secret 注入，不提交到仓库。`GET /health` 用于存活检查，`/.well-known/oauth-protected-resource/mcp` 提供资源元数据。

## 执行、状态与重试

协议无状态不等于业务无状态。文件和草稿通过明确的 `fileId`、`draftId` 关联；每次访问都检查归属与有效期。草稿仅保存当前流程需要的信息，完成或取消后清除材料；文件到期不可访问，HTTP 定期清理，stdio 在后续调用时清理。导入源文件由宿主管理。

`operationId` 绑定预览内容和调用凭据，不是客户同意的证明；宿主负责展示和确认。凭据变化需要重新预览；资质草稿绑定创建时的凭据，授权有效期应覆盖该流程。

写请求结果未知时不自动重发、不新建相同操作绕过保护。先用 `get_sms_operation_result` 或 `get_qualification_draft` 查询记录；没有确切证据时返回 `outcome_unknown`。本地去重保护不等于上游 API 支持幂等键。

已开始执行的操作可以在 `SMS_MCP_OPERATION_TTL` 保留期内查询结果，不受较短的预览有效期影响；过期预览仍不能再次执行。

## 开发与验收

```bash
uv sync --extra test
uv run pytest
uv run ruff check src tests --select F,E9
uv build
uv run python -m twine check dist/*
```

自动测试使用模拟短信响应，覆盖无网页依赖的资质工具流程、预览失效、重复提交、未知结果恢复、手机号验证、文件隔离、普通群发和协议兼容。CI 另运行 PostgreSQL 共享存储测试。

`tests/live_readonly.py` 和 `tests/desktop_launcher.py` 用于可选的真实账号验收。它们使用指定 master Skill 的既有登录解析器，并从指定 wheel 运行 Server；凭据只在进程内传递。桌面启动脚本使用临时状态目录，结束后删除，不能用作持久部署。真实材料上传、验证码发送、申请提交、短信发送分别需要客户授权；查询成功不代表这些写操作已通过验收。

2026-09-14 本地 TraeWork 验收已覆盖资源查询、资质草稿创建与取消、非法材料拒绝，以及经客户确认的单条短信提交；发送接口返回成功和 Message ID，送达回执尚未确认。真实材料/OCR、手机号验证、资质/签名/模板申请提交、普通群发和云端宿主集成仍待验收。

仓库现有工作流在 PR 中构建检查新增包；合入 main 后对新增包或版本变更发布 PyPI，发布权限由仓库维护者提供。该工作流不负责云端部署。

## 来源与许可证

保留官方 master Skill 的 Apache-2.0 许可证。适配内容为短信 Action、签名、字段过滤、普通发送/群发、分析、资质校验与提交规则；不包含特殊通知群发、前端资产、CLI 登录流程或本机 MCP App 实现。
