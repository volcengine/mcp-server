import { useEffect, useRef, useState } from 'react';
import { OperationError, page, withPrefilledOptions } from './client.js';
import { messageGroupSchema } from './contracts.js';

// 两个新表单复用消息组分页与预填定位；实际资源始终来自当前授权账号的查询结果。
export function useMessageGroups(client, operation, initialIds = []) {
  const initial = useRef(initialIds);
  const [listing, setListing] = useState({ rows: [], total: 0, page: 0 });
  const [prefilled, setPrefilled] = useState([]);
  const load = async (next = listing.page + 1) => {
    const result = page(await client.query('GetSubAccountListForAgent', { pageIndex: next, pageSize: 100 }), messageGroupSchema);
    setListing(current => ({ rows: next === 1 ? result.rows : [...current.rows, ...result.rows], total: result.total, page: next }));
    return result.rows;
  };
  useEffect(() => {
    operation.run(async () => {
      const rows = await load(1);
      const exact = [];
      for (const id of initial.current) {
        if (rows.some(row => row.subAccountId === id)) continue;
        const found = page(await client.query('GetSubAccountListForAgent', { subAccount: id, pageIndex: 1, pageSize: 100 }), messageGroupSchema)
          .rows.find(row => row.subAccountId === id);
        if (!found) throw new OperationError('预填消息组当前不可用，请重新选择。');
        exact.push(found);
      }
      setPrefilled(exact);
    });
  }, [client]);
  return { ...listing, options: withPrefilledOptions(listing.rows, prefilled, 'subAccountId'), load };
}
