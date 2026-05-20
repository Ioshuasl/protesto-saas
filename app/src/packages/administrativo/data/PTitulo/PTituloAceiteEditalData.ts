import { enrichTitulo } from '@/packages/administrativo/data/PTitulo/ptituloEnrich';
import { ptituloListRef } from '@/packages/administrativo/data/PTitulo/ptituloInMemory';
import { pPessoaVinculoListRef } from '@/packages/administrativo/data/PTitulo/ptituloPessoasVinculoInMemory';
import {
  PTITULO_FAKE_ENDPOINTS,
  isPTituloMockDataEnabled,
} from '@/packages/administrativo/data/PTitulo/ptituloDataConfig';
import type { PTituloAceiteEditalInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloAceiteEditalInterface';
import type { PTituloInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloInterface';
import type { TituloListItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import { parseLocalIsoDateOnly } from '@/shared/actions/dateTime/LocalDateOnly';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export async function PTituloAceiteEditalData(
  id: number,
  payload: PTituloAceiteEditalInterface,
): Promise<TituloListItem> {
  if (!isPTituloMockDataEnabled()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.PUT,
        endpoint: PTITULO_FAKE_ENDPOINTS.aceiteEdital(id),
        body: payload,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return enrichTitulo(response.data as PTituloInterface);
    }
  }

  console.log('[PTituloAceiteEditalData] fluxo hooks -> service -> data executado (mock)');

  const current = ptituloListRef.current.find((item) => item.titulo_id === id);
  if (!current) throw new Error('Título não encontrado');

  payload.devedores.forEach((devedorPayload) => {
    const idx = pPessoaVinculoListRef.current.findIndex(
      (item) =>
        item.pessoa_vinculo_id === devedorPayload.pessoa_vinculo_id && Number(item.titulo_id) === Number(id),
    );
    if (idx === -1) return;
    const prevVinculo = pPessoaVinculoListRef.current[idx]!;
    const parsedDate = parseLocalIsoDateOnly(devedorPayload.devedor_data_aceite);
    pPessoaVinculoListRef.current[idx] = {
      ...prevVinculo,
      devedor_tipo_aceite: devedorPayload.devedor_tipo_aceite,
      devedor_data_aceite: parsedDate ?? prevVinculo.devedor_data_aceite,
    };
  });

  const next: PTituloInterface = {
    ...current,
    data_aceite: parseLocalIsoDateOnly(payload.devedores[0]?.devedor_data_aceite) ?? current.data_aceite,
    tipo_aceite: payload.devedores[0]?.devedor_tipo_aceite ?? current.tipo_aceite,
    situacao_aceite: current.situacao_aceite || 'Intimado',
  };

  const tituloIdx = ptituloListRef.current.findIndex((item) => item.titulo_id === id);
  if (tituloIdx >= 0) ptituloListRef.current[tituloIdx] = next;

  return enrichTitulo(next);
}
