import { pespecieListRef } from '@/packages/administrativo/data/PEspecie/pespecieInMemory';
import {
  PESPECIE_FAKE_ENDPOINTS,
  usePEspecieMockData,
} from '@/packages/administrativo/data/PEspecie/pespecieDataConfig';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePEspecieDeleteData(id: number) {
  if (!usePEspecieMockData()) {
    const api = new API();
    return await api.send({
      method: Methods.DELETE,
      endpoint: PESPECIE_FAKE_ENDPOINTS.delete(id),
    });
  }

  await mockDbDelay(500);
  const list = pespecieListRef.current;
  const removed = list.find((row) => row.especie_id === id);
  pespecieListRef.current = list.filter((row) => row.especie_id !== id);

  return {
    status: 200,
    message: 'Espécie removida com sucesso',
    data: removed ?? { especie_id: id },
  };
}

export const PEspecieDeleteData = withClientErrorHandler(executePEspecieDeleteData);
