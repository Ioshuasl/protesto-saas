import { pmotivosCancelamentoListRef } from '@/packages/administrativo/data/PMotivosCancelamento/pmotivosCancelamentoInMemory';
import {
  PMOTIVOS_CANCELAMENTO_FAKE_ENDPOINTS,
  usePMotivosCancelamentoMockData,
} from '@/packages/administrativo/data/PMotivosCancelamento/pmotivosCancelamentoDataConfig';
import type { PMotivosCancelamentoInterface } from '@/packages/administrativo/interfaces/PMotivosCancelamento/PMotivosCancelamentoInterface';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export async function PMotivosCancelamentoShowData(
  id: number,
): Promise<PMotivosCancelamentoInterface | undefined> {
  if (!usePMotivosCancelamentoMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: PMOTIVOS_CANCELAMENTO_FAKE_ENDPOINTS.show(id),
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as PMotivosCancelamentoInterface;
    }
  }

  await mockDbDelay(300);
  return pmotivosCancelamentoListRef.current.find((row) => row.motivos_cancelamento_id === id);
}
