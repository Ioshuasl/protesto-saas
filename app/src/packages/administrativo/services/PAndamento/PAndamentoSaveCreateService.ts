'use server';

import { PAndamentoSaveCreateData } from '@/packages/administrativo/data/PAndamento/PAndamentoSaveData';
import type { PAndamentoSavePayload } from '@/packages/administrativo/interfaces/PAndamento/PAndamentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePAndamentoSaveCreateService(data: PAndamentoSavePayload) {
  return await PAndamentoSaveCreateData(data);
}

export const PAndamentoSaveCreateService = withClientErrorHandler(
  executePAndamentoSaveCreateService,
);
