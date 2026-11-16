import React from 'react';
import { afterEach, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { checkedTemplatePreview, TemplateForm, templatePayload } from './template.jsx';
import { OperationError } from './client.js';

afterEach(cleanup);

const draft = { name: '预约通知', channelType: 'CN_NTC', content: ' 原始正文 ${time} ',
  signatures: ['签名'], subAccounts: ['g'], templateParams: [{ name: 'time', paramType: 1 }] };
const token = 'a'.repeat(64);
function preview(request, extra = {}) {
  return { request: { ...request, area: 'cn' }, account: { userType: 'enterprise', businessName: '测试企业' },
    fixedTraffic: [], warnings: [], confirmation: token, ...extra };
}
function client() {
  return { report: vi.fn().mockResolvedValue(), query: vi.fn(async action => {
    if (action === 'GetSubAccountListForAgent') return { list: [{ subAccountId: 'g', subAccountName: '测试组' }], total: 1 };
    if (action === 'GetTobTrafficDrivingLinkListForAgent') return { list: [{ id: 12, link: 'https://example.com/activity' }], total: 1 };
    if (action === 'GetTobTrafficDrivingPhoneListForAgent') return { list: [{ id: 21, number: '4008000000' }], total: 1 };
    return { List: [{ Signature: '签名' }], Total: 1 };
  }),
  call: vi.fn(async (name, args) => {
    if (name === 'preview_template') return preview(args.request);
    if (name === 'submit_template') return { templateId: 'accepted', status: 1 };
    throw new Error('Unexpected tool');
  }) };
}
async function ready(api, value = draft) {
  render(<TemplateForm client={api} prefill={value} />);
  await waitFor(() => expect(api.query.mock.calls.some(([action]) => action === 'ListSignaturesForAgent')).toBe(true));
  await waitFor(() => expect(screen.getByRole('button', { name: '核对模板申请' }).disabled).toBe(false));
}

it('删除截图圈出的控件，隐藏预填项目和范围仍原样提交', async () => {
  const api = client(); const value = { ...draft, project: '宿主预填项目' };
  await ready(api, value);
  expect(screen.queryByLabelText('项目（可选）')).toBeNull();
  expect(screen.queryByLabelText('适用消息组')).toBeNull();
  expect(screen.queryByText(/不限定消息组/)).toBeNull();
  expect(screen.queryByText(/变量写作/)).toBeNull();
  expect(screen.queryByRole('button', { name: '从正文提取变量' })).toBeNull();
  expect(screen.queryByLabelText(/变量 \d+ 名称/)).toBeNull();
  expect(screen.getByLabelText('关联签名')).toBeTruthy();
  expect(screen.queryByText('适用签名', { exact: true })).toBeNull();
  expect(screen.queryByRole('button', { name: '刷新签名' })).toBeNull();
  expect(api.query.mock.calls.some(([action]) => action === 'GetSubAccountListForAgent')).toBe(false);
  await userEvent.click(screen.getByRole('button', { name: '核对模板申请' }));
  await screen.findByRole('button', { name: '确认提交模板' });
  expect(screen.queryByText('项目', { exact: true })).toBeNull();
  expect(screen.queryByText('宿主预填项目')).toBeNull();
  expect(screen.queryByText('适用消息组', { exact: true })).toBeNull();
  await userEvent.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await userEvent.click(screen.getByRole('button', { name: '确认提交模板' }));
  await screen.findByText('模板申请已受理');
  expect(api.call).toHaveBeenCalledWith('submit_template', { request: { ...value, area: 'cn' }, confirmation: token }, { write: true });
});

it('本地校验错误显示在对应表单项并滚动聚焦，不再显示顶部错误条', async () => {
  const api = client();
  await ready(api, { ...draft, signatures: [] });
  await userEvent.click(screen.getByRole('button', { name: '核对模板申请' }));
  expect(screen.getByText('请至少选择一个签名。', { selector: '.traffic-field-error' })).toBeTruthy();
  expect(screen.getByLabelText('关联签名').getAttribute('aria-invalid')).toBe('true');
  expect(document.querySelector('.sms-feedback')).toBeNull();
  await waitFor(() => expect(Element.prototype.scrollIntoView).toHaveBeenCalled());
  expect(api.call).not.toHaveBeenCalled();
});

it('正文错误显示在模版内容下方，编辑对应字段后立即清除', async () => {
  const api = client(); const user = userEvent.setup();
  await ready(api, { ...draft, channelType: 'CN_MKT', content: '营销活动', templateParams: [] });
  await user.click(screen.getByRole('button', { name: '核对模板申请' }));
  expect(screen.getByText('营销模板末尾必须为“拒收请回复R”。', { selector: '.traffic-field-error' })).toBeTruthy();
  expect(screen.getByLabelText('模版内容').getAttribute('aria-invalid')).toBe('true');
  fireEvent.change(screen.getByLabelText('模版内容'), { target: { value: '营销活动 拒收请回复R' } });
  expect(screen.queryByText('营销模板末尾必须为“拒收请回复R”。', { selector: '.traffic-field-error' })).toBeNull();
  expect(screen.getByLabelText('模版内容').getAttribute('aria-invalid')).toBe('false');
});

it.each([{ subAccounts: undefined }, { subAccounts: [] }])('消息组范围 %j 不要求补选，省略范围与显式空数组保持区别', async ({ subAccounts }) => {
  const api = client(); const value = { ...draft };
  if (subAccounts === undefined) delete value.subAccounts;
  else value.subAccounts = subAccounts;
  await ready(api, value);
  expect(api.query.mock.calls.every(([action, params]) => action === 'ListSignaturesForAgent' && !Object.hasOwn(params, 'SubAccounts'))).toBe(true);
  await userEvent.click(screen.getByRole('button', { name: '核对模板申请' }));
  await screen.findByRole('button', { name: '确认提交模板' });
  expect(api.call).toHaveBeenCalledWith('preview_template', { request: value });
  expect(Object.hasOwn(api.call.mock.calls[0][1].request, 'subAccounts')).toBe(subAccounts !== undefined);
});

it('正文自动提取并去重变量，新变量按主项目默认使用普通变量', async () => {
  const api = client(); const user = userEvent.setup();
  await ready(api);
  const content = '预约 ${time}，备注 ${Next}，再次显示 ${Next}';
  fireEvent.change(screen.getByLabelText('模版内容'), { target: { value: content } });
  expect(screen.getByLabelText('变量 time 的名称').value).toBe('time');
  expect(screen.getByLabelText('变量 Next 的名称').value).toBe('Next');
  await user.click(screen.getByRole('button', { name: '核对模板申请' }));
  await screen.findByRole('button', { name: '确认提交模板' });
  expect(api.call).toHaveBeenCalledWith('preview_template', { request: { ...draft, content,
    templateParams: [{ name: 'time', paramType: 1 }, { name: 'Next', paramType: 1 }] } });
});

it('正文修改同步变量名称，保留未改变的引流变量类型和资源绑定', async () => {
  const api = client(); const user = userEvent.setup();
  const value = { ...draft, content: '预约 ${time}，详情 ${url}',
    templateParams: [{ name: 'time', paramType: 1 }, { name: 'url', paramType: 2 }],
    templateTrafficDriving: [[{ name: 'url', paramType: 2, id: 12, content: 'https://example.com/Case?Q=A' }]] };
  await ready(api, value);
  const content = '详情 ${url}，预约 ${Time}';
  fireEvent.change(screen.getByLabelText('模版内容'), { target: { value: content } });
  expect(screen.queryByLabelText('变量 time 的名称')).toBeNull();
  expect(screen.getByLabelText('变量 Time 的名称').value).toBe('Time');
  await user.click(screen.getByRole('button', { name: '核对模板申请' }));
  await screen.findByRole('button', { name: '确认提交模板' });
  expect(api.call).toHaveBeenCalledWith('preview_template', { request: { ...value, content,
    templateParams: [{ name: 'url', paramType: 2 }, { name: 'Time', paramType: 1 }] } });
});

it('新增引流信息在弹窗选择资源，主表只展示组合摘要', async () => {
  const api = client(); const user = userEvent.setup();
  await ready(api, { ...draft, content: '详情 ${url}，电话 ${phone}',
    templateParams: [{ name: 'url', paramType: 2 }, { name: 'phone', paramType: 3 }] });
  expect(screen.getByText('变量管理', { exact: true })).toBeTruthy();
  expect(screen.getByText('引流信息管理', { exact: true })).toBeTruthy();
  expect(screen.getByRole('button', { name: '添加引流信息' }).disabled).toBe(false);
  await user.click(screen.getByRole('button', { name: '添加引流信息' }));
  const modalTitle = await screen.findByText('新增引流信息');
  expect(modalTitle.closest('.arco-modal-wrapper').classList.contains('template-traffic-modal-wrap')).toBe(true);
  expect(api.query).toHaveBeenCalledWith('GetTobTrafficDrivingLinkListForAgent', { useVolcLink: false });
  expect(screen.queryByText('已报备资源', { exact: true })).toBeNull();
  expect(screen.queryByLabelText('原始链接')).toBeNull();
  expect(screen.queryByLabelText('原始号码')).toBeNull();
  for (const [name, optionName] of [['url', 'https://example.com/activity'], ['phone', '4008000000']]) {
    await user.click(screen.getByLabelText(`变量 ${name} 的引流信息`));
    const option = await screen.findByRole('option', { name: optionName });
    await waitFor(() => expect(window.getComputedStyle(option).pointerEvents).not.toBe('none'));
    await user.click(option.querySelector('.arco-select-option') ?? option);
  }
  await user.click(screen.getByRole('button', { name: '确定' }));
  await waitFor(() => expect(screen.queryByText('新增引流信息')).toBeNull());
  expect(screen.getAllByText('https://example.com/activity').length).toBeGreaterThan(0);
  expect(screen.getAllByText('4008000000').length).toBeGreaterThan(0);
});

it('切换平台短链模式会清空旧引流绑定并按新模式查询链接库', async () => {
  const api = client(); const user = userEvent.setup();
  await ready(api, { ...draft, channelType: 'CN_MKT', content: '详情 ${url} 拒收请回复R',
    templateParams: [{ name: 'url', paramType: 2 }],
    shortUrlConfig: { isEnabled: '1', belong: 'DEFAULT', isNeedClickDetails: '0', uaCheckStrategy: 0 },
    templateTrafficDriving: [[{ name: 'url', paramType: 2, id: 12, content: 'https://example.com/activity' }]] });
  await waitFor(() => expect(api.query).toHaveBeenCalledWith(
    'GetTobTrafficDrivingLinkListForAgent', { useVolcLink: true },
  ));
  expect(screen.getAllByText('https://example.com/activity').length).toBeGreaterThan(0);
  const group = screen.getByLabelText('使用平台生成短链');
  await user.click(within(group).getByRole('radio', { name: '否' }));
  expect(screen.queryByText('https://example.com/activity')).toBeNull();
  await user.click(screen.getByRole('button', { name: '添加引流信息' }));
  await waitFor(() => expect(api.query).toHaveBeenCalledWith(
    'GetTobTrafficDrivingLinkListForAgent', { useVolcLink: false },
  ));
});

it('占位符输入中间状态不打断填写、不丢类型，核对仍阻断不完整正文', async () => {
  const api = client(); await ready(api);
  fireEvent.change(screen.getByLabelText('模版内容'), { target: { value: '预约 ${time' } });
  expect(screen.queryByText('请使用完整的 ${变量名}，名称仅含英文、数字或下划线。')).toBeNull();
  expect(screen.queryByText('操作未完成，请核对当前结果。')).toBeNull();
  expect(screen.getByLabelText('模版内容').value).toBe('预约 ${time');
  expect(screen.getByLabelText('变量 time 的名称').value).toBe('time');
  await userEvent.click(screen.getByRole('button', { name: '核对模板申请' }));
  await screen.findByText('请使用完整的 ${变量名}，名称仅含英文、数字或下划线。');
  expect(api.call).not.toHaveBeenCalled();
  const content = '预约 ${time}';
  fireEvent.change(screen.getByLabelText('模版内容'), { target: { value: content } });
  await userEvent.click(screen.getByRole('button', { name: '核对模板申请' }));
  await screen.findByRole('button', { name: '确认提交模板' });
  expect(api.call).toHaveBeenCalledWith('preview_template', { request: { ...draft, content } });
});

it('正文移除变量后自动移除对应设置，不留手动清理项', async () => {
  const api = client(); await ready(api);
  const content = '预约时间为明天下午';
  fireEvent.change(screen.getByLabelText('模版内容'), { target: { value: content } });
  expect(screen.queryByLabelText('变量 time 的名称')).toBeNull();
  await userEvent.click(screen.getByRole('button', { name: '核对模板申请' }));
  await screen.findByRole('button', { name: '确认提交模板' });
  expect(api.call).toHaveBeenCalledWith('preview_template', { request: { ...draft, content, templateParams: [] } });
});

it('通知和营销模板最多允许 20 个变量，营销正文必须使用主项目退订后缀', () => {
  const variables = count => Array.from({ length: count }, (_item, index) => `\${v${index}}`).join('，');
  const params = count => Array.from({ length: count }, (_item, index) => ({ name: `v${index}`, paramType: 1 }));
  expect(() => templatePayload({ ...draft, content: variables(20), templateParams: params(20) })).not.toThrow();
  expect(() => templatePayload({ ...draft, content: variables(21), templateParams: params(21) })).toThrow('最多包含 20 个变量');
  expect(() => templatePayload({ ...draft, channelType: 'CN_MKT', content: '活动优惠', templateParams: [] }))
    .toThrow('营销模板末尾必须为“拒收请回复R”');
  expect(() => templatePayload({ ...draft, channelType: 'CN_MKT', content: '活动优惠 拒收请回复R', templateParams: [] }))
    .not.toThrow();
});

it('变量引流必须选择当前账号引流信息库中的资源 ID', () => {
  const values = { ...draft, content: '详情 ${url}', templateParams: [{ name: 'url', paramType: 2 }],
    templateTrafficDriving: [[{ name: 'url', paramType: 2, content: 'https://example.com' }]] };
  expect(() => templatePayload(values)).toThrow('选择引流信息库中的链接或号码');
});

it('切换验证码模板后变量强制改为普通类型并清除引流绑定', async () => {
  const api = client(); const user = userEvent.setup();
  await ready(api, { ...draft, content: '验证码 ${code}', templateParams: [{ name: 'code', paramType: 2 }],
    templateTrafficDriving: [[{ name: 'code', paramType: 2, id: 12, content: 'https://example.com' }]] });
  await user.click(screen.getByLabelText('模版类型'));
  const option = await screen.findByRole('option', { name: '验证码' });
  await waitFor(() => expect(window.getComputedStyle(option).pointerEvents).not.toBe('none'));
  await user.click(option.querySelector('.arco-select-option') ?? option);
  expect(screen.getByText('普通变量')).toBeTruthy();
  expect(screen.queryByText('引流信息管理', { exact: true })).toBeNull();
  expect(screen.queryByRole('button', { name: '添加引流信息' })).toBeNull();
  expect(screen.queryByText('引流组合 1')).toBeNull();
});

it.each([
  { name: '中'.repeat(34) }, { name: 'a'.repeat(51) }, { desc: '😀'.repeat(151) },
  { content: '${time}${time}' }, { content: ' ${time}'.repeat(21) },
  { content: '${VOLC_SMS_URL_TOKEN}', templateParams: [{ name: 'VOLC_SMS_URL_TOKEN', paramType: 1 }] },
  { channelType: 'CN_OTP', content: '预约 ${time}' },
  { shortUrlConfig: { isEnabled: 1 } }, { shortUrlConfig: { isNeedClickDetails: 'true' } },
])('拒绝不符合参考规则的字段 %j', changes => {
  expect(() => templatePayload({ ...draft, ...changes })).toThrow(OperationError);
});

it('姓名按浏览器 UTF-16 计数，保留大小写、空格和原生短链枚举', () => {
  const values = { ...draft, name: '😀'.repeat(25), desc: '😀'.repeat(150),
    shortUrlConfig: { isEnabled: '0', isNeedClickDetails: '1', belong: 'VMS', uaCheckStrategy: 3 } };
  expect(templatePayload(values)).toEqual(values);
});

it.each([
  { confirmation: undefined }, { fixedTraffic: [{ paramType: 2, isExist: false }] },
  { fixedTraffic: [{ paramType: '2', isExist: true }] }, { account: {} },
  { request: { ...draft, area: 'cn', content: '被改写的正文' } },
])('不完整或不属于本次请求的预览不能进入确认 %j', extra => {
  expect(() => checkedTemplatePreview(preview(draft, extra), draft)).toThrow(OperationError);
});

it('显式资源 ID 可在预览中补齐原始链接，保留原生字段', () => {
  const request = { ...draft, templateTrafficDriving: [[{ name: 'url', paramType: 2, id: 12 }]] };
  const result = preview({ ...request, templateTrafficDriving: [[{ name: 'url', paramType: 2, id: 12, content: 'https://example.com/Case?Q=A' }]] });
  expect(checkedTemplatePreview(result, request)).toBe(result);
});

it.each(['账号未开放营销变量', '固定链接尚未录入', '固定引流查询失败'])('核对失败保留表单且不申请：%s', async message => {
  const api = client(); api.call.mockRejectedValue(new OperationError(message, { code: 'check_failed', requestId: 'check-request' }));
  await ready(api);
  await userEvent.click(screen.getByRole('button', { name: '核对模板申请' }));
  await screen.findByText(message);
  expect(screen.queryByRole('button', { name: '确认提交模板' })).toBeNull();
  expect(screen.getByLabelText('模版内容').value).toBe(draft.content);
  expect(api.call.mock.calls.map(([name]) => name)).toEqual(['preview_template']);
  expect(screen.getByText('排障编号：check-request')).toBeTruthy();
});

it('预览展示固定引流与风险，双击核对和提交各只调用一次', async () => {
  const api = client();
  let resolvePreview, resolveSubmit;
  api.call.mockImplementation((name, args) => name === 'preview_template' ? new Promise(resolve => {
    resolvePreview = () => resolve(preview(args.request, { fixedTraffic: [{ paramType: 3, isExist: true, content: '4008000000' }],
      warnings: ['小微账号模板存在审核风险'] }));
  }) : new Promise(resolve => { resolveSubmit = () => resolve({ templateId: 'accepted', status: 1 }); }));
  await ready(api);
  const review = screen.getByRole('button', { name: '核对模板申请' });
  fireEvent.click(review); fireEvent.click(review);
  await waitFor(() => expect(api.call).toHaveBeenCalledTimes(1));
  expect(screen.queryByRole('button', { name: '确认提交模板' })).toBeNull();
  resolvePreview();
  await screen.findByRole('button', { name: '确认提交模板' });
  expect(screen.getByText('4008000000')).toBeTruthy();
  expect(screen.getByText('小微账号模板存在审核风险')).toBeTruthy();
  await userEvent.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  const submit = screen.getByRole('button', { name: '确认提交模板' });
  fireEvent.click(submit); fireEvent.click(submit);
  await waitFor(() => expect(api.call.mock.calls.filter(([name]) => name === 'submit_template')).toHaveLength(1));
  resolveSubmit();
  await screen.findByText('模板申请已受理');
  expect(api.call).toHaveBeenCalledWith('submit_template', { request: { ...draft, area: 'cn' }, confirmation: token }, { write: true });
  expect(api.report.mock.calls).toEqual([[{ form: 'template', state: 'submitted', templateId: 'accepted', status: 1 }]]);
});

it('返回修改后撤销旧确认，重新预检新的正文', async () => {
  const api = client(); const user = userEvent.setup(); await ready(api);
  await user.click(screen.getByRole('button', { name: '核对模板申请' }));
  await screen.findByRole('button', { name: '确认提交模板' });
  await user.click(screen.getByRole('button', { name: '返回修改' }));
  fireEvent.change(screen.getByLabelText('模版内容'), { target: { value: '新的 ${time}' } });
  await user.click(screen.getByRole('button', { name: '核对模板申请' }));
  await screen.findByText('新的 ${time}');
  expect(api.call.mock.calls.map(([name]) => name)).toEqual(['preview_template', 'preview_template']);
  expect(api.call.mock.calls[1][1].request.content).toBe('新的 ${time}');
  expect(screen.getByRole('button', { name: '确认提交模板' }).disabled).toBe(true);
});

it('提交前账号变化撤销确认并保留用户正文，必须重新核对', async () => {
  const api = client(); const normal = api.call.getMockImplementation();
  api.call.mockImplementation((name, ...args) => name === 'submit_template'
    ? Promise.reject(new OperationError('账号条件已变化，请重新核对', { code: 'template_confirmation_changed' })) : normal(name, ...args));
  await ready(api);
  await userEvent.click(screen.getByRole('button', { name: '核对模板申请' }));
  await screen.findByRole('button', { name: '确认提交模板' });
  await userEvent.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await userEvent.click(screen.getByRole('button', { name: '确认提交模板' }));
  await screen.findByText('账号条件已变化，请重新核对');
  expect(screen.getByLabelText('模版内容').value).toBe(draft.content);
  expect(screen.queryByRole('button', { name: '确认提交模板' })).toBeNull();
});

it.each([new OperationError('模板申请结果未知', { unknown: true }), {}])('未知写入或不完整受理结果锁定编辑和重试', async result => {
  const api = client(); const normal = api.call.getMockImplementation();
  api.call.mockImplementation((name, ...args) => name !== 'submit_template' ? normal(name, ...args)
    : result instanceof Error ? Promise.reject(result) : Promise.resolve(result));
  await ready(api);
  await userEvent.click(screen.getByRole('button', { name: '核对模板申请' }));
  await screen.findByRole('button', { name: '确认提交模板' });
  await userEvent.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await userEvent.click(screen.getByRole('button', { name: '确认提交模板' }));
  await waitFor(() => expect(screen.getByRole('button', { name: '确认提交模板' }).disabled).toBe(true));
  expect(screen.getByRole('button', { name: '返回修改' }).disabled).toBe(true);
  expect(api.call.mock.calls.filter(([name]) => name === 'submit_template')).toHaveLength(1);
});
