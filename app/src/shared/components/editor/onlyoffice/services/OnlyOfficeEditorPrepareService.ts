'use server';

import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import { OnlyOfficeEditorPrepareData } from '@/shared/components/editor/onlyoffice/data/OnlyOfficeEditorPrepareData';

export default async function executeOnlyOfficeEditorPrepareService() {
  const response = await OnlyOfficeEditorPrepareData();
  return response;
}

export const OnlyOfficeEditorPrepareService = withClientErrorHandler(
  executeOnlyOfficeEditorPrepareService,
);
