'use server';

import { GEmolumentoShowData } from '@/packages/administrativo/data/GEmolumento/GEmolumentoShowData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGEmolumentoShowService(id: number) {
  const response = await GEmolumentoShowData(id);

  return response;
}

export const GEmolumentoShowService = withClientErrorHandler(executeGEmolumentoShowService);
