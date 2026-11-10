import React, { useState } from 'react';
import { Button } from '@arco-design/web-react';
import { Confirm, Field, Receipt, Summary } from './common.jsx';
import { OperationError, page, required } from './client.js';

const deliveryLabels = {
  1: '已发送，等待回执',
  2: '发送失败',
  3: '已收到成功回执',
};

export function BatchTestSms({ client, operation, subAccount, signature, template, variables, trial, setTrial }) {
  const [mobile, setMobile] = useState('');
  const [params, setParams] = useState({});
  const [snapshot, setSnapshot] = useState(null);
  const receipt = trial?.receipt;
  const delivery = trial?.delivery;
  const templateContent = template.TemplateContent ?? template.Content;

  const prepare = () => operation.run(() => {
    if (!/^1[3-9][0-9]{9}$/.test(mobile)) throw new OperationError('请填写有效的中国大陆测试手机号。');
    required(templateContent, '模板正文不完整，请重新选择模板。');
    const templateParams = Object.fromEntries(variables.map(name => [
      name, required(Object.hasOwn(params, name) ? params[name] : undefined, '请填写所有试发变量。'),
    ]));
    setSnapshot({
      sub_account: subAccount, signature, template_id: template.TemplateId,
      template_content: templateContent, mobile, template_params: templateParams,
    });
  });
  const readDelivery = async result => {
    const logs = await client.call('list_send_logs', {
      sub_account: subAccount, message_id: result.messageId,
      from_time: result.requestedAt, to_time: Math.max(result.requestedAt, Math.floor(Date.now() / 1000)) + 1,
      page: 1, page_size: 20,
    });
    const matches = page(logs).rows.filter(row => (row.messageId ?? row.MessageId ?? row.MessageID) === result.messageId);
    const match = matches.length === 1 ? matches[0] : null;
    setTrial({
      receipt: result,
      delivery: match && { status: match.status ?? match.Status, errorCode: match.errorCode ?? match.ErrorCode },
    });
  };
  const send = () => operation.run(async () => {
    const result = await client.call('send_batch_test_sms', { request: snapshot }, { write: true });
    if (typeof result?.messageId !== 'string' || !result.messageId || !Number.isInteger(result.requestedAt)) {
      throw new OperationError('未收到可核对的试发回执，请查询发送记录。', { unknown: true });
    }
    setTrial({ receipt: result, delivery: null }); setSnapshot(null); setMobile(''); setParams({});
    await readDelivery(result);
  }, { mutation: true });

  return <section className="batch-section">
    <h2>发送测试短信</h2>
    {snapshot ? <Confirm title="核对单条试发" submitLabel="确认发送测试短信"
      busy={operation.busy} disabled={operation.uncertain} onBack={() => setSnapshot(null)} onSubmit={send}>
      <p>确认后向这个测试号码发送，费用按当前账号计费。</p>
      <Summary items={[
        ['测试手机号', snapshot.mobile], ['签名', snapshot.signature], ['模板正文', snapshot.template_content],
        ...Object.entries(snapshot.template_params).map(([name, value]) => [`变量 ${name}`, value]),
      ]} />
    </Confirm> : <>
      <p>先用自己的号码确认签名、模板和变量效果。</p>
      <div className="batch-param-grid">
        <Field label="测试手机号" value={mobile} onChange={setMobile} maxLength={11} />
        {variables.map(name => <Field key={name} label={`试发变量 ${name}`} value={Object.hasOwn(params, name) ? params[name] : ''}
          onChange={value => setParams(current => ({ ...current, [name]: value }))} />)}
      </div>
      <Button disabled={operation.busy || operation.uncertain || !mobile} onClick={prepare}>核对测试短信</Button>
    </>}
    {receipt && <Receipt title="测试短信已受理" id={receipt.messageId}>
      <Summary items={[
        ['发送状态', delivery ? deliveryLabels[delivery.status] ?? '请核对发送记录' : '暂未查到对应记录'],
        ...(delivery?.errorCode ? [['错误码', delivery.errorCode]] : []),
      ]} />
      <Button loading={operation.busy} onClick={() => operation.run(() => readDelivery(receipt))}>刷新试发回执</Button>
    </Receipt>}
  </section>;
}
