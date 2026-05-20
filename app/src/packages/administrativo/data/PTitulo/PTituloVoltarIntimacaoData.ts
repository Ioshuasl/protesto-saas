import { enrichTitulo } from '@/packages/administrativo/data/PTitulo/ptituloEnrich';
import { ptituloListRef } from '@/packages/administrativo/data/PTitulo/ptituloInMemory';
import {
  PTITULO_FAKE_ENDPOINTS,
  isPTituloMockDataEnabled,
} from '@/packages/administrativo/data/PTitulo/ptituloDataConfig';
import type { PTituloInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloInterface';
import type { TituloListItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import type { PTituloVoltarIntimacaoInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloVoltarIntimacaoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export async function PTituloVoltarIntimacaoData(
  id: number,
  payload: PTituloVoltarIntimacaoInterface,
): Promise<TituloListItem> {
  if (!isPTituloMockDataEnabled()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.PUT,
        endpoint: PTITULO_FAKE_ENDPOINTS.voltarIntimacao(id),
        body: payload,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return enrichTitulo(response.data as PTituloInterface);
    }
  }

  console.log('[PTituloVoltarIntimacaoData] fluxo hooks -> service -> data executado (mock)');

  const idx = ptituloListRef.current.findIndex((item) => item.titulo_id === id);
  if (idx === -1) throw new Error('Título não encontrado');

  const prev = ptituloListRef.current[idx]!;
  const next: PTituloInterface = {
    ...prev,
    ocorrencia_id: payload.ocorrencia_id,
    data_protesto: undefined,
    livro_id_protesto: undefined,
    folha_protesto: undefined,
    situacao_aceite: 'Intimado',
  };

  ptituloListRef.current[idx] = next;

  return enrichTitulo(next);
}
