import { pocorrenciasListRef } from '@/packages/administrativo/data/POcorrencias/pocorrenciasInMemory';
import {
  POCORRENCIAS_FAKE_ENDPOINTS,
  usePOcorrenciasMockData,
} from '@/packages/administrativo/data/POcorrencias/pocorrenciasDataConfig';
import type { POcorrenciasInterface } from '@/packages/administrativo/interfaces/POcorrencias/POcorrenciasInterface';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export async function POcorrenciasIndexData(): Promise<POcorrenciasInterface[]> {
  if (!usePOcorrenciasMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: POCORRENCIAS_FAKE_ENDPOINTS.index,
      }),
    );
    const response = await apiCall();
    if (
      Number(response?.status) >= 200 &&
      Number(response?.status) < 300 &&
      Array.isArray(response?.data)
    ) {
      return response.data as POcorrenciasInterface[];
    }
  }

  await mockDbDelay(500);
  return [...pocorrenciasListRef.current];
}
