import { plivroNaturezaListRef } from '@/packages/administrativo/data/PLivroNatureza/plivroNaturezaInMemory';
import {
  PLIVRO_NATUREZA_FAKE_ENDPOINTS,
  usePLivroNaturezaMockData,
} from '@/packages/administrativo/data/PLivroNatureza/plivroNaturezaDataConfig';
import type { PLivroNaturezaInterface } from '@/packages/administrativo/interfaces/PLivroNatureza/PLivroNaturezaInterface';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export async function PLivroNaturezaIndexData(): Promise<PLivroNaturezaInterface[]> {
  if (!usePLivroNaturezaMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: PLIVRO_NATUREZA_FAKE_ENDPOINTS.index,
      }),
    );
    const response = await apiCall();
    if (
      Number(response?.status) >= 200 &&
      Number(response?.status) < 300 &&
      Array.isArray(response?.data)
    ) {
      return response.data as PLivroNaturezaInterface[];
    }
  }

  await mockDbDelay(500);
  return [...plivroNaturezaListRef.current];
}
