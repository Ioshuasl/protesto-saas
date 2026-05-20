import { mockDbDelay } from "@/packages/administrativo/shared/mockDbDelay";
import {
  PTITULOAPONTAMENTOBATCH_FAKE_ENDPOINTS,
  usePTituloApontamentoBatchMockData,
} from "@/packages/apontamento-lote/data/PTituloApontamentoBatch/pTituloApontamentoBatchDataConfig";
import { pTituloApontamentoBatchListRef } from "@/packages/apontamento-lote/data/PTituloApontamentoBatch/pTituloApontamentoBatchInMemory";
import type { PTituloApontamentoBatchInterface } from "@/packages/apontamento-lote/interface/PTituloApontamentoBatch/PTituloApontamentoBatchInterface";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

export async function PTituloApontamentoBatchIndexData(): Promise<PTituloApontamentoBatchInterface[]> {
  if (!usePTituloApontamentoBatchMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: PTITULOAPONTAMENTOBATCH_FAKE_ENDPOINTS.index,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && Array.isArray(response?.data)) {
      return response.data as PTituloApontamentoBatchInterface[];
    }
  }

  await mockDbDelay(350);
  return [...pTituloApontamentoBatchListRef.current];
}
