import { OperationError } from './client.js';

export const labels = {
  useVolcLink: '使用火山短链', protocol: '文案链接协议', link: '文案链接',
  linkDomainIcp: '文案域名备案号', linkDomainIcpBody: '文案域名备案主体',
  linkDomain: '文案链接二级域名', linkPath: '文案链接 Path',
  jumpLink: '跳转链接', jumpLinkDomainIcp: '跳转域名备案号', jumpLinkDomainIcpBody: '跳转域名备案主体',
  jumpLinkDomain: '跳转链接二级域名', jumpLinkPath: '跳转链接 Path',
  numberType: '号码类型', number: '联系号码', company: '号码所属企业',
  numberPerson: '号码所属人', personType: '证件类型', personId: '证件号码',
  numberProvince: '号码归属省份', numberCity: '号码归属城市',
};
export const numberTypes = [[1, '手机号码'], [2, '400 号码'], [3, '700 号码'], [4, '800 号码'], [5, '95 / 96 号码'], [6, '12 号码'], [7, '固定电话']];
const numberPatterns = {
  1: /^1[3456789]\d{9}$/, 2: /^400\d{7}$/, 3: /^700\d+$/, 4: /^800\d{7}$/,
  5: /^9[56]\d{3}$/, 6: /^12\d{3}$/, 7: /^\d{10,12}$/,
};
const numberErrors = {
  1: '请输入正确的手机号', 2: '请输入正确的 400 号码', 3: '请输入正确的 700 号码',
  4: '请输入正确的 800 号码', 5: '请输入正确的 95 或 96 号码',
  6: '请输入正确的 12 号码', 7: '请输入正确的固定电话',
};

export function inferNumberType(number) {
  if (!number) return undefined;
  if (/^1[3456789]/.test(number)) return 1;
  if (number.startsWith('400')) return 2;
  if (number.startsWith('700')) return 3;
  if (number.startsWith('800')) return 4;
  if (/^9[56]/.test(number)) return 5;
  if (number.startsWith('12')) return 6;
  return 7;
}

export function inferProtocol(link) {
  if (link?.startsWith('https://')) return 'https';
  if (link?.startsWith('http://')) return 'http';
  return '缺省';
}

export function parseLink(link) {
  if (!link) return { domain: '', path: '' };
  try {
    const parsed = new URL(link.includes('://') ? link : `https://${link}`);
    return { domain: parsed.hostname, path: parsed.pathname + parsed.search };
  } catch {
    return { domain: '', path: '' };
  }
}

export function initialRow(kind, row = {}) {
  if (kind === 'phone') {
    const hasPerson = ['numberPerson', 'personType', 'personId'].some(key => row[key] != null);
    return { ...row, numberType: row.numberType ?? inferNumberType(row.number) ?? (hasPerson ? 1 : undefined) };
  }
  return {
    ...row, useVolcLink: row.useVolcLink === true,
    ...(!row.useVolcLink && row.link && !row.protocol ? { protocol: inferProtocol(row.link) } : {}),
  };
}

export function validateRows(kind, rows) {
  const errors = {};
  const requireField = (index, row, key) => {
    if (row[key] == null || row[key] === '') errors[`${index}.${key}`] = '此项必填';
  };
  rows.forEach((row, index) => {
    if (kind === 'link') {
      requireField(index, row, 'useVolcLink');
      (row.useVolcLink
        ? ['jumpLink', 'jumpLinkDomainIcp', 'jumpLinkDomainIcpBody']
        : ['protocol', 'link', 'linkDomainIcp', 'linkDomainIcpBody'])
        .forEach(key => requireField(index, row, key));
    } else {
      requireField(index, row, 'numberType');
      requireField(index, row, 'number');
      if (row.numberType && row.number && !numberPatterns[row.numberType]?.test(row.number)) {
        errors[`${index}.number`] = numberErrors[row.numberType] ?? '请选择正确的号码类型';
      }
    }
  });
  return errors;
}

export function trafficPayload(kind, rows) {
  if (!rows.length || rows.length > (kind === 'link' ? 10 : 100)) {
    throw new OperationError(kind === 'link' ? '本次可录入 1 至 10 条链接。' : '本次可录入 1 至 100 条号码。');
  }
  const firstError = Object.entries(validateRows(kind, rows))[0];
  if (firstError) {
    const [index, key] = firstError[0].split('.');
    throw new OperationError(`第 ${Number(index) + 1} 条${labels[key]}：${firstError[1]}`);
  }
  return rows.map(row => {
    if (kind === 'phone') {
      const fields = ['numberType', 'number', 'numberProvince', 'numberCity',
        ...(row.numberType === 1 ? ['numberPerson', 'personType', 'personId'] : ['company'])];
      return Object.fromEntries(fields.filter(key => row[key] != null).map(key => [key, row[key]]));
    }
    const linkParts = parseLink(row.link);
    const jumpParts = parseLink(row.jumpLink);
    const complete = {
      ...row,
      ...(row.link ? { linkDomain: linkParts.domain, linkPath: linkParts.path } : {}),
      ...(row.jumpLink ? { jumpLinkDomain: jumpParts.domain, jumpLinkPath: jumpParts.path } : {}),
    };
    const fields = row.useVolcLink
      ? ['useVolcLink', 'jumpLink', 'jumpLinkDomainIcp', 'jumpLinkDomainIcpBody', 'jumpLinkDomain', 'jumpLinkPath']
      : ['useVolcLink', 'protocol', 'link', 'linkDomainIcp', 'linkDomainIcpBody', 'linkDomain', 'linkPath',
        'jumpLink', 'jumpLinkDomainIcp', 'jumpLinkDomainIcpBody', 'jumpLinkDomain', 'jumpLinkPath'];
    return Object.fromEntries(fields.filter(key => complete[key] != null).map(key => [key, complete[key]]));
  });
}

export function displayValue(key, value) {
  if (key === 'useVolcLink') return value ? '是' : '否';
  if (key === 'numberType') return numberTypes.find(([id]) => id === value)?.[1] ?? String(value);
  if (key === 'personType') return value === 1 ? '居民身份证' : '未填写';
  return String(value);
}
