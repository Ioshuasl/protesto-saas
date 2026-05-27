'use server';

import { GEmolumentoItemShowData } from '@/packages/administrativo/data/GEmolumentoItem/GEmolumentoItemShowData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeGEmolumentoItemShowService(id: number) {
  const response = await GEmolumentoItemShowData(id);

  return response;
}

export const GEmolumentoItemShowService = withClientErrorHandler(executeGEmolumentoItemShowService);
