import React, { useState } from 'react';
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Files } from './files.jsx';
import { materialPreview } from './client.js';

beforeEach(() => { URL.createObjectURL.mockClear(); URL.revokeObjectURL.mockClear(); });
afterEach(cleanup);
const image = name => ({ name, localFile: new Blob(['image fixture'], { type: 'image/png' }), fileContent: `materials/${name}`, fileSuffix: 'png' });

it('图片选中后立即回显，上传完成沿用本地内容，移除后释放预览', async () => {
  let finish;
  const upload = vi.fn(() => new Promise(resolve => { finish = resolve; }));
  function Picker() {
    const [files, setFiles] = useState([]);
    return <Files label="营业证件" accept=".png" value={files} onRemove={() => setFiles([])} onSelect={async selected => {
      await upload(selected[0]);
      setFiles([{ name: selected[0].name, localFile: selected[0], fileContent: 'material/uploaded', fileSuffix: 'png' }]);
    }} />;
  }
  render(<Picker />);
  const file = new File(['image fixture'], '营业执照.png', { type: 'image/png' });
  fireEvent.change(screen.getByLabelText('营业证件'), { target: { files: [file] } });
  const first = await screen.findByRole('img', { name: '营业证件' });
  expect(first.getAttribute('src')).toMatch(/^blob:fixture-image-/);
  expect(upload).toHaveBeenCalledWith(file);
  const pendingUrl = first.getAttribute('src');
  finish();
  await waitFor(() => expect(URL.revokeObjectURL).toHaveBeenCalledWith(pendingUrl));
  expect(screen.getByRole('img', { name: '营业证件' }).getAttribute('src')).toMatch(/^blob:/);
  expect(URL.revokeObjectURL).toHaveBeenCalledWith(pendingUrl);
  await userEvent.click(screen.getByRole('button', { name: '移除' }));
  await waitFor(() => expect(screen.queryByRole('img', { name: '营业证件' })).toBeNull());
  expect(URL.revokeObjectURL).toHaveBeenCalledTimes(2);
});

it('替换图片、切换步骤和退出页面时释放 Blob URL', async () => {
  const props = { label: '身份证人像面', accept: '.png', onSelect: vi.fn(), onRemove: vi.fn() };
  const first = image('front.png'); const second = image('replacement.png');
  const view = render(<Files {...props} value={[first]} />);
  const oldUrl = (await screen.findByRole('img', { name: props.label })).getAttribute('src');
  view.rerender(<Files {...props} value={[second]} />);
  await waitFor(() => expect(screen.getByRole('img', { name: props.label }).getAttribute('src')).not.toBe(oldUrl));
  const newUrl = screen.getByRole('img', { name: props.label }).getAttribute('src');
  expect(URL.revokeObjectURL).toHaveBeenCalledWith(oldUrl);
  view.unmount();
  expect(URL.revokeObjectURL).toHaveBeenCalledWith(newUrl);
  render(<Files {...props} value={[second]} />);
  expect((await screen.findByRole('img', { name: props.label })).getAttribute('src')).not.toBe(newUrl);
});

it('预填图片可本地预览；只有远端文件引用时不补查或请求远端图片', async () => {
  const fetch = vi.spyOn(globalThis, 'fetch');
  const upload = vi.fn();
  const view = render(<Files label="营业证件" accept=".png" value={[{ name: 'draft.png', data: 'aW1hZ2U=' }]} onSelect={upload} onRemove={vi.fn()} />);
  expect(screen.getByRole('img', { name: '营业证件' }).getAttribute('src')).toBe('data:image/png;base64,aW1hZ2U=');
  view.rerender(<Files label="营业证件" accept=".png" value={[{ name: 'remote.png', fileContent: 'https://example.com/private-file.png', fileSuffix: 'png' }]} onSelect={upload} onRemove={vi.fn()} />);
  expect(screen.queryByRole('img', { name: '营业证件' })).toBeNull();
  expect(screen.getByText('remote.png')).toBeTruthy();
  expect(upload).not.toHaveBeenCalled(); expect(fetch).not.toHaveBeenCalled();
  fetch.mockRestore();
});

it('多张图片与非图片附件使用同一上传入口，非图片保留文件名', async () => {
  const onSelect = vi.fn(); const onRemove = vi.fn();
  render(<Files label="证明材料" multiple accept=".png,.pdf" value={[image('one.png'), { name: 'proof.pdf', fileContent: 'materials/proof.pdf' }]} onSelect={onSelect} onRemove={onRemove} />);
  expect((await screen.findByRole('img', { name: '证明材料：one.png' })).getAttribute('src')).toMatch(/^blob:/);
  expect(screen.getByText('proof.pdf')).toBeTruthy();
  expect(screen.getAllByRole('img')).toHaveLength(1);
  const two = new File(['two'], 'two.png'); const three = new File(['three'], 'three.png');
  fireEvent.change(screen.getByLabelText('证明材料'), { target: { files: [two, three] } });
  await waitFor(() => expect(onSelect).toHaveBeenCalledWith([two, three], undefined));
});

it('图片预览不会进入业务提交参数', () => {
  const file = image('license.png');
  const preview = materialPreview(material => ({ businessCertificate: material(file, 1) }));
  expect(preview.request).toEqual({ businessCertificate: { fileType: 1, fileContent: 'materials/license.png', fileSuffix: 'png' } });
  expect(JSON.stringify(preview)).not.toContain('localFile');
});

it('点击缩略图可查看大图', async () => {
  render(<Files label="营业证件" accept=".png" value={[image('license.png')]} onSelect={vi.fn()} onRemove={vi.fn()} />);
  const thumbnail = await screen.findByRole('img', { name: '营业证件' });
  fireEvent.load(thumbnail);
  await userEvent.click(thumbnail);
  await waitFor(() => expect(document.querySelector('.arco-image-preview')).not.toBeNull());
});
