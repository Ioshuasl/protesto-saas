import { pocorrenciasListRef } from '@/packages/administrativo/data/POcorrencias/pocorrenciasInMemory';
import {
  POCORRENCIAS_FAKE_ENDPOINTS,
  usePOcorrenciasMockData,
} from '@/packages/administrativo/data/POcorrencias/pocorrenciasDataConfig';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePOcorrenciasDeleteData(id: number) {
  if (!usePOcorrenciasMockData()) {
    const api = new API();
    return await api.send({
      method: Methods.DELETE,
      endpoint: POCORRENCIAS_FAKE_ENDPOINTS.delete(id),
    });
  }

  await mockDbDelay(500);
  const list = pocorrenciasListRef.current;
  const removed = list.find((row) => row.ocorrencias_id === id);
  pocorrenciasListRef.current = list.filter((row) => row.ocorrencias_id !== id);

  return {
    status: 200,
    message: 'Ocorrência removida com sucesso',
    data: removed ?? { ocorrencias_id: id },
  };
}

export const POcorrenciasDeleteData = withClientErrorHandler(executePOcorrenciasDeleteData);
