import { pmotivosCancelamentoListRef } from '@/packages/administrativo/data/PMotivosCancelamento/pmotivosCancelamentoInMemory';
import {
  PMOTIVOS_CANCELAMENTO_FAKE_ENDPOINTS,
  usePMotivosCancelamentoMockData,
} from '@/packages/administrativo/data/PMotivosCancelamento/pmotivosCancelamentoDataConfig';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePMotivosCancelamentoDeleteData(id: number) {
  if (!usePMotivosCancelamentoMockData()) {
    const api = new API();
    return await api.send({
      method: Methods.DELETE,
      endpoint: PMOTIVOS_CANCELAMENTO_FAKE_ENDPOINTS.delete(id),
    });
  }

  await mockDbDelay(500);
  const list = pmotivosCancelamentoListRef.current;
  const removed = list.find((row) => row.motivos_cancelamento_id === id);
  pmotivosCancelamentoListRef.current = list.filter((row) => row.motivos_cancelamento_id !== id);

  return {
    status: 200,
    message: 'Motivo de cancelamento removido com sucesso',
    data: removed ?? { motivos_cancelamento_id: id },
  };
}

export const PMotivosCancelamentoDeleteData = withClientErrorHandler(
  executePMotivosCancelamentoDeleteData,
);
