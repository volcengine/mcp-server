import { fromByteArray } from 'base64-js';
import config from '../../src/mcp_server_sms/form_config.json';
import { failureSchema } from './contracts.js';

export const MAX_UPLOAD_BYTES = config.maxUploadBytes;

export class OperationError extends Error {
  constructor(message, { code, unknown = false, requestId } = {}) {
    super(message);
    Object.assign(this, { code, unknown, requestId });
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
    } catch {
      throw new OperationError(write ? '操作结果待确认，请先查询，勿重复提交。' : '查询未完成，请检查连接后重试。', { unknown: write });
    }
    const envelope = response._meta?.['sms/form'] ?? response.structuredContent;
    if (response.isError || envelope?.success !== true) {
      const checked = failureSchema.safeParse(envelope);
      const error = checked.success ? checked.data.error : null;
      throw new OperationError(error?.message ?? '参数校验或工具调用未完成，请检查表单。', {
        code: error?.code,
        unknown: write && (!checked.success || error.outcome_unknown !== false),
        requestId: envelope?.request_id,
      });
    }
    return envelope.result;
  }

  query(action, params = {}) {
    return this.call('query_sms_resources', { request: { action, params } });
  }

  async upload(file, request) {
    return this.call('upload_sms_file', { request: { ...request, ...await fileInput(file) } }, { write: true });
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

export async function fileInput(file) {
  if (!file || (file.data === undefined && (file.size === 0 || file.size > MAX_UPLOAD_BYTES))) {
    throw new OperationError('请选择不超过 10 MB 的非空文件。');
  }
  const data = file.data ?? fromByteArray(new Uint8Array(await file.arrayBuffer()));
  return { name: file.name, data };
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
