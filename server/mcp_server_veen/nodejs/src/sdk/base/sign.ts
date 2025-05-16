import hmacSHA256 from "crypto-js/hmac-sha256";
import SHA256 from "crypto-js/sha256";
import CryptoJS from "crypto-js/core";
import { Credentials, RequestObj, SignerOptions } from "./types";
import FormData from "form-data";
import utils from "util";

const debugLog = utils.debuglog("signer");

const util = {
  crypto: {
    hmac: function hmac(key, string) {
      return hmacSHA256(string, key);
    },

    sha256: function sha256(data) {
      return Buffer.isBuffer(data) ? SHA256(arrayBufferToWordArray(data)) : SHA256(data);
    },
  },
};

const unsignableHeaders = [
  "authorization",
  "content-type",
  "content-length",
  "user-agent",
  "presigned-expires",
  "expect",
];

const constant = {
  algorithm: "HMAC-SHA256",
  v4Identifier: "request",
  dateHeader: "X-Date",
  tokenHeader: "X-Security-Token",
  contentSha256Header: "X-Content-Sha256",
  notSignBody: "X-NotSignBody",
  kDatePrefix: "",
  credential: "X-Credential",
  algorithmKey: "X-Algorithm",
  signHeadersKey: "X-SignedHeaders",
  signQueriesKey: "X-SignedQueries",
  signatureKey: "X-Signature",
};

const uriEscape = (str) => {
  try {
    return encodeURIComponent(str)
      .replace(/[^A-Za-z0-9_.~\-%]+/g, escape)
      .replace(/[*]/g, (ch) => `%${ch.charCodeAt(0).toString(16).toUpperCase()}`);
  } catch (e) {
    return "";
  }
};

export const queryParamsToString = (params) =>
  Object.keys(params)
    .map((key) => {
      const val = params[key];
      if (typeof val === "undefined" || val === null) {
        return;
      }

      const escapedKey = uriEscape(key);
      if (!escapedKey) {
        return;
      }

      if (Array.isArray(val)) {
        return `${escapedKey}=${val.map(uriEscape).sort().join(`&${escapedKey}=`)}`;
      }

      return `${escapedKey}=${uriEscape(val)}`;
    })
    .filter((v) => v)
    .join("&");

export default class Signer {
  request: RequestObj;
  serviceName: string;
  bodySha256?: string;

  constructor(request: RequestObj, serviceName: string, options?: SignerOptions) {
    this.request = request;
    this.request.headers = request.headers || {};
    this.serviceName = serviceName;
    options = options || {};
    this.bodySha256 = options.bodySha256;
    this.request.params = this.sortParams(this.request.params);
  }

  sortParams(params) {
    const newParams = {};
    if (params) {
      Object.keys(params)
        .filter((key) => {
          const value = params[key];
          return typeof value !== "undefined" && value !== null;
        })
        .sort()
        .map((key) => {
          newParams[key] = params[key];
        });
    }
    return newParams;
  }

  addAuthorization(credentials: Credentials, date?: Date): void {
    const datetime = this.getDateTime(date);
    this.addHeaders(credentials, datetime);
    this.request.headers["Authorization"] = this.authorization(credentials, datetime);
  }

  authorization(credentials: Credentials, datetime: string) {
    const parts: string[] = [];
    const credString = this.credentialString(datetime);
    parts.push(`${constant.algorithm} Credential=${credentials.accessKeyId}/${credString}`);
    parts.push(`SignedHeaders=${this.signedHeaders()}`);
    // parts.push(`SignedQueries=${this.signedQueries()}`);
    parts.push(`Signature=${this.signature(credentials, datetime)}`);
    return parts.join(", ");
  }

  getSignUrl(credentials: Credentials, date?: Date): string {
    const datetime = this.getDateTime(date);
    let query = { ...this.request.params };
    const params = this.request.params;
    const headers = this.request.headers;
    if (credentials.sessionToken) {
      query[constant.tokenHeader] = credentials.sessionToken;
    }
    query[constant.dateHeader] = datetime;
    query[constant.notSignBody] = "";
    query[constant.credential] = `${credentials.accessKeyId}/${this.credentialString(datetime)}`;
    query[constant.algorithmKey] = constant.algorithm;
    query[constant.signHeadersKey] = "";
    query[constant.signQueriesKey] = undefined;
    query[constant.signatureKey] = undefined;
    query = this.sortParams(query);
    this.request.params = query;
    this.request.headers = {};
    const sig = this.signature(credentials, datetime);
    this.request.params = params;
    this.request.headers = headers;
    query[constant.signQueriesKey] = Object.keys(query).sort().join(";");
    query[constant.signatureKey] = sig;
    return queryParamsToString(query);
  }

  getDateTime(date?: Date): string {
    return this.iso8601(date).replace(/[:\-]|\.\d{3}/g, "");
  }

  addHeaders(credentials: Credentials, datetime: string) {
    this.request.headers[constant.dateHeader] = datetime;
    if (credentials.sessionToken) {
      this.request.headers[constant.tokenHeader] = credentials.sessionToken;
    }
    if (this.request.body) {
      let body = this.request.body;
      if (typeof body !== "string") {
        if (body instanceof URLSearchParams) {
          body = body.toString();
        } else if (body instanceof FormData) {
          body = body.getBuffer();
        } else {
          body = JSON.stringify(body);
        }
      }
      this.request.headers[constant.contentSha256Header] =
        this.bodySha256 || util.crypto.sha256(body).toString();
    }
  }

  signature(credentials: Credentials, datetime: string) {
    const signingKey = this.getSigningKey(
      credentials,
      datetime.substr(0, 8),
      this.request.region,
      this.serviceName
    );
    return util.crypto.hmac(signingKey, this.stringToSign(datetime));
  }

  stringToSign(datetime: string) {
    const parts: string[] = [];
    parts.push(constant.algorithm);
    parts.push(datetime);
    parts.push(this.credentialString(datetime));
    parts.push(this.hexEncodedHash(this.canonicalString()).toString());
    const result = parts.join("\n");
    debugLog("--------SignString:\n%s", result);
    return result;
  }

  canonicalString(): string {
    const parts: string[] = [],
      pathname = this.request.pathname || "/";

    parts.push(this.request.method.toUpperCase());
    parts.push(pathname);
    const queryString = queryParamsToString(this.request.params) || "";
    parts.push(queryString);
    parts.push(`${this.canonicalHeaders()}\n`);
    parts.push(this.signedHeaders());
    parts.push(this.hexEncodedBodyHash());
    const result = parts.join("\n");
    debugLog("--------CanonicalString:\n%s", result);
    return result;
  }

  canonicalHeaders() {
    const headers: [string, string][] = [];
    Object.keys(this.request.headers).forEach((key) => {
      headers.push([key, this.request.headers[key]]);
    });
    headers.sort((a, b) => (a[0].toLowerCase() < b[0].toLowerCase() ? -1 : 1));
    const parts: string[] = [];
    headers.forEach((item) => {
      const key = item[0].toLowerCase();
      if (this.isSignableHeader(key)) {
        const value = item[1];
        if (
          typeof value === "undefined" ||
          value === null ||
          typeof value.toString !== "function"
        ) {
          throw new Error(`Header ${key} contains invalid value`);
        }
        parts.push(`${key}:${this.canonicalHeaderValues(value.toString())}`);
      }
    });
    return parts.join("\n");
  }

  canonicalHeaderValues(values: string) {
    return values.replace(/\s+/g, " ").replace(/^\s+|\s+$/g, "");
  }

  signedHeaders() {
    const keys: string[] = [];
    Object.keys(this.request.headers).forEach((key) => {
      key = key.toLowerCase();
      if (this.isSignableHeader(key)) {
        keys.push(key);
      }
    });
    return keys.sort().join(";");
  }

  signedQueries() {
    return Object.keys(this.request.params).join(";");
  }

  credentialString(datetime: string) {
    return this.createScope(datetime.substr(0, 8), this.request.region, this.serviceName);
  }

  hexEncodedHash(str: string) {
    return util.crypto.sha256(str);
  }

  hexEncodedBodyHash() {
    if (this.request.headers[constant.contentSha256Header]) {
      return this.request.headers[constant.contentSha256Header];
    }

    if (this.request.body) {
      return this.hexEncodedHash(queryParamsToString(this.request.body));
    }
    return this.hexEncodedHash("");
  }

  isSignableHeader(key: string) {
    return unsignableHeaders.indexOf(key) < 0;
  }

  iso8601(date?: Date) {
    if (date === undefined) {
      date = new Date();
    }
    return date.toISOString().replace(/\.\d{3}Z$/, "Z");
  }

  getSigningKey(credentials: Credentials, date: string, region: string, service: string) {
    const kDate = util.crypto.hmac(`${constant.kDatePrefix}${credentials.secretKey}`, date);
    const kRegion = util.crypto.hmac(kDate, region);
    const kService = util.crypto.hmac(kRegion, service);

    return util.crypto.hmac(kService, constant.v4Identifier);
  }

  createScope(date: string, region: string, serviceName: string) {
    return [date.substr(0, 8), region, serviceName, constant.v4Identifier].join("/");
  }
}

function arrayBufferToWordArray(buf: Buffer) {
  const i8a = new Uint8Array(buf);
  const a: number[] = [];
  for (let i = 0; i < i8a.length; i += 4) {
    a.push((i8a[i] << 24) | (i8a[i + 1] << 16) | (i8a[i + 2] << 8) | i8a[i + 3]);
  }
  return CryptoJS.lib.WordArray.create(a, i8a.length);
}
