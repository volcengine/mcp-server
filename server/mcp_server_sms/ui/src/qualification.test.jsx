import React from 'react';
import { afterEach, expect, it, vi } from 'vitest';
import { cleanup, render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QualificationForm } from './qualification.jsx';
import { QualificationController, rankFields } from './qualification-controller.js';
import { OperationError } from './client.js';

afterEach(cleanup);
const rank = Object.fromEntries(rankFields.map(key => [key, false]));
const business = { businessCertificateType: 1, businessCertificateName: '测试企业',
  unifiedSocialCreditIdentifier: 'fixture-credit', legalPersonName: '测试法人',
  businessCertificateValidityPeriodStart: '2020-01-01', businessCertificateValidityPeriodEnd: '2099-12-31' };
const person = { certificateType: 0, personName: '测试人员', personIDCard: '11010119900101001X', personMobile: '' };
const image = name => ({ name, data: 'Zml4dHVyZQ==' });
function apiFixture({ requirements = rank, userType = 'enterprise', manual = false, submit } = {}) {
  return {
    call: vi.fn(async name => {
      if (name === 'get_qualification_requirements') return requirements;
      if (name === 'get_account_information') return { businessName: '账号企业', userType };
      if (name === 'check_qualification_enterprise') return manual
        ? { manualReview: true, code: 'enterprise_check_mismatch', requestId: 'fixture-check' }
        : { status: 0, ticket: 'business-ticket' };
      if (name === 'check_qualification_person') return { status: '0', ticket: 'person-ticket' };
      if (name === 'recognize_qualification_document') return { ...business, ...person };
      if (name === 'send_verification_code') return { messageId: 'verification-message' };
      if (name === 'verify_code') return { status: 0 };
      if (name === 'submit_qualification') return submit ? submit() : 123;
      throw new Error(`Unexpected tool ${name}`);
    }),
    upload: vi.fn(async file => ({ name: file.name, fileContent: `private/${file.name}`, fileSuffix: 'png' })),
    report: vi.fn().mockResolvedValue(undefined),
  };
}
const post = (controller, path, body) => controller.request(path, { body: JSON.stringify(body) });
async function readyController(options = {}) {
  const api = apiFixture(options);
  const controller = new QualificationController(api);
  await controller.request('/api/state');
  await post(controller, '/api/base', { purpose: options.purpose ?? 1, materialName: '', materialNameSource: 'auto' });
  await post(controller, '/api/business', { ...business, materialName: '', materialNameSource: 'auto' });
  await post(controller, '/api/check', { target: 'business' });
  await post(controller, '/api/person', { role: 'legal', skipEmpty: true });
  await post(controller, '/api/person', { ...person, ...options.person, role: 'operator' });
  await post(controller, '/api/check', { target: 'operator' });
  await post(controller, '/api/responsible-mode', { sameOperator: true });
  return { api, controller };
}
async function uiToReview(api) {
  const user = userEvent.setup();
  render(<QualificationForm client={api} prefill={{ businessInfo: business, operatorPerson: person }} />);
  await screen.findByRole('heading', { name: '基础信息' });
  await user.click(screen.getByRole('button', { name: '下一步' }));
  await user.click(await screen.findByRole('button', { name: '营业证件有效性校验' }));
  await screen.findByRole('button', { name: /校验已通过|重新校验/ });
  await user.click(screen.getByRole('button', { name: '下一步' }));
  await screen.findByRole('heading', { name: '法人信息' });
  await user.click(screen.getByRole('button', { name: '确认并继续' }));
  await user.click(await screen.findByRole('button', { name: '经办人信息校验' }));
  await screen.findByRole('button', { name: '校验已通过' });
  await user.click(screen.getByRole('button', { name: '确认并继续' }));
  await user.click(await screen.findByRole('button', { name: '是同一个人' }));
  await screen.findByRole('heading', { name: '核对并提交' });
  await screen.findByText('我已核对以上内容，同意提交审核');
  return user;
}

it('保留参考表单的六个自用步骤、日期范围组件与前进校验', async () => {
  const api = apiFixture();
  const user = userEvent.setup();
  render(<QualificationForm client={api} />);
  await screen.findByRole('heading', { name: '基础信息' });
  expect(document.querySelectorAll('.wizard-sidebar .arco-steps-item')).toHaveLength(6);
  await user.click(screen.getByRole('button', { name: '下一步' }));
  await screen.findByRole('heading', { name: '企业信息' });
  expect(document.querySelector('.arco-picker-range')).toBeTruthy();
  expect(screen.getByRole('button', { name: '营业证件有效性校验' }).disabled).toBe(true);
  await user.click(screen.getByRole('button', { name: '下一步' }));
  expect(screen.getByRole('heading', { name: '企业信息' })).toBeTruthy();
  expect(api.call.mock.calls.map(([name]) => name)).toEqual(['get_qualification_requirements', 'get_account_information']);
});

it('校验后仍需勾选确认，重复点击只提交一次，Agent 仅收到申请编号', async () => {
  let resolve;
  const api = apiFixture({ submit: () => new Promise(done => { resolve = done; }) });
  const user = await uiToReview(api);
  const submit = screen.getByRole('button', { name: '提交资质' });
  await user.click(submit);
  expect(api.call.mock.calls.filter(([name]) => name === 'submit_qualification')).toHaveLength(0);
  await user.click(screen.getByText('我已核对以上内容，同意提交审核'));
  await user.dblClick(submit);
  await waitFor(() => expect(api.call.mock.calls.filter(([name]) => name === 'submit_qualification')).toHaveLength(1));
  resolve(123);
  await screen.findByText('资质申请已提交');
  const request = api.call.mock.calls.find(([name]) => name === 'submit_qualification')[1].request;
  expect(request).toMatchObject({ materialName: '测试企业', sameOperator: true,
    operatorPerson: person, responsiblePersonInfo: person, responsibleCheckTicket: 'person-ticket' });
  expect(request.legalPerson).toBeUndefined();
  expect(api.report).toHaveBeenCalledWith({ form: 'qualification', state: 'submitted', qualificationId: 123 });
});

it('企业核验失败展示排障编号，并通过参考确认弹窗转人工审核', async () => {
  const api = apiFixture({ manual: true });
  const user = await uiToReview(api);
  await user.click(screen.getByText('我已核对以上内容，同意提交审核'));
  await user.click(screen.getByRole('button', { name: '提交资质' }));
  expect(api.call.mock.calls.filter(([name]) => name === 'submit_qualification')).toHaveLength(0);
  const dialog = await screen.findByRole('dialog');
  expect(within(dialog).getByText('企业信息核查失败，是否强制提交审核？')).toBeTruthy();
  await user.click(within(dialog).getByRole('button', { name: '确认提交' }));
  await screen.findByText('资质申请已提交');
  const args = api.call.mock.calls.find(([name]) => name === 'submit_qualification')[1];
  expect(args.confirm_manual_review).toBe(true);
  expect(args.request.businessCheckTicket).toBeUndefined();
});

it('他用显示第七步，预填材料保留私密草稿且不自动上传或校验', async () => {
  const api = apiFixture();
  const controller = new QualificationController(api, { purpose: 2, materialName: '预填资质',
    businessInfo: { ...business, businessCertificate: image('营业.png') },
    operatorPerson: { ...person, personCertificate: { front: image('人像.png'), back: image('国徽.png') } },
    legalPerson: { certificateType: 1, personName: '不会覆盖企业法人', personIDCard: 'passport',
      personCertificate: { document: image('护照.png') } },
    powerOfAttorney: [image('委托.png')], otherMaterials: [image('其他.png')] });
  const state = (await controller.request('/api/state')).state;
  expect(state.savedData.people.legal.personName).toBe('测试法人');
  expect(state.readyForPreview).toBe(false);
  expect(controller.initialFiles.legalOther[0].originFile.name).toBe('护照.png');
  expect(api.upload).not.toHaveBeenCalled();
  expect(api.call).toHaveBeenCalledTimes(2);
  render(<QualificationForm client={api} prefill={{ purpose: 2, materialName: '预填资质' }} />);
  expect((await screen.findByLabelText('资质名称（选填）')).value).toBe('预填资质');
  expect(document.querySelectorAll('.wizard-sidebar .arco-steps-item')).toHaveLength(7);
});

it('复用经办人生成责任人专用材料类型，并复用票据', async () => {
  const { controller } = await readyController();
  await controller.request('/api/person-image?role=operator&side=front', { body: image('front.png') });
  await controller.request('/api/person-image?role=operator&side=back', { body: image('back.png') });
  await post(controller, '/api/person', { ...person, role: 'operator', identityImagesChanged: true });
  expect(() => controller.submission()).toThrow('校验');
  await post(controller, '/api/check', { target: 'operator' });
  const { request } = controller.submission();
  expect(request.operatorPerson.personCertificate.map(file => file.fileType)).toEqual([8, 9]);
  expect(request.responsiblePersonInfo.personCertificate.map(file => file.fileType)).toEqual([10, 11]);
  expect(request.responsibleCheckTicket).toBe(request.operatorCheckTicket);
});

it('移除身份证图片后清除已上传的待保存材料，防止旧图片重新进入申请', async () => {
  const { controller } = await readyController();
  for (const side of ['front', 'back']) {
    await controller.request(`/api/person-image?role=operator&side=${side}`, { body: image(`${side}.png`) });
  }
  controller.clearPending('operatorFront');
  controller.clearPending('operatorBack');
  await post(controller, '/api/person', { ...person, role: 'operator', identityImagesChanged: true });
  await post(controller, '/api/check', { target: 'operator' });
  expect(controller.submission().request.operatorPerson.personCertificate).toEqual([]);
});

it.each([1, 4, 7, 6])('营业证件枚举 %i 原样用于证件信息和材料类型', async type => {
  const { controller } = await readyController();
  await controller.request('/api/business-ocr', { headers: { 'X-Document-Type': String(type) }, body: image('business.png') });
  await post(controller, '/api/business', { ...business, businessCertificateType: type, materialName: '', materialNameSource: 'auto' });
  await post(controller, '/api/check', { target: 'business' });
  await post(controller, '/api/person', { role: 'legal', skipEmpty: true });
  expect(controller.submission().request.businessInfo).toMatchObject({
    businessCertificateType: type, businessCertificate: { fileType: type },
  });
});

it.each([[1, 12], [2, 13], [3, 14], [4, 15], [9, 6]])('法人证件枚举 %i 映射 %i，允许两张附件，切换身份证清除旧材料', async (type, fileType) => {
  const { controller } = await readyController();
  for (const index of [0, 1]) {
    await controller.request(`/api/legal-document?index=${index}&certificateType=${type}${index === 0 ? '&replace=1' : ''}`,
      { body: image(`legal${index}.png`) });
  }
  await post(controller, '/api/person', { role: 'legal', certificateType: type, personName: '测试法人',
    personIDCard: 'passport', documentsChanged: true, documentCount: 2 });
  expect(controller.submission().request.legalPerson.personCertificate.map(file => file.fileType)).toEqual([fileType, fileType]);
  await post(controller, '/api/person', { role: 'legal', certificateType: 0, personName: '测试法人',
    personIDCard: '', identityImagesChanged: true, documentsChanged: true, documentCount: 0 });
  expect(controller.submission().request.legalPerson.personCertificate).toEqual([]);
});

it('法人姓名来自企业，身份证号选填但一旦填写必须核验，企业修改重新确认法人', async () => {
  const { controller } = await readyController();
  await expect(post(controller, '/api/person', { role: 'legal', personName: '另一人' })).rejects.toThrow('法人姓名必须');
  await post(controller, '/api/person', { role: 'legal', personName: '测试法人', personIDCard: person.personIDCard });
  expect(controller.state().readyForPreview).toBe(false);
  await post(controller, '/api/check', { target: 'legal' });
  expect(controller.state().readyForPreview).toBe(true);
  const result = await post(controller, '/api/business', { ...business, legalPersonName: '新法人', materialName: '', materialNameSource: 'auto' });
  expect(result.invalidatedLegal).toBe(true);
  expect(controller.state().legalAcknowledged).toBe(false);
  expect(controller.state().checks.business.attempted).toBe(false);
});

it('他用授权方和被授权方取对应主体，材料类型为 5/6，自用清除授权材料', async () => {
  const { controller } = await readyController({ purpose: 2, requirements: { ...rank, needOtherUseCheck: true } });
  expect(controller.state().readyForPreview).toBe(false);
  await controller.request('/api/power-of-attorney', { body: image('power.png') });
  await controller.request('/api/other-material?index=0&replace=1', { body: image('other.png') });
  await post(controller, '/api/authorization', { otherMaterialsChanged: true, otherMaterialCount: 1 });
  const { request } = controller.submission();
  expect(request).toMatchObject({ authorizer: '测试企业', authorizee: '账号企业',
    powerOfAttorney: [{ fileType: 5 }], otherMaterials: [{ fileType: 6 }] });
  await expect(controller.request('/api/other-material?index=5', { body: image('sixth.png') })).rejects.toThrow('数量');
  await post(controller, '/api/base', { purpose: 1, materialName: '', materialNameSource: 'auto' });
  expect(controller.submission().request).toMatchObject({ powerOfAttorney: [], otherMaterials: [] });
});

it('账号材料与手机号规则生效，复用责任人前检查经办人是否满足责任人材料要求', async () => {
  const { controller } = await readyController({ requirements: { ...rank } });
  controller.rank.needResponsibleImage = true;
  await expect(post(controller, '/api/responsible-mode', { sameOperator: true })).rejects.toThrow('补充身份证正反面');
  controller.rank.needResponsibleImage = false;
  controller.rank.needResponsibleMobile = true;
  await expect(post(controller, '/api/responsible-mode', { sameOperator: true })).rejects.toThrow('补充手机号');
  await expect(post(controller, '/api/person', { ...person, role: 'responsible' })).rejects.toThrow('手机号');
});

it('SMB 四位验证码使用参考配置，手机号变化使核验及验证码失效', async () => {
  const { api, controller } = await readyController({ userType: 'smb', person: { personMobile: '13800000000' },
    requirements: { ...rank, operatorThreeElement: true } });
  expect(controller.state().readyForPreview).toBe(false);
  await post(controller, '/api/mobile-code/send', { role: 'operator' });
  expect(api.call).toHaveBeenCalledWith('send_verification_code', {
    app_id: 482875, scene: 3, mobile: '13800000000', template_id: 59030, code_type: 0, channel_id: 2430,
  }, { write: true });
  await expect(post(controller, '/api/mobile-code/verify', { role: 'operator', code: '123456' })).rejects.toThrow('4 位');
  await post(controller, '/api/mobile-code/verify', { role: 'operator', code: '1234' });
  expect(controller.state().readyForPreview).toBe(true);
  await post(controller, '/api/person', { ...person, role: 'operator', personMobile: '13900000000' });
  expect(controller.state().checks.operator.attempted).toBe(false);
  expect(controller.state().mobileVerifications.operator).toBe(false);
});

it('预览版本过期阻止提交，未知结果锁住请求并保留诊断编号', async () => {
  const { api, controller } = await readyController({ submit: () => {
    throw new OperationError('结果待确认', { unknown: true, requestId: 'fixture-unknown' });
  } });
  const revision = controller.preview().revision;
  await post(controller, '/api/base', { purpose: 1, materialName: '新名称', materialNameSource: 'manual' });
  await expect(post(controller, '/api/submit', { confirmed: true, revision })).rejects.toThrow('材料已变化');
  expect(api.call.mock.calls.filter(([name]) => name === 'submit_qualification')).toHaveLength(0);
  const body = { confirmed: true, revision: controller.preview().revision };
  await expect(post(controller, '/api/submit', body)).rejects.toMatchObject({ unknown: true, outcomeUnknown: true,
    message: expect.stringContaining('fixture-unknown') });
  await expect(post(controller, '/api/submit', body)).rejects.toThrow('已结束');
  expect(api.call.mock.calls.filter(([name]) => name === 'submit_qualification')).toHaveLength(1);
});
