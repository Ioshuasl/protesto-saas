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

export async function PEspecieSaveCreateData(
  data: Omit<PEspecieInterface, 'especie_id'>,
): Promise<PEspecieInterface> {
  if (!usePEspecieMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.POST,
        endpoint: PESPECIE_FAKE_ENDPOINTS.create,
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as PEspecieInterface;
    }
  }

  await mockDbDelay(600);
  const list = pespecieListRef.current;
  const newId = list.length > 0 ? Math.max(...list.map((row) => row.especie_id)) + 1 : 1;
  const created = { ...data, especie_id: newId } as PEspecieInterface;
  list.push(created);
  return created;
}

export async function PEspecieSaveUpdateData(
  id: number,
  data: Partial<PEspecieInterface>,
): Promise<PEspecieInterface> {
  if (!usePEspecieMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.PUT,
        endpoint: PESPECIE_FAKE_ENDPOINTS.update(id),
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as PEspecieInterface;
    }
  }

  await mockDbDelay(600);
  const list = pespecieListRef.current;
  const index = list.findIndex((row) => row.especie_id === id);
  if (index === -1) throw new Error('Espécie não encontrada');
  list[index] = { ...list[index], ...data };
  return list[index];
}
