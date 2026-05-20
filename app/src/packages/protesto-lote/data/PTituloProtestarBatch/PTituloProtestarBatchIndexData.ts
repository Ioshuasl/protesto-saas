import { mockDbDelay } from "@/packages/administrativo/shared/mockDbDelay";
import {
  PTITULOPROTESTARBATCH_FAKE_ENDPOINTS,
  usePTituloProtestarBatchMockData,
} from "@/packages/protesto-lote/data/PTituloProtestarBatch/pTituloProtestarBatchDataConfig";
import { pTituloProtestarBatchListRef } from "@/packages/protesto-lote/data/PTituloProtestarBatch/pTituloProtestarBatchInMemory";
import type { PTituloProtestarBatchInterface } from "@/packages/protesto-lote/interface/PTituloProtestarBatch/PTituloProtestarBatchInterface";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

export async function PTituloProtestarBatchIndexData(): Promise<PTituloProtestarBatchInterface[]> {
  if (!usePTituloProtestarBatchMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: PTITULOPROTESTARBATCH_FAKE_ENDPOINTS.index,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && Array.isArray(response?.data)) {
      return response.data as PTituloProtestarBatchInterface[];
    }
  }

  await mockDbDelay(350);
  return [...pTituloProtestarBatchListRef.current];
}
