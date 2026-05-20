import { enrichTitulo } from '@/packages/administrativo/data/PTitulo/ptituloEnrich';
import { ptituloListRef } from '@/packages/administrativo/data/PTitulo/ptituloInMemory';
import {
  PTITULO_FAKE_ENDPOINTS,
  isPTituloMockDataEnabled,
} from '@/packages/administrativo/data/PTitulo/ptituloDataConfig';
import type { PTituloInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloInterface';
import type { PTituloRetiradaFormInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloRetiradaFormInterface';
import type { TituloListItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

/** Mock: `data_retirada` não existe em `PTituloInterface`; persistimos ocorrência e motivo e atualizamos situação. */
export async function PTituloRetiradaData(id: number, payload: PTituloRetiradaFormInterface): Promise<TituloListItem> {
  if (!isPTituloMockDataEnabled()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.PUT,
        endpoint: PTITULO_FAKE_ENDPOINTS.retiradaTitulo(id),
        body: payload,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return enrichTitulo(response.data as PTituloInterface);
    }
  }

  console.log('[PTituloRetiradaData] fluxo hooks -> service -> data executado (mock)');

  const idx = ptituloListRef.current.findIndex((item) => item.titulo_id === id);
  if (idx === -1) throw new Error('Título não encontrado');
  const prev = ptituloListRef.current[idx]!;

  const next: PTituloInterface = {
    ...prev,
    ocorrencia_id: payload.ocorrencia_id,
    motivo_cancelamento: payload.motivo_cancelamento_id,
    servico_gratuito: payload.servico_gratuito,
    situacao_aceite: 'Retirado',
  };

  ptituloListRef.current[idx] = next;

  return enrichTitulo(next);
}
