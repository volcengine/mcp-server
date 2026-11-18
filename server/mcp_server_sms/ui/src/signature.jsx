import React, { useEffect, useRef, useState } from 'react';
import { Alert, Button, Input, Modal, Select, Spin } from '@arco-design/web-react';
import { Feedback, useOperation } from './common.jsx';
import { OperationError, page } from './client.js';
import { signatureSchema } from './contracts.js';
import {
  channels, loadSignatureGroups, loadSignatureQualifications, maxFiles, purposes,
  signatureBaseErrors, signaturePreview, sources,
} from './signature-controller.js';
import { SignatureUpload } from './signature-upload.jsx';

export { signaturePreview } from './signature-controller.js';
const reviewLabels = { 1: '审核中', 2: '审核未通过', 3: '审核通过', 5: '免审', 16: '等待资质审核通过' };
const guide = 'https://www.volcengine.com/docs/6361/1551554';

function SignatureField({ name, label, required, help, error, children }) {
  return <section className={`signature-field${error ? ' is-error' : ''}`} data-validation-field={name}>
    <label htmlFor={children?.props?.id}>{label}{required && <> <em>*</em></>}</label>
    {children?.props?.id ? React.cloneElement(children, { 'aria-label': label }) : children}
    {error && <p className="signature-field-error">{error}</p>}
    {help && <p className="signature-help">{help}</p>}
  </section>;
}

export function SignatureForm({ client, prefill }) {
  const [values, setValues] = useState(() => ({
    source: prefill?.source ?? (prefill?.appIcp ? 2 : prefill?.trademark ? 3 : 1),
    content: prefill?.content, desc: prefill?.desc, projectName: prefill?.projectName,
    appIcp: prefill?.appIcp, trademark: prefill?.trademark,
  }));
  const [scope, setScope] = useState(() => prefill?.isLimitSubAccount === 0
    ? 'all' : prefill?.isLimitSubAccount === 1 || prefill?.subAccounts?.length
      ? 'limited' : prefill?.subAccounts ? 'all' : null);
  const [qualifications, setQualifications] = useState([]);
  const [groups, setGroups] = useState([]);
  const [loaded, setLoaded] = useState(false);
  const [step, setStep] = useState('base');
  const [baseCompleted, setBaseCompleted] = useState(false);
  const [fieldErrors, setFieldErrors] = useState({});
  const [attachments, setAttachments] = useState(() => Object.fromEntries([
    ['app', prefill?.appIcp?.appIcpFileList], ['trademark', prefill?.trademark?.trademarkFileList],
    ['other', prefill?.uploadFileList],
  ].map(([kind, files]) => [kind, (files ?? []).map((file, index) => ({ ...file, uid: `${kind}-${index}` }))])));
  const attachmentsRef = useRef(attachments);
  const uploadQueue = useRef(Promise.resolve());
  const pendingUploads = useRef(0);
  const reservedFiles = useRef(0);
  const [uploadBusy, setUploadBusy] = useState(false);
  const [uploadError, setUploadError] = useState(null);
  const [preview, setPreviewState] = useState(null);
  const previewRef = useRef(null);
  const setPreview = next => { previewRef.current = next; setPreviewState(next); };
  const [receipt, setReceipt] = useState(null);
  const [statuses, setStatuses] = useState(null);
  const done = useRef(false);
  const operation = useOperation();
  const locked = operation.busy || operation.uncertain || uploadBusy;
  const material = qualifications.find(row => row.id === values.signatureIdentificationID);
  const qualificationLocked = prefill?.signatureIdentificationID !== undefined
    && qualifications.some(row => row.id === prefill.signatureIdentificationID);
  const qualificationOptions = qualifications
    .filter(row => values.purpose === undefined || row.purpose === values.purpose)
    .map(row => ({ value: row.id,
      label: `${row.id}【${row.businessCertificateName}】· ${row.purpose === 1 ? '自用' : '他用'}` }));
  const totalFiles = Object.values(attachments).flat().length;

  const edit = (patch, { invalidateBase = false, clearErrors = Object.keys(patch) } = {}) => {
    if (locked || done.current) return;
    setValues(previous => ({ ...previous, ...patch }));
    setFieldErrors(previous => Object.fromEntries(
      Object.entries(previous).filter(([field]) => !clearErrors.includes(field)),
    ));
    if (invalidateBase) setBaseCompleted(false);
    setPreview(null);
    setUploadError(null);
  };
  useEffect(() => {
    let active = true;
    operation.run(async () => {
      const results = await Promise.allSettled([
        loadSignatureQualifications(client, prefill).then(({ rows, selected, unavailable }) => {
          if (!active) return;
          setQualifications(rows);
          if (selected) setValues(previous => ({ ...previous, purpose: selected.purpose,
            signatureIdentificationID: selected.id,
            ...(previous.source === 1 && previous.content === undefined
              ? { content: selected.businessCertificateName } : {}) }));
          if (unavailable) throw new OperationError('预填资质当前不可用，请重新选择。');
        }),
        loadSignatureGroups(client).then(rows => {
          if (!active) return;
          setGroups(rows);
          if (prefill?.subAccounts?.length) {
            const ids = [...new Set(prefill.subAccounts)];
            const available = ids.filter(id => rows.some(row => row.subAccountId === id));
            setValues(previous => ({ ...previous, subAccounts: available }));
            if (available.length !== ids.length) {
              throw new OperationError('部分预填消息组当前不可用，请核对绑定范围。');
            }
          } else if (prefill?.subAccounts === undefined && prefill?.isLimitSubAccount !== 0 && rows.length === 1) {
            setValues(previous => ({ ...previous, subAccounts: [rows[0].subAccountId] }));
            setScope('limited');
          }
        }),
      ]);
      if (!active) return;
      setLoaded(true);
      const failure = results.find(result => result.status === 'rejected');
      if (failure) throw failure.reason;
    });
    return () => { active = false; };
  }, [client]);

  const changePurpose = purpose => {
    if (qualificationLocked) return;
    edit({ purpose, ...(material?.purpose === purpose ? {} : { signatureIdentificationID: undefined }) },
      { invalidateBase: true });
  };
  const selectQualification = id => {
    const next = qualifications.find(row => row.id === id);
    if (!next) { edit({ signatureIdentificationID: undefined }); return; }
    const useFullName = !values.content || values.content === material?.businessCertificateName;
    edit({ signatureIdentificationID: id, purpose: next.purpose,
      ...(values.source === 1 && useFullName ? { content: next.businessCertificateName } : {}) });
  };
  const changeContent = content => edit({ content,
    ...(!qualificationLocked && values.purpose === 2 ? { signatureIdentificationID: undefined } : {}),
  }, { invalidateBase: true });
  const nextStep = () => {
    if (locked) return;
    const errors = signatureBaseErrors(values, scope);
    setFieldErrors(errors);
    if (Object.keys(errors).length) {
      const first = document.querySelector(`[data-validation-field="${Object.keys(errors)[0]}"]`);
      first?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      first?.querySelector('input, textarea, [tabindex]')?.focus();
      return;
    }
    setBaseCompleted(true);
    setPreview(null);
    setStep('materials');
  };
  // MCP 宿主可能禁止原生表单提交；按钮和普通输入框的 Enter 直接触发页面动作。
  const inputEnter = action => event => {
    if (event.key === 'Enter' && !event.nativeEvent.isComposing
      && event.target.tagName === 'INPUT' && !event.target.closest('.arco-select')) {
      event.preventDefault();
      if (!locked) action();
    }
  };
  const saveAttachments = next => {
    attachmentsRef.current = next;
    setAttachments(next);
    setPreview(null);
  };
  const upload = (kind, file, uid) => {
    if (done.current || operation.uncertain) return Promise.reject(new OperationError('本次填写已结束。'));
    const replacement = attachmentsRef.current[kind].some(item => item.uid === uid);
    if (!replacement && Object.values(attachmentsRef.current).flat().length + reservedFiles.current >= maxFiles) {
      const error = new OperationError('本次最多上传 5 份材料。');
      setUploadError(error);
      return Promise.reject(error);
    }
    if (!replacement) reservedFiles.current += 1;
    pendingUploads.current += 1;
    setUploadBusy(true);
    setUploadError(null);
    const task = uploadQueue.current.then(async () => {
      if (done.current) throw new OperationError('本次填写已结束。');
      const uploaded = await client.upload(file, { kind: 'material', category: kind });
      const item = { ...uploaded, uid };
      const current = attachmentsRef.current;
      saveAttachments({ ...current, [kind]: replacement
        ? current[kind].map(previous => previous.uid === uid ? item : previous)
        : [...current[kind], item] });
      return uploaded;
    });
    const settled = task.catch(error => {
      setUploadError(error instanceof OperationError ? error : new OperationError(error.message));
      throw error;
    }).finally(() => {
      if (!replacement) reservedFiles.current -= 1;
      pendingUploads.current -= 1;
      setUploadBusy(pendingUploads.current > 0);
    });
    uploadQueue.current = settled.catch(() => {});
    return settled;
  };
  const fileField = kind => <SignatureUpload key={kind} kind={kind} files={attachments[kind]}
    total={totalFiles} disabled={locked} onUpload={upload}
    onRemove={(category, uid) => {
      if (!locked) saveAttachments({ ...attachmentsRef.current,
        [category]: attachmentsRef.current[category].filter(file => file.uid !== uid) });
    }} />;
  const buildPreview = () => operation.run(() => {
    if (values.subAccounts?.some(id => !groups.some(row => row.subAccountId === id))) {
      throw new OperationError('所选消息组当前不可用，请核对绑定范围。');
    }
    setPreview(signaturePreview(values, material, scope, attachmentsRef.current));
  });
  const submit = confirmedPreview => operation.run(async () => {
    if (done.current || previewRef.current !== confirmedPreview) return;
    let result;
    try {
      result = await client.call('submit_signature', { request: confirmedPreview.request }, { write: true });
    } catch (error) {
      if (error instanceof OperationError && !error.unknown) setPreview(null);
      throw error;
    }
    done.current = true;
    setReceipt({ ...result, signature: confirmedPreview.request.content });
    setPreview(null);
    saveAttachments({ app: [], trademark: [], other: [] });
    await client.report({ form: 'signature', state: 'response_received', applyId: result.applyId, status: result.status });
  }, { mutation: true });
  const confirmRisk = () => {
    const current = preview;
    Modal.confirm({
      title: '确认承担签名报备风险',
      content: '当前签名未连续出现在营业执照企业名称中，可能存在审核或报备失败风险。是否仍要强制提交？',
      okText: '确认承担风险并提交', cancelText: '返回修改',
      onOk: () => submit(current),
    });
  };
  const abandon = () => {
    if (locked) return;
    done.current = true;
    setPreview(null);
    saveAttachments({ app: [], trademark: [], other: [] });
    setValues({});
    setReceipt({ abandoned: true });
    void client.report({ form: 'signature', state: 'abandoned' }).catch(() => {});
  };
  const goBack = () => { if (!locked) { setPreview(null); setStep('base'); } };

  if (!loaded) return <main className="signature-shell">
    <section className="signature-page signature-loading"><Spin tip="正在读取已有资质" /></section>
  </main>;
  if (receipt) return <main className="signature-shell">
    <section className="signature-page signature-result" data-state="completed">
      <div className="signature-result__icon">✓</div>
      <h1>{receipt.abandoned ? '本次填写已结束' : '签名申请已提交'}</h1>
      <p>{receipt.abandoned ? '已清理本次填写的草稿和材料。' : '已取得申请编号，审核与报备结果请继续查询。'}</p>
      {receipt.applyId && <>
        <div className="signature-result__detail"><span>申请编号</span><strong>{String(receipt.applyId)}</strong></div>
        <div className="signature-result__detail"><span>本次请求返回状态</span>
          <strong>{reviewLabels[receipt.status] ?? '待查询'}</strong></div>
        <Button loading={operation.busy} onClick={() => operation.run(async () => {
          setStatuses(page(await client.query('ListSignaturesForAgent', {
            Signature: receipt.signature, ExactMatch: true, Page: 1, PageSize: 100,
          }), signatureSchema).rows);
        })}>刷新审核状态</Button>
        {statuses?.map((row, index) => <div className="signature-result__detail" key={index}>
          <span>{[row.ChannelType, row.Industry].filter(Boolean).join(' · ') || '审核结果'}</span>
          <strong>{row.StatusDescription ?? reviewLabels[row.Status] ?? '未提供'}
            {row.AuditOpinion && <p>{row.AuditOpinion}</p>}</strong>
        </div>)}
      </>}
      <Feedback operation={operation} />
    </section>
  </main>;

  return <main className="signature-shell"><section className="signature-page">
    <header className="signature-header"><div>
      <span className="signature-eyebrow">国内短信</span><h1>创建短信签名</h1>
      <p>签名将显示在短信正文开头，请按实际使用主体填写并提交审核。</p>
    </div><a href={guide} target="_blank" rel="noreferrer">查看签名规范</a></header>
    <nav className="signature-steps" aria-label="申请步骤">
      <button type="button" disabled={locked}
        className={`signature-step is-active${step === 'base' ? ' is-current' : ''}`} onClick={goBack}>
        <span>{baseCompleted ? '✓' : '1'}</span><strong>签名信息</strong>
      </button><i />
      <button type="button" disabled={locked || !baseCompleted}
        className={`signature-step${step === 'materials' ? ' is-active is-current' : ''}`}
        onClick={() => { if (baseCompleted) setStep('materials'); }}>
        <span>2</span><strong>资质材料</strong>
      </button>
    </nav>
    <Feedback operation={operation} />
    {uploadError && <Feedback operation={{ error: uploadError }} />}
    {Object.keys(fieldErrors).length > 0 && <Alert type="error" content="请修正表单中的错误后继续。" />}
    {step === 'base' ? <form onSubmit={event => event.preventDefault()} onKeyDown={inputEnter(nextStep)}>
      <section className="signature-panel">
        <div className="signature-panel__title"><span>01</span>
          <div><h2>签名信息</h2><p>填写签名展示方式和适用范围</p></div></div>
        <div className="signature-grid">
          <SignatureField name="source" label="签名类型" required error={fieldErrors.source}>
            <Select id="signature-source" aria-label="签名类型" value={values.source} disabled={locked}
              placeholder="请选择签名类型" options={sources.map(([value, label]) => ({ value, label }))}
              onChange={source => edit({ source }, { invalidateBase: true })} />
          </SignatureField>
          <SignatureField name="purpose" label="签名归属类型" required error={fieldErrors.purpose}
            help={purposes.find(([value]) => value === values.purpose)?.[2] || '根据签名实际归属企业选择'}>
            <Select id="signature-purpose" aria-label="签名归属类型" value={values.purpose}
              disabled={locked || qualificationLocked} placeholder="请选择签名归属类型"
              options={purposes.map(([value, label]) => ({ value, label }))} onChange={changePurpose} />
          </SignatureField>
        </div>
        <SignatureField name="content" label="签名内容" required error={fieldErrors.content}
          help="请输入 2–25 个字符，建议使用可核验的公司、APP 或商标名称。">
          <Input id="signature-name" name="content" value={values.content || ''} disabled={locked}
            maxLength={25} showWordLimit onChange={changeContent} placeholder="请输入签名内容" />
        </SignatureField>
        <SignatureField label="发送类型" required help="签名审核通过后可用于国内短信的全部发送类型。">
          <div className="signature-static-options">
            {channels.map(([, label]) => <span key={label}>✓ {label}</span>)}
          </div>
        </SignatureField>
        <SignatureField name="groupScope" label="是否限定可使用消息组" required error={fieldErrors.groupScope}>
          <div className="signature-choice-group">
            {[['limited', '是', '仅指定消息组可使用'], ['all', '否', '全部消息组均可使用']].map(([value, label, help]) =>
              <label key={value} className={scope === value ? 'is-selected' : ''}>
                <input type="radio" name="group-scope" checked={scope === value} disabled={locked}
                  onChange={() => {
                    if (locked) return;
                    setScope(value);
                    edit({ isLimitSubAccount: value === 'limited' ? 1 : 0,
                      subAccounts: value === 'all' ? [] : values.subAccounts?.length ? values.subAccounts : undefined },
                    { invalidateBase: true, clearErrors: ['groupScope', 'subAccounts'] });
                  }} />
                <span><strong>{label}</strong><small>{help}</small></span>
              </label>)}
          </div>
        </SignatureField>
        {scope === 'limited' && <SignatureField name="subAccounts" label="允许使用的消息组范围" required error={fieldErrors.subAccounts}>
          <Select id="signature-groups" aria-label="允许使用的消息组范围" mode="multiple"
            value={values.subAccounts || []} disabled={locked} placeholder="请选择消息组"
            options={groups.map(row => ({ label: row.subAccountName || row.subAccountId, value: row.subAccountId }))}
            onChange={subAccounts => edit({ subAccounts: subAccounts.length ? subAccounts : undefined },
              { invalidateBase: true })} />
        </SignatureField>}
        <SignatureField name="desc" label="申请说明" error={fieldErrors.desc}>
          <Input.TextArea id="signature-description" name="desc" value={values.desc || ''} maxLength={300}
            showWordLimit disabled={locked} onChange={desc => edit({ desc }, { invalidateBase: true })}
            placeholder="请输入该签名的使用场景" />
        </SignatureField>
      </section>
      <div className="signature-actions signature-actions--split">
        <Button disabled={locked} onClick={abandon}>放弃本次填写</Button>
        <Button type="primary" htmlType="button" disabled={locked} onClick={nextStep}>下一步</Button>
      </div>
    </form> : <form onSubmit={event => event.preventDefault()} onKeyDown={inputEnter(buildPreview)}>
      <section className="signature-panel">
        <div className="signature-panel__title"><span>02</span>
          <div><h2>资质材料</h2><p>选择企业资质并按签名类型补充证明</p></div></div>
        {values.source === 2 && <div className="signature-subsection">
          <div className="signature-subsection__title"><div>
            <h3>APP ICP 备案信息</h3><p>备案号和附件至少填写一项</p>
          </div><a href={guide} target="_blank" rel="noreferrer">填写说明</a></div>
          <SignatureField label="APP ICP 备案号">
            <Input id="app-number" name="appIcpFilling" value={values.appIcp?.appIcpFilling || ''} disabled={locked}
              onChange={appIcpFilling => edit({ appIcp: { ...values.appIcp, appIcpFilling } })}
              placeholder="请输入 APP ICP 备案号" />
          </SignatureField>
          {fileField('app')}
        </div>}
        {values.source === 3 && <div className="signature-subsection">
          <div className="signature-subsection__title"><div>
            <h3>商标信息</h3><p>商标注册号为必填项</p>
          </div><a href={guide} target="_blank" rel="noreferrer">填写说明</a></div>
          <div className="signature-grid">
            {[['trademarkCn', '商标中文名', 'trademark-cn'], ['trademarkEn', '商标英文名', 'trademark-en']]
              .map(([key, label, id]) => <SignatureField key={key} label={label}>
                <Input id={id} name={key} value={values.trademark?.[key] || ''} disabled={locked}
                  onChange={value => edit({ trademark: { ...values.trademark, [key]: value } })}
                  placeholder={`请输入${label}`} />
              </SignatureField>)}
          </div>
          <SignatureField label="商标注册号" required>
            <Input id="trademark-number" name="trademarkNumber" value={values.trademark?.trademarkNumber || ''}
              disabled={locked} onChange={trademarkNumber => edit({ trademark: { ...values.trademark, trademarkNumber } })}
              placeholder="请输入商标注册号" />
          </SignatureField>
          {fileField('trademark')}
        </div>}
        <SignatureField label="资质" required help={qualificationLocked
          ? '该资质由申请上下文确定，本次不可更换。'
          : '仅展示当前账号下审核通过且与归属类型一致的可用资质。'}>
          <Select id="signature-qualification" aria-label="资质" value={values.signatureIdentificationID}
            disabled={locked || qualificationLocked} allowClear={!qualificationLocked}
            placeholder={values.purpose ? '请选择与归属类型一致的资质' : '请先选择签名归属类型'}
            options={qualificationOptions} onChange={selectQualification} />
        </SignatureField>
        {material && <div className="signature-qualification" data-field="qualification">
          <div><span>资质 ID</span><strong>{material.id}</strong></div>
          <div><span>企业名称</span><strong>{material.businessCertificateName}</strong></div>
          <div><span>资质归属</span><strong>{material.purpose === 1 ? '自用' : '他用'}</strong></div>
          <div><span>资质状态</span><strong className="is-success">审核通过，可用</strong></div>
        </div>}
        {fileField('other')}
        {preview && <section className="signature-preview" aria-label="申请预览">
          <div className="signature-preview__title"><div><span>✓</span>
            <div><h2>请核对本次申请</h2><p>确认无误后提交审核</p></div></div>
            <Button size="small" disabled={locked} onClick={() => setPreview(null)}>返回修改</Button>
          </div>
          <dl className="signature-summary">
            <dt>签名内容</dt><dd>{preview.request.content}</dd>
            <dt>签名类型</dt><dd>{sources.find(([value]) => value === preview.request.source)?.[1]}</dd>
            <dt>签名归属</dt><dd>{preview.request.purpose === 1 ? '自用' : '他用'}</dd>
            <dt>企业资质</dt><dd>{preview.request.signatureIdentificationID}【{preview.businessName}】</dd>
            <dt>发送类型</dt><dd>{channels.map(([, label]) => label).join('、')}</dd>
            <dt>消息组</dt><dd>{preview.request.subAccounts.length
              ? preview.request.subAccounts.map(id => groups.find(row => row.subAccountId === id)?.subAccountName || id).join('、')
              : '全部消息组'}</dd>
            <dt>补充材料</dt><dd>{preview.attachmentNames.join('、') || '未添加'}</dd>
          </dl>
          {preview.nameRisk && <>
            <Alert type="warning" content="当前签名未连续出现在营业执照企业名称中，可能存在审核或报备失败风险，建议修改" />
            <p className="signature-help">当前签名可能存在报备失败风险，建议返回修改；继续提交后仍需审核。</p>
          </>}
        </section>}
      </section>
      <div className="signature-actions signature-actions--split"><div>
        <Button disabled={locked} onClick={goBack}>上一步</Button>
        <Button disabled={locked} onClick={abandon}>放弃本次填写</Button>
      </div>{!preview ? <Button type="primary" htmlType="button" disabled={locked}
        onClick={buildPreview}>核对申请</Button>
        : preview.nameRisk ? <Button type="primary" status="warning" disabled={locked} onClick={confirmRisk}>强制提交</Button>
          : <Button type="primary" disabled={locked} onClick={() => submit(preview)}>确认提交</Button>}
      </div>
    </form>}
  </section></main>;
}
