import { gferiadoListRef } from "@/packages/administrativo/data/GFeriado/gferiadoInMemory";
import { GFERIADO_FAKE_ENDPOINTS, useGFeriadoMockData } from "@/packages/administrativo/data/GFeriado/gferiadoDataConfig";
import { GFeriadoInterface } from "@/packages/administrativo/interfaces/GFeriado/GFeriadoInterface";
import { mockDbDelay } from "@/packages/administrativo/shared/mockDbDelay";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

async function executeGFeriadoDeleteData(data: GFeriadoInterface) {
  const id = data.feriado_id;
  if (!useGFeriadoMockData()) {
    const api = new API();
    return await api.send({
      method: Methods.DELETE,
      endpoint: GFERIADO_FAKE_ENDPOINTS.delete(id),
    });
  }

  await mockDbDelay(500);
  gferiadoListRef.current = gferiadoListRef.current.filter((row) => row.feriado_id !== id);

  return {
    status: 200,
    message: "Feriado removido com sucesso",
    data,
  };
}

export const GFeriadoDeleteData = withClientErrorHandler(executeGFeriadoDeleteData);
