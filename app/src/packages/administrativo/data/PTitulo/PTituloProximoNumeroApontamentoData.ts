import { ptituloListRef } from '@/packages/administrativo/data/PTitulo/ptituloInMemory';
import {
  PTITULO_FAKE_ENDPOINTS,
  isPTituloMockDataEnabled,
} from '@/packages/administrativo/data/PTitulo/ptituloDataConfig';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

function getMaxNumeroApontamentoFromMock(): number {
  return ptituloListRef.current.reduce((acc, item) => {
    const numero = typeof item.numero_apontamento === 'number' ? item.numero_apontamento : 0;
    return Math.max(acc, numero);
  }, 0);
}

export async function PTituloProximoNumeroApontamentoData(): Promise<number> {
  if (!isPTituloMockDataEnabled()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: PTITULO_FAKE_ENDPOINTS.proximoNumeroApontamento(),
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300) {
      const numero = Number((response?.data as { proximo_numero_apontamento?: unknown })?.proximo_numero_apontamento);
      if (!Number.isNaN(numero) && numero > 0) return numero;
    }
  }

  console.log('[PTituloProximoNumeroApontamentoData] fluxo hooks -> service -> data executado (mock)');
  return getMaxNumeroApontamentoFromMock() + 1;
}
