import { pbancoListRef } from '@/packages/administrativo/data/PBanco/pbancoInMemory';
import { PBANCO_FAKE_ENDPOINTS, usePBancoMockData } from '@/packages/administrativo/data/PBanco/pbancoDataConfig';
import type { PBancoInterface } from '@/packages/administrativo/interfaces/PBanco/PBancoInterface';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export async function PBancoShowData(id: number): Promise<PBancoInterface | undefined> {
  if (!usePBancoMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: PBANCO_FAKE_ENDPOINTS.show(id),
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as PBancoInterface;
    }
  }

  await mockDbDelay(300);
  return pbancoListRef.current.find((row) => row.banco_id === id);
}
