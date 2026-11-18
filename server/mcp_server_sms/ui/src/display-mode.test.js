import { expect, it, vi } from 'vitest';
import { formDisplayPreference } from './display-mode.js';

const state = { ready: true, supported: true,
  toolResult: { structuredContent: { form: 'qualification', mode: 'input' } } };
function fixture(context = { displayMode: 'inline', availableDisplayModes: ['inline', 'fullscreen'] }) {
  const app = { getHostContext: vi.fn(() => context), requestDisplayMode: vi.fn().mockResolvedValue({ mode: 'fullscreen' }) };
  return { app, prefer: formDisplayPreference(app) };
}

it.each(['qualification', 'signature', 'traffic', 'batch', 'service', 'template'])(
  '%s 输入表单打开且 MCP Apps 握手完成后请求展开',
  async form => {
    const { app, prefer } = fixture();
    const formState = { ...state, toolResult: { structuredContent: { form, mode: 'input' } } };
    await prefer({ ...formState, ready: false });
    expect(app.requestDisplayMode).not.toHaveBeenCalled();
    await prefer(formState);
    expect(app.requestDisplayMode).toHaveBeenCalledExactlyOnceWith({ mode: 'fullscreen' });
  },
);

it('先握手后收到工具结果也能展开，重绘和用户收回面板不会再次请求', async () => {
  const { app, prefer } = fixture();
  await prefer({ ready: true, supported: true });
  await prefer(state);
  await prefer(state);
  expect(app.requestDisplayMode).toHaveBeenCalledTimes(1);
});

it.each([
  { displayMode: 'inline', availableDisplayModes: ['inline'] },
  { displayMode: 'fullscreen', availableDisplayModes: ['inline', 'fullscreen'] },
  undefined,
])('不支持展开或已经展开时保持宿主选择', async context => {
  const { app, prefer } = fixture();
  app.getHostContext.mockReturnValue(context);
  await prefer(state);
  expect(app.requestDisplayMode).not.toHaveBeenCalled();
});

it('宿主拒绝展示请求时保留表单，不反复尝试', async () => {
  const { app, prefer } = fixture();
  app.requestDisplayMode.mockRejectedValue(new Error('Host rejected display change'));
  await expect(prefer(state)).resolves.toBeUndefined();
  await prefer(state);
  expect(app.requestDisplayMode).toHaveBeenCalledTimes(1);
});

it('未知表单、历史收据及不支持 MCP Apps 的客户端不自动展开', async () => {
  const { app, prefer } = fixture();
  await prefer({ ...state, supported: false });
  await prefer({ ...state, toolResult: { structuredContent: { form: 'qualification', mode: 'result' } } });
  await prefer({ ...state, toolResult: { structuredContent: { form: 'unknown', mode: 'input' } } });
  expect(app.requestDisplayMode).not.toHaveBeenCalled();
});
