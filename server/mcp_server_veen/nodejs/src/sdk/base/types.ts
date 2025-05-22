import { Method } from "axios";
export interface OpenApiError {
  Code?: string;
  Message: string;
  CodeN?: number;
}
export interface OpenApiResponseMetadataParams {
  RequestId?: string;
  Action?: string;
  Version?: string;
  Service?: string;
  Region?: string;
  Error?: OpenApiError;
}
export interface OpenApiResponseMetadata extends OpenApiResponseMetadataParams {
  RequestId: string;
  Service: string;
}
export interface OpenApiResponse<T> {
  ResponseMetadata: OpenApiResponseMetadata;
  Result?: T;
}

export interface STS {
  /**
   * create time of STS. unix timestamp.
   */
  CurrentTime: string | number;
  /**
   * expire time of STS. unix timestamp.
   */
  ExpiredTime: string | number;
  AccessKeyId: string;
  SecretKey: string;
  SessionToken: string;
}
export interface RequestObj {
  region: string;
  method: string;
  params?: any;
  pathname?: string;
  headers?: any;
  body?: any;
}
export interface SignerOptions {
  bodySha256?: string;
}
export interface CredentialsBase {
  accessKeyId?: string;
  secretKey?: string;
  sessionToken?: string;
}
export interface Credentials extends CredentialsBase {
  accessKeyId: string;
  secretKey: string;
}
export interface ServiceOptionsBase extends CredentialsBase {
  /**
   * openpai host default is 'cn-north-1'
   */
  region?: string;
  /**
   * openpai host default is 'open.volcengineapi.com'
   */
  host?: string;
  serviceName?: string;
  /**
   * openpai host default is 'http'
   */
  protocol?: string;
  /**
   * default open api version of this service
   */
  defaultVersion?: string;
}
export interface ServiceOptions extends ServiceOptionsBase {
  serviceName: string;
}
export interface FetchParams {
  Action: string;
  Version?: string;
  query?: any;
  pathname?: string;
}
export interface CreateAPIParams {
  /**
   * OpenAPI Version. If not provide, will use service defaultVersion.
   */
  Version?: string;
  /**
   * http method like GET POST PUT
   */
  method?: Method;
  /**
   * body content type. support: json urlencode form-data
   */
  contentType?: "json" | "urlencode" | "form-data";
  /**
   * keys in query
   */
  queryKeys?: string[];
}

export interface Statement {
  Effect: string;
  Action: string[];
  Resource: string[];
  Condition?: string;
}

export interface Policy {
  Statement: Statement[];
}

export interface SecurityToken2 {
  AccessKeyId: string;
  SecretAccessKey: string;
  CurrentTime?: string;
  ExpiredTime?: string;
  SessionToken?: string;
}

export interface InnerToken {
  LTAccessKeyId: string;
  AccessKeyId: string;
  SignedSecretAccessKey: string;
  ExpiredTime: number;
  PolicyString: string;
  Signature: string;
}
