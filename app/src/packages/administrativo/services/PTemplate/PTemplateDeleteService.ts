'use server';

import { PTemplateDeleteData } from '@/packages/administrativo/data/PTemplate/PTemplateDeleteData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTemplateDeleteService(id: number) {
  const response = await PTemplateDeleteData(id);
  return response;
}

export const PTemplateDeleteService = withClientErrorHandler(executePTemplateDeleteService);
