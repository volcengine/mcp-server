import React, { useEffect, useState } from 'react';
import { Button, Radio } from '@arco-design/web-react';
import { Choice, Confirm, Feedback, Field, Files, LockedFields, More, Receipt, Summary, useOperation } from './common.jsx';
import { OperationError, page, required } from './client.js';
import { messageGroupSchema, qualificationSchema, signatureSchema } from './contracts.js';

const channels = ['CN_OTP', 'CN_NTC', 'CN_MKT'];
const sources = [[1, '公司全称／简称'], [2, 'APP 全称'], [3, '商标全称']];
export const materialFile = (file, type) => ({ fileType: type, fileContent: file.fileContent, fileSuffix: file.fileSuffix });

export function signaturePayload(values, qualification, scope, attachments) {
  required(values.content, '请输入签名内容。');
  if (!qualification || qualification.usable !== true || qualification.auditStatus !== 3) throw new OperationError('请选择审核通过且可用的资质。');
  required(scope, '请选择消息组范围。');
  if (scope === 'limited' && !values.subAccounts?.length) throw new OperationError('请选择绑定的消息组。');
  if (values.source === 2 && !values.appIcpFilling && !attachments.app.length) throw new OperationError('请填写 APP ICP 备案号或上传备案截图。');
  return {
    content: values.content, purpose: qualification.purpose, signatureIdentificationID: qualification.id,
    source: values.source, channelTypes: channels, isLimitSubAccount: scope === 'all' ? 0 : 1,
    subAccounts: scope === 'all' ? [] : values.subAccounts, from: 'vconsole',
    ...(values.desc !== undefined ? { desc: values.desc } : {}),
    ...(values.source === 2 ? { appIcp: {
      ...(values.appIcpFilling !== undefined ? { appIcpFilling: values.appIcpFilling } : {}),
      appIcpFileList: attachments.app.map(file => materialFile(file, 16)),
    } } : {}),
    ...(values.source === 3 ? { trademark: {
      trademarkCn: values.trademarkCn ?? '', trademarkEn: values.trademarkEn ?? '', trademarkNumber: values.trademarkNumber ?? '',
      trademarkFileList: attachments.trademark.map(file => materialFile(file, 17)),
    } } : {}),
    uploadFileList: attachments.other.map(file => materialFile(file, 6)),
  };
}

export function SignatureForm({ client }) {
  const [values, setValues] = useState({ source: 1 });
  const [scope, setScope] = useState(null);
  const [qualifications, setQualifications] = useState({ rows: [], total: 0, page: 0 });
  const [groups, setGroups] = useState({ rows: [], total: 0, page: 0 });
  const [attachments, setAttachments] = useState({ app: [], trademark: [], other: [] });
  const [snapshot, setSnapshot] = useState(null);
  const [receipt, setReceipt] = useState(null);
  const [status, setStatus] = useState(null);
  const operation = useOperation();
  const update = (key, value) => setValues(current => ({ ...current, [key]: value }));
  const selected = qualifications.rows.find(row => row.id === values.signatureIdentificationID);
  const loadQualifications = async () => {
    const next = qualifications.page + 1;
    const result = page(await client.call('list_qualifications', { status: [3], page: next, page_size: 100 }), qualificationSchema);
    setQualifications(current => ({ ...result, rows: [...current.rows, ...result.rows], page: next }));
  };
  const loadGroups = async () => {
    const next = groups.page + 1;
    const result = page(await client.query('GetSubAccountListForAgent', { pageIndex: next, pageSize: 100 }), messageGroupSchema);
    setGroups(current => ({ ...result, rows: [...current.rows, ...result.rows], page: next }));
  };
  useEffect(() => { operation.run(async () => { await loadQualifications(); await loadGroups(); }); }, [client]);
  const upload = (category, files) => operation.run(async () => {
    if (attachments[category].length + files.length > 5) throw new OperationError('每类材料最多上传 5 个文件。');
    for (const file of files) {
      const uploaded = await client.upload(file, { kind: 'material', category });
      setAttachments(current => ({ ...current, [category]: [...current[category], uploaded] }));
    }
  }, { mutation: true });
  const fileArea = (category, label, accept) => <Files label={label} accept={accept} value={attachments[category]} multiple
    disabled={operation.busy || operation.uncertain} onSelect={files => upload(category, files)}
    onRemove={index => setAttachments(current => ({ ...current, [category]: current[category].filter((_, i) => i !== index) }))} />;
  const submit = () => operation.run(async () => {
    const result = await client.call('apply_signature', { request: snapshot }, { write: true });
    setReceipt({ ...result, signature: snapshot.content }); setSnapshot(null); setAttachments({ app: [], trademark: [], other: [] });
    await client.report({ form: 'signature', state: 'response_received', applyId: result.applyId, status: result.status });
  }, { mutation: true });

  return <LockedFields locked={operation.busy || operation.uncertain}><div className="signature-shell"><main className="signature-page">
    <header className="signature-header"><div><span className="signature-eyebrow">火山引擎 · 短信服务</span><h1>申请短信签名</h1><p>选择已有资质，填写签名信息和证明材料。</p></div></header>
    <Feedback operation={operation} />
    {receipt ? <Receipt title="签名申请结果" id={receipt.applyId}>
      <p>申请返回不等于审核通过，请查询最新审核状态。</p>
      <Button loading={operation.busy} onClick={() => operation.run(async () => setStatus(page(await client.query('ListSignaturesForAgent', { Signature: receipt.signature, ExactMatch: true, Page: 1, PageSize: 100 }), signatureSchema).rows))}>刷新审核状态</Button>
      {status?.map((row, index) => <Summary key={index} items={[[row.Industry ?? '审核结果', row.StatusDescription ?? String(row.Status ?? '未提供')], ['审核意见', row.AuditOpinion ?? '未提供']]} />)}
    </Receipt> : snapshot ? <div className="signature-panel"><Confirm title="确认签名申请" onBack={() => setSnapshot(null)} onSubmit={submit} busy={operation.busy} disabled={operation.uncertain}>
      <Summary items={[
        ['签名', snapshot.content], ['资质', selected?.materialName ?? String(snapshot.signatureIdentificationID)],
        ['签名归属', snapshot.purpose === 1 ? '自用' : '他用'], ['来源', sources.find(([id]) => id === snapshot.source)?.[1]],
        ['短信类型', '验证码、通知、营销'], ['消息组', scope === 'all' ? '全部消息组' : snapshot.subAccounts.join('、')],
        ['证明材料', Object.values(attachments).flat().map(file => file.name).join('、') || '未添加'],
        ...(snapshot.appIcp ? [['APP ICP 备案号', snapshot.appIcp.appIcpFilling || '已提供附件']] : []),
        ...(snapshot.trademark ? [['商标中文名', snapshot.trademark.trademarkCn], ['商标英文名', snapshot.trademark.trademarkEn], ['商标注册号', snapshot.trademark.trademarkNumber]] : []),
        ...(snapshot.desc ? [['申请说明', snapshot.desc]] : []),
      ]} />
    </Confirm></div> : <>
      <section className="signature-panel"><h2>基础信息</h2><div className="form-grid">
        <Field label="签名内容" value={values.content} onChange={value => update('content', value)} required maxLength={25} />
        <Choice label="签名来源" value={values.source} onChange={value => update('source', value)} options={sources} />
        <div className="span-2"><Choice label="关联资质" value={values.signatureIdentificationID} onChange={value => update('signatureIdentificationID', value)}
          options={qualifications.rows.filter(row => row.usable === true && row.auditStatus === 3).map(row => [row.id, `${row.materialName ?? row.businessInfo?.businessCertificateName ?? row.id} · ${row.purpose === 1 ? '自用' : '他用'}`])} />
          <More loaded={qualifications.rows.length} total={qualifications.total} disabled={operation.busy} onClick={() => operation.run(loadQualifications)} /></div>
        <div className="span-2"><Field label="消息组范围"><Radio.Group value={scope} onChange={setScope} options={[{ value: 'all', label: '全部消息组' }, { value: 'limited', label: '指定消息组' }]} /></Field></div>
        {scope === 'limited' && <div className="span-2"><Choice label="绑定消息组" mode="multiple" value={values.subAccounts} onChange={value => update('subAccounts', value)}
          options={groups.rows.map(row => [row.subAccountId, row.subAccountName || row.subAccountId])} />
          <More loaded={groups.rows.length} total={groups.total} disabled={operation.busy} onClick={() => operation.run(loadGroups)} /></div>}
      </div></section>
      <section className="signature-panel"><h2>证明材料</h2>
        {values.source === 2 && <><Field label="APP ICP 备案号" value={values.appIcpFilling} onChange={value => update('appIcpFilling', value)} />{fileArea('app', 'APP ICP 备案截图', '.png,.jpg,.jpeg,.pdf,.zip')}</>}
        {values.source === 3 && <><div className="form-grid">{[['trademarkCn', '商标中文名'], ['trademarkEn', '商标英文名'], ['trademarkNumber', '商标注册号']].map(([key, label]) =>
          <Field key={key} label={label} value={values[key]} onChange={value => update(key, value)} />)}</div>{fileArea('trademark', '商标证书文件', '.png,.jpg,.jpeg,.pdf,.zip')}</>}
        {fileArea('other', '更多资料（选填）', '.png,.jpg,.jpeg,.gif,.doc,.docx,.zip')}
        <Field label="申请说明（选填）" value={values.desc} onChange={value => update('desc', value)} multiline />
      </section>
      <div className="signature-actions"><Button type="primary" loading={operation.busy} disabled={operation.uncertain}
        onClick={() => operation.run(() => setSnapshot(signaturePayload(values, selected, scope, attachments)))}>核对申请信息</Button></div>
    </>}
  </main></div></LockedFields>;
}
