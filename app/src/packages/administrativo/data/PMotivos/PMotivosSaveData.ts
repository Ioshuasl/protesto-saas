import { pmotivosListRef } from '@/packages/administrativo/data/PMotivos/pmotivosInMemory';
import {
  PMOTIVOS_FAKE_ENDPOINTS,
  usePMotivosMockData,
} from '@/packages/administrativo/data/PMotivos/pmotivosDataConfig';
import type { PMotivosInterface } from '@/packages/administrativo/interfaces/PMotivos/PMotivosInterface';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export async function PMotivosSaveCreateData(
  data: Omit<PMotivosInterface, 'motivos_id'>,
): Promise<PMotivosInterface> {
  if (!usePMotivosMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.POST,
        endpoint: PMOTIVOS_FAKE_ENDPOINTS.create,
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as PMotivosInterface;
    }
  }

  await mockDbDelay(600);
  const list = pmotivosListRef.current;
  const newId = list.length > 0 ? Math.max(...list.map((row) => row.motivos_id)) + 1 : 1;
  const created = { ...data, motivos_id: newId } as PMotivosInterface;
  list.push(created);
  return created;
}

export async function PMotivosSaveUpdateData(
  id: number,
  data: Partial<PMotivosInterface>,
): Promise<PMotivosInterface> {
  if (!usePMotivosMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.PUT,
        endpoint: PMOTIVOS_FAKE_ENDPOINTS.update(id),
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as PMotivosInterface;
    }
  }

  await mockDbDelay(600);
  const list = pmotivosListRef.current;
  const index = list.findIndex((row) => row.motivos_id === id);
  if (index === -1) throw new Error('Motivo de apontamento não encontrado');
  list[index] = { ...list[index], ...data };
  return list[index];
}
