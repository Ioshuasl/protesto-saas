import { mockDbDelay } from "@/packages/administrativo/shared/mockDbDelay";
import {
  PTITULOINTIMACAOBATCH_FAKE_ENDPOINTS,
  usePTituloIntimacaoBatchMockData,
} from "@/packages/intimacao-lote/data/PTituloIntimacaoBatch/pTituloIntimacaoBatchDataConfig";
import { pTituloIntimacaoBatchListRef } from "@/packages/intimacao-lote/data/PTituloIntimacaoBatch/pTituloIntimacaoBatchInMemory";
import type { PTituloIntimacaoBatchInterface } from "@/packages/intimacao-lote/interface/PTituloIntimacaoBatch/PTituloIntimacaoBatchInterface";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

export async function PTituloIntimacaoBatchIndexData(): Promise<PTituloIntimacaoBatchInterface[]> {
  if (!usePTituloIntimacaoBatchMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: PTITULOINTIMACAOBATCH_FAKE_ENDPOINTS.index,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && Array.isArray(response?.data)) {
      return response.data as PTituloIntimacaoBatchInterface[];
    }
  }

  await mockDbDelay(350);
  return [...pTituloIntimacaoBatchListRef.current];
}
