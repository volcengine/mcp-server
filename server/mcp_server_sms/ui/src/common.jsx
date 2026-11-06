import React, { createContext, useContext, useId, useRef, useState } from 'react';
import { Alert, Button, Checkbox, Input, Select } from '@arco-design/web-react';
import { IconUpload } from '@arco-design/web-react/icon';
import { OperationError } from './client.js';

const LockContext = createContext(false);
export function LockedFields({ locked, children }) {
  return <LockContext.Provider value={locked}>{children}</LockContext.Provider>;
}

export function Field({ label, value, onChange, required = false, type = 'text', multiline = false, children, ...props }) {
  const id = useId();
  const locked = useContext(LockContext);
  const Component = multiline ? Input.TextArea : Input;
  return <div className="traffic-field">
    <label htmlFor={id}>{required && <span className="traffic-required">*</span>}{label}</label>
    {React.isValidElement(children) ? React.cloneElement(children, { disabled: locked || children.props.disabled })
      : <Component id={id} aria-label={label} value={value ?? ''} type={type} onChange={onChange} {...props} disabled={locked || props.disabled} />}
  </div>;
}

export function Choice({ label, value, onChange, options, ...props }) {
  const id = useId();
  return <Field label={label}><Select id={id} aria-label={label} value={value} onChange={onChange}
    options={options.map(([value, label]) => ({ value, label }))} {...props} /></Field>;
}

export function Files({ label, accept, value = [], onSelect, onRemove, multiple = false, disabled = false }) {
  const input = useRef(null);
  return <div className="upload-block">
    <div className="upload-label">{label}</div>
    <div className="upload-zone">
      <IconUpload className="upload-icon" />
      <Button disabled={disabled} onClick={() => input.current?.click()}>选择并上传</Button>
      <input ref={input} hidden type="file" aria-label={label} accept={accept} multiple={multiple}
        disabled={disabled} onChange={event => {
          const selected = Array.from(event.target.files ?? []);
          event.target.value = '';
          if (selected.length) onSelect(selected);
        }} />
      <div className="upload-tip">单个文件最大 10 MB</div>
    </div>
    {value.map((file, index) => <div className="sms-file" key={index}>
      <span>{file.name}</span><Button type="text" disabled={disabled} onClick={() => onRemove(index)}>移除</Button>
    </div>)}
  </div>;
}

export function useOperation() {
  const lock = useRef(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);
  const [uncertain, setUncertain] = useState(false);
  const run = async (operation, { mutation = false } = {}) => {
    if (lock.current || (mutation && uncertain)) return;
    lock.current = true; setBusy(true); setError(null);
    try { return await operation(); }
    catch (cause) {
      const known = cause instanceof OperationError;
      const problem = known ? cause : new OperationError('操作未完成，请核对当前结果。', { unknown: mutation });
      setError(problem);
      if (problem.unknown) setUncertain(true);
    } finally { lock.current = false; setBusy(false); }
  };
  return { run, busy, error, uncertain };
}

export function Feedback({ operation }) {
  if (!operation.error) return null;
  return <Alert className="sms-feedback" type={operation.uncertain ? 'warning' : 'error'}
    content={<>{operation.error.message}{operation.error.code && <div>错误码：{operation.error.code}</div>}{operation.error.requestId && <div>排障编号：{operation.error.requestId}</div>}</>} />;
}

export function Summary({ items }) {
  return <dl className="traffic-preview">{items.map(([name, value]) => <React.Fragment key={name}>
    <dt>{name}</dt><dd>{value}</dd>
  </React.Fragment>)}</dl>;
}

export function maskedIdentifier(value) {
  if (!value) return '未填写';
  return value.length > 7 ? value.slice(0, 3) + '…' + value.slice(-4) : '已填写';
}

export function Confirm({ title, children, onBack, onSubmit, busy, disabled, submitLabel = '确认提交', backLabel = '返回修改' }) {
  const [agreed, setAgreed] = useState(false);
  return <section className="review-section">
    <h2>{title}</h2>{children}
    <Checkbox checked={agreed} onChange={setAgreed}>我已核对以上信息，同意提交本次操作</Checkbox>
    <div className="traffic-actions">
      <Button disabled={busy || disabled} onClick={onBack}>{backLabel}</Button>
      <Button type="primary" loading={busy} disabled={!agreed || disabled} onClick={onSubmit}>{submitLabel}</Button>
    </div>
  </section>;
}

export function Receipt({ title, id, children }) {
  return <div className="completion traffic-result"><h2>{title}</h2>
    {id && <p>编号：{id}</p>}{children}
  </div>;
}

export function More({ loaded, total, onClick, disabled }) {
  return <div className="sms-catalog-count">已加载 {loaded} / {total}
    {loaded < total && <Button type="text" disabled={disabled} onClick={onClick}>加载更多</Button>}
  </div>;
}
