import React from 'react';
import { afterEach, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { SignatureForm } from './signature.jsx';
import { OperationError } from './client.js';
import { loadSignatureGroups, signaturePreview, validateSignatureContent } from './signature-controller.js';

afterEach(cleanup);
const company = { id: 12, purpose: 1, materialName: '企业资质', businessCertificateName: '示例科技有限公司' };
const otherCompany = { id: 24, purpose: 2, materialName: '客户资质', businessCertificateName: '客户科技有限公司' };
const group = { subAccountId: 'group', subAccountName: '客户通知' };
const emptyAttachments = { app: [], trademark: [], other: [] };
function client(qualifications = [company], overrides = {}) {
  return {
    query: vi.fn(async action => action === 'GetApplySignatureBind' ? qualifications
      : action === 'GetSubAccountListForAgent' ? { list: [group], total: 1 }
        : { List: [{ Signature: '示例科技', Status: 3, StatusDescription: '审核通过' }], Total: 1 }),
    call: vi.fn().mockResolvedValue({ applyId: 'application', status: 1 }),
    upload: vi.fn(async file => ({ name: file.name, fileContent: `private/${file.name}`, fileSuffix: file.name.split('.').pop() })),
    report: vi.fn().mockResolvedValue(undefined),
    ...overrides,
  };
}
async function choose(user, label, name) {
  await user.click(screen.getByLabelText(label));
  const option = await screen.findByRole('option', { name });
  await waitFor(() => expect(window.getComputedStyle(option).pointerEvents).not.toBe('none'));
  await user.click(option);
}
async function materials(user) {
  await screen.findByRole('button', { name: '下一步' });
  await user.click(screen.getByRole('button', { name: '下一步' }));
  return screen.findByRole('button', { name: '核对申请' });
}
async function preview(user) {
  await materials(user);
  await user.click(screen.getByRole('button', { name: '核对申请' }));
  return screen.findByRole('region', { name: '申请预览' });
}

it.each([
  ['', '请输入签名内容'], [' 公司', '签名首尾不能包含空格'], ['公', '签名最少2个字符'],
  ['公司@', '签名存在不支持的特殊符号'], ['公司.com', '签名不能包含网址'],
  ['123456', '签名不支持纯数字'], ['公司13800000000', '签名不能包含联系方式'],
  ['()()', '签名至少存在一个中文或英文或数字'],
])('签名沿用 skill 的名称校验并保留原值：%s', (content, error) => {
  expect(validateSignatureContent(content)).toBe(error);
  expect(() => signaturePreview({ source: 1, content }, company, 'all', emptyAttachments)).toThrow(error);
});

it('两步表单使用相同 Arco 控件、固定三种发送类型且不增加项目名称字段', async () => {
  const user = userEvent.setup();
  const api = client();
  render(<SignatureForm client={api} />);
  await screen.findByText('创建短信签名');
  expect(screen.getByLabelText('签名内容').value).toBe(company.businessCertificateName);
  expect(screen.queryByLabelText('资质')).toBeNull();
  expect(screen.getByText('✓ 验证码短信')).toBeTruthy();
  expect(screen.getByText('✓ 通知短信')).toBeTruthy();
  expect(screen.getByText('✓ 营销短信')).toBeTruthy();
  expect(screen.getByLabelText('申请说明').maxLength).toBe(300);
  await user.type(screen.getByLabelText('申请说明'), '用于订单通知');
  await preview(user);
  expect(screen.getByLabelText('资质').closest('.arco-select')).toBeTruthy();
  expect(screen.queryByLabelText('项目名称（选填）')).toBeNull();
  expect(screen.getByLabelText('更多资料').accept).toBe('.png,.jpg,.jpeg,.doc,.docx,.gif,.zip');
  await user.click(screen.getByRole('button', { name: '确认提交' }));
  await screen.findByText('签名申请已提交');
  expect(api.call).toHaveBeenCalledWith('submit_signature', { request: {
    content: company.businessCertificateName, purpose: 1, signatureIdentificationID: 12,
    source: 1, channelTypes: ['CN_OTP', 'CN_NTC', 'CN_MKT'], isLimitSubAccount: 1,
    subAccounts: ['group'], from: 'vconsole', desc: '用于订单通知', uploadFileList: [],
  } }, { write: true });
  expect(api.query.mock.calls.filter(([action]) => action === 'GetApplySignatureBind')).toHaveLength(1);
  await waitFor(() => expect(screen.getByRole('button', { name: '刷新审核状态' }).disabled).toBe(false));
  await user.click(screen.getByRole('button', { name: '刷新审核状态' }));
  await screen.findByText('审核通过');
  expect(api.query).toHaveBeenCalledWith('ListSignaturesForAgent', {
    Signature: company.businessCertificateName, ExactMatch: true, Page: 1, PageSize: 100,
  });
});

it('基础信息必填校验阻止进入材料步骤，并定位错误字段', async () => {
  const user = userEvent.setup();
  render(<SignatureForm client={client([company, otherCompany])} />);
  await screen.findByRole('button', { name: '下一步' });
  await user.click(screen.getByRole('button', { name: '下一步' }));
  expect(screen.getByText('请选择签名归属类型', { selector: '.signature-field-error' })).toBeTruthy();
  expect(screen.getByText('请输入签名内容', { selector: '.signature-field-error' })).toBeTruthy();
  expect(screen.queryByRole('button', { name: '核对申请' })).toBeNull();
});

it.each(['按钮', 'Enter'])('宿主禁止原生表单提交时，下一步与核对申请仍通过%s执行', async action => {
  const user = userEvent.setup();
  const api = client();
  render(<SignatureForm client={api} prefill={{ source: 2, content: '示例科技',
    isLimitSubAccount: 0, appIcp: { appIcpFilling: '备案一号' } }} />);
  await screen.findByRole('button', { name: '下一步' });
  const blockSubmit = vi.fn(event => {
    event.preventDefault();
    event.stopImmediatePropagation();
  });
  document.addEventListener('submit', blockSubmit, true);
  try {
    if (action === '按钮') await user.click(screen.getByRole('button', { name: '下一步' }));
    else { await user.click(screen.getByLabelText('签名内容')); await user.keyboard('{Enter}'); }
    await screen.findByRole('button', { name: '核对申请' });
    if (action === '按钮') await user.click(screen.getByRole('button', { name: '核对申请' }));
    else { await user.click(screen.getByLabelText('APP ICP 备案号')); await user.keyboard('{Enter}'); }
    await screen.findByRole('region', { name: '申请预览' });
    expect(blockSubmit).not.toHaveBeenCalled();
    expect(api.call).not.toHaveBeenCalled();
  } finally {
    document.removeEventListener('submit', blockSubmit, true);
  }
});

it('预填资质锁定归属与资质，返回修改保留名称和说明', async () => {
  const user = userEvent.setup();
  render(<SignatureForm client={client([company, otherCompany])} prefill={{
    signatureIdentificationID: 24, content: '客户科技', desc: '客户通知', isLimitSubAccount: 0,
  }} />);
  await screen.findByText('创建短信签名');
  expect(screen.getByLabelText('签名归属类型').getAttribute('aria-disabled')).toBe('true');
  await materials(user);
  expect(screen.getByLabelText('资质').getAttribute('aria-disabled')).toBe('true');
  expect(screen.getByText('该资质由申请上下文确定，本次不可更换。')).toBeTruthy();
  await user.click(screen.getByRole('button', { name: '上一步' }));
  expect(screen.getByLabelText('签名内容').value).toBe('客户科技');
  expect(screen.getByLabelText('申请说明').value).toBe('客户通知');
});

it('他用资质按归属筛选，名称改变后重新选择且保留手动名称', async () => {
  const user = userEvent.setup();
  render(<SignatureForm client={client([company, otherCompany])} prefill={{
    content: '客户科技', isLimitSubAccount: 0,
  }} />);
  await screen.findByText('创建短信签名');
  await choose(user, '签名归属类型', '他用');
  await materials(user);
  await user.click(screen.getByLabelText('资质'));
  const options = screen.getAllByRole('option');
  expect(options.map(option => option.textContent)).toEqual(['24【客户科技有限公司】· 他用']);
  await waitFor(() => expect(window.getComputedStyle(options[0]).pointerEvents).not.toBe('none'));
  await user.click(options[0]);
  await user.click(screen.getByRole('button', { name: '上一步' }));
  await user.clear(screen.getByLabelText('签名内容'));
  await user.type(screen.getByLabelText('签名内容'), '客户科技服务');
  await materials(user);
  expect(screen.getByLabelText('资质').querySelector('input').value).toBe('');
  await choose(user, '资质', '24【客户科技有限公司】· 他用');
  await user.click(screen.getByRole('button', { name: '上一步' }));
  expect(screen.getByLabelText('签名内容').value).toBe('客户科技服务');
});

it.each([2, 3])('来源 %s 保留嵌套 key、材料类型与项目预填，切换来源不提交隐藏材料', async source => {
  const user = userEvent.setup();
  const api = client();
  const prefill = { source, content: '示例科技', isLimitSubAccount: 0, projectName: '已有项目',
    appIcp: { appIcpFilling: '备案一号', appIcpFileList: [{ name: 'app.png', fileContent: 'private/app', fileSuffix: 'png' }] },
    trademark: { trademarkCn: '示例科技', trademarkEn: 'Example', trademarkNumber: '123456',
      trademarkFileList: [{ name: 'mark.pdf', fileContent: 'private/mark', fileSuffix: 'pdf' }] },
    uploadFileList: [{ name: 'other.docx', fileContent: 'private/other', fileSuffix: 'docx' }],
  };
  render(<SignatureForm client={api} prefill={prefill} />);
  await preview(user);
  if (source === 2) expect(screen.getByLabelText('APP ICP 备案号').value).toBe('备案一号');
  else expect(screen.getByLabelText('商标注册号').value).toBe('123456');
  await user.click(screen.getByRole('button', { name: '确认提交' }));
  await screen.findByText('签名申请已提交');
  const request = api.call.mock.calls[0][1].request;
  expect(request.projectName).toBe('已有项目');
  expect(request.uploadFileList).toEqual([{ fileType: 6, fileContent: 'private/other', fileSuffix: 'docx' }]);
  if (source === 2) {
    expect(request.trademark).toBeUndefined();
    expect(request.appIcp).toEqual({ appIcpFilling: '备案一号',
      appIcpFileList: [{ fileType: 16, fileContent: 'private/app', fileSuffix: 'png' }] });
  } else {
    expect(request.appIcp).toBeUndefined();
    expect(request.trademark).toEqual({ trademarkCn: '示例科技', trademarkEn: 'Example', trademarkNumber: '123456',
      trademarkFileList: [{ fileType: 17, fileContent: 'private/mark', fileSuffix: 'pdf' }] });
  }
});

it.each([2, 3])('来源 %s 在材料缺失时阻止核对，填写后允许继续', async source => {
  const user = userEvent.setup();
  const api = client();
  render(<SignatureForm client={api} prefill={{ source, content: '示例科技', isLimitSubAccount: 0 }} />);
  await materials(user);
  await user.click(screen.getByRole('button', { name: '核对申请' }));
  await screen.findByText(source === 2 ? '请填写 APP ICP 备案号或上传备案截图。' : '请填写商标注册号。');
  await user.type(screen.getByLabelText(source === 2 ? 'APP ICP 备案号' : '商标注册号'), '123456');
  await user.click(screen.getByRole('button', { name: '核对申请' }));
  await screen.findByRole('region', { name: '申请预览' });
  expect(api.call).not.toHaveBeenCalled();
});

it('消息组完整分页读取，唯一消息组以外的选择不被自动替换', async () => {
  const rows = Array.from({ length: 101 }, (_, index) => ({ subAccountId: `group-${index}` }));
  const api = client([], { query: vi.fn(async (_action, params) => ({
    list: params.pageIndex === 1 ? rows.slice(0, 100) : rows.slice(100), total: rows.length,
  })) });
  expect(await loadSignatureGroups(api)).toEqual(rows);
  expect(api.query.mock.calls).toEqual([
    ['GetSubAccountListForAgent', { pageIndex: 1, pageSize: 100 }],
    ['GetSubAccountListForAgent', { pageIndex: 2, pageSize: 100 }],
  ]);
});

it('强制提交需弹窗确认，取消及编辑均不提交旧预览', async () => {
  const user = userEvent.setup();
  const api = client();
  render(<SignatureForm client={api} prefill={{ content: '其他品牌', isLimitSubAccount: 0 }} />);
  await preview(user);
  await user.click(screen.getByRole('button', { name: '强制提交' }));
  expect(api.call).not.toHaveBeenCalled();
  await user.click(screen.getAllByRole('button', { name: '返回修改' }).at(-1));
  await waitFor(() => expect(screen.queryByText('确认承担签名报备风险')).toBeNull());
  await user.click(screen.getByRole('button', { name: '返回修改' }));
  expect(screen.queryByRole('button', { name: '强制提交' })).toBeNull();
  await user.click(screen.getByRole('button', { name: '上一步' }));
  await user.clear(screen.getByLabelText('签名内容'));
  await user.type(screen.getByLabelText('签名内容'), '示例科技');
  await preview(user);
  expect(screen.queryByRole('button', { name: '强制提交' })).toBeNull();
  expect(api.call).not.toHaveBeenCalled();
});

it('提交期间重复点击只写一次，未知写结果锁定所有编辑和重试', async () => {
  const user = userEvent.setup();
  let reject;
  const api = client([company], { call: vi.fn(() => new Promise((_resolve, fail) => { reject = fail; })) });
  render(<SignatureForm client={api} prefill={{ content: '示例科技', isLimitSubAccount: 0 }} />);
  await preview(user);
  await user.dblClick(screen.getByRole('button', { name: '确认提交' }));
  expect(api.call).toHaveBeenCalledTimes(1);
  reject(new OperationError('申请结果待核实', { unknown: true }));
  await screen.findByText('申请结果待核实');
  for (const button of ['确认提交', '返回修改', '上一步', '放弃本次填写']) {
    expect(screen.getByRole('button', { name: button }).disabled).toBe(true);
  }
  expect(screen.getByLabelText('资质').getAttribute('aria-disabled')).toBe('true');
  expect(api.call).toHaveBeenCalledTimes(1);
});

it('已知提交失败保留表单材料，重新核对后才能重试且不重复查询资质', async () => {
  const user = userEvent.setup();
  const api = client([company], { call: vi.fn().mockRejectedValueOnce(new OperationError('请核对资质'))
    .mockResolvedValue({ applyId: 'retry-application', status: 1 }) });
  render(<SignatureForm client={api} prefill={{ content: '示例科技', isLimitSubAccount: 0 }} />);
  await preview(user);
  await user.click(screen.getByRole('button', { name: '确认提交' }));
  await screen.findByText('请核对资质');
  expect(screen.queryByRole('button', { name: '确认提交' })).toBeNull();
  await user.click(screen.getByRole('button', { name: '核对申请' }));
  await user.click(screen.getByRole('button', { name: '确认提交' }));
  await screen.findByText('签名申请已提交');
  expect(api.call).toHaveBeenCalledTimes(2);
  expect(api.query.mock.calls.filter(([action]) => action === 'GetApplySignatureBind')).toHaveLength(1);
});

it('不同材料分类共享五份上限，批量选择上传不遗漏且只提交私密引用', async () => {
  const user = userEvent.setup();
  const api = client();
  render(<SignatureForm client={api} prefill={{ source: 2, content: '示例科技', isLimitSubAccount: 0,
    appIcp: { appIcpFilling: '备案一号', appIcpFileList: Array.from({ length: 3 }, (_, index) =>
      ({ name: `app-${index}.png`, fileContent: `private/app-${index}`, fileSuffix: 'png' })) } }} />);
  await materials(user);
  fireEvent.change(screen.getByLabelText('更多资料'), { target: { files: [
    new File(['one'], 'one.zip'), new File(['two'], 'two.zip'), new File(['three'], 'three.zip'),
  ] } });
  await screen.findByText('本次最多上传 5 份材料。');
  await waitFor(() => expect(api.upload).toHaveBeenCalledTimes(2));
  await waitFor(() => expect(screen.getByRole('button', { name: '核对申请' }).disabled).toBe(false));
  await user.click(screen.getByRole('button', { name: '核对申请' }));
  await user.click(screen.getByRole('button', { name: '确认提交' }));
  await screen.findByText('签名申请已提交');
  const request = api.call.mock.calls[0][1].request;
  expect(request.appIcp.appIcpFileList).toHaveLength(3);
  expect(request.uploadFileList).toEqual([
    { fileType: 6, fileContent: 'private/one.zip', fileSuffix: 'zip' },
    { fileType: 6, fileContent: 'private/two.zip', fileSuffix: 'zip' },
  ]);
});

it('预填附件可在相同 Arco 上传控件内上传，图片回显只使用本地数据', async () => {
  const user = userEvent.setup();
  const api = client();
  render(<SignatureForm client={api} prefill={{ content: '示例科技', isLimitSubAccount: 0,
    uploadFileList: [{ name: 'proof.png', data: 'aGVsbG8=' }] }} />);
  await materials(user);
  await user.click(screen.getByRole('button', { name: '核对申请' }));
  await screen.findByText('请先上传或移除待上传的材料。');
  const upload = document.querySelector('[data-material="other"]');
  expect(within(upload).getByText('proof.png（待上传）')).toBeTruthy();
  const start = upload.querySelector('.arco-upload-list-start-icon');
  expect(start).toBeTruthy();
  fireEvent.click(start);
  await waitFor(() => expect(api.upload).toHaveBeenCalledTimes(1));
  await screen.findByText('proof.png');
  await user.click(screen.getByRole('button', { name: '核对申请' }));
  await user.click(screen.getByRole('button', { name: '确认提交' }));
  await screen.findByText('签名申请已提交');
  expect(api.call.mock.calls[0][1].request.uploadFileList).toEqual([
    { fileType: 6, fileContent: 'private/proof.png', fileSuffix: 'png' },
  ]);
});

it('放弃本次填写清理草稿并报告结束，不提交业务申请', async () => {
  const user = userEvent.setup();
  const api = client();
  render(<SignatureForm client={api} />);
  await screen.findByRole('button', { name: '下一步' });
  await user.click(screen.getByRole('button', { name: '放弃本次填写' }));
  await screen.findByText('本次填写已结束');
  expect(api.call).not.toHaveBeenCalled();
  expect(api.report).toHaveBeenCalledWith({ form: 'signature', state: 'abandoned' });
});
