import React, { useEffect, useLayoutEffect, useRef, useState } from 'react';
import { Alert, Button, Checkbox, Steps } from '@arco-design/web-react';
import { Choice, Confirm, Feedback, Field, Files, LockedFields, Receipt, Summary, maskedIdentifier, useOperation } from './common.jsx';
import { OperationError, checkedTicket, page, required } from './client.js';
import { materialFile } from './signature.jsx';
import config from '../../src/mcp_server_sms/form_config.json';

const stepTitles = ['基础与企业信息', '人员信息', '授权与补充材料', '确认提交'];
const rankFields = ['isOnlyTwoElement', 'isSkipOtherUse', 'needOtherUseCheck', 'operatorThreeElement', 'needOperatorImage', 'needOperatorMobile', 'responsibleThreeElement', 'needResponsibleImage', 'needResponsibleMobile', 'needBusinessCertificateImage'];
const roleLabels = { operator: '经办人', responsible: '责任人', legal: '法人' };
const personFiles = { operator: [8, 9], responsible: [10, 11], legal: [18, 19] };
const legalFiles = { 1: 12, 2: 13, 3: 14, 4: 15, 9: 6 };
const certificateTypes = [[0, '居民身份证'], [1, '护照'], [2, '港澳居民来往内地通行证'], [3, '台湾居民来往大陆通行证'], [4, '港澳台居民居住证'], [9, '其他']];
const initialValues = () => ({ purpose: 1, sameOperator: true, includeLegal: false, business: { businessCertificateType: 1 }, operator: { certificateType: 0 }, responsible: { certificateType: 0 }, legal: { certificateType: 0 } });
const businessFields = [['businessCertificateName', '企业名称'], ['unifiedSocialCreditIdentifier', '统一社会信用代码'], ['legalPersonName', '法人姓名'], ['businessCertificateValidityPeriodStart', '证件有效期开始'], ['businessCertificateValidityPeriodEnd', '证件有效期结束（长期请填写“长期”）']];

function personPayload(person, role, files) {
  const value = { certificateType: person.certificateType, personName: person.personName ?? '', personIDCard: person.personIDCard ?? '',
    ...(person.personMobile !== undefined ? { personMobile: person.personMobile } : {}) };
  if (person.certificateType === 0 && files.front && files.back) value.personCertificate = [materialFile(files.front, personFiles[role][0]), materialFile(files.back, personFiles[role][1])];
  if (person.certificateType !== 0 && files.document) value.personCertificate = [materialFile(files.document, legalFiles[person.certificateType])];
  return value;
}

export function qualificationPayload(values, files, tickets, verified, rank, account) {
  if (!rank || rankFields.some(key => typeof rank[key] !== 'boolean')) throw new OperationError('尚未取得完整的材料要求，请刷新表单。');
  businessFields.forEach(([key, label]) => required(values.business[key], `请填写${label}。`));
  const materialName = values.materialName || values.business.businessCertificateName;
  if (materialName.length > 20) throw new OperationError('资质名称最多 20 字，请单独填写一个简短名称。');
  required(tickets.business, '请先完成企业信息校验。');
  if (rank.needBusinessCertificateImage && !files.business) throw new OperationError('当前账号需要上传营业证件。');
  for (const role of ['operator', 'responsible']) {
    const actual = role === 'responsible' && values.sameOperator ? 'operator' : role;
    const person = values[actual];
    const pictures = files[actual] ?? {};
    if (Boolean(pictures.front) !== Boolean(pictures.back)) throw new OperationError(`请补齐${roleLabels[actual]}身份证正反面，或同时移除。`);
    required(person.personName, `请填写${roleLabels[actual]}姓名。`); required(person.personIDCard, `请填写${roleLabels[actual]}身份证号。`);
    required(tickets[actual], `请完成${roleLabels[actual]}信息校验。`);
    const suffix = role === 'operator' ? 'Operator' : 'Responsible';
    if (rank['need' + suffix + 'Image'] && (!files[actual]?.front || !files[actual]?.back)) throw new OperationError(`请上传${roleLabels[actual]}身份证正反面。`);
    if (rank['need' + suffix + 'Mobile'] || rank[role + 'ThreeElement']) required(person.personMobile, `请填写${roleLabels[actual]}手机号。`);
    if (account.userType === 'smb' && person.personMobile && verified[actual] !== person.personMobile) throw new OperationError(`请完成${roleLabels[actual]}手机号验证。`);
  }
  if (values.purpose === 2 && rank.needOtherUseCheck && !files.authorization) throw new OperationError('请上传他用授权委托书。');
  const legalEntered = values.includeLegal && Boolean(values.legal.personName || values.legal.personIDCard || values.legal.personMobile || files.legal?.front || files.legal?.back || files.legal?.document);
  if (legalEntered) {
    required(values.legal.personName, '请填写法人姓名。');
    if (values.legal.certificateType === 0) {
      if (Boolean(files.legal?.front) !== Boolean(files.legal?.back)) throw new OperationError('请补齐法人身份证正反面，或同时移除。');
      if (values.legal.personIDCard) required(tickets.legal, '请完成法人信息校验。');
    }
  }
  const businessInfo = { ...values.business };
  if (files.business) businessInfo.businessCertificate = materialFile(files.business, values.business.businessCertificateType);
  const body = {
    purpose: values.purpose, materialName, sameOperator: values.sameOperator, businessInfo,
    operatorPerson: personPayload(values.operator, 'operator', files.operator ?? {}),
    responsiblePersonInfo: personPayload(values[values.sameOperator ? 'operator' : 'responsible'], 'responsible', files[values.sameOperator ? 'operator' : 'responsible'] ?? {}),
    businessCheckTicket: tickets.business, operatorCheckTicket: tickets.operator, responsibleCheckTicket: tickets[values.sameOperator ? 'operator' : 'responsible'],
    otherMaterials: (files.other ?? []).map(file => materialFile(file, 6)),
  };
  if (values.purpose === 2) {
    body.authorizer = values.business.businessCertificateName;
    body.authorizee = required(account.businessName, '当前账号主体信息缺失。');
    if (files.authorization) body.powerOfAttorney = [materialFile(files.authorization, 5)];
  }
  if (legalEntered) {
    body.legalPerson = personPayload(values.legal, 'legal', files.legal ?? {});
    if (tickets.legal) body.legalCheckTicket = tickets.legal;
  }
  return body;
}

export function QualificationForm({ client }) {
  const [values, setValues] = useState(initialValues);
  const [rank, setRank] = useState(null);
  const [account, setAccount] = useState(null);
  const [files, setFiles] = useState({ other: [] });
  const [tickets, setTickets] = useState({});
  const [codes, setCodes] = useState({});
  const [verified, setVerified] = useState({});
  const [sentAt, setSentAt] = useState({});
  const [step, setStep] = useState(0);
  const [snapshot, setSnapshot] = useState(null);
  const [receipt, setReceipt] = useState(null);
  const [status, setStatus] = useState(null);
  const operation = useOperation();
  const stepHeading = useRef(null);
  const previousStep = useRef(step);
  useLayoutEffect(() => {
    const advanced = step > previousStep.current;
    previousStep.current = step;
    const heading = stepHeading.current;
    if (!advanced || !heading) return;
    heading.focus({ preventScroll: true });
    heading.scrollIntoView({ block: 'start', inline: 'nearest' });
  }, [step]);
  useEffect(() => { operation.run(async () => {
    const requirements = await client.call('get_qualification_requirements');
    if (rankFields.some(key => typeof requirements?.[key] !== 'boolean')) throw new OperationError('材料要求返回不完整，暂不能提交。');
    const identity = await client.call('get_account_information');
    if (typeof identity?.businessName !== 'string' || typeof identity?.userType !== 'string') throw new OperationError('账号主体信息不完整，暂不能提交。');
    setRank(requirements); setAccount(identity);
  }); }, [client]);
  const updateBase = (key, value) => setValues(current => ({ ...current, [key]: value }));
  const updateSection = (section, key, value) => {
    setValues(current => ({ ...current, [section]: { ...current[section], [key]: value } }));
    setTickets(current => ({ ...current, [section]: undefined }));
    if (key === 'personMobile') setVerified(current => ({ ...current, [section]: undefined }));
    if (key === 'certificateType') setFiles(current => ({ ...current, [section]: {} }));
  };
  const upload = (slot, selected, { role, side, category = 'identity', many = false } = {}) => operation.run(async () => {
    if (many && (files.other.length + selected.length > 5)) throw new OperationError('其他材料最多 5 张。');
    for (const file of selected) {
      const result = await client.upload(file, { kind: 'material', category });
      setFiles(current => role ? { ...current, [role]: { ...current[role], [side]: result } }
        : { ...current, [slot]: many ? [...current.other, result] : result });
    }
    setTickets(current => ({ ...current, [role ?? slot]: undefined }));
  }, { mutation: true });
  const removeFile = (slot, role, side, index) => {
    setFiles(current => role ? { ...current, [role]: { ...current[role], [side]: undefined } }
      : { ...current, [slot]: slot === 'other' ? current.other.filter((_, i) => i !== index) : undefined });
    setTickets(current => ({ ...current, [role ?? slot]: undefined }));
  };
  const fileArea = (label, slot, options = {}) => {
    const selected = options.role ? files[options.role]?.[options.side] : files[slot];
    return <Files label={label} accept=".jpg,.jpeg,.png" value={Array.isArray(selected) ? selected : selected ? [selected] : []}
      multiple={options.many} disabled={operation.busy || operation.uncertain} onSelect={selected => upload(slot, selected, options)}
      onRemove={index => removeFile(slot, options.role, options.side, index)} />;
  };
  const businessOcr = () => operation.run(async () => {
    required(files.business, '请先上传营业证件。');
    const result = await client.call('recognize_qualification_document', { business_certificate_type: values.business.businessCertificateType, certificate: files.business.fileContent, private: true });
    const extracted = Object.fromEntries(businessFields.filter(([key]) => typeof result?.[key] === 'string').map(([key]) => [key, result[key]]));
    setValues(current => ({ ...current, business: { ...current.business, ...extracted } }));
    setTickets(current => ({ ...current, business: undefined }));
  });
  const personOcr = role => operation.run(async () => {
    const material = files[role]; required(material?.front, '请上传身份证人像面。'); required(material?.back, '请上传身份证国徽面。');
    const result = await client.call('recognize_qualification_document', { id_card_front_image: material.front.fileContent, id_card_back_image: material.back.fileContent, private: true });
    const extracted = Object.fromEntries(['personName', 'personIDCard'].filter(key => typeof result?.[key] === 'string').map(key => [key, result[key]]));
    setValues(current => ({ ...current, [role]: { ...current[role], ...extracted } }));
    setTickets(current => ({ ...current, [role]: undefined }));
  });
  const check = role => operation.run(async () => {
    const person = values[role];
    const business = values.business;
    let result;
    if (role === 'business') {
      result = await client.call('check_qualification_enterprise', {
        business_certificate_name: required(business.businessCertificateName, '请输入企业名称。'),
        unified_social_credit_identifier: required(business.unifiedSocialCreditIdentifier, '请输入社会信用代码。'),
        legal_person_name: required(business.legalPersonName, '请输入法人姓名。'), private: true,
      });
    } else {
      const needsPhone = role !== 'legal' && (rank?.[role + 'ThreeElement'] || role === 'operator' && values.sameOperator && rank?.responsibleThreeElement);
      result = await client.call('check_qualification_person', {
        person_name: required(person.personName, '请输入姓名。'), person_id_card: required(person.personIDCard, '请输入证件号码。'),
        ...(needsPhone ? { person_mobile: required(person.personMobile, '当前校验需要手机号。') } : {}), private: true,
      });
    }
    setTickets(current => ({ ...current, [role]: checkedTicket(result) }));
  });
  const verifyMobile = (role, send) => operation.run(async () => {
    const mobile = required(values[role].personMobile, '请输入手机号。');
    if (send && sentAt[role] && Date.now() - sentAt[role] < 60000) throw new OperationError('请等待 60 秒后再获取验证码。');
    const result = await client.call(send ? 'send_verification_code' : 'verify_code', {
      app_id: config.qualificationVerification.appId, scene: config.qualificationVerification.scene, mobile,
      ...(send ? { template_id: config.qualificationVerification.templates[role], code_type: 0, channel_id: config.qualificationVerification.channelId }
        : { code: required(codes[role], '请输入收到的验证码。'), function: 2 }),
    }, { write: true });
    if (send) setSentAt(current => ({ ...current, [role]: Date.now() }));
    else {
      if (result?.status !== 0) throw new OperationError('验证码未通过或已过期，请核对后重新获取。');
      setVerified(current => ({ ...current, [role]: mobile }));
    }
  }, { mutation: true });
  const prepare = () => operation.run(() => { setSnapshot(qualificationPayload(values, files, tickets, verified, rank, account)); setStep(3); });
  const submit = () => operation.run(async () => {
    const id = await client.call('apply_qualification', { request: snapshot }, { write: true });
    setReceipt(id); setSnapshot(null); setValues(initialValues()); setTickets({}); setCodes({}); setVerified({}); setFiles({ other: [] });
    await client.report({ form: 'qualification', state: 'submitted', qualificationId: id });
  }, { mutation: true });
  const personSection = role => <section className="step-section" key={role}>
    <h3>{roleLabels[role]}信息</h3><div className="form-grid">
      {role === 'legal' && <Choice label="法人证件类型" value={values.legal.certificateType} onChange={value => updateSection('legal', 'certificateType', value)} options={certificateTypes} />}
      {[['personName', '姓名'], ['personIDCard', '证件号码'], ['personMobile', '手机号']].map(([key, label]) =>
        <Field key={key} label={roleLabels[role] + label} value={values[role][key]} onChange={value => updateSection(role, key, value)} required={role !== 'legal' && key !== 'personMobile'} />)}
    </div>
    <div className="form-grid person-upload-grid">{values[role].certificateType === 0 ? <>
      {fileArea(`${roleLabels[role]}身份证人像面`, null, { role, side: 'front' })}
      {fileArea(`${roleLabels[role]}身份证国徽面`, null, { role, side: 'back' })}
    </> : fileArea('法人证件图片', null, { role, side: 'document' })}</div>
    <div className="sms-check">{values[role].certificateType === 0 && <><Button disabled={operation.busy || operation.uncertain} onClick={() => personOcr(role)}>识别证件并回填</Button>
      <Button disabled={operation.busy || operation.uncertain} onClick={() => check(role)}>校验{roleLabels[role]}信息</Button><span>{tickets[role] ? '校验已通过' : '信息修改后需重新校验'}</span></>}</div>
    {role !== 'legal' && account?.userType === 'smb' && values[role].personMobile && <div className="mobile-verification">
      <p>短信验证码仅发送到本页填写的手机号。</p><Field label={`${roleLabels[role]}短信验证码`} value={codes[role]} onChange={value => setCodes(current => ({ ...current, [role]: value }))} />
      <div className="sms-check"><Button disabled={operation.busy || operation.uncertain} onClick={() => verifyMobile(role, true)}>获取验证码</Button>
        <Button disabled={operation.busy || operation.uncertain} onClick={() => verifyMobile(role, false)}>验证手机号</Button>
        {verified[role] === values[role].personMobile && <span>手机号已验证</span>}
      </div>
    </div>}
  </section>;

  return <LockedFields locked={operation.busy || operation.uncertain}><main className="wizard-page"><header className="wizard-header"><div className="wizard-header-inner">
    <div className="wizard-brand">火山引擎 · 短信服务</div><h1 className="wizard-title">申请短信资质</h1>
    <p className="wizard-subtitle">在页面填写和核对材料。提交申请后，仍需等待资质审核。</p>
  </div></header><div className="wizard-body"><Feedback operation={operation} />
    {receipt ? <div className="wizard-content"><Receipt title="资质申请已提交" id={receipt}><Button loading={operation.busy}
      onClick={() => operation.run(async () => setStatus(page(await client.call('list_qualifications', { qualification_id: receipt })).rows))}>刷新审核状态</Button>
      {status?.map(row => <Summary key={row.id} items={[[row.materialName ?? '资质', ({ 1: '审核中', 2: '审核未通过', 3: '审核通过' })[row.auditStatus] ?? '待核对'], ['审核意见', row.reason ?? row.auditOpinion ?? '未提供']]} />)}
    </Receipt></div> : <div className="wizard-workspace"><aside className="wizard-sidebar"><div className="wizard-sidebar-title">办理步骤</div>
      <Steps direction="vertical" current={step + 1} size="small">{stepTitles.map(title => <Steps.Step key={title} title={title} />)}</Steps>
    </aside><div className="wizard-content">
      <div className="sms-mobile-step">第 {step + 1} / 4 步</div>
      {!rank || !account ? <p>正在读取当前账号的材料要求…</p> : snapshot ? <Confirm title="确认本次资质申请" onBack={() => { setSnapshot(null); setStep(2); }} onSubmit={submit} busy={operation.busy} disabled={operation.uncertain}>
        <Summary items={[
          ['资质名称', snapshot.materialName], ['用途', snapshot.purpose === 1 ? '自用' : '他用'],
          ['企业名称', snapshot.businessInfo.businessCertificateName], ['统一社会信用代码', snapshot.businessInfo.unifiedSocialCreditIdentifier],
          ['法人姓名', snapshot.businessInfo.legalPersonName], ['经办人', snapshot.operatorPerson.personName],
          ['经办人证件', maskedIdentifier(snapshot.operatorPerson.personIDCard)], ['经办人手机', maskedIdentifier(snapshot.operatorPerson.personMobile)],
          ['责任人', snapshot.responsiblePersonInfo.personName], ['责任人证件', maskedIdentifier(snapshot.responsiblePersonInfo.personIDCard)],
          ['责任人手机', maskedIdentifier(snapshot.responsiblePersonInfo.personMobile)],
          ['证件与授权材料', [files.business, files.authorization, ...Object.values(files.operator ?? {}), ...Object.values(files.responsible ?? {}), ...Object.values(files.legal ?? {}), ...files.other].filter(Boolean).map(file => file.name).join('、') || '未添加'],
          ...(snapshot.legalPerson ? [['法人补充证件', maskedIdentifier(snapshot.legalPerson.personIDCard)]] : []),
        ]} />
      </Confirm> : <>
        <div className="step-heading"><h2 ref={stepHeading} tabIndex={-1}>{stepTitles[step]}</h2></div>
        {step === 0 && <><div className="form-grid">
          <Field label="资质名称（选填，最多 20 字）" value={values.materialName} onChange={value => updateBase('materialName', value)} maxLength={20} placeholder="留空时使用企业名称" />
          <Choice label="资质用途" value={values.purpose} onChange={value => updateBase('purpose', value)} options={[[1, '自用'], [2, '他用']]} />
          <Choice label="营业证件类型" value={values.business.businessCertificateType} onChange={value => updateSection('business', 'businessCertificateType', value)} options={[[1, '企业营业执照'], [4, '社会信用代码证书'], [7, '事业单位法人证书'], [6, '其他']]} />
        </div><p>当前账号主体：{account.businessName}。营业证件照片{rank.needBusinessCertificateImage ? '必填' : '选填'}。</p>
          {fileArea('营业证件', 'business', { category: 'business' })}<Button disabled={operation.busy || operation.uncertain} onClick={businessOcr}>识别营业证件并回填</Button>
          <div className="form-grid">{businessFields.map(([key, label]) => <Field key={key} label={label} value={values.business[key]} onChange={value => updateSection('business', key, value)} required />)}</div>
          <div className="sms-check"><Button disabled={operation.busy || operation.uncertain} onClick={() => check('business')}>校验企业信息</Button>{tickets.business && <span>校验已通过</span>}</div>
        </>}
        {step === 1 && <>
          <Alert content={`经办人照片${rank.needOperatorImage ? '必填' : '选填'}、手机号${rank.needOperatorMobile || rank.operatorThreeElement ? '必填' : '选填'}；独立责任人照片${rank.needResponsibleImage ? '必填' : '选填'}、手机号${rank.needResponsibleMobile || rank.responsibleThreeElement ? '必填' : '选填'}。`} />
          {personSection('operator')}<Checkbox disabled={operation.busy || operation.uncertain} checked={values.sameOperator} onChange={value => { updateBase('sameOperator', value); setTickets(current => ({ ...current, operator: undefined, responsible: undefined })); }}>责任人与经办人相同</Checkbox>
          {!values.sameOperator && personSection('responsible')}
          <div className="step-section"><Checkbox disabled={operation.busy || operation.uncertain} checked={values.includeLegal} onChange={value => updateBase('includeLegal', value)}>补充法人证件信息（选填）</Checkbox>{values.includeLegal && personSection('legal')}</div>
        </>}
        {step === 2 && <>
          {values.purpose === 2 && <><Summary items={[["授权方", values.business.businessCertificateName], ["被授权方", account.businessName]]} />
            {rank.needOtherUseCheck && fileArea('授权委托书（必填）', 'authorization', { category: 'authorization' })}</>}
          {fileArea('其他材料（选填，最多 5 张）', 'other', { category: 'business', many: true })}
        </>}
        <div className="step-actions">{step > 0 && <Button disabled={operation.busy} onClick={() => setStep(step - 1)}>上一步</Button>}
          {step < 2 ? <Button type="primary" disabled={operation.busy || operation.uncertain} onClick={() => setStep(step + 1)}>下一步</Button>
            : <Button type="primary" loading={operation.busy} disabled={operation.uncertain} onClick={prepare}>核对申请信息</Button>}
        </div>
      </>}
    </div></div>}
  </div></main></LockedFields>;
}
