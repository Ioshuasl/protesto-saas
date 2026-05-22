'use server';

import { PAndamentoShowData } from '@/packages/administrativo/data/PAndamento/PAndamentoShowData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePAndamentoShowService(id: number) {
  return await PAndamentoShowData(id);
}

export const PAndamentoShowService = withClientErrorHandler(executePAndamentoShowService);
