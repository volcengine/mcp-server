import React, { useEffect, useRef, useState } from 'react';
import { Alert, Button, Input, Modal, Radio, Select, Table } from '@arco-design/web-react';
import { IconPlus } from '@arco-design/web-react/icon';
import { Choice, Confirm, Feedback, Field, LockedFields, Receipt, Summary, useOperation } from './common.jsx';
import { OperationError, page } from './client.js';
import { signatureSchema, templatePreviewSchema } from './contracts.js';
import { templateVariables } from './template-variables.js';

const channels = [['CN_OTP', '验证码'], ['CN_NTC', '通知'], ['CN_MKT', '营销']];
const parameterTypes = [[1, '普通变量'], [2, '链接'], [3, '电话号码'], [4, '链接路径'], [5, '超级变量']];
const selectableParameterTypes = parameterTypes.filter(([kind]) => kind !== 5);
const maxTemplateVariables = 20;
const marketingUnsubscribeSuffix = '拒收请回复R';
const defaultShortUrlConfig = { isEnabled: '0', belong: 'DEFAULT', isNeedClickDetails: '0', uaCheckStrategy: 0 };

export function templatePayload(values) {
  if (!values.name) throw new OperationError('请填写模版名称。', { field: 'name' });
  if (!values.content) throw new OperationError('请填写模版内容。', { field: 'content' });
  if (values.name.length > 50) throw new OperationError('模版名称最多 50 字符。', { field: 'name' });
  if ((values.desc?.length ?? 0) > 300) throw new OperationError('模版用途最多 300 字符。', { field: 'desc' });
  if (new TextEncoder().encode(values.name).length > 100) throw new OperationError('模版名称不能超过 100 个字节。', { field: 'name' });
  if (!channels.some(([kind]) => kind === values.channelType)) throw new OperationError('请选择模版类型。', { field: 'channelType' });
  if (!values.signatures?.length) throw new OperationError('请至少选择一个签名。', { field: 'signatures' });
  let occurrences;
  try {
    occurrences = templateVariables(values.content);
  } catch (cause) {
    if (cause instanceof OperationError) cause.field = 'content';
    throw cause;
  }
  const names = [...new Set(occurrences)];
  if (names.some(name => name.toLowerCase() === 'volc_sms_url_token')) {
    throw new OperationError('不能使用保留变量名 volc_sms_url_token。', { field: 'content' });
  }
  const params = values.templateParams ?? [];
  if (new Set(params.map(row => row.name)).size !== params.length || params.length !== names.length
    || params.some(row => !names.includes(row.name) || !parameterTypes.some(([kind]) => row.paramType === kind))) {
    throw new OperationError('正文变量与变量设置必须一一对应，请明确选择每个变量的类型。', { field: 'templateParams' });
  }
  if (values.channelType === 'CN_OTP' && (occurrences.length !== 1 || params.length !== 1 || params[0].paramType !== 1)) {
    throw new OperationError('验证码模板需要一个普通变量。', { field: 'templateParams' });
  }
  if (values.channelType === 'CN_OTP') {
    if (!/验证码|code\s|code\s+is|注册码|校验码|动态码|动态密码/.test(values.content)) {
      throw new OperationError('验证码正文需要包含验证码、注册码、校验码、动态码、动态密码或 code。', { field: 'content' });
    }
    if (values.templateTrafficDriving?.length) throw new OperationError('验证码模板不支持引流绑定。', { field: 'templateTrafficDriving' });
  } else {
    const matches = [...values.content.matchAll(/\$\{([^{}]*)\}/g)];
    if (matches.some((match, index) => index && matches[index - 1].index + matches[index - 1][0].length === match.index)) {
      throw new OperationError('通知和营销模板不支持相邻占位符，请保留分隔内容。', { field: 'content' });
    }
    if (occurrences.length > maxTemplateVariables) {
      throw new OperationError(`每个通知或营销模板最多包含 ${maxTemplateVariables} 个变量占位符。`, { field: 'content' });
    }
  }
  if (values.channelType === 'CN_MKT' && !values.content.endsWith(marketingUnsubscribeSuffix)) {
    throw new OperationError(`营销模板末尾必须为“${marketingUnsubscribeSuffix}”。`, { field: 'content' });
  }
  const config = values.shortUrlConfig;
  for (const key of ['isEnabled', 'isNeedClickDetails']) {
    if (config?.[key] !== undefined && !['0', '1'].includes(config[key])) {
      throw new OperationError('短链开关必须为字符串 0 或 1。', { field: 'shortUrlConfig' });
    }
  }
  if (config?.isEnabled === '1' && values.channelType !== 'CN_MKT') throw new OperationError('平台短链只适用于营销短信。', { field: 'shortUrlConfig' });
  if (config?.uaCheckStrategy !== undefined && !Number.isInteger(config.uaCheckStrategy)) throw new OperationError('访问校验策略应为整数。', { field: 'shortUrlConfig' });
  const traffic = params.filter(row => [2, 3].includes(row.paramType));
  if ([[2, 1], [3, 2], [4, 1]].some(([kind, maximum]) => params.filter(row => row.paramType === kind).length > maximum)) {
    throw new OperationError('包含固定内容在内，最多 1 个链接、2 个联系号码和 1 个链接 Path。', { field: 'templateParams' });
  }
  const combinations = values.templateTrafficDriving ?? [];
  if (traffic.length && !combinations.length) throw new OperationError('请添加引流信息并选择对应的链接或号码。', { field: 'templateTrafficDriving' });
  for (const group of combinations) {
    if (!group.length || group.length !== traffic.length || new Set(group.map(row => row.name)).size !== group.length
      || group.some(row => !traffic.some(item => item.name === row.name && item.paramType === row.paramType)
        || !(Number.isInteger(row.id) && row.id > 0))) {
      throw new OperationError('每组引流信息需完整覆盖对应变量，并选择引流信息库中的链接或号码。', { field: 'templateTrafficDriving' });
    }
  }
  return { name: values.name, content: values.content, channelType: values.channelType,
    signatures: [...values.signatures], ...(values.subAccounts !== undefined ? { subAccounts: [...values.subAccounts] } : {}),
    templateParams: params.map(row => ({ ...row })),
    ...(values.desc !== undefined ? { desc: values.desc } : {}), ...(values.project !== undefined ? { project: values.project } : {}),
    ...(config ? { shortUrlConfig: { ...config } } : {}),
    ...(combinations.length ? { templateTrafficDriving: combinations.map(rows => rows.map(row => ({ ...row }))) } : {}) };
}

function sameValue(left, right) {
  if (left === right) return true;
  if (!left || !right || typeof left !== 'object' || typeof right !== 'object') return false;
  const keys = Object.keys(left).filter(key => left[key] !== undefined);
  const other = Object.keys(right).filter(key => right[key] !== undefined);
  return keys.length === other.length && keys.every(key => Object.hasOwn(right, key) && sameValue(left[key], right[key]));
}

export function checkedTemplatePreview(result, request) {
  if (!templatePreviewSchema.safeParse(result).success) throw new OperationError('模板核对结果不完整，请重新核对。');
  // 服务端只可给显式资源 ID 补齐原始内容；已填写的字段必须与本次请求一致。
  const comparable = { ...result.request };
  if (request.templateTrafficDriving) comparable.templateTrafficDriving = result.request.templateTrafficDriving?.map((rows, group) =>
    rows.map((row, index) => {
      const original = request.templateTrafficDriving[group]?.[index];
      const copy = { ...row };
      if (original?.id && !original.content) delete copy.content;
      return copy;
    }));
  delete comparable.area;
  if (!sameValue(request, comparable)) throw new OperationError('模板核对结果与填写内容不一致，请重新核对。');
  return result;
}

function CatalogMore({ loaded, total, ...props }) {
  return loaded < total && <Button type="text" {...props}>加载更多</Button>;
}

function parametersFromContent(content, previous) {
  try {
    return [...new Set(templateVariables(content))].map(name =>
      previous.find(row => row.name === name) ?? { name, paramType: 1 });
  } catch (cause) {
    // 输入占位符的中间状态不报错、不丢失已选类型；核对时仍严格校验正文。
    if (cause instanceof OperationError) return previous;
    throw cause;
  }
}

function trafficParameters(params) {
  return params.filter(row => [2, 3].includes(row.paramType));
}

function syncTrafficBindings(params, groups) {
  const traffic = trafficParameters(params);
  return groups.map(rows => traffic.map(parameter => {
    const current = rows.find(row => row.name === parameter.name && row.paramType === parameter.paramType);
    return current ? { ...current } : { name: parameter.name, paramType: parameter.paramType };
  })).filter(rows => rows.length);
}

function resourceLabel(row, traffic) {
  const source = row.paramType === 2 ? traffic.links : traffic.phones;
  const item = source.find(resource => resource.id === row.id);
  return row.content ?? item?.link ?? item?.jumpLink ?? item?.number ?? (row.id ? `引流信息 ${row.id}` : '-');
}

function bindingContent(content, rows, traffic) {
  return rows.reduce((result, row) =>
    result.replace(new RegExp(`\\$\\{${row.name}\\}`, 'g'), resourceLabel(row, traffic)), content);
}

function trafficCombinations(params, selections) {
  return params.reduce((groups, parameter) => groups.flatMap(rows =>
    (selections[parameter.name] ?? []).map(id => [...rows, {
      name: parameter.name, paramType: parameter.paramType, id,
    }])), [[]]);
}

export function TemplateForm({ client, prefill }) {
  const [values, setValues] = useState(() => {
    const parsedParams = parametersFromContent(
      prefill?.content ?? '', prefill?.templateParams?.map(row => ({ ...row })) ?? [],
    );
    const templateParams = prefill?.channelType === 'CN_OTP'
      ? parsedParams.map(row => ({ ...row, paramType: 1 }))
      : parsedParams;
    return { ...prefill, signatures: prefill?.signatures ?? [], templateParams,
      templateTrafficDriving: prefill?.channelType === 'CN_OTP' ? []
        : prefill?.templateTrafficDriving?.map(rows => rows.map(row => ({ ...row }))) ?? [],
      shortUrlConfig: prefill?.channelType === 'CN_MKT'
        ? { ...defaultShortUrlConfig, ...prefill?.shortUrlConfig } : undefined };
  });
  const [signatures, setSignatures] = useState({ rows: [], total: 0, page: 0 });
  const [traffic, setTraffic] = useState({ links: [], phones: [] });
  const [trafficEditorOpen, setTrafficEditorOpen] = useState(false);
  const [trafficSelections, setTrafficSelections] = useState({});
  const [trafficEditorError, setTrafficEditorError] = useState('');
  const loadedTrafficMode = useRef(null);
  const [snapshot, setSnapshot] = useState(null);
  const [receipt, setReceipt] = useState(null);
  const [status, setStatus] = useState(null);
  const [fieldErrors, setFieldErrors] = useState({});
  const form = useRef(null);
  const operation = useOperation();
  const trafficOperation = useOperation();
  const loadedScope = useRef(null);
  const initialSignatures = useRef(prefill?.signatures ?? []);
  const clearFieldError = key => setFieldErrors(current => {
    if (!current[key]) return current;
    const next = { ...current }; delete next[key]; return next;
  });
  const update = (key, value) => {
    clearFieldError(key);
    if (key === 'content') {
      clearFieldError('templateParams');
      clearFieldError('templateTrafficDriving');
    }
    setValues(current => {
    if (key !== 'content') return { ...current, [key]: value };
    const templateParams = parametersFromContent(value, current.templateParams);
    return { ...current, content: value, templateParams,
      templateTrafficDriving: syncTrafficBindings(templateParams, current.templateTrafficDriving) };
    });
  };
  const signatureScope = { ...(values.subAccounts?.length ? { SubAccounts: values.subAccounts } : {}),
    ...(values.channelType ? { ChannelTypes: [values.channelType] } : {}), Statuses: [3, 5] };
  const loadSignatures = async (next = 1) => {
    const result = page(await client.query('ListSignaturesForAgent', { ...signatureScope, Page: next, PageSize: 100 }), signatureSchema);
    const rows = [...result.rows];
    if (next === 1) {
      for (const name of initialSignatures.current) {
        if (rows.some(row => row.Signature === name)) continue;
        const match = page(await client.query('ListSignaturesForAgent', { ...signatureScope, Signature: name, ExactMatch: true, Page: 1, PageSize: 100 }), signatureSchema)
          .rows.find(row => row.Signature === name);
        if (!match) throw new OperationError('预填签名当前不可用，请重新选择。');
        rows.push(match);
      }
      initialSignatures.current = [];
    }
    setSignatures(current => ({ rows: next === 1 ? rows : [...current.rows, ...rows], total: result.total, page: next }));
  };
  const scopeKey = JSON.stringify([values.subAccounts, values.channelType]);
  useEffect(() => {
    if (operation.busy || loadedScope.current === scopeKey) return;
    loadedScope.current = scopeKey;
    operation.run(() => loadSignatures(1));
  }, [scopeKey, operation.busy]);
  const changeChannel = value => {
    clearFieldError('channelType'); clearFieldError('templateParams');
    clearFieldError('templateTrafficDriving'); clearFieldError('shortUrlConfig');
    // 补齐未知类型时保留预填签名并重新核实；更换已确定类型才清除旧选择。
    const hadType = values.channelType !== undefined;
    initialSignatures.current = hadType ? [] : [...values.signatures];
    setSignatures({ rows: [], total: 0, page: 0 });
    setValues(current => {
      const templateParams = value === 'CN_OTP'
        ? current.templateParams.map(row => ({ ...row, paramType: 1 }))
        : current.templateParams;
      return { ...current, channelType: value, signatures: hadType ? [] : current.signatures,
        templateParams,
        templateTrafficDriving: value === 'CN_OTP' ? [] : syncTrafficBindings(templateParams, current.templateTrafficDriving),
        shortUrlConfig: value === 'CN_MKT'
          ? current.shortUrlConfig ?? { ...defaultShortUrlConfig } : undefined };
    });
  };
  const editParameter = (index, value) => {
    clearFieldError('templateParams'); clearFieldError('templateTrafficDriving');
    setValues(current => {
    const templateParams = current.templateParams.map((row, i) => i === index ? { ...row, paramType: value } : row);
    return { ...current, templateParams,
      templateTrafficDriving: syncTrafficBindings(templateParams, current.templateTrafficDriving) };
    });
  };
  const fetchTraffic = async () => {
    const useVolcLink = values.shortUrlConfig?.isEnabled === '1';
    const links = await client.query('GetTobTrafficDrivingLinkListForAgent', { useVolcLink });
    const phones = await client.query('GetTobTrafficDrivingPhoneListForAgent');
    const linkRows = links?.list ?? links?.List; const phoneRows = phones?.list ?? phones?.List;
    if (!Array.isArray(linkRows) || !Array.isArray(phoneRows)) throw new OperationError('引流信息列表不完整，请稍后重试。');
    setTraffic({ links: linkRows, phones: phoneRows });
    loadedTrafficMode.current = useVolcLink;
  };
  const openTrafficEditor = () => trafficOperation.run(async () => {
    await fetchTraffic();
    setTrafficSelections({}); setTrafficEditorError(''); setTrafficEditorOpen(true);
  });
  useEffect(() => {
    const mode = values.shortUrlConfig?.isEnabled === '1';
    if (prefill?.templateTrafficDriving?.length && !trafficOperation.busy && loadedTrafficMode.current !== mode) {
      loadedTrafficMode.current = mode;
      trafficOperation.run(fetchTraffic);
    }
  }, [trafficOperation.busy, values.shortUrlConfig?.isEnabled]);
  const saveTrafficEditor = () => {
    const params = trafficParameters(values.templateParams);
    if (params.some(row => !trafficSelections[row.name]?.length)) {
      setTrafficEditorError('请为每个引流变量至少选择一条引流信息。');
      return;
    }
    update('templateTrafficDriving', [...values.templateTrafficDriving,
      ...trafficCombinations(params, trafficSelections)]);
    setTrafficEditorOpen(false);
  };
  const focusFirstError = errors => {
    requestAnimationFrame(() => {
      const first = form.current?.querySelector(`[data-validation-field="${Object.keys(errors)[0]}"]`);
      first?.scrollIntoView?.({ block: 'center', behavior: 'smooth' });
      first?.querySelector('input, textarea, [tabindex]')?.focus();
    });
  };
  const reviewTemplate = () => {
    if (operation.busy || operation.uncertain) return;
    setSnapshot(null); operation.clearError();
    let request;
    try {
      if (values.signatures.some(name => !signatures.rows.some(row => row.Signature === name))) {
        throw new OperationError('签名尚未核实，请重新选择。', { field: 'signatures' });
      }
      request = templatePayload(values);
    } catch (cause) {
      if (cause instanceof OperationError && cause.field) {
        const errors = { [cause.field]: cause.message };
        setFieldErrors(errors); focusFirstError(errors); return;
      }
      throw cause;
    }
    setFieldErrors({});
    return operation.run(async () => {
      setSnapshot(checkedTemplatePreview(await client.call('preview_template', { request }), request));
    });
  };
  const submit = () => operation.run(async () => {
    let result;
    try {
      result = await client.call('submit_template', { request: snapshot.request, confirmation: snapshot.confirmation }, { write: true });
    } catch (cause) {
      if (cause instanceof OperationError && !cause.unknown) setSnapshot(null);
      throw cause;
    }
    if (typeof result?.templateId !== 'string' || !result.templateId) {
      throw new OperationError('模板申请结果不完整，请查询模板记录后核实。', { unknown: true, code: 'invalid_response' });
    }
    setReceipt({ ...result, name: snapshot.request.name }); setSnapshot(null);
    await client.report({ form: 'template', state: 'submitted', templateId: result.templateId, status: result.status });
  }, { mutation: true });
  const shortUrl = values.shortUrlConfig ?? {};
  const shortField = (key, value) => {
    if (key === 'isEnabled' && value !== shortUrl.isEnabled) {
      loadedTrafficMode.current = null;
      setTraffic({ links: [], phones: [] });
      setTrafficSelections({});
      setFieldErrors(current => {
        const next = { ...current }; delete next.shortUrlConfig; delete next.templateTrafficDriving; return next;
      });
      setValues(current => ({ ...current,
        shortUrlConfig: { ...current.shortUrlConfig, [key]: value },
        templateTrafficDriving: [] }));
      return;
    }
    update('shortUrlConfig', { ...shortUrl, [key]: value });
  };
  const review = snapshot?.request;
  return <LockedFields locked={operation.busy || operation.uncertain}><main className="batch-page template-page">
    <header className="batch-header"><div className="batch-header-inner"><div className="batch-brand">火山引擎 · 短信服务</div>
      <h1>申请短信模板</h1><p>填写正文与变量。提交后仍需等待模板审核和运营商报备。</p></div></header>
    <div className="batch-body"><Feedback operation={operation} /><Feedback operation={trafficOperation} />
      <section className="batch-sheet batch-section">
      {receipt ? <Receipt title="模板申请已受理" id={receipt.templateId}>
        <p>{receipt.name} 已提交；受理不等于审核或报备通过。</p>
        {receipt.templateId && <Button loading={operation.busy} onClick={() => operation.run(async () => setStatus(page(await client.call('list_templates', {
          template_id: receipt.templateId, page: 1, page_size: 100,
        }))))}>刷新审核状态</Button>}
        {status && <p>查询到 {status.total} 条模板记录；{status.rows.map(row => row.StatusDescription ?? row.statusDescription ?? '请按返回的审核状态继续核对').join('；')}</p>}
      </Receipt> : snapshot ? <Confirm title="核对模板申请" submitLabel="确认提交模板" busy={operation.busy} disabled={operation.uncertain}
        onBack={() => setSnapshot(null)} onSubmit={submit}>
        <Summary items={[["名称", review.name], ["短信类型", channels.find(([kind]) => kind === review.channelType)?.[1]],
          ["签名", review.signatures.join('、')], ["正文", review.content], ["用途说明", review.desc]]} />
        {review.templateParams.map(row => <Summary key={row.name} items={[["变量", row.name], ["类型", parameterTypes.find(([kind]) => kind === row.paramType)?.[1]]]} />)}
        {review.templateTrafficDriving?.map((rows, group) => <div key={group}><h3>引流信息 {group + 1}</h3>{rows.map((row, index) => <Summary key={index} items={[["变量", row.name], ["内容", row.content ?? `引流信息 ${row.id}`]]} />)}</div>)}
        {review.shortUrlConfig && <Summary items={[["平台短链", review.shortUrlConfig.isEnabled === '1' ? '启用' : '未启用'], ["短链归属", review.shortUrlConfig.belong],
          ["点击明细", review.shortUrlConfig.isNeedClickDetails], ["访问校验策略", review.shortUrlConfig.uaCheckStrategy]]} />}
        <div className="template-check-result"><h3>固定引流信息检查</h3>
          {snapshot.fixedTraffic.length ? snapshot.fixedTraffic.map((row, index) => <Summary key={index}
            items={[["类型", row.paramType === 2 ? '固定链接' : '固定联系号码'], ["内容", row.content ?? '已识别资源'], ["录入状态", '已录入引流信息库']]} />)
            : <p>未识别到固定链接或联系号码。</p>}
        </div>
        {snapshot.warnings.map(warning => <Alert className="sms-feedback" type="warning" key={warning} content={warning} />)}
      </Confirm> : <div className="template-form" ref={form}>
        <div className="template-form-grid">
          <Field validationName="name" error={fieldErrors.name} label="模版名称"
            value={values.name} onChange={value => update('name', value)} maxLength={50} required />
          <Choice validationName="channelType" error={fieldErrors.channelType}
            label="模版类型" value={values.channelType} options={channels} onChange={changeChannel} />
          <Choice label="关联签名" mode="multiple" value={values.signatures}
            validationName="signatures" error={fieldErrors.signatures}
            options={signatures.rows.map(row => [row.Signature, row.Signature])} onChange={value => update('signatures', value)} />
          <Field validationName="desc" error={fieldErrors.desc}
            label="模版用途" value={values.desc} onChange={value => update('desc', value)} maxLength={300} />
        </div>
        <CatalogMore loaded={signatures.rows.length} total={signatures.total} disabled={operation.busy}
          onClick={() => operation.run(() => loadSignatures(signatures.page + 1))} />
        {values.channelType === 'CN_MKT' && <div className="template-form-grid template-short-url"
          data-validation-field="shortUrlConfig">
          <Field label="使用平台生成短链"><Radio.Group aria-label="使用平台生成短链"
            value={shortUrl.isEnabled ?? '0'} onChange={value => shortField('isEnabled', value)}>
            <Radio value="1">是</Radio><Radio value="0">否</Radio>
          </Radio.Group></Field>
          {shortUrl.isEnabled === '1' && <Field label="个性化点击情况统计"><Radio.Group aria-label="个性化点击情况统计"
            value={shortUrl.isNeedClickDetails ?? '0'} onChange={value => shortField('isNeedClickDetails', value)}>
            <Radio value="1">是</Radio><Radio value="0">否</Radio>
          </Radio.Group></Field>}
          {shortUrl.isEnabled === '1' && <Field label="短链接访问设备"><Radio.Group aria-label="短链接访问设备"
            value={shortUrl.uaCheckStrategy ?? 0} onChange={value => shortField('uaCheckStrategy', value)}>
            <Radio value={0}>仅移动设备可访问</Radio><Radio value={1}>所有设备可访问</Radio>
          </Radio.Group></Field>}
          {fieldErrors.shortUrlConfig && <div className="traffic-field-error span-2" role="alert">{fieldErrors.shortUrlConfig}</div>}
        </div>}
        <Field wrapperClassName="template-content-field" validationName="content" error={fieldErrors.content} label="模版内容"
          value={values.content} onChange={value => update('content', value)} multiline required />
        <section className="template-variable-manager" aria-label="模板变量与引流信息">
          <div className="template-subtitle">变量管理</div>
          <div className="template-param-validation" data-validation-field="templateParams">
          <Table className="template-param-table" pagination={false} rowKey="name" data={values.templateParams}
            noDataElement={<span className="template-empty">暂无变量</span>}
            columns={[
              { title: '变量名', dataIndex: 'name', render: name =>
                <Input aria-label={`变量 ${name} 的名称`} value={name} disabled /> },
              { title: '变量类型', dataIndex: 'paramType', render: (value, row, index) =>
                <Radio.Group aria-label={`变量 ${row.name} 的类型`} value={value}
                  onChange={next => editParameter(index, next)}>
                  {(values.channelType === 'CN_OTP' ? [parameterTypes[0]] : selectableParameterTypes)
                    .map(([kind, label]) => <Radio key={kind} value={kind}>{label}</Radio>)}
                </Radio.Group> },
            ]} />
          {fieldErrors.templateParams && <div className="traffic-field-error" role="alert">{fieldErrors.templateParams}</div>}
          </div>
          {trafficParameters(values.templateParams).length > 0 && <div className="template-traffic-manager">
            <div className="template-subtitle">引流信息管理</div>
          <Table className="template-drive-table" pagination={false} rowKey={(_row, index) => String(index)}
            noDataElement={<span className="template-empty">暂无引流信息</span>}
            data={values.templateTrafficDriving}
            columns={[
              { title: '变量模版内容', render: (_value, rows) => bindingContent(values.content, rows, traffic) },
              ...trafficParameters(values.templateParams).map(parameter => ({
                title: parameter.name,
                render: (_value, rows) => {
                  const row = rows.find(item => item.name === parameter.name);
                  return row ? resourceLabel(row, traffic) : '-';
                },
              })),
              { title: '操作', width: 72, render: (_rows, _record, index) =>
                <Button type="text" disabled={operation.busy || operation.uncertain}
                  aria-label={`删除第 ${index + 1} 组引流信息`}
                  onClick={() => update('templateTrafficDriving', values.templateTrafficDriving.filter((_rows, i) => i !== index))}>删除</Button> },
            ]} />
          <Button className="template-add-traffic" type="text" icon={<IconPlus />}
            loading={trafficOperation.busy}
            disabled={operation.busy || operation.uncertain || trafficOperation.busy || trafficOperation.uncertain}
            onClick={openTrafficEditor}>添加引流信息</Button>
          {fieldErrors.templateTrafficDriving && <div data-validation-field="templateTrafficDriving"
            className="traffic-field-error" role="alert">{fieldErrors.templateTrafficDriving}</div>}
          </div>}
        </section>
        <Modal className="template-traffic-modal" wrapClassName="template-traffic-modal-wrap"
          visible={trafficEditorOpen} title="新增引流信息" maskClosable={false} unmountOnExit
          onCancel={() => setTrafficEditorOpen(false)} onOk={saveTrafficEditor}>
          <div className="template-modal-subtitle">模版信息</div>
          <dl className="template-modal-description"><dt>模版内容</dt><dd>{values.content}</dd></dl>
          <div className="template-modal-subtitle">变量管理</div>
          {trafficParameters(values.templateParams).map(parameter => {
            const source = parameter.paramType === 2 ? traffic.links : traffic.phones;
            return <Field key={parameter.name}
              label={`变量名称：${parameter.name}`}>
              <Select aria-label={`变量 ${parameter.name} 的引流信息`} mode="multiple"
                placeholder={parameter.paramType === 2 ? '请选择链接' : '请选择号码'}
                value={trafficSelections[parameter.name] ?? []}
                options={source.filter(item => Number.isInteger(item.id)).map(item => ({
                  value: item.id, label: item.link ?? item.jumpLink ?? item.number ?? `引流信息 ${item.id}`,
                }))}
                onChange={ids => {
                  setTrafficSelections(current => ({ ...current, [parameter.name]: ids }));
                  setTrafficEditorError('');
                }} />
            </Field>;
          })}
          {trafficEditorError && <Alert type="error" content={trafficEditorError} />}
        </Modal>
        <Alert type="info" content="模板申请受理后仍需审核；营销内容按实际业务保留退订提示，是否可用以审核和报备结果为准。" />
        <Button type="primary" loading={operation.busy} disabled={operation.busy || operation.uncertain}
          onClick={reviewTemplate}>核对模板申请</Button>
      </div>}
    </section></div>
  </main></LockedFields>;
}
