import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { SmsApp } from './app.jsx';
import { TrafficForm } from './traffic.jsx';
import { SignatureForm, signaturePreview } from './signature.jsx';
import { BatchForm, batchPayload } from './batch.jsx';
import { OperationError, SmsFormClient, page } from './client.js';
import { batchTemplateSchema, signatureQualificationSchema } from './contracts.js';

afterEach(cleanup);
const rank = Object.fromEntries(['isOnlyTwoElement', 'isSkipOtherUse', 'needOtherUseCheck', 'operatorThreeElement', 'needOperatorImage', 'needOperatorMobile', 'responsibleThreeElement', 'needResponsibleImage', 'needResponsibleMobile', 'needBusinessCertificateImage'].map(key => [key, false]));

function client(overrides = {}) {
  return { call: vi.fn(), query: vi.fn(), upload: vi.fn(), downloadCsv: vi.fn(), report: vi.fn().mockResolvedValue(undefined), ...overrides };
}
function uploadedRecipients(name, file) {
  return { name, file, receipt: { signature: 'fixture-' + file,
    context: { name, file, expires_at: 9999999999 } } };
}
function checkedRecipients(args, totalCount = 1) {
  return { name: args.request.context.name, file: args.request.context.file,
    receipt: args.request, totalCount, dupCount: 0 };
}
function openDraft(form, prefill) {
  return { structuredContent: { form, mode: 'input' }, _meta: { 'sms/form': { prefill } } };
}
async function type(user, label, value) { await user.type(screen.getByLabelText(label), value); }
async function choose(user, label, text) {
  await user.click(screen.getByLabelText(label));
  const option = await screen.findByRole('option', { name: text });
  await waitFor(() => expect(window.getComputedStyle(option).pointerEvents).not.toBe('none'));
  await user.click(option);
}

it('引流必须先预览再确认录入，重复点击只提交一次', async () => {
  const user = userEvent.setup();
  let resolve;
  const api = client({ call: vi.fn(name => name === 'preview_traffic_resource'
    ? Promise.resolve({ count: 1 }) : new Promise(done => { resolve = done; })) });
  render(<TrafficForm client={api} />);
  await type(user, '文案链接', 'https://example.com/Path?Q=One');
  await type(user, '文案域名备案号', '备案一号');
  await type(user, '文案域名备案主体', '测试企业');
  expect(screen.queryByRole('button', { name: '确认录入' })).toBeNull();
  await user.click(screen.getByRole('button', { name: '预览录入内容' }));
  expect(api.call.mock.calls.map(([name]) => name)).toEqual(['preview_traffic_resource']);
  const submit = screen.getByRole('button', { name: '确认录入' });
  expect(submit.disabled).toBe(false);
  await user.dblClick(submit);
  expect(api.call).toHaveBeenCalledTimes(2);
  expect(api.call.mock.calls[1][1].request.params.data[0].link).toBe('https://example.com/Path?Q=One');
  resolve('');
  await screen.findByText('引流信息已提交');
  expect(api.report).toHaveBeenCalledWith({ form: 'traffic', state: 'accepted', kind: 'link', count: 1 });
});

it('未知写入结果不会解锁重试或返回修改', async () => {
  const user = userEvent.setup();
  const api = client({ call: vi.fn().mockResolvedValueOnce({ count: 1 })
    .mockRejectedValueOnce(new OperationError('结果待确认', { unknown: true })) });
  render(<TrafficForm client={api} />);
  await type(user, '文案链接', 'https://example.com'); await type(user, '文案域名备案号', '备案'); await type(user, '文案域名备案主体', '企业');
  await user.click(screen.getByRole('button', { name: '预览录入内容' }));
  await user.click(screen.getByRole('button', { name: '确认录入' }));
  await screen.findByText('结果待确认');
  for (const name of ['确认录入', '预览录入内容', '添加一条', '结束本次录入']) {
    expect(screen.getByRole('button', { name }).disabled).toBe(true);
  }
  expect(screen.getByLabelText('文案链接').disabled).toBe(true);
  expect(screen.getByLabelText('使用火山短链').getAttribute('aria-disabled')).toBe('true');
  expect(api.call).toHaveBeenCalledTimes(2);
});

it('签名申请使用已选资质的归属和私密附件，不修改原始签名', () => {
  const values = { content: '测试签名', source: 2, appIcp: { appIcpFilling: '备案一号' } };
  const qualification = { id: 12, purpose: 2, materialName: '示例资质', businessCertificateName: '示例测试签名公司' };
  const { request: result, attachmentNames } = signaturePreview(values, qualification, 'all', { app: [{ fileContent: 'private/app', fileSuffix: 'png', name: 'app.png' }], trademark: [], other: [] });
  expect(result).toMatchObject({ content: '测试签名', purpose: 2, signatureIdentificationID: 12, isLimitSubAccount: 0, subAccounts: [] });
  expect(result.appIcp.appIcpFileList).toEqual([{ fileType: 16, fileContent: 'private/app', fileSuffix: 'png' }]);
  expect(attachmentNames).toEqual(['app.png']);
  expect(() => signaturePreview(values, { ...qualification, purpose: 3 }, 'all', { app: [], trademark: [], other: [] })).toThrow('审核通过的资质');
});

it('签名表单保留消息组范围选择和提交前确认', async () => {
  const user = userEvent.setup();
  const api = client({ call: vi.fn().mockResolvedValue({ applyId: 'application', status: 1 }),
    query: vi.fn(async action => action === 'GetApplySignatureBind'
      ? [{ id: 12, materialName: '示例资质', businessCertificateName: '示例企业', purpose: 1 }]
      : { list: [{ subAccountId: 'group', subAccountName: '唯一启用组' }], total: 1 }),
  });
  render(<SignatureForm client={api} />);
  await screen.findByText('唯一启用组');
  expect(screen.getByLabelText('签名内容').value).toBe('示例企业');
  await user.clear(screen.getByLabelText('签名内容'));
  await type(user, '签名内容', '测试签名');
  await user.click(screen.getByRole('button', { name: '下一步' }));
  await user.click(screen.getByRole('button', { name: '核对申请' }));
  expect(api.call.mock.calls.filter(([name]) => name === 'submit_signature')).toHaveLength(0);
  await user.click(screen.getByRole('button', { name: '强制提交' }));
  expect(api.call).not.toHaveBeenCalled();
  await user.click(screen.getByRole('button', { name: '确认承担风险并提交' }));
  await screen.findByText('签名申请已提交');
  expect(api.query.mock.calls.filter(([action]) => action === 'GetApplySignatureBind')).toEqual([
    ['GetApplySignatureBind', {}],
  ]);
  expect(api.call).toHaveBeenCalledTimes(1);
  expect(api.call).toHaveBeenCalledWith('submit_signature', {
    request: expect.objectContaining({ signatureIdentificationID: 12, purpose: 1, content: '测试签名' }),
  }, { write: true });
});

it('签名候选一次读取完整数组，超过一百条的预填资质也不补查', async () => {
  const rows = Array.from({ length: 128 }, (_, index) => ({
    id: index + 1, purpose: 1, materialName: `资质${index + 1}`,
    businessCertificateName: `主体${index + 1}`,
  }));
  const api = client({ query: vi.fn(async action => action === 'GetApplySignatureBind'
    ? rows : { list: [], total: 0 }) });
  render(<SignatureForm client={api} prefill={{ signatureIdentificationID: 128, isLimitSubAccount: 0 }} />);
  await waitFor(() => expect(screen.getByLabelText('签名内容').value).toBe('主体128'));
  expect(api.query.mock.calls.filter(([action]) => action === 'GetApplySignatureBind')).toEqual([
    ['GetApplySignatureBind', {}],
  ]);
  expect(api.call).not.toHaveBeenCalled();
});

it.each([[null], [[]]])('签名候选为空时不补查完整资质列表或生成默认选项：%s', async candidates => {
  const user = userEvent.setup();
  const api = client({ query: vi.fn(async action => action === 'GetApplySignatureBind'
    ? candidates : { list: [], total: 0 }) });
  render(<SignatureForm client={api} prefill={{ content: '测试签名', isLimitSubAccount: 0 }} />);
  await screen.findByRole('button', { name: '下一步' });
  await choose(user, '签名归属类型', '自用');
  await user.click(screen.getByRole('button', { name: '下一步' }));
  await user.click(screen.getByRole('button', { name: '核对申请' }));
  await screen.findByText('请选择审核通过的资质。');
  expect(api.query.mock.calls.filter(([action]) => action === 'GetApplySignatureBind')).toHaveLength(1);
  expect(api.call).not.toHaveBeenCalled();
});

it('失效的预填资质不触发详情补查，也不自动改选其他资质', async () => {
  const api = client({ query: vi.fn(async action => action === 'GetApplySignatureBind'
    ? [{ id: 12, purpose: 1, materialName: '可用资质', businessCertificateName: '示例企业' }]
    : { list: [], total: 0 }) });
  render(<SignatureForm client={api} prefill={{ signatureIdentificationID: 99 }} />);
  await screen.findByText('预填资质当前不可用，请重新选择。');
  expect(screen.getByLabelText('签名内容').value).toBe('');
  expect(api.query.mock.calls.filter(([action]) => action === 'GetApplySignatureBind')).toHaveLength(1);
  expect(api.call).not.toHaveBeenCalled();
});

it('签名候选拒绝分页对象，不把旧接口响应当作新接口数组', async () => {
  const api = client({ query: vi.fn().mockResolvedValue({ list: [], total: 0 }) });
  render(<SignatureForm client={api} />);
  await screen.findByText('资质候选返回不完整，请重新查询。');
  expect(api.query.mock.calls.filter(([action]) => action === 'GetApplySignatureBind')).toHaveLength(1);
  expect(api.call).not.toHaveBeenCalled();
});

it('候选接口不可用时显示查询错误，不回退到完整资质列表', async () => {
  const api = client({ query: vi.fn(async action => {
    if (action === 'GetApplySignatureBind') throw new OperationError('候选接口尚不可用。', { code: 'InvalidActionOrVersion' });
    return { list: [], total: 0 };
  }) });
  render(<SignatureForm client={api} />);
  await screen.findByText('候选接口尚不可用。');
  expect(api.query.mock.calls.filter(([action]) => action === 'GetApplySignatureBind')).toHaveLength(1);
  expect(api.call).not.toHaveBeenCalled();
});

it('群发一次确认创建并启动，启动后取消仍单独确认', async () => {
  const user = userEvent.setup();
  let started = false;
  let cancelled = false;
  const api = client({
    query: vi.fn(async action => {
      if (action === 'GetSubAccountListForAgent') return { list: [{ subAccountId: 'g', subAccountName: '通知组' }], total: 1 };
      if (action === 'ListSignaturesForAgent') return { List: [{ Signature: '测试签名' }], Total: 1 };
      return { List: [{ TemplateId: 't', TemplateName: '通知模板', ChannelType: 'CN_NTC', TemplateContent: '原始正文', TaskFields: [] }], Total: 1 };
    }),
    call: vi.fn(async (name, args) => {
      if (name === 'complete_recipients_upload') return checkedRecipients(args);
      if (name === 'get_batch_csv_template') return { value: 'phone\n13800000000\n', variables: [] };
      if (name === 'create_batch_task') return { taskId: 'task-1', totalCount: 1, dupCount: 0 };
      if (name === 'start_batch_task') { started = true; return null; }
      if (name === 'cancel_batch_task') { cancelled = true; return null; }
      if (name === 'query_batch_tasks') return { taskId: 'task-1', subAccount: 'g', templateId: 't', sendContent: '实际任务正文', status: cancelled ? 7 : started ? 3 : 2 };
      throw new Error('unexpected call');
    }),
    upload: vi.fn().mockResolvedValue(uploadedRecipients('list.csv', 'private/list.csv')),
  });
  render(<BatchForm client={api} />);
  await waitFor(() => expect(api.query).toHaveBeenCalled());
  await type(user, '任务名称', '测试任务');
  await choose(user, '消息组', '通知组');
  await choose(user, '短信签名', '测试签名');
  await choose(user, '群发模板', '通知模板');
  await screen.findByRole('button', { name: '点击下载模板' });
  fireEvent.change(screen.getByLabelText('群发 CSV 名单'), { target: { files: [new File(['phone\n13800000000\n'], 'list.csv', { type: 'text/csv' })] } });
  await screen.findByText('文件已就绪。');
  await user.click(screen.getByRole('button', { name: '核对群发任务' }));
  await screen.findByText('我已核对任务信息、文件校验结果和发送时间，同意创建任务并启动发送');
  await user.click(screen.getByRole('button', { name: '返回修改' }));
  await user.click(screen.getByRole('button', { name: '核对群发任务' }));
  await screen.findByText('我已核对任务信息、文件校验结果和发送时间，同意创建任务并启动发送');
  expect(api.call.mock.calls.filter(([name]) => name === 'complete_recipients_upload')).toHaveLength(1);
  await user.click(screen.getByText('我已核对任务信息、文件校验结果和发送时间，同意创建任务并启动发送'));
  await user.click(screen.getByRole('button', { name: '确认创建并启动' }));
  await screen.findByText('群发任务已创建并确认发送');
  await waitFor(() => expect(started).toBe(true));
  expect(api.call.mock.calls.filter(([name]) => name === 'start_batch_task')).toHaveLength(1);
  expect(screen.queryByRole('button', { name: '核对并启动' })).toBeNull();
  expect(screen.queryByRole('button', { name: '重试确认发送' })).toBeNull();
  expect(screen.queryByRole('button', { name: '确认启动群发' })).toBeNull();
  expect(api.call.mock.calls.find(([name]) => name === 'create_batch_task')[1].request.idempotencyKey).toBeTruthy();
  await waitFor(() => expect(screen.getByRole('button', { name: '取消任务' }).disabled).toBe(false));
  await user.click(screen.getByRole('button', { name: '刷新任务状态' }));
  await waitFor(() => expect(screen.getByRole('button', { name: '取消任务' }).disabled).toBe(false));
  await user.click(screen.getByRole('button', { name: '取消任务' }));
  const cancel = await screen.findByRole('button', { name: '确认取消任务' });
  expect(cancel.disabled).toBe(true);
  expect(cancelled).toBe(false);
  await user.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await user.click(cancel);
  await waitFor(() => expect(cancelled).toBe(true));
  expect(api.call.mock.calls.filter(([name]) => name === 'cancel_batch_task')).toHaveLength(1);
});

it('宿主预填签名、适用消息组和证明材料，真实查询后才选中资源', async () => {
  const user = userEvent.setup();
  const proof = { name: '商标证明.pdf', data: 'Zml4dHVyZQ==' };
  const api = client({
    query: vi.fn(async action => action === 'GetApplySignatureBind'
      ? [{ id: 12, purpose: 1, materialName: '可用资质', businessCertificateName: '宿主填写的签名公司' }]
      : { list: [{ subAccountId: 'g', subAccountName: '已核实的消息组' }], total: 1 }),
    upload: vi.fn().mockResolvedValue({ name: proof.name, fileContent: 'fixture/proof', fileSuffix: 'pdf' }),
  });
  render(<SmsApp client={api} ready supported toolResult={openDraft('signature', {
    content: '宿主填写的签名', source: 3, signatureIdentificationID: 12,
    subAccounts: ['g'], isLimitSubAccount: 1, desc: ' 保留说明原文 ', projectName: '宿主项目',
    trademark: { trademarkCn: '测试品牌', trademarkEn: 'Example', trademarkNumber: '0001',
      trademarkFileList: [proof] },
  })} />);
  expect(await screen.findByText('已核实的消息组')).toBeTruthy();
  expect(screen.getByLabelText('签名内容').value).toBe('宿主填写的签名');
  expect(screen.getByLabelText('申请说明').value).toBe(' 保留说明原文 ');
  await user.click(screen.getByRole('button', { name: '下一步' }));
  expect(screen.getByText('12【宿主填写的签名公司】· 自用')).toBeTruthy();
  expect(screen.getByLabelText('商标中文名').value).toBe('测试品牌');
  expect(screen.getByLabelText('商标英文名').value).toBe('Example');
  expect(screen.getByLabelText('商标注册号').value).toBe('0001');
  expect(screen.queryByLabelText('项目名称（选填）')).toBeNull();
  expect(screen.getByText('商标证明.pdf（待上传）')).toBeTruthy();
  await user.click(screen.getByRole('button', { name: '核对申请' }));
  expect(await screen.findByText('请先上传或移除待上传的材料。')).toBeTruthy();
  expect(api.upload).not.toHaveBeenCalled();
  fireEvent.click(document.querySelector('[data-material="trademark"] .arco-upload-list-start-icon'));
  expect(await screen.findByText('商标证明.pdf')).toBeTruthy();
  await user.click(screen.getByRole('button', { name: '核对申请' }));
  expect((await screen.findByRole('button', { name: '确认提交' })).disabled).toBe(false);
  await user.click(screen.getByRole('button', { name: '返回修改' }));
  await user.click(screen.getByRole('button', { name: '上一步' }));
  await choose(user, '签名类型', '公司全称／简称');
  await user.click(screen.getByRole('button', { name: '下一步' }));
  await user.click(screen.getByRole('button', { name: '核对申请' }));
  expect((await screen.findByRole('button', { name: '确认提交' })).disabled).toBe(false);
  expect(screen.queryByText('商标证明.pdf')).toBeNull();
  expect(api.call).not.toHaveBeenCalled();
  expect(api.query.mock.calls.filter(([action]) => action === 'GetApplySignatureBind')).toHaveLength(1);
});

it('宿主预填引流链接，普通链接与火山短链保留各自行的备案信息', async () => {
  const user = userEvent.setup();
  const api = client();
  render(<SmsApp client={api} ready supported toolResult={openDraft('traffic', { kind: 'link', data: [
    { useVolcLink: false, protocol: 'http', link: 'http://example.com/Original?Q=One',
      linkDomainIcp: '测试文案备案号', linkDomainIcpBody: '文案域名主体' },
    { useVolcLink: true, jumpLink: 'https://example.com/Go?Next=2',
      jumpLinkDomainIcp: '测试跳转备案号', jumpLinkDomainIcpBody: '跳转域名主体' },
  ] })} />);
  expect(screen.getByLabelText('文案链接').value).toBe('http://example.com/Original?Q=One');
  expect(screen.getAllByLabelText('跳转链接').map(field => field.value)).toEqual(['', 'https://example.com/Go?Next=2']);
  expect(screen.getByLabelText('文案域名备案号').value).toBe('测试文案备案号');
  expect(screen.getAllByLabelText('跳转域名备案主体').map(field => field.value)).toEqual(['', '跳转域名主体']);
  await user.click(screen.getByRole('button', { name: '预览录入内容' }));
  expect((await screen.findByRole('button', { name: '确认录入' })).disabled).toBe(false);
  expect(api.call.mock.calls.map(([name]) => name)).toEqual(['preview_traffic_resource']);
});

it('宿主预填引流手机和企业号码，私密字段只在对应行显示', () => {
  const api = client();
  render(<SmsApp client={api} ready supported toolResult={openDraft('traffic', { kind: 'phone', data: [
    { number: '13800000000', numberPerson: '测试号主', personType: 1,
      personId: 'fixture-id', numberProvince: '北京', numberCity: '北京' },
    { numberType: 2, number: '4008000000', company: '测试企业', numberProvince: '江苏', numberCity: '南京' },
  ] })} />);
  expect(screen.getAllByRole('textbox', { name: '联系号码' }).map(field => field.value)).toEqual(['13800000000', '4008000000']);
  expect(screen.getByLabelText('号码所属人').value).toBe('测试号主');
  expect(screen.getByLabelText('证件号码').value).toBe('fixture-id');
  expect(screen.getByText('居民身份证')).toBeTruthy();
  expect(screen.getByLabelText('号码所属企业').value).toBe('测试企业');
  expect(screen.getAllByLabelText('号码归属省份').map(field => field.value)).toEqual(['北京', '江苏']);
  expect(screen.getAllByLabelText('号码归属城市').map(field => field.value)).toEqual(['北京', '南京']);
  expect(api.call).not.toHaveBeenCalled();
});

it('引流部分预填识别文案协议，火山短链缺少备案时在字段旁校验', async () => {
  const user = userEvent.setup();
  const api = client();
  render(<TrafficForm client={api} prefill={{ kind: 'link', data: [
    { link: 'http://example.com/Path', linkDomainIcp: '备案号', linkDomainIcpBody: '备案主体' },
    { useVolcLink: true, jumpLink: 'https://example.com/Go' },
  ] }} />);
  expect(screen.getByLabelText('文案链接').value).toBe('http://example.com/Path');
  expect(screen.getAllByLabelText('跳转链接').map(field => field.value)).toEqual(['', 'https://example.com/Go']);
  expect(screen.getByLabelText('文案链接协议').textContent).toContain('http');
  await user.click(screen.getByRole('button', { name: '预览录入内容' }));
  expect(screen.getAllByLabelText('跳转域名备案号')[1].getAttribute('aria-invalid')).toBe('true');
  expect(screen.getAllByLabelText('跳转域名备案主体')[1].getAttribute('aria-invalid')).toBe('true');
  expect(screen.getAllByText('此项必填')).toHaveLength(2);
  expect(api.call).not.toHaveBeenCalled();
});

it('群发表单保留部分预填，选消息组后再核对签名、模板和待上传名单', async () => {
  const user = userEvent.setup();
  const date = new Date(Date.now() + 86400000 + 8 * 3600000).toISOString().slice(0, 10);
  const sendTime = Date.parse(date + 'T10:15:13+08:00') / 1000;
  const list = { name: '宿主名单.csv', data: 'cGhvbmUKMTM4MDAwMDAwMDAK' };
  const template = { TemplateId: 't', TemplateName: '特殊通知', ChannelType: 'CN_NTC',
    TaskFields: [{ Name: 'content', Label: '任务正文', Required: true }] };
  const api = client({
    query: vi.fn(async action => {
      if (action === 'GetSubAccountListForAgent') return { list: [{ subAccountId: 'g', subAccountName: '测试消息组' }], total: 1 };
      if (action === 'ListSignaturesForAgent') return { List: [{ Signature: '已知签名' }], Total: 1 };
      if (action === 'ValidateBatchTaskContentForAgent') return { Approved: true };
      return { List: [template], Total: 1 };
    }),
    call: vi.fn(async (name, args) => name === 'complete_recipients_upload' ? checkedRecipients(args) : { value: 'phone\n', variables: [] }),
    upload: vi.fn().mockResolvedValue(uploadedRecipients(list.name, 'verified/list.csv')),
  });
  render(<SmsApp client={api} ready supported toolResult={openDraft('batch', {
    name: '双十一通知', signature: '已知签名', templateId: 't', content: ' 保留原文 ',
    scheduled: true, sendTime, recipientsFile: list,
  })} />);
  expect(screen.getByLabelText('任务名称').value).toBe('双十一通知');
  expect(Date.parse(screen.getByLabelText('定时时间').value.replace(' ', 'T') + '+08:00') / 1000).toBe(Math.floor(sendTime / 60) * 60);
  expect(screen.getByText('宿主名单.csv（待上传）')).toBeTruthy();
  expect(screen.getByRole('button', { name: '上传 宿主名单.csv' }).disabled).toBe(true);
  await choose(user, '消息组', '测试消息组');
  expect(await screen.findByText('已知签名')).toBeTruthy();
  expect(await screen.findAllByText('特殊通知')).toHaveLength(2);
  expect(screen.getByLabelText('任务正文').value).toBe(' 保留原文 ');
  expect(api.upload).not.toHaveBeenCalled();
  await user.click(screen.getByRole('button', { name: '上传 宿主名单.csv' }));
  expect(await screen.findByText('文件已就绪。')).toBeTruthy();
  expect(api.upload).toHaveBeenCalledWith(list, { kind: 'recipients', sub_account: 'g', template_id: 't' });
  await user.click(screen.getByRole('button', { name: '核对群发任务' }));
  await screen.findByText('我已核对任务信息、文件校验结果和发送时间，同意创建任务并启动发送');
  expect((await screen.findByRole('button', { name: '确认创建并启动' })).disabled).toBe(true);
  expect(screen.getByText(/10:15:13（北京时间）/)).toBeTruthy();
  expect(api.call.mock.calls.map(([name]) => name)).toEqual(['get_batch_csv_template', 'complete_recipients_upload']);
});

it('群发表单预选首屏以外的已核实资源，并允许用户重新选择', async () => {
  const user = userEvent.setup();
  const group = { subAccountId: 'chosen-group', subAccountName: '预填消息组' };
  const signature = { Signature: '预填签名' };
  const template = {
    TemplateId: 'chosen-template', TemplateName: '预填群发模板',
    ChannelType: 'CN_MKT', TemplateContent: '预填模板正文',
  };
  const api = client({
    query: vi.fn(async (action, params) => {
      if (action === 'GetSubAccountListForAgent') {
        return params.subAccount ? { list: [group], total: 1 }
          : { list: [{ subAccountId: 'other', subAccountName: '手动消息组' }], total: 2 };
      }
      if (action === 'ListSignaturesForAgent') {
        return params.Signature ? { List: [signature], Total: 1 }
          : { List: [{ Signature: '其他签名' }], Total: 2 };
      }
      return params.TemplateId ? { List: [template], Total: 1 } : { List: [], Total: 1 };
    }),
    call: vi.fn().mockResolvedValue({ value: 'phone\n', variables: [] }),
  });
  render(<SmsApp client={api} ready supported toolResult={openDraft('batch', {
    subAccount: 'chosen-group', signature: '预填签名', templateId: 'chosen-template',
  })} />);
  await screen.findByRole('button', { name: '点击下载模板' });
  expect(screen.getByText('预填消息组')).toBeTruthy();
  expect(screen.getByText('预填签名')).toBeTruthy();
  expect(screen.getAllByText('预填群发模板')).toHaveLength(2);
  expect(screen.getByText('预填模板正文')).toBeTruthy();
  expect(api.call.mock.calls).toEqual([['get_batch_csv_template', {
    sub_account: 'chosen-group', template_id: 'chosen-template', include_variables: true,
  }]]);
  expect(api.upload).not.toHaveBeenCalled();

  await choose(user, '消息组', '手动消息组');
  expect(screen.queryByText('预填签名')).toBeNull();
  expect(screen.queryByText('预填模板正文')).toBeNull();
  expect(screen.queryByRole('button', { name: '点击下载模板' })).toBeNull();
});

it('预填模板不可用时保留已核实的消息组和签名，让用户重选', async () => {
  const api = client({
    query: vi.fn(async action => {
      if (action === 'GetSubAccountListForAgent') {
        return { list: [{ subAccountId: 'g', subAccountName: '可用消息组' }], total: 1 };
      }
      if (action === 'ListSignaturesForAgent') {
        return { List: [{ Signature: '可用签名' }], Total: 1 };
      }
      return { List: [], Total: 0 };
    }),
  });
  render(<BatchForm client={api} prefill={{ subAccount: 'g', signature: '可用签名', templateId: 'stale' }} />);
  await screen.findByText(/模板配置缺失/);
  expect(screen.getByText('可用消息组')).toBeTruthy();
  expect(screen.getByText('可用签名')).toBeTruthy();
  expect(screen.queryByRole('button', { name: '点击下载模板' })).toBeNull();
  expect(api.call).not.toHaveBeenCalled();
});

it('名单示例首次查询失败后，可重选精查到的同一个模板', async () => {
  const user = userEvent.setup();
  const template = { TemplateId: 't', TemplateName: '可重试模板', ChannelType: 'CN_MKT' };
  const api = client({
    query: vi.fn(async (action, params) => {
      if (action === 'GetSubAccountListForAgent') return { list: [{ subAccountId: 'g' }], total: 1 };
      if (action === 'ListSignaturesForAgent') return { List: [{ Signature: '可用签名' }], Total: 1 };
      return params.TemplateId ? { List: [template], Total: 1 } : { List: [], Total: 1 };
    }),
    call: vi.fn().mockRejectedValueOnce(new OperationError('名单示例暂未取得'))
      .mockResolvedValueOnce({ value: 'phone\n', variables: [] }),
  });
  render(<BatchForm client={api} prefill={{ subAccount: 'g', signature: '可用签名', templateId: 't' }} />);
  await screen.findByText('名单示例暂未取得');
  expect(screen.queryByRole('button', { name: '点击下载模板' })).toBeNull();
  await choose(user, '群发模板', '可重试模板');
  await screen.findByRole('button', { name: '点击下载模板' });
  expect(api.call.mock.calls).toEqual([
    ['get_batch_csv_template', { sub_account: 'g', template_id: 't', include_variables: true }],
    ['get_batch_csv_template', { sub_account: 'g', template_id: 't', include_variables: true }],
  ]);
});

it('开通表单展示协议，单独确认后提交，刷新未生效时不再显示提交', async () => {
  const user = userEvent.setup();
  const view = {
    businessName: '测试企业', status: 'activation_required', confirmation: 'confirm-current',
    protocols: [{ id: 17, title: '测试服务协议', url: 'https://example.com/terms' }],
    pricingUrl: 'https://example.com/pricing', consoleUrl: 'https://example.com/console',
  };
  const api = client({ call: vi.fn(async name => name === 'get_sms_service_onboarding'
    ? view : { status: 'activation_pending', requestId: 'activation-request' }) });
  render(<SmsApp client={api} ready supported toolResult={openDraft('service', {})} />);
  expect(await screen.findByText('测试服务协议', { exact: false })).toBeTruthy();
  const submit = screen.getByRole('button', { name: '同意协议并开通' });
  expect(submit.disabled).toBe(true);
  expect(api.call.mock.calls).toEqual([['get_sms_service_onboarding']]);
  await user.click(screen.getByRole('checkbox'));
  await user.click(submit);
  await screen.findByText('开通请求已受理，等待状态更新');
  expect(api.call).toHaveBeenCalledWith('submit_sms_service_onboarding', { confirmation: 'confirm-current' }, { write: true });
  await user.click(screen.getByRole('button', { name: '刷新服务状态' }));
  expect(screen.queryByRole('button', { name: '同意协议并开通' })).toBeNull();
});

it('引流检查随名单上传自动执行，试发仍须单独确认并查询对应回执', async () => {
  const user = userEvent.setup();
  const template = { TemplateId: 't', ChannelType: 'CN_NTC', TemplateContent: '查看 ${url}' };
  const api = client({
    query: vi.fn(async action => {
      if (action === 'GetSubAccountListForAgent') return { List: [{ subAccountId: 'g' }], Total: 1 };
      if (action === 'ListSignaturesForAgent') return { List: [{ Signature: '签名' }], Total: 1 };
      return { List: [template], Total: 1 };
    }),
    call: vi.fn(async (name, args) => {
      if (name === 'get_batch_csv_template') return { value: 'phone,url\n', variables: ['url'] };
      if (name === 'send_batch_test_sms') return { messageId: 'test-sms-id', requestedAt: 1000 };
      if (name === 'list_send_logs') return { List: [{ messageId: 'test-sms-id', status: 3,
        SendTime: Date.parse('2026-11-13T10:15:13+08:00'), ReceiptTime: Date.parse('2026-11-13T10:15:20+08:00') }], Total: 1 };
      if (name === 'complete_recipients_upload') {
        return { ...checkedRecipients(args, 2), trafficReport: { checkedRows: 1, totalRows: 2, failedRows: 0, uncheckedRows: 1, missingResourceRows: 1, missingRowNumbers: [2] } };
      }
      throw new Error('unexpected write');
    }),
    upload: vi.fn().mockResolvedValue(uploadedRecipients('预填名单.csv', 'private-file')),
  });
  const file = { name: '预填名单.csv', data: 'Zml4dHVyZQ==' };
  render(<BatchForm client={api} prefill={{
    name: '测试任务', subAccount: 'g', signature: '签名', templateId: 't',
    checkTraffic: true, recipientsFile: file,
  }} />);
  await screen.findByLabelText('测试手机号');
  await type(user, '测试手机号', '13800000000');
  await type(user, 'url', 'https://example.com/test');
  await user.click(screen.getByRole('button', { name: '发送测试短信' }));
  const send = screen.getByRole('button', { name: '确认发送测试短信' });
  expect(send.disabled).toBe(true);
  expect(api.call.mock.calls.filter(([name]) => name === 'send_batch_test_sms')).toHaveLength(0);
  await user.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await user.click(send);
  await screen.findByText('已收到成功回执');
  expect(screen.getByText('测试短信已提交，请在测试手机上确认触达效果。')).toBeTruthy();
  expect(screen.getByText('2026年11月13日 10:15:13（北京时间）')).toBeTruthy();
  expect(screen.getByText('2026年11月13日 10:15:20（北京时间）')).toBeTruthy();
  expect(api.call).toHaveBeenCalledWith('list_send_logs', expect.objectContaining({ message_id: 'test-sms-id' }));
  await user.click(screen.getByRole('button', { name: '上传 预填名单.csv' }));
  await screen.findByText('缺少资源的 CSV 行号 2');
  expect(api.call.mock.calls.filter(([name]) => name === 'complete_recipients_upload')).toHaveLength(1);
  expect(api.call).toHaveBeenCalledWith('complete_recipients_upload', { request: expect.objectContaining({ signature: 'fixture-private-file' }), columns: ['phone', 'url'], traffic: expect.objectContaining({ template_id: 't', content: '查看 ${url}' }) });
  expect(screen.getByRole('button', { name: '确认创建并启动' }).disabled).toBe(true);
  await user.click(screen.getByRole('button', { name: '返回修改' }));
  await user.click(screen.getByRole('button', { name: '核对群发任务' }));
  await screen.findByText('缺少资源的 CSV 行号 2');
  expect(api.call.mock.calls.filter(([name]) => name === 'complete_recipients_upload')).toHaveLength(2);
  await user.click(screen.getByRole('button', { name: '返回修改' }));
  expect(screen.getByText('已收到成功回执')).toBeTruthy();
  await user.click(screen.getByRole('button', { name: '刷新发送结果' }));
  expect(api.call.mock.calls.filter(([name]) => name === 'list_send_logs')).toHaveLength(2);
  expect(api.query.mock.calls.filter(([action]) => action === 'ListBatchTemplatesForAgent')).toHaveLength(1);
  expect(api.call.mock.calls.filter(([name]) => name === 'get_batch_csv_template')).toHaveLength(1);
  expect(api.call).toHaveBeenCalledWith('send_batch_test_sms', { request: {
    sub_account: 'g', signature: '签名', template_id: 't', mobile: '13800000000',
    template_params: { url: 'https://example.com/test' },
  } }, { write: true });
});

it('特殊通知保持任务正文和幂等键，拒绝未知任务字段', () => {
  const values = { name: '任务', subAccount: 'g', signature: '签名', scheduled: false, content: ' 原始正文 ' };
  const template = { TemplateId: 't', ChannelType: 'CN_NTC', TaskFields: [{ Name: 'content', Required: true }] };
  expect(batchPayload(values, template, { file: 'key' }, 'stable')).toMatchObject({ content: ' 原始正文 ', idempotencyKey: 'stable', sendTime: 0 });
  expect(() => batchPayload(values, { ...template, TaskFields: [{ Name: 'unsupported' }] }, { file: 'key' }, 'stable')).toThrow('尚未支持');
});

it('群发核对复用已加载定义和检查结果，更换文件后重新检查', async () => {
  const user = userEvent.setup();
  const api = client({
    query: vi.fn(async action => {
      if (action === 'GetSubAccountListForAgent') return { list: [{ subAccountId: 'g' }], total: 1 };
      if (action === 'ListSignaturesForAgent') return { List: [{ Signature: '签名' }], Total: 1 };
      return { List: [{ TemplateId: 't', ChannelType: 'CN_NTC', TemplateContent: '测试正文' }], Total: 1 };
    }),
    call: vi.fn(async (name, args) => {
      if (name === 'get_batch_csv_template') return { value: 'phone\n', variables: [] };
      if (name === 'complete_recipients_upload') return checkedRecipients(args);
      throw new Error('unexpected write');
    }),
    upload: vi.fn(async file => uploadedRecipients(file.name, file.name)),
  });
  render(<BatchForm client={api} prefill={{ name: '测试任务', subAccount: 'g', signature: '签名', templateId: 't' }} />);
  await screen.findByRole('button', { name: '点击下载模板' });
  const upload = async name => {
    fireEvent.change(screen.getByLabelText('群发 CSV 名单'), { target: { files: [new File(['phone\n13800000000\n'], name)] } });
    await screen.findByText('文件已就绪。');
  };
  const prepare = async () => {
    await user.click(screen.getByRole('button', { name: '核对群发任务' }));
    await screen.findByText('我已核对任务信息、文件校验结果和发送时间，同意创建任务并启动发送');
    await user.click(screen.getByRole('button', { name: '返回修改' }));
  };
  await upload('first.csv');
  await prepare();
  await prepare();
  expect(api.call.mock.calls.filter(([name]) => name === 'complete_recipients_upload')).toHaveLength(1);
  await upload('second.csv');
  await prepare();
  const checks = api.call.mock.calls.filter(([name]) => name === 'complete_recipients_upload');
  expect(checks.map(([, args]) => args.request.context.file)).toEqual(['first.csv', 'second.csv']);
  expect(checks.every(([, args]) => JSON.stringify(args.columns) === '["phone"]')).toBe(true);
  expect(api.query.mock.calls.filter(([action]) => action === 'ListBatchTemplatesForAgent')).toHaveLength(1);
  expect(api.call.mock.calls.filter(([name]) => name === 'get_batch_csv_template')).toHaveLength(1);
});

it('不完整的资源记录在渲染选择器之前失败，不改写未知业务字段', () => {
  expect(() => page({ List: [{ TemplateId: 't', ChannelType: 'CN_NTC', TaskFields: {} }], Total: 1 }, batchTemplateSchema)).toThrow('资源字段');
  expect(signatureQualificationSchema.safeParse({ id: 12, purpose: 1 }).success).toBe(false);
  const record = { TemplateId: 't', ChannelType: 'CN_NTC', TaskFields: [], customBusinessField: 'keep' };
  expect(page({ List: [record], Total: 1 }, batchTemplateSchema).rows[0]).toBe(record);
});

it('历史结果和不支持 Apps 的宿主都不重放业务调用', () => {
  const api = client();
  const view = render(<SmsApp client={api} ready supported toolResult={{ structuredContent: { form: 'qualification', success: true, result: 123 } }} />);
  expect(screen.getByText('此操作已返回结果')).toBeTruthy();
  expect(api.call).not.toHaveBeenCalled();
  view.rerender(<SmsApp client={api} ready supported={false} toolResult={openDraft('batch', {})} />);
  expect(screen.getByText(/当前客户端不支持表单操作/)).toBeTruthy();
  expect(api.call).not.toHaveBeenCalled();
});

describe('标准 AppBridge 调用边界', () => {
  it.each(['1999', 'SY:0500', 1007])('后端错误 %s 保留原文与完整响应，由宿主判断结果', async code => {
    const message = ' 后端原文\n结果待确认，RequestId 保持原样 ';
    const backend = { ResponseMetadata: { Error: { Code: code, Message: message, Details: ['原字段'] } } };
    const app = { callServerTool: vi.fn().mockResolvedValue({ isError: true, structuredContent: {
      success: false, request_id: 'api-request', error: { code, message, http_status: 503, backend_response: backend },
    } }) };
    await expect(new SmsFormClient(app).call('submit_template', {}, { write: true })).rejects.toMatchObject({
      code, message, requestId: 'api-request', httpStatus: 503, backendResponse: backend, unknown: false,
    });
    expect(app.callServerTool).toHaveBeenCalledTimes(1);
  });
  it('宿主连接异常保留异常信息，不推断业务最终结果', async () => {
    const app = { callServerTool: vi.fn().mockRejectedValue(Object.assign(new Error('bridge disconnected'), { code: -32000 })) };
    await expect(new SmsFormClient(app).call('submit_template', {}, { write: true })).rejects.toMatchObject({
      message: 'bridge disconnected', code: -32000, unknown: false,
    });
  });
  it.each([undefined, null, 'false', 'true', 0, 1])('不从缺失或异常结果标记 %s 推断业务结果', async flag => {
    const app = { callServerTool: vi.fn().mockResolvedValue({ isError: true, structuredContent: {
      success: false, error: { code: 'fixture', message: '待核对', ...(flag === undefined ? {} : { outcome_unknown: flag }) },
    } }) };
    await expect(new SmsFormClient(app).call('submit_signature', {}, { write: true })).rejects.toMatchObject({ message: '待核对', unknown: false });
    expect(app.callServerTool).toHaveBeenCalledTimes(1);
  });
  it('本地参数错误与格式异常都不推断短信业务最终结果', async () => {
    const app = { callServerTool: vi.fn().mockResolvedValue({ isError: true, structuredContent: {
      success: false, error: { code: 'invalid_arguments', message: '参数不完整', outcome_unknown: false },
    } }) };
    await expect(new SmsFormClient(app).call('submit_signature', {}, { write: true })).rejects.toMatchObject({ unknown: false });
    app.callServerTool.mockResolvedValue({ isError: true, structuredContent: {
      success: true, error: { code: 'fixture', message: '矛盾响应', outcome_unknown: false },
    } });
    await expect(new SmsFormClient(app).call('submit_signature', {}, { write: true })).rejects.toMatchObject({ unknown: false });
  });
  it('只从私密元数据读取 OCR，宿主上下文更新失败不改变调用结果', async () => {
    const app = { callServerTool: vi.fn().mockResolvedValue({ structuredContent: { success: true, result: null }, _meta: { 'sms/form': { success: true, result: { personName: 'private' } } } }), updateModelContext: vi.fn().mockRejectedValue(new Error('unsupported')) };
    const api = new SmsFormClient(app);
    expect(await api.call('recognize_qualification_document', {})).toEqual({ personName: 'private' });
    await api.report({ form: 'qualification', state: 'submitted', qualificationId: 123 });
    expect(JSON.stringify(app.updateModelContext.mock.calls)).not.toContain('private');
  });
  it('写操作连接中断透传异常且不自动重试', async () => {
    const app = { callServerTool: vi.fn().mockRejectedValue(new Error('raw transport private data')) };
    const api = new SmsFormClient(app);
    await expect(api.call('submit_signature', {}, { write: true })).rejects.toMatchObject({ message: 'raw transport private data', unknown: false });
    expect(app.callServerTool).toHaveBeenCalledTimes(1);
  });
});
