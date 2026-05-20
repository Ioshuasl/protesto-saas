import { mockDbDelay } from "@/packages/administrativo/shared/mockDbDelay";
import { pArquivoTituloListRef } from "@/packages/cra/data/PTituloArquivo/pArquivoTituloInMemory";
import {
  PTITULOARQUIVO_FAKE_ENDPOINTS,
  usePTituloArquivoMockData,
} from "@/packages/cra/data/PTituloArquivo/pTituloArquivoDataConfig";
import type { PArquivoTituloInterface } from "@/packages/cra/interface/PArquivoTitulo/PArquivoTituloInterface";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

export async function PTituloArquivoShowData(): Promise<PArquivoTituloInterface[]> {
  if (!usePTituloArquivoMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: PTITULOARQUIVO_FAKE_ENDPOINTS.index,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && Array.isArray(response?.data)) {
      return response.data as PArquivoTituloInterface[];
    }
  }

  await mockDbDelay(300);
  return [...pArquivoTituloListRef.current];
}
