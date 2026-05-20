import { pbancoListRef } from '@/packages/administrativo/data/PBanco/pbancoInMemory';
import { PBANCO_FAKE_ENDPOINTS, usePBancoMockData } from '@/packages/administrativo/data/PBanco/pbancoDataConfig';
import type { PBancoInterface } from '@/packages/administrativo/interfaces/PBanco/PBancoInterface';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export async function PBancoSaveCreateData(
  data: Omit<PBancoInterface, 'banco_id'>,
): Promise<PBancoInterface> {
  if (!usePBancoMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.POST,
        endpoint: PBANCO_FAKE_ENDPOINTS.create,
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as PBancoInterface;
    }
  }

  await mockDbDelay(600);
  const list = pbancoListRef.current;
  const newId = list.length > 0 ? Math.max(...list.map((row) => row.banco_id)) + 1 : 1;
  const created = { ...data, banco_id: newId } as PBancoInterface;
  list.push(created);
  return created;
}

export async function PBancoSaveUpdateData(
  id: number,
  data: Partial<PBancoInterface>,
): Promise<PBancoInterface> {
  if (!usePBancoMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.PUT,
        endpoint: PBANCO_FAKE_ENDPOINTS.update(id),
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as PBancoInterface;
    }
  }

  await mockDbDelay(600);
  const list = pbancoListRef.current;
  const index = list.findIndex((row) => row.banco_id === id);
  if (index === -1) throw new Error('Banco não encontrado');
  list[index] = { ...list[index], ...data };
  return list[index];
}
