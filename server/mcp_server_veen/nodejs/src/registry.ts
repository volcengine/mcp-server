import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { registerServices as reg, addProxyTools } from './utils/tools';
import { computeTools, veenEdgeService } from './tools/veen/compute';
import { trafficRouteTools, trafficRouteService } from './tools/tr/all';

/**
 * Registers all tools.
 */
export function registerTools(server?: McpServer) {
  addProxyTools(computeTools, server);
  addProxyTools(trafficRouteTools, server);
  
}

/**
 * Registers all services.
 */
export function registerServices() {
  reg({
    [veenEdgeService]: {
      serviceName: veenEdgeService,
      defaultVersion: '2021-04-30',
    },
    [trafficRouteService]: {
      serviceName: 'dns',
      defaultVersion: '2018-08-01',
    },
    'domain': {
      serviceName: 'domain_openapi',
      defaultVersion: '2022-12-12',
    },
    'ssl': {
      region: 'cn-beijing',
      serviceName: 'certificate_service',
      defaultVersion: '2024-10-01',
    },
  });
}
