'use server';

import { PAndamentoDeleteData } from '@/packages/administrativo/data/PAndamento/PAndamentoDeleteData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePAndamentoDeleteService(id: number) {
  return await PAndamentoDeleteData(id);
}

export const PAndamentoDeleteService = withClientErrorHandler(executePAndamentoDeleteService);
