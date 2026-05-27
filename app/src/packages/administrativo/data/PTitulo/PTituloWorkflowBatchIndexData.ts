'use server';

import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { buildPTituloIndexEndpoint } from '@/packages/administrativo/data/PTitulo/ptituloIndexQueryBuilder';
import { mapPTituloIndexItemToBatchRow } from '@/packages/administrativo/data/PTitulo/ptituloIndexItemToBatchMapper';
import type { PTituloBatchRowBase } from '@/packages/administrativo/data/PTitulo/ptituloIndexItemToBatchMapper';
import { PTITULO_ENDPOINTS } from '@/packages/administrativo/data/PTitulo/ptituloDataConfig';
import type { PTituloIndexItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexItem';
import type { PTituloIndexQuery } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export async function PTituloWorkflowBatchIndexData(
  query?: PTituloIndexQuery,
): Promise<PTituloBatchRowBase[]> {
  const api = new API();
  const apiCall = withClientErrorHandler(async () =>
    api.send({
      method: Methods.GET,
      endpoint: buildPTituloIndexEndpoint(PTITULO_ENDPOINTS.index, query),
    }),
  );
  const response = await apiCall();

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && Array.isArray(response?.data)) {
    return (response.data as PTituloIndexItem[]).map(mapPTituloIndexItemToBatchRow);
  }

  return [];
}

/** Mantido para compatibilidade com mocks legados em desenvolvimento local. */
export async function PTituloWorkflowBatchIndexDataWithMockFallback(
  query: PTituloIndexQuery | undefined,
  mockRows: PTituloBatchRowBase[],
  useMock: boolean,
): Promise<PTituloBatchRowBase[]> {
  if (!useMock) {
    return PTituloWorkflowBatchIndexData(query);
  }

  await mockDbDelay(350);
  return [...mockRows];
}
