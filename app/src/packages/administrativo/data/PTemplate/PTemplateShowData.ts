'use server';

import { PTEMPLATE_ENDPOINTS } from '@/packages/administrativo/data/PTemplate/pTemplateDataConfig';
import type { PTemplateInterface } from '@/packages/administrativo/interfaces/PTemplate/PTemplateInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePTemplateShowData(id: number): Promise<PTemplateInterface | undefined> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: PTEMPLATE_ENDPOINTS.show(id),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PTemplateInterface;
  }

  return undefined;
}

export const PTemplateShowData = withClientErrorHandler(executePTemplateShowData);
