import { PCERTIDAO_ENDPOINTS } from "@/packages/certidao/data/PCertidao/pCertidaoDataConfig";
import type { PCertidaoInterface } from "@/packages/certidao/interface/PCertidao/PCertidaoInterface";
import type { PCertidaoSavePayload } from "@/packages/certidao/interface/PCertidao/PCertidaoSaveInterface";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

export async function PCertidaoSaveData(data: PCertidaoSavePayload): Promise<PCertidaoInterface> {
  const isEditing = typeof data.certidao_id === "number";
  const api = new API();
  const response = await api.send({
    method: isEditing ? Methods.PUT : Methods.POST,
    endpoint: isEditing ? PCERTIDAO_ENDPOINTS.update(data.certidao_id!) : PCERTIDAO_ENDPOINTS.create,
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PCertidaoInterface;
  }

  throw new Error(response?.message || "Não foi possível salvar a certidão");
}
