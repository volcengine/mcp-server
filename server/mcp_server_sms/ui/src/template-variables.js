import { OperationError } from './client.js';

// 短信接口的占位符语法，与业务参数值无关；不改写正文或变量大小写。
export function templateVariables(content) {
  const matches = [...content.matchAll(/\$\{([^{}]*)\}/g)];
  if (content.replace(/\$\{([^{}]*)\}/g, '').includes('${')
    || matches.some(match => !/^[A-Za-z0-9_]+$/.test(match[1]))) {
    throw new OperationError('请使用完整的 ${变量名}，名称仅含英文、数字或下划线。');
  }
  return matches.map(match => match[1]);
}

export function renderSmsContent(content, params) {
  const names = [...new Set(templateVariables(content))];
  if (names.length !== Object.keys(params).length || names.some(name => !Object.hasOwn(params, name) || !params[name])) {
    throw new OperationError('请完整填写当前模板变量，且不要添加多余变量。');
  }
  return content.replace(/\$\{([^{}]*)\}/g, (_placeholder, name) => params[name]);
}
