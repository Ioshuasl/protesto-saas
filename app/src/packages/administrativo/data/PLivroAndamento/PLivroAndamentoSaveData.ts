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

export async function PLivroAndamentoSaveCreateData(
  data: Omit<PLivroAndamentoInterface, 'livro_andamento_id'>,
): Promise<PLivroAndamentoInterface> {
  if (!usePLivroAndamentoMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.POST,
        endpoint: PLIVRO_ANDAMENTO_FAKE_ENDPOINTS.create,
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as PLivroAndamentoInterface;
    }
  }

  await mockDbDelay(600);
  const list = plivroAndamentoListRef.current;
  const newId =
    list.length > 0 ? Math.max(...list.map((row) => row.livro_andamento_id)) + 1 : 1;
  const created = { ...data, livro_andamento_id: newId } as PLivroAndamentoInterface;
  list.push(created);
  return created;
}

export async function PLivroAndamentoSaveUpdateData(
  id: number,
  data: Partial<PLivroAndamentoInterface>,
): Promise<PLivroAndamentoInterface> {
  if (!usePLivroAndamentoMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.PUT,
        endpoint: PLIVRO_ANDAMENTO_FAKE_ENDPOINTS.update(id),
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as PLivroAndamentoInterface;
    }
  }

  await mockDbDelay(600);
  const list = plivroAndamentoListRef.current;
  const index = list.findIndex((row) => row.livro_andamento_id === id);
  if (index === -1) throw new Error('Livro Andamento não encontrado');
  list[index] = { ...list[index], ...data };
  return list[index];
}
