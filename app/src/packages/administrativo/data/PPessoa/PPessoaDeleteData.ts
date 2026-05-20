import { ppessoaListRef } from '@/packages/administrativo/data/PPessoa/ppessoaInMemory';
import {
  PPESSOA_FAKE_ENDPOINTS,
  usePPessoaMockData,
} from '@/packages/administrativo/data/PPessoa/ppessoaDataConfig';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePPessoaDeleteData(id: number) {
  if (!usePPessoaMockData()) {
    const api = new API();
    return await api.send({
      method: Methods.DELETE,
      endpoint: PPESSOA_FAKE_ENDPOINTS.delete(id),
    });
  }

  await mockDbDelay(500);
  const list = ppessoaListRef.current;
  const removed = list.find((p) => p.pessoa_id === id);
  ppessoaListRef.current = list.filter((p) => p.pessoa_id !== id);

  return {
    status: 200,
    message: 'Pessoa removida com sucesso',
    data: removed ?? { pessoa_id: id },
  };
}

export const PPessoaDeleteData = withClientErrorHandler(executePPessoaDeleteData);
