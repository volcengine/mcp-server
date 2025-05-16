import type { ILocaleStrings } from "./interfaces";
import { Resources } from "langpack";
import { strings as hansStrings } from './hans';
import { strings as enStrings } from './en';

const settings = {
  hasInit: false
};

/**
 * The resources.
 */
export const res = new Resources();

/**
 * Initializes the language pack.
 */
export function init(force = false) {
  if (settings.hasInit && !force) return;
  settings.hasInit = true;
  res.register({
    language: 'en',
    strings: enStrings,
  });
  res.register({
    language: ['zh-Hans', 'zh-CN', 'zh-SG'],
    strings: hansStrings,
  });
}

/**
 * Gets the locale string.
 * @param key The key of resource.
 * @returns A string in local language.
 */
export function getString(key: keyof(ILocaleStrings)) {
  init();
  return res.getLocaleString(key);
}
