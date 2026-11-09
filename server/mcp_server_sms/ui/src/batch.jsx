import React, { useEffect, useState } from 'react';
import { Button, Radio } from '@arco-design/web-react';
import { Choice, Confirm, Feedback, Field, Files, LockedFields, More, Receipt, Summary, useOperation } from './common.jsx';
import { OperationError, page, required } from './client.js';
import { batchTemplateSchema, messageGroupSchema, signatureSchema } from './contracts.js';

// 0–5 的任务可以请求取消，是否超过取消截止时间由短信服务最终校验。
const cancellableStatuses = new Set([0, 1, 2, 3, 4, 5]);

export function batchPayload(values, template, file, key) {
  required(values.subAccount, '请选择消息组。'); required(values.signature, '请选择签名。');
  required(values.name, '请填写任务名称。');
  if (!template || !['CN_NTC', 'CN_MKT'].includes(template.ChannelType)) throw new OperationError('请选择通知或营销群发模板。');
  if (!file?.file) throw new OperationError('请先上传符合模板要求的 CSV 名单。');
  const fields = template.TaskFields ?? [];
  if (!Array.isArray(fields) || fields.some(field => field.Name !== 'content')) throw new OperationError('当前模板需要此表单尚未支持的任务字段，请在控制台处理。');
  if (fields.some(field => field.Required === true)) required(values.content, '请填写任务正文。');
  const sendTime = values.scheduled ? Math.floor(new Date(values.sendAt + '+08:00').getTime() / 1000) : 0;
  if (values.scheduled && (!Number.isFinite(sendTime) || sendTime <= Date.now() / 1000)) throw new OperationError('请填写未来的北京时间。');
  return {
    subAccount: values.subAccount, name: values.name, signature: values.signature, templateId: template.TemplateId,
    fileUrl: file.file, scheduled: values.scheduled, sendTime, idempotencyKey: key,
    ...(fields.length && values.content !== undefined ? { content: values.content } : {}),
  };
}

export function BatchForm({ client }) {
  const [values, setValues] = useState({ scheduled: false });
  const [groups, setGroups] = useState({ rows: [], total: 0, page: 0 });
  const [signatures, setSignatures] = useState({ rows: [], total: 0, page: 0 });
  const [templates, setTemplates] = useState({ rows: [], total: 0, page: 0 });
  const [demo, setDemo] = useState(null);
  const [file, setFile] = useState(null);
  const [snapshot, setSnapshot] = useState(null);
  const [previewTemplate, setPreviewTemplate] = useState(null);
  const [task, setTask] = useState(null);
  const [taskAction, setTaskAction] = useState(null);
  const [detail, setDetail] = useState(null);
  const operation = useOperation();
  const selected = templates.rows.find(row => row.TemplateId === values.templateId);
  const update = (key, value) => setValues(current => ({ ...current, [key]: value }));
  const loadGroups = async () => {
    const next = groups.page + 1;
    const result = page(await client.query('GetSubAccountListForAgent', { pageIndex: next, pageSize: 100 }), messageGroupSchema);
    setGroups(current => ({ ...result, rows: [...current.rows, ...result.rows], page: next }));
  };
  useEffect(() => { operation.run(loadGroups); }, [client]);
  const loadSignatures = async (group, next = 1) => {
    const result = page(await client.query('ListSignaturesForAgent', {
      SubAccounts: [group], ChannelTypes: ['CN_NTC', 'CN_MKT'], Statuses: [3, 5], Page: next, PageSize: 100,
    }), signatureSchema);
    setSignatures(current => ({ ...result, rows: next === 1 ? result.rows : [...current.rows, ...result.rows], page: next }));
  };
  const loadTemplates = async (signature, next = 1) => {
    const result = page(await client.query('ListBatchTemplatesForAgent', { SubAccounts: [values.subAccount], Signatures: [signature], Page: next, PageSize: 100 }), batchTemplateSchema);
    setTemplates(current => ({ ...result, rows: next === 1 ? result.rows : [...current.rows, ...result.rows], page: next }));
  };
  const chooseGroup = group => operation.run(async () => {
    setValues(current => ({ ...current, subAccount: group, signature: undefined, templateId: undefined, content: undefined }));
    setSignatures({ rows: [], total: 0, page: 0 }); setTemplates({ rows: [], total: 0, page: 0 }); setDemo(null); setFile(null);
    await loadSignatures(group);
  });
  const chooseSignature = signature => operation.run(async () => {
    setValues(current => ({ ...current, signature, templateId: undefined, content: undefined }));
    setTemplates({ rows: [], total: 0, page: 0 }); setDemo(null); setFile(null);
    await loadTemplates(signature);
  });
  const chooseTemplate = templateId => operation.run(async () => {
    setValues(current => ({ ...current, templateId, content: undefined })); setFile(null); setDemo(null);
    const result = await client.call('get_batch_csv_template', { sub_account: values.subAccount, template_id: templateId });
    if (typeof result?.value !== 'string' || !result.value) throw new OperationError('模板未返回 CSV 示例。');
    setDemo(result.value);
  });
  const readTemplate = async (subAccount, signature, templateId) => {
    const current = page(await client.query('ListBatchTemplatesForAgent', {
      TemplateId: templateId, SubAccounts: [subAccount], Signatures: [signature], Page: 1, PageSize: 100,
    }), batchTemplateSchema);
    if (current.total !== 1 || current.rows.length !== 1 || current.rows[0].TemplateId !== templateId) {
      throw new OperationError('模板配置缺失或存在多条结果，请先核对明确的模板配置。');
    }
    return current.rows[0];
  };
  const readTask = async expected => {
    const result = await client.call('get_batch_task', { sub_account: expected.subAccount, task_id: expected.taskId });
    if (result?.taskId !== expected.taskId || result?.subAccount !== expected.subAccount || !Number.isInteger(result?.status)) {
      throw new OperationError('返回的任务身份或状态不完整，请先查询核对。');
    }
    return result;
  };
  const prepare = () => operation.run(async () => {
    const currentTemplate = await readTemplate(required(values.subAccount, '请选择消息组。'), required(values.signature, '请选择签名。'), required(values.templateId, '请选择群发模板。'));
    const body = batchPayload(values, currentTemplate, file, crypto.randomUUID());
    if ((currentTemplate.TaskFields ?? []).length) {
      const checked = await client.query('ValidateBatchTaskContentForAgent', { subAccount: body.subAccount, signature: body.signature, templateId: body.templateId, ...(body.content !== undefined ? { content: body.content } : {}) });
      if (checked?.Approved !== true) throw new OperationError(checked?.Reason || '任务正文未通过预检。');
    }
    setPreviewTemplate(currentTemplate);
    setSnapshot(body);
  });
  const create = () => operation.run(async () => {
    const result = await client.call('create_batch_task', { request: snapshot }, { write: true });
    const created = { ...result, subAccount: snapshot.subAccount, name: snapshot.name, signature: snapshot.signature, templateId: snapshot.templateId };
    setTask(created);
    setSnapshot(null); setFile(null); setDemo(null);
    await client.report({ form: 'batch', state: 'created', taskId: result.taskId, totalCount: result.totalCount, dupCount: result.dupCount });
    setDetail(await readTask(created));
  }, { mutation: true });
  const refresh = () => operation.run(async () => setDetail(await readTask(task)));
  const prepareTaskAction = action => operation.run(async () => {
    const current = await readTask(task);
    if (action === 'cancel' && !cancellableStatuses.has(current.status)) throw new OperationError('当前任务状态不支持取消，请核对最新状态。');
    let confirmationContent = current.sendContent;
    if (action === 'start') {
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
    await client.call(taskAction === 'start' ? 'start_batch_task' : 'cancel_batch_task', { sub_account: task.subAccount, task_id: task.taskId }, { write: true });
    setTask(current => ({ ...current, submittedAction: taskAction }));
    setTaskAction(null);
    setDetail(null);
    await client.report({ form: 'batch', state: 'operation_accepted', taskId: task.taskId, operation: taskAction });
    setDetail(await readTask(task));
  }, { mutation: true });

  return <LockedFields locked={operation.busy || operation.uncertain}><main className="batch-page">
    <header className="batch-header"><div className="batch-header-inner"><div className="batch-brand">火山引擎 · 短信服务</div>
      <div className="batch-title-row"><div><h1>创建短信群发任务</h1><p>选择模板、上传名单并核对。创建任务后，仍需单独确认启动。</p></div></div>
    </div></header>
    <div className="batch-body"><Feedback operation={operation} /><div className="batch-sheet">
      {task ? <section className="batch-section"><Receipt title="群发任务已创建" id={task.taskId}><p>任务创建成功不等于已经发送。</p></Receipt>
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
      </section> : snapshot ? <section className="batch-section"><Confirm title="确认创建群发任务" submitLabel="确认创建任务" onBack={() => setSnapshot(null)} onSubmit={create} busy={operation.busy} disabled={operation.uncertain}>
        <Summary items={[
          ['任务名称', snapshot.name], ['消息组', groups.rows.find(row => row.subAccountId === snapshot.subAccount)?.subAccountName],
          ['签名', snapshot.signature], ['模板', previewTemplate?.TemplateName], ['名单文件', file?.name],
          ['名单数量', file?.totalCount], ['重复号码', file?.dupCount],
          ['发送时间', snapshot.scheduled ? new Intl.DateTimeFormat('zh-CN', { timeZone: 'Asia/Shanghai', dateStyle: 'medium', timeStyle: 'short', hour12: false }).format(new Date(snapshot.sendTime * 1000)) + '（北京时间）' : '启动后立即发送'],
          ['短信正文', snapshot.content ?? previewTemplate?.TemplateContent ?? previewTemplate?.Content],
        ]} />
        {file?.samples?.length > 0 && <details><summary>查看名单样例（前 {file.samples.length} 行）</summary>
          {file.samples.map((sample, index) => <Summary key={index} items={[["号码", sample.phone], ...Object.entries(sample.params)]} />)}
        </details>}
      </Confirm></section> : <>
        <section className="batch-section"><h2>任务与模板</h2><div className="form-grid">
          <Field label="任务名称" value={values.name} onChange={value => update('name', value)} required />
          <div><Choice label="消息组" value={values.subAccount} onChange={chooseGroup} disabled={operation.busy || operation.uncertain} options={groups.rows.map(row => [row.subAccountId, row.subAccountName || row.subAccountId])} />
            <More loaded={groups.rows.length} total={groups.total} onClick={() => operation.run(loadGroups)} disabled={operation.busy} /></div>
          <div><Choice label="短信签名" value={values.signature} onChange={chooseSignature} disabled={!values.subAccount || operation.busy || operation.uncertain}
            options={[...new Set(signatures.rows.map(row => row.Signature))].map(name => [name, name])} />
            <More loaded={signatures.rows.length} total={signatures.total} onClick={() => operation.run(() => loadSignatures(values.subAccount, signatures.page + 1))} disabled={operation.busy} /></div>
          <div><Choice label="群发模板" value={values.templateId} onChange={chooseTemplate} disabled={!values.signature || operation.busy || operation.uncertain}
            options={templates.rows.filter(row => ['CN_NTC', 'CN_MKT'].includes(row.ChannelType)).map(row => [row.TemplateId, row.TemplateName || row.TemplateId])} />
            <More loaded={templates.rows.length} total={templates.total} onClick={() => operation.run(() => loadTemplates(values.signature, templates.page + 1))} disabled={operation.busy} /></div>
        </div>
          {selected && <div className="batch-content-block"><p className="batch-message-content">{selected.TemplateContent ?? selected.Content}</p>
            {(selected.TaskFields ?? []).map(field => field.Name === 'content' && <Field key={field.Name} label={field.Label ?? '任务正文'} value={values.content} onChange={value => update('content', value)} multiline maxLength={field.MaxLength} required={field.Required} />)}
          </div>}
        </section>
        <section className="batch-section"><h2>发送名单</h2><p>请按当前模板的 CSV 示例填写，列名和顺序保持一致。</p>
          {demo && <><Button onClick={() => operation.run(() => client.downloadCsv(demo))}>下载名单模板</Button><details><summary>查看 / 复制 CSV 示例</summary><pre>{demo}</pre></details></>}
          <Files label="群发 CSV 名单" accept=".csv" value={file ? [file] : []} disabled={!demo || operation.busy || operation.uncertain}
            onSelect={files => operation.run(async () => setFile(await client.upload(files[0], { kind: 'recipients', sub_account: values.subAccount, template_id: values.templateId })), { mutation: true })} onRemove={() => setFile(null)} />
          {file && <p>已校验 {file.totalCount} 条记录，其中重复号码 {file.dupCount} 条。实际任务数量以创建结果为准。</p>}
        </section>
        <section className="batch-section"><h2>发送时间</h2><Radio.Group disabled={operation.busy || operation.uncertain} value={values.scheduled} onChange={value => update('scheduled', value)}
          options={[{ value: false, label: '启动后立即发送' }, { value: true, label: '定时发送' }]} />
          {values.scheduled && <Field label="发送时间（北京时间）" type="datetime-local" value={values.sendAt} onChange={value => update('sendAt', value)} />}
          <div className="batch-actions"><Button type="primary" loading={operation.busy} disabled={operation.uncertain} onClick={prepare}>核对群发任务</Button></div>
        </section>
      </>}
    </div></div>
  </main></LockedFields>;
}
