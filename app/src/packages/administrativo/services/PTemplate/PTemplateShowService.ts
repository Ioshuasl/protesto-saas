'use server';

import { PTemplateShowData } from '@/packages/administrativo/data/PTemplate/PTemplateShowData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTemplateShowService(id: number) {
  const response = await PTemplateShowData(id);
  return response;
}

export const PTemplateShowService = withClientErrorHandler(executePTemplateShowService);
