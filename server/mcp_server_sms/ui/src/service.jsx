import React, { useEffect, useState } from 'react';
import { Button } from '@arco-design/web-react';
import { Confirm, Feedback, Summary, useOperation } from './common.jsx';

const statusLabels = {
  available: '国内短信已开通，协议有效',
  activation_required: '等待开通',
  reopening_required: '等待重新开通',
  protocol_confirmation_required: '有待更新的协议',
  activation_pending: '开通请求已受理，等待状态更新',
  protocol_confirmation_pending: '协议签署请求已受理，等待状态更新',
  submission_in_progress: '已有请求正在提交，请刷新核对状态',
  submission_outcome_unknown: '上次提交结果待核对，请刷新状态或到控制台查看',
  protocol_confirmation_failed: '部分协议签署失败',
  activation_rejected: '协议已处理，开通请求未受理',
  product_not_allowed: '当前账号不支持开通此商品',
  product_forced_closed: '短信服务已被关闭，请到控制台核对',
  account_disabled: '账号已停用，请到控制台核对',
  arrears_closed: '短信服务因欠费关闭，请到控制台核对',
  expired_closed: '短信服务已到期，请到控制台核对',
  protocol_state_unknown: '存在未识别的协议，请到控制台核对',
  service_state_unknown: '当前服务状态待核对，请到控制台查看',
};
const pendingStates = new Set(['activation_pending', 'protocol_confirmation_pending']);

export function ServiceForm({ client }) {
  const [view, setView] = useState(null);
  const [submittedStatus, setSubmittedStatus] = useState(null);
  const operation = useOperation();
  const refresh = () => operation.run(async () => {
    const latest = await client.call('get_sms_service_onboarding');
    setView(latest);
    if (latest.status === 'available') {
      setSubmittedStatus(null);
      await client.report({ form: 'service', state: 'available' });
    }
  });
  useEffect(() => { refresh(); }, [client]);
  const submit = () => operation.run(async () => {
    const result = await client.call('submit_sms_service_onboarding', { confirmation: view.confirmation }, { write: true });
    setView(result);
    setSubmittedStatus(pendingStates.has(result.status) ? result.status : null);
    await client.report({ form: 'service', state: result.status, requestId: result.requestId });
  }, { mutation: true });
  const showLink = (title, url) => client.canOpenLinks?.()
    ? <Button type="text" disabled={operation.busy} onClick={() => operation.run(() => client.openLink(url))}>{title}</Button>
    : <span>{title}　<code style={{ overflowWrap: 'anywhere' }}>{url}</code></span>;
  const canConfirm = Boolean(view?.confirmation && !submittedStatus && !operation.uncertain);
  const renewal = view?.status === 'protocol_confirmation_required';

  return <div className="signature-shell"><main className="signature-page">
    <header className="signature-header"><div><span className="signature-eyebrow">火山引擎 · 短信服务</span>
      <h1>国内短信开通与协议更新</h1><p>核对当前账号与待签协议后确认办理。</p>
    </div></header>
    <Feedback operation={operation} />
    <section className="signature-panel">
      {view ? <Summary items={[
        ['账号主体', view.businessName || '以当前登录账号为准'],
        ['当前状态', statusLabels[view.confirmation && submittedStatus ? submittedStatus : view.status] ?? statusLabels.service_state_unknown],
        ...(view.requestId ? [['请求编号', view.requestId]] : []),
        ...(view.errorCode ? [['错误码', view.errorCode]] : []),
      ]} /> : <p>正在查询短信服务状态。</p>}
      {view?.failedDocuments?.length > 0 && <p>签署失败的协议编号 {view.failedDocuments.join('、')}。请刷新后核对。</p>}
      {view?.consoleUrl && showLink('打开短信控制台', view.consoleUrl)}
      <Button loading={operation.busy} onClick={refresh}>刷新服务状态</Button>
    </section>
    {canConfirm && <section className="signature-panel">
      <Confirm key={view.confirmation} title={renewal ? '确认签署更新协议' : '确认开通国内短信'}
        consentLabel="我已阅读并同意以上协议及计费说明" submitLabel={renewal ? '确认签署协议' : '确认签署并开通'}
        busy={operation.busy} onSubmit={submit}>
        <ul>{view.protocols.map(item => <li key={item.id}>{showLink(item.title, item.url)}</li>)}</ul>
        <p>短信费用按当前账号合同和官方计费说明结算。</p>
        {showLink('查看国内短信计费说明', view.pricingUrl)}
      </Confirm>
    </section>}
  </main></div>;
}
