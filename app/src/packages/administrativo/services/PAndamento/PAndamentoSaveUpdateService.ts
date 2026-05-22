'use server';

import { PAndamentoSaveUpdateData } from '@/packages/administrativo/data/PAndamento/PAndamentoSaveData';
import type { PAndamentoUpdatePayload } from '@/packages/administrativo/interfaces/PAndamento/PAndamentoInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePAndamentoSaveUpdateService(
  id: number,
  data: PAndamentoUpdatePayload,
) {
  return await PAndamentoSaveUpdateData(id, data);
}

export const PAndamentoSaveUpdateService = withClientErrorHandler(
  executePAndamentoSaveUpdateService,
);
