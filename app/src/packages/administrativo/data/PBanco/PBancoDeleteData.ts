import { pbancoListRef } from '@/packages/administrativo/data/PBanco/pbancoInMemory';
import { PBANCO_FAKE_ENDPOINTS, usePBancoMockData } from '@/packages/administrativo/data/PBanco/pbancoDataConfig';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePBancoDeleteData(id: number) {
  if (!usePBancoMockData()) {
    const api = new API();
    return await api.send({
      method: Methods.DELETE,
      endpoint: PBANCO_FAKE_ENDPOINTS.delete(id),
    });
  }

  await mockDbDelay(500);
  const list = pbancoListRef.current;
  const removed = list.find((row) => row.banco_id === id);
  pbancoListRef.current = list.filter((row) => row.banco_id !== id);

  return {
    status: 200,
    message: 'Banco removido com sucesso',
    data: removed ?? { banco_id: id },
  };
}

export const PBancoDeleteData = withClientErrorHandler(executePBancoDeleteData);
