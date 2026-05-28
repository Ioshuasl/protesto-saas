'use server';

import { PTEMPLATE_ENDPOINTS } from '@/packages/administrativo/data/PTemplate/pTemplateDataConfig';
import type { PTemplateInterface } from '@/packages/administrativo/interfaces/PTemplate/PTemplateInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executePTemplateSaveCreateData(
  data: Omit<PTemplateInterface, 'template_id'>,
): Promise<PTemplateInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.POST,
    endpoint: PTEMPLATE_ENDPOINTS.create,
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PTemplateInterface;
  }

  throw new Error(response?.message ?? 'Erro ao cadastrar template');
}

async function executePTemplateSaveUpdateData(
  id: number,
  data: Partial<PTemplateInterface>,
): Promise<PTemplateInterface> {
  const api = new API();
  const response = await api.send({
    method: Methods.PUT,
    endpoint: PTEMPLATE_ENDPOINTS.update(id),
    body: data,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PTemplateInterface;
  }

  throw new Error(response?.message ?? 'Erro ao atualizar template');
}

export const PTemplateSaveCreateData = withClientErrorHandler(executePTemplateSaveCreateData);
export const PTemplateSaveUpdateData = withClientErrorHandler(executePTemplateSaveUpdateData);
