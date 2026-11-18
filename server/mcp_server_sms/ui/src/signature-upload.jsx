import React, { useEffect, useRef, useState } from 'react';
import { Message, Upload } from '@arco-design/web-react';
import { MAX_UPLOAD_BYTES } from './client.js';
import { materialTypes, maxFiles } from './signature-controller.js';

export function SignatureUpload({ kind, files, total, disabled, onUpload, onRemove }) {
  const container = useRef(null);
  const urls = useRef(new Map());
  const [previews, setPreviews] = useState({});
  const material = materialTypes[kind];
  useEffect(() => {
    container.current?.querySelector('input[type="file"]')?.setAttribute('aria-label', material.title);
    const current = new Set(files.map(file => file.uid));
    for (const [uid, url] of urls.current) {
      if (!current.has(uid)) { URL.revokeObjectURL(url); urls.current.delete(uid); }
    }
    for (const file of files) {
      if (file.localFile instanceof Blob && !urls.current.has(file.uid)) {
        urls.current.set(file.uid, URL.createObjectURL(file.localFile));
      }
    }
    setPreviews(Object.fromEntries(urls.current));
  }, [files, material.title]);
  useEffect(() => () => {
    urls.current.forEach(url => URL.revokeObjectURL(url));
    urls.current.clear();
  }, []);
  const fileList = files.map(file => {
    const image = /\.(png|jpe?g|gif)$/i.test(file.name);
    const url = image && (file.data !== undefined
      ? `data:image/${file.name.split('.').pop().toLowerCase() === 'jpg' ? 'jpeg' : file.name.split('.').pop().toLowerCase()};base64,${file.data}`
      : previews[file.uid]);
    return { ...file, name: file.data !== undefined ? `${file.name}（待上传）` : file.name,
      originFile: file.data !== undefined ? file : undefined, status: file.data !== undefined ? 'init' : 'done',
      // 草稿可能是私密元数据对象；显式空 URL 防止 Arco 为非 Blob 调用 createObjectURL。
      url: url || '', ...(url ? { thumbUrl: url } : {}) };
  });
  return <section ref={container} className="signature-field signature-upload" data-material={kind}>
    <label>{material.title}</label>
    <p className="signature-help">{material.hint}</p>
    <Upload className="signature-upload__control" accept={material.accept} autoUpload drag multiple
      disabled={disabled} fileList={fileList}
      limit={{ maxCount: maxFiles, hideOnExceedLimit: false }}
      beforeUpload={file => {
        const suffix = `.${file.name?.split('.').pop().toLowerCase()}`;
        if (!material.accept.split(',').includes(suffix)) {
          Message.error('请选择当前材料支持的文件类型。'); return false;
        }
        if (!file.size || file.size > MAX_UPLOAD_BYTES) {
          Message.error('请选择不超过 10 MB 的非空文件。'); return false;
        }
        return true;
      }}
      customRequest={({ file, onSuccess, onError }) => {
        onUpload(kind, file.originFile ?? file, file.uid ?? crypto.randomUUID()).then(onSuccess, onError);
        return { abort() {} };
      }}
      onRemove={item => { onRemove(kind, item.uid); return false; }}
      onExceedLimit={() => Message.warning('本次最多上传 5 份材料')}
    >
      <div className="signature-upload__trigger" aria-disabled={disabled || total >= maxFiles}>
        <span className="signature-upload__icon">＋</span>
        <strong>点击或拖拽文件到这里</strong>
        <small>{material.description}</small>
        <small>单个文件最大 10 MB，本次最多上传 5 份材料</small>
      </div>
    </Upload>
  </section>;
}
