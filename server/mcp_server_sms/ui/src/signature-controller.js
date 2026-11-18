import { OperationError, materialPreview, page, required } from './client.js';
import { messageGroupSchema, signatureQualificationSchema } from './contracts.js';

// 表单规则来自 byted-sms-sender 1.4.6；查询与提交沿用当前 MCP 契约。
export const sources = [[1, '公司全称／简称'], [2, 'APP 全称'], [3, '商标全称']];
export const purposes = [
  [1, '自用', '签名归属于当前火山账号对应的企业'],
  [2, '他用', '签名归属于非当前火山账号对应的企业'],
];
export const channels = [['CN_OTP', '验证码短信'], ['CN_NTC', '通知短信'], ['CN_MKT', '营销短信']];
export const maxFiles = 5;
export const materialTypes = {
  other: {
    title: '更多资料', hint: '其他有助于审核的证明文件（选填）',
    accept: '.png,.jpg,.jpeg,.doc,.docx,.gif,.zip',
    description: '支持 png、jpg、jpeg、doc、docx、gif、zip 文件',
  },
  app: {
    title: 'APP ICP 备案截图', hint: '备案号和附件至少填写一项',
    accept: '.zip,.pdf,.jpg,.png,.jpeg',
    description: '支持 zip、pdf、jpg、png、jpeg 文件',
  },
  trademark: {
    title: '商标证书文件', hint: '为提升审核效率，建议上传商标文件或截图',
    accept: '.zip,.pdf,.jpg,.png,.jpeg',
    description: '支持 zip、pdf、jpg、png、jpeg 文件',
  },
};

export function validateSignatureContent(content) {
  if (!content) return '请输入签名内容';
  if (content.trim() !== content) return '签名首尾不能包含空格';
  if (content.length > 25) return '签名最多支持25个字符';
  if (content.length < 2) return '签名最少2个字符';
  if (!/^[\u4E00-\uFA29\uE7C7-\uE7F3a-zA-Z0-9()（）:：\-.'·+&\s]{2,25}$/.test(content)) {
    return '签名存在不支持的特殊符号';
  }
  if (/http:|https:|www\.|\.com/.test(content)) return '签名不能包含网址';
  if (/^\d+$/.test(content)) return '签名不支持纯数字';
  if (/1[3-9]\d{9}|0\d{2,3}-\d{5,8}/.test(content)) return '签名不能包含联系方式';
  if (!/[\u4E00-\uFA29\uE7C7-\uE7F3a-zA-Z0-9]/.test(content)) {
    return '签名至少存在一个中文或英文或数字';
  }
  return '';
}

export function signatureBaseErrors(values, scope) {
  const errors = {};
  if (!sources.some(([source]) => source === values.source)) errors.source = '请选择签名类型';
  if (!purposes.some(([purpose]) => purpose === values.purpose)) errors.purpose = '请选择签名归属类型';
  const contentError = validateSignatureContent(values.content);
  if (contentError) errors.content = contentError;
  if (!scope) errors.groupScope = '请选择是否限定可使用消息组';
  if (scope === 'limited' && !values.subAccounts?.length) errors.subAccounts = '请选择消息组';
  if (values.desc?.length > 300) errors.desc = '申请说明最多 300 字';
  return errors;
}

export function signaturePreview(values, qualification, scope, attachments) {
  const contentError = validateSignatureContent(values.content);
  if (contentError) throw new OperationError(contentError);
  if (!sources.some(([source]) => source === values.source)) throw new OperationError('请选择签名类型');
  if (!signatureQualificationSchema.safeParse(qualification).success) {
    throw new OperationError('请选择审核通过的资质。');
  }
  if (values.purpose !== undefined && values.purpose !== qualification.purpose) {
    throw new OperationError('自用／他用需要与所选资质一致。');
  }
  const businessName = required(qualification.businessCertificateName, '关联资质缺少营业证件名称，请重新查询。');
  required(scope, '请选择消息组范围。');
  if (scope === 'limited' && !values.subAccounts?.length) throw new OperationError('请选择绑定的消息组。');
  if (new Set(values.subAccounts ?? []).size !== (values.subAccounts ?? []).length) {
    throw new OperationError('消息组不能重复。');
  }
  if (values.source === 2 && !values.appIcp?.appIcpFilling && !attachments.app.length) {
    throw new OperationError('请填写 APP ICP 备案号或上传备案截图。');
  }
  if (values.source === 3) required(values.trademark?.trademarkNumber, '请填写商标注册号。');
  if (values.desc?.length > 300) throw new OperationError('申请说明最多 300 字。');
  if (Object.values(attachments).flat().length > maxFiles) throw new OperationError('本次最多上传 5 份材料。');
  const preview = materialPreview(materialFile => ({
    content: values.content, purpose: qualification.purpose, signatureIdentificationID: qualification.id,
    source: values.source, channelTypes: channels.map(([value]) => value),
    isLimitSubAccount: scope === 'all' ? 0 : 1,
    subAccounts: scope === 'all' ? [] : [...values.subAccounts], from: 'vconsole',
    ...(values.desc !== undefined ? { desc: values.desc } : {}),
    ...(values.projectName !== undefined ? { projectName: values.projectName } : {}),
    ...(values.source === 2 ? { appIcp: {
      ...(values.appIcp?.appIcpFilling !== undefined ? { appIcpFilling: values.appIcp.appIcpFilling } : {}),
      appIcpFileList: attachments.app.map(file => materialFile(file, 16)),
    } } : {}),
    ...(values.source === 3 ? { trademark: {
      trademarkCn: values.trademark?.trademarkCn ?? '', trademarkEn: values.trademark?.trademarkEn ?? '',
      trademarkNumber: values.trademark.trademarkNumber,
      trademarkFileList: attachments.trademark.map(file => materialFile(file, 17)),
    } } : {}),
    uploadFileList: attachments.other.map(file => materialFile(file, 6)),
  }));
  return { ...preview, businessName, nameRisk: !businessName.includes(values.content) };
}

export async function loadSignatureQualifications(client, prefill) {
  const result = signatureQualificationSchema.array().nullable().safeParse(
    await client.query('GetApplySignatureBind', {}),
  );
  if (!result.success) throw new OperationError('资质候选返回不完整，请重新查询。');
  const rows = result.data ?? [];
  const id = prefill?.signatureIdentificationID;
  const selected = id === undefined ? rows.length === 1 ? rows[0] : undefined : rows.find(row => row.id === id);
  return { rows, selected, unavailable: id !== undefined && !selected };
}

export async function loadSignatureGroups(client) {
  const rows = [];
  for (let index = 1; index <= 100; index += 1) {
    const result = page(await client.query('GetSubAccountListForAgent', {
      pageIndex: index, pageSize: 100,
    }), messageGroupSchema);
    rows.push(...result.rows);
    if (rows.length >= result.total) return rows;
    if (!result.rows.length) break;
  }
  throw new OperationError('资源列表未完整读取，请缩小查询范围。');
}
