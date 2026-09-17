# 火山引擎短信 MCP Server

[English](README.md)

独立的短信 API 适配服务，支持 **MCP 2026-07-28**、stdio 和 **Stateless Streamable HTTP**。每个工具接收完整参数，调用一次对应短信接口并返回结果。

不依赖 Skill，不保存业务草稿或预览，不提供页面、本地文件服务及通用 `prepare/execute` 流程；不需要 SQLite、PostgreSQL、Redis 或业务加密密钥。客户端负责交互和用户确认，现有短信服务负责业务校验、申请、任务与发送记录。

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
| `apply_template` | `ApplySmsTemplateV2` |
| `send_sms` | `SendSmsForAgent` |
| `list_send_logs` | `ListSmsSendLogForAgent` |
| `get_send_statistics` | `ListTotalSendCountStatForAgent` |
| `get_batch_upload_url` | `GetUploadTosURL` |
| `get_batch_csv_template` | `TemplateUploadDemo` |
| `create_batch_task` | `SetBatchTask` |
| `get_batch_task` | `GetBatchTaskDetail` |
| `list_batch_tasks` | `GetBatchTaskList` |
| `start_batch_task` | `ConsentBatchTask` |
| `cancel_batch_task` | `DeleteBatchTask` |

共 26 个工具。普通群发仅覆盖国内通知和营销短信，不包含特殊通知群发、验证码群发或国际短信。服务开通由用户在[短信控制台](https://console.volcengine.com/sms)阅读协议并完成；`RE:0001` 表示未开通。

工具不替换签名、不匹配或改写模板、不去重号码，也不生成跳过校验票据。已有模板 ID 直接交给发送接口校验，不因查询列表缺少某类模板就自行禁止发送。

## 资质与文件

资质申请接收完整企业、经办人、责任人、可选法人信息、材料引用和上游校验票据。`ticket` 是短信校验接口返回的业务凭据，由客户端保管并在申请时传回，不是 MCP 的草稿 ID。上游要求、票据有效性和审核结果由短信服务判断。

验证码接口所需的应用 ID、场景、模板和通道来自已有业务配置，MCP 不硬编码某个内部应用或自动选择。客户端应通过私密渠道提供个人材料和验证码；OCR 返回识别字段，由客户核对后决定提交内容。

资质材料应先通过现有短信材料渠道上传，OCR 和申请工具接收该渠道的文件引用。MCP 不读取本机路径、不下载任意 URL、不托管文件，也不提供额外的 `/files` 接口。实际客户端须具备可用的私密材料渠道，普通聊天附件不会自动转换成短信材料引用。

群发 CSV：调用 `get_batch_upload_url`，客户端使用短期签名 URL 直接上传原文件，再把返回的 `file` 对象 Key 作为 `fileUrl` 传入 `create_batch_task`。创建与启动是短信业务本身的两个操作，必须分别调用。

## 本地运行

需要 Python 3.11 或以上版本。配置 `VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY` 及可选 `VOLCENGINE_SESSION_TOKEN`，再运行：

```bash
uv sync --extra test
uv run mcp-server-sms --transport stdio
```

凭据放在客户端进程环境中，不放入工具参数、聊天或仓库。无需配置数据库、流程有效期、本地身份或材料目录。

0.1.0 发布后可使用固定版本：

```bash
uvx --from 'mcp-server-sms==0.1.0' mcp-server-sms --transport stdio
```

发布前可以从源码或指定 wheel 安装。

## 云端运行

```bash
mcp-server-sms --transport streamable-http --host 0.0.0.0 --port 8000 \
  --public-url https://sms-mcp.example.com
```

客户端连接 `/mcp`。部署平台提供 HTTPS 和访问策略，每个请求通过 `Authorization: Bearer <Base64 JSON>` 传递短信凭据：

```json
{"AccessKeyId":"<access-key>","SecretAccessKey":"<secret-key>","SessionToken":"<optional-session-token>"}
```

这沿用仓库已有的凭据传递方式，**不是 OAuth access token，Base64 也不是加密**。由客户端或可信网关在模型之外构造请求头，不得写入访问日志。每次短信请求独立执行官方 V4 签名，由短信/IAM 校验权限；HTTP 缺少凭据时不会使用进程默认账号。

不创建 OAuth 登录应用，不保存用户身份。`--public-url` 用于配置 HTTP 域名校验；未提供时仅允许本机域名。无需协议会话或共享存储，多副本可以独立处理请求。云端平台的实际请求头与材料渠道仍需联调确认。

HTTP 连接池随 MCP 服务启动和关闭，凭据和签名头仍逐请求生成，不保留不同调用者之间的响应 Cookie。连接复用不引入业务状态或数据库。

## 执行语义

- 写工具直接产生业务操作，客户端必须先取得用户授权；工具注解不是授权证明。
- 发送接口成功只表示受理，需按 Message ID 查询送达回执。空列表不是失败证据。
- 资质、签名和模板申请成功不等于审核通过，分别查询其状态。
- 不自动重试任何 API 调用。写请求超时或响应不足以确认结果时返回 `outcome_unknown`，不能盲目重发；不承诺跨请求去重或“恰好一次”。
- 非结构化的 HTTP 400/401/403/404/405/413/415/422/429 响应按明确拒绝处理；其他非结构化状态、服务端异常和损坏或缺少关键结果的成功响应，仍保留未知写结果。API 响应错误携带 `http_status`，不回显响应正文。
- 上传接口顶层 `url` 保持完整原文，包括参与签名的凭证参数；其他字段仍按规则脱敏。完整 URL 是短期授权信息，不要修改后上传，也不要写入日志。
- 接口调用成功也可能返回校验未通过，例如验证码的 `status` 非零；保留上游字段，调用方应检查业务结果。
- 错误保留公开错误码和 RequestId，不回显请求正文、验证码、凭据或原始服务端错误文本；正常业务数据不做无声改写。

## 验证和发布

```bash
uv run ruff check src tests
uv run pytest -q
uv build
uv run python -m twine check dist/*
```

测试覆盖直接调用、参数映射、调用者凭据隔离、未知写结果、业务错误、CSV 响应及无状态协议；不会真的发送短信或提交申请。实际写操作验收需要客户单独授权，旧实现的测试结果不能代表本版已完成全流程验收。

请求字段参照[官方短信 SDK](https://github.com/volcengine/volcengine-python-sdk/tree/3b116781c5b8bb648f215b29587f2ec74d9e5d02/volcenginesdkvolcsms)，请求签名使用[官方 Python SDK](https://github.com/volcengine/volc-sdk-python)。资质扩展 Action 按现有短信服务契约接入，需确认部署账号的接口可用性。

包版本为 0.1.0，尚未发布。复用仓库现有 PR 构建检查和合入后的 PyPI 发布流程，发布权限由维护者提供；包发布不等于云端部署。许可证为 Apache-2.0。
