import { ppessoaListRef } from '@/packages/administrativo/data/PPessoa/ppessoaInMemory';
import {
  PPESSOA_FAKE_ENDPOINTS,
  usePPessoaMockData,
} from '@/packages/administrativo/data/PPessoa/ppessoaDataConfig';
import type { PPessoaInterface } from '@/packages/administrativo/interfaces/PPessoa/PPessoaInterface';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export async function PPessoaIndexData(): Promise<PPessoaInterface[]> {
  if (!usePPessoaMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: PPESSOA_FAKE_ENDPOINTS.index,
      }),
    );
    const response = await apiCall();
    if (
      Number(response?.status) >= 200 &&
      Number(response?.status) < 300 &&
      Array.isArray(response?.data)
    ) {
      return response.data as PPessoaInterface[];
    }
  }

  await mockDbDelay(500);
  return [...ppessoaListRef.current];
}
