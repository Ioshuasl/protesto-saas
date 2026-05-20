import { plivroNaturezaListRef } from '@/packages/administrativo/data/PLivroNatureza/plivroNaturezaInMemory';
import {
  PLIVRO_NATUREZA_FAKE_ENDPOINTS,
  usePLivroNaturezaMockData,
} from '@/packages/administrativo/data/PLivroNatureza/plivroNaturezaDataConfig';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePLivroNaturezaDeleteData(id: number) {
  if (!usePLivroNaturezaMockData()) {
    const api = new API();
    return await api.send({
      method: Methods.DELETE,
      endpoint: PLIVRO_NATUREZA_FAKE_ENDPOINTS.delete(id),
    });
  }

  await mockDbDelay(500);
  const list = plivroNaturezaListRef.current;
  const removed = list.find((row) => row.livro_natureza_id === id);
  plivroNaturezaListRef.current = list.filter((row) => row.livro_natureza_id !== id);

  return {
    status: 200,
    message: 'Natureza de livro removida com sucesso',
    data: removed ?? { livro_natureza_id: id },
  };
}

export const PLivroNaturezaDeleteData = withClientErrorHandler(executePLivroNaturezaDeleteData);
