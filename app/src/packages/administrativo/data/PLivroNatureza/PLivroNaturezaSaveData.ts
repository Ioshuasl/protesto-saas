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

export async function PLivroNaturezaSaveCreateData(
  data: Omit<PLivroNaturezaInterface, 'livro_natureza_id'>,
): Promise<PLivroNaturezaInterface> {
  if (!usePLivroNaturezaMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.POST,
        endpoint: PLIVRO_NATUREZA_FAKE_ENDPOINTS.create,
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as PLivroNaturezaInterface;
    }
  }

  await mockDbDelay(600);
  const list = plivroNaturezaListRef.current;
  const newId =
    list.length > 0 ? Math.max(...list.map((row) => row.livro_natureza_id)) + 1 : 1;
  const created = { ...data, livro_natureza_id: newId } as PLivroNaturezaInterface;
  list.push(created);
  return created;
}

export async function PLivroNaturezaSaveUpdateData(
  id: number,
  data: Partial<PLivroNaturezaInterface>,
): Promise<PLivroNaturezaInterface> {
  if (!usePLivroNaturezaMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.PUT,
        endpoint: PLIVRO_NATUREZA_FAKE_ENDPOINTS.update(id),
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as PLivroNaturezaInterface;
    }
  }

  await mockDbDelay(600);
  const list = plivroNaturezaListRef.current;
  const index = list.findIndex((row) => row.livro_natureza_id === id);
  if (index === -1) throw new Error('Livro Natureza não encontrado');
  list[index] = { ...list[index], ...data };
  return list[index];
}
