import { gferiadoListRef } from "@/packages/administrativo/data/GFeriado/gferiadoInMemory";
import { GFERIADO_FAKE_ENDPOINTS, useGFeriadoMockData } from "@/packages/administrativo/data/GFeriado/gferiadoDataConfig";
import { mockDbDelay } from "@/packages/administrativo/shared/mockDbDelay";
import type { GFeriadoInterface } from "@/packages/administrativo/interfaces/GFeriado/GFeriadoInterface";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

export async function GFeriadoSaveCreateData(
  data: Omit<GFeriadoInterface, "feriado_id">,
): Promise<GFeriadoInterface> {
  if (!useGFeriadoMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.POST,
        endpoint: GFERIADO_FAKE_ENDPOINTS.create,
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as GFeriadoInterface;
    }
  }

  await mockDbDelay(600);
  const list = gferiadoListRef.current;
  const newId = list.length > 0 ? Math.max(...list.map((row) => row.feriado_id)) + 1 : 1;
  const created = { ...data, feriado_id: newId } as GFeriadoInterface;
  list.push(created);
  return created;
}

export async function GFeriadoSaveUpdateData(
  id: number,
  data: Partial<GFeriadoInterface>,
): Promise<GFeriadoInterface> {
  if (!useGFeriadoMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.PUT,
        endpoint: GFERIADO_FAKE_ENDPOINTS.update(id),
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as GFeriadoInterface;
    }
  }

  await mockDbDelay(600);
  const list = gferiadoListRef.current;
  const index = list.findIndex((row) => row.feriado_id === id);
  if (index === -1) throw new Error("Feriado não encontrado");
  list[index] = { ...list[index], ...data };
  return list[index];
}
