import React, { useRef, useState } from 'react';
import { Alert, Button, Input, Select } from '@arco-design/web-react';
import { Feedback, useOperation } from './common.jsx';
import { OperationError } from './client.js';
import {
  displayValue, inferProtocol, initialRow, labels, numberTypes, parseLink, trafficPayload, validateRows,
} from './traffic-controller.js';

export { trafficPayload } from './traffic-controller.js';

export function TrafficForm({ client, prefill }) {
  const [kind, setKind] = useState(prefill?.kind ?? 'link');
  const [rows, setRows] = useState(() => prefill?.data?.map(row => initialRow(kind, row)) ?? [initialRow(kind)]);
  const [preview, setPreview] = useState(null);
  const [receipt, setReceipt] = useState(null);
  const [fieldErrors, setFieldErrors] = useState({});
  const form = useRef(null);
  const ended = useRef(false);
  const operation = useOperation();
  const locked = operation.busy || operation.uncertain || Boolean(receipt);
  const invalidate = () => { setPreview(null); setFieldErrors({}); };
  const edit = (index, field, value) => {
    if (locked || ended.current) return;
    setRows(current => current.map((row, position) => position !== index ? row
      : field === 'link' ? { ...row, link: value, protocol: inferProtocol(value) }
        : { ...row, [field]: value }));
    invalidate();
  };
  const prepare = () => {
    if (locked || ended.current) return;
    // 每次预览先撤销旧确认，服务端校验成功后才展示新请求。
    setPreview(null);
    const errors = validateRows(kind, rows);
    setFieldErrors(errors);
    if (Object.keys(errors).length) {
      const first = form.current?.querySelector(`[data-validation-field="${Object.keys(errors)[0]}"]`);
      first?.scrollIntoView?.({ block: 'center', behavior: 'smooth' });
      first?.querySelector('input, [tabindex]')?.focus();
      return;
    }
    return operation.run(async () => {
      const request = {
        action: kind === 'link' ? 'BulkCreateTobTrafficDrivingLinkForAgent' : 'BulkCreateTobTrafficDrivingPhoneForAgent',
        params: { data: trafficPayload(kind, rows) },
      };
      await client.call('preview_traffic_resource', { request });
      setPreview(request);
    });
  };
  const submit = () => {
    if (!preview || locked || ended.current) return;
    return operation.run(async () => {
      const count = preview.params.data.length;
      let result;
      try {
        result = await client.call('submit_traffic_resources', { request: preview }, { write: true });
      } catch (error) {
        if (error instanceof OperationError && !error.unknown) setPreview(null);
        throw error;
      }
      if (result !== '') throw new OperationError('未收到明确的引流录入结果，请查询核对。', { unknown: true });
      ended.current = true;
      setReceipt({ count }); setRows([]); setPreview(null); setFieldErrors({});
      await client.report({ form: 'traffic', state: 'accepted', kind, count });
    }, { mutation: true });
  };
  const abandon = () => {
    if (locked || ended.current) return;
    return operation.run(async () => {
      ended.current = true;
      setRows([]); setPreview(null); setFieldErrors({}); setReceipt({ abandoned: true });
      await client.report({ form: 'traffic', state: 'abandoned' });
    });
  };
  const inputEnter = event => {
    if (event.key === 'Enter' && !event.nativeEvent.isComposing
      && event.target.tagName === 'INPUT' && !event.target.readOnly && !event.target.closest('.arco-select')) {
      event.preventDefault();
      prepare();
    }
  };
  function field(index, key, { required = false, wide = false, options = null, placeholder = '' } = {}) {
    const id = `traffic-${index}-${key}`;
    const value = rows[index][key] ?? '';
    const error = fieldErrors[`${index}.${key}`];
    return <div className={`traffic-field${wide ? ' wide' : ''}`} key={key}
      data-field={key} data-validation-field={`${index}.${key}`}>
      <label htmlFor={id}>{required && <span className="traffic-required" aria-hidden="true">*</span>}{labels[key]}</label>
      {options ? <Select id={id} aria-label={labels[key]} value={value === '' ? undefined : value}
        options={options.map(([value, label]) => ({ value, label }))} placeholder="请选择"
        disabled={locked} error={Boolean(error)} aria-required={required} aria-invalid={Boolean(error)}
        onChange={value => edit(index, key, value)} />
        : <Input id={id} name={key} aria-label={labels[key]} autoComplete="off" value={value}
          placeholder={placeholder} disabled={locked} error={Boolean(error)}
          aria-required={required} aria-invalid={Boolean(error)} onChange={value => edit(index, key, value)} />}
      {error && <div className="traffic-field-error" role="alert">{error}</div>}
    </div>;
  }
  function derivedField(index, key, value) {
    const id = `traffic-${index}-${key}`;
    return <div className="traffic-field" data-field={key}>
      <label htmlFor={id}>{labels[key]}</label>
      <Input id={id} aria-label={labels[key]} value={value} readOnly />
    </div>;
  }

  return <main className="traffic-page">
    <div className="traffic-eyebrow">火山引擎短信</div>
    <h1>{kind === 'phone' ? '录入引流号码' : '录入引流链接'}</h1>
    <p>{kind === 'phone' ? '填写号码及归属信息，确认后提交短信服务。个人材料不会进入对话。'
      : '核对链接及域名备案信息，确认后提交短信服务。已有查询结果可预填，缺失项在这里补充。'}</p>
    {kind === 'link' && <Alert type="info" content="文案链接是短信正文中的链接；使用火山短链时，跳转链接是客户点击后打开的落地页。" />}
    <Feedback operation={operation} />
    {receipt ? <section className="traffic-card traffic-result" aria-live="polite">
      <h2>{receipt.abandoned ? '本次录入已结束' : '引流信息已提交'}</h2>
      <p>{receipt.abandoned ? '尚未提交的材料已清除。'
        : `本次提交 ${receipt.count} 条资料。录入成功不代表运营商报备已生效，可回到对话查询资源并继续申请模板。`}</p>
    </section> : <>
      {!prefill?.kind && <div className="traffic-kind">
        <label htmlFor="traffic-kind">引流类型</label>
        <Select id="traffic-kind" aria-label="引流类型" value={kind} disabled={locked}
          options={[{ label: '引流链接', value: 'link' }, { label: '引流号码', value: 'phone' }]}
          onChange={value => {
            if (locked || ended.current) return;
            setKind(value); setRows([initialRow(value)]); invalidate();
          }} />
      </div>}
      <form ref={form} onSubmit={event => event.preventDefault()} onKeyDown={inputEnter}>
        {rows.map((row, index) => <section className="traffic-card" key={index}>
          <div className="traffic-row-title"><h2>{kind === 'link' ? '链接' : '号码'} {index + 1}</h2>
            {rows.length > 1 && <Button type="text" htmlType="button" disabled={locked} onClick={() => {
              setRows(current => current.filter((_, position) => position !== index)); invalidate();
            }}>移除</Button>}
          </div>
          <div className="traffic-fields">
            {kind === 'link' ? <>
              {field(index, 'useVolcLink', { required: true, options: [[false, '否'], [true, '是']] })}
              {!row.useVolcLink && <>
                {field(index, 'protocol', { required: true, options: [['https', 'https'], ['http', 'http'], ['缺省', '不带协议']] })}
                {field(index, 'link', { required: true, placeholder: '请输入短信正文中的完整链接' })}
                {field(index, 'linkDomainIcp', { required: true })}
                {field(index, 'linkDomainIcpBody', { required: true })}
                {derivedField(index, 'linkDomain', parseLink(row.link).domain)}
                {derivedField(index, 'linkPath', parseLink(row.link).path)}
              </>}
              {field(index, 'jumpLink', { required: row.useVolcLink === true, wide: true, placeholder: '请输入点击后打开的完整落地页链接' })}
              {field(index, 'jumpLinkDomainIcp', { required: row.useVolcLink === true })}
              {field(index, 'jumpLinkDomainIcpBody', { required: row.useVolcLink === true })}
              {row.jumpLink && <>
                {derivedField(index, 'jumpLinkDomain', parseLink(row.jumpLink).domain)}
                {derivedField(index, 'jumpLinkPath', parseLink(row.jumpLink).path)}
              </>}
            </> : <>
              {field(index, 'numberType', { required: true, options: numberTypes })}
              {field(index, 'number', { required: true, placeholder: '不带 86、空格或分隔符' })}
              {row.numberType === 1 ? <>
                {field(index, 'numberPerson')}
                {field(index, 'personType', { options: [[1, '居民身份证']] })}
                {field(index, 'personId', { wide: true })}
              </> : field(index, 'company', { wide: true })}
              {field(index, 'numberProvince')}{field(index, 'numberCity')}
            </>}
          </div>
        </section>)}
        <div className="traffic-actions">
          <Button htmlType="button" disabled={locked || rows.length >= (kind === 'link' ? 10 : 100)} onClick={() => {
            setRows(current => [...current, initialRow(kind)]); invalidate();
          }}>添加一条</Button>
          <Button type="primary" htmlType="button" disabled={locked} loading={operation.busy} onClick={prepare}>预览录入内容</Button>
        </div>
      </form>
      {preview && <section className="traffic-card" aria-label="录入预览" aria-live="polite">
        <h2>核对本次录入</h2>
        {preview.params.data.map((row, index) => <dl className="traffic-preview" key={index}>
          {Object.entries(row).filter(([, value]) => value !== '').map(([key, value]) => <React.Fragment key={key}>
            <dt>{labels[key]}</dt><dd>{displayValue(key, value)}</dd>
          </React.Fragment>)}
        </dl>)}
        <div className="traffic-actions">
          <Button type="primary" htmlType="button" disabled={locked} loading={operation.busy} onClick={submit}>确认录入</Button>
        </div>
      </section>}
      <div className="traffic-actions"><Button htmlType="button" disabled={locked} onClick={abandon}>结束本次录入</Button></div>
    </>}
  </main>;
}
