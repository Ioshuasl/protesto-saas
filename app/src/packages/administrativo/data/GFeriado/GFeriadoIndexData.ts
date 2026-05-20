import { gferiadoListRef } from "@/packages/administrativo/data/GFeriado/gferiadoInMemory";
import { GFERIADO_FAKE_ENDPOINTS, useGFeriadoMockData } from "@/packages/administrativo/data/GFeriado/gferiadoDataConfig";
import type { GFeriadoInterface } from "@/packages/administrativo/interfaces/GFeriado/GFeriadoInterface";
import { mockDbDelay } from "@/packages/administrativo/shared/mockDbDelay";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

export async function GFeriadoIndexData(): Promise<GFeriadoInterface[]> {
  if (!useGFeriadoMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: GFERIADO_FAKE_ENDPOINTS.index,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && Array.isArray(response?.data)) {
      return response.data as GFeriadoInterface[];
    }
  }

  await mockDbDelay(500);
  return [...gferiadoListRef.current];
}
