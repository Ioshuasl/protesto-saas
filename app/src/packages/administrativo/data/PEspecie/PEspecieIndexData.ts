import { pespecieListRef } from '@/packages/administrativo/data/PEspecie/pespecieInMemory';
import {
  PESPECIE_FAKE_ENDPOINTS,
  usePEspecieMockData,
} from '@/packages/administrativo/data/PEspecie/pespecieDataConfig';
import type { PEspecieInterface } from '@/packages/administrativo/interfaces/PEspecie/PEspecieInterface';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export async function PEspecieIndexData(): Promise<PEspecieInterface[]> {
  if (!usePEspecieMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: PESPECIE_FAKE_ENDPOINTS.index,
      }),
    );
    const response = await apiCall();
    if (
      Number(response?.status) >= 200 &&
      Number(response?.status) < 300 &&
      Array.isArray(response?.data)
    ) {
      return response.data as PEspecieInterface[];
    }
  }

  await mockDbDelay(500);
  return [...pespecieListRef.current];
}
