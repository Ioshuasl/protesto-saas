import { pmotivosListRef } from '@/packages/administrativo/data/PMotivos/pmotivosInMemory';
import {
  PMOTIVOS_FAKE_ENDPOINTS,
  usePMotivosMockData,
} from '@/packages/administrativo/data/PMotivos/pmotivosDataConfig';
import type { PMotivosInterface } from '@/packages/administrativo/interfaces/PMotivos/PMotivosInterface';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

export async function PMotivosShowData(id: number): Promise<PMotivosInterface | undefined> {
  if (!usePMotivosMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: PMOTIVOS_FAKE_ENDPOINTS.show(id),
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as PMotivosInterface;
    }
  }

  await mockDbDelay(300);
  return pmotivosListRef.current.find((row) => row.motivos_id === id);
}
