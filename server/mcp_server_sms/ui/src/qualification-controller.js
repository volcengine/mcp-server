import { MAX_UPLOAD_BYTES, OperationError, checkedTicket, materialPreview } from './client.js';
import { toByteArray } from 'base64-js';
import config from '../../src/mcp_server_sms/form_config.json';

// Port of byted-sms-sender 1.4.6 scripts/qualification_wizard.py.
// Drafts stay in this iframe; only existing MCP tools and direct material uploads cross the bridge.
export const rankFields = ['isOnlyTwoElement', 'isSkipOtherUse', 'needOtherUseCheck',
  'operatorThreeElement', 'needOperatorImage', 'needOperatorMobile',
  'responsibleThreeElement', 'needResponsibleImage', 'needResponsibleMobile',
  'needBusinessCertificateImage'];
const personFiles = { operator: [8, 9], responsible: [10, 11], legal: [18, 19] };
const legalFiles = { 1: 12, 2: 13, 3: 14, 4: 15, 9: 6 };
const labels = { legal: '法人', operator: '经办人', responsible: '责任人' };
const businessKeys = ['businessCertificateType', 'businessCertificateName',
  'unifiedSocialCreditIdentifier', 'legalPersonName',
  'businessCertificateValidityPeriodStart', 'businessCertificateValidityPeriodEnd'];
const personKeys = ['certificateType', 'personName', 'personIDCard', 'personMobile'];
const pick = (source, keys) => Object.fromEntries(keys.map(key => [key, source?.[key]]));
const pair = person => Boolean(person?.images?.front && person?.images?.back);
const fail = message => { throw new OperationError(message); };
function text(value, label, max = 256, optional = false) {
  const result = typeof value === 'string' ? value.trim() : '';
  if ((!result && !optional) || result.length > max) fail(`请填写正确的${label}。`);
  return result;
}
function date(value) {
  const parsed = new Date(value);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value ?? '')
    || Number.isNaN(parsed.getTime()) || parsed.toISOString().slice(0, 10) !== value) fail('请选择正确的营业证件有效期。');
  return value;
}
function mobile(value, required) {
  const result = text(value, '手机号', 11, !required);
  if (result && !/^1[3-9]\d{9}$/.test(result)) fail('请输入正确的 11 位手机号。');
  return result;
}
function identity(value, required) {
  const result = text(value, '身份证号', 18, !required).toUpperCase();
  if (result && !/^\d{17}[\dX]$/.test(result)) fail('请输入正确的 18 位身份证号。');
  return result;
}
function materialName(value, source, businessName) {
  const name = text(value, '资质名称', 20, true);
  return source === 'manual' && name ? name : text(businessName, '资质名称（最多 20 个字）', 20);
}
function uploadItem(file, key, index) {
  const item = { uid: `${key}-${index}`, name: file.name, originFile: file, status: 'init' };
  if (typeof file.data === 'string' && file.data.length <= Math.ceil(MAX_UPLOAD_BYTES / 3) * 4) {
    try {
      const blob = new Blob([toByteArray(file.data)], { type: `image/${file.name.split('.').pop()}` });
      item.url = item.thumbUrl = item.__localPreviewUrl = URL.createObjectURL(blob);
    } catch { /* Invalid prefill stays a draft and is validated when the customer uploads. */ }
  }
  return item;
}
function personDraft(person = {}) {
  return { ...pick(person, personKeys), certificateType: person.certificateType ?? 0,
    personName: person.personName ?? '', personIDCard: person.personIDCard ?? '',
    personMobile: person.personMobile ?? '' };
}

export class QualificationController {
  constructor(client, prefill = {}) {
    this.client = client;
    this.rank = null;
    this.account = null;
    this.revision = 0;
    this.baseSaved = false;
    this.purpose = prefill.purpose ?? 1;
    this.materialName = prefill.materialName ?? '';
    this.materialNameSource = prefill.materialName ? 'manual' : 'auto';
    this.sameOperator = prefill.sameOperator ?? null;
    this.legalAcknowledged = false;
    this.authorizationAcknowledged = false;
    this.sections = {};
    this.pending = {};
    this.checks = {};
    this.verifications = {};
    this.sentAt = {};
    this.initialFiles = {};
    this.queue = Promise.resolve();
    this.done = false;
    const add = (key, files) => {
      this.initialFiles[key] = (files ?? []).filter(Boolean).map((file, index) => uploadItem(file, key, index));
    };
    if (prefill.businessInfo) {
      this.sections.business = pick(prefill.businessInfo, businessKeys);
      this.sections.business.businessCertificateType ??= 1;
      if (/长期|永久/.test(this.sections.business.businessCertificateValidityPeriodEnd ?? '')) {
        this.sections.business.businessCertificateValidityPeriodEnd = '2099-12-31';
      }
      add('business', [prefill.businessInfo.businessCertificate]);
    }
    for (const [role, person] of Object.entries({
      legal: prefill.includeLegal === false ? undefined : prefill.legalPerson,
      operator: prefill.operatorPerson, responsible: prefill.responsiblePersonInfo,
    })) {
      if (!person) continue;
      this.sections[role] = personDraft(person);
      if (role === 'legal') this.sections.legal.personName = this.sections.business?.legalPersonName ?? '';
      const files = person.personCertificate;
      add(`${role}Front`, [files?.front]);
      add(`${role}Back`, [files?.back]);
      if (role === 'legal') add('legalOther', files?.documents ?? [files?.document]);
    }
    add('power', prefill.powerOfAttorney);
    add('otherMaterials', prefill.otherMaterials);
    // Bind a stable request function for the reference React component's effects.
    this.request = (path, options = {}) => {
      const task = this.queue.then(() => this.dispatch(path, options));
      this.queue = task.catch(() => {});
      return task.catch(error => {
        error.outcomeUnknown = Boolean(error.unknown);
        if (error.requestId && !error.message.includes(error.requestId)) {
          error.message += `（排障编号：${error.requestId}）`;
        }
        throw error;
      });
    };
  }

  requirement(role, kind) {
    if (role === 'legal') return false;
    const prefix = role === 'operator' ? 'Operator' : 'Responsible';
    return kind === 'image' ? this.rank[`need${prefix}Image`]
      : this.rank[`${role}ThreeElement`] || this.rank[`need${prefix}Mobile`];
  }

  clearPending(fileKey) {
    const identitySlot = fileKey.match(/^(legal|operator|responsible)(Front|Back)$/);
    if (identitySlot) {
      const [, role, side] = identitySlot;
      if (this.pending[role]?.images) delete this.pending[role].images[side.toLowerCase()];
      if (this.pending[role]) delete this.pending[role].recognizedName;
    } else if (fileKey === 'legalOther') {
      if (this.pending.legal) delete this.pending.legal.documents;
    } else delete this.pending[fileKey === 'power' ? 'power' : fileKey];
  }

  verified(role) {
    if (role === 'responsible' && this.sameOperator) role = 'operator';
    const person = this.sections[role];
    return !this.account || this.account.userType !== 'smb' || !person?.personMobile
      || this.verifications[role]?.mobile === person.personMobile && this.verifications[role]?.verified === true;
  }

  state() {
    const sections = Object.fromEntries(Object.keys(personFiles).map(role => [role, Boolean(this.sections[role])]));
    if (this.sameOperator) sections.responsible = sections.operator;
    const checks = Object.fromEntries(['business', ...Object.keys(personFiles)].map(role => {
      const check = this.checks[role];
      return [role, check ? { attempted: true, matched: check.matched,
        canContinue: role === 'business' || check.matched, forceSkip: check.manualReview === true,
        status: check.status, ...(check.error ? { error: check.error } : {}) }
        : { attempted: false, matched: false, canContinue: false }];
    }));
    if (this.sameOperator) checks.responsible = { ...checks.operator };
    const people = Object.fromEntries(Object.entries(this.sections).filter(([role]) => role in personFiles)
      .map(([role, person]) => [role, { ...pick(person, personKeys),
        hasImages: pair(person), hasIdentityImages: pair(person), hasDocuments: Boolean(person.documents?.length) }]));
    const business = this.sections.business;
    const legalCheckRequired = Boolean(this.sections.legal?.certificateType === 0 && this.sections.legal.personIDCard);
    const powerOfAttorneyRequired = this.purpose === 2 && this.rank?.needOtherUseCheck === true;
    return {
      revision: this.revision, baseSaved: this.baseSaved, materialSaved: Boolean(this.materialName),
      materialName: this.materialName, materialNameSource: this.materialNameSource,
      purpose: this.purpose, sameOperator: this.sameOperator,
      legalAcknowledged: this.legalAcknowledged, authorizationAcknowledged: this.authorizationAcknowledged,
      sections, businessSaved: Boolean(business), powerOfAttorneyRequired,
      powerOfAttorneySaved: Boolean(this.sections.power), otherMaterialCount: this.sections.otherMaterials?.length ?? 0,
      authorizer: business?.businessCertificateName ?? '',
      authorizee: this.purpose === 2 ? this.account?.businessName ?? '' : '',
      legalCheckRequired, rank: this.rank, mobileVerificationRequired: this.account?.userType === 'smb',
      mobileVerifications: { operator: this.verified('operator'), responsible: this.verified('responsible') },
      savedData: { business: business ? { ...pick(business, businessKeys), hasImage: Boolean(business.image) } : {}, people },
      checks,
      readyForPreview: Boolean(this.baseSaved && business && sections.operator && sections.responsible
        && checks.business.canContinue && checks.operator.matched && checks.responsible.matched
        && (!legalCheckRequired || checks.legal.matched) && this.verified('operator') && this.verified('responsible')
        && this.materialName && this.legalAcknowledged && (!powerOfAttorneyRequired || this.sections.power)
        && (this.purpose !== 2 || this.authorizationAcknowledged && this.account?.businessName)),
    };
  }

  preview() {
    if (!this.state().readyForPreview) fail('请先完成必填材料和信息校验；他用资质可能还需要授权委托书。');
    const business = this.sections.business;
    return {
      revision: this.revision, materialName: this.materialName, purpose: this.purpose === 2 ? '他用' : '自用',
      powerOfAttorney: this.sections.power ? '已提供' : '无需提供',
      authorization: this.purpose === 2 ? { authorizer: business.businessCertificateName,
        authorizee: this.account.businessName, otherMaterialCount: this.sections.otherMaterials?.length ?? 0 } : null,
      business: pick(business, businessKeys),
      people: Object.fromEntries(Object.keys(personFiles).flatMap(role => {
        const person = this.sections[role === 'responsible' && this.sameOperator ? 'operator' : role];
        return person ? [[role, { ...pick(person, personKeys), label: labels[role],
          reusedFromOperator: role === 'responsible' && this.sameOperator }]] : [];
      })),
      checks: { business: this.checks.business.matched ? '通过' : '未通过自动校验，将转人工审核',
        legal: this.checks.legal?.matched ? '通过' : '无需校验', operator: '通过',
        responsible: this.sameOperator ? '同经办人，复用经办人校验' : '通过' },
    };
  }

  submission() {
    this.preview();
    const business = this.sections.business;
    return materialPreview(material => {
      const person = (role, source = role) => {
        const section = this.sections[source];
        const body = { ...pick(section, personKeys), personCertificate: [] };
        if (section.certificateType === 0 && pair(section)) {
          body.personCertificate = ['front', 'back'].map((side, index) => material(section.images[side], personFiles[role][index]));
        } else if (role === 'legal' && section.certificateType !== 0) {
          body.personCertificate = (section.documents ?? []).map(file => material(file, legalFiles[section.certificateType]));
        }
        return body;
      };
      return {
        purpose: this.purpose, materialName: this.materialName, sameOperator: this.sameOperator === true,
        businessInfo: { ...pick(business, businessKeys),
          ...(business.image ? { businessCertificate: material(business.image, business.businessCertificateType) } : {}) },
        operatorPerson: person('operator'), responsiblePersonInfo: person('responsible', this.sameOperator ? 'operator' : 'responsible'),
        ...(this.checks.business.manualReview ? {} : { businessCheckTicket: this.checks.business.ticket }),
        operatorCheckTicket: this.checks.operator.ticket,
        responsibleCheckTicket: this.checks[this.sameOperator ? 'operator' : 'responsible'].ticket,
        ...(this.sections.legal ? { legalPerson: person('legal'),
          ...(this.checks.legal?.ticket ? { legalCheckTicket: this.checks.legal.ticket } : {}) } : {}),
        powerOfAttorney: this.purpose === 2 && this.rank.needOtherUseCheck ? [material(this.sections.power, 5)] : [],
        otherMaterials: (this.sections.otherMaterials ?? []).map(file => material(file, 6)), effectSignatures: [],
        ...(this.purpose === 2 ? { authorizer: business.businessCertificateName, authorizee: this.account.businessName } : {}),
      };
    });
  }

  async upload(file, category) {
    if (!file || !/\.(jpe?g|png)$/i.test(file.name ?? '') || file.size > MAX_UPLOAD_BYTES) {
      fail('请选择 JPG、JPEG、PNG 图片，单张不大于 10 MB。');
    }
    const result = await this.client.upload(file, { kind: 'material', category });
    if (!result?.fileContent || !result.fileSuffix) fail('文件上传结果不完整，请重新选择文件。');
    return result;
  }

  async dispatch(path, options) {
    const url = new URL(path, 'https://qualification.local');
    const query = url.searchParams;
    const data = typeof options.body === 'string' ? JSON.parse(options.body) : {};
    const ok = { success: true };
    if (url.pathname === '/api/state') {
      if (!this.rank) {
        const rank = await this.client.call('get_qualification_requirements');
        if (!rank || rankFields.some(key => typeof rank[key] !== 'boolean')) fail('材料要求返回不完整，暂不能提交。');
        const account = await this.client.call('get_account_information');
        if (typeof account?.businessName !== 'string' || typeof account.userType !== 'string') fail('账号主体信息不完整，暂不能提交。');
        this.rank = rank;
        this.account = account;
      }
      return { ...ok, state: this.state() };
    }
    if (this.done) fail('本次填写已结束，请查询已有申请的状态。');
    switch (url.pathname) {
      case '/api/base': {
        if (![1, 2].includes(data.purpose)) fail('请选择资质归属。');
        const name = text(data.materialName, '资质名称', 20, true);
        this.materialNameSource = name && data.materialNameSource === 'manual' ? 'manual' : 'auto';
        this.materialName = this.materialNameSource === 'auto' && this.sections.business?.businessCertificateName
          ? materialName('', 'auto', this.sections.business.businessCertificateName) : name;
        if (this.purpose !== data.purpose) this.authorizationAcknowledged = false;
        this.purpose = data.purpose;
        this.baseSaved = true;
        if (this.purpose === 1) {
          delete this.sections.power; delete this.sections.otherMaterials;
          delete this.pending.power; delete this.pending.otherMaterials;
        }
        break;
      }
      case '/api/business-ocr': {
        const type = Number(new Headers(options.headers).get('X-Document-Type'));
        if (![1, 4, 6, 7].includes(type)) fail('请选择营业证件类型。');
        const image = await this.upload(options.body, 'business');
        const document = await this.client.call('recognize_qualification_document',
          { business_certificate_type: type, certificate: image.fileContent });
        this.pending.business = image;
        return { ...ok, document };
      }
      case '/api/business': {
        if (![1, 4, 6, 7].includes(data.businessCertificateType)) fail('请选择营业证件类型。');
        const business = { businessCertificateType: data.businessCertificateType,
          businessCertificateName: text(data.businessCertificateName, '营业证件名称'),
          unifiedSocialCreditIdentifier: text(data.unifiedSocialCreditIdentifier, '统一社会信用代码', 64),
          legalPersonName: text(data.legalPersonName, '法人姓名'),
          businessCertificateValidityPeriodStart: date(data.businessCertificateValidityPeriodStart),
          businessCertificateValidityPeriodEnd: date(data.businessCertificateValidityPeriodEnd),
          image: this.pending.business ?? this.sections.business?.image };
        if (business.businessCertificateValidityPeriodEnd < business.businessCertificateValidityPeriodStart) fail('有效期结束日期不能早于开始日期。');
        if (this.rank.needBusinessCertificateImage && !business.image) fail('请先上传营业证件并识别。');
        this.materialName = materialName(data.materialName, data.materialNameSource, business.businessCertificateName);
        this.materialNameSource = data.materialNameSource === 'manual' && data.materialName ? 'manual' : 'auto';
        const invalidatedLegal = Boolean(this.sections.legal && this.sections.legal.personName !== business.legalPersonName);
        if (invalidatedLegal) {
          delete this.sections.legal; delete this.pending.legal; delete this.checks.legal;
        }
        this.sections.business = business;
        delete this.pending.business;
        delete this.checks.business;
        this.legalAcknowledged = false;
        this.baseSaved = true;
        this.authorizationAcknowledged = false;
        this.revision++;
        return { ...ok, invalidatedLegal };
      }
      case '/api/person-image': {
        const role = query.get('role'), side = query.get('side');
        if (!(role in personFiles) || !['front', 'back'].includes(side)) fail('不支持当前证件材料。');
        const image = await this.upload(options.body, 'identity');
        this.pending[role] ??= {};
        this.pending[role].images ??= {};
        this.pending[role].images[side] = image;
        return ok;
      }
      case '/api/person-ocr': {
        const images = this.pending[query.get('role')]?.images;
        if (!images?.front || !images?.back) fail('请同时上传身份证人像面和国徽面。');
        const person = await this.client.call('recognize_qualification_document',
          { id_card_front_image: images.front.fileContent, id_card_back_image: images.back.fileContent });
        this.pending[query.get('role')].recognizedName = person?.personName;
        return { ...ok, person };
      }
      case '/api/legal-document':
      case '/api/other-material': {
        const legal = url.pathname === '/api/legal-document';
        const index = Number(query.get('index'));
        if (!Number.isInteger(index) || index < 0 || index >= (legal ? 2 : 5)) fail('材料数量超过限制。');
        if (legal && !Object.hasOwn(legalFiles, Number(query.get('certificateType')))) fail('请选择法人证件类型。');
        if (!legal && this.purpose !== 2) fail('自用资质无需授权材料。');
        const image = await this.upload(options.body, legal ? 'identity' : 'business');
        const pending = legal ? this.pending.legal ??= {} : this.pending;
        const key = legal ? 'documents' : 'otherMaterials';
        if (query.get('replace') === '1') pending[key] = [];
        pending[key] ??= [];
        pending[key][index] = image;
        return ok;
      }
      case '/api/person': {
        const role = data.role;
        if (!(role in personFiles)) fail('不支持当前人员信息。');
        const type = data.certificateType ?? 0;
        if (!(role === 'legal' ? [0, 1, 2, 3, 4, 9] : [0]).includes(type)) fail('请选择正确的证件类型。');
        if (role === 'legal' && data.skipEmpty && !data.personIDCard && !data.personMobile) {
          delete this.sections.legal; delete this.pending.legal; delete this.checks.legal;
          this.legalAcknowledged = true;
          break;
        }
        const name = role === 'legal' ? this.sections.business?.legalPersonName : data.personName;
        if (role === 'legal' && data.personName !== name) fail('法人姓名必须与营业证件一致。');
        if (role === 'legal' && type === 0 && this.pending.legal?.recognizedName
          && this.pending.legal.recognizedName !== name) fail('身份证姓名与营业证件中的法人姓名不一致，请重新核对。');
        const section = { certificateType: type, personName: text(name, `${labels[role]}姓名`),
          personIDCard: type === 0 ? identity(data.personIDCard, role !== 'legal') : text(data.personIDCard, '证件号码', 64, true),
          personMobile: mobile(data.personMobile, this.requirement(role, 'mobile')) };
        const pending = this.pending[role], existing = this.sections[role];
        if (type === 0) {
          section.images = pair(pending) ? pending.images : data.identityImagesChanged ? undefined : existing?.images;
          if (this.requirement(role, 'image') && !pair(section)) fail(`请上传${labels[role]}身份证正反面。`);
        } else {
          section.documents = data.documentsChanged ? (pending?.documents ?? []).slice(0, data.documentCount)
            : existing?.certificateType === type ? existing.documents : [];
        }
        this.sections[role] = section;
        delete this.pending[role]; delete this.checks[role]; delete this.verifications[role];
        if (existing?.personMobile !== section.personMobile) delete this.sentAt[role];
        if (role === 'legal') this.legalAcknowledged = true;
        if (role === 'operator' && this.sameOperator) {
          delete this.sections.responsible; delete this.pending.responsible; delete this.checks.responsible;
        }
        break;
      }
      case '/api/responsible-mode': {
        if (typeof data.sameOperator !== 'boolean' || !this.sections.operator) fail('请先保存经办人信息。');
        if (data.sameOperator && this.rank.needResponsibleImage && !pair(this.sections.operator)) {
          fail('请先为经办人补充身份证正反面，再选择与经办人相同。');
        }
        if (data.sameOperator && this.rank.needResponsibleMobile && !this.sections.operator.personMobile) {
          fail('请先为经办人补充手机号，再选择与经办人相同。');
        }
        this.sameOperator = data.sameOperator;
        delete this.checks.responsible; delete this.verifications.responsible;
        if (data.sameOperator) { delete this.sections.responsible; delete this.pending.responsible; }
        break;
      }
      case '/api/check': {
        const role = data.target, section = this.sections[role];
        if (!section) fail('请先保存本页信息。');
        const result = await this.client.call(role === 'business' ? 'check_qualification_enterprise' : 'check_qualification_person',
          role === 'business' ? { business_certificate_name: section.businessCertificateName,
            unified_social_credit_identifier: section.unifiedSocialCreditIdentifier, legal_person_name: section.legalPersonName }
            : { person_name: section.personName, person_id_card: section.personIDCard,
              ...(this.rank[`${role}ThreeElement`] ? { person_mobile: section.personMobile } : {}) });
        const manualReview = role === 'business' && result?.manualReview === true;
        let ticket = '';
        const status = String(result?.status ?? '').replace(/^[\u0000-\u0003]$/, character => String(character.charCodeAt(0)));
        if (!manualReview && status === '0') ticket = checkedTicket(result);
        else if (!manualReview && !['1', '2', '3'].includes(status)) fail('校验服务没有返回可识别的校验状态，请稍后重试。');
        const diagnostic = result?.failure?.error;
        this.checks[role] = { matched: Boolean(ticket), ticket, status, manualReview,
          ...(manualReview ? { error: { message: diagnostic?.message ?? '自动校验未通过，将转人工审核；你仍可继续。',
            code: diagnostic?.code ?? result.code, requestId: result.requestId } } : {}) };
        delete this.verifications[role];
        break;
      }
      case '/api/mobile-code/send':
      case '/api/mobile-code/verify': {
        const role = data.role, section = this.sections[role];
        if (!['operator', 'responsible'].includes(role) || !this.checks[role]?.matched
          || !section?.personMobile || this.account.userType !== 'smb' || role === 'responsible' && this.sameOperator) {
          fail('请先完成当前人员信息校验。');
        }
        const send = url.pathname.endsWith('/send');
        if (send && Date.now() - (this.sentAt[role] ?? 0) < 60000) fail('请等待 60 秒后再获取验证码。');
        if (!send && (!/^\d{4}$/.test(data.code ?? '') || this.verifications[role]?.mobile !== section.personMobile)) {
          fail('请先获取当前手机号的验证码，并输入 4 位验证码。');
        }
        const settings = config.qualificationVerification;
        const result = await this.client.call(send ? 'send_verification_code' : 'verify_code',
          { app_id: settings.appId, scene: settings.scene, mobile: section.personMobile,
            ...(send ? { template_id: settings.templates[role], code_type: 0, channel_id: settings.channelId }
              : { code: data.code, function: 2 }) }, { write: true });
        if (send) {
          if (typeof result?.messageId !== 'string' || !result.messageId.trim()) fail('验证码发送接口未返回消息 ID。');
          this.sentAt[role] = Date.now();
          this.verifications[role] = { mobile: section.personMobile, verified: false };
        } else {
          if (result?.status !== 0) fail(result?.status === 2 ? '验证码已过期，请重新获取。' : '验证码不正确，请重新输入。');
          this.verifications[role].verified = true;
        }
        break;
      }
      case '/api/power-of-attorney':
        if (this.purpose !== 2 || !this.rank.needOtherUseCheck) fail('当前资质无需授权委托书。');
        this.sections.power = await this.upload(options.body, 'authorization');
        break;
      case '/api/authorization':
        if (this.purpose !== 2 || !this.account.businessName) fail('请先确认资质归属和账号主体。');
        if (data.otherMaterialsChanged) this.sections.otherMaterials = (this.pending.otherMaterials ?? []).slice(0, data.otherMaterialCount);
        delete this.pending.otherMaterials;
        this.authorizationAcknowledged = true;
        break;
      case '/api/preview':
        return { ...ok, preview: this.preview() };
      case '/api/submit': {
        if (data.confirmed !== true || data.revision !== this.revision) fail('材料已变化，请重新生成并确认预览。');
        const { request } = this.submission();
        this.done = true;
        let qualificationId;
        try {
          qualificationId = await this.client.call('submit_qualification', { request,
            ...(this.checks.business.manualReview ? { confirm_manual_review: true } : {}) }, { write: true });
          if (!Number.isInteger(qualificationId) || qualificationId <= 0) {
            throw new OperationError('提交结果暂时无法确认，请勿重复提交。', { unknown: true });
          }
        } catch (error) {
          if (!error.unknown) this.done = false;
          else await this.client.report({ form: 'qualification', state: 'outcome_unknown',
            ...(error.requestId ? { requestId: error.requestId } : {}) });
          throw error;
        }
        await this.client.report({ form: 'qualification', state: 'submitted', qualificationId });
        return { ...ok, qualificationId };
      }
      case '/api/abandon':
        this.done = true;
        this.sections = {}; this.pending = {}; this.checks = {}; this.verifications = {};
        await this.client.report({ form: 'qualification', state: 'abandoned' });
        return ok;
      default:
        fail('不支持当前表单操作。');
    }
    this.revision++;
    return ok;
  }
}
