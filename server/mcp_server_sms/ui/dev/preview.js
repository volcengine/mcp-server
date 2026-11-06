import { AppBridge, PostMessageTransport } from '@modelcontextprotocol/ext-apps/app-bridge';
import html from '../../src/mcp_server_sms/static/forms.html?raw';

// 仅用于本地可视验证。没有真实 API 客户端、账号凭据或线上请求。
const rank = Object.fromEntries(['isOnlyTwoElement', 'isSkipOtherUse', 'needOtherUseCheck', 'operatorThreeElement', 'needOperatorImage', 'needOperatorMobile', 'responsibleThreeElement', 'needResponsibleImage', 'needResponsibleMobile', 'needBusinessCertificateImage'].map(key => [key, false]));
const group = { subAccountId: 'demo-group', subAccountName: '客户通知' };
let bridge, frame;
let taskStatus = 2;
let called = 0;
function response(result, privateData = false) {
  const envelope = { success: true, result, error: null };
  return { content: [{ type: 'text', text: '模拟结果' }], structuredContent: privateData ? { ...envelope, result: null } : envelope,
    ...(privateData ? { _meta: { 'sms/form': envelope } } : {}) };
}
function tool({ name, arguments: args }) {
  called += 1;
  document.getElementById('status').textContent = `AppBridge 已连接 · 模拟工具调用 ${called} 次 · 最近工具 ${name}`;
  if (name === 'get_qualification_requirements') return response(rank);
  if (name === 'get_account_information') return response({ businessName: '演示科技有限公司', userType: 'enterprise' });
  if (name === 'list_qualifications') return response({ list: [{ id: 101, materialName: '演示企业资质', purpose: 1, auditStatus: 3, usable: true }], total: 1 });
  if (name === 'query_sms_resources') {
    const { action } = args.request;
    if (action === 'GetSubAccountListForAgent') return response({ list: [group], total: 1 });
    if (action === 'ListSignaturesForAgent') return response({ List: [{ Signature: '演示科技', Status: 3, StatusDescription: '审核通过', Usable: true }], Total: 1 });
    if (action === 'ListBatchTemplatesForAgent') return response({ List: [{ TemplateId: 'demo-template', TemplateName: '预约通知', ChannelType: 'CN_NTC', TemplateContent: '您预约的服务时间为 ${time}，请准时到店。', TaskFields: [] }], Total: 1 });
    if (action === 'ValidateBatchTaskContentForAgent') return response({ Approved: true });
  }
  if (name === 'check_qualification_enterprise' || name === 'check_qualification_person') return response({ status: 0, ticket: 'demo-ticket' }, args.private);
  if (name === 'recognize_qualification_document') return response({ businessCertificateName: '演示科技有限公司', unifiedSocialCreditIdentifier: 'DEMO-CREDIT', legalPersonName: '演示人员', businessCertificateValidityPeriodStart: '2020-01-01', businessCertificateValidityPeriodEnd: '长期', personName: '演示人员', personIDCard: 'DEMO-ID' }, args.private);
  if (name === 'upload_sms_file') return response(args.request.kind === 'recipients'
    ? { file: 'demo/list.csv', name: args.request.name, totalCount: 2, dupCount: 0 }
    : { fileContent: 'demo/material', fileSuffix: 'png', name: args.request.name }, true);
  if (name === 'get_batch_csv_template') return response({ value: 'phone,time\n13800000000,明天上午\n' });
  if (name === 'apply_qualification') return response(1001);
  if (name === 'apply_signature') return response({ applyId: 'demo-application', status: 1 });
  if (name === 'create_batch_task') { taskStatus = 2; return response({ taskId: 'demo-task', totalCount: 2, dupCount: 0 }); }
  if (name === 'get_batch_task') return response({ taskId: 'demo-task', subAccount: 'demo-group', templateId: 'demo-template', sendContent: '您预约的服务时间为 ${time}，请准时到店。', status: taskStatus });
  if (name === 'start_batch_task') { taskStatus = 3; return response(null); }
  if (name === 'cancel_batch_task') { taskStatus = 7; return response(null); }
  if (name === 'register_traffic_resource') return response(null);
  if (name === 'send_verification_code') return response({ messageId: 'demo-message' });
  if (name === 'verify_code') return response({ status: 0 });
  return { content: [{ type: 'text', text: '模拟器没有此工具' }], isError: true };
}

async function open() {
  if (bridge) { await bridge.teardownResource({}).catch(() => {}); await bridge.close(); }
  frame?.remove(); called = 0;
  frame = document.createElement('iframe');
  frame.title = '短信表单'; frame.style.width = '960px'; frame.style.height = '540px';
  frame.setAttribute('sandbox', 'allow-scripts allow-same-origin');
  document.getElementById('mount').appendChild(frame);
  bridge = new AppBridge(null, { name: 'SMS local preview', version: '1' }, { serverTools: {}, downloadFile: {} }, {
    hostContext: { theme: document.getElementById('dark').checked ? 'dark' : 'light', displayMode: 'inline', availableDisplayModes: ['inline', 'fullscreen'] },
  });
  bridge.oncalltool = async params => tool(params);
  bridge.onupdatemodelcontext = async () => ({});
  bridge.ondownloadfile = async () => ({});
  bridge.onsandboxready = () => bridge.sendSandboxResourceReady({ html });
  bridge.oninitialized = () => {
    document.getElementById('status').textContent = 'AppBridge 已连接';
    return bridge.sendToolResult({ content: [{ type: 'text', text: '打开模拟表单' }], structuredContent: {
      success: true, form: document.getElementById('form').value, mode: 'input', result: null,
    } });
  };
  await bridge.connect(new PostMessageTransport(frame.contentWindow, frame.contentWindow));
  const sandbox = new URL('/dev/sandbox.html', window.location.href);
  sandbox.hostname = window.location.hostname === 'localhost' ? '127.0.0.1' : 'localhost';
  frame.src = sandbox.href;
}
document.getElementById('form').addEventListener('change', open);
document.getElementById('wide').addEventListener('click', () => { frame.style.width = '960px'; });
document.getElementById('narrow').addEventListener('click', () => { frame.style.width = '390px'; });
document.getElementById('dark').addEventListener('change', event => bridge.setHostContext({ theme: event.target.checked ? 'dark' : 'light' }));
open();
