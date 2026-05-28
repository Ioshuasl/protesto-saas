'use server';

import { PTemplateOpenEditorData } from '@/packages/administrativo/data/PTemplate/PTemplateOpenEditorData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTemplateOpenEditorService(
  templateId: number,
  mode: 'edit' | 'view' = 'edit',
) {
  return await PTemplateOpenEditorData(templateId, mode);
}

export const PTemplateOpenEditorService = withClientErrorHandler(executePTemplateOpenEditorService);

