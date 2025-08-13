import { z } from "zod";

export const searchMode = z.enum(['like', 'exact']).describe('搜索模式（包括模糊搜索和精确匹配）');
export const ids = z.array(z.string());
