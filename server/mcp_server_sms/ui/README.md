# 短信 MCP Apps

四种表单由同一个自包含 HTML 资源承载。使用官方 MCP Apps SDK 的 AppBridge 调用本服务工具，不依赖 localhost HTTP、浏览器存储或客户端凭据。

`src/styles/{qualification,signature,traffic,batch}.css` 原样复制自 byted-sms-sender 1.4.6 对应的 `*_wizard.css`（参考仓库提交 e3d7e1f997671590cb1c26d1977f0dcd19abcba2）。布局和组件沿用 React 18.2.0、Arco 2.66.15；窄屏、对话卡片和主题覆盖在 `host.css` 中维护。这里的构建和运行都不读取或修改 Skill。

前端开发使用 Node.js 22.12 或以上版本；部署预构建的 Python wheel 不需要 Node.js。

```bash
npm ci
npm test
npm run build
```

构建输出 `../src/mcp_server_sms/static/forms.html`，由 Python 包随 wheel 分发。业务数据不能写入 HTML。修改前端后需重新构建再打 Python 包。

`npm run dev` 后打开 `/dev/preview.html` 可预览四个表单、窄屏和深色模式；这里使用官方 AppBridge 与跨源双 iframe 沙箱、模拟业务数据，不连接线上。`dev/sandbox.ts` 复用官方 ext-apps 的 basic-host 沙箱。生产构建不包含这些预览代码。构建器生成的 `THIRD_PARTY_LICENSES.md` 随 Python 包分发。
