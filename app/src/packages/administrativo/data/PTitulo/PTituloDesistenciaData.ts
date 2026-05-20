import { enrichTitulo } from '@/packages/administrativo/data/PTitulo/ptituloEnrich';
import { ptituloListRef } from '@/packages/administrativo/data/PTitulo/ptituloInMemory';
import {
  PTITULO_FAKE_ENDPOINTS,
  isPTituloMockDataEnabled,
} from '@/packages/administrativo/data/PTitulo/ptituloDataConfig';
import type { PTituloDesistenciaFormInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloDesistenciaFormInterface';
import type { PTituloInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloInterface';
import type { TituloListItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import { parseLocalIsoDateOnly } from '@/shared/actions/dateTime/LocalDateOnly';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export async function PTituloDesistenciaData(
  id: number,
  payload?: PTituloDesistenciaFormInterface,
): Promise<TituloListItem> {
  if (!isPTituloMockDataEnabled()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.PUT,
        endpoint: PTITULO_FAKE_ENDPOINTS.desistirTitulo(id),
        ...(payload ? { body: payload } : {}),
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return enrichTitulo(response.data as PTituloInterface);
    }
  }

  console.log('[PTituloDesistenciaData] fluxo hooks -> service -> data executado (mock)');

  const idx = ptituloListRef.current.findIndex((item) => item.titulo_id === id);
  if (idx === -1) throw new Error('Título não encontrado');
  const current = ptituloListRef.current[idx]!;

  if (!payload) {
    return enrichTitulo(current);
  }

  const payloadDate = parseLocalIsoDateOnly(payload.data_desistencia);
  const next: PTituloInterface = {
    ...current,
    data_desistencia: payloadDate ?? current.data_desistencia,
    ocorrencia_id: payload.ocorrencia_id,
    motivo_cancelamento: payload.motivo_cancelamento_id,
    servico_gratuito: payload.servico_gratuito,
    situacao_aceite: 'Desistido',
  };

  ptituloListRef.current[idx] = next;

  return enrichTitulo(next);
}
