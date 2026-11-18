import React, { useEffect, useRef, useState } from 'react';
import { Button, Checkbox, Result, Spin } from '@arco-design/web-react';
import { IconMessage } from '@arco-design/web-react/icon';
import { Feedback, useOperation } from './common.jsx';
import { OperationError } from './client.js';

const presentations = {
  activation: {
    title: '开通国内短信服务', subtitle: '阅读并同意相关协议后开通服务。',
    sectionTitle: '服务协议', hint: '请逐项阅读当前版本的协议。',
    consentText: '我已阅读并同意以上全部协议，并确认开通国内短信服务。',
    submitLabel: '同意协议并开通',
    cancelTitle: '已取消开通', cancelDescription: '本次未提交国内短信服务开通请求。',
    successTitle: '国内短信服务已开通', successDescription: '服务与相关协议已经生效。',
    failureTitle: '国内短信服务开通未完成',
  },
  renewal: {
    title: '重新签署短信服务协议',
    subtitle: '短信服务协议已更新，请阅读并重新签署后继续使用国内短信服务。',
    sectionTitle: '更新协议', hint: '请逐项阅读以下更新后的协议。',
    consentText: '我已阅读并同意以上更新协议。', submitLabel: '同意并重新签署',
    cancelTitle: '已取消重新签署', cancelDescription: '本次未重新签署更新后的短信服务协议。',
    successTitle: '短信服务协议已重新签署', successDescription: '更新后的协议已生效，可继续使用国内短信服务。',
    failureTitle: '短信服务协议重新签署未完成',
  },
};

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
  activation_error: '开通接口返回错误',
  product_not_allowed: '当前账号不支持开通此商品',
  product_forced_closed: '短信服务已被关闭，请到控制台核对',
  account_disabled: '账号已停用，请到控制台核对',
  arrears_closed: '短信服务因欠费关闭，请到控制台核对',
  expired_closed: '短信服务已到期，请到控制台核对',
  protocol_state_unknown: '存在未识别的协议，请到控制台核对',
  service_state_unknown: '当前服务状态待核对，请到控制台查看',
};
const submittableStates = new Set(['activation_required', 'reopening_required', 'protocol_confirmation_required']);
const pendingStates = new Set(['activation_pending', 'protocol_confirmation_pending', 'submission_in_progress', 'submission_outcome_unknown']);

function resultDisplay(status, presentation, needsRefresh, uncertain) {
  if (status === 'available') return { status: 'success', title: presentation.successTitle, description: presentation.successDescription };
  if (uncertain || status === 'submission_outcome_unknown') return {
    status: 'warning', title: '操作结果待核实', description: statusLabels.submission_outcome_unknown,
  };
  if (pendingStates.has(status)) return { status: 'info', title: '请求已提交', description: statusLabels[status] };
  if (needsRefresh || ['protocol_confirmation_failed', 'activation_error'].includes(status)) return {
    status: 'error', title: presentation.failureTitle,
    description: needsRefresh ? '请刷新服务状态，重新阅读并确认当前协议。' : statusLabels[status],
  };
  return { status: 'warning', title: '当前无法办理', description: statusLabels[status] ?? statusLabels.service_state_unknown };
}

export function ServiceForm({ client }) {
  const [view, setView] = useState(null);
  const [intent, setIntent] = useState('activation');
  const [agreed, setAgreed] = useState(false);
  const [cancelled, setCancelled] = useState(false);
  const [needsRefresh, setNeedsRefresh] = useState(false);
  const live = useRef(true);
  const ended = useRef(false);
  const pending = useRef(null);
  const operation = useOperation();
  const refresh = () => operation.run(async () => {
    const latest = await client.call('get_sms_service_onboarding');
    if (!live.current || ended.current) return;
    setAgreed(false);
    setNeedsRefresh(false);
    // 已受理或未知的写入不能被暂未更新的可提交状态重新解锁。
    const stale = pending.current && submittableStates.has(latest.status);
    if (!pending.current) {
      setIntent(['protocol_confirmation_required', 'protocol_confirmation_pending'].includes(latest.status) ? 'renewal' : 'activation');
    }
    if (pendingStates.has(latest.status)) pending.current = latest.status;
    setView(previous => stale ? { ...latest, status: pending.current, requestId: previous?.requestId } : latest);
    if (latest.status === 'available') {
      pending.current = null;
      await client.report({ form: 'service', state: 'available' });
    }
  });
  useEffect(() => {
    live.current = true;
    refresh();
    return () => { live.current = false; };
  }, [client]);
  const presentation = presentations[intent];
  const canConfirm = Boolean(view?.confirmation && view.protocols?.length
    && submittableStates.has(view.status) && !pending.current && !needsRefresh && !operation.uncertain && !cancelled);
  const submit = () => operation.run(async () => {
    if (!agreed || !canConfirm || ended.current) return;
    let result;
    try {
      result = await client.call('submit_sms_service_onboarding', { confirmation: view.confirmation }, { write: true });
    } catch (cause) {
      if (live.current) {
        setAgreed(false);
        setNeedsRefresh(true);
        if (!(cause instanceof OperationError) || cause.unknown) pending.current = 'submission_outcome_unknown';
      }
      throw cause;
    }
    if (!live.current) return;
    setAgreed(false);
    if (pendingStates.has(result.status)) pending.current = result.status;
    setView(result);
    setNeedsRefresh(submittableStates.has(result.status));
    await client.report({ form: 'service', state: result.status, requestId: result.requestId });
  }, { mutation: true });
  const abandon = () => operation.run(async () => {
    if (ended.current || pending.current || operation.uncertain) return;
    ended.current = true;
    setAgreed(false);
    setCancelled(true);
    setView(null);
    await client.report({ form: 'service', state: 'abandoned' });
  });
  const showLink = (title, url) => client.canOpenLinks?.()
    ? <Button className="service-link" type="text" htmlType="button" disabled={operation.busy}
      onClick={() => operation.run(() => client.openLink(url))}>{title}</Button>
    : <span className="service-link-fallback">{title}<code>{url}</code></span>;
  const feedback = <><Feedback operation={operation} />
    {view?.failure && <Feedback operation={{
      error: { ...view.failure.error, requestId: view.failure.request_id, httpStatus: view.failure.error?.http_status },
      uncertain: Boolean(view.failure.error?.outcome_unknown),
    }} />}</>;
  const support = <footer className="service-support">
    {view?.businessName && <p>账号主体：{view.businessName}</p>}
    {view?.requestId && <p>请求编号：{view.requestId}</p>}
    {view?.errorCode != null && <p>错误码：{view.errorCode}</p>}
    {view?.failedDocuments?.length > 0 && <p>签署失败的协议编号 {view.failedDocuments.join('、')}。请刷新后核对。</p>}
    {view?.pricingUrl && <div>{showLink('查看国内短信计费说明', view.pricingUrl)}</div>}
    <div className="service-support-actions">
      {view?.consoleUrl && showLink('打开短信控制台', view.consoleUrl)}
      <Button htmlType="button" loading={operation.busy} disabled={operation.busy} onClick={refresh}>刷新服务状态</Button>
    </div>
  </footer>;

  if (cancelled) return <main className="service-page"><section className="service-result">
    <Result status="info" title={presentation.cancelTitle} subTitle={presentation.cancelDescription} />{feedback}
  </section></main>;
  if (!view) return <main className="service-page">
    <div className="service-loading">{operation.error ? feedback : <Spin dot tip="正在查询短信服务状态。" />}</div>
    {operation.error && support}
  </main>;
  if (!canConfirm) {
    const display = resultDisplay(view.status, presentation, needsRefresh, operation.uncertain);
    return <main className="service-page"><section className="service-result">
      <Result status={display.status} title={display.title} subTitle={display.description} />
      {feedback}{support}
    </section></main>;
  }
  return <main className="service-page">
    <header className="service-header">
      <div className="service-brand">火山引擎短信</div>
      <h1>{presentation.title}</h1><p>{presentation.subtitle}</p>
    </header>
    <section className="service-panel">
      <div className="service-product">
        <div className="service-product-icon" aria-hidden="true"><IconMessage /></div>
        <div><h2>国内短信</h2><p>支持向中国大陆号码发送验证码短信、通知短信、推广/营销短信。</p></div>
      </div>
      <div className="service-content">
        <h2>{presentation.sectionTitle}</h2><p className="service-hint">{presentation.hint}</p>
        <ol className="service-protocols">{view.protocols.map((protocol, index) => <li key={protocol.id ?? protocol.url}>
          <span className="service-protocols-index">{index + 1}</span>{showLink(protocol.title, protocol.url)}
        </li>)}</ol>
        <div className="service-consent"><Checkbox checked={agreed} disabled={operation.busy} onChange={setAgreed}>
          {presentation.consentText}
        </Checkbox></div>
        {feedback}
        <div className="service-actions">
          <Button htmlType="button" disabled={operation.busy} onClick={abandon}>取消</Button>
          <Button htmlType="button" type="primary" loading={operation.busy} disabled={!agreed || operation.busy} onClick={submit}>
            {presentation.submitLabel}
          </Button>
        </div>
      </div>
    </section>
    {support}
  </main>;
}
