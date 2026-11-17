import React from 'react';
import { afterEach, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { TemplateForm, templatePayload } from './template.jsx';
import { BatchForm } from './batch.jsx';
import { SmsApp } from './app.jsx';
import { OperationError, SmsFormClient } from './client.js';

afterEach(cleanup);

it('模板提交展示后端 1007 原文与编号，不把错误改成未知结果或自动重试', async () => {
  const message = '营销模板末尾必须为拒收请回复R且退订关键词必须在模版末尾';
  const backend = { ResponseMetadata: { RequestId: 'template-request', Error: { Code: '1007', Message: message } } };
  const app = { callServerTool: vi.fn(async ({ name, arguments: args }) => {
    if (name === 'preview_template') return { _meta: { 'sms/form': { success: true, result: preview(args.request) } } };
    if (name === 'submit_template') return { isError: true, structuredContent: {
      success: false, request_id: 'template-request', error: { code: '1007', message, http_status: 400, backend_response: backend },
    } };
    const action = args.request.action;
    const result = action === 'GetSubAccountListForAgent'
      ? { list: [{ subAccountId: 'g', subAccountName: '测试消息组' }], total: 1 }
      : { List: [{ Signature: '测试签名' }], Total: 1 };
    return { structuredContent: { success: true, result } };
  }) };
  const user = userEvent.setup();
  render(<TemplateForm client={new SmsFormClient(app)} prefill={{ name: '活动通知', content: '活动优惠 拒收请回复R',
    channelType: 'CN_MKT', signatures: ['测试签名'], subAccounts: ['g'], templateParams: [] }} />);
  await waitFor(() => expect(screen.getByRole('button', { name: '核对模板申请' }).disabled).toBe(false));
  await user.click(screen.getByRole('button', { name: '核对模板申请' }));
  await screen.findByRole('button', { name: '确认提交模板' });
  await user.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await user.click(screen.getByRole('button', { name: '确认提交模板' }));
  await screen.findByText(message);
  expect(screen.getByText('错误码：1007')).toBeTruthy();
  expect(screen.getByText('HTTP 状态：400')).toBeTruthy();
  expect(screen.getByText('排障编号：template-request')).toBeTruthy();
  expect(screen.getByLabelText('模版内容').value).toBe('活动优惠 拒收请回复R');
  expect(app.callServerTool.mock.calls.filter(([call]) => call.name === 'submit_template')).toHaveLength(1);
});
function preview(request) {
  return { request: { ...request, area: 'cn' }, account: { userType: 'enterprise', mktParam: 1 },
    fixedTraffic: [], warnings: [], confirmation: 'a'.repeat(64) };
}
function client() {
  return { report: vi.fn().mockResolvedValue(undefined), query: vi.fn(async action => {
    if (action === 'GetSubAccountListForAgent') return { list: [{ subAccountId: 'g', subAccountName: '测试消息组' }], total: 1 };
    if (action === 'ListSignaturesForAgent') return { List: [{ Signature: '测试签名' }], Total: 1 };
    return { list: [], total: 0 };
  }), call: vi.fn(async (name, args) => {
    if (name === 'preview_template') return preview(args.request);
    if (name === 'submit_template') return { templateId: 't', status: 1 };
    throw new Error('unexpected call');
  }) };
}


it('模板表单预填完整字段，返回修改保留内容，页面确认后才提交', async () => {
  const api = client(); const user = userEvent.setup();
  const draft = { name: '双十一', content: '优惠 ${url} 拒收请回复R', channelType: 'CN_MKT', signatures: ['测试签名'], subAccounts: ['g'],
    desc: ' 原用途 ', project: '项目', templateParams: [{ name: 'url', paramType: 2 }],
    shortUrlConfig: { isEnabled: '1', belong: 'VMS', isNeedClickDetails: '1', uaCheckStrategy: 3 },
    templateTrafficDriving: [[{ name: 'url', paramType: 2, id: 12, content: 'https://example.com/Path?Q=A' }]] };
  render(<TemplateForm client={api} prefill={draft} />);
  await waitFor(() => expect(api.query.mock.calls.some(([action]) => action === 'ListSignaturesForAgent')).toBe(true));
  await waitFor(() => expect(screen.getByRole('button', { name: '核对模板申请' }).disabled).toBe(false));
  await user.click(screen.getByRole('button', { name: '核对模板申请' }));
  await screen.findByRole('button', { name: '确认提交模板' });
  expect(api.call.mock.calls.map(([name]) => name)).toEqual(['preview_template']);
  await user.click(screen.getByRole('button', { name: '返回修改' }));
  expect(screen.getByLabelText('模版内容').value).toBe(draft.content);
  expect(screen.getByLabelText('模版用途').value).toBe(draft.desc);
  await user.click(screen.getByRole('button', { name: '核对模板申请' }));
  await user.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await user.click(screen.getByRole('button', { name: '确认提交模板' }));
  await screen.findByText('模板申请已受理');
  expect(api.call).toHaveBeenCalledWith('submit_template', { request: { ...draft, area: 'cn' }, confirmation: 'a'.repeat(64) }, { write: true });
});

it('模板变量、组合绑定和验证码占位符校验不会自动改写用户内容', () => {
  const draft = { name: 'n', content: '验证码 ${code}', channelType: 'CN_OTP', signatures: ['s'], subAccounts: ['g'], templateParams: [{ name: 'code', paramType: 1 }] };
  expect(templatePayload(draft).content).toBe(draft.content);
  expect(() => templatePayload({ ...draft, content: '${code}${code}' })).toThrow('一个普通变量');
  expect(() => templatePayload({ ...draft, templateParams: [] })).toThrow('一一对应');
  expect(() => templatePayload({ ...draft, shortUrlConfig: { isEnabled: '1' } })).toThrow('营销短信');
});

it('已有任务开表只查询，页面内确认后才启动，不重新创建', async () => {
  let status = 2;
  const api = client(); const normal = api.call.getMockImplementation();
  api.call.mockImplementation(async (name, ...args) => {
    if (name === 'query_batch_tasks') return { taskId: 'task', subAccount: 'g', templateId: 't', signature: '测试签名', name: '历史任务', sendContent: '实际正文', status };
    if (name === 'start_batch_task') { status = 3; return null; }
    return normal(name, ...args);
  });
  const user = userEvent.setup();
  render(<BatchForm client={api} initialTask={{ subAccount: 'g', taskId: 'task' }} />);
  await screen.findByText('历史任务');
  expect(api.query).not.toHaveBeenCalled();
  expect(api.call.mock.calls.map(([name]) => name)).toEqual(['query_batch_tasks']);
  await user.click(screen.getByRole('button', { name: '核对并启动' }));
  await screen.findByText('实际正文');
  await user.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await user.click(screen.getByRole('button', { name: '确认启动群发' }));
  await screen.findByText('启动请求已受理，请刷新核对最新状态。');
  expect(api.call).toHaveBeenCalledWith('start_batch_task', { sub_account: 'g', task_id: 'task' }, { write: true });
  expect(api.call.mock.calls.some(([name]) => name === 'create_batch_task')).toBe(false);
});

it('启动返回 1999 但任务状态已推进时只回查一次且不重复启动', async () => {
  let reads = 0;
  const api = client(); const normal = api.call.getMockImplementation();
  api.call.mockImplementation(async (name, ...args) => {
    if (name === 'query_batch_tasks') {
      reads += 1;
      return { taskId: 'task', subAccount: 'g', templateId: 't', signature: '测试签名',
        name: '历史任务', sendContent: '实际正文', status: reads < 3 ? 2 : 3 };
    }
    if (name === 'start_batch_task') {
      throw new OperationError('Invalid operation to the record, please check the status and the permission', {
        code: 1999, httpStatus: 200, requestId: 'request-id',
      });
    }
    return normal(name, ...args);
  });
  const user = userEvent.setup();
  render(<BatchForm client={api} initialTask={{ subAccount: 'g', taskId: 'task' }} />);
  await screen.findByText('历史任务');
  await user.click(screen.getByRole('button', { name: '核对并启动' }));
  await user.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await user.click(screen.getByRole('button', { name: '确认启动群发' }));
  await screen.findByText('任务已启动，送达结果请查询回执');
  expect(api.call.mock.calls.filter(([name]) => name === 'start_batch_task')).toHaveLength(1);
  expect(api.call.mock.calls.filter(([name]) => name === 'query_batch_tasks')).toHaveLength(3);
  expect(screen.queryByText(/Invalid operation/)).toBeNull();
  expect(api.report).toHaveBeenCalledWith({
    form: 'batch', state: 'operation_already_applied', taskId: 'task', operation: 'start',
  });
});

it('不支持表单的宿主给出控制台路径，不声称存在文本提交后备工具', () => {
  render(<SmsApp client={client()} ready supported={false} />);
  expect(screen.getByText(/支持 MCP Apps 的客户端或短信控制台/)).toBeTruthy();
  expect(screen.queryByText(/文本工具/)).toBeNull();
});

async function choose(user, label, text) {
  await user.click(screen.getByLabelText(label));
  const option = await screen.findByRole('option', { name: text });
  await waitFor(() => expect(window.getComputedStyle(option).pointerEvents).not.toBe('none'));
  // Arco 多选的 option 外层仅提供语义，实际点击目标为内部文字。
  await user.click(option.querySelector('.arco-select-option') ?? option);
}

it('历史任务首次读取失败，刷新补齐身份详情后可以核对启动', async () => {
  const api = client(); let reads = 0;
  api.call.mockImplementation(async name => {
    if (name === 'query_batch_tasks') {
      reads += 1;
      if (reads === 1) throw new OperationError('查询暂不可用');
      return { taskId: 'task', subAccount: 'g', templateId: 't', signature: '测试签名', name: '恢复的任务', sendContent: '已核实正文', status: 2 };
    }
    throw new Error('unexpected write');
  });
  const user = userEvent.setup();
  render(<BatchForm client={api} initialTask={{ subAccount: 'g', taskId: 'task' }} />);
  await screen.findByText('查询暂不可用');
  await user.click(screen.getByRole('button', { name: '刷新任务状态' }));
  await screen.findByText('恢复的任务');
  await user.click(screen.getByRole('button', { name: '核对并启动' }));
  await screen.findByText('已核实正文');
  expect(screen.getByRole('button', { name: '确认启动群发' }).disabled).toBe(true);
  expect(api.call.mock.calls.every(([name]) => name === 'query_batch_tasks')).toBe(true);
});

it.each([{ channelType: 'CN_NTC' }, { subAccounts: ['g'] }])('模板缺少消息组或待补类型时仍按预填名称核对签名 %j', async partial => {
  const api = client(); const normal = api.query.getMockImplementation();
  api.query.mockImplementation((action, params) => action === 'ListSignaturesForAgent'
    ? Promise.resolve({ List: params.Signature === '测试签名' ? [{ Signature: '测试签名' }] : [], Total: params.Signature ? 1 : 0 })
    : normal(action, params));
  const user = userEvent.setup();
  render(<TemplateForm client={api} prefill={{ ...partial, name: '测试模板', content: '预约 ${time}',
    signatures: ['测试签名'], templateParams: [{ name: 'time', paramType: 1 }] }} />);
  if (!partial.channelType) {
    await waitFor(() => expect(screen.getByRole('button', { name: '核对模板申请' }).disabled).toBe(false));
    await choose(user, '模版类型', '通知');
  }
  await waitFor(() => expect(api.query.mock.calls.filter(([action]) => action === 'ListSignaturesForAgent').map(([, params]) => params))
    .toContainEqual(expect.objectContaining({ Signature: '测试签名', ChannelTypes: ['CN_NTC'],
      ...(partial.subAccounts ? { SubAccounts: ['g'] } : {}) })));
  expect(api.query.mock.calls.some(([action]) => action === 'GetSubAccountListForAgent')).toBe(false);
  if (!partial.subAccounts) expect(api.query.mock.calls.every(([, params]) => !Object.hasOwn(params, 'SubAccounts'))).toBe(true);
  await waitFor(() => expect(screen.getByRole('button', { name: '核对模板申请' }).disabled).toBe(false));
  await user.click(screen.getByRole('button', { name: '核对模板申请' }));
  await screen.findByRole('button', { name: '确认提交模板' });
  expect(api.call.mock.calls.map(([name]) => name)).toEqual(['preview_template']);
});

it('模板明确更换已确定的短信类型时清除原签名，要求重新选择', async () => {
  const api = client(); const user = userEvent.setup();
  render(<TemplateForm client={api} prefill={{ subAccounts: ['g'], channelType: 'CN_NTC', name: '测试模板',
    content: '原文', signatures: ['测试签名'] }} />);
  await waitFor(() => expect(api.query.mock.calls.some(([action]) => action === 'ListSignaturesForAgent')).toBe(true));
  await waitFor(() => expect(screen.getByRole('button', { name: '核对模板申请' }).disabled).toBe(false));
  await choose(user, '模版类型', '营销');
  await waitFor(() => expect(screen.getByRole('button', { name: '核对模板申请' }).disabled).toBe(false));
  await user.click(screen.getByRole('button', { name: '核对模板申请' }));
  await screen.findByText('请至少选择一个签名。');
  expect(api.call).not.toHaveBeenCalled();
});


it('历史任务启动受理后回查失败，关闭确认框且不能重复提交启动', async () => {
  const api = client(); let reads = 0;
  api.call.mockImplementation(async name => {
    if (name === 'query_batch_tasks') {
      if (++reads === 3) throw new OperationError('查询最新状态失败');
      return { taskId: 'task', subAccount: 'g', templateId: 't', signature: '测试签名',
        sendContent: '实际正文', status: reads < 3 ? 2 : 3 };
    }
    if (name === 'start_batch_task') return null;
    throw new Error('unexpected call');
  });
  const user = userEvent.setup();
  render(<BatchForm client={api} initialTask={{ subAccount: 'g', taskId: 'task' }} />);
  await user.click(await screen.findByRole('button', { name: '核对并启动' }));
  await user.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await user.click(screen.getByRole('button', { name: '确认启动群发' }));
  await screen.findByText('查询最新状态失败');
  expect(screen.queryByRole('button', { name: '确认启动群发' })).toBeNull();
  expect(screen.queryByRole('button', { name: '核对并启动' })).toBeNull();
  await user.click(screen.getByRole('button', { name: '刷新任务状态' }));
  await screen.findByText('任务已启动，送达结果请查询回执');
  expect(api.call.mock.calls.filter(([name]) => name === 'start_batch_task')).toHaveLength(1);
});


it.each([3, 4, 5, 6])('重新打开状态为 %s 的已启动任务只查询，不再提供核对启动', async status => {
  const api = client();
  api.call.mockImplementation(async name => {
    if (name === 'query_batch_tasks') return { taskId: 'task', subAccount: 'g', status };
    throw new Error('unexpected write');
  });
  render(<BatchForm client={api} initialTask={{ subAccount: 'g', taskId: 'task' }} />);
  await screen.findByText('任务已启动，送达结果请查询回执');
  expect(screen.queryByRole('button', { name: '核对并启动' })).toBeNull();
  expect(screen.queryByRole('button', { name: '确认启动群发' })).toBeNull();
  expect(screen.getByText(/已确认发送，无需再次启动/)).toBeTruthy();
  expect(api.call.mock.calls.map(([name]) => name)).toEqual(['query_batch_tasks']);
});

it('旧页面显示待确认但回查已启动时，直接同步状态，不报错也不再次启动', async () => {
  const api = client(); let reads = 0;
  api.call.mockImplementation(async name => {
    if (name === 'query_batch_tasks') return { taskId: 'task', subAccount: 'g',
      templateId: 't', signature: '测试签名', sendContent: '实际正文', status: ++reads === 1 ? 2 : 3 };
    throw new Error('unexpected write');
  });
  const user = userEvent.setup();
  render(<BatchForm client={api} initialTask={{ subAccount: 'g', taskId: 'task' }} />);
  await screen.findByText('待确认发送');
  await user.click(screen.getByRole('button', { name: '核对并启动' }));
  await screen.findByText('任务已启动，送达结果请查询回执');
  expect(screen.queryByText('任务尚未通过校验或已启动、结束，请核对最新状态。')).toBeNull();
  expect(screen.queryByText('待确认发送')).toBeNull();
  expect(screen.queryByRole('button', { name: '核对并启动' })).toBeNull();
  expect(screen.queryByRole('button', { name: '确认启动群发' })).toBeNull();
  expect(api.call.mock.calls.map(([name]) => name)).toEqual(['query_batch_tasks', 'query_batch_tasks']);
  expect(api.report).toHaveBeenCalledWith({
    form: 'batch', state: 'operation_already_applied', taskId: 'task', operation: 'start',
  });
});

it('回查已取消任务先更新旧状态，再拒绝启动，不继续显示待确认', async () => {
  const api = client(); let reads = 0;
  api.call.mockImplementation(async name => {
    if (name === 'query_batch_tasks') return { taskId: 'task', subAccount: 'g',
      templateId: 't', signature: '测试签名', status: ++reads === 1 ? 2 : 7 };
    throw new Error('unexpected write');
  });
  const user = userEvent.setup();
  render(<BatchForm client={api} initialTask={{ subAccount: 'g', taskId: 'task' }} />);
  await screen.findByText('待确认发送');
  await user.click(screen.getByRole('button', { name: '核对并启动' }));
  await screen.findByText('任务尚未通过校验或已启动、结束，请核对最新状态。');
  expect(screen.queryByText('待确认发送')).toBeNull();
  expect(screen.queryByRole('button', { name: '确认启动群发' })).toBeNull();
  expect(api.call.mock.calls.every(([name]) => name === 'query_batch_tasks')).toBe(true);
});
