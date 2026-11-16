import { AppBridge, PostMessageTransport } from '@modelcontextprotocol/ext-apps/app-bridge';
import html from '../../src/mcp_server_sms/static/forms.html?raw';
import config from '../../src/mcp_server_sms/form_config.json';
import sampleProof from './sample-proof.png?inline';

// 仅用于本地可视验证。没有真实 API 客户端、账号凭据或线上请求。
const previewParams = new URLSearchParams(window.location.search);
const previewWidth = previewParams.get('width') === 'narrow' ? '390px' : '960px';
const rank = Object.fromEntries(['isOnlyTwoElement', 'isSkipOtherUse', 'needOtherUseCheck', 'operatorThreeElement', 'needOperatorImage', 'needOperatorMobile', 'responsibleThreeElement', 'needResponsibleImage', 'needResponsibleMobile', 'needBusinessCertificateImage'].map(key => [key, false]));
const group = { subAccountId: 'demo-group', subAccountName: '客户通知' };
const templatePrefill = { name: '预约通知草稿', content: '您预约的服务时间为 ${time}，请准时到店。',
  signatures: ['演示科技'], templateParams: [{ name: 'time', paramType: 1 }] };
const task = { subAccount: 'demo-group', taskId: 'demo-task' };
const material = { name: '本地示例图片.png', data: sampleProof.split(',')[1] };
// 仅用于模拟既有上传回执和只读校验；不会执行实际上传或访问这个私密文件引用。
const batchPrefill = { name: '预约提醒群发', subAccount: 'demo-group', signature: '演示科技', templateId: 'demo-template',
  recipientsFile: { name: '演示名单.csv', file: 'preview/recipients.csv',
    receipt: { signature: 'preview-receipt', context: { name: '演示名单.csv', file: 'preview/recipients.csv', expires_at: 9999999999 } } } };
const scenarios = {
  qualification: [
    { id: 'image', label: '图片回显', prefill: { materialName: '演示企业资质',
      businessInfo: { businessCertificate: material } } },
  ],
  signature: [
    { id: 'image', label: '图片回显', prefill: { content: '演示科技', source: 3, signatureIdentificationID: 101,
      isLimitSubAccount: 0, trademark: { trademarkNumber: 'DEMO-001', trademarkFileList: [material] } } },
  ],
  traffic: [
    { id: 'links', label: '链接与跳转预填', prefill: { kind: 'link', data: [
      { useVolcLink: false, link: 'https://www.example.com/Notice?Source=SMS',
        linkDomainIcp: '演示文案备案号', linkDomainIcpBody: '演示科技有限公司',
        jumpLink: 'https://landing.example.com/Detail?Item=One',
        jumpLinkDomainIcp: '演示跳转备案号', jumpLinkDomainIcpBody: '演示科技有限公司' },
      { useVolcLink: true, jumpLink: 'https://landing.example.com/Activity?From=SMS',
        jumpLinkDomainIcp: '演示跳转备案号', jumpLinkDomainIcpBody: '演示科技有限公司' },
    ] } },
    { id: 'phones', label: '手机与企业号码', prefill: { kind: 'phone', data: [
      { number: '13800000000', numberPerson: '演示号主', personType: 1,
        numberProvince: '北京', numberCity: '北京' },
      { number: '4008000000', company: '演示科技有限公司', numberProvince: '江苏', numberCity: '南京' },
    ] } },
  ],
  service: [
    { id: 'renewal', label: '协议更新', serviceStatus: 'protocol_confirmation_required' },
    { id: 'pending', label: '开通待生效', serviceStatus: 'activation_pending' },
    { id: 'unknown', label: '提交结果待核实', serviceStatus: 'submission_outcome_unknown' },
    { id: 'closed', label: '服务欠费关闭', serviceStatus: 'arrears_closed' },
    { id: 'available', label: '已开通', serviceStatus: 'available' },
  ],
  template: [
    { id: 'ready', label: '通知模板核对', prefill: { ...templatePrefill, channelType: 'CN_NTC', subAccounts: ['demo-group'] } },
    { id: 'fixed', label: '固定链接已录入', prefill: { name: '链接通知', content: '详情请查看 https://example.com/Notice?Source=SMS',
      channelType: 'CN_NTC', signatures: ['演示科技'], subAccounts: ['demo-group'], templateParams: [] }, templateFixed: true },
    { id: 'fixed_missing', label: '固定引流未录入', prefill: { name: '链接通知', content: '详情请查看 https://example.com/Notice?Source=SMS',
      channelType: 'CN_NTC', signatures: ['演示科技'], subAccounts: ['demo-group'], templateParams: [] }, templateFixedMissing: true },
    { id: 'check_failure', label: '固定引流查询失败', prefill: { ...templatePrefill, channelType: 'CN_NTC', subAccounts: ['demo-group'] }, templateCheckFailure: true },
    { id: 'smb_notice', label: '小微通知变量受限', prefill: { ...templatePrefill, channelType: 'CN_NTC', subAccounts: ['demo-group'] }, templateSmb: true },
    { id: 'marketing', label: '营销变量与平台短链', prefill: { ...templatePrefill, name: '活动提醒', channelType: 'CN_MKT',
      content: '您预约的活动时间为 ${time}，拒收请回复R', subAccounts: ['demo-group'], shortUrlConfig: { isEnabled: '1' } } },
    { id: 'traffic_binding', label: '引流变量绑定', prefill: { ...templatePrefill, name: '活动链接通知',
      channelType: 'CN_NTC', content: '活动详情 ${url}', subAccounts: ['demo-group'],
      templateParams: [{ name: 'url', paramType: 2 }],
      templateTrafficDriving: [[{ name: 'url', paramType: 2, id: 12 }]] } },
    { id: 'marketing_off', label: '营销变量未开放', prefill: { ...templatePrefill, channelType: 'CN_MKT',
      content: `${templatePrefill.content} 拒收请回复R`, subAccounts: ['demo-group'] }, templateMarketingOff: true },
    { id: 'changed', label: '提交前账号变化', prefill: { ...templatePrefill, channelType: 'CN_NTC', subAccounts: ['demo-group'] }, templateChanged: true },
    { id: 'unknown', label: '模板提交结果未知', prefill: { ...templatePrefill, channelType: 'CN_NTC', subAccounts: ['demo-group'] }, templateUnknown: true },
    { id: 'missing_group', label: '预填：未指定消息组范围', prefill: { ...templatePrefill, channelType: 'CN_NTC' } },
    { id: 'missing_type', label: '预填：待补短信类型', prefill: { ...templatePrefill, subAccounts: ['demo-group'] } },
  ],
  batch: [
    { id: 'partial', label: '部分预填：待补任务名称', prefill: { ...batchPrefill, name: undefined } },
    { id: 'ready', label: '自动校验与重复号码', prefill: batchPrefill },
    { id: 'scheduled', label: '北京时间定时', prefill: { ...batchPrefill, scheduled: true,
      sendTime: Math.floor(Date.now() / 1000) + 86400 } },
    { id: 'traffic', label: '引流检查部分失败', prefill: { ...batchPrefill, checkTraffic: true }, trafficFailure: true },
    { id: 'special', label: '特殊通知正文', prefill: { ...batchPrefill, content: '请在明天下午三点到店办理业务。' }, special: true },
    { id: 'unknown_create', label: '创建结果待核实', prefill: batchPrefill, createUnknown: true },
    { id: 'existing', label: '历史任务', task },
    { id: 'read_failure', label: '历史任务：首次查询失败', task, firstReadFails: true },
  ],
};
let bridge, frame;
let scenario = {};
let taskReads = 0;
let taskStatus = 2;
let serviceAvailable = false;
let called = 0;
function displayMode(mode) {
  const expanded = mode === 'fullscreen';
  document.getElementById('mount').classList.toggle('preview-side-panel', expanded);
  if (frame) {
    frame.style.width = expanded ? '100%' : previewWidth;
    frame.style.height = expanded ? '100%' : '540px';
  }
}
function response(result, privateData = false) {
  const envelope = { success: true, result, error: null };
  return { content: [{ type: 'text', text: '模拟结果' }], structuredContent: privateData ? { ...envelope, result: null } : envelope,
    ...(privateData ? { _meta: { 'sms/form': envelope } } : {}) };
}
function templateFailure(code, message, unknown = false) {
  return { content: [], isError: true, structuredContent: { success: false, request_id: 'demo-template-check',
    error: { code, message, outcome_unknown: unknown } } };
}
function tool({ name, arguments: args }) {
  called += 1;
  document.getElementById('status').textContent = `AppBridge 已连接 · 模拟工具调用 ${called} 次 · 最近工具 ${name}`;
  if (name === 'get_qualification_requirements') return response(rank);
  if (name === 'get_account_information') return response({ businessName: '演示科技有限公司',
    userType: scenario.templateSmb ? 'smb' : 'enterprise', mktParam: scenario.templateMarketingOff ? 0 : 1 });
  if (name === 'list_qualifications') return response({ list: [{ id: 101, materialName: '演示企业资质', businessCertificateName: '演示科技有限公司', purpose: 1, auditStatus: 3, usable: true }], total: 1 });
  if (name === 'query_sms_resources') {
    const { action } = args.request;
    if (action === 'GetApplySignatureBind') return response([{ id: 101, materialName: '演示企业资质', businessCertificateName: '演示科技有限公司', purpose: 1 }]);
    if (action === 'GetSubAccountListForAgent') return response({ list: [group], total: 1 });
    if (action === 'ListSignaturesForAgent') return response({ List: [{ Signature: '演示科技', Status: 3, StatusDescription: '审核通过', Usable: true }], Total: 1 });
    if (action === 'ListBatchTemplatesForAgent') return response({ List: [{ TemplateId: 'demo-template', TemplateName: '预约通知', ChannelType: 'CN_NTC',
      TemplateContent: scenario.special ? '使用本次任务正文' : '您预约的服务时间为 ${time}，请准时到店。',
      TaskFields: scenario.special ? [{ Name: 'content', Label: '任务正文', Required: true }] : [] }], Total: 1 });
    if (action === 'GetTobTrafficDrivingLinkListForAgent') return response({ list: [
      { id: 12, link: 'https://example.com/activity' },
    ], total: 1 });
    if (action === 'GetTobTrafficDrivingPhoneListForAgent') return response({ list: [
      { id: 21, number: '4008000000' },
    ], total: 1 });
    if (action === 'ValidateBatchTaskContentForAgent') return response({ Approved: true });
    if (action === 'CheckTrafficDrivingExist') return response({ list: scenario.templateFixed || scenario.templateFixedMissing
      ? [{ paramType: 2, isExist: !scenario.templateFixedMissing, content: 'https://example.com/Notice?Source=SMS' }] : [] });
  }
  if (name === 'check_qualification_enterprise' && args.business_certificate_name === '演示待人工企业') {
    return response({ manualReview: true, code: 'enterprise_check_mismatch', requestId: 'demo-check' }, true);
  }
  if (name === 'check_qualification_enterprise' || name === 'check_qualification_person') return response({ status: 0, ticket: 'demo-ticket' }, true);
  if (name === 'recognize_qualification_document') return response({ businessCertificateName: '演示科技有限公司', unifiedSocialCreditIdentifier: 'DEMO-CREDIT', legalPersonName: '演示人员', businessCertificateValidityPeriodStart: '2020-01-01', businessCertificateValidityPeriodEnd: '长期', personName: '演示人员', personIDCard: 'DEMO-ID' }, true);
  // 本地预览不会联网或上传文件。实际字节传输由 uploads.test.jsx 的模拟 HTTP 验证。
  if (name === 'prepare_material_upload' || name === 'prepare_recipients_upload') {
    return { content: [], isError: true, structuredContent: { success: false, error: {
      code: 'preview_upload_unavailable', message: '本地样式预览不执行上传，请使用上传回归或联调环境。', outcome_unknown: false,
    } } };
  }
  if (name === 'preview_template') {
    const request = args.request;
    if (request.channelType === 'CN_NTC' && request.templateParams.length && scenario.templateSmb) {
      return templateFailure('template_account_restricted', '因短信行业风险管控，小微账号暂不支持带变量的通知模板');
    }
    if (request.channelType === 'CN_MKT' && request.templateParams.length && scenario.templateMarketingOff) {
      return templateFailure('template_account_restricted', '当前账号未允许营销模板使用变量');
    }
    if (scenario.templateCheckFailure) return templateFailure('1999', '模拟固定引流信息查询失败，请重新核对。');
    if (scenario.templateFixedMissing) return templateFailure('fixed_traffic_missing', '正文中的固定链接或联系号码尚未录入引流信息库，请先录入');
    return response({ request: { ...request, area: 'cn' },
      account: { businessName: '演示科技有限公司', userType: scenario.templateSmb ? 'smb' : 'enterprise', mktParam: 1 },
      fixedTraffic: scenario.templateFixed ? [{ paramType: 2, isExist: true, content: 'https://example.com/Notice?Source=SMS' }] : [],
      warnings: [],
      confirmation: 'a'.repeat(64) }, true);
  }
  if (name === 'submit_template') {
    if (scenario.templateChanged) return templateFailure('template_confirmation_changed', '模板参数、账号或引流核对结果已变化，请重新核对模板申请');
    if (scenario.templateUnknown) return templateFailure('1999', '模拟模板申请结果待核实，请查询模板记录。', true);
    return response({ templateId: 'demo-template', status: 1 });
  }
  if (name === 'get_batch_csv_template') return response({ value: 'phone,time\n13800000000,明天上午\n', variables: ['time'] });
  if (name === 'send_batch_test_sms') return response({ messageId: 'demo-test-sms', requestedAt: Math.floor(Date.now() / 1000) }, true);
  if (name === 'list_send_logs') return response({ list: [{ messageId: 'demo-test-sms', status: 3,
    sendTime: Date.now() - 10000, receiptTime: Date.now(), count: 1 }], total: 1 });
  if (name === 'complete_recipients_upload') {
    return response({ name: args.request.context.name, file: args.request.context.file, receipt: args.request, totalCount: 5, dupCount: 2,
      ...(args.traffic ? { trafficReport: { totalRows: 5, checkedRows: scenario.trafficFailure ? 3 : 5,
        failedRows: scenario.trafficFailure ? 2 : 0, uncheckedRows: 0, missingResourceRows: scenario.trafficFailure ? 1 : 0,
        missingRowNumbers: scenario.trafficFailure ? [2] : [],
        ...(scenario.trafficFailure ? { failures: [{ error: { code: '1999', message: '模拟引流查询失败，请稍后重新核对。' }, request_id: 'demo-traffic-query' }] } : {}) } } : {}) }, true);
  }
  if (name === 'submit_qualification') return response(1001);
  if (name === 'submit_signature') return response({ applyId: 'demo-application', status: 1 });
  if (name === 'create_batch_task') {
    if (scenario.createUnknown) return { content: [], isError: true, structuredContent: { success: false,
      error: { code: '1999', message: '模拟创建结果待确认，请先查询群发任务。', outcome_unknown: true } } };
    taskStatus = 2; return response({ taskId: 'demo-task', totalCount: 3, dupCount: 2 });
  }
  if (name === 'query_batch_tasks') {
    taskReads += 1;
    if (scenario.firstReadFails && taskReads === 1) return { content: [], isError: true, structuredContent: { success: false,
      error: { code: 'preview_query_failed', message: '模拟首次查询失败，请刷新任务状态。', outcome_unknown: false } } };
    return response({ taskId: 'demo-task', subAccount: 'demo-group', templateId: 'demo-template', signature: '演示科技', name: '演示历史任务', totalCount: 2, dupCount: 0, sendContent: '您预约的服务时间为 ${time}，请准时到店。', status: taskStatus });
  }
  if (name === 'start_batch_task') { taskStatus = 3; return response(null); }
  if (name === 'cancel_batch_task') { taskStatus = 7; return response(null); }
  if (name === 'preview_traffic_resource') return response({ count: args.request.params.data.length });
  if (name === 'submit_traffic_resources') return response('');
  if (name === 'submit_sms_service_onboarding') serviceAvailable = true;
  if (name === 'get_sms_service_onboarding' || name === 'submit_sms_service_onboarding') {
    const status = serviceAvailable ? 'available' : (scenario.serviceStatus ?? 'activation_required');
    const canSubmit = ['activation_required', 'reopening_required', 'protocol_confirmation_required'].includes(status);
    return response({
      status, businessName: '演示科技有限公司',
      protocols: canSubmit ? (status === 'protocol_confirmation_required' ? config.smsOnboarding.protocols.slice(0, 2) : config.smsOnboarding.protocols) : [],
      pricingUrl: config.smsOnboarding.pricingUrl, consoleUrl: config.smsOnboarding.consoleUrl,
      ...(canSubmit ? { confirmation: 'demo-confirmation' } : {}),
    }, true);
  }
  if (name === 'send_verification_code') return response({ messageId: 'demo-message' });
  if (name === 'verify_code') return response({ status: 0 });
  return { content: [{ type: 'text', text: '模拟器没有此工具' }], isError: true };
}

async function open() {
  const formSelect = document.getElementById('form');
  const scenarioSelect = document.getElementById('scenario');
  if (formSelect.disabled) return;
  const form = formSelect.value;
  formSelect.disabled = true; scenarioSelect.disabled = true;
  document.getElementById('status').textContent = '正在建立标准 AppBridge 连接…';
  if (bridge) { await bridge.teardownResource({}).catch(() => {}); await bridge.close(); }
  frame?.remove(); displayMode('inline'); called = 0; taskReads = 0; taskStatus = 2; serviceAvailable = false;
  scenario = (scenarios[form] ?? []).find(item => item.id === scenarioSelect.value) ?? {};
  frame = document.createElement('iframe');
  frame.title = '短信表单'; frame.style.width = previewWidth; frame.style.height = '540px';
  frame.setAttribute('sandbox', 'allow-scripts allow-same-origin');
  document.getElementById('mount').appendChild(frame);
  bridge = new AppBridge(null, { name: 'SMS local preview', version: '1' }, { serverTools: {}, downloadFile: {} }, {
    hostContext: { theme: document.getElementById('dark').checked ? 'dark' : 'light', displayMode: 'inline', availableDisplayModes: ['inline', 'fullscreen'] },
  });
  bridge.oncalltool = async params => tool(params);
  bridge.onupdatemodelcontext = async () => ({});
  bridge.onsizechange = ({ height }) => {
    if (Number.isFinite(height) && height > 0 && !document.getElementById('mount').classList.contains('preview-side-panel')) {
      frame.style.height = `${height}px`;
    }
  };
  // This local host maps the standard expanded mode to a right panel for visual verification.
  bridge.onrequestdisplaymode = async ({ mode }) => {
    const actual = mode === 'fullscreen' ? 'fullscreen' : 'inline';
    displayMode(actual);
    bridge.setHostContext({ displayMode: actual });
    document.getElementById('status').textContent = `AppBridge 已连接 · 展示模式 ${actual}`;
    return { mode: actual };
  };
  bridge.ondownloadfile = async () => ({});
  bridge.onsandboxready = () => bridge.sendSandboxResourceReady({ html });
  bridge.oninitialized = async () => {
    document.getElementById('status').textContent = 'AppBridge 已连接';
    await bridge.sendToolResult({ content: [{ type: 'text', text: '打开模拟表单' }], structuredContent: {
      success: true, form, mode: 'input', result: null,
    }, _meta: { 'sms/form': { prefill: scenario.prefill, task: scenario.task } } });
    formSelect.disabled = false;
    scenarioSelect.disabled = !scenarios[form]?.length;
  };
  await bridge.connect(new PostMessageTransport(frame.contentWindow, frame.contentWindow));
  const sandbox = new URL('/dev/sandbox.html', window.location.href);
  sandbox.hostname = window.location.hostname === 'localhost' ? '127.0.0.1' : 'localhost';
  frame.src = sandbox.href;
}
function updateScenarios() {
  const select = document.getElementById('scenario');
  const options = scenarios[document.getElementById('form').value] ?? [];
  select.replaceChildren(new Option('空白表单', ''), ...options.map(item => new Option(item.label, item.id)));
  select.disabled = options.length === 0;
}
document.getElementById('form').addEventListener('change', () => { updateScenarios(); open(); });
document.getElementById('scenario').addEventListener('change', open);
document.getElementById('wide').addEventListener('click', () => { frame.style.width = '960px'; });
document.getElementById('narrow').addEventListener('click', () => { frame.style.width = '390px'; });
document.getElementById('dark').addEventListener('change', event => bridge.setHostContext({ theme: event.target.checked ? 'dark' : 'light' }));
document.getElementById('inline').addEventListener('click', () => {
  displayMode('inline');
  bridge.setHostContext({ displayMode: 'inline' });
});
const initialForm = previewParams.get('form');
if ([...document.getElementById('form').options].some(option => option.value === initialForm)) {
  document.getElementById('form').value = initialForm;
}
document.getElementById('dark').checked = previewParams.get('theme') === 'dark';
updateScenarios();
const initialScenario = previewParams.get('scenario');
if ([...document.getElementById('scenario').options].some(option => option.value === initialScenario)) {
  document.getElementById('scenario').value = initialScenario;
}
open();
