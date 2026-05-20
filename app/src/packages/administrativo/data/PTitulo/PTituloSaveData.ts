import { enrichTitulo, mapStatusToOcorrencia } from '@/packages/administrativo/data/PTitulo/ptituloEnrich';
import { ptituloListRef } from '@/packages/administrativo/data/PTitulo/ptituloInMemory';
import {
  PTITULO_FAKE_ENDPOINTS,
  isPTituloMockDataEnabled,
} from '@/packages/administrativo/data/PTitulo/ptituloDataConfig';
import type { PTituloInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloInterface';
import type { TituloListItem, TituloStatus } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export async function PTituloSaveUpdateStatusData(
  id: number,
  status: TituloStatus,
): Promise<TituloListItem> {
  if (!isPTituloMockDataEnabled()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.PUT,
        endpoint: PTITULO_FAKE_ENDPOINTS.updateStatus(id),
        body: { status },
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return enrichTitulo(response.data as PTituloInterface);
    }
  }

  await mockDbDelay(500);
  const list = ptituloListRef.current;
  const index = list.findIndex((t) => t.titulo_id === id);
  if (index === -1) throw new Error('Título não encontrado');

  const now = new Date();
  const partial: Partial<PTituloInterface> = { situacao_aceite: status };
  const ocorrenciaId = mapStatusToOcorrencia(status);
  if (ocorrenciaId) partial.ocorrencia_id = ocorrenciaId;

  if (status === 'Protestado') partial.data_protesto = now;
  if (status === 'Pago' || status === 'Liquidado') partial.data_pago = now;
  if (status === 'Cancelado' || status === 'Desistido') partial.data_cancelamento = now;
  if (status === 'Em Tríduo') partial.data_intimacao = now;

  list[index] = { ...list[index], ...partial };
  return enrichTitulo(list[index]);
}
