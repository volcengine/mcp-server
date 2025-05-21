import { InnerToken, ServiceOptions, SecurityToken2, Policy } from "./types";
import { v4 as uuidv4 } from "uuid";
import crypto from "crypto";

const LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

function base64(str: string): string {
  return Buffer.from(str).toString("base64");
}

function randStringRunes(n: number): string {
  const arr: string[] = [];
  for (let i = 0; i < n; i++) {
    arr.push(LETTERS[Math.floor(Math.random() * 32)]);
  }
  return arr.join("");
}

function GenerateAccessKeyId(prefix: string): string {
  const uid = uuidv4();
  const uidBase64 = base64(uid.replace(/-/g, "")).replace(/=|\/|\+|-/g, "");
  return prefix + uidBase64;
}

function toBuffer(x: any) {
  if (x instanceof Buffer) return x;
  return Buffer.from(x, "utf8");
}

function ZeroPadding(data, blockSize: number) {
  const padding = blockSize - (data.length % blockSize);
  if (padding === 0) {
    return data;
  }
  const buff = Buffer.alloc(padding);
  const totalLength = data.length + padding;
  return Buffer.concat([data, buff], totalLength);
}

function AesEncryptCBCWithBase64(data, key) {
  if ([16, 24, 32].indexOf(key.length) < 0) {
    throw new Error("aes cbc block size must be 16|24|32 bytes");
  }

  data = toBuffer(data);

  key = toBuffer(key);

  const blocksize = key.length;
  const iv = key;
  const cipher = crypto.createCipheriv(`aes-128-cbc`, key, iv);
  const finaldata = ZeroPadding(data, blocksize);

  let encrypted = cipher.update(finaldata);
  const final = cipher.final();
  encrypted = Buffer.concat([encrypted, final], encrypted.length + final.length);
  return Buffer.from(encrypted).toString("base64");
}

function GenerateSecretKey(): string {
  const randomString = randStringRunes(32);
  return AesEncryptCBCWithBase64(randomString, "volcenginenodejs");
}

function CreateTempAKSK(): { AccessKeyId: string; SecretAccessKey: string } {
  return {
    AccessKeyId: GenerateAccessKeyId("AKTP"),
    SecretAccessKey: GenerateSecretKey(),
  };
}

function hmac(type: string, str: string, secret): string {
  return crypto.createHmac(type, secret).update(str).digest("hex");
}

function hash(type, str: string) {
  return crypto.createHash(type).update(str).digest();
}

function CreateInnerToken(
  config: ServiceOptions,
  sts: SecurityToken2,
  inlinePolicy: Policy | undefined,
  t: number
): InnerToken {
  const key = hash("md5", config.secretKey as string);

  let SignedSecretAccessKey = AesEncryptCBCWithBase64(sts.SecretAccessKey, key);
  SignedSecretAccessKey = SignedSecretAccessKey.slice(0, -24);

  const signStr = Object.values({
    LTAccessKeyId: config.accessKeyId,
    AccessKeyId: sts.AccessKeyId,
    ExpiredTime: t,
    SignedSecretAccessKey,
    PolicyString: inlinePolicy ? JSON.stringify(inlinePolicy) : "",
  }).join("|");

  return {
    LTAccessKeyId: config.accessKeyId as string,
    AccessKeyId: sts.AccessKeyId,
    SignedSecretAccessKey,
    ExpiredTime: t,
    PolicyString: inlinePolicy ? JSON.stringify(inlinePolicy) : "",
    Signature: hmac("sha256", signStr, key),
  };
}

export { CreateInnerToken, CreateTempAKSK, base64 };
