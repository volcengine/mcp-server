import z from "zod";
import * as zCommon from '../../schema/common';
import type { IProxyToolModel } from "../../utils/tools";

/**
 * The service name.
 */
export const trafficRouteService = 'traffic-route';

/**
 * All related MCP tools.
 */
export const trafficRouteTools: IProxyToolModel[] = [
  {
    name: 'list-zones',
    description: '获取在 TrafficRoute 上的解析域名列表。',
    args: {
      Key: z.string().describe('搜索关键词'),
      SearchMode: zCommon.searchMode,
    },
    action: 'ListZones',
    service: trafficRouteService,
    method: 'POST',
  },
  {
    name: 'create-zone',
    description: '添加域名。添加完毕后，后续可以通过 create-record 工具来添加解析。',
    args: {
      ZoneName: z.string().describe('域名'),
    },
    action: 'CreateZone',
    service: trafficRouteService,
    method: 'POST',
  },
  {
    name: 'create-record',
    description: '给指定域名增加解析记录。',
    args: {
      ZID: z.number().describe('关联的域名 ID'),
      Host: z.string().describe('主机名'),
      Type: z.string().describe('解析记录类型'),
      Value: z.string().describe('解析记录值'),
      TTL: z.number().default(600).optional().describe('生存时间，单位为秒'),
      Weight: z.number().default(1).optional().describe('权重'),
    },
    action: 'CreateRecord',
    service: trafficRouteService,
    method: 'POST',
  },
  {
    name: 'update-record',
    description: '修改指定域名的解析记录。',
    args: {
      RecordID: z.string().describe('解析记录 ID'),
      Host: z.string().describe('域名'),
      Line: z.string(),
      Type: z.string().describe('解析记录类型'),
      Value: z.string().describe('解析记录值'),
      TTL: z.number().default(600).optional(),
      Weight: z.number().default(1).optional().describe('权重'),
    },
    action: 'UpdateRecord',
    service: trafficRouteService,
    method: 'POST',
  },
  {
    name: 'list-records',
    description: '获取域名的全部解析记录列表。',
    args: {
      ZID: z.number().describe('关联的域名 ID')
    },
    action: 'ListRecords',
    service: trafficRouteService,
    method: 'POST',
  },
];
