import React, { useState } from 'react';
import { Alert, Button, Input, Spin } from '@arco-design/web-react';
import { IconRefresh } from '@arco-design/web-react/icon';
import { Confirm, Summary } from './common.jsx';
import { BatchDetails, BatchField, BatchHeading, batchTime } from './batch-controls.jsx';
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
  const locked = operation.busy || operation.uncertain;

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
      delivery: match && { status: match.status ?? match.Status, errorCode: match.errorCode ?? match.ErrorCode,
        errorMessage: match.errorMessage ?? match.ErrorMessage, count: match.count ?? match.Count,
        sendTime: match.sendTime ?? match.SendTime, receiptTime: match.receiptTime ?? match.ReceiptTime },
    });
  };
  const send = () => operation.run(async () => {
    const result = await client.call('send_batch_test_sms', { request: {
      sub_account: snapshot.sub_account, signature: snapshot.signature, template_id: snapshot.template_id,
      mobile: snapshot.mobile, template_params: snapshot.template_params,
    } }, { write: true });
    if (typeof result?.messageId !== 'string' || !result.messageId || !Number.isInteger(result.requestedAt)) {
      throw new OperationError('未收到可核对的试发回执，请查询发送记录。', { unknown: true });
    }
    setTrial({ receipt: result, delivery: null }); setSnapshot(null); setMobile(''); setParams({});
    await readDelivery(result);
  }, { mutation: true });

  return <section className="batch-section">
    <BatchHeading title="发送测试短信" description="可发送一条测试短信确认签名、模板和变量替换后的触达效果。" />
    {snapshot ? <Confirm title="核对单条试发" submitLabel="确认发送测试短信"
      busy={operation.busy} disabled={operation.uncertain} onBack={() => setSnapshot(null)} onSubmit={send}>
      <p>确认后向这个测试号码发送，费用按当前账号计费。</p>
      <Summary items={[
        ['测试手机号', snapshot.mobile], ['签名', snapshot.signature], ['模板正文', snapshot.template_content],
        ...Object.entries(snapshot.template_params).map(([name, value]) => [`变量 ${name}`, value]),
      ]} />
    </Confirm> : <>
      <div className="batch-test-phone"><BatchField label="测试手机号">
        <div className="batch-inline-control">
        <Input aria-label="测试手机号" value={mobile} onChange={setMobile} disabled={locked}
          maxLength={20} placeholder="请输入中国大陆手机号" />
        <Button htmlType="button" disabled={locked || !mobile} onClick={prepare}>发送测试短信</Button>
      </div></BatchField></div>
      <div className="batch-test-params"><div className="batch-field-label">测试所需参数</div>
        {!variables.length && <div className="batch-none">无</div>}
        <div className="batch-param-grid">
        {variables.map(name => <BatchField key={name} label={name}
          value={Object.hasOwn(params, name) ? params[name] : ''} disabled={locked}
          placeholder={`请输入 ${name}`} onChange={value => setParams(current => ({ ...current, [name]: value }))} />)}
      </div></div>
    </>}
    {receipt && <><Alert className="batch-test-result" type="success" showIcon
      content="测试短信已提交，请在测试手机上确认触达效果。" />
      <div className="batch-test-log">
      <div className="batch-test-log-header"><div><div className="batch-field-label">发送结果</div>
        <div className="batch-field-help">提交后自动查询；运营商回执可能稍后到达。</div></div>
        <Button htmlType="button" type="text" icon={<IconRefresh />} loading={operation.busy} disabled={operation.busy}
          onClick={() => operation.run(() => readDelivery(receipt))}>刷新发送结果</Button>
      </div>
      <Spin loading={operation.busy}>{delivery ? <BatchDetails items={[
        ['Message ID', receipt.messageId],
        ['发送状态', deliveryLabels[delivery.status] ?? '请核对发送记录'],
        ['发送时间', batchTime(delivery?.sendTime)], ['回执时间', batchTime(delivery?.receiptTime)],
        ['计费条数', delivery?.count], ['错误码', delivery?.errorCode], ['错误信息', delivery?.errorMessage],
      ]} /> : <Alert type="info" showIcon content="暂未查询到发送结果，可稍后刷新。" />}</Spin>
    </div></>}
  </section>;
}
