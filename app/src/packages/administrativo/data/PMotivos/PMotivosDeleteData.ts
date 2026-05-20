import { pmotivosListRef } from '@/packages/administrativo/data/PMotivos/pmotivosInMemory';
import {
  PMOTIVOS_FAKE_ENDPOINTS,
  usePMotivosMockData,
} from '@/packages/administrativo/data/PMotivos/pmotivosDataConfig';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePMotivosDeleteData(id: number) {
  if (!usePMotivosMockData()) {
    const api = new API();
    return await api.send({
      method: Methods.DELETE,
      endpoint: PMOTIVOS_FAKE_ENDPOINTS.delete(id),
    });
  }

  await mockDbDelay(500);
  const list = pmotivosListRef.current;
  const removed = list.find((row) => row.motivos_id === id);
  pmotivosListRef.current = list.filter((row) => row.motivos_id !== id);

  return {
    status: 200,
    message: 'Motivo de apontamento removido com sucesso',
    data: removed ?? { motivos_id: id },
  };
}

export const PMotivosDeleteData = withClientErrorHandler(executePMotivosDeleteData);
