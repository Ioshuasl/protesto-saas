'use server';

import { PTEMPLATE_ENDPOINTS } from '@/packages/administrativo/data/PTemplate/pTemplateDataConfig';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePTemplateDeleteData(id: number) {
  const api = new API();
  return await api.send({
    method: Methods.DELETE,
    endpoint: PTEMPLATE_ENDPOINTS.delete(id),
  });
}

export const PTemplateDeleteData = withClientErrorHandler(executePTemplateDeleteData);
