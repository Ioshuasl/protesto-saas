import { mockDbDelay } from "@/packages/administrativo/shared/mockDbDelay";
import {
  PCERTIDAO_FAKE_ENDPOINTS,
  usePCertidaoMockData,
} from "@/packages/certidao/data/PCertidao/pCertidaoDataConfig";
import { pCertidaoListRef } from "@/packages/certidao/data/PCertidao/pCertidaoInMemory";
import type { PCertidaoInterface } from "@/packages/certidao/interface/PCertidao/PCertidaoInterface";
import type { PCertidaoSavePayload } from "@/packages/certidao/interface/PCertidao/PCertidaoSaveInterface";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

export async function PCertidaoSaveData(data: PCertidaoSavePayload): Promise<PCertidaoInterface> {
  const isEditing = typeof data.certidao_id === "number";

  if (!usePCertidaoMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: isEditing ? Methods.PUT : Methods.POST,
        endpoint: isEditing ? PCERTIDAO_FAKE_ENDPOINTS.update(data.certidao_id!) : PCERTIDAO_FAKE_ENDPOINTS.create,
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as PCertidaoInterface;
    }
  }

  await mockDbDelay(600);
  const list = pCertidaoListRef.current;

  if (isEditing) {
    const index = list.findIndex((item) => item.certidao_id === data.certidao_id);
    if (index === -1) throw new Error("Certidão não encontrada");
    list[index] = { ...list[index], ...data, certidao_id: data.certidao_id! };
    return list[index];
  }

  const nextId = list.length > 0 ? Math.max(...list.map((item) => item.certidao_id)) + 1 : 1;
  const created: PCertidaoInterface = {
    ...data,
    certidao_id: nextId,
  };
  list.unshift(created);
  return created;
}
