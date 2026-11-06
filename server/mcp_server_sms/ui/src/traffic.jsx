import React, { useState } from 'react';
import { Button, Checkbox, Radio } from '@arco-design/web-react';
import { Choice, Confirm, Feedback, Field, Receipt, Summary, maskedIdentifier, useOperation } from './common.jsx';
import { required } from './client.js';

const numberTypes = [[1, '手机号码'], [2, '400 号码'], [3, '700 号码'], [4, '800 号码'], [5, '95 / 96 号码'], [6, '12 号码'], [7, '固定电话']];
const labels = {
  link: '文案链接', protocol: '文案链接协议', linkDomainIcp: '文案域名备案号', linkDomainIcpBody: '文案域名备案主体',
  jumpLink: '跳转链接', jumpLinkDomainIcp: '跳转域名备案号', jumpLinkDomainIcpBody: '跳转域名备案主体',
  number: '联系号码', company: '号码所属企业', numberProvince: '号码归属省份', numberCity: '号码归属城市',
  numberPerson: '号码所属人', personId: '证件号码',
  useVolcLink: '使用火山短链', numberType: '号码类型', personType: '证件类型',
};

export function trafficPayload(kind, rows) {
  return rows.map(row => {
    if (kind === 'phone') {
      required(row.numberType, '请选择号码类型。'); required(row.number, '请输入联系号码。');
      const fields = ['numberType', 'number', 'numberProvince', 'numberCity', ...(row.numberType === 1 ? ['numberPerson', 'personType', 'personId'] : ['company'])];
      return Object.fromEntries(fields.filter(key => row[key] !== undefined).map(key => [key, row[key]]));
    }
    const fields = row.useVolcLink
      ? ['useVolcLink', 'jumpLink', 'jumpLinkDomainIcp', 'jumpLinkDomainIcpBody']
      : ['useVolcLink', 'protocol', 'link', 'linkDomainIcp', 'linkDomainIcpBody'];
    fields.forEach(key => required(row[key], `请填写${labels[key] ?? '链接类型'}。`));
    return Object.fromEntries(fields.map(key => [key, row[key]]));
  });
}

export function TrafficForm({ client }) {
  const [kind, setKind] = useState('link');
  const [rows, setRows] = useState([{ useVolcLink: false, protocol: 'https' }]);
  const [preview, setPreview] = useState(null);
  const [receipt, setReceipt] = useState(false);
  const operation = useOperation();
  const edit = (index, field, value) => setRows(current => current.map((row, i) => i === index ? { ...row, [field]: value } : row));
  const submit = () => operation.run(async () => {
    const count = preview.length;
    await client.call('register_traffic_resource', { request: {
      action: kind === 'link' ? 'BulkCreateTobTrafficDrivingLinkForAgent' : 'BulkCreateTobTrafficDrivingPhoneForAgent',
      params: { data: preview },
    } }, { write: true });
    setReceipt(true); setRows([]); setPreview(null);
    await client.report({ form: 'traffic', state: 'accepted', kind, count });
  }, { mutation: true });

  return <main className="traffic-page">
    <span className="traffic-eyebrow">火山引擎 · 短信服务</span>
    <h1>录入短信引流信息</h1><p>填写真实的链接备案或号码归属信息，核对后再提交。</p>
    <Feedback operation={operation} />
    {receipt ? <Receipt title="录入请求已受理"><p>资源录入不代表模板审核、运营商报备或短信送达。</p></Receipt>
      : preview ? <div className="traffic-card"><Confirm title="确认本次引流信息" busy={operation.busy} disabled={operation.uncertain}
        onBack={() => setPreview(null)} onSubmit={submit}>
        {preview.map((row, index) => <Summary key={index} items={[
          ['序号', index + 1], ...Object.entries(row).map(([key, value]) => [labels[key],
            key === 'useVolcLink' ? value ? '是' : '否'
              : key === 'numberType' ? numberTypes.find(([id]) => id === value)?.[1]
                : key === 'personType' ? value === 1 ? '居民身份证' : '未填写'
                  : key === 'personId' ? maskedIdentifier(value) : value || '未填写']),
        ]} />)}
      </Confirm></div> : <>
        <Radio.Group value={kind} disabled={operation.busy || operation.uncertain} onChange={value => {
          setKind(value); setRows([value === 'link' ? { useVolcLink: false, protocol: 'https' } : {}]);
        }} options={[{ label: '引流链接', value: 'link' }, { label: '联系号码', value: 'phone' }]} />
        <fieldset disabled={operation.busy || operation.uncertain} className="sms-fieldset">
          {rows.map((row, index) => <section className="traffic-card" key={index}>
            <div className="traffic-row-title"><h2>{kind === 'link' ? '链接' : '号码'} {index + 1}</h2>
              {rows.length > 1 && <Button type="text" onClick={() => setRows(rows.filter((_, i) => i !== index))}>移除</Button>}
            </div>
            {kind === 'link' ? <>
              <Checkbox checked={row.useVolcLink} onChange={value => edit(index, 'useVolcLink', value)}>使用火山短链</Checkbox>
              <div className="traffic-fields">
                {!row.useVolcLink && <Choice label="文案链接协议" value={row.protocol} onChange={value => edit(index, 'protocol', value)} options={[['https', 'https'], ['http', 'http'], ['缺省', '缺省']]} />}
                {(row.useVolcLink ? ['jumpLink', 'jumpLinkDomainIcp', 'jumpLinkDomainIcpBody'] : ['link', 'linkDomainIcp', 'linkDomainIcpBody']).map(key =>
                  <Field key={key} label={labels[key]} value={row[key]} onChange={value => edit(index, key, value)} required />)}
              </div>
            </> : <div className="traffic-fields">
              <Choice label="号码类型" value={row.numberType} onChange={value => edit(index, 'numberType', value)} options={numberTypes} />
              <Field label="联系号码" value={row.number} onChange={value => edit(index, 'number', value)} required />
              {(row.numberType === 1 ? ['numberPerson', 'personId'] : ['company']).map(key =>
                <Field key={key} label={labels[key]} value={row[key]} onChange={value => edit(index, key, value)} />)}
              {row.numberType === 1 && <Choice label="证件类型" value={row.personType} onChange={value => edit(index, 'personType', value)} options={[[0, '未填写'], [1, '居民身份证']]} />}
              {['numberProvince', 'numberCity'].map(key => <Field key={key} label={labels[key]} value={row[key]} onChange={value => edit(index, key, value)} />)}
            </div>}
          </section>)}
        </fieldset>
        <div className="traffic-actions">
          <Button disabled={operation.busy || operation.uncertain || rows.length >= (kind === 'link' ? 10 : 100)} onClick={() => setRows([...rows, kind === 'link' ? { useVolcLink: false, protocol: 'https' } : {}])}>继续添加</Button>
          <Button type="primary" loading={operation.busy} disabled={operation.uncertain} onClick={() => operation.run(() => setPreview(trafficPayload(kind, rows)))}>核对信息</Button>
        </div>
      </>}
  </main>;
}
