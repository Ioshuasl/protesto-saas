import { PCERTIDAO_ENDPOINTS } from "@/packages/certidao/data/PCertidao/pCertidaoDataConfig";
import type { PCertidaoInterface } from "@/packages/certidao/interface/PCertidao/PCertidaoInterface";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

export async function PCertidaoShowData(certidaoId: number): Promise<PCertidaoInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: PCERTIDAO_ENDPOINTS.show(certidaoId),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PCertidaoInterface;
  }

  throw new Error(response?.message || "Certidão não encontrada");
}
