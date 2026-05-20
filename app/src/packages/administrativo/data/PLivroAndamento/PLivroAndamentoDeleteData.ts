import { plivroAndamentoListRef } from '@/packages/administrativo/data/PLivroAndamento/plivroAndamentoInMemory';
import {
  PLIVRO_ANDAMENTO_FAKE_ENDPOINTS,
  usePLivroAndamentoMockData,
} from '@/packages/administrativo/data/PLivroAndamento/plivroAndamentoDataConfig';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePLivroAndamentoDeleteData(id: number) {
  if (!usePLivroAndamentoMockData()) {
    const api = new API();
    return await api.send({
      method: Methods.DELETE,
      endpoint: PLIVRO_ANDAMENTO_FAKE_ENDPOINTS.delete(id),
    });
  }

  await mockDbDelay(500);
  const list = plivroAndamentoListRef.current;
  const removed = list.find((row) => row.livro_andamento_id === id);
  plivroAndamentoListRef.current = list.filter((row) => row.livro_andamento_id !== id);

  return {
    status: 200,
    message: 'Livro em andamento removido com sucesso',
    data: removed ?? { livro_andamento_id: id },
  };
}

export const PLivroAndamentoDeleteData = withClientErrorHandler(executePLivroAndamentoDeleteData);
