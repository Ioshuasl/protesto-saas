import { PLAYOUT_FAKE_ENDPOINTS, usePLayoutMockData } from "@/packages/administrativo/data/PLayout/playoutDataConfig";
import { playoutListRef } from "@/packages/administrativo/data/PLayout/playoutInMemory";
import type { PLayoutInterface } from "@/packages/administrativo/interfaces/PLayout/PLayoutInterface";
import { mockDbDelay } from "@/packages/administrativo/shared/mockDbDelay";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

export async function PLayoutIndexData(): Promise<PLayoutInterface[]> {
  if (!usePLayoutMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: PLAYOUT_FAKE_ENDPOINTS.index,
      }),
    );

    const response = await apiCall();
    if (
      Number(response?.status) >= 200 &&
      Number(response?.status) < 300 &&
      Array.isArray(response?.data)
    ) {
      return response.data as PLayoutInterface[];
    }
  }

  await mockDbDelay(500);
  return [...playoutListRef.current];
}
