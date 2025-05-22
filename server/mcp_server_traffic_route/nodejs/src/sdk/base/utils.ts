import debug from "debug";
import fs from "fs";
import path from "path";
import packageInfo from "../../package.json";
export const packageName = packageInfo.name;
export const packageVersion = packageInfo.version;
export function createDebug(moduleName: string): debug.Debugger {
  return debug(`${packageName}:${moduleName}`);
}
export function getDefaultOption() {
  const defaultOptions = {
    host: "open.volcengineapi.com",
    region: "cn-north-1",
    protocol: "https:",
    // Read aksk by environment variables
    accessKeyId: process.env.VOLC_ACCESSKEY,
    secretKey: process.env.VOLC_SECRETKEY,
  };
  try {
    // Read aksk from ~/.volc/config. Priority is lower than environment variables
    if (process.env.HOME && !(defaultOptions.accessKeyId && defaultOptions.secretKey)) {
      const homeConfigPath = path.resolve(process.env.HOME, ".volc/config");
      if (fs.existsSync(homeConfigPath)) {
        const configData = JSON.parse(fs.readFileSync(homeConfigPath, { encoding: "utf-8" }));
        if (!defaultOptions.accessKeyId && configData.VOLC_ACCESSKEY) {
          defaultOptions.accessKeyId = configData.VOLC_ACCESSKEY;
        }
        if (!defaultOptions.secretKey && configData.VOLC_SECRETKEY) {
          defaultOptions.secretKey = configData.VOLC_SECRETKEY;
        }
      }
    }
  } catch {}
  return defaultOptions;
}
