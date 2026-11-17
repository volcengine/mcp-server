import React from 'react';
import { afterEach, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BatchForm, batchPayload } from './batch.jsx';
import { OperationError } from './client.js';

afterEach(() => { cleanup(); vi.restoreAllMocks(); vi.useRealTimers(); });
const consent = '我已核对任务信息、文件校验结果和发送时间，同意创建任务并启动发送';
const template = { TemplateId: 't', TemplateName: '通知模板', ChannelType: 'CN_NTC', TemplateContent: '预约 ${time}' };
const recipients = { name: '名单.csv', file: 'private/list.csv', receipt: {
  signature: 'signed-list', context: { name: '名单.csv', file: 'private/list.csv', expires_at: 9999999999 },
} };
function client(overrides = {}) {
  let started = false;
  return { report: vi.fn().mockResolvedValue(undefined), downloadCsv: vi.fn(), upload: vi.fn(),
    query: vi.fn(async action => {
      if (action === 'GetSubAccountListForAgent') return { list: [{ subAccountId: 'g', subAccountName: '通知组' }], total: 1 };
      if (action === 'ListSignaturesForAgent') return { List: [{ Signature: '签名' }], Total: 1 };
      if (action === 'ValidateBatchTaskContentForAgent') return { Approved: true };
      return { List: [template], Total: 1 };
    }),
    call: vi.fn(async (name, args) => {
      if (name === 'get_batch_csv_template') return { value: 'phone,time\n', variables: ['time'] };
      if (name === 'complete_recipients_upload') return { file: args.request.context.file,
        receipt: args.request, totalCount: 5, dupCount: 2 };
      if (name === 'create_batch_task') return { taskId: 'task', totalCount: 3, dupCount: 2 };
      if (name === 'start_batch_task') { started = true; return null; }
      if (name === 'query_batch_tasks') return { taskId: 'task', subAccount: 'g', templateId: 't', signature: '签名', status: started ? 3 : 2 };
      throw new Error('unexpected call');
    }), ...overrides };
}
function open(api, overrides = {}) {
  return render(<BatchForm client={api} prefill={{ name: '预约通知', subAccount: 'g', signature: '签名',
    templateId: 't', recipientsFile: recipients, ...overrides }} />);
}
function calls(api, name) { return api.call.mock.calls.filter(([tool]) => tool === name); }
async function reviewed() {
  await screen.findByText(consent);
  await waitFor(() => expect(screen.getByLabelText('群发 CSV 名单').disabled).toBe(false));
}

async function openEditable(api) {
  open(api, { name: undefined });
  await screen.findByRole('button', { name: '点击下载模板' });
  await waitFor(() => expect(screen.getByLabelText('任务名称').disabled).toBe(false));
  fireEvent.change(screen.getByLabelText('任务名称'), { target: { value: '预约通知' } });
  await reviewed();
}

it('完整且有效的预填信息只读展示，自动校验名单，未确认不创建或启动', async () => {
  const api = client(); open(api); await reviewed();
  const counts = document.querySelector('.batch-counts');
  expect(within(counts.children[0]).getByText('3')).toBeTruthy();
  expect(within(counts.children[1]).getByText('2')).toBeTruthy();
  const info = screen.getByRole('region', { name: '任务信息' });
  expect(within(info).getByText('预约通知')).toBeTruthy();
  expect(within(info).getByText('g')).toBeTruthy();
  expect(within(info).getByText('签名')).toBeTruthy();
  expect(within(info).queryByRole('textbox')).toBeNull();
  expect(within(info).queryByRole('combobox')).toBeNull();
  expect(screen.queryByRole('button', { name: '加载更多' })).toBeNull();
  expect(calls(api, 'complete_recipients_upload')).toHaveLength(1);
  expect(calls(api, 'create_batch_task')).toHaveLength(0);
  expect(calls(api, 'start_batch_task')).toHaveLength(0);
  expect(screen.getByRole('button', { name: '确认创建并启动' }).disabled).toBe(true);
});

it('编辑任务信息立即撤销旧确认，重新校验可复用同一名单', async () => {
  const api = client(); const user = userEvent.setup(); await openEditable(api);
  await user.click(screen.getByText(consent));
  expect(screen.getByRole('button', { name: '确认创建并启动' }).disabled).toBe(false);
  fireEvent.change(screen.getByLabelText('任务名称'), { target: { value: '修改后的名称' } });
  expect(screen.queryByText(consent)).toBeNull();
  expect(screen.getByRole('button', { name: '确认创建并启动' }).disabled).toBe(true);
  await reviewed();
  expect(screen.getByRole('checkbox', { name: consent }).checked).toBe(false);
  expect(calls(api, 'complete_recipients_upload')).toHaveLength(1);
});

it('禁止原生表单提交的沙箱仍可一次确认创建并启动，双击只执行一次', async () => {
  const api = client(); const user = userEvent.setup(); let resolve;
  const normal = api.call.getMockImplementation();
  api.call.mockImplementation((name, args) => name === 'create_batch_task'
    ? new Promise(done => { resolve = done; }) : normal(name, args));
  const block = vi.fn(event => event.preventDefault());
  document.addEventListener('submit', block, true);
  try {
    open(api); await reviewed(); await user.click(screen.getByText(consent));
    await user.dblClick(screen.getByRole('button', { name: '确认创建并启动' }));
    expect(calls(api, 'create_batch_task')).toHaveLength(1);
    expect(block).not.toHaveBeenCalled();
    resolve({ taskId: 'task', totalCount: 3, dupCount: 2 });
    await screen.findByText('群发任务已创建并确认发送');
    await waitFor(() => expect(calls(api, 'start_batch_task')).toHaveLength(1));
    expect(api.report).toHaveBeenCalledWith({ form: 'batch', state: 'created', taskId: 'task', totalCount: 3, dupCount: 2 });
    expect(JSON.stringify(api.report.mock.calls)).not.toContain('private/list.csv');
  } finally { document.removeEventListener('submit', block, true); }
});

it('已知创建失败保留同一请求的幂等键，重试前重新确认', async () => {
  const api = client(); const user = userEvent.setup(); const normal = api.call.getMockImplementation();
  let writes = 0;
  api.call.mockImplementation((name, args) => name === 'create_batch_task' && ++writes === 1
    ? Promise.reject(new OperationError('任务名重复', { code: '1007', requestId: 'req' })) : normal(name, args));
  open(api); await reviewed(); await user.click(screen.getByText(consent));
  await user.click(screen.getByRole('button', { name: '确认创建并启动' }));
  await screen.findByText('任务名重复');
  expect(screen.getByRole('button', { name: '确认创建并启动' }).disabled).toBe(true);
  await user.click(screen.getByText(consent));
  await user.click(screen.getByRole('button', { name: '确认创建并启动' }));
  await screen.findByText('群发任务已创建并确认发送');
  expect(calls(api, 'create_batch_task').map(([, args]) => args.request.idempotencyKey)[0])
    .toBe(calls(api, 'create_batch_task')[1][1].request.idempotencyKey);
});

it('未知创建结果锁定所有编辑、重试和结束按钮', async () => {
  const api = client(); const user = userEvent.setup(); const normal = api.call.getMockImplementation();
  api.call.mockImplementation((name, args) => name === 'create_batch_task'
    ? Promise.reject(new OperationError('结果待确认', { unknown: true })) : normal(name, args));
  open(api); await reviewed(); await user.click(screen.getByText(consent));
  await user.click(screen.getByRole('button', { name: '确认创建并启动' }));
  await screen.findByText('结果待确认');
  expect(screen.queryByLabelText('任务名称')).toBeNull();
  expect(screen.getByLabelText('群发 CSV 名单').disabled).toBe(true);
  for (const label of ['确认创建并启动', '返回修改', '核对群发任务', '结束预览']) {
    expect(screen.getAllByRole('button', { name: label }).every(button => button.disabled)).toBe(true);
  }
  expect(calls(api, 'create_batch_task')).toHaveLength(1);
});

it('移除名单会撤销校验与同意，结束预览只报告摘要', async () => {
  const api = client(); const user = userEvent.setup(); open(api); await reviewed();
  await user.click(screen.getByText(consent));
  await user.click(screen.getByRole('button', { name: '移除' }));
  expect(screen.queryByText(consent)).toBeNull();
  await user.click(screen.getAllByRole('button', { name: '结束预览' })[0]);
  await screen.findByText('已结束群发预览');
  expect(api.report).toHaveBeenCalledWith({ form: 'batch', state: 'abandoned' });
  expect(calls(api, 'create_batch_task')).toHaveLength(0);
  expect(calls(api, 'cancel_batch_task')).toHaveLength(0);
});

it('校验返回错误身份或空有效名单时不可确认，重试由用户触发', async () => {
  const api = client(); const user = userEvent.setup(); const normal = api.call.getMockImplementation();
  api.call.mockImplementation((name, args) => name === 'complete_recipients_upload'
    ? Promise.resolve({ file: 'wrong-file', receipt: args.request, totalCount: 2, dupCount: 2 }) : normal(name, args));
  open(api); await screen.findByText('名单核对结果不完整，请重新核对。');
  expect(screen.queryByText(consent)).toBeNull();
  expect(calls(api, 'complete_recipients_upload')).toHaveLength(1);
  await user.click(screen.getByRole('button', { name: '核对群发任务' }));
  await screen.findByText('名单核对结果不完整，请重新核对。');
  expect(calls(api, 'complete_recipients_upload')).toHaveLength(2);
});

it('定时未填不自动校验，核对时提示选择定时时间', async () => {
  const api = client(); const user = userEvent.setup(); open(api, { scheduled: true });
  await screen.findByRole('button', { name: '点击下载模板' });
  expect(screen.getByText('请选择定时时间，设置完成后将自动校验。')).toBeTruthy();
  expect(calls(api, 'complete_recipients_upload')).toHaveLength(0);
  await user.click(screen.getByRole('button', { name: '核对群发任务' }));
  await screen.findAllByText('请选择定时时间');
  expect(screen.getByLabelText('定时时间').closest('.arco-picker').className).toContain('arco-picker-error');
});

it.each([
  ['过去', -1, '必须晚于当前时间'],
  ['当前', 0, '必须晚于当前时间'],
  ['超过30天', 30 * 86400 + 1, '未来 30 天内'],
])('拒绝%s的定时任务，包括预填绕过日期选择的值', (_name, offset, message) => {
  const now = Date.parse('2026-11-15T10:20:00+08:00');
  vi.spyOn(Date, 'now').mockReturnValue(now);
  const sendAt = new Date(now + offset * 1000 + 8 * 3600000).toISOString().slice(0, 19);
  expect(() => batchPayload({ subAccount: 'g', signature: '签名', name: '任务', scheduled: true, sendAt },
    template, recipients, 'key')).toThrow(message);
});

it('接受30天边界与账号例外时段，按北京时间生成Unix秒', () => {
  const now = Date.parse('2026-11-15T03:20:00+08:00');
  vi.spyOn(Date, 'now').mockReturnValue(now);
  const request = batchPayload({ subAccount: 'g', signature: '签名', name: '任务', scheduled: true,
    sendAt: '2026-12-15T03:20:00' }, template, recipients, 'key');
  expect(request.sendTime).toBe(now / 1000 + 30 * 86400);
});

it.each([
  ['当日', '2026-11-15T10:25:00+08:00', '14', '09', '20', '21'],
  ['30天边界日', '2026-12-15T10:15:00+08:00', '16', '11', '21', '20'],
])('%s日历禁选越界日期，并限制边界小时与分钟', async (_name, initial, day, hour, minute, availableMinute) => {
  vi.spyOn(Date, 'now').mockReturnValue(Date.parse('2026-11-15T10:20:30+08:00'));
  const api = client(); const user = userEvent.setup();
  open(api, { scheduled: true, sendTime: Date.parse(initial) / 1000 }); await reviewed();
  const input = screen.getByLabelText('定时时间');
  await user.click(input);
  const selectTime = screen.getByRole('button', { name: '选择时间' });
  await waitFor(() => expect(window.getComputedStyle(selectTime).pointerEvents).not.toBe('none'));
  const cell = [...document.querySelectorAll('.arco-picker-cell-in-view')].find(item => item.textContent === day);
  expect(cell.className).toContain('arco-picker-cell-disabled');
  await user.click(cell);
  expect(input.value).toBe(initial.slice(0, 16).replace('T', ' '));
  await user.click(selectTime);
  const lists = document.querySelectorAll('.arco-timepicker-list');
  expect(lists).toHaveLength(2);
  expect(within(lists[0]).getByText(hour).closest('li').className).toContain('arco-timepicker-cell-disabled');
  expect(within(lists[1]).getByText(minute).closest('li').className).toContain('arco-timepicker-cell-disabled');
  const available = within(lists[1]).getByText(availableMinute);
  expect(available.closest('li').className).not.toContain('arco-timepicker-cell-disabled');
  await user.click(available);
  await user.click(screen.getByRole('button', { name: '确定' }));
  await reviewed();
  expect(input.value).toBe(initial.slice(0, 14).replace('T', ' ') + availableMinute);
});

it('核对后定时时间过期，最终提交仍阻止创建并撤销同意', async () => {
  const api = client(); const user = userEvent.setup();
  const sendTime = Math.floor(Date.now() / 1000) + 120;
  open(api, { scheduled: true, sendTime }); await reviewed();
  await user.click(screen.getByText(consent));
  vi.spyOn(Date, 'now').mockReturnValue(sendTime * 1000);
  await user.click(screen.getByRole('button', { name: '确认创建并启动' }));
  await screen.findByText('定时时间必须晚于当前时间。');
  expect(calls(api, 'create_batch_task')).toHaveLength(0);
  expect(screen.getByRole('button', { name: '确认创建并启动' }).disabled).toBe(true);
});

it('选框隐藏加载统计，仍能分页载入更多消息组', async () => {
  const api = client(); const user = userEvent.setup(); const normal = api.query.getMockImplementation();
  api.query.mockImplementation((action, params) => action === 'GetSubAccountListForAgent'
    ? Promise.resolve({ list: [{ subAccountId: params.pageIndex === 2 ? 'g2' : 'g',
      subAccountName: params.pageIndex === 2 ? '第二组' : '通知组' }], total: 2 }) : normal(action, params));
  await openEditable(api);
  expect(screen.queryByText(/已加载/)).toBeNull();
  await user.click(screen.getByRole('button', { name: '加载更多' }));
  await waitFor(() => expect(screen.queryByRole('button', { name: '加载更多' })).toBeNull());
  expect(api.query).toHaveBeenCalledWith('GetSubAccountListForAgent', { pageIndex: 2, pageSize: 100 });
  await user.click(screen.getByLabelText('消息组'));
  expect(await screen.findByRole('option', { name: '第二组' })).toBeTruthy();
});

it('试发尚无发送记录时提示稍后刷新，不误报失败或再次发送', async () => {
  const api = client(); const user = userEvent.setup(); const normal = api.call.getMockImplementation();
  api.call.mockImplementation((name, args) => {
    if (name === 'send_batch_test_sms') return Promise.resolve({ messageId: 'test-id', requestedAt: Math.floor(Date.now() / 1000) });
    if (name === 'list_send_logs') return Promise.resolve({ List: [{ MessageId: 'another-id', Status: 2 }], Total: 1 });
    return normal(name, args);
  });
  open(api); await reviewed();
  await user.type(screen.getByLabelText('测试手机号'), '13800000000');
  await user.type(screen.getByLabelText('time'), '明天上午');
  await user.click(screen.getByRole('button', { name: '发送测试短信' }));
  await user.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await user.click(screen.getByRole('button', { name: '确认发送测试短信' }));
  await screen.findByText('暂未查询到发送结果，可稍后刷新。');
  await user.click(screen.getByRole('button', { name: '刷新发送结果' }));
  expect(calls(api, 'send_batch_test_sms')).toHaveLength(1);
  expect(calls(api, 'list_send_logs')).toHaveLength(2);
  expect(screen.queryByText('发送失败')).toBeNull();
});

it('特殊通知自动校验原始正文，群发专用模板不显示试发', async () => {
  const api = client(); const normal = api.query.getMockImplementation();
  api.query.mockImplementation(action => action === 'ListBatchTemplatesForAgent'
    ? Promise.resolve({ List: [{ ...template, BatchOnly: true, TaskFields: [{ Name: 'content', Required: true }] }], Total: 1 })
    : normal(action));
  open(api, { content: ' 保留原始正文 ' }); await reviewed();
  expect(screen.queryByLabelText('测试手机号')).toBeNull();
  expect(screen.queryByLabelText('任务正文')).toBeNull();
  expect(within(screen.getByRole('region', { name: '任务信息' })).getByText('保留原始正文').textContent)
    .toBe(' 保留原始正文 ');
  expect(api.query).toHaveBeenCalledWith('ValidateBatchTaskContentForAgent', {
    subAccount: 'g', signature: '签名', templateId: 't', content: ' 保留原始正文 ',
  });
});

it('必填任务正文未预填时仍可补全，填写后不突然变成只读', async () => {
  const api = client(); const normal = api.query.getMockImplementation();
  api.query.mockImplementation(action => action === 'ListBatchTemplatesForAgent'
    ? Promise.resolve({ List: [{ ...template, TaskFields: [{ Name: 'content', Required: true }] }], Total: 1 })
    : normal(action));
  open(api);
  await screen.findByRole('button', { name: '点击下载模板' });
  await waitFor(() => expect(screen.getByLabelText('任务正文').disabled).toBe(false));
  fireEvent.change(screen.getByLabelText('任务正文'), { target: { value: ' 补全正文 ' } });
  await reviewed();
  expect(screen.getByLabelText('任务正文').value).toBe(' 补全正文 ');
  expect(screen.getByLabelText('任务名称').disabled).toBe(false);
  expect(api.query).toHaveBeenCalledWith('ValidateBatchTaskContentForAgent', {
    subAccount: 'g', signature: '签名', templateId: 't', content: ' 补全正文 ',
  });
});

it.each(['GetSubAccountListForAgent', 'ListSignaturesForAgent', 'ListBatchTemplatesForAgent'])(
  '完整预填的资源在%s核实失败时保留填写入口，不能创建任务', async unavailable => {
    const api = client(); const normal = api.query.getMockImplementation();
    api.query.mockImplementation((action, args) => action === unavailable
      ? Promise.resolve(action === 'GetSubAccountListForAgent' ? { list: [], total: 0 } : { List: [], Total: 0 })
      : normal(action, args));
    open(api);
    await screen.findByText(/预填消息组当前不可用|预填签名在所选消息组中不可用|模板配置缺失/);
    await waitFor(() => expect(screen.getByLabelText('任务名称').disabled).toBe(false));
    expect(screen.getByLabelText('任务名称').value).toBe('预约通知');
    expect(screen.getByLabelText('消息组')).toBeTruthy();
    expect(screen.getByRole('button', { name: '确认创建并启动' }).disabled).toBe(true);
    expect(calls(api, 'complete_recipients_upload')).toHaveLength(0);
    expect(calls(api, 'create_batch_task')).toHaveLength(0);
  });


it('确认发送已受理但详情仍为旧状态时，不要求再次核对或启动', async () => {
  const api = client(); const user = userEvent.setup(); const normal = api.call.getMockImplementation();
  api.call.mockImplementation((name, args) => name === 'query_batch_tasks'
    ? Promise.resolve({ taskId: 'task', subAccount: 'g', templateId: 't', signature: '签名', status: 2 })
    : normal(name, args));
  open(api); await reviewed(); await user.click(screen.getByText(consent));
  await user.click(screen.getByRole('button', { name: '确认创建并启动' }));
  await screen.findByText('群发任务已创建并确认发送');
  await waitFor(() => expect(screen.getByRole('button', { name: '刷新任务状态' }).disabled).toBe(false));
  expect(screen.getByText('确认发送已受理，等待状态更新')).toBeTruthy();
  expect(screen.queryByText('待确认发送')).toBeNull();
  expect(screen.queryByRole('button', { name: '核对并启动' })).toBeNull();
  expect(screen.queryByRole('button', { name: '重试确认发送' })).toBeNull();
  await user.click(screen.getByRole('button', { name: '刷新任务状态' }));
  await waitFor(() => expect(calls(api, 'query_batch_tasks')).toHaveLength(3));
  expect(calls(api, 'create_batch_task')).toHaveLength(1);
  expect(calls(api, 'start_batch_task')).toHaveLength(1);
});

it('确认发送成功后详情查询失败仍保留受理结果，刷新不会重复创建或启动', async () => {
  const api = client(); const user = userEvent.setup(); const normal = api.call.getMockImplementation();
  let reads = 0;
  api.call.mockImplementation((name, args) => {
    if (name === 'query_batch_tasks' && ++reads === 2) {
      return Promise.reject(new OperationError('任务状态查询暂不可用', { code: 'query_failed' }));
    }
    return normal(name, args);
  });
  open(api); await reviewed(); await user.click(screen.getByText(consent));
  await user.click(screen.getByRole('button', { name: '确认创建并启动' }));
  await screen.findByText('任务状态查询暂不可用');
  expect(screen.getByText('群发任务已创建并确认发送')).toBeTruthy();
  expect(screen.queryByRole('button', { name: '核对并启动' })).toBeNull();
  expect(screen.queryByRole('button', { name: '重试确认发送' })).toBeNull();
  expect(screen.queryByText('待确认发送')).toBeNull();
  await user.click(screen.getByRole('button', { name: '刷新任务状态' }));
  await screen.findByText('任务已启动，送达结果请查询回执');
  expect(screen.queryByText('任务状态查询暂不可用')).toBeNull();
  expect(calls(api, 'create_batch_task')).toHaveLength(1);
  expect(calls(api, 'start_batch_task')).toHaveLength(1);
});


it('创建回查显示任务已经启动时，不重复确认发送', async () => {
  const api = client(); const user = userEvent.setup(); const normal = api.call.getMockImplementation();
  api.call.mockImplementation((name, args) => name === 'query_batch_tasks'
    ? Promise.resolve({ taskId: 'task', subAccount: 'g', templateId: 't', signature: '签名', status: 3 })
    : normal(name, args));
  open(api); await reviewed(); await user.click(screen.getByText(consent));
  await user.click(screen.getByRole('button', { name: '确认创建并启动' }));
  await screen.findByText('群发任务已创建并确认发送');
  expect(screen.queryByRole('button', { name: '核对并启动' })).toBeNull();
  expect(screen.queryByRole('button', { name: '重试确认发送' })).toBeNull();
  expect(calls(api, 'create_batch_task')).toHaveLength(1);
  expect(calls(api, 'start_batch_task')).toHaveLength(0);
  expect(api.report).toHaveBeenCalledWith({
    form: 'batch', state: 'operation_already_applied', taskId: 'task', operation: 'start',
  });
});

it('创建成功但确认发送被拒绝时保留原始错误，明确重试只启动同一任务', async () => {
  const api = client(); const user = userEvent.setup(); const normal = api.call.getMockImplementation();
  let starts = 0;
  api.call.mockImplementation((name, args) => {
    if (name === 'start_batch_task' && ++starts === 1) {
      return Promise.reject(new OperationError('确认发送被拒绝', {
        code: '1999', httpStatus: 200, requestId: 'start-request',
      }));
    }
    return normal(name, args);
  });
  open(api); await reviewed(); await user.click(screen.getByText(consent));
  await user.click(screen.getByRole('button', { name: '确认创建并启动' }));
  await screen.findByText('确认发送被拒绝');
  expect(screen.getByText('群发任务已创建')).toBeTruthy();
  expect(screen.getByText('排障编号：start-request')).toBeTruthy();
  expect(screen.queryByText('群发任务已创建并确认发送')).toBeNull();
  expect(calls(api, 'create_batch_task')).toHaveLength(1);
  expect(calls(api, 'start_batch_task')).toHaveLength(1);
  await user.click(screen.getByRole('button', { name: '重试确认发送' }));
  await user.click(screen.getByText('我已核对以上信息，同意提交本次操作'));
  await user.click(screen.getByRole('button', { name: '确认启动群发' }));
  await screen.findByText('群发任务已创建并确认发送');
  expect(calls(api, 'create_batch_task')).toHaveLength(1);
  expect(calls(api, 'start_batch_task')).toHaveLength(2);
  expect(calls(api, 'start_batch_task').every(([, args]) =>
    args.sub_account === 'g' && args.task_id === 'task')).toBe(true);
});


it('旧响应误报失败后刷新查到已启动，恢复组合成功结果且不重复创建启动', async () => {
  const api = client(); const normal = api.call.getMockImplementation(); let reads = 0;
  api.call.mockImplementation((name, args) => {
    if (name === 'query_batch_tasks') return Promise.resolve({
      taskId: 'task', subAccount: 'g', templateId: 't', signature: '签名', status: ++reads === 1 ? 2 : 3,
    });
    if (name === 'start_batch_task') return Promise.reject(new OperationError('未收到可确认的短信 API 响应', {
      code: 'invalid_response', httpStatus: 200, requestId: 'start-request',
    }));
    return normal(name, args);
  });
  const user = userEvent.setup(); open(api); await reviewed();
  await user.click(screen.getByText(consent));
  await user.click(screen.getByRole('button', { name: '确认创建并启动' }));
  await screen.findByText('未收到可确认的短信 API 响应');
  await user.click(screen.getByRole('button', { name: '刷新任务状态' }));
  await screen.findByText('群发任务已创建并确认发送');
  expect(screen.queryByText('未收到可确认的短信 API 响应')).toBeNull();
  expect(screen.queryByText('待确认发送')).toBeNull();
  expect(screen.queryByRole('button', { name: '核对并启动' })).toBeNull();
  expect(screen.queryByRole('button', { name: '重试确认发送' })).toBeNull();
  expect(calls(api, 'create_batch_task')).toHaveLength(1);
  expect(calls(api, 'start_batch_task')).toHaveLength(1);
});
