import React, { useEffect, useRef, useState } from 'react';
import { Alert, Button, Checkbox, DatePicker, Radio, Result } from '@arco-design/web-react';
import { IconCheck, IconClose, IconDownload } from '@arco-design/web-react/icon';
import { BatchTestSms } from './batch-test-sms.jsx';
import { BatchChoice, BatchDetails, BatchField, BatchHeading, BatchUpload, batchTime } from './batch-controls.jsx';
import { Confirm, Feedback, LockedFields, Receipt, Summary, useOperation } from './common.jsx';
import { OperationError, page, required, withPrefilledOptions } from './client.js';
import { batchTemplateSchema, messageGroupSchema, signatureSchema } from './contracts.js';

// 0–5 的任务可以请求取消，是否超过取消截止时间由短信服务最终校验。
const cancellableStatuses = new Set([0, 1, 2, 3, 4, 5]);
const startedStatuses = new Set([3, 4, 5, 6]);
const batchChannelTypes = ['CN_NTC', 'CN_MKT'];
const scheduleWindow = 30 * 86400;

function beijingDate(milliseconds) {
  return new Date(milliseconds + 8 * 3600000).toISOString().slice(0, 10);
}

function disabledScheduleDate(current) {
  const now = Date.now();
  const date = current.format('YYYY-MM-DD');
  return date < beijingDate(now) || date > beijingDate(now + scheduleWindow * 1000);
}

function disabledScheduleTime(current) {
  const now = Date.now();
  const date = current?.format('YYYY-MM-DD') ?? beijingDate(now);
  const midnight = Date.parse(date + 'T00:00:00+08:00');
  const unavailable = milliseconds => milliseconds <= now || milliseconds > now + scheduleWindow * 1000;
  const range = (length, predicate) => Array.from({ length }, (_, index) => index).filter(predicate);
  return {
    disabledHours: () => range(24, hour => range(60, minute =>
      !unavailable(midnight + (hour * 60 + minute) * 60000)).length === 0),
    disabledMinutes: hour => range(60, minute => unavailable(midnight + (hour * 60 + minute) * 60000)),
  };
}

function BatchMore({ loaded, total, onClick, disabled }) {
  return loaded < total && <Button htmlType="button" type="text" disabled={disabled} onClick={onClick}>加载更多</Button>;
}

function signatureScope(group) {
  return { SubAccounts: [group], ChannelTypes: batchChannelTypes, Statuses: [3, 5] };
}

export function batchPayload(values, template, file, key) {
  required(values.subAccount, '请选择消息组。'); required(values.signature, '请选择签名。');
  required(values.name, '请填写任务名称。');
  if (!template || !batchChannelTypes.includes(template.ChannelType)) throw new OperationError('请选择通知或营销群发模板。');
  if (!file?.file) throw new OperationError('请先上传符合模板要求的 CSV 名单。');
  const fields = template.TaskFields ?? [];
  if (!Array.isArray(fields) || fields.some(field => field.Name !== 'content')) throw new OperationError('当前模板需要此表单尚未支持的任务字段，请在控制台处理。');
  if (fields.some(field => field.Required === true)) required(values.content, '请填写任务正文。');
  if (values.scheduled) required(values.sendAt, '请选择定时时间');
  const sendTime = values.scheduled ? Math.floor(new Date(values.sendAt + '+08:00').getTime() / 1000) : 0;
  const now = Date.now() / 1000;
  if (values.scheduled && (!Number.isFinite(sendTime) || sendTime <= now)) throw new OperationError('定时时间必须晚于当前时间。');
  if (values.scheduled && sendTime > now + scheduleWindow) throw new OperationError('定时发送须在未来 30 天内。');
  return {
    subAccount: values.subAccount, name: values.name, signature: values.signature, templateId: template.TemplateId,
    fileUrl: file.file, scheduled: values.scheduled, sendTime, idempotencyKey: key,
    ...(fields.length && values.content !== undefined ? { content: values.content } : {}),
  };
}

export function BatchForm({ client, prefill, initialTask }) {
  const [values, setValues] = useState(() => ({
    name: prefill?.name,
    content: prefill?.content,
    scheduled: prefill?.scheduled ?? (prefill?.sendTime > 0),
    // 日期控件展示北京时间，不取宿主系统时区；保留 Unix 秒的精度。
    sendAt: prefill?.sendTime > 0
      ? new Date((prefill.sendTime + 8 * 3600) * 1000).toISOString().slice(0, 19)
      : undefined,
  }));
  const [groups, setGroups] = useState({ rows: [], total: 0, page: 0 });
  const [signatures, setSignatures] = useState({ rows: [], total: 0, page: 0 });
  const [templates, setTemplates] = useState({ rows: [], total: 0, page: 0 });
  const [prefilled, setPrefilled] = useState({});
  const [sendTimeTouched, setSendTimeTouched] = useState(false);
  const pending = useRef({ signature: prefill?.signature, templateId: prefill?.templateId });
  const [csvExample, setDemo] = useState(null);
  const demo = csvExample?.value;
  const [file, setFile] = useState(prefill?.recipientsFile ?? null);
  const [snapshot, setSnapshot] = useState(null);
  const [agreed, setAgreed] = useState(false);
  const [ended, setEnded] = useState(false);
  const [previewTemplate, setPreviewTemplate] = useState(null);
  // 与参考页一致，引流检查由开表配置决定，随名单校验执行，不额外增加勾选步骤。
  const [checkTraffic] = useState(prefill?.checkTraffic ?? false);
  const [trafficReport, setTrafficReport] = useState(null);
  const recipientReview = useRef(null);
  const automaticReview = useRef(null);
  const [trial, setTrial] = useState(null);
  const [task, setTask] = useState(initialTask ?? null);
  const [taskAction, setTaskAction] = useState(null);
  const [detail, setDetail] = useState(null);
  const operation = useOperation();
  // 精确查询补到的选项单独保留，分页进度仍由常规列表决定。
  const groupRows = withPrefilledOptions(groups.rows, prefilled.group ? [prefilled.group] : [], 'subAccountId');
  const signatureRows = withPrefilledOptions(signatures.rows, prefilled.signature ? [prefilled.signature] : [], 'Signature');
  const templateRows = withPrefilledOptions(templates.rows, prefilled.template ? [prefilled.template] : [], 'TemplateId');
  const selected = templateRows.find(row => row.TemplateId === values.templateId);
  const invalidate = () => {
    setSnapshot(null); setAgreed(false); setPreviewTemplate(null); setTrafficReport(null);
  };
  const update = (key, value) => {
    invalidate();
    setValues(current => ({ ...current, [key]: value }));
  };
  const loadGroups = async (next = groups.page + 1) => {
    const result = page(await client.query('GetSubAccountListForAgent', { pageIndex: next, pageSize: 100 }), messageGroupSchema);
    setGroups(current => ({ ...result, rows: next === 1 ? result.rows : [...current.rows, ...result.rows], page: next }));
    return result.rows;
  };
  const loadSignatures = async (group, next = 1) => {
    const result = page(await client.query('ListSignaturesForAgent', {
      ...signatureScope(group), Page: next, PageSize: 100,
    }), signatureSchema);
    setSignatures(current => ({ ...result, rows: next === 1 ? result.rows : [...current.rows, ...result.rows], page: next }));
    return result.rows;
  };
  const loadTemplates = async (group, signature, next = 1) => {
    const result = page(await client.query('ListBatchTemplatesForAgent', { SubAccounts: [group], Signatures: [signature], Page: next, PageSize: 100 }), batchTemplateSchema);
    setTemplates(current => ({ ...result, rows: next === 1 ? result.rows : [...current.rows, ...result.rows], page: next }));
    return result.rows;
  };
  const loadCsvExample = async (group, templateId) => {
    const result = await client.call('get_batch_csv_template', {
      sub_account: group, template_id: templateId, include_variables: true,
    });
    if (typeof result?.value !== 'string' || !result.value) throw new OperationError('模板未返回 CSV 示例。');
    if (!Array.isArray(result.variables) || result.variables.some(name => typeof name !== 'string' || !name)) {
      throw new OperationError('模板未返回完整的 CSV 列定义。');
    }
    setDemo(result);
  };
  const clearTemplateInput = fields => {
    invalidate();
    setValues(current => ({ ...current, ...fields, templateId: undefined,
      content: current.templateId === undefined ? current.content : undefined }));
    // 已上传名单属于原消息组和模板；待上传文件可在新模板下重新校验。
    setFile(current => values.templateId === undefined || current?.data !== undefined ? current : null);
    setTrial(null);
    setDemo(null);
  };
  const readTemplate = async (subAccount, signature, templateId) => {
    const current = page(await client.query('ListBatchTemplatesForAgent', {
      TemplateId: templateId, SubAccounts: [subAccount], Signatures: [signature], Page: 1, PageSize: 100,
    }), batchTemplateSchema);
    if (current.total !== 1 || current.rows.length !== 1 || current.rows[0].TemplateId !== templateId) {
      throw new OperationError('模板配置缺失或存在多条结果，请先核对明确的模板配置。');
    }
    return current.rows[0];
  };
  const applyTemplatePrefill = async (group, signature, rows) => {
    const templateId = pending.current.templateId;
    if (templateId === undefined) return;
    pending.current.templateId = undefined;
    const template = rows.find(row => row.TemplateId === templateId) ?? await readTemplate(group, signature, templateId);
    if (!batchChannelTypes.includes(template.ChannelType) ||
        (template.TaskFields ?? []).some(field => field.Name !== 'content')) {
      throw new OperationError('预填模板不适用于当前群发表单，请重新选择。');
    }
    setPrefilled(current => ({ ...current, template }));
    await loadCsvExample(group, templateId);
    update('templateId', templateId);
  };
  const selectGroup = async group => {
    clearTemplateInput({ subAccount: group, signature: undefined });
    setPrefilled(current => ({ group: current.group }));
    setSignatures({ rows: [], total: 0, page: 0 });
    setTemplates({ rows: [], total: 0, page: 0 });
    const rows = await loadSignatures(group);
    const signature = pending.current.signature;
    if (signature === undefined) return;
    pending.current.signature = undefined;
    const matches = row => row.Signature === signature;
    const choice = rows.find(matches) ?? page(await client.query('ListSignaturesForAgent', {
      ...signatureScope(group), Signature: signature, ExactMatch: true, Page: 1, PageSize: 100,
    }), signatureSchema).rows.find(matches);
    if (!choice) throw new OperationError('预填签名在所选消息组中不可用，请重新选择。');
    setPrefilled(current => ({ ...current, signature: choice }));
    update('signature', signature);
    await applyTemplatePrefill(group, signature, await loadTemplates(group, signature));
  };
  const chooseGroup = group => operation.run(() => selectGroup(group));
  const chooseSignature = signature => operation.run(async () => {
    pending.current.signature = undefined;
    clearTemplateInput({ signature });
    setPrefilled(current => ({ ...current, template: undefined }));
    setTemplates({ rows: [], total: 0, page: 0 });
    await applyTemplatePrefill(values.subAccount, signature, await loadTemplates(values.subAccount, signature));
  });
  const chooseTemplate = templateId => operation.run(async () => {
    pending.current.templateId = undefined;
    clearTemplateInput({});
    await loadCsvExample(values.subAccount, templateId);
    update('templateId', templateId);
  });
  const loadInitialOptions = async () => {
    const rows = await loadGroups(1);
    const subAccount = prefill?.subAccount;
    if (subAccount === undefined) return;
    const matches = row => row.subAccountId === subAccount;
    const group = rows.find(matches) ?? page(await client.query('GetSubAccountListForAgent', {
      subAccount, pageIndex: 1, pageSize: 100,
    }), messageGroupSchema).rows.find(matches);
    if (!group) throw new OperationError('预填消息组当前不可用，请重新选择。');
    setPrefilled({ group });
    await selectGroup(subAccount);
  };
  // 初始结果只用于打开时的预选；宿主更新界面样式不会覆盖用户的后续选择。
  useEffect(() => { operation.run(async () => {
    if (initialTask) {
      await loadTask(initialTask);
    } else await loadInitialOptions();
  }); }, [client]);
  const readTask = async expected => {
    const result = await client.call('query_batch_tasks', { request: { action: 'GetBatchTaskDetail', params: { subAccount: expected.subAccount, taskId: expected.taskId } } });
    if (result?.taskId !== expected.taskId || result?.subAccount !== expected.subAccount || !Number.isInteger(result?.status)) {
      throw new OperationError('返回的任务身份或状态不完整，请先查询核对。');
    }
    return result;
  };
  const loadTask = async reference => {
    const current = await readTask(reference);
    // 身份核对通过后同时更新摘要和详情，首次查询失败后的刷新也能恢复完整操作上下文。
    setTask(previous => ({ ...previous, ...reference,
      name: current.name ?? current.taskName ?? previous?.name,
      signature: current.signature ?? previous?.signature,
      templateId: current.templateId ?? previous?.templateId,
      totalCount: current.totalCount ?? previous?.totalCount,
      dupCount: current.dupCount ?? previous?.dupCount,
    }));
    setDetail(current);
  };
  const startTask = async target => {
    try {
      await client.call('start_batch_task', {
        sub_account: target.subAccount, task_id: target.taskId,
      }, { write: true });
    } catch (cause) {
      if (String(cause?.code) !== '1999') throw cause;
      let current;
      try { current = await readTask(target); } catch { throw cause; }
      setDetail(current);
      if (!startedStatuses.has(current.status)) throw cause;
      await client.report({
        form: 'batch', state: 'operation_already_applied', taskId: target.taskId, operation: 'start',
      });
      return { accepted: false, current };
    }
    await client.report({
      form: 'batch', state: 'operation_accepted', taskId: target.taskId, operation: 'start',
    });
    const current = await readTask(target);
    setDetail(current);
    return { accepted: true, current };
  };
  const prepare = () => operation.run(async () => {
    automaticReview.current = automaticKey;
    if (values.scheduled) setSendTimeTouched(true);
    invalidate();
    const currentTemplate = required(selected, '请选择群发模板。');
    const body = batchPayload(values, currentTemplate, file, crypto.randomUUID());
    if ((currentTemplate.TaskFields ?? []).length) {
      const checked = await client.query('ValidateBatchTaskContentForAgent', { subAccount: body.subAccount, signature: body.signature, templateId: body.templateId, ...(body.content !== undefined ? { content: body.content } : {}) });
      if (checked?.Approved !== true) throw new OperationError(checked?.Reason || '任务正文未通过预检。');
    }
    const traffic = checkTraffic ? {
      sub_account: body.subAccount, signature: body.signature, template_id: body.templateId,
      content: body.content ?? currentTemplate.TemplateContent ?? currentTemplate.Content,
    } : undefined;
    const request = required(file.receipt, '名单上传信息不完整，请重新选择文件。');
    const columns = ['phone', ...required(csvExample, '请先读取当前模板的 CSV 示例。').variables];
    const reviewKey = JSON.stringify({ request, traffic, template: currentTemplate, columns });
    // 仅复用本页同一文件和模板的展示结果；创建任务仍由短信后端重新校验文件。
    let checked = recipientReview.current?.key === reviewKey
      && request.context?.expires_at * 1000 > Date.now() ? recipientReview.current.result : null;
    if (!checked) {
      checked = await client.call('complete_recipients_upload', { request, columns, ...(traffic ? { traffic } : {}) });
      if (checked?.file !== file.file || checked?.receipt?.signature !== request.signature
        || !Number.isInteger(checked.totalCount) || checked.totalCount <= 0
        || !Number.isInteger(checked.dupCount) || checked.dupCount < 0
        || checked.dupCount >= checked.totalCount) {
        throw new OperationError('名单核对结果不完整，请重新核对。');
      }
      const report = checked.trafficReport;
      if (checkTraffic && (!report || report.totalRows !== checked.totalCount)) {
        throw new OperationError('名单引流检查结果不完整，请重新核对。');
      }
      recipientReview.current = !report || (report.checkedRows === report.totalRows
        && report.failedRows === 0 && report.uncheckedRows === 0 && report.missingResourceRows === 0)
        ? { key: reviewKey, result: checked } : null;
    }
    setFile(previous => ({ ...previous, ...checked }));
    setTrafficReport(checked.trafficReport ?? null);
    setPreviewTemplate(currentTemplate);
    setSnapshot(body);
  });
  // 自动校验只读接口；失败不自动重试，修改输入或手动核对后再尝试。
  const automaticKey = JSON.stringify({ values, template: selected, receipt: file?.receipt,
    file: file?.file, columns: csvExample?.variables, checkTraffic });
  useEffect(() => {
    if (task || ended || operation.busy || operation.uncertain || !selected || !csvExample
      || !file?.file || !file?.receipt || !values.name || (values.scheduled && !values.sendAt)
      || automaticReview.current === automaticKey) return;
    const timer = setTimeout(() => {
      automaticReview.current = automaticKey;
      prepare();
    }, 300);
    return () => clearTimeout(timer);
  }, [automaticKey, operation.busy, operation.uncertain, task, ended]);
  const create = () => operation.run(async () => {
    if (!snapshot || !agreed) return;
    // 确认时重新核对时间，避免停留过久后提交已经过期的定时任务。
    let result;
    try {
      batchPayload(values, previewTemplate, file, snapshot.idempotencyKey);
      result = await client.call('create_batch_task', { request: snapshot }, { write: true });
      if (typeof result?.taskId !== 'string' || !result.taskId) {
        throw new OperationError('未收到可核对的任务编号，请先查询任务记录。', { unknown: true });
      }
    } catch (cause) { setAgreed(false); throw cause; }
    const created = { ...result, subAccount: snapshot.subAccount, name: snapshot.name, signature: snapshot.signature, templateId: snapshot.templateId };
    setTask(created);
    setSnapshot(null); setFile(null); setDemo(null);
    await client.report({ form: 'batch', state: 'created', taskId: result.taskId, totalCount: result.totalCount, dupCount: result.dupCount });
    let current = await readTask(created);
    setDetail(current);
    if (startedStatuses.has(current.status)) return;
    if (current.status !== 2) throw new OperationError('任务创建成功，但当前状态尚不能启动，请刷新任务状态。');
    const started = await startTask(created);
    if (started.accepted) setTask(value => ({ ...value, submittedAction: 'start' }));
  }, { mutation: true });
  const upload = source => operation.run(async () => {
    invalidate();
    const uploaded = await client.upload(source, { kind: 'recipients', sub_account: values.subAccount, template_id: values.templateId });
    setFile({ ...uploaded, source });
    return uploaded;
  }, { mutation: true });
  const abandon = () => operation.run(async () => {
    invalidate(); setFile(null); setTrial(null); recipientReview.current = null; setEnded(true);
    await client.report({ form: 'batch', state: 'abandoned' });
  });
  const refresh = () => operation.run(() => loadTask(task));
  const prepareTaskAction = action => operation.run(async () => {
    const current = await readTask(task);
    if (action === 'cancel' && !cancellableStatuses.has(current.status)) throw new OperationError('当前任务状态不支持取消，请核对最新状态。');
    let confirmationContent = current.sendContent;
    if (action === 'start') {
      required(current.signature ?? task.signature, '任务签名未完整返回，请查询核对后操作。');
      if (current.status !== 2) throw new OperationError('任务尚未通过校验或已启动、结束，请核对最新状态。');
      if (current.templateId !== task.templateId) throw new OperationError('任务模板与本次创建请求不一致，请核对。');
      if (typeof current.sendContent !== 'string' || !current.sendContent) {
        const template = await readTemplate(task.subAccount, task.signature, task.templateId);
        if ((template.TaskFields ?? []).length) throw new OperationError('无法取得特殊通知的实际任务正文，暂不能确认启动。');
        confirmationContent = required(template.TemplateContent ?? template.Content, '模板正文缺失，暂不能启动。');
      }
    }
    setDetail({ ...current, confirmationContent }); setTaskAction(action);
  });
  const changeTask = () => operation.run(async () => {
    const action = taskAction;
    if (action === 'start') {
      const started = await startTask(task);
      if (started.accepted) setTask(current => ({ ...current, submittedAction: action }));
      setTaskAction(null);
      return;
    }
    await client.call('cancel_batch_task', {
      sub_account: task.subAccount, task_id: task.taskId,
    }, { write: true });
    setTask(current => ({ ...current, submittedAction: action }));
    setTaskAction(null);
    setDetail(null);
    await client.report({ form: 'batch', state: 'operation_accepted', taskId: task.taskId, operation: action });
    setDetail(await readTask(task));
  }, { mutation: true });

  const locked = operation.busy || operation.uncertain;
  // 完整预填资源核实通过后，按参考页只读展示；部分预填及失效资源仍可补全、重选。
  const readonlyInfo = Boolean(prefill?.name && values.name === prefill.name
    && prefilled.group?.subAccountId === prefill.subAccount && values.subAccount === prefill.subAccount
    && prefilled.signature?.Signature === prefill.signature && values.signature === prefill.signature
    && selected && csvExample && selected.TemplateId === prefill.templateId && values.templateId === prefill.templateId
    && (selected.TaskFields ?? []).every(field => field.Required !== true || Boolean(prefill.content))
    && values.content === prefill.content);
  const messageContent = (selected?.TaskFields ?? []).length && values.content !== undefined
    ? values.content : selected?.TemplateContent ?? selected?.Content ?? '请填写本次任务正文。';
  const fileSize = file?.receipt?.context?.size;
  const fileReady = Number.isFinite(fileSize) && fileSize > 0
    ? `文件已就绪，大小 ${fileSize < 1024 * 1024 ? (fileSize / 1024).toFixed(1) + ' KB' : (fileSize / 1024 / 1024).toFixed(2) + ' MB'}`
    : '文件已就绪。';
  if (ended) return <main className="batch-result-page"><Result status="info" title="已结束群发预览"
    subTitle="本次未创建群发任务。" /><Feedback operation={operation} /></main>;
  return <LockedFields locked={locked}><main className="batch-page">
    <header className="batch-header"><div className="batch-header-inner">
      <div className="batch-title-row"><div><div className="batch-brand">火山引擎短信</div>
        <h1>{initialTask ? '管理短信群发任务' : '创建群发任务'}</h1><p>{initialTask ? '按任务编号核对当前状态，确认后再启动或取消。' : '核对短信信息和收件人名单，一次确认后创建任务并启动发送。'}</p></div>
        {!task && <Button htmlType="button" status="danger" icon={<IconClose />} disabled={locked} onClick={abandon}>结束预览</Button>}</div>
      {!task && <Alert className="batch-privacy" type="success" showIcon content="手机号和逐行变量仅由本机页面传给短信服务，不会作为工具结果进入对话。完成前请保持本页面打开。" />}
    </div></header>
    <div className="batch-body"><Feedback operation={operation} /><div className="batch-sheet">
      {task ? <section className="batch-section"><Receipt title={initialTask ? '群发任务详情' : '群发任务已创建'} id={task.taskId}><p>任务创建成功不等于已经发送。</p></Receipt>
        {task.submittedAction && <p>{task.submittedAction === 'start' ? '启动' : '取消'}请求已受理，请刷新核对最新状态。</p>}
        <Summary items={[['任务', task.name], ['名单数量', task.totalCount], ['重复号码', task.dupCount], ...(detail ? [['当前状态', detail.status === 2 ? '待确认发送' : [3, 4, 5, 6].includes(detail.status) ? '任务已启动，送达结果请查询回执' : '正在处理或已经结束，请核对平台任务记录']] : [])]} />
        {taskAction ? <Confirm key={taskAction} title={taskAction === 'start' ? '确认启动本次群发' : '确认取消本次任务'}
          submitLabel={taskAction === 'start' ? '确认启动群发' : '确认取消任务'} backLabel="暂不操作"
          onBack={() => setTaskAction(null)} onSubmit={changeTask} busy={operation.busy} disabled={operation.uncertain}>
          <p>{taskAction === 'start' ? '启动后会向任务中的名单发送短信，并产生相应费用。' : '是否仍可取消，以短信服务返回结果为准。'}</p>
          <p>任务编号：{task.taskId}</p>
          {taskAction === 'start' && <Summary items={[["签名", detail?.signature ?? task.signature], [detail?.sendContent ? '任务正文' : '已重新核对的模板正文', detail?.confirmationContent]]} />}
        </Confirm> : <div className="batch-actions">
          <Button loading={operation.busy} onClick={refresh}>刷新任务状态</Button>
          <Button disabled={operation.busy || operation.uncertain || task.submittedAction === 'cancel' || !cancellableStatuses.has(detail?.status)} onClick={() => prepareTaskAction('cancel')}>取消任务</Button>
          <Button type="primary" disabled={operation.busy || operation.uncertain || Boolean(task.submittedAction) || detail?.status !== 2} onClick={() => prepareTaskAction('start')}>核对并启动</Button>
        </div>}
      </section> : <>
        <section className="batch-section" aria-label="任务信息"><BatchHeading title="任务信息"
          description={readonlyInfo ? '以下信息由已确认的短信资源生成，仅支持查看。' : '请填写任务名称，并选择消息组、短信签名和群发模板。'} />
          {readonlyInfo ? <BatchDetails items={[
            ['任务名称', values.name], ['消息组', values.subAccount], ['短信签名', values.signature],
            ['模板 ID', selected.TemplateId],
          ]} /> : <div className="form-grid">
          <BatchField label="任务名称" value={values.name} onChange={value => update('name', value)} disabled={locked} required />
          <div><BatchChoice label="消息组" value={values.subAccount} onChange={chooseGroup} disabled={locked} options={groupRows.map(row => [row.subAccountId, row.subAccountName || row.subAccountId])} />
            <BatchMore loaded={groups.rows.length} total={groups.total} onClick={() => operation.run(loadGroups)} disabled={operation.busy} /></div>
          <div><BatchChoice label="短信签名" value={values.signature} onChange={chooseSignature} disabled={!values.subAccount || locked}
            options={[...new Set(signatureRows.map(row => row.Signature))].map(name => [name, name])} />
            <BatchMore loaded={signatures.rows.length} total={signatures.total} onClick={() => operation.run(() => loadSignatures(values.subAccount, signatures.page + 1))} disabled={operation.busy} /></div>
          <div><BatchChoice label="群发模板" value={values.templateId} onChange={chooseTemplate} disabled={!values.signature || locked}
            options={templateRows.filter(row => batchChannelTypes.includes(row.ChannelType)).map(row => [row.TemplateId, row.TemplateName || row.TemplateId])} />
            <BatchMore loaded={templates.rows.length} total={templates.total} onClick={() => operation.run(() => loadTemplates(values.subAccount, values.signature, templates.page + 1))} disabled={operation.busy} /></div>
        </div>}
          {selected && <div className="batch-content-block">
            {!readonlyInfo && <BatchDetails items={[['消息组 ID', values.subAccount], ['模板 ID', selected.TemplateId],
              ['发送类型', selected.ChannelType === 'CN_MKT' ? '营销短信' : '通知短信'],
              ['模板名称', selected.TemplateName]]} />}
            <div className="batch-field-label">短信内容</div><p className="batch-message-content">{messageContent}</p>
            {!readonlyInfo && (selected.TaskFields ?? []).map(field => field.Name === 'content' && <BatchField key={field.Name} label={field.Label ?? '任务正文'} value={values.content} onChange={value => update('content', value)} disabled={locked} multiline maxLength={field.MaxLength} required={field.Required} />)}
          </div>}
        </section>
        <section className="batch-section"><BatchHeading title="上传文件" />
          <div className="batch-upload-actions">
            {demo && <Button htmlType="button" icon={<IconDownload />} disabled={locked}
              onClick={() => operation.run(() => client.downloadCsv(demo))}>点击下载模板</Button>}
            <BatchUpload file={file} disabled={locked} uploadDisabled={!demo || locked} onUpload={upload}
              onRemove={() => { invalidate(); setFile(null); }} />
          </div>
          <ol className="batch-upload-notes">
            <li>请先下载模板，填写对应变量后上传文件。注意请勿修改表格第一行！</li>
            <li>群发任务文件最多支持上传 100 万条手机号</li>
            <li>请上传 .csv 格式文件，大小为 10 MB 以内</li>
          </ol>
          {file?.file && <Alert className="batch-file-ready" type="success" showIcon content={fileReady} />}
        </section>
        <section className="batch-section"><BatchHeading title="发送时间" />
          <div className="batch-form-field"><div className="batch-field-label">是否定时</div>
            <Radio.Group disabled={locked} value={values.scheduled} onChange={value => update('scheduled', value)}
              options={[{ value: false, label: '否' }, { value: true, label: '是' }]} /></div>
          {values.scheduled && <div className="batch-form-field"><BatchField label="定时时间" disabled={locked} required>
            <DatePicker showTime={{ format: 'HH:mm' }} format="YYYY-MM-DD HH:mm" utcOffset={8} showNowBtn={false}
              disabledDate={disabledScheduleDate} disabledTime={disabledScheduleTime}
              error={sendTimeTouched && !values.sendAt} inputProps={{ 'aria-label': '定时时间' }}
              value={values.sendAt?.replace('T', ' ')}
              placeholder="请选择日期" onBlur={() => setSendTimeTouched(true)}
              onChange={value => { setSendTimeTouched(true); update('sendAt', value?.replace(' ', 'T')); }} />
          </BatchField>{sendTimeTouched && !values.sendAt && <div className="batch-field-error">请选择定时时间</div>}
            <div className="batch-field-help">定时发送须在未来 30 天内。国内默认发送时段为 08:00–21:30，具体限制以服务端对当前账号的校验为准。</div></div>}
        </section>
        {selected && selected.BatchOnly !== true && !(selected.TaskFields ?? []).length && Array.isArray(csvExample?.variables) &&
          <BatchTestSms key={JSON.stringify([values.subAccount, values.signature, values.templateId])}
            client={client} operation={operation} subAccount={values.subAccount}
            signature={values.signature} template={selected} variables={csvExample.variables}
            trial={trial} setTrial={setTrial} />}
        <section className="batch-section"><BatchHeading title="校验结果与确认" description="文件上传且发送时间有效后，短信服务会自动校验；确认后将创建任务并启动发送。" />
          {!snapshot ? <Alert type="info" showIcon content={!file?.file ? '上传名单文件后将自动校验。'
            : values.scheduled && !values.sendAt ? '请选择定时时间，设置完成后将自动校验。'
            : operation.error ? '校验未完成，请检查当前文件和发送时间。'
            : operation.busy ? '短信服务正在自动校验文件。' : '请完善任务信息，短信服务将自动校验文件。'} /> : <div id="batch-validation-result">
            <div className="batch-counts"><div><span>有效号码</span><strong>{file.totalCount - file.dupCount}</strong></div>
              <div><span>重复数据</span><strong>{file.dupCount}</strong></div></div>
            <BatchDetails className="batch-confirm-details" items={[
              ['任务名称', snapshot.name], ['短信签名', snapshot.signature], ['模板 ID', snapshot.templateId],
              ['发送安排', snapshot.scheduled ? batchTime(snapshot.sendTime) : '启动后立即发送'], ['名单文件', file.name],
              ['总记录数', file.totalCount],
            ]} />
            {file.dupCount > 0 && <Alert className="batch-validation-warning" type="warning" showIcon
              content="名单中存在重复号码，请核对有效号码数后继续。最终去重结果以创建任务返回为准。" />}
            {file.samples?.length > 0 && <details><summary>查看名单样例（前 {file.samples.length} 行）</summary>
              {file.samples.map((sample, index) => <BatchDetails key={index} items={[['号码', sample.phone], ...Object.entries(sample.params)]} />)}
            </details>}
            {trafficReport && <Alert className="batch-validation-warning" showIcon
              type={trafficReport.missingResourceRows || trafficReport.failedRows || trafficReport.uncheckedRows ? 'warning' : 'success'} content={<>
                引流资源已检查 {trafficReport.checkedRows} / {trafficReport.totalRows} 行，
                缺少资源 {trafficReport.missingResourceRows} 行，查询失败 {trafficReport.failedRows} 行，未覆盖 {trafficReport.uncheckedRows} 行。
                {trafficReport.missingRowNumbers?.length > 0 && <div>缺少资源的 CSV 行号 {trafficReport.missingRowNumbers.join('、')}</div>}
                {trafficReport.reason === 'short_link_mode_unavailable' && <div>当前模板的短链配置暂不可核对，引流检查未覆盖本次名单。</div>}
                {trafficReport.failures?.map((failure, index) => <div key={index} style={{ whiteSpace: 'pre-wrap' }}>
                  {failure.error.message}
                  {failure.error.code != null && <div>错误码：{failure.error.code}</div>}
                  {failure.request_id && <div>排障编号：{failure.request_id}</div>}
                </div>)}
              </>} />}
            <div className="batch-confirm"><Checkbox checked={agreed} disabled={locked} onChange={setAgreed}>
              我已核对任务信息、文件校验结果和发送时间，同意创建任务并启动发送
            </Checkbox></div>
          </div>}
        </section>
        <footer className="batch-actions"><Button htmlType="button" status="danger" disabled={locked} onClick={abandon}>结束预览</Button>
          <div>{snapshot && <Button htmlType="button" disabled={locked} onClick={invalidate}>返回修改</Button>}
            <Button htmlType="button" loading={operation.busy} disabled={operation.uncertain} onClick={prepare}>核对群发任务</Button>
            <Button htmlType="button" type="primary" icon={<IconCheck />} loading={operation.busy} disabled={locked || !snapshot || !agreed} onClick={create}>确认创建并启动</Button>
          </div></footer>
      </>}
    </div></div>
  </main></LockedFields>;
}
