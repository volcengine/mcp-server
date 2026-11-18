import React, { useEffect, useRef, useState } from 'react';
import { Button, Image } from '@arco-design/web-react';
import { IconUpload } from '@arco-design/web-react/icon';
import { MAX_UPLOAD_BYTES } from './client.js';

const imageTypes = { jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png', gif: 'image/gif' };

function LocalImage({ file, label }) {
  const [preview, setPreview] = useState(null);
  const suffix = file.name?.split('.').pop().toLowerCase();
  const type = imageTypes[suffix];
  useEffect(() => {
    if (!type || !(file.localFile instanceof Blob)) return;
    const url = URL.createObjectURL(file.localFile);
    setPreview({ file, url });
    return () => URL.revokeObjectURL(url);
  }, [file, type]);
  const src = type && typeof file.data === 'string' ? `data:${type};base64,${file.data}`
    : preview?.file === file ? preview.url : undefined;
  return src ? <Image className="sms-file-preview" src={src} alt={label} width={96} height={72}
    preview previewProps={{ imgAttributes: { alt: label } }} /> : null;
}

// 保留原上传控件，仅为当前页面持有的图片增加预览，不查询远端材料。
export function Files({ label, accept, value = [], onSelect, onRemove, multiple = false, disabled = false, uploadDisabled = disabled }) {
  const input = useRef(null);
  const [pending, setPending] = useState({ files: [], index: undefined });
  const select = async (selected, index) => {
    if (!selected.length || uploadDisabled) return;
    setPending({ files: selected.filter(file => imageTypes[file.name?.split('.').pop().toLowerCase()]).map(file => ({ name: file.name,
      localFile: file.size <= MAX_UPLOAD_BYTES ? file : undefined, data: file.data })), index });
    try { await onSelect(selected, index); } finally { setPending({ files: [], index: undefined }); }
  };
  const files = pending.files.length ? pending.index !== undefined
    ? value.map((file, index) => index === pending.index ? pending.files[0] : file)
    : multiple ? [...value, ...pending.files] : pending.files : value;
  return <div className="upload-block">
    <div className="upload-label">{label}</div>
    <div className="upload-zone">
      <IconUpload className="upload-icon" />
      <Button disabled={uploadDisabled} onClick={() => input.current?.click()}>选择并上传</Button>
      <input ref={input} hidden type="file" aria-label={label} accept={accept} multiple={multiple}
        disabled={uploadDisabled} onChange={event => {
          const selected = Array.from(event.target.files ?? []);
          event.target.value = '';
          select(selected);
        }} />
      <div className="upload-tip">单个文件最大 10 MB</div>
    </div>
    {files.map((file, index) => <div className="sms-file" key={index}>
      <div className="sms-file-content"><LocalImage file={file} label={multiple ? `${label}：${file.name}` : label} />
        <span>{file.name}{file.data !== undefined && '（待上传）'}</span></div>
      {file.data !== undefined && <Button type="text" disabled={uploadDisabled || pending.files.includes(file)} aria-label={`上传 ${file.name}`}
        onClick={() => select([file], index)}>上传</Button>}
      <Button type="text" disabled={disabled || pending.files.includes(file)} onClick={() => onRemove(index)}>移除</Button>
    </div>)}
  </div>;
}
