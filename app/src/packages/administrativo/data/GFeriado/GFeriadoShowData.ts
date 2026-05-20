import { gferiadoListRef } from "@/packages/administrativo/data/GFeriado/gferiadoInMemory";
import { GFERIADO_FAKE_ENDPOINTS, useGFeriadoMockData } from "@/packages/administrativo/data/GFeriado/gferiadoDataConfig";
import { mockDbDelay } from "@/packages/administrativo/shared/mockDbDelay";
import type { GFeriadoInterface } from "@/packages/administrativo/interfaces/GFeriado/GFeriadoInterface";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

export async function GFeriadoShowData(id: number): Promise<GFeriadoInterface | undefined> {
  if (!useGFeriadoMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: GFERIADO_FAKE_ENDPOINTS.show(id),
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as GFeriadoInterface;
    }
  }

  await mockDbDelay(300);
  return gferiadoListRef.current.find((row) => row.feriado_id === id);
}
