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

export async function PEspecieShowData(id: number): Promise<PEspecieInterface | undefined> {
  if (!usePEspecieMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: PESPECIE_FAKE_ENDPOINTS.show(id),
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as PEspecieInterface;
    }
  }

  await mockDbDelay(300);
  return pespecieListRef.current.find((row) => row.especie_id === id);
}
