import React, { useEffect, useState } from 'react';
import { Alert, Button, Radio } from '@arco-design/web-react';
import { Choice, Confirm, Feedback, Field, Files, LockedFields, More, Receipt, Summary, useOperation } from './common.jsx';
import { OperationError, materialPreview, page, required, withPrefilledOptions } from './client.js';
import { messageGroupSchema, qualificationSchema, signatureSchema } from './contracts.js';

const channels = ['CN_OTP', 'CN_NTC', 'CN_MKT'];
const sources = [[1, '公司全称／简称'], [2, 'APP 全称'], [3, '商标全称']];
const usableQualification = row => row.usable === true && row.auditStatus === 3;
const qualificationName = row => row?.businessInfo?.businessCertificateName || row?.businessCertificateName;

export function signaturePreview(values, qualification, scope, attachments) {
  required(values.content, '请输入签名内容。');
  const contentLength = Array.from(values.content).length;
  if (contentLength < 2 || contentLength > 25) throw new OperationError('签名内容须为 2 至 25 个字符。');
  if (!qualification || !usableQualification(qualification)) throw new OperationError('请选择审核通过且可用的资质。');
  const businessName = required(qualificationName(qualification), '关联资质缺少营业证件名称，请重新查询。');
  required(scope, '请选择消息组范围。');
  if (scope === 'limited' && !values.subAccounts?.length) throw new OperationError('请选择绑定的消息组。');
  if (values.source === 2 && !values.appIcpFilling && !attachments.app.length) throw new OperationError('请填写 APP ICP 备案号或上传备案截图。');
  if (values.source === 3) required(values.trademarkNumber, '请填写商标注册号。');
  if (values.desc && Array.from(values.desc).length > 300) throw new OperationError('申请说明最多 300 字。');
  const preview = materialPreview(materialFile => ({
    content: values.content, purpose: qualification.purpose, signatureIdentificationID: qualification.id,
    source: values.source, channelTypes: channels, isLimitSubAccount: scope === 'all' ? 0 : 1,
    subAccounts: scope === 'all' ? [] : values.subAccounts, from: 'vconsole',
    ...(values.desc !== undefined ? { desc: values.desc } : {}),
    ...(values.projectName !== undefined ? { projectName: values.projectName } : {}),
    ...(values.source === 2 ? { appIcp: {
      ...(values.appIcpFilling !== undefined ? { appIcpFilling: values.appIcpFilling } : {}),
      appIcpFileList: attachments.app.map(file => materialFile(file, 16)),
    } } : {}),
    ...(values.source === 3 ? { trademark: {
      trademarkCn: values.trademarkCn ?? '', trademarkEn: values.trademarkEn ?? '', trademarkNumber: values.trademarkNumber ?? '',
      trademarkFileList: attachments.trademark.map(file => materialFile(file, 17)),
    } } : {}),
    uploadFileList: attachments.other.map(file => materialFile(file, 6)),
  }));
  return { ...preview, businessName, nameRisk: !businessName.includes(values.content) };
}

export function SignatureForm({ client, prefill }) {
  const [values, setValues] = useState(() => ({
    source: prefill?.source ?? (prefill?.appIcp ? 2 : prefill?.trademark ? 3 : 1),
    content: prefill?.content,
    desc: prefill?.desc,
    projectName: prefill?.projectName,
    appIcpFilling: prefill?.appIcp?.appIcpFilling,
    trademarkCn: prefill?.trademark?.trademarkCn,
    trademarkEn: prefill?.trademark?.trademarkEn,
    trademarkNumber: prefill?.trademark?.trademarkNumber,
  }));
  const [scope, setScope] = useState(() => prefill?.isLimitSubAccount === 0
    ? 'all'
    : prefill?.isLimitSubAccount === 1 || prefill?.subAccounts?.length
      ? 'limited' : prefill?.subAccounts ? 'all' : null);
  const [qualifications, setQualifications] = useState({ rows: [], total: 0, page: 0 });
  const [groups, setGroups] = useState({ rows: [], total: 0, page: 0 });
  const [prefilledQualifications, setPrefilledQualifications] = useState([]);
  const [prefilledGroups, setPrefilledGroups] = useState([]);
  const [attachments, setAttachments] = useState(() => ({
    app: prefill?.appIcp?.appIcpFileList ?? [],
    trademark: prefill?.trademark?.trademarkFileList ?? [],
    other: prefill?.uploadFileList ?? [],
  }));
  const [preview, setPreview] = useState(null);
  const snapshot = preview?.request;
  const [receipt, setReceipt] = useState(null);
  const [status, setStatus] = useState(null);
  const operation = useOperation();
  const update = (key, value) => setValues(current => ({ ...current, [key]: value }));
  const qualificationRows = withPrefilledOptions(qualifications.rows, prefilledQualifications, 'id');
  const groupRows = withPrefilledOptions(groups.rows, prefilledGroups, 'subAccountId');
  const selected = qualificationRows.find(row => row.id === values.signatureIdentificationID);
  const content = values.content ?? (values.source === 1 ? qualificationName(selected) : undefined);
  const loadQualifications = async () => {
    const next = qualifications.page + 1;
    const result = page(await client.call('list_qualifications', { status: [3], page: next, page_size: 100 }), qualificationSchema);
    setQualifications(current => ({ ...result, rows: [...current.rows, ...result.rows], page: next }));
    return result;
  };
  const loadGroups = async () => {
    const next = groups.page + 1;
    const result = page(await client.query('GetSubAccountListForAgent', { pageIndex: next, pageSize: 100 }), messageGroupSchema);
    setGroups(current => ({ ...result, rows: [...current.rows, ...result.rows], page: next }));
    return result;
  };
  const loadInitialQualifications = async () => {
    const { rows, total } = await loadQualifications();
    const id = prefill?.signatureIdentificationID;
    if (id === undefined) {
      const usable = rows.filter(usableQualification);
      if (total === rows.length && usable.length === 1) update('signatureIdentificationID', usable[0].id);
      return;
    }
    const matches = row => row.id === id && usableQualification(row);
    const choice = rows.find(matches) ?? page(await client.call('list_qualifications', {
      qualification_id: id, status: [3], page: 1, page_size: 100,
    }), qualificationSchema).rows.find(matches);
    if (!choice) throw new OperationError('预填资质当前不可用，请重新选择。');
    setPrefilledQualifications([choice]);
    update('signatureIdentificationID', id);
  };
  const loadInitialGroups = async () => {
    const { rows, total } = await loadGroups();
    if (!prefill?.subAccounts?.length) {
      if (prefill?.subAccounts === undefined && prefill?.isLimitSubAccount !== 0 && total === 1 && rows.length === 1) {
        update('subAccounts', [rows[0].subAccountId]);
        setScope('limited');
      }
      return;
    }
    const ids = [...new Set(prefill.subAccounts)];
    const resolved = [];
    let unavailable = false;
    for (const id of ids) {
      const matches = row => row.subAccountId === id;
      const choice = rows.find(matches) ?? page(await client.query('GetSubAccountListForAgent', {
        subAccount: id, pageIndex: 1, pageSize: 100,
      }), messageGroupSchema).rows.find(matches);
      if (choice) resolved.push(choice);
      else unavailable = true;
    }
    setPrefilledGroups(resolved);
    update('subAccounts', resolved.map(row => row.subAccountId));
    if (unavailable) throw new OperationError('部分预填消息组当前不可用，请核对绑定范围。');
  };
  useEffect(() => { operation.run(async () => {
    const results = await Promise.allSettled([loadInitialQualifications(), loadInitialGroups()]);
    const failure = results.find(result => result.status === 'rejected');
    if (failure) throw failure.reason;
  }); }, [client]);
  const upload = (category, files, draftIndex) => operation.run(async () => {
    if (draftIndex === undefined && attachments[category].length + files.length > 5) throw new OperationError('每类材料最多上传 5 个文件。');
    for (const file of files) {
      const uploaded = await client.upload(file, { kind: 'material', category });
      setAttachments(current => ({ ...current, [category]: draftIndex === undefined
        ? [...current[category], uploaded]
        : current[category].map((file, index) => index === draftIndex ? uploaded : file) }));
    }
  }, { mutation: true });
  const fileArea = (category, label, accept) => <Files label={label} accept={accept} value={attachments[category]} multiple
    disabled={operation.busy || operation.uncertain} onSelect={(files, draftIndex) => upload(category, files, draftIndex)}
    onRemove={index => setAttachments(current => ({ ...current, [category]: current[category].filter((_, i) => i !== index) }))} />;
  const submit = () => operation.run(async () => {
    const result = await client.call('apply_signature', {
      request: snapshot,
      confirmation: { businessCertificateName: preview.businessName, acceptNameRisk: preview.nameRisk },
    }, { write: true });
    setReceipt({ ...result, signature: snapshot.content }); setPreview(null); setAttachments({ app: [], trademark: [], other: [] });
    await client.report({ form: 'signature', state: 'response_received', applyId: result.applyId, status: result.status });
  }, { mutation: true });

  return <LockedFields locked={operation.busy || operation.uncertain}><div className="signature-shell"><main className="signature-page">
    <header className="signature-header"><div><span className="signature-eyebrow">火山引擎 · 短信服务</span><h1>申请短信签名</h1><p>选择已有资质，填写签名信息和证明材料。</p></div></header>
    <Feedback operation={operation} />
    {receipt ? <Receipt title="签名申请结果" id={receipt.applyId}>
      <p>申请返回不等于审核通过，请查询最新审核状态。</p>
      <Button loading={operation.busy} onClick={() => operation.run(async () => setStatus(page(await client.query('ListSignaturesForAgent', { Signature: receipt.signature, ExactMatch: true, Page: 1, PageSize: 100 }), signatureSchema).rows))}>刷新审核状态</Button>
      {status?.map((row, index) => <Summary key={index} items={[[row.Industry ?? '审核结果', row.StatusDescription ?? String(row.Status ?? '未提供')], ['审核意见', row.AuditOpinion ?? '未提供']]} />)}
    </Receipt> : snapshot ? <div className="signature-panel"><Confirm title="确认签名申请" onBack={() => setPreview(null)} onSubmit={submit} busy={operation.busy} disabled={operation.uncertain}
      additionalConsent={preview.nameRisk ? '我了解签名可能审核或报备失败，仍要提交' : undefined}
      submitLabel={preview.nameRisk ? '确认承担风险并提交' : undefined}>
      {preview.nameRisk && <Alert type="warning" content="签名没有连续出现在营业证件名称中，可能无法通过审核或报备。" />}
      <Summary items={[
        ['签名', snapshot.content], ['资质', selected?.materialName ?? String(snapshot.signatureIdentificationID)],
        ['营业证件名称', preview.businessName],
        ['签名归属', snapshot.purpose === 1 ? '自用' : '他用'], ['来源', sources.find(([id]) => id === snapshot.source)?.[1]],
        ['短信类型', '验证码、通知、营销'], ['消息组', scope === 'all' ? '全部消息组' : snapshot.subAccounts.join('、')],
        ['证明材料', preview.attachmentNames.join('、') || '未添加'],
        ...(snapshot.appIcp ? [['APP ICP 备案号', snapshot.appIcp.appIcpFilling || '已提供附件']] : []),
        ...(snapshot.trademark ? [['商标中文名', snapshot.trademark.trademarkCn], ['商标英文名', snapshot.trademark.trademarkEn], ['商标注册号', snapshot.trademark.trademarkNumber]] : []),
        ...(snapshot.desc ? [['申请说明', snapshot.desc]] : []),
        ...(snapshot.projectName ? [['项目名称', snapshot.projectName]] : []),
      ]} />
    </Confirm></div> : <>
      <section className="signature-panel"><h2>基础信息</h2><div className="form-grid">
        <Field label="签名内容" value={content} onChange={value => update('content', value)} required maxLength={25} />
        <Choice label="签名来源" value={values.source} onChange={value => update('source', value)} options={sources} />
        <div className="span-2"><Choice label="关联资质" value={values.signatureIdentificationID} onChange={value => update('signatureIdentificationID', value)}
          options={qualificationRows.filter(usableQualification).map(row => [row.id, `${row.materialName ?? row.businessInfo?.businessCertificateName ?? row.id} · ${row.purpose === 1 ? '自用' : '他用'}`])} />
          <More loaded={qualifications.rows.length} total={qualifications.total} disabled={operation.busy} onClick={() => operation.run(loadQualifications)} /></div>
        <div className="span-2"><Field label="消息组范围"><Radio.Group value={scope} onChange={setScope} options={[{ value: 'all', label: '全部消息组' }, { value: 'limited', label: '指定消息组' }]} /></Field></div>
        {scope === 'limited' && <div className="span-2"><Choice label="绑定消息组" mode="multiple" value={values.subAccounts} onChange={value => update('subAccounts', value)}
          options={groupRows.map(row => [row.subAccountId, row.subAccountName || row.subAccountId])} />
          <More loaded={groups.rows.length} total={groups.total} disabled={operation.busy} onClick={() => operation.run(loadGroups)} /></div>}
      </div></section>
      <section className="signature-panel"><h2>证明材料</h2>
        {values.source === 2 && <><Field label="APP ICP 备案号" value={values.appIcpFilling} onChange={value => update('appIcpFilling', value)} />{fileArea('app', 'APP ICP 备案截图', '.png,.jpg,.jpeg,.pdf,.zip')}</>}
        {values.source === 3 && <><div className="form-grid">{[['trademarkCn', '商标中文名'], ['trademarkEn', '商标英文名'], ['trademarkNumber', '商标注册号']].map(([key, label]) =>
          <Field key={key} label={label} required={key === 'trademarkNumber'} value={values[key]} onChange={value => update(key, value)} />)}</div>{fileArea('trademark', '商标证书文件', '.png,.jpg,.jpeg,.pdf,.zip')}</>}
        {fileArea('other', '更多资料（选填）', '.png,.jpg,.jpeg,.gif,.doc,.docx,.zip')}
        <Field label="项目名称（选填）" value={values.projectName} onChange={value => update('projectName', value)} />
        <Field label="申请说明（选填）" value={values.desc} onChange={value => update('desc', value)} maxLength={300} multiline />
      </section>
      <div className="signature-actions"><Button type="primary" loading={operation.busy} disabled={operation.uncertain}
        onClick={() => operation.run(() => setPreview(signaturePreview({ ...values, content }, selected, scope, attachments)))}>核对申请信息</Button></div>
    </>}
  </main></div></LockedFields>;
}
