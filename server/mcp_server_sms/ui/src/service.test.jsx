import React from 'react';
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, expect, it, vi } from 'vitest';
import { ServiceForm } from './service.jsx';
import { OperationError } from './client.js';

afterEach(() => { cleanup(); vi.restoreAllMocks(); });
const activation = {
  status: 'activation_required', confirmation: 'current-confirmation', businessName: '测试企业',
  protocols: [
    { id: 17, title: '短信服务协议', url: 'https://example.com/terms' },
    { id: 18, title: '隐私协议', url: 'https://example.com/privacy' },
  ],
  pricingUrl: 'https://example.com/pricing', consoleUrl: 'https://example.com/console',
};
const renewal = { ...activation, status: 'protocol_confirmation_required', protocols: [activation.protocols[1]] };
function client(...responses) {
  return { call: vi.fn().mockImplementation(() => {
    const response = responses.shift();
    if (response instanceof Error) return Promise.reject(response);
    return Promise.resolve(response);
  }), report: vi.fn().mockResolvedValue(), canOpenLinks: vi.fn(() => false) };
}
async function consentAndSubmit(user, label = '同意协议并开通') {
  await user.click(await screen.findByRole('checkbox'));
  await user.click(screen.getByRole('button', { name: label }));
}

it.each([
  [activation, '开通国内短信服务', '同意协议并开通', '国内短信服务已开通', '服务与相关协议已经生效。'],
  [{ ...activation, status: 'reopening_required' }, '开通国内短信服务', '同意协议并开通', '国内短信服务已开通', '服务与相关协议已经生效。'],
  [renewal, '重新签署短信服务协议', '同意并重新签署', '短信服务协议已重新签署', '更新后的协议已生效，可继续使用国内短信服务。'],
])('必须勾选后才使用当前确认凭据提交：%s', async (view, title, label, success, description) => {
  const user = userEvent.setup();
  const api = client(view, { ...view, status: 'available', confirmation: undefined, requestId: 'submitted-request' });
  render(<ServiceForm client={api} />);
  await screen.findByRole('heading', { name: title });
  const button = screen.getByRole('button', { name: label });
  expect(button.disabled).toBe(true);
  expect(button.type).toBe('button');
  expect(screen.getByRole('list').querySelectorAll('li')).toHaveLength(view.protocols.length);
  expect(api.call.mock.calls).toEqual([['get_sms_service_onboarding']]);
  await user.click(button);
  expect(api.call).toHaveBeenCalledTimes(1);
  await consentAndSubmit(user, label);
  await screen.findByText(success);
  expect(screen.getByText(description)).toBeTruthy();
  expect(api.call).toHaveBeenCalledWith('submit_sms_service_onboarding', { confirmation: 'current-confirmation' }, { write: true });
  expect(api.report).toHaveBeenCalledWith({ form: 'service', state: 'available', requestId: 'submitted-request' });
  expect(screen.queryByRole('checkbox')).toBeNull();
});

it('刷新撤销同意，协议变化后只提交新的确认凭据', async () => {
  const user = userEvent.setup();
  const api = client(activation, { ...renewal, confirmation: 'updated-confirmation' }, { status: 'available' });
  render(<ServiceForm client={api} />);
  await user.click(await screen.findByRole('checkbox'));
  await user.click(screen.getByRole('button', { name: '刷新服务状态' }));
  await screen.findByRole('heading', { name: '重新签署短信服务协议' });
  expect(screen.getByRole('checkbox').checked).toBe(false);
  expect(screen.getByRole('button', { name: '同意并重新签署' }).disabled).toBe(true);
  expect(screen.queryByText('短信服务协议', { exact: true })).toBeNull();
  await consentAndSubmit(user, '同意并重新签署');
  expect(api.call.mock.calls[2]).toEqual(['submit_sms_service_onboarding', { confirmation: 'updated-confirmation' }, { write: true }]);
});

it.each([
  [activation, '已取消开通', '本次未提交国内短信服务开通请求。'],
  [renewal, '已取消重新签署', '本次未重新签署更新后的短信服务协议。'],
])('取消只结束本次页面，不写业务接口：%s', async (view, title, description) => {
  const user = userEvent.setup();
  const api = client(view);
  render(<ServiceForm client={api} />);
  await user.click(await screen.findByRole('button', { name: '取消' }));
  await screen.findByText(title);
  expect(screen.getByText(description)).toBeTruthy();
  expect(api.call.mock.calls).toEqual([['get_sms_service_onboarding']]);
  expect(api.report).toHaveBeenCalledWith({ form: 'service', state: 'abandoned' });
  expect(screen.queryByRole('checkbox')).toBeNull();
  expect(screen.queryByRole('button', { name: '刷新服务状态' })).toBeNull();
});

it('同意后双击只提交一次，提交期间不能取消或刷新', async () => {
  const user = userEvent.setup();
  let resolve;
  const api = client(activation);
  api.call.mockImplementationOnce(() => Promise.resolve(activation))
    .mockImplementationOnce(() => new Promise(done => { resolve = done; }));
  render(<ServiceForm client={api} />);
  await user.click(await screen.findByRole('checkbox'));
  await user.dblClick(screen.getByRole('button', { name: '同意协议并开通' }));
  expect(api.call).toHaveBeenCalledTimes(2);
  expect(screen.getByRole('button', { name: '取消' }).disabled).toBe(true);
  expect(screen.getByRole('button', { name: '刷新服务状态' }).disabled).toBe(true);
  await act(async () => { resolve({ status: 'available' }); });
  await screen.findByText('国内短信服务已开通');
});

it.each([
  [activation, 'activation_pending', '同意协议并开通', '国内短信服务已开通'],
  [renewal, 'protocol_confirmation_pending', '同意并重新签署', '短信服务协议已重新签署'],
])('已受理后旧状态不能解锁，核实成功保留原操作文案：%s', async (view, status, label, title) => {
  const user = userEvent.setup();
  const api = client(view, { status, requestId: 'pending-request' }, view, { status: 'available' });
  render(<ServiceForm client={api} />);
  await consentAndSubmit(user, label);
  await screen.findByText('请求已提交');
  await user.click(screen.getByRole('button', { name: '刷新服务状态' }));
  expect(screen.queryByRole('button', { name: label })).toBeNull();
  expect(screen.getByText('请求编号：pending-request')).toBeTruthy();
  await user.click(screen.getByRole('button', { name: '刷新服务状态' }));
  await screen.findByText(title);
  expect(api.call.mock.calls.filter(([name]) => name === 'submit_sms_service_onboarding')).toHaveLength(1);
});

it('未知写结果保留原始错误并锁定重试，仍可刷新核实', async () => {
  const user = userEvent.setup();
  const api = client(activation, new OperationError('上游响应中断', {
    unknown: true, code: 'upstream_timeout', requestId: 'unknown-request', httpStatus: 504,
  }), activation, { status: 'available' });
  render(<ServiceForm client={api} />);
  await consentAndSubmit(user);
  await screen.findByText('操作结果待核实');
  expect(screen.getByText('上游响应中断')).toBeTruthy();
  expect(screen.getByText('错误码：upstream_timeout')).toBeTruthy();
  expect(screen.getByText('HTTP 状态：504')).toBeTruthy();
  expect(screen.getByText('排障编号：unknown-request')).toBeTruthy();
  await user.click(screen.getByRole('button', { name: '刷新服务状态' }));
  expect(screen.queryByRole('button', { name: '同意协议并开通' })).toBeNull();
  expect(screen.queryByRole('button', { name: '取消' })).toBeNull();
  await user.click(screen.getByRole('button', { name: '刷新服务状态' }));
  await screen.findByText('国内短信服务已开通');
  expect(api.call.mock.calls.filter(([name]) => name === 'submit_sms_service_onboarding')).toHaveLength(1);
});

it('协议凭据失效后必须刷新并重新勾选', async () => {
  const user = userEvent.setup();
  const api = client(activation, new OperationError('账号状态或协议清单已变化，请刷新后重新确认', {
    code: 'service_confirmation_changed', requestId: 'changed-request',
  }), { ...activation, confirmation: 'fresh-confirmation' }, { status: 'available' });
  render(<ServiceForm client={api} />);
  await consentAndSubmit(user);
  await screen.findByText('国内短信服务开通未完成');
  expect(screen.getByText('错误码：service_confirmation_changed')).toBeTruthy();
  expect(screen.queryByRole('button', { name: '同意协议并开通' })).toBeNull();
  await user.click(screen.getByRole('button', { name: '刷新服务状态' }));
  expect(screen.getByRole('button', { name: '同意协议并开通' }).disabled).toBe(true);
  await consentAndSubmit(user);
  expect(api.call.mock.calls[3]).toEqual(['submit_sms_service_onboarding', { confirmation: 'fresh-confirmation' }, { write: true }]);
});

it('部分协议失败展示编号，刷新前不能重签', async () => {
  const user = userEvent.setup();
  const api = client(renewal, { ...renewal, confirmation: undefined,
    status: 'protocol_confirmation_failed', failedDocuments: [18], requestId: 'partial-request' });
  render(<ServiceForm client={api} />);
  await consentAndSubmit(user, '同意并重新签署');
  await screen.findByText('短信服务协议重新签署未完成');
  expect(screen.getByText('签署失败的协议编号 18。请刷新后核对。')).toBeTruthy();
  expect(screen.queryByRole('checkbox')).toBeNull();
});

it('开通错误保留 MCP 原始错误、HTTP 状态及排障编号', async () => {
  const user = userEvent.setup();
  const api = client(activation, { ...activation, confirmation: undefined, status: 'activation_error',
    requestId: 'activation-request', errorCode: 'activation_denied',
    failure: { request_id: 'failure-request', error: { code: 'activation_denied', message: '商品开通失败原文', http_status: 403 } } });
  render(<ServiceForm client={api} />);
  await consentAndSubmit(user);
  await screen.findByText('国内短信服务开通未完成');
  expect(screen.getByText('商品开通失败原文')).toBeTruthy();
  expect(screen.getByText('HTTP 状态：403')).toBeTruthy();
  expect(screen.getByText('排障编号：failure-request')).toBeTruthy();
  expect(screen.getByText('请求编号：activation-request')).toBeTruthy();
});

it.each([
  'product_not_allowed', 'product_forced_closed', 'account_disabled', 'arrears_closed',
  'expired_closed', 'protocol_state_unknown', 'service_state_unknown',
  'submission_in_progress', 'submission_outcome_unknown', 'available',
])('不可办理状态即使含确认凭据也不展示提交：%s', async status => {
  const api = client({ ...activation, status });
  render(<ServiceForm client={api} />);
  await screen.findByRole('button', { name: '刷新服务状态' });
  expect(screen.queryByRole('checkbox')).toBeNull();
  expect(screen.queryByRole('button', { name: '同意协议并开通' })).toBeNull();
  expect(api.call.mock.calls).toEqual([['get_sms_service_onboarding']]);
});

it('初次查询失败可以刷新，卸载后的迟到查询不报告结果', async () => {
  const user = userEvent.setup();
  let resolve;
  const api = client(new OperationError('服务状态查询失败'));
  api.call.mockRejectedValueOnce(new OperationError('服务状态查询失败'))
    .mockImplementationOnce(() => new Promise(done => { resolve = done; }));
  const page = render(<ServiceForm client={api} />);
  await screen.findByText('服务状态查询失败');
  await user.click(screen.getByRole('button', { name: '刷新服务状态' }));
  page.unmount();
  await act(async () => { resolve({ status: 'available' }); });
  expect(api.report).not.toHaveBeenCalled();
});

it('协议、计费和控制台链接使用宿主能力，无能力时回显完整地址', async () => {
  const user = userEvent.setup();
  const api = client(activation);
  api.canOpenLinks.mockReturnValue(true);
  api.openLink = vi.fn().mockResolvedValue();
  const page = render(<ServiceForm client={api} />);
  for (const [title, url] of [
    ['短信服务协议', activation.protocols[0].url], ['隐私协议', activation.protocols[1].url],
    ['查看国内短信计费说明', activation.pricingUrl], ['打开短信控制台', activation.consoleUrl],
  ]) {
    await user.click(await screen.findByRole('button', { name: title }));
    expect(api.openLink).toHaveBeenLastCalledWith(url);
  }
  expect(api.call).toHaveBeenCalledTimes(1);
  page.unmount();
  render(<ServiceForm client={client(activation)} />);
  await screen.findByText(activation.protocols[0].url);
  expect(screen.getByText(activation.pricingUrl)).toBeTruthy();
  expect(screen.queryByRole('link')).toBeNull();
});

it('宿主阻断原生 submit 时按钮仍可完成开通', async () => {
  const api = client(activation, { status: 'available' });
  const submitEvent = vi.fn(event => event.preventDefault());
  document.addEventListener('submit', submitEvent);
  try {
    render(<ServiceForm client={api} />);
    fireEvent.click(await screen.findByRole('checkbox'));
    fireEvent.click(screen.getByRole('button', { name: '同意协议并开通' }));
    await screen.findByText('国内短信服务已开通');
    expect(submitEvent).not.toHaveBeenCalled();
    expect(api.call.mock.calls[1]).toEqual(['submit_sms_service_onboarding', { confirmation: 'current-confirmation' }, { write: true }]);
  } finally { document.removeEventListener('submit', submitEvent); }
});
