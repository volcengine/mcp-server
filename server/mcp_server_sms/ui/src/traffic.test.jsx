import React from 'react';
import { afterEach, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { TrafficForm } from './traffic.jsx';
import { initialRow, parseLink, trafficPayload, validateRows } from './traffic-controller.js';
import { OperationError } from './client.js';

afterEach(cleanup);
const link = {
  useVolcLink: false, link: 'https://WWW.example.com/Original?Q=One#Section',
  linkDomainIcp: '文案备案号', linkDomainIcpBody: '文案主体',
  jumpLink: 'https://landing.example.com/Go?Next=Two',
  jumpLinkDomainIcp: '跳转备案号', jumpLinkDomainIcpBody: '跳转主体',
};
function client(overrides = {}) {
  return {
    call: vi.fn(async name => name === 'preview_traffic_resource' ? { count: 1 } : ''),
    report: vi.fn().mockResolvedValue(undefined), ...overrides,
  };
}
async function choose(user, label, name) {
  await user.click(screen.getByLabelText(label));
  const option = await screen.findByRole('option', { name, exact: true });
  await waitFor(() => expect(window.getComputedStyle(option).pointerEvents).not.toBe('none'));
  await user.click(option);
}
async function preview(user) {
  await user.click(screen.getByRole('button', { name: '预览录入内容' }));
  return screen.findByRole('region', { name: '录入预览' });
}

it('自有链接及跳转信息沿用原生 key，解析字段只读且保留原链接大小写与查询参数', async () => {
  const user = userEvent.setup();
  const api = client();
  render(<TrafficForm client={api} prefill={{ kind: 'link', data: [link] }} />);
  expect(screen.queryByLabelText('引流类型')).toBeNull();
  expect(screen.getByLabelText('使用火山短链').closest('.arco-select')).toBeTruthy();
  expect(screen.getByLabelText('文案链接二级域名').value).toBe('www.example.com');
  expect(screen.getByLabelText('文案链接 Path').value).toBe('/Original?Q=One');
  expect(screen.getByLabelText('跳转链接 Path').value).toBe('/Go?Next=Two');
  for (const label of ['文案链接二级域名', '文案链接 Path', '跳转链接二级域名', '跳转链接 Path']) {
    expect(screen.getByLabelText(label).readOnly).toBe(true);
  }
  const region = await preview(user);
  expect(within(region).getByText(link.link)).toBeTruthy();
  expect(api.call).toHaveBeenCalledWith('preview_traffic_resource', { request: {
    action: 'BulkCreateTobTrafficDrivingLinkForAgent', params: { data: [{
      ...link, protocol: 'https', linkDomain: 'www.example.com', linkPath: '/Original?Q=One',
      jumpLinkDomain: 'landing.example.com', jumpLinkPath: '/Go?Next=Two',
    }] },
  } });
  await user.click(screen.getByRole('button', { name: '确认录入' }));
  await screen.findByText('引流信息已提交');
  expect(api.call.mock.calls[1][1]).toEqual(api.call.mock.calls[0][1]);
  expect(api.call.mock.calls[1][2]).toEqual({ write: true });
  expect(screen.queryByLabelText('文案链接')).toBeNull();
  expect(api.report).toHaveBeenCalledWith({ form: 'traffic', state: 'accepted', kind: 'link', count: 1 });
});

it('火山短链只提交跳转分支，切换和字段修改会撤销旧预览', async () => {
  const user = userEvent.setup();
  const api = client();
  render(<TrafficForm client={api} prefill={{ kind: 'link', data: [link] }} />);
  await preview(user);
  await choose(user, '使用火山短链', '是');
  expect(screen.queryByRole('region', { name: '录入预览' })).toBeNull();
  expect(screen.queryByLabelText('文案链接')).toBeNull();
  expect(screen.getByLabelText('跳转链接').getAttribute('aria-required')).toBe('true');
  await preview(user);
  expect(api.call.mock.calls[1][1].request.params.data).toEqual([{
    useVolcLink: true, jumpLink: link.jumpLink,
    jumpLinkDomainIcp: link.jumpLinkDomainIcp, jumpLinkDomainIcpBody: link.jumpLinkDomainIcpBody,
    jumpLinkDomain: 'landing.example.com', jumpLinkPath: '/Go?Next=Two',
  }]);
  await user.type(screen.getByLabelText('跳转链接'), '&source=SMS');
  expect(screen.queryByRole('button', { name: '确认录入' })).toBeNull();
  expect(screen.getByLabelText('跳转链接 Path').value).toBe('/Go?Next=Two&source=SMS');
  expect(api.call.mock.calls.every(([name]) => name === 'preview_traffic_resource')).toBe(true);
});

it.each([
  ['http://example.com/Path?Q=1', 'http'], ['https://example.com/Path', 'https'],
  ['example.com/Path?Q=One', '缺省'],
])('文案链接输入和预填自动识别协议：%s', async (value, protocol) => {
  const user = userEvent.setup();
  const api = client();
  render(<TrafficForm client={api} prefill={{ kind: 'link', data: [{ ...link, link: value }] }} />);
  await preview(user);
  expect(api.call.mock.calls[0][1].request.params.data[0].protocol).toBe(protocol);
  await user.clear(screen.getByLabelText('文案链接'));
  await user.type(screen.getByLabelText('文案链接'), 'http://example.com/Changed?Case=Yes');
  await preview(user);
  expect(api.call.mock.calls[1][1].request.params.data[0]).toMatchObject({
    protocol: 'http', link: 'http://example.com/Changed?Case=Yes', linkPath: '/Changed?Case=Yes',
  });
});

it('缺少必填链接字段时在字段旁报错且不调用预览，非法链接不会让页面崩溃', async () => {
  const user = userEvent.setup();
  const api = client();
  render(<TrafficForm client={api} prefill={{ kind: 'link' }} />);
  await user.click(screen.getByRole('button', { name: '预览录入内容' }));
  expect(screen.getAllByText('此项必填')).toHaveLength(4);
  expect(screen.getByLabelText('文案链接').getAttribute('aria-invalid')).toBe('true');
  expect(api.call).not.toHaveBeenCalled();
  expect(parseLink('https://[')).toEqual({ domain: '', path: '' });
  expect(parseLink('')).toEqual({ domain: '', path: '' });
});

it.each([
  [1, '13800000000', '请输入正确的手机号'],
  [2, '4008000000', '请输入正确的 400 号码'],
  [3, '7001234', '请输入正确的 700 号码'],
  [4, '8001234567', '请输入正确的 800 号码'],
  [5, '95588', '请输入正确的 95 或 96 号码'],
  [6, '12345', '请输入正确的 12 号码'],
  [7, '01012345678', '请输入正确的固定电话'],
])('号码类型 %s 与 skill 相同，预填推断类型且格式校验不改原值', (numberType, number, message) => {
  expect(initialRow('phone', { number }).numberType).toBe(numberType);
  expect(validateRows('phone', [{ numberType, number }])).toEqual({});
  for (const invalid of [number + ' ', '+86' + number, number + '-']) {
    expect(validateRows('phone', [{ numberType, number: invalid }])).toEqual({ '0.number': message });
    expect(() => trafficPayload('phone', [{ numberType, number: invalid }])).toThrow(message);
  }
});

it('号码字段校验与证件枚举相同，切换企业号码不提交隐藏的个人信息', async () => {
  const user = userEvent.setup();
  const api = client();
  render(<TrafficForm client={api} prefill={{ kind: 'phone', data: [{
    number: '13800000000', numberPerson: '测试号主', personType: 1, personId: 'private-fixture',
    company: '预填企业', numberProvince: '北京', numberCity: '北京',
  }] }} />);
  await user.click(screen.getByLabelText('证件类型'));
  const option = await screen.findByRole('option', { name: '居民身份证' });
  expect(screen.getAllByRole('option')).toHaveLength(1);
  await waitFor(() => expect(window.getComputedStyle(option).pointerEvents).not.toBe('none'));
  await user.click(option);
  await preview(user);
  expect(api.call.mock.calls[0][1].request.params.data[0]).toEqual({
    numberType: 1, number: '13800000000', numberPerson: '测试号主', personType: 1,
    personId: 'private-fixture', numberProvince: '北京', numberCity: '北京',
  });
  await choose(user, '号码类型', '400 号码');
  expect(screen.queryByLabelText('证件号码')).toBeNull();
  expect(screen.queryByRole('button', { name: '确认录入' })).toBeNull();
  await user.click(screen.getByRole('button', { name: '预览录入内容' }));
  expect(screen.getByText('请输入正确的 400 号码')).toBeTruthy();
  expect(api.call).toHaveBeenCalledTimes(1);
  await user.clear(screen.getByLabelText('联系号码'));
  await user.type(screen.getByLabelText('联系号码'), '4008000000');
  await preview(user);
  expect(api.call.mock.calls[1][1].request.params.data[0]).toEqual({
    numberType: 2, number: '4008000000', company: '预填企业', numberProvince: '北京', numberCity: '北京',
  });
});

it.each(['按钮', 'Enter'])('宿主禁止原生 submit 时通过%s预览，Enter 不会直接写入', async action => {
  const user = userEvent.setup();
  const api = client();
  render(<TrafficForm client={api} prefill={{ kind: 'link', data: [link] }} />);
  const blockSubmit = vi.fn(event => { event.preventDefault(); event.stopImmediatePropagation(); });
  document.addEventListener('submit', blockSubmit, true);
  try {
    if (action === '按钮') await preview(user);
    else {
      await user.click(screen.getByLabelText('文案链接'));
      await user.keyboard('{Enter}');
      await screen.findByRole('region', { name: '录入预览' });
      await user.keyboard('{Enter}');
    }
    expect(blockSubmit).not.toHaveBeenCalled();
    expect(api.call.mock.calls.every(([name]) => name === 'preview_traffic_resource')).toBe(true);
    const count = api.call.mock.calls.length;
    fireEvent.keyDown(screen.getByLabelText('文案链接'), { key: 'Enter', isComposing: true });
    fireEvent.keyDown(screen.getByLabelText('文案链接协议').querySelector('input'), { key: 'Enter' });
    expect(api.call).toHaveBeenCalledTimes(count);
  } finally {
    document.removeEventListener('submit', blockSubmit, true);
  }
});

it('添加和移除撤销预览，批量条数沿用 MCP 的链接十条及号码一百条上限', async () => {
  const user = userEvent.setup();
  const api = client();
  const view = render(<TrafficForm client={api} prefill={{ kind: 'link', data: [link] }} />);
  await preview(user);
  await user.click(screen.getByRole('button', { name: '添加一条' }));
  expect(screen.queryByRole('region', { name: '录入预览' })).toBeNull();
  expect(screen.getAllByLabelText('文案链接')).toHaveLength(2);
  await user.click(screen.getAllByRole('button', { name: '移除' })[1]);
  expect(screen.getByLabelText('文案链接').value).toBe(link.link);
  await preview(user);
  await user.click(screen.getByRole('button', { name: '结束本次录入' }));
  await screen.findByText('本次录入已结束');
  expect(api.report).toHaveBeenCalledWith({ form: 'traffic', state: 'abandoned' });
  expect(screen.queryByLabelText('文案链接')).toBeNull();
  expect(api.call.mock.calls.every(([name]) => name === 'preview_traffic_resource')).toBe(true);
  view.unmount();
  const limit = render(<TrafficForm client={client()} prefill={{
    kind: 'link', data: Array.from({ length: 10 }, () => ({ ...link, jumpLink: undefined })),
  }} />);
  expect(screen.getByRole('button', { name: '添加一条' }).disabled).toBe(true);
  limit.unmount();
  for (const [kind, max, row] of [['link', 10, link], ['phone', 100, { number: '13800000000' }]]) {
    expect(trafficPayload(kind, Array.from({ length: max }, () => initialRow(kind, row)))).toHaveLength(max);
    expect(() => trafficPayload(kind, Array.from({ length: max + 1 }, () => initialRow(kind, row)))).toThrow();
  }
});

it('MCP 返回协议或重复项错误时不允许确认，已知写入失败需重新预览', async () => {
  const user = userEvent.setup();
  const api = client({ call: vi.fn().mockRejectedValueOnce(new OperationError('第 1 行协议与文案链接不一致'))
    .mockResolvedValueOnce({ count: 1 }).mockRejectedValueOnce(new OperationError('资源重复，请核对'))
    .mockResolvedValueOnce({ count: 1 }).mockResolvedValueOnce('') });
  render(<TrafficForm client={api} prefill={{ kind: 'link', data: [link] }} />);
  await user.click(screen.getByRole('button', { name: '预览录入内容' }));
  await screen.findByText('第 1 行协议与文案链接不一致');
  expect(screen.queryByRole('button', { name: '确认录入' })).toBeNull();
  await preview(user);
  await user.click(screen.getByRole('button', { name: '确认录入' }));
  await screen.findByText('资源重复，请核对');
  expect(screen.queryByRole('button', { name: '确认录入' })).toBeNull();
  expect(screen.getByLabelText('文案链接').value).toBe(link.link);
  await preview(user);
  await user.click(screen.getByRole('button', { name: '确认录入' }));
  await screen.findByText('引流信息已提交');
  expect(api.call.mock.calls.map(([name]) => name)).toEqual([
    'preview_traffic_resource', 'preview_traffic_resource', 'submit_traffic_resources',
    'preview_traffic_resource', 'submit_traffic_resources',
  ]);
});

it('未收到原生空字符串结果时锁定号码和个人字段，不报告受理或自动重试', async () => {
  const user = userEvent.setup();
  const api = client({ call: vi.fn().mockResolvedValueOnce({ count: 1 }).mockResolvedValueOnce({}) });
  render(<TrafficForm client={api} prefill={{ kind: 'phone', data: [{ number: '13800000000', personId: 'private-fixture' }] }} />);
  await preview(user);
  await user.click(screen.getByRole('button', { name: '确认录入' }));
  await screen.findByText('未收到明确的引流录入结果，请查询核对。');
  for (const label of ['联系号码', '号码所属人', '证件号码', '号码归属省份', '号码归属城市']) {
    expect(screen.getByLabelText(label).disabled).toBe(true);
  }
  await user.click(screen.getByRole('button', { name: '确认录入' }));
  expect(api.call).toHaveBeenCalledTimes(2);
  expect(api.report).not.toHaveBeenCalled();
});
