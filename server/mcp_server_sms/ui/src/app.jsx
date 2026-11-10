import React from 'react';
import { Alert } from '@arco-design/web-react';
import { QualificationForm } from './qualification.jsx';
import { SignatureForm } from './signature.jsx';
import { TrafficForm } from './traffic.jsx';
import { BatchForm } from './batch.jsx';
import { ServiceForm } from './service.jsx';
import { Receipt } from './common.jsx';

const forms = {
  qualification: QualificationForm, signature: SignatureForm, traffic: TrafficForm,
  batch: BatchForm, service: ServiceForm,
};

export function SmsApp({ client, toolResult, ready, supported, error }) {
  if (error) return <div className="sms-boot"><Alert type="warning" content={error} /></div>;
  if (!ready) return <div className="sms-boot">正在连接短信表单…</div>;
  if (!supported) return <div className="sms-boot"><Alert type="warning" content="当前客户端不支持表单操作，请通过短信控制台或文本工具继续。已提交的操作不要重复提交。" /></div>;
  const initial = toolResult?.structuredContent;
  const Form = forms[initial?.form];
  if (!Form) return <div className="sms-boot">请从对话中打开短信业务表单。</div>;
  // 历史结果只展示收据；不能因为 iframe 重建而再次执行申请或创建任务。
  if (initial.mode !== 'input') return <div className="sms-app"><Receipt title="此操作已返回结果"
    id={typeof initial.result === 'number' ? initial.result : initial.result?.applyId ?? initial.result?.taskId}>
    <p>请使用状态查询核对审核、任务和发送结果；恢复页面不会重新提交。</p>
  </Receipt></div>;
  return <div className="sms-app"><Form client={client} prefill={toolResult._meta?.['sms/form']?.prefill} /></div>;
}
