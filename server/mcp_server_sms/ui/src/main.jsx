import React from 'react';
import { createRoot } from 'react-dom/client';
import { App, applyDocumentTheme, applyHostStyleVariables, applyHostFonts } from '@modelcontextprotocol/ext-apps';
import '@arco-design/web-react/dist/css/arco.css';
import './styles/qualification.css';
import './styles/signature.css';
import './styles/traffic.css';
import './styles/batch.css';
import './host.css';
import { SmsApp } from './app.jsx';
import { SmsFormClient } from './client.js';

const app = new App(
  { name: '火山引擎短信表单', version: '0.2.0' },
  { availableDisplayModes: ['inline', 'fullscreen'] },
  { autoResize: true, strict: true, webMcpBridge: false },
);
const client = new SmsFormClient(app);
const root = createRoot(document.getElementById('root'));
let state = { ready: false, supported: false, toolResult: null };
let disposed = false;
function render(update) {
  if (disposed) return;
  state = { ...state, ...update };
  root.render(<SmsApp client={client} {...state} />);
}
function hostContext(context) {
  if (context.theme) {
    applyDocumentTheme(context.theme);
    document.body.setAttribute('arco-theme', context.theme === 'dark' ? 'dark' : 'light');
  }
  if (context.styles?.variables) applyHostStyleVariables(context.styles.variables);
  if (context.styles?.css?.fonts) applyHostFonts(context.styles.css.fonts);
  if (context.safeAreaInsets) {
    for (const side of ['top', 'right', 'bottom', 'left']) document.body.style['padding' + side[0].toUpperCase() + side.slice(1)] = `${context.safeAreaInsets[side]}px`;
  }
}

// 监听先于 connect，避免遗漏宿主投递的初始结果；不读取父页面或浏览器存储。
app.ontoolresult = result => render({ toolResult: result });
app.onhostcontextchanged = hostContext;
app.ontoolcancelled = () => render({ error: '本次表单已取消。若有操作已经提交，请先查询其状态。' });
app.onerror = () => render({ error: '表单连接中断。已提交操作的结果需要查询核对，请勿重复提交。' });
app.onteardown = async () => { disposed = true; client.dispose(); root.unmount(); return {}; };
render({});
app.connect().then(() => {
  const context = app.getHostContext();
  if (context) hostContext(context);
  render({ ready: true, supported: Boolean(app.getHostCapabilities()?.serverTools) });
}).catch(() => render({ error: '无法建立表单连接，请使用支持 MCP Apps 的客户端重新打开。' }));
