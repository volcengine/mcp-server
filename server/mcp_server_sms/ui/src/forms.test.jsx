import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { SmsApp } from './app.jsx';
import { TrafficForm } from './traffic.jsx';
import { QualificationForm, qualificationPayload } from './qualification.jsx';
import { SignatureForm, signaturePayload } from './signature.jsx';
import { BatchForm, batchPayload } from './batch.jsx';
import { OperationError, SmsFormClient, page } from './client.js';
import { batchTemplateSchema, qualificationSchema } from './contracts.js';

afterEach(cleanup);
const rank = Object.fromEntries(['isOnlyTwoElement', 'isSkipOtherUse', 'needOtherUseCheck', 'operatorThreeElement', 'needOperatorImage', 'needOperatorMobile', 'responsibleThreeElement', 'needResponsibleImage', 'needResponsibleMobile', 'needBusinessCertificateImage'].map(key => [key, false]));
const record = { personName: '测试人员', personIDCard: 'fixture-identity', certificateType: 0 };
const business = { businessCertificateType: 1, businessCertificateName: '测试企业', unifiedSocialCreditIdentifier: 'fixture-credit', legalPersonName: '测试法人', businessCertificateValidityPeriodStart: '2020-01-01', businessCertificateValidityPeriodEnd: '长期' };

function client(overrides = {}) {
  return { call: vi.fn(), query: vi.fn(), upload: vi.fn(), downloadCsv: vi.fn(), report: vi.fn().mockResolvedValue(undefined), ...overrides };
}
async function type(user, label, value) { await user.type(screen.getByLabelText(label), value); }
async function choose(user, label, text) {
  await user.click(screen.getByLabelText(label));
  const option = await screen.findByRole('option', { name: text });
  await waitFor(() => expect(window.getComputedStyle(option).pointerEvents).not.toBe('none'));
  await user.click(option);
}

it('引流必须先预览并勾选确认，重复点击只提交一次', async () => {
  const user = userEvent.setup();
  let resolve;
  const api = client({ call: vi.fn(() => new Promise(done => { resolve = done; })) });
  render(<TrafficForm client={api} />);
  await type(user, '文案链接', 'https://example.com/Path?Q=One');
  await type(user, '文案域名备案号', '备案一号');
  await type(user, '文案域名备案主体', '测试企业');
  await user.click(screen.getByRole('button', { name: '核对信息' }));
  expect(api.call).not.toHaveBeenCalled();
  const submit = screen.getByRole('button', { name: '确认提交' });
  expect(submit.disabled).toBe(true);
  await user.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await user.dblClick(submit);
  expect(api.call).toHaveBeenCalledTimes(1);
  expect(api.call.mock.calls[0][1].request.params.data[0].link).toBe('https://example.com/Path?Q=One');
  resolve(null);
  await screen.findByText('录入请求已受理');
  expect(api.report).toHaveBeenCalledWith({ form: 'traffic', state: 'accepted', kind: 'link', count: 1 });
});

it('未知写入结果不会解锁重试或返回修改', async () => {
  const user = userEvent.setup();
  const api = client({ call: vi.fn().mockRejectedValue(new OperationError('结果待确认', { unknown: true })) });
  render(<TrafficForm client={api} />);
  await type(user, '文案链接', 'https://example.com'); await type(user, '文案域名备案号', '备案'); await type(user, '文案域名备案主体', '企业');
  await user.click(screen.getByRole('button', { name: '核对信息' }));
  await user.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await user.click(screen.getByRole('button', { name: '确认提交' }));
  await screen.findByText('结果待确认');
  expect(screen.getByRole('button', { name: '确认提交' }).disabled).toBe(true);
  expect(screen.getByRole('button', { name: '返回修改' }).disabled).toBe(true);
  expect(api.call).toHaveBeenCalledTimes(1);
});

it('资质复用经办人时保留正确材料类型，缺失校验不会生成跳过票据', () => {
  const values = { purpose: 1, sameOperator: true, business, operator: record };
  const file = { fileContent: 'private/ref', fileSuffix: 'png' };
  const files = { operator: { front: file, back: file }, other: [] };
  const result = qualificationPayload(values, files, { business: 'business-ticket', operator: 'person-ticket' }, {}, rank, { userType: 'enterprise' });
  expect(result.operatorPerson.personCertificate.map(item => item.fileType)).toEqual([8, 9]);
  expect(result.responsiblePersonInfo.personCertificate.map(item => item.fileType)).toEqual([10, 11]);
  expect(result.responsibleCheckTicket).toBe('person-ticket');
  expect(result.materialName).toBe('测试企业');
  expect(() => qualificationPayload(values, files, {}, {}, rank, { userType: 'enterprise' })).toThrow('企业信息校验');
  expect(() => qualificationPayload(values, { operator: { front: file }, other: [] }, { business: 'b', operator: 'p' }, {}, rank, { userType: 'enterprise' })).toThrow('身份证正反面');
  expect(() => qualificationPayload(values, files, { business: 'b', operator: 'p' }, {}, { ...rank, needBusinessCertificateImage: true }, { userType: 'enterprise' })).toThrow('营业证件');
});

it('资质表单通过校验后仍需用户确认，模型上下文只收到申请编号', async () => {
  const user = userEvent.setup();
  const api = client({ call: vi.fn(async (name) => {
    if (name === 'get_qualification_requirements') return rank;
    if (name === 'get_account_information') return { businessName: '测试企业', userType: 'enterprise' };
    if (name === 'check_qualification_enterprise' || name === 'check_qualification_person') return { status: 0, ticket: 'private-ticket' };
    if (name === 'apply_qualification') return 123;
    throw new Error('unexpected call');
  }) });
  render(<QualificationForm client={api} />);
  await screen.findByText('当前账号主体：测试企业。营业证件照片选填。');
  for (const [label, value] of [['企业名称', '测试企业'], ['统一社会信用代码', 'fixture-credit'], ['法人姓名', '测试法人'], ['证件有效期开始', '2020-01-01'], ['证件有效期结束（长期请填写“长期”）', '长期']]) await type(user, label, value);
  await user.click(screen.getByRole('button', { name: '校验企业信息' }));
  await screen.findByText('校验已通过');
  await user.click(screen.getByRole('button', { name: '下一步' }));
  await type(user, '经办人姓名', '测试人员'); await type(user, '经办人证件号码', 'fixture-identity');
  await user.click(screen.getByRole('button', { name: '校验经办人信息' }));
  await screen.findByText('校验已通过');
  await user.click(screen.getByRole('button', { name: '下一步' }));
  await user.click(screen.getByRole('button', { name: '核对申请信息' }));
  expect(api.call.mock.calls.filter(([name]) => name === 'apply_qualification')).toHaveLength(0);
  await user.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await user.click(screen.getByRole('button', { name: '确认提交' }));
  await screen.findByText('资质申请已提交');
  const request = api.call.mock.calls.find(([name]) => name === 'apply_qualification')[1].request;
  expect(request.operatorPerson.personIDCard).toBe('fixture-identity');
  expect(request.responsibleCheckTicket).toBe('private-ticket');
  expect(api.report).toHaveBeenCalledWith({ form: 'qualification', state: 'submitted', qualificationId: 123 });
});

it('签名申请使用已选资质的归属和私密附件，不修改原始签名', () => {
  const values = { content: '测试签名', source: 2, appIcpFilling: '备案一号' };
  const qualification = { id: 12, purpose: 2, usable: true, auditStatus: 3 };
  const result = signaturePayload(values, qualification, 'all', { app: [{ fileContent: 'private/app', fileSuffix: 'png', name: 'app.png' }], trademark: [], other: [] });
  expect(result).toMatchObject({ content: '测试签名', purpose: 2, signatureIdentificationID: 12, isLimitSubAccount: 0, subAccounts: [] });
  expect(result.appIcp.appIcpFileList).toEqual([{ fileType: 16, fileContent: 'private/app', fileSuffix: 'png' }]);
  expect(() => signaturePayload(values, { ...qualification, usable: false }, 'all', { app: [], trademark: [], other: [] })).toThrow('可用的资质');
});

it('签名表单保留消息组范围选择和提交前确认', async () => {
  const user = userEvent.setup();
  const api = client({ call: vi.fn(async name => name === 'list_qualifications'
    ? { list: [{ id: 12, materialName: '示例资质', purpose: 1, auditStatus: 3, usable: true }], total: 1 }
    : { applyId: 'application', status: 1 }), query: vi.fn().mockResolvedValue({ list: [], total: 0 }) });
  render(<SignatureForm client={api} />);
  await waitFor(() => expect(api.query).toHaveBeenCalled());
  await type(user, '签名内容', '测试签名');
  await choose(user, '关联资质', '示例资质 · 自用');
  await user.click(screen.getByText('全部消息组'));
  await user.click(screen.getByRole('button', { name: '核对申请信息' }));
  expect(api.call.mock.calls.filter(([name]) => name === 'apply_signature')).toHaveLength(0);
  await user.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await user.click(screen.getByRole('button', { name: '确认提交' }));
  await screen.findByText('签名申请结果');
});

it('群发创建、启动和启动后取消分别要求确认', async () => {
  const user = userEvent.setup();
  let started = false;
  let cancelled = false;
  const api = client({
    query: vi.fn(async action => {
      if (action === 'GetSubAccountListForAgent') return { list: [{ subAccountId: 'g', subAccountName: '通知组' }], total: 1 };
      if (action === 'ListSignaturesForAgent') return { List: [{ Signature: '测试签名' }], Total: 1 };
      return { List: [{ TemplateId: 't', TemplateName: '通知模板', ChannelType: 'CN_NTC', TemplateContent: '原始正文', TaskFields: [] }], Total: 1 };
    }),
    call: vi.fn(async name => {
      if (name === 'get_batch_csv_template') return { value: 'phone\n13800000000\n' };
      if (name === 'create_batch_task') return { taskId: 'task-1', totalCount: 1, dupCount: 0 };
      if (name === 'start_batch_task') { started = true; return null; }
      if (name === 'cancel_batch_task') { cancelled = true; return null; }
      if (name === 'get_batch_task') return { taskId: 'task-1', subAccount: 'g', templateId: 't', sendContent: '实际任务正文', status: cancelled ? 7 : started ? 3 : 2 };
      throw new Error('unexpected call');
    }),
    upload: vi.fn().mockResolvedValue({ name: 'list.csv', file: 'private/list.csv', totalCount: 1, dupCount: 0 }),
  });
  render(<BatchForm client={api} />);
  await waitFor(() => expect(api.query).toHaveBeenCalled());
  await type(user, '任务名称', '测试任务');
  await choose(user, '消息组', '通知组');
  await choose(user, '短信签名', '测试签名');
  await choose(user, '群发模板', '通知模板');
  await screen.findByRole('button', { name: '下载名单模板' });
  fireEvent.change(screen.getByLabelText('群发 CSV 名单'), { target: { files: [new File(['phone\n13800000000\n'], 'list.csv', { type: 'text/csv' })] } });
  await screen.findByText(/已校验 1 条记录/);
  await user.click(screen.getByRole('button', { name: '核对群发任务' }));
  await user.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await user.click(screen.getByRole('button', { name: '确认创建任务' }));
  await screen.findByText('群发任务已创建');
  expect(started).toBe(false);
  await waitFor(() => expect(screen.getByRole('button', { name: '核对并启动' }).disabled).toBe(false));
  await user.click(screen.getByRole('button', { name: '核对并启动' }));
  await screen.findByText('实际任务正文');
  expect(screen.getByRole('button', { name: '确认启动群发' }).disabled).toBe(true);
  await user.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await user.click(screen.getByRole('button', { name: '确认启动群发' }));
  await waitFor(() => expect(started).toBe(true));
  expect(api.call.mock.calls.filter(([name]) => name === 'start_batch_task')).toHaveLength(1);
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

it('特殊通知保持任务正文和幂等键，拒绝未知任务字段', () => {
  const values = { name: '任务', subAccount: 'g', signature: '签名', scheduled: false, content: ' 原始正文 ' };
  const template = { TemplateId: 't', ChannelType: 'CN_NTC', TaskFields: [{ Name: 'content', Required: true }] };
  expect(batchPayload(values, template, { file: 'key' }, 'stable')).toMatchObject({ content: ' 原始正文 ', idempotencyKey: 'stable', sendTime: 0 });
  expect(() => batchPayload(values, { ...template, TaskFields: [{ Name: 'unsupported' }] }, { file: 'key' }, 'stable')).toThrow('尚未支持');
});

it('不完整的资源记录在渲染选择器之前失败，不改写未知业务字段', () => {
  expect(() => page({ List: [{ TemplateId: 't', ChannelType: 'CN_NTC', TaskFields: {} }], Total: 1 }, batchTemplateSchema)).toThrow('资源字段');
  expect(() => page({ list: [{ id: 12, auditStatus: 3, usable: true }], total: 1 }, qualificationSchema)).toThrow('资源字段');
  const record = { TemplateId: 't', ChannelType: 'CN_NTC', TaskFields: [], customBusinessField: 'keep' };
  expect(page({ List: [record], Total: 1 }, batchTemplateSchema).rows[0]).toBe(record);
});

it('历史结果和不支持 Apps 的宿主都不重放业务调用', () => {
  const api = client();
  const view = render(<SmsApp client={api} ready supported initial={{ form: 'qualification', success: true, result: 123 }} />);
  expect(screen.getByText('此操作已返回结果')).toBeTruthy();
  expect(api.call).not.toHaveBeenCalled();
  view.rerender(<SmsApp client={api} ready supported={false} initial={{ form: 'batch', mode: 'input' }} />);
  expect(screen.getByText(/当前客户端不支持表单操作/)).toBeTruthy();
  expect(api.call).not.toHaveBeenCalled();
});

describe('标准 AppBridge 调用边界', () => {
  it.each([undefined, null, 'false', 'true', 0, 1])('缺失或异常结果标记 %s 不能解除写入锁', async flag => {
    const app = { callServerTool: vi.fn().mockResolvedValue({ isError: true, structuredContent: {
      success: false, error: { code: 'fixture', message: '待核对', ...(flag === undefined ? {} : { outcome_unknown: flag }) },
    } }) };
    await expect(new SmsFormClient(app).call('apply_signature', {}, { write: true })).rejects.toMatchObject({ unknown: true });
    expect(app.callServerTool).toHaveBeenCalledTimes(1);
  });
  it('只有完整且明确的失败响应允许修改后重新提交', async () => {
    const app = { callServerTool: vi.fn().mockResolvedValue({ isError: true, structuredContent: {
      success: false, error: { code: 'invalid_arguments', message: '参数不完整', outcome_unknown: false },
    } }) };
    await expect(new SmsFormClient(app).call('apply_signature', {}, { write: true })).rejects.toMatchObject({ unknown: false });
    app.callServerTool.mockResolvedValue({ isError: true, structuredContent: {
      success: true, error: { code: 'fixture', message: '矛盾响应', outcome_unknown: false },
    } });
    await expect(new SmsFormClient(app).call('apply_signature', {}, { write: true })).rejects.toMatchObject({ unknown: true });
  });
  it('只从私密元数据读取 OCR，宿主上下文更新失败不改变调用结果', async () => {
    const app = { callServerTool: vi.fn().mockResolvedValue({ structuredContent: { success: true, result: null }, _meta: { 'sms/form': { success: true, result: { personName: 'private' } } } }), updateModelContext: vi.fn().mockRejectedValue(new Error('unsupported')) };
    const api = new SmsFormClient(app);
    expect(await api.call('recognize_qualification_document', { private: true })).toEqual({ personName: 'private' });
    await api.report({ form: 'qualification', state: 'submitted', qualificationId: 123 });
    expect(JSON.stringify(app.updateModelContext.mock.calls)).not.toContain('private');
  });
  it('写操作连接中断保留未知结果且不重试', async () => {
    const app = { callServerTool: vi.fn().mockRejectedValue(new Error('raw transport private data')) };
    const api = new SmsFormClient(app);
    await expect(api.call('apply_signature', {}, { write: true })).rejects.toMatchObject({ unknown: true });
    expect(app.callServerTool).toHaveBeenCalledTimes(1);
  });
});
