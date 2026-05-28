'use server';

import { PTemplateIndexData } from '@/packages/administrativo/data/PTemplate/PTemplateIndexData';
import type { PTemplateIndexQuery } from '@/packages/administrativo/interfaces/PTemplate/PTemplateIndexQuery';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTemplateIndexService(query?: PTemplateIndexQuery) {
  return await PTemplateIndexData(query);
}

export const PTemplateIndexService = withClientErrorHandler(executePTemplateIndexService);
