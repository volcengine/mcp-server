import { z } from 'zod';

export const failureSchema = z.object({
  success: z.literal(false),
  error: z.object({ code: z.union([z.string(), z.number()]).nullish(), message: z.string().nullish() }).passthrough(),
}).passthrough();

// 仅校验表单实际消费的字段，未知业务字段和原始值保留在原响应中。
export const messageGroupSchema = z.object({
  subAccountId: z.string().min(1), subAccountName: z.string().optional(),
}).passthrough();
export const signatureQualificationSchema = z.object({
  id: z.number().int().positive(), purpose: z.union([z.literal(1), z.literal(2)]),
  materialName: z.string(), businessCertificateName: z.string(),
}).passthrough();
export const signatureSchema = z.object({ Signature: z.string().min(1) }).passthrough();
export const batchTemplateSchema = z.object({
  TemplateId: z.string().min(1), TemplateName: z.string().optional(), ChannelType: z.string(),
  TemplateContent: z.string().optional(), Content: z.string().optional(), BatchOnly: z.boolean().optional(),
  TaskFields: z.array(z.object({
    Name: z.string(), Required: z.boolean().optional(), Label: z.string().optional(),
    MaxLength: z.number().int().positive().optional(),
  }).passthrough()).optional(),
}).passthrough();


const confirmationSignature = z.string().regex(/^[0-9a-f]{64}$/);
export const templatePreviewSchema = z.object({
  request: z.object({
    name: z.string().min(1), content: z.string().min(1),
    channelType: z.enum(['CN_OTP', 'CN_NTC', 'CN_MKT']), area: z.literal('cn'),
    signatures: z.array(z.string().min(1)).min(1),
    templateParams: z.array(z.object({ name: z.string(), paramType: z.number().int().min(1).max(5) })),
  }).passthrough(),
  account: z.object({ userType: z.string(), businessName: z.string().nullish() }).passthrough(),
  fixedTraffic: z.array(z.object({ paramType: z.union([z.literal(2), z.literal(3)]),
    isExist: z.literal(true), content: z.string().optional() }).passthrough()),
  warnings: z.array(z.string()), confirmation: z.object({
    expires_at: z.number().int().positive(), signature: confirmationSignature,
  }),
});
const fileMetadata = {
  name: z.string().min(1).max(255), size: z.number().int().positive(),
};
const uploadRequest = {
  url: z.string().url(), headers: z.record(z.string(), z.string()),
};
export const materialUploadPlanSchema = z.object({
  upload: z.object({ ...uploadRequest, method: z.literal('PUT') }),
  confirmation: z.object({
    context: z.object({
      name: fileMetadata.name, suffix: z.string().min(1), uri: z.string().min(1),
      session_key: z.string().min(1), expires_at: z.number().int().positive(),
    }),
    signature: confirmationSignature,
  }),
});
export const recipientsUploadPlanSchema = z.object({
  upload: z.object({ ...uploadRequest, method: z.literal('PUT') }),
  confirmation: z.object({
    context: z.object({
      ...fileMetadata, sha256: z.string().regex(/^[0-9a-f]{64}$/),
      sub_account: z.string().min(1), template_id: z.string().min(1),
      file: z.string().min(1), expires_at: z.number().int().positive(),
    }),
    signature: confirmationSignature,
  }),
});
