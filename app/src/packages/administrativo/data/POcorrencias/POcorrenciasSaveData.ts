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

export async function POcorrenciasSaveCreateData(
  data: Omit<POcorrenciasInterface, 'ocorrencias_id'>,
): Promise<POcorrenciasInterface> {
  if (!usePOcorrenciasMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.POST,
        endpoint: POCORRENCIAS_FAKE_ENDPOINTS.create,
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as POcorrenciasInterface;
    }
  }

  await mockDbDelay(600);
  const list = pocorrenciasListRef.current;
  const newId = list.length > 0 ? Math.max(...list.map((row) => row.ocorrencias_id)) + 1 : 1;
  const created = { ...data, ocorrencias_id: newId } as POcorrenciasInterface;
  list.push(created);
  return created;
}

export async function POcorrenciasSaveUpdateData(
  id: number,
  data: Partial<POcorrenciasInterface>,
): Promise<POcorrenciasInterface> {
  if (!usePOcorrenciasMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.PUT,
        endpoint: POCORRENCIAS_FAKE_ENDPOINTS.update(id),
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as POcorrenciasInterface;
    }
  }

  await mockDbDelay(600);
  const list = pocorrenciasListRef.current;
  const index = list.findIndex((row) => row.ocorrencias_id === id);
  if (index === -1) throw new Error('Ocorrência não encontrada');
  list[index] = { ...list[index], ...data };
  return list[index];
}
