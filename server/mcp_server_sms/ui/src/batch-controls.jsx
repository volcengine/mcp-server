import React, { useEffect, useRef, useState } from 'react';
import { Button, Descriptions, Form, Input, Message, Select, Upload } from '@arco-design/web-react';
import { IconUpload } from '@arco-design/web-react/icon';
import { MAX_UPLOAD_BYTES } from './client.js';

export function BatchHeading({ title, description }) {
  return <div className="batch-section-heading"><h2>{title}</h2>
    {description && <p>{description}</p>}</div>;
}

export function BatchField({ label, value, onChange, required = false, multiline = false, disabled = false, children, ...props }) {
  const Component = multiline ? Input.TextArea : Input;
  return <Form.Item className="batch-input-field" layout="vertical" labelCol={{ span: 24 }} wrapperCol={{ span: 24 }}
    label={label} required={required} colon={false}>
    {React.isValidElement(children) ? (typeof children.type === 'string' ? children
      : React.cloneElement(children, { disabled: disabled || children.props.disabled }))
      : <Component aria-label={label} value={value ?? ''} onChange={onChange} {...props} disabled={disabled} />}
  </Form.Item>;
}

export function BatchChoice({ label, value, onChange, options, ...props }) {
  return <BatchField label={label}><Select aria-label={label} value={value} onChange={onChange}
    options={options.map(([value, label]) => ({ value, label }))} {...props} /></BatchField>;
}

export function BatchDetails({ items, className }) {
  const [compact, setCompact] = useState(() => window.innerWidth < 600);
  useEffect(() => {
    const resize = () => setCompact(window.innerWidth < 600);
    window.addEventListener('resize', resize);
    return () => window.removeEventListener('resize', resize);
  }, []);
  return <Descriptions className={['batch-details', className].filter(Boolean).join(' ')} border column={compact ? 1 : 2}
    data={items.map(([label, value]) => ({ label, value: value ?? '--' }))} />;
}

export function batchTime(value) {
  const numeric = typeof value === 'number' || (typeof value === 'string' && /^\d+(\.\d+)?$/.test(value)) ? Number(value) : null;
  // 任务时间使用 Unix 秒，发送记录返回毫秒；也兼容明确带时区的 ISO 时间。
  const milliseconds = numeric !== null ? (numeric < 1e12 ? numeric * 1000 : numeric)
    : typeof value === 'string' && /(Z|[+-]\d{2}:\d{2})$/.test(value) ? Date.parse(value) : NaN;
  const date = new Date(milliseconds);
  return milliseconds > 0 && Number.isFinite(date.getTime()) ? new Intl.DateTimeFormat('zh-CN', {
    timeZone: 'Asia/Shanghai', dateStyle: 'medium', timeStyle: 'medium', hour12: false,
  }).format(date) + '（北京时间）' : '--';
}

export function BatchUpload({ file, disabled, uploadDisabled, onUpload, onRemove }) {
  const container = useRef(null);
  useEffect(() => {
    const input = container.current?.querySelector('input[type="file"]');
    if (input) { input.setAttribute('aria-label', '群发 CSV 名单'); input.disabled = uploadDisabled; }
  });
  const fileList = file ? [{ uid: file.file ?? file.name, name: file.name + (file.data !== undefined ? '（待上传）' : ''),
    status: file.data !== undefined ? 'init' : 'done', url: '' }] : [];
  return <div ref={container} className="batch-upload-button">
    <Upload accept=".csv,text/csv" autoUpload disabled={uploadDisabled} fileList={fileList}
      showUploadList={{ removeIcon: null, previewIcon: null, startIcon: null, reuploadIcon: null, cancelIcon: null }}
      beforeUpload={source => {
        if (!/\.csv$/i.test(source.name)) { Message.error('请选择 CSV 名单文件。'); return false; }
        if (!source.size || source.size > MAX_UPLOAD_BYTES) {
          Message.error('请选择不超过 10 MB 的非空文件。'); return false;
        }
        return true;
      }}
      customRequest={({ file: selected, onSuccess, onError }) => {
        onUpload(selected.originFile ?? selected).then(result => result ? onSuccess() : onError(), onError);
        return { abort() {} };
      }}>
      <Button htmlType="button" type="primary" disabled={uploadDisabled} icon={<IconUpload />}>点击上传文件</Button>
    </Upload>
    {file && <div className="batch-file-actions">
      {file.data !== undefined && <Button htmlType="button" type="text" disabled={uploadDisabled}
        aria-label={`上传 ${file.name}`} onClick={() => onUpload(file)}>上传</Button>}
      <Button htmlType="button" type="text" disabled={disabled} onClick={onRemove}>移除</Button>
    </div>}
  </div>;
}
