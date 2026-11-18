import { defineConfig } from 'vite';
import { viteSingleFile } from 'vite-plugin-singlefile';
import { createHash } from 'node:crypto';
import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const uiRoot = path.dirname(fileURLToPath(import.meta.url));
const packageRoot = path.dirname(uiRoot);

export default defineConfig({
  plugins: [viteSingleFile(), {
    name: 'sms-source-manifest',
    enforce: 'post',
    generateBundle: { order: 'post', handler(_options, bundle) {
      const inputs = new Set([
        path.join(uiRoot, 'forms.html'), path.join(uiRoot, 'package.json'),
        path.join(uiRoot, 'package-lock.json'), path.join(uiRoot, 'vite.config.js'),
      ]);
      for (const id of this.getModuleIds()) {
        if ((id.startsWith(path.join(uiRoot, 'src') + path.sep)
          || id === path.join(packageRoot, 'src/mcp_server_sms/form_config.json')) && existsSync(id)) inputs.add(id);
      }
      const sources = Object.fromEntries([...inputs].sort().map(file => [
        path.relative(packageRoot, file), createHash('sha256').update(readFileSync(file)).digest('hex'),
      ]));
      // 生成许可证文档时统一 Markdown 行尾，不改写许可正文，避免依赖包 CRLF/尾空格进入产物。
      const license = bundle['THIRD_PARTY_LICENSES.md'];
      if (license?.type === 'asset' && typeof license.source === 'string') {
        license.source = license.source.replace(/\r\n/g, '\n').replace(/[ \t]+$/gm, '');
      }
      const html = bundle['forms.html'];
      if (!html || html.type !== 'asset') throw new Error('Missing self-contained forms.html');
      this.emitFile({ type: 'asset', fileName: 'build-manifest.json', source: JSON.stringify({
        sources, htmlSha256: createHash('sha256').update(html.source).digest('hex'),
      }, null, 2) + '\n' });
    } },
  }, {
    name: 'local-sandbox-csp',
    configureServer(server) {
      server.middlewares.use('/dev/sandbox.html', (_request, response, next) => {
        response.setHeader('Content-Security-Policy', "default-src 'none'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'none'; frame-src 'self'; object-src 'none'");
        next();
      });
    },
  }],
  server: { hmr: false, fs: { allow: ['..'] } },
  build: {
    outDir: '../src/mcp_server_sms/static',
    emptyOutDir: true,
    license: { fileName: 'THIRD_PARTY_LICENSES.md' },
    rollupOptions: { input: 'forms.html' },
  },
  test: { environment: 'jsdom', setupFiles: ['./src/test-setup.js'] },
});
