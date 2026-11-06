import { z } from 'zod';

export const failureSchema = z.object({
  success: z.literal(false),
  error: z.object({ code: z.string(), message: z.string(), outcome_unknown: z.boolean() }).passthrough(),
}).passthrough();

// 仅校验表单实际消费的字段，未知业务字段和原始值保留在原响应中。
export const messageGroupSchema = z.object({
  subAccountId: z.string().min(1), subAccountName: z.string().optional(),
}).passthrough();
export const qualificationSchema = z.object({
  id: z.number().int().positive(), purpose: z.union([z.literal(1), z.literal(2)]),
  auditStatus: z.number().int(), usable: z.boolean(), materialName: z.string().optional(),
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
