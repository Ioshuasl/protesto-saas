import { pmotivosCancelamentoListRef } from '@/packages/administrativo/data/PMotivosCancelamento/pmotivosCancelamentoInMemory';
import {
  PMOTIVOS_CANCELAMENTO_FAKE_ENDPOINTS,
  usePMotivosCancelamentoMockData,
} from '@/packages/administrativo/data/PMotivosCancelamento/pmotivosCancelamentoDataConfig';
import type { PMotivosCancelamentoInterface } from '@/packages/administrativo/interfaces/PMotivosCancelamento/PMotivosCancelamentoInterface';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export async function PMotivosCancelamentoSaveCreateData(
  data: Omit<PMotivosCancelamentoInterface, 'motivos_cancelamento_id'>,
): Promise<PMotivosCancelamentoInterface> {
  if (!usePMotivosCancelamentoMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.POST,
        endpoint: PMOTIVOS_CANCELAMENTO_FAKE_ENDPOINTS.create,
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as PMotivosCancelamentoInterface;
    }
  }

  await mockDbDelay(600);
  const list = pmotivosCancelamentoListRef.current;
  const newId =
    list.length > 0
      ? Math.max(...list.map((row) => row.motivos_cancelamento_id)) + 1
      : 1;
  const created = { ...data, motivos_cancelamento_id: newId } as PMotivosCancelamentoInterface;
  list.push(created);
  return created;
}

export async function PMotivosCancelamentoSaveUpdateData(
  id: number,
  data: Partial<PMotivosCancelamentoInterface>,
): Promise<PMotivosCancelamentoInterface> {
  if (!usePMotivosCancelamentoMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.PUT,
        endpoint: PMOTIVOS_CANCELAMENTO_FAKE_ENDPOINTS.update(id),
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as PMotivosCancelamentoInterface;
    }
  }

  await mockDbDelay(600);
  const list = pmotivosCancelamentoListRef.current;
  const index = list.findIndex((row) => row.motivos_cancelamento_id === id);
  if (index === -1) throw new Error('Motivo de cancelamento não encontrado');
  list[index] = { ...list[index], ...data };
  return list[index];
}
