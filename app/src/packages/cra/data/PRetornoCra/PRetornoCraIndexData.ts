import { ptituloListRef } from "@/packages/administrativo/data/PTitulo/ptituloInMemory";
import type { PTituloInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloInterface";
import { mockDbDelay } from "@/packages/administrativo/shared/mockDbDelay";
import { PRETORNOCRA_FAKE_ENDPOINTS, usePRetornoCraMockData } from "@/packages/cra/data/PRetornoCra/pRetornoCraDataConfig";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

export async function PRetornoCraIndexData(): Promise<PTituloInterface[]> {
  if (!usePRetornoCraMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: PRETORNOCRA_FAKE_ENDPOINTS.index,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && Array.isArray(response?.data)) {
      return response.data as PTituloInterface[];
    }
  }

  await mockDbDelay(400);
  return [...ptituloListRef.current];
}
