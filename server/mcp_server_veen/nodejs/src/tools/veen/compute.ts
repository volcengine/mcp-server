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
    name: 'get_cloud_server',
    description: '获取边缘服务（边缘计算节点）的详细信息。',
    args: {
      cloud_server_identity: z.string().describe('边缘服务的 ID'),
    },
    action: 'GetCloudServer',
    service: veenEdgeService,
    method: 'GET',
  },
  {
    name: 'list_cloud_servers',
    description: '获取当前用户所有的边缘服务（边缘计算节点）。',
    args: {
    },
    action: 'ListAccountCloudServers',
    service: veenEdgeService,
    method: 'POST',
  },
  {
    name: 'check_cloud_server_name',
    description: '检查边缘计算节点的名称是否已经存在。',
    args: {
      name: z.string().describe('名称，用于检查是否已经存在。'),
    },
    action: 'CheckCloudServerName',
    service: veenEdgeService,
    method: 'POST',
  },
  {
    name: 'start_instances',
    description: '根据边缘实例 ID 启动实例。',
    args: {
      instance_identities: zCommon.ids.describe('边缘实例 ID 列表。可以通过 list_instances 工具查询边缘实例 ID。'),
    },
    action: 'StartInstances',
    service: veenEdgeService,
    method: 'POST',
  },
  {
    name: 'list_instances',
    description: '列出指定的边缘服务或所有边缘服务下的边缘实例。',
    args: {
      countries: z.string().describe('国家或地区代码列表，用于过滤边缘实例。'),
      status: z.enum(['opening', 'starting', 'running', 'stopping', 'stop', 'rebooting', 'terminating', 'open_fail']).describe('边缘实例状态，用于过滤边缘实例。'),
      cloud_server_identities: z.string().describe('边缘服务 ID 列表，用于过滤边缘实例。ID 之间用半角逗号（,）分隔。'),
      spec_names: z.string().describe('边缘实例规格名称列表，用于过滤边缘实例。规格名称之间用半角逗号（,）分隔。'),
      instance_identities: z.string().describe('边缘实例 ID 列表，用于过滤边缘实例。ID 之间用半角逗号（,）分隔。'),
    },
    action: 'ListInstances',
    service: veenEdgeService,
    method: 'POST',
  },
  {
    name: 'get_instance',
    description: '根据边缘实例 ID 获取实例详细信息。',
    args: {
      instance_identity: z.string().describe('边缘实例的 ID。可以通过 list_instances 工具查询边缘实例 ID。'),
    },
    action: 'GetInstance',
    service: veenEdgeService,
    method: 'POST',
  },
  {
    name: 'set_instance_name',
    description: '边缘实例的名称。',
    args: {
      instance_identity: z.string().describe('边缘实例的 ID。可以通过 list_instances 工具查询边缘实例 ID。'),
      instance_name: z.string().describe('边缘实例的新名称。允许5~80个字符，支持中文、大写字母、小写字母、数字、下划线（_）、中划线（-）和空格等，不支持引号、空格、斜线、反斜线。'),
    },
    action: 'SetInstanceName',
    service: veenEdgeService,
    method: 'POST',
  },
  {
    name: 'list_instance_internal_ips',
    description: '获取指定边缘实例的私网 IP 地址的列表。',
    args: {
      instance_identity: z.string().describe('边缘实例的 ID。可以通过 list_instances 工具查询边缘实例 ID。'),
    },
    action: 'ListInstanceInternalIps',
    service: veenEdgeService,
    method: 'POST',
  },
  {
    name: 'list_instance_types',
    description: '获取边缘服务下可开通的实例规格。',
    args: {
    },
    action: 'ListInstanceTypes',
    service: veenEdgeService,
    method: 'POST',
  },
  {
    name: 'list_images',
    description: '获取某一实例规格支持的镜像列表，包括公共镜像和自定义镜像。',
    args: {
      instance_type: z.string().describe('实例规格。可以通过 list_instance_types 工具查询可开通的实例规格。'),
    },
    action: 'ListImages',
    service: veenEdgeService,
    method: 'POST',
  },
  {
    name: 'get_image',
    description: '获取镜像详情。',
    args: {
      image_id: z.string().describe('镜像 ID。可以通过 list_images 工具查询镜像 ID。'),
    },
    action: 'GetImage',
    service: veenEdgeService,
    method: 'POST',
  },
];
