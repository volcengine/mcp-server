import z from "zod";
import * as zCommon from '../../schema/common';
import type { IProxyToolModel } from "../../utils/tools";

/**
 * The service name.
 */
export const veenEdgeService = 'veenedge';

/**
 * All related MCP tools.
 */
export const computeTools: IProxyToolModel[] = [
  {
    name: 'get-cloud-server',
    description: '获取边缘服务（边缘计算节点）的详细信息。',
    args: {
      cloud_server_identity: z.string().describe('边缘服务的 ID'),
    },
    action: 'GetCloudServer',
    service: veenEdgeService,
    method: 'GET',
  },
  {
    name: 'list-account-cloud-servers',
    description: '获取当前用户所有的边缘服务（边缘计算节点）。',
    args: {
    },
    action: 'ListAccountCloudServers',
    service: veenEdgeService,
    method: 'POST',
  },
  {
    name: 'check-cloud-server-name',
    description: '检查边缘计算节点的名称是否已经存在。',
    args: {
      name: z.string().describe('名称，用于检查是否已经存在。'),
    },
    action: 'CheckCloudServerName',
    service: veenEdgeService,
    method: 'POST',
  },
];
