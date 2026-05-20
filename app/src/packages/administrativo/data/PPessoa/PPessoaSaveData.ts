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

export async function PPessoaSaveCreateData(
  data: Omit<PPessoaInterface, 'pessoa_id'>,
): Promise<PPessoaInterface> {
  if (!usePPessoaMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.POST,
        endpoint: PPESSOA_FAKE_ENDPOINTS.create,
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as PPessoaInterface;
    }
  }

  await mockDbDelay(600);
  const list = ppessoaListRef.current;
  const newId = list.length > 0 ? Math.max(...list.map((p) => p.pessoa_id)) + 1 : 1;
  const newPessoa: PPessoaInterface = { ...data, pessoa_id: newId };
  list.push(newPessoa);
  return newPessoa;
}

export async function PPessoaSaveUpdateData(
  id: number,
  data: Partial<PPessoaInterface>,
): Promise<PPessoaInterface> {
  if (!usePPessoaMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.PUT,
        endpoint: PPESSOA_FAKE_ENDPOINTS.update(id),
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as PPessoaInterface;
    }
  }

  await mockDbDelay(600);
  const list = ppessoaListRef.current;
  const index = list.findIndex((p) => p.pessoa_id === id);
  if (index === -1) throw new Error('Pessoa não encontrada');
  list[index] = { ...list[index], ...data };
  return list[index];
}
