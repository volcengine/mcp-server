import { toByteArray } from 'base64-js';
import CRC32 from 'crc-32';
import config from '../../src/mcp_server_sms/form_config.json';
import { failureSchema, materialUploadPlanSchema, recipientsUploadPlanSchema } from './contracts.js';

export const MAX_UPLOAD_BYTES = config.maxUploadBytes;

export class OperationError extends Error {
  constructor(message, { code, unknown = false, requestId, backendResponse, httpStatus, field } = {}) {
    super(message);
    Object.assign(this, { code, unknown, requestId, backendResponse, httpStatus, field });
  }
}

export class SmsFormClient {
  constructor(app) {
    this.app = app;
    this.controller = new AbortController();
  }

  async call(name, args = {}, { write = false } = {}) {
    let response;
    try {
      response = await this.app.callServerTool({ name, arguments: args }, {
        signal: this.controller.signal, timeout: 180000,
      });
    } catch (cause) {
      throw new OperationError(cause instanceof Error ? cause.message : String(cause), {
        code: cause?.code,
      });
    }
    const envelope = response._meta?.['sms/form'] ?? response.structuredContent;
    if (response.isError || envelope?.success !== true) {
      const checked = failureSchema.safeParse(envelope);
      const error = checked.success ? checked.data.error : null;
      throw new OperationError(checked.success ? error.message ?? '' : '参数校验或工具调用未完成，请检查表单。', {
        code: error?.code,
        unknown: write && error?.outcome_unknown === true,
        requestId: envelope?.request_id,
        backendResponse: error?.backend_response,
        httpStatus: error?.http_status,
      });
    }
    return envelope.result;
  }

  query(action, params = {}) {
    return this.call('query_sms_resources', { request: { action, params } });
  }

  async upload(file, request) {
    // 上传完成只产生文件引用，不会提交业务申请；失败允许用户手动重选，不自动重试。
    try {
      const bytes = await uploadBytes(file);
      const material = request.kind === 'material';
      if (!material && request.kind !== 'recipients') {
        throw new OperationError('不支持的文件上传类别。', { code: 'invalid_file_type' });
      }
      const metadata = material
        ? { name: file.name, size: bytes.length, category: request.category,
          crc32: (CRC32.buf(bytes) >>> 0).toString(16).padStart(8, '0') }
        : { name: file.name, size: bytes.length, sub_account: request.sub_account,
          template_id: request.template_id, sha256: await sha256(bytes) };
      const schema = material ? materialUploadPlanSchema : recipientsUploadPlanSchema;
      const checked = schema.safeParse(await this.call(
        material ? 'prepare_material_upload' : 'prepare_recipients_upload',
        { request: metadata }, { write: true },
      ));
      if (!checked.success || checked.data.confirmation.context.name !== file.name) {
        throw new OperationError('上传服务返回的文件信息不完整。', { code: 'invalid_upload_plan' });
      }
      const plan = checked.data;
      if (!material && ['size', 'sha256', 'sub_account', 'template_id'].some(
        key => plan.confirmation.context[key] !== metadata[key],
      )) {
        throw new OperationError('上传服务返回的名单信息不一致。', { code: 'invalid_upload_plan' });
      }
      const context = plan.confirmation.context;
      await this.uploadHttp(plan.upload, bytes, material, context.uri);
      // 名单在核对任务时统一回读，统计和可选的引流检查共用一次下载。
      if (!material) return { name: file.name, file: context.file, receipt: plan.confirmation };
      const result = await this.call('complete_material_upload', {
        request: plan.confirmation,
      }, { write: true });
      const valid = result?.name === file.name
        && result.fileContent === context.uri && result.fileSuffix === context.suffix;
      if (!valid) throw new OperationError('文件上传结果不完整，请重新选择文件。', { code: 'invalid_upload_result' });
      // 本地 Blob 只供当前表单回显；业务提交仍由 materialPreview 显式提取文件引用。
      return ['jpg', 'jpeg', 'png', 'gif'].includes(result.fileSuffix)
        ? { ...result, localFile: new Blob([bytes], { type: file.type }) } : result;
    } catch (cause) {
      if (cause instanceof OperationError) throw cause;
      throw new OperationError(cause instanceof Error ? cause.message : String(cause), { code: 'upload_failed' });
    }
  }

  async uploadHttp(upload, bytes, material, materialUri) {
    const url = new URL(upload.url);
    const allowed = material ? config.materialUpload.uploadHosts.includes(url.hostname)
      && decodeURIComponent(url.pathname) === '/' + materialUri && !url.search
      : url.hostname.endsWith('.volces.com');
    if (!allowed || url.protocol !== 'https:' || url.username || url.password || url.hash
      || url.port && url.port !== '443') {
      throw new OperationError('上传服务返回的地址不在受信范围内。', { code: 'invalid_upload_url' });
    }
    const fields = { action: material ? 'UploadMaterial' : 'UploadRecipients', correlation_id: crypto.randomUUID() };
    const started = performance.now();
    let errorCode, httpStatus;
    this.uploadLog({ ...fields, event: 'start' });
    try {
      const response = await fetch(upload.url, {
        method: upload.method, headers: upload.headers, body: bytes,
        credentials: 'omit', redirect: 'error',
        signal: AbortSignal.any([this.controller.signal, AbortSignal.timeout(60000)]),
      });
      httpStatus = response.status;
      if (!response.ok) {
        const body = await response.text();
        throw new OperationError(body, { code: 'upload_http_error', httpStatus,
          backendResponse: body, requestId: response.headers.get('x-tos-request-id') ?? response.headers.get('x-tt-logid') });
      }
      if (material) {
        const result = await response.json();
        if (result?.success !== 0) {
          throw new OperationError(typeof result?.error === 'string' ? result.error
            : result?.error?.message ?? JSON.stringify(result), {
            code: result?.error?.code ?? 'upload_not_confirmed', httpStatus,
            backendResponse: result,
            requestId: response.headers?.get('x-tos-request-id') ?? response.headers?.get('x-tt-logid'),
          });
        }
      }
    } catch (cause) {
      errorCode = cause instanceof OperationError ? cause.code : 'upload_transport_error';
      throw cause instanceof OperationError ? cause
        : new OperationError(cause instanceof Error ? cause.message : String(cause), { code: errorCode });
    } finally {
      this.uploadLog({ ...fields, event: 'end', duration_ms: Math.round(performance.now() - started),
        result_class: errorCode ? 'failed' : 'success', error_code: errorCode, http_status: httpStatus });
    }
  }

  uploadLog(data) {
    // 只记录阶段、耗时与稳定错误码，不记录文件名、内容、地址、票据或授权头。
    try { console.info('sms_upload', data); } catch { /* 日志失败不改变上传结果。 */ }
    try { this.app.sendLog?.({ level: 'info', logger: 'sms.upload', data })?.catch(() => {}); }
    catch { /* 宿主未提供日志通道时仍保留页面日志，不影响上传。 */ }
  }

  async downloadCsv(value) {
    if (!this.app.getHostCapabilities()?.downloadFile) {
      throw new OperationError('当前客户端不支持文件下载，请复制页面中的 CSV 示例保存。');
    }
    await this.app.downloadFile({ contents: [{ type: 'resource', resource: {
      uri: 'file:///sms-recipients.csv', mimeType: 'text/csv', text: value,
    } }] });
  }

  canOpenLinks() { return Boolean(this.app.getHostCapabilities()?.openLinks); }

  async openLink(url) {
    const result = await this.app.openLink({ url }, { signal: this.controller.signal });
    if (result?.isError) throw new OperationError('无法打开链接，请到火山引擎官网查看。');
  }

  async report(summary) {
    try {
      await this.app.updateModelContext({ structuredContent: summary }, {
        signal: this.controller.signal, timeout: 5000,
      });
    } catch { /* 宿主拒绝上下文更新，不改变已经返回的业务结果。 */ }
  }

  dispose() { this.controller.abort(); }
}

async function uploadBytes(file) {
  if (!file || typeof file.name !== 'string' || !file.name) {
    throw new OperationError('请选择文件。', { code: 'invalid_file' });
  }
  if (file.data !== undefined && (typeof file.data !== 'string'
    || file.data.length > Math.ceil(MAX_UPLOAD_BYTES / 3) * 4
    || file.data.length % 4 !== 0 || !/^[A-Za-z0-9+/]*={0,2}$/.test(file.data))) {
    throw new OperationError('预填文件编码无效或超过 10 MB。', { code: 'invalid_file' });
  }
  if (file.data === undefined && (!file.size || file.size > MAX_UPLOAD_BYTES)) {
    throw new OperationError('请选择不超过 10 MB 的非空文件。', { code: 'invalid_file_size' });
  }
  const bytes = file.data === undefined ? new Uint8Array(await file.arrayBuffer()) : toByteArray(file.data);
  if (!bytes.length || bytes.length > MAX_UPLOAD_BYTES) {
    throw new OperationError('请选择不超过 10 MB 的非空文件。', { code: 'invalid_file_size' });
  }
  return bytes;
}

async function sha256(bytes) {
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return Array.from(new Uint8Array(digest), value => value.toString(16).padStart(2, '0')).join('');
}


export function page(result, rowSchema) {
  const rows = result?.list ?? result?.List ?? result?.items ?? result?.Items;
  const total = result?.total ?? result?.Total;
  if (!Array.isArray(rows) || !Number.isInteger(total) || total < 0) {
    throw new OperationError('资源列表返回不完整，请稍后重新查询。');
  }
  if (rows.some(row => row === null || typeof row !== 'object' || Array.isArray(row) || rowSchema && !rowSchema.safeParse(row).success)) {
    throw new OperationError('资源字段返回不完整，请重新查询，不能用缺失的信息提交。');
  }
  return { rows, total };
}

export function withPrefilledOptions(rows, records, key) {
  // 预填补到的选项不改变常规列表的分页计数。
  const listed = new Set(rows.map(row => row[key]));
  return [...rows, ...records.filter(row => !listed.has(row[key]))];
}

export function materialPreview(buildRequest) {
  const included = new Set();
  const request = buildRequest((file, type) => {
    const fileContent = required(file.fileContent, '请先上传或移除待上传的材料。');
    included.add(file);
    return { fileType: type, fileContent, fileSuffix: file.fileSuffix };
  });
  return { request, attachmentNames: Array.from(included, file => file.name) };
}

export function checkedTicket(result) {
  // 兼容短信校验接口已记录的整数、数字文本和 rune 状态编码，不从文案推断成功。
  if (![0, '0', '\u0000'].includes(result?.status) || typeof result?.ticket !== 'string' || !result.ticket) {
    throw new OperationError('信息校验未通过或未返回有效票据，请核对填写内容。');
  }
  return result.ticket;
}

export function required(value, message) {
  if (value === '' || value === undefined || value === null) throw new OperationError(message);
  return value;
}
