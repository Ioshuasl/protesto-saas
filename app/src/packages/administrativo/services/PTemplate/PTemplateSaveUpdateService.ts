'use server';

import { PTemplateSaveUpdateData } from '@/packages/administrativo/data/PTemplate/PTemplateSaveData';
import type { PTemplateInterface } from '@/packages/administrativo/interfaces/PTemplate/PTemplateInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTemplateSaveUpdateService(id: number, data: Partial<PTemplateInterface>) {
  const response = await PTemplateSaveUpdateData(id, data);
  return response;
}

export const PTemplateSaveUpdateService = withClientErrorHandler(
  executePTemplateSaveUpdateService,
);
