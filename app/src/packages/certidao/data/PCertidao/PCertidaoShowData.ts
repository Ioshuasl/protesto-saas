import { mockDbDelay } from "@/packages/administrativo/shared/mockDbDelay";
import {
  PCERTIDAO_FAKE_ENDPOINTS,
  usePCertidaoMockData,
} from "@/packages/certidao/data/PCertidao/pCertidaoDataConfig";
import { pCertidaoListRef } from "@/packages/certidao/data/PCertidao/pCertidaoInMemory";
import type { PCertidaoInterface } from "@/packages/certidao/interface/PCertidao/PCertidaoInterface";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

export async function PCertidaoShowData(certidaoId: number): Promise<PCertidaoInterface> {
  if (!usePCertidaoMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: PCERTIDAO_FAKE_ENDPOINTS.show(certidaoId),
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as PCertidaoInterface;
    }
  }

  await mockDbDelay(300);
  const certidao = pCertidaoListRef.current.find((item) => item.certidao_id === certidaoId);
  if (!certidao) throw new Error("Certidão não encontrada");
  return certidao;
}
