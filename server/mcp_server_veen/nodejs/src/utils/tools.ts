import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import type { AxiosRequestConfig } from "axios";
import type { ServiceOptions, FetchParams, OpenApiResponse } from "../sdk/base/types";
import type { CallToolResult, ServerRequest, ServerNotification } from "@modelcontextprotocol/sdk/types.js";
import type { RequestHandlerExtra } from "@modelcontextprotocol/sdk/shared/protocol.js";
import { server as globalServer } from "../server";
import { ZodTypeAny } from 'zod';
import { getString } from './lang';
import Service from "../sdk/base/service";

/**
 * The message container object.
 */
interface IMessageObject {
  /**
   * The message.
   */
  message: string;
}

/**
 * The description about resolving the data.
 */
interface IResponseValueObject extends IMessageObject {
  /**
   * The field of response to return.
   */
  field?: string;
}

/**
 * The message container on no response.
 */
interface INoResponseMessageObject extends IMessageObject {
  /**
   * The message on no response.
   */
  noRespMessage?: string;
}

/**
 * The tool model of Open API proxy.
 */
export interface IProxyToolModel<T = any> {
  /**
   * The name of the tool. Should contains lowercase alphabet, dash and number digits only.
   */
  name: string;
  /**
   * The prompt description of this tool.
   */
  description: string;
  /**
   * The prompt description of each arguments.
   */
  args: Record<string, ZodTypeAny>;
  /**
   * The action of the web API.
   */
  action: string;
  /**
   * The service key.
   */
  service: string | Service;
  /**
   * The HTTP method to resolve data.
   */
  method: 'POST' | 'GET' | 'PUSH' | 'DELETE' | 'PATCH' | 'OPTIONS' | boolean;
  /**
   * Additional API version.
   */
  version?: string;
  /**
   * Creates a context.
   * @param args The arguments.
   * @param extra The extra information of the request.
   */
  createContext?(args: Record<string, any>, extra: RequestHandlerExtra<ServerRequest, ServerNotification>): any;
  /**
   * Occurs on fetching.
   * @param params 
   * @param context The context of this operation.
   */
  onFetch?(params: FetchParams & AxiosRequestConfig, context: any): void;
  /**
   * Standandizes the response.
   * @param resp The raw response data.
   * @param context The context of this operation.
   * @returns The response data following Open API spec.
   */
  standardizeResult?(resp: unknown, context: any): OpenApiResponse<T>;
  /**
   * Occurs on getting response succeeded.
   * @param result The tool result model.
   * @param resp The response from Open API.
   * @param context The context of this operation.
   */
  onSuccess?: ((result: CallToolResult, resp: OpenApiResponse<T>, context: any) => void) | IResponseValueObject;
  /**
   * Occurs on getting response failed by business error.
   * @param result The tool result model.
   * @param resp The response from Open API.
   * @param context The context of this operation.
   */
  onError?: ((result: CallToolResult, resp: OpenApiResponse<T> | undefined, context: any) => void) | INoResponseMessageObject;
  /**
   * Occurs on getting response failed by fetch or other connection issue.
   * @param result The tool result model.
   * @param error The error catched.
   * @param context The context of this operation.
   */
  onFetchError?: ((result: CallToolResult, error: unknown, context: any) => void) | IMessageObject;
}

/**
 * The internal store.
 */
const store = {
  services: {} as Record<string, Service>
}

/**
 * Generates the tool result by text.
 * @param value The input text to convert.
 */
export function generateTextResult(value: string | string[]): CallToolResult {
  if (value instanceof Array) {
    const arr: {
      type: 'text',
      text: string
    }[] = value.filter(line => {
      return line;
    }).map(line => {
      return {
        type: 'text',
        text: line
      };
    });
    return {
      content: arr
    };
  }

  return {
    content: [
      {
        type: 'text',
        text: value
      }
    ]
  };
}

/**
 * Registers a specific service.
 * @param key The service key.
 * @param service The service instance.
 */
export function registerService(key: string | undefined, service: Service | ServiceOptions | undefined) {
  if (!service) {
    if (key) {
      delete store.services[key];
    }
    
    return undefined;
  } else if (service instanceof Service) {
    if (!key) {
      return undefined;
    }

    store.services[key] = service;
    return service;
  } else {
    if (!key) {
      key = service.serviceName;
    }
    
    if (!key) {
      return;
    }
    
    const obj = new Service(service);
    if (process.env.VOLC_ACCESS_KEY_ID && process.env.VOLC_ACCESS_KEY_SECRET) {
      obj.setAccessKeyId(process.env.VOLC_ACCESS_KEY_ID);
      obj.setSecretKey(process.env.VOLC_ACCESS_KEY_SECRET);
    }

    store.services[key] = obj;
    return obj;
  }
}

/**
 * Update credential of each service.
 */
export function batchUpdateAccessKey() {
  if (!process.env.VOLC_ACCESS_KEY_ID || !process.env.VOLC_ACCESS_KEY_SECRET) return;
  for (const key in store.services) {
    if (typeof key !== 'string') continue;
    const service = store.services[key];
    if (service instanceof Service) {
      service.setAccessKeyId(process.env.VOLC_ACCESS_KEY_ID);
      service.setSecretKey(process.env.VOLC_ACCESS_KEY_SECRET);
    }
  }
}

/**
 * Registers a set of services.
 * @param services All services.
 */
export function registerServices(services: Record<string, Service | ServiceOptions | undefined> | ServiceOptions[]) {
  if (!services) return;
  if (services instanceof Array) {
    for (const i in services) {
      if (typeof i !== 'number' && typeof i !== 'string') continue;
      const service = services[i];
      if (!service || !service.serviceName) continue;
      registerService(undefined, service);
    }

    return;
  }

  const keys = Object.keys(services);
  for (const i in keys) {
    if (typeof i !== 'number' && typeof i !== 'string') continue;
    const key = keys[i];
    if (!key) continue;
    registerService(key, services[key]);
  }
}

/**
 * Gets a specific service.
 * @param key The service key.
 * @returns The service instance.
 */
export function getService(key: string | Service) {
  if (!key) return undefined;
  return key instanceof Service ? key : store.services[key];
}

/**
 * Adds a tool with functionality from a specific Open API of VolcEngine.
 * @param param0 The proxy tool model.
 * @param server The optional MCP server.
 * @returns The tool registered.
 */
export function addProxyTool<T = any>({
    name,
    description,
    args,
    action,
    service,
    method,
    version,
    createContext,
    onFetch,
    standardizeResult,
    onSuccess,
    onError,
    onFetchError,
  }: IProxyToolModel, server?: McpServer) {
  if (!name || !description) {
    return undefined;
  }

  return (server ?? globalServer).tool(name, description, args, async (args, extra) => {
    const context = typeof createContext === 'function' ? createContext(args, extra) : undefined;
    const serviceInstance = getService(service);
    if (!method) {
      method = 'GET';
    } else if (method === true) {
      method = 'POST';
    }

    const params: FetchParams & AxiosRequestConfig = {
      Action: action,
      method,
      headers: {
        'content-type': 'application/json',
      }
    };
    switch (method.toUpperCase()) {
      case 'GET':
      case 'DELETE':
        params.query = args;
        break;
      default:
        params.data = args;
        break;
    }

    if (version) {
      params.Version = version;
    }

    try {
      if (typeof onFetch === 'function') {
        onFetch(params, context);
      }

      let resp = await serviceInstance?.fetchOpenAPI<T>(params);
      if (typeof standardizeResult === 'function') {
        resp = standardizeResult(resp, context);
      }

      if (!resp) {
        let errorMessage: string | undefined = undefined;
        if (onError) {
          errorMessage = (onError as INoResponseMessageObject).noRespMessage;
          if (!errorMessage) {
            errorMessage = `${(onError as INoResponseMessageObject).message}\n${getString('noResponse')}`;
          }
        }

        if (!errorMessage) errorMessage = `${getString('failAccessRes')}\n${getString('noResponse')}`;
        const errorResult = generateTextResult(errorMessage);
        if (typeof onError === 'function') {
          onError(errorResult, resp, context);
        }

        return errorResult;
      }

      const error = resp.ResponseMetadata.Error;
      if (error) {
        const errorResult = generateTextResult(`${(onError as IMessageObject)?.message ?? getString('failAccessRes')}\n${getString('reasonFollowing')}\n\n${error.Message}`);
        if (typeof onError === 'function') {
          onError(errorResult, resp, context);
        }

        return errorResult;
      }

      let json = resp.Result;
      const field = (onSuccess as IResponseValueObject)?.field;
      if (field && json) {
        json = (json as Record<string, unknown>)[field] as T;
      }

      const result = generateTextResult(`${(onSuccess as IMessageObject)?.message ?? getString('resultInJson')}\n\n\`\`\`json\n${JSON.stringify(json)}\`\`\``);
      if (typeof onSuccess === 'function') {
        onSuccess(result, resp, context);
      }

      return result;
    } catch (error) {
      let errorMessage = (onFetchError as IMessageObject)?.message ?? getString('failAccessRes');
      if (error instanceof Error) {
        errorMessage += '\n' + getString('reasonFollowing') + '\n\n' + error.message;
      }

      const errorResult = generateTextResult(errorMessage);
      if (typeof onFetchError === 'function') {
        onFetchError(errorResult, error, context);
      }

      return errorResult;
    }
  })
}

/**
 * Adds a set of tools with functionality from Open API of VolcEngine.
 * @param models A set of proxy tool model.
 */
export function addProxyTools(models: IProxyToolModel[], server?: McpServer) {
  if (!models) return;
  for (const i in models) {
    if (typeof i !== 'number' && typeof i !== 'string') continue;
    addProxyTool(models[i], server);
  }
}
