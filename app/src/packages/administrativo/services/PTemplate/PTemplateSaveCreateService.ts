'use server';

import { PTemplateSaveCreateData } from '@/packages/administrativo/data/PTemplate/PTemplateSaveData';
import type { PTemplateInterface } from '@/packages/administrativo/interfaces/PTemplate/PTemplateInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTemplateSaveCreateService(data: Omit<PTemplateInterface, 'template_id'>) {
  const response = await PTemplateSaveCreateData(data);
  return response;
}

export const PTemplateSaveCreateService = withClientErrorHandler(
  executePTemplateSaveCreateService,
);
