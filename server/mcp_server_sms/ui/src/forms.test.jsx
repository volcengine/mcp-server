import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { SmsApp } from './app.jsx';
import { TrafficForm } from './traffic.jsx';
import { QualificationForm, qualificationPreview } from './qualification.jsx';
import { SignatureForm, signaturePreview } from './signature.jsx';
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

it('引流必须先预览并勾选确认，重复点击只提交一次', async () => {
  const user = userEvent.setup();
  let resolve;
  const api = client({ call: vi.fn(name => name === 'preview_traffic_resource'
    ? Promise.resolve({ count: 1 }) : new Promise(done => { resolve = done; })) });
  render(<TrafficForm client={api} />);
  await type(user, '文案链接', 'https://example.com/Path?Q=One');
  await type(user, '文案域名备案号', '备案一号');
  await type(user, '文案域名备案主体', '测试企业');
  await user.click(screen.getByRole('button', { name: '核对信息' }));
  expect(api.call.mock.calls.map(([name]) => name)).toEqual(['preview_traffic_resource']);
  const submit = screen.getByRole('button', { name: '确认提交' });
  expect(submit.disabled).toBe(true);
  await user.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await user.dblClick(submit);
  expect(api.call).toHaveBeenCalledTimes(2);
  expect(api.call.mock.calls[1][1].request.params.data[0].link).toBe('https://example.com/Path?Q=One');
  resolve({ resourceIds: [17], verified: true });
  await screen.findByText('引流资源已录入并核对');
  expect(api.report).toHaveBeenCalledWith({ form: 'traffic', state: 'verified', kind: 'link', count: 1, resourceIds: [17] });
});

it('未知写入结果不会解锁重试或返回修改', async () => {
  const user = userEvent.setup();
  const api = client({ call: vi.fn().mockResolvedValueOnce({ count: 1 })
    .mockRejectedValueOnce(new OperationError('结果待确认', { unknown: true })) });
  render(<TrafficForm client={api} />);
  await type(user, '文案链接', 'https://example.com'); await type(user, '文案域名备案号', '备案'); await type(user, '文案域名备案主体', '企业');
  await user.click(screen.getByRole('button', { name: '核对信息' }));
  await user.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await user.click(screen.getByRole('button', { name: '确认提交' }));
  await screen.findByText('结果待确认');
  expect(screen.getByRole('button', { name: '确认提交' }).disabled).toBe(true);
  expect(screen.getByRole('button', { name: '返回修改' }).disabled).toBe(true);
  expect(api.call).toHaveBeenCalledTimes(2);
});

it('资质复用经办人时保留正确材料类型，缺失校验不会生成跳过票据', () => {
  const values = { purpose: 1, sameOperator: true, business, operator: record };
  const file = { fileContent: 'private/ref', fileSuffix: 'png' };
  const files = { operator: { front: file, back: file }, other: [] };
  const { request: result } = qualificationPreview(values, files, { business: 'business-ticket', operator: 'person-ticket' }, {}, rank, { userType: 'enterprise' });
  expect(result.operatorPerson.personCertificate.map(item => item.fileType)).toEqual([8, 9]);
  expect(result.responsiblePersonInfo.personCertificate.map(item => item.fileType)).toEqual([10, 11]);
  expect(result.responsibleCheckTicket).toBe('person-ticket');
  expect(result.materialName).toBe('测试企业');
  expect(() => qualificationPreview(values, files, {}, {}, rank, { userType: 'enterprise' })).toThrow('企业信息校验');
  expect(() => qualificationPreview(values, { operator: { front: file }, other: [] }, { business: 'b', operator: 'p' }, {}, rank, { userType: 'enterprise' })).toThrow('身份证正反面');
  expect(() => qualificationPreview(values, files, { business: 'b', operator: 'p' }, {}, { ...rank, needBusinessCertificateImage: true }, { userType: 'enterprise' })).toThrow('营业证件');
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
  render(<QualificationForm client={api} prefill={{ legalPerson: {
    certificateType: 1, personCertificate: { document: { name: '不提交的证件.png', data: 'Zml4dHVyZQ==' } },
  } }} />);
  await screen.findByText('当前账号主体：测试企业。营业证件照片选填。');
  for (const [label, value] of [['企业名称', '测试企业'], ['统一社会信用代码', 'fixture-credit'], ['法人姓名', '测试法人'], ['证件有效期开始', '2020-01-01'], ['证件有效期结束（长期请填写“长期”）', '长期']]) await type(user, label, value);
  await user.click(screen.getByRole('button', { name: '校验企业信息' }));
  await screen.findByText('校验已通过');
  await user.click(screen.getByRole('button', { name: '下一步' }));
  expect(document.activeElement).toBe(screen.getByRole('heading', { name: '人员信息', exact: true }));
  await user.click(screen.getByRole('button', { name: '上一步' }));
  expect(screen.getByLabelText('企业名称').value).toBe('测试企业');
  expect(screen.getByText('校验已通过')).toBeTruthy();
  await user.click(screen.getByRole('button', { name: '下一步' }));
  await type(user, '经办人姓名', '测试人员'); await type(user, '经办人证件号码', 'fixture-identity');
  expect(screen.getByText('不提交的证件.png（待上传）')).toBeTruthy();
  await user.click(screen.getByText('补充法人证件信息（选填）'));
  await user.click(screen.getByRole('button', { name: '校验经办人信息' }));
  await screen.findByText('校验已通过');
  await user.click(screen.getByRole('button', { name: '下一步' }));
  expect(document.activeElement).toBe(screen.getByRole('heading', { name: '授权与补充材料', exact: true }));
  await user.click(screen.getByRole('button', { name: '核对申请信息' }));
  expect(screen.queryByText('不提交的证件.png')).toBeNull();
  expect(api.call.mock.calls.filter(([name]) => name === 'apply_qualification')).toHaveLength(0);
  await user.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await user.click(screen.getByRole('button', { name: '确认提交' }));
  await screen.findByText('资质申请已提交');
  const request = api.call.mock.calls.find(([name]) => name === 'apply_qualification')[1].request;
  expect(request.legalPerson).toBeUndefined();
  expect(request.operatorPerson.personIDCard).toBe('fixture-identity');
  expect(request.responsibleCheckTicket).toBe('private-ticket');
  expect(api.report).toHaveBeenCalledWith({ form: 'qualification', state: 'submitted', qualificationId: 123 });
});

it('签名申请使用已选资质的归属和私密附件，不修改原始签名', () => {
  const values = { content: '测试签名', source: 2, appIcpFilling: '备案一号' };
  const qualification = { id: 12, purpose: 2, usable: true, auditStatus: 3, businessCertificateName: '示例测试签名公司' };
  const { request: result, attachmentNames } = signaturePreview(values, qualification, 'all', { app: [{ fileContent: 'private/app', fileSuffix: 'png', name: 'app.png' }], trademark: [], other: [] });
  expect(result).toMatchObject({ content: '测试签名', purpose: 2, signatureIdentificationID: 12, isLimitSubAccount: 0, subAccounts: [] });
  expect(result.appIcp.appIcpFileList).toEqual([{ fileType: 16, fileContent: 'private/app', fileSuffix: 'png' }]);
  expect(attachmentNames).toEqual(['app.png']);
  expect(() => signaturePreview(values, { ...qualification, usable: false }, 'all', { app: [], trademark: [], other: [] })).toThrow('可用的资质');
});

it('签名表单保留消息组范围选择和提交前确认', async () => {
  const user = userEvent.setup();
  const api = client({ call: vi.fn(async name => name === 'list_qualifications'
    ? { list: [{ id: 12, materialName: '示例资质', businessCertificateName: '示例企业', purpose: 1, auditStatus: 3, usable: true }], total: 1 }
    : { applyId: 'application', status: 1 }), query: vi.fn().mockResolvedValue({
    list: [{ subAccountId: 'group', subAccountName: '唯一启用组' }], total: 1,
  }) });
  render(<SignatureForm client={api} />);
  await screen.findByText('唯一启用组');
  expect(screen.getByLabelText('签名内容').value).toBe('示例企业');
  await user.clear(screen.getByLabelText('签名内容'));
  await type(user, '签名内容', '测试签名');
  await user.click(screen.getByRole('button', { name: '核对申请信息' }));
  expect(api.call.mock.calls.filter(([name]) => name === 'apply_signature')).toHaveLength(0);
  await user.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  const submit = screen.getByRole('button', { name: '确认承担风险并提交' });
  expect(submit.disabled).toBe(true);
  await user.click(screen.getByText('我了解签名可能审核或报备失败，仍要提交'));
  await user.click(submit);
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

it('宿主预填资质的企业、人员及材料，校验和上传仍由用户触发', async () => {
  const user = userEvent.setup();
  const draft = name => ({ name, data: 'Zml4dHVyZQ==' });
  const api = client({
    call: vi.fn(async name => name === 'get_qualification_requirements' ? rank
      : { businessName: '当前账号主体', userType: 'smb' }),
    upload: vi.fn(async file => ({ name: file.name, fileContent: 'fixture/uploaded', fileSuffix: 'png' })),
  });
  render(<SmsApp client={api} ready supported toolResult={openDraft('qualification', {
    materialName: '宿主填写资质', purpose: 2, sameOperator: false, includeLegal: true,
    businessInfo: { ...business, businessCertificate: draft('营业执照.png') },
    operatorPerson: { personName: record.personName, personIDCard: record.personIDCard, personMobile: '13800000000',
      personCertificate: { front: draft('经办人正面.png'), back: draft('经办人反面.png') } },
    responsiblePersonInfo: { personName: '独立责任人', personIDCard: 'fixture-responsible' },
    legalPerson: { certificateType: 1, personName: '法人补充姓名', personIDCard: 'fixture-passport',
      personCertificate: { document: draft('法人护照.png') } },
    powerOfAttorney: [draft('委托书.png')], otherMaterials: [draft('补充材料.png')],
  })} />);
  expect((await screen.findByLabelText('企业名称')).value).toBe('测试企业');
  expect(screen.getByLabelText(/资质名称/).value).toBe('宿主填写资质');
  expect(screen.getByLabelText('统一社会信用代码').value).toBe('fixture-credit');
  expect(screen.getByText('营业执照.png（待上传）')).toBeTruthy();
  await user.click(screen.getByRole('button', { name: '下一步' }));
  expect(screen.getByLabelText('经办人证件号码').value).toBe('fixture-identity');
  expect(screen.getByLabelText('经办人手机号').value).toBe('13800000000');
  expect(screen.getByLabelText('经办人短信验证码').value).toBe('');
  expect(screen.getByLabelText('责任人姓名').value).toBe('独立责任人');
  expect(screen.getByLabelText('法人证件号码').value).toBe('fixture-passport');
  expect(screen.getByText('护照')).toBeTruthy();
  for (const name of ['经办人正面.png', '经办人反面.png', '法人护照.png']) {
    expect(screen.getByText(name + '（待上传）')).toBeTruthy();
  }
  await user.click(screen.getByRole('button', { name: '下一步' }));
  expect(screen.getByText('委托书.png（待上传）')).toBeTruthy();
  expect(screen.getByText('补充材料.png（待上传）')).toBeTruthy();
  expect(api.call.mock.calls.map(([name]) => name)).toEqual(['get_qualification_requirements', 'get_account_information']);
  expect(api.upload).not.toHaveBeenCalled();
  await user.click(screen.getByRole('button', { name: '上传 委托书.png' }));
  expect(await screen.findByText('委托书.png')).toBeTruthy();
  expect(api.upload).toHaveBeenCalledWith(draft('委托书.png'), { kind: 'material', category: 'authorization' });
  await user.click(screen.getByRole('button', { name: '核对申请信息' }));
  expect(await screen.findByText('请先完成企业信息校验。')).toBeTruthy();
  expect(api.call).not.toHaveBeenCalledWith('apply_qualification', expect.anything(), expect.anything());
});

it('宿主预填签名、适用消息组和证明材料，真实查询后才选中资源', async () => {
  const user = userEvent.setup();
  const proof = { name: '商标证明.pdf', data: 'Zml4dHVyZQ==' };
  const api = client({
    call: vi.fn(async (name, args) => args.qualification_id
      ? { list: [{ id: 12, purpose: 1, auditStatus: 3, usable: true, materialName: '可用资质', businessCertificateName: '宿主填写的签名公司' }], total: 1 }
      : { list: [], total: 1 }),
    query: vi.fn(async (action, params) => params.subAccount
      ? { list: [{ subAccountId: 'g', subAccountName: '已核实的消息组' }], total: 1 }
      : { list: [], total: 1 }),
    upload: vi.fn().mockResolvedValue({ name: proof.name, fileContent: 'fixture/proof', fileSuffix: 'pdf' }),
  });
  render(<SmsApp client={api} ready supported toolResult={openDraft('signature', {
    content: '宿主填写的签名', source: 3, signatureIdentificationID: 12,
    subAccounts: ['g'], isLimitSubAccount: 1, desc: ' 保留说明原文 ', projectName: '宿主项目',
    trademark: { trademarkCn: '测试品牌', trademarkEn: 'Example', trademarkNumber: '0001',
      trademarkFileList: [proof] },
  })} />);
  expect(await screen.findByText('可用资质 · 自用')).toBeTruthy();
  expect(await screen.findByText('已核实的消息组')).toBeTruthy();
  expect(screen.getByLabelText('签名内容').value).toBe('宿主填写的签名');
  expect(screen.getByLabelText('商标中文名').value).toBe('测试品牌');
  expect(screen.getByLabelText('商标英文名').value).toBe('Example');
  expect(screen.getByLabelText('商标注册号').value).toBe('0001');
  expect(screen.getByLabelText('申请说明（选填）').value).toBe(' 保留说明原文 ');
  expect(screen.getByLabelText('项目名称（选填）').value).toBe('宿主项目');
  expect(screen.getByText('商标证明.pdf（待上传）')).toBeTruthy();
  await user.click(screen.getByRole('button', { name: '核对申请信息' }));
  expect(await screen.findByText('请先上传或移除待上传的材料。')).toBeTruthy();
  expect(api.upload).not.toHaveBeenCalled();
  await user.click(screen.getByRole('button', { name: '上传 商标证明.pdf' }));
  expect(await screen.findByText('商标证明.pdf')).toBeTruthy();
  await user.click(screen.getByRole('button', { name: '核对申请信息' }));
  expect((await screen.findByRole('button', { name: '确认提交' })).disabled).toBe(true);
  expect(screen.getByText('商标证明.pdf')).toBeTruthy();
  await user.click(screen.getByRole('button', { name: '返回修改' }));
  await choose(user, '签名来源', '公司全称／简称');
  await user.click(screen.getByRole('button', { name: '核对申请信息' }));
  expect((await screen.findByRole('button', { name: '确认提交' })).disabled).toBe(true);
  expect(screen.queryByText('商标证明.pdf')).toBeNull();
  expect(api.call.mock.calls.every(([name]) => name === 'list_qualifications')).toBe(true);
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
  expect(screen.getByLabelText('跳转链接').value).toBe('https://example.com/Go?Next=2');
  expect(screen.getByLabelText('文案域名备案号').value).toBe('测试文案备案号');
  expect(screen.getByLabelText('跳转域名备案主体').value).toBe('跳转域名主体');
  await user.click(screen.getByRole('button', { name: '核对信息' }));
  expect((await screen.findByRole('button', { name: '确认提交' })).disabled).toBe(true);
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

it('引流部分预填显示跳转字段，保留缺失协议让客户确认', async () => {
  const user = userEvent.setup();
  const api = client();
  render(<TrafficForm client={api} prefill={{ kind: 'link', data: [
    { link: 'http://example.com/Path', linkDomainIcp: '备案号', linkDomainIcpBody: '备案主体' },
    { jumpLink: 'https://example.com/Go' },
  ] }} />);
  expect(screen.getByLabelText('文案链接').value).toBe('http://example.com/Path');
  expect(screen.getByLabelText('跳转链接').value).toBe('https://example.com/Go');
  await user.click(screen.getByRole('button', { name: '核对信息' }));
  expect(await screen.findByText('请填写文案链接协议。')).toBeTruthy();
  expect(api.call).not.toHaveBeenCalled();
});

it('群发表单保留部分预填，选消息组后再核对签名、模板和待上传名单', async () => {
  const user = userEvent.setup();
  const sendTime = Date.parse('2027-11-11T10:15:13+08:00') / 1000;
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
    call: vi.fn().mockResolvedValue({ value: 'phone\n' }),
    upload: vi.fn().mockResolvedValue({ name: list.name, file: 'verified/list.csv', totalCount: 1, dupCount: 0 }),
  });
  render(<SmsApp client={api} ready supported toolResult={openDraft('batch', {
    name: '双十一通知', signature: '已知签名', templateId: 't', content: ' 保留原文 ',
    scheduled: true, sendTime, recipientsFile: list,
  })} />);
  expect(screen.getByLabelText('任务名称').value).toBe('双十一通知');
  expect(Date.parse(screen.getByLabelText('发送时间（北京时间）').value + '+08:00') / 1000).toBe(sendTime);
  expect(screen.getByText('宿主名单.csv（待上传）')).toBeTruthy();
  expect(screen.getByRole('button', { name: '上传 宿主名单.csv' }).disabled).toBe(true);
  await choose(user, '消息组', '测试消息组');
  expect(await screen.findByText('已知签名')).toBeTruthy();
  expect(await screen.findByText('特殊通知')).toBeTruthy();
  expect(screen.getByLabelText('任务正文').value).toBe(' 保留原文 ');
  expect(api.upload).not.toHaveBeenCalled();
  await user.click(screen.getByRole('button', { name: '上传 宿主名单.csv' }));
  expect(await screen.findByText(/已校验 1 条记录/)).toBeTruthy();
  expect(api.upload).toHaveBeenCalledWith(list, { kind: 'recipients', sub_account: 'g', template_id: 't' });
  await user.click(screen.getByRole('button', { name: '核对群发任务' }));
  expect((await screen.findByRole('button', { name: '确认创建任务' })).disabled).toBe(true);
  expect(screen.getByText(/10:15:13（北京时间）/)).toBeTruthy();
  expect(api.call.mock.calls.every(([name]) => name === 'get_batch_csv_template')).toBe(true);
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
    call: vi.fn().mockResolvedValue({ value: 'phone\n' }),
  });
  render(<SmsApp client={api} ready supported toolResult={openDraft('batch', {
    subAccount: 'chosen-group', signature: '预填签名', templateId: 'chosen-template',
  })} />);
  await screen.findByRole('button', { name: '下载名单模板' });
  expect(screen.getByText('预填消息组')).toBeTruthy();
  expect(screen.getByText('预填签名')).toBeTruthy();
  expect(screen.getByText('预填群发模板')).toBeTruthy();
  expect(screen.getByText('预填模板正文')).toBeTruthy();
  expect(api.call.mock.calls).toEqual([['get_batch_csv_template', {
    sub_account: 'chosen-group', template_id: 'chosen-template', include_variables: true,
  }]]);
  expect(api.upload).not.toHaveBeenCalled();

  await choose(user, '消息组', '手动消息组');
  expect(screen.queryByText('预填签名')).toBeNull();
  expect(screen.queryByText('预填模板正文')).toBeNull();
  expect(screen.queryByRole('button', { name: '下载名单模板' })).toBeNull();
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
  expect(screen.queryByRole('button', { name: '下载名单模板' })).toBeNull();
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
      .mockResolvedValueOnce({ value: 'phone\n' }),
  });
  render(<BatchForm client={api} prefill={{ subAccount: 'g', signature: '可用签名', templateId: 't' }} />);
  await screen.findByText('名单示例暂未取得');
  expect(screen.queryByRole('button', { name: '下载名单模板' })).toBeNull();
  await choose(user, '群发模板', '可重试模板');
  await screen.findByRole('button', { name: '下载名单模板' });
  expect(api.call.mock.calls).toEqual([
    ['get_batch_csv_template', { sub_account: 'g', template_id: 't', include_variables: true }],
    ['get_batch_csv_template', { sub_account: 'g', template_id: 't', include_variables: true }],
  ]);
});

it('企业校验未通过时，只有客户额外确认才转人工审核', async () => {
  const user = userEvent.setup();
  const api = client({ call: vi.fn(async name => {
    if (name === 'get_qualification_requirements') return rank;
    if (name === 'get_account_information') return { businessName: '测试企业', userType: 'enterprise' };
    if (name === 'check_qualification_enterprise') return { manualReview: true, code: 'enterprise_check_mismatch', requestId: 'test-check' };
    if (name === 'check_qualification_person') return { status: 0, ticket: 'person-check' };
    if (name === 'apply_qualification') return 123;
    throw new Error('unexpected tool');
  }) });
  render(<QualificationForm client={api} prefill={{ businessInfo: business, operatorPerson: record }} />);
  await user.click(await screen.findByRole('button', { name: '校验企业信息' }));
  expect(await screen.findByText('排障编号 test-check')).toBeTruthy();
  await user.click(screen.getByRole('button', { name: '下一步' }));
  await user.click(screen.getByRole('button', { name: '校验经办人信息' }));
  await screen.findByText('校验已通过');
  await user.click(screen.getByRole('button', { name: '下一步' }));
  await user.click(screen.getByRole('button', { name: '核对申请信息' }));
  const submit = screen.getByRole('button', { name: '确认转人工审核' });
  await user.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  expect(submit.disabled).toBe(true);
  await user.click(screen.getByText('我已核对企业信息，同意转人工审核'));
  await user.click(submit);
  const [, args] = api.call.mock.calls.find(([name]) => name === 'apply_qualification');
  expect(args).toMatchObject({ confirm_manual_review: true, request: { operatorCheckTicket: 'person-check' } });
  expect(args.request.businessCheckTicket).toBeUndefined();
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
  const submit = screen.getByRole('button', { name: '确认签署并开通' });
  expect(submit.disabled).toBe(true);
  expect(api.call.mock.calls).toEqual([['get_sms_service_onboarding']]);
  await user.click(screen.getByText('我已阅读并同意以上协议及计费说明'));
  await user.click(submit);
  await screen.findByText('开通请求已受理，等待状态更新');
  expect(api.call).toHaveBeenCalledWith('submit_sms_service_onboarding', { confirmation: 'confirm-current' }, { write: true });
  await user.click(screen.getByRole('button', { name: '刷新服务状态' }));
  expect(screen.queryByRole('button', { name: '确认签署并开通' })).toBeNull();
});

it('群发试发须单独确认，查询对应回执，名单引流检查与正式创建分开', async () => {
  const user = userEvent.setup();
  const template = { TemplateId: 't', ChannelType: 'CN_NTC', TemplateContent: '查看 ${url}' };
  const api = client({
    query: vi.fn(async action => {
      if (action === 'GetSubAccountListForAgent') return { List: [{ subAccountId: 'g' }], Total: 1 };
      if (action === 'ListSignaturesForAgent') return { List: [{ Signature: '签名' }], Total: 1 };
      return { List: [template], Total: 1 };
    }),
    call: vi.fn(async name => {
      if (name === 'get_batch_csv_template') return { value: 'phone,url\n', variables: ['url'] };
      if (name === 'send_batch_test_sms') return { messageId: 'test-sms-id', requestedAt: 1000 };
      if (name === 'list_send_logs') return { List: [{ messageId: 'test-sms-id', status: 3 }], Total: 1 };
      if (name === 'check_batch_traffic_resources') {
        return { checkedRows: 1, totalRows: 2, failedRows: 0, uncheckedRows: 1, missingResourceRows: 1, missingRowNumbers: [2] };
      }
      throw new Error('unexpected write');
    }),
    upload: vi.fn().mockResolvedValue({ name: '预填名单.csv', file: 'private-file', totalCount: 2, dupCount: 0 }),
  });
  const file = { name: '预填名单.csv', data: 'Zml4dHVyZQ==' };
  render(<BatchForm client={api} prefill={{
    name: '测试任务', subAccount: 'g', signature: '签名', templateId: 't',
    checkTraffic: true, recipientsFile: file,
  }} />);
  await screen.findByLabelText('测试手机号');
  await type(user, '测试手机号', '13800000000');
  await type(user, '试发变量 url', 'https://example.com/test');
  await user.click(screen.getByRole('button', { name: '核对测试短信' }));
  const send = screen.getByRole('button', { name: '确认发送测试短信' });
  expect(send.disabled).toBe(true);
  expect(api.call.mock.calls.filter(([name]) => name === 'send_batch_test_sms')).toHaveLength(0);
  await user.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await user.click(send);
  await screen.findByText('已收到成功回执');
  expect(api.call).toHaveBeenCalledWith('list_send_logs', expect.objectContaining({ message_id: 'test-sms-id' }));
  await user.click(screen.getByRole('button', { name: '上传 预填名单.csv' }));
  await user.click(screen.getByRole('button', { name: '核对群发任务' }));
  await screen.findByText('缺少资源的 CSV 行号 2');
  expect(api.call).toHaveBeenCalledWith('check_batch_traffic_resources', { request: expect.objectContaining({ file, template_id: 't' }) });
  expect(screen.getByRole('button', { name: '确认创建任务' }).disabled).toBe(true);
  await user.click(screen.getByRole('button', { name: '返回修改' }));
  expect(screen.getByText('已收到成功回执')).toBeTruthy();
  await user.click(screen.getByRole('button', { name: '刷新试发回执' }));
  expect(api.call.mock.calls.filter(([name]) => name === 'list_send_logs')).toHaveLength(2);
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
  const view = render(<SmsApp client={api} ready supported toolResult={{ structuredContent: { form: 'qualification', success: true, result: 123 } }} />);
  expect(screen.getByText('此操作已返回结果')).toBeTruthy();
  expect(api.call).not.toHaveBeenCalled();
  view.rerender(<SmsApp client={api} ready supported={false} toolResult={openDraft('batch', {})} />);
  expect(screen.getByText(/当前客户端不支持表单操作/)).toBeTruthy();
  expect(api.call).not.toHaveBeenCalled();
});

describe('标准 AppBridge 调用边界', () => {
  it('把宿主带入的附件原样交给已有私密上传工具', async () => {
    const draft = { name: 'proof.png', data: 'Zml4dHVyZQ==' };
    const file = { name: draft.name, fileContent: 'fixture/uploaded', fileSuffix: 'png' };
    const app = { callServerTool: vi.fn().mockResolvedValue({
      structuredContent: { success: true, result: null },
      _meta: { 'sms/form': { success: true, result: file } },
    }) };
    const api = new SmsFormClient(app);
    const request = { kind: 'material', category: 'business' };
    expect(await api.upload(draft, request)).toEqual(file);
    expect(app.callServerTool.mock.calls[0][0]).toEqual({
      name: 'upload_sms_file', arguments: { request: { ...request, ...draft } },
    });
  });
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
