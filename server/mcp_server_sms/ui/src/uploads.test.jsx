import React from 'react';
import { webcrypto } from 'node:crypto';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { SmsFormClient, MAX_UPLOAD_BYTES } from './client.js';
import { QualificationForm } from './qualification.jsx';
import config from '../../src/mcp_server_sms/form_config.json';

const signature = 'a'.repeat(64);
const uri = 'bucket/proof.png';
const envelope = data => ({ structuredContent: { success: true, result: null },
  _meta: { 'sms/form': { success: true, result: data } } });
const selected = (bytes, name = 'proof.png') => ({ name, size: bytes.length, arrayBuffer: async () => bytes.buffer });
beforeEach(() => { vi.stubGlobal('crypto', webcrypto); vi.spyOn(console, 'info').mockImplementation(() => {}); });
afterEach(() => { cleanup(); vi.restoreAllMocks(); vi.unstubAllGlobals(); });

function fixture({ recipients = false, failPrepare = false, failComplete = false, url, materialUri = uri } = {}) {
  const app = { sendLog: vi.fn().mockResolvedValue(undefined), callServerTool: vi.fn(async ({ name, arguments: args }) => {
    // 宿主的实际限制针对整个 arguments，文件不享有例外。
    if (JSON.stringify(args).length > 32000) throw Object.assign(new Error('fixture limit'), { code: -32602 });
    if (name === 'get_qualification_requirements') return envelope(Object.fromEntries(
      ['isOnlyTwoElement', 'isSkipOtherUse', 'needOtherUseCheck', 'operatorThreeElement',
        'needOperatorImage', 'needOperatorMobile', 'responsibleThreeElement', 'needResponsibleImage',
        'needResponsibleMobile', 'needBusinessCertificateImage'].map(key => [key, false]),
    ));
    if (name === 'get_account_information') return envelope({ userType: 'enterprise', businessName: '测试企业' });
    if (name === 'recognize_qualification_document') return envelope({
      businessCertificateName: '测试企业', unifiedSocialCreditIdentifier: 'fixture-credit',
      legalPersonName: '测试法人', businessCertificateValidityPeriodStart: '2020-01-01',
      businessCertificateValidityPeriodEnd: '2099-12-31',
    });
    if (name.startsWith('prepare_')) {
      if (failPrepare) throw Object.assign(new Error('fixture-private-error'), { code: -32603 });
      return envelope({
        upload: { method: 'PUT',
          url: url ?? (recipients ? 'https://bucket.tos-cn-beijing.volces.com/fixture.csv?signature=private'
            : 'https://' + config.materialUpload.uploadHosts[0] + '/' + materialUri),
          headers: recipients ? {} : { Authorization: 'fixture-file-auth', 'Content-CRC32': args.request.crc32 } },
        confirmation: { signature, context: recipients
          ? { ...args.request, file: 'fixture.csv', expires_at: 9999999999 }
          : { name: args.request.name, suffix: 'png', uri: materialUri, session_key: 'fixture-session', expires_at: 9999999999 } },
      });
    }
    if (name.startsWith('complete_')) {
      if (failComplete) throw new Error('fixture-private-error');
      return envelope(recipients
        ? { name: args.request.context.name, file: args.request.context.file, totalCount: 6000, dupCount: 5999, receipt: args.request }
        : { name: args.request.context.name, fileContent: args.request.context.uri, fileSuffix: 'png' });
    }
    throw new Error('unexpected tool');
  }) };
  const fetch = vi.fn().mockResolvedValue({ ok: true, status: 200, json: async () => ({ success: 0, error: null, payload: {} }) });
  vi.stubGlobal('fetch', fetch);
  return { app, fetch, client: new SmsFormClient(app) };
}

it.each([7314599, MAX_UPLOAD_BYTES])('材料 %i 字节通过严格宿主限制，HTTP 字节保持原样', async size => {
  const bytes = new Uint8Array(size).fill(97);
  bytes.set([137, 80, 78, 71, 13, 10, 26, 10]);
  const { app, fetch, client } = fixture();
  const result = await client.upload(selected(bytes), { kind: 'material', category: 'business' });
  expect(result.fileContent).toBe(uri);
  expect(result.localFile).toBeInstanceOf(Blob);
  expect(result.localFile.size).toBe(size);
  expect(app.callServerTool.mock.calls.map(([c]) => c.name)).toEqual(['prepare_material_upload', 'complete_material_upload']);
  for (const [call] of app.callServerTool.mock.calls) {
    expect(JSON.stringify(call.arguments).length).toBeLessThan(32000);
    expect(call.arguments.request.data).toBeUndefined();
  }
  expect(Buffer.from(fetch.mock.calls[0][1].body).equals(Buffer.from(bytes))).toBe(true);
  expect(fetch.mock.calls[0][0]).toBe('https://' + config.materialUpload.uploadHosts[0] + '/' + uri);
  expect(fetch.mock.calls[0][1]).toMatchObject({ method: 'PUT', credentials: 'omit', redirect: 'error',
    headers: { 'Content-CRC32': app.callServerTool.mock.calls[0][0].arguments.request.crc32 } });
  const logs = JSON.stringify(app.sendLog.mock.calls);
  expect(logs).toContain('start'); expect(logs).toContain('end');
  expect(logs).not.toContain('fixture-file-auth'); expect(logs).not.toContain('proof.png');
});
it('上传准备的短信后端错误原样展示，不追加或替换错误文案', async () => {
  const { app, client, fetch } = fixture();
  const message = ' 原始上传授权错误\n请联系账号管理员 ';
  const backend = { ResponseMetadata: { RequestId: 'upload-request', Error: { Code: 'AccessDenied', Message: message } } };
  app.callServerTool.mockResolvedValue({ isError: true, structuredContent: {
    success: false, request_id: 'upload-request', error: { code: 'AccessDenied', message, http_status: 403, backend_response: backend },
  } });
  await expect(client.upload(selected(new Uint8Array([1, 2, 3])), { kind: 'material', category: 'business' }))
    .rejects.toMatchObject({ message, code: 'AccessDenied', requestId: 'upload-request', backendResponse: backend, unknown: false });
  expect(fetch).not.toHaveBeenCalled();
  expect(app.callServerTool).toHaveBeenCalledTimes(1);
});
it('宿主预填文件解码后直传，不重新经过 MCP 参数', async () => {
  const { app, fetch, client } = fixture();
  await client.upload({ name: 'proof.png', data: 'Zml4dHVyZQ==' }, { kind: 'material', category: 'business' });
  expect(Array.from(fetch.mock.calls[0][1].body)).toEqual(Array.from(new TextEncoder().encode('fixture')));
  expect(JSON.stringify(app.callServerTool.mock.calls)).not.toContain('Zml4dHVyZQ==');
});
it('大 CSV 直传后保留签名引用，在任务核对时再统一校验', async () => {
  const bytes = new TextEncoder().encode('phone,url\n' + '13800000000,https://example.com/CaseSensitive\n'.repeat(6000));
  const { app, fetch, client } = fixture({ recipients: true });
  const result = await client.upload(selected(bytes, 'list.csv'), { kind: 'recipients', sub_account: 'group', template_id: 'template' });
  expect(result.totalCount).toBeUndefined(); expect(result.receipt.context.sha256).toHaveLength(64);
  expect(Buffer.from(fetch.mock.calls[0][1].body).equals(Buffer.from(bytes))).toBe(true);
  expect(fetch.mock.calls[0][1].method).toBe('PUT');
  expect(app.callServerTool.mock.calls.map(([c]) => c.name)).toEqual(['prepare_recipients_upload']);
  expect(JSON.stringify(app.callServerTool.mock.calls)).not.toContain('13800000000');
});
it.each([0, MAX_UPLOAD_BYTES + 1])('拒绝 %i 字节文件，不请求上传权限', async size => {
  const { app, fetch, client } = fixture();
  await expect(client.upload({ name: 'proof.png', size }, { kind: 'material', category: 'business' }))
    .rejects.toMatchObject({ code: 'invalid_file_size', unknown: false });
  expect(app.callServerTool).not.toHaveBeenCalled(); expect(fetch).not.toHaveBeenCalled();
});
it.each([
  'http://127.0.0.1/bucket/proof.png', 'https://evil.example/bucket/proof.png',
  'https://evil.volces.com.example/bucket/proof.png', 'https://tos-d-ct-hl.snssdk.com/bucket/proof.png',
  `https://${config.materialUpload.uploadHosts[0]}/bucket/other.png`,
  `https://${config.materialUpload.uploadHosts[0]}/upload/v1/${uri}`,
  `https://${config.materialUpload.uploadHosts[0]}/${uri}?unexpected=value`,
])('拒绝非固定入口或与授权对象不一致的地址 %s', async url => {
  const { app, fetch, client } = fixture({ url });
  await expect(client.upload(selected(new Uint8Array([1])), { kind: 'material', category: 'business' }))
    .rejects.toMatchObject({ code: 'invalid_upload_url', unknown: false });
  expect(fetch).not.toHaveBeenCalled(); expect(app.callServerTool).toHaveBeenCalledTimes(1);
});
it.each(config.materialUpload.uploadHosts)('固定入口 %s 支持包含空格、中文和特殊字符的对象路径', async host => {
  const materialUri = 'bucket/sub dir/名 #?%.png';
  const url = `https://${host}/bucket/sub%20dir/%E5%90%8D%20%23%3F%25.png`;
  const { client, fetch } = fixture({ url, materialUri });
  const result = await client.upload(selected(new Uint8Array([1, 2, 3])), { kind: 'material', category: 'business' });
  expect(fetch.mock.calls[0][0]).toBe(url);
  expect(result.fileContent).toBe(materialUri);
});
it.each(['prepare', 'transfer', 'confirm'])('%s 失败可以重选，业务提交连接异常保留原文', async stage => {
  const { app, fetch, client } = fixture({ failPrepare: stage === 'prepare', failComplete: stage === 'confirm' });
  if (stage === 'transfer') fetch.mockRejectedValue(new TypeError('fixture-private-error'));
  await expect(client.upload(selected(new Uint8Array([1, 2, 3])), { kind: 'material', category: 'business' }))
    .rejects.toMatchObject({ unknown: false, message: 'fixture-private-error' });
  expect(fetch).toHaveBeenCalledTimes(stage === 'prepare' ? 0 : 1);
  expect(app.callServerTool).toHaveBeenCalledTimes(stage === 'confirm' ? 2 : 1);
  app.callServerTool.mockRejectedValue(new Error('fixture-private-error'));
  await expect(client.call('submit_qualification', {}, { write: true })).rejects.toMatchObject({ message: 'fixture-private-error', unknown: false });
});
it('HTTP 和业务上传错误均停止，不调用完成确认', async () => {
  const { app, fetch, client } = fixture();
  fetch.mockResolvedValueOnce({ ok: false, status: 403, text: async () => 'original upload rejection', headers: new Headers({ 'x-tos-request-id': 'tos-request' }) });
  await expect(client.upload(selected(new Uint8Array([1])), { kind: 'material', category: 'business' }))
    .rejects.toMatchObject({ code: 'upload_http_error', message: 'original upload rejection', httpStatus: 403,
      backendResponse: 'original upload rejection', requestId: 'tos-request' });
  fetch.mockResolvedValueOnce({ ok: true, status: 200, json: async () => ({ code: 5000 }) });
  await expect(client.upload(selected(new Uint8Array([1])), { kind: 'material', category: 'business' }))
    .rejects.toMatchObject({ code: 'upload_not_confirmed' });
  expect(app.callServerTool.mock.calls.every(([c]) => c.name === 'prepare_material_upload')).toBe(true);
});
it('固定入口返回业务错误时保留错误原文、错误码和完整响应', async () => {
  const { app, fetch, client } = fixture();
  const body = { success: 1, error: { code: 'InvalidCRC', message: ' 原始校验失败\n请核对文件 ' }, payload: { detail: 'original' } };
  fetch.mockResolvedValue({ ok: true, status: 200, json: async () => body, headers: new Headers({ 'x-tt-logid': 'image-request' }) });
  await expect(client.upload(selected(new Uint8Array([1, 2, 3])), { kind: 'material', category: 'business' }))
    .rejects.toMatchObject({ message: body.error.message, code: 'InvalidCRC', backendResponse: body, requestId: 'image-request', httpStatus: 200, unknown: false });
  expect(app.callServerTool).toHaveBeenCalledTimes(1);
});
it('资质表单上传失败保留输入并允许重新选择，重选成功显示附件', async () => {
  const { app, fetch, client } = fixture();
  fetch.mockRejectedValueOnce(new TypeError('fixture network error'));
  render(<QualificationForm client={client} prefill={{ materialName: '保留的资质名称' }} />);
  await screen.findByRole('heading', { name: '基础信息' });
  fireEvent.click(screen.getByRole('button', { name: '下一步' }));
  const input = await screen.findByLabelText('营业证件附件');
  fireEvent.change(input, { target: { files: [selected(new Uint8Array([1, 2, 3]))] } });
  await screen.findByText('fixture network error');
  fireEvent.click(screen.getByRole('button', { name: '上一步' }));
  expect((await screen.findByLabelText('资质名称（选填）')).value).toBe('保留的资质名称');
  fireEvent.click(screen.getByRole('button', { name: '下一步' }));
  const retryInput = await screen.findByLabelText('营业证件附件');
  fireEvent.change(retryInput, { target: { files: [selected(new Uint8Array([1, 2, 3]))] } });
  await screen.findByText('proof.png');
  await waitFor(() => expect(screen.queryByText('fixture network error')).toBeNull());
  await screen.findByText('识别完成，请核对信息。');
  expect((await screen.findByRole('img', { name: '营业证件附件' })).getAttribute('src')).toMatch(/^blob:/);
  fetch.mockRejectedValueOnce(new TypeError('replacement upload failed'));
  fireEvent.change(retryInput, { target: { files: [selected(new Uint8Array([4, 5, 6]), 'replacement.png')] } });
  await screen.findByText('replacement upload failed');
  expect(screen.getByText('replacement.png')).toBeTruthy();
  expect(screen.getByRole('img', { name: '营业证件附件' }).getAttribute('src')).toMatch(/^blob:/);
  expect(app.callServerTool.mock.calls.some(([c]) => c.name === 'submit_qualification')).toBe(false);
  expect(app.callServerTool.mock.calls.filter(([c]) => c.name === 'recognize_qualification_document')).toHaveLength(1);
});
