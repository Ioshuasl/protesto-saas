import { plivroAndamentoListRef } from '@/packages/administrativo/data/PLivroAndamento/plivroAndamentoInMemory';
import {
  PLIVRO_ANDAMENTO_FAKE_ENDPOINTS,
  usePLivroAndamentoMockData,
} from '@/packages/administrativo/data/PLivroAndamento/plivroAndamentoDataConfig';
import type { PLivroAndamentoInterface } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoInterface';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export async function PLivroAndamentoIndexData(): Promise<PLivroAndamentoInterface[]> {
  if (!usePLivroAndamentoMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: PLIVRO_ANDAMENTO_FAKE_ENDPOINTS.index,
      }),
    );
    const response = await apiCall();
    if (
      Number(response?.status) >= 200 &&
      Number(response?.status) < 300 &&
      Array.isArray(response?.data)
    ) {
      return response.data as PLivroAndamentoInterface[];
    }
  }

  await mockDbDelay(500);
  return [...plivroAndamentoListRef.current];
}
