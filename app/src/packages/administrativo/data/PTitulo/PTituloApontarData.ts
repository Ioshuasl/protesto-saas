import { enrichTitulo } from '@/packages/administrativo/data/PTitulo/ptituloEnrich';
import { ptituloListRef } from '@/packages/administrativo/data/PTitulo/ptituloInMemory';
import {
  PTITULO_FAKE_ENDPOINTS,
  isPTituloMockDataEnabled,
} from '@/packages/administrativo/data/PTitulo/ptituloDataConfig';
import type { PTituloApontarInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloApontarInterface';
import type { PTituloInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloInterface';
import type { TituloListItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import { parseLocalIsoDateOnly } from '@/shared/actions/dateTime/LocalDateOnly';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export async function PTituloApontarData(id: number, payload: PTituloApontarInterface): Promise<TituloListItem> {
  if (!isPTituloMockDataEnabled()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.PUT,
        endpoint: PTITULO_FAKE_ENDPOINTS.apontarTitulo(id),
        body: payload,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return enrichTitulo(response.data as PTituloInterface);
    }
  }

  console.log('[PTituloApontarData] fluxo hooks -> service -> data executado (mock)');

  const idx = ptituloListRef.current.findIndex((item) => item.titulo_id === id);
  if (idx === -1) throw new Error('Título não encontrado');

  const prev = ptituloListRef.current[idx]!;
  const payloadDate = parseLocalIsoDateOnly(payload.data_apontamento);
  const next: PTituloInterface = {
    ...prev,
    numero_apontamento: payload.numero_apontamento ?? prev.numero_apontamento ?? Date.now(),
    motivo_apontamento_id: payload.motivo_apontamento_id,
    ocorrencia_id: payload.ocorrencia_id,
    data_apontamento:
      payloadDate ?? prev.data_apontamento ?? new Date(),
    situacao_aceite: 'Apontado',
  };

  ptituloListRef.current[idx] = next;

  return enrichTitulo(next);
}
