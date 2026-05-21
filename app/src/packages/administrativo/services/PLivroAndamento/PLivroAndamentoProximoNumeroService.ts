'use server';

import { PLivroAndamentoProximoNumeroData } from '@/packages/administrativo/data/PLivroAndamento/PLivroAndamentoProximoNumeroData';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePLivroAndamentoProximoNumeroService(livroNaturezaId: number) {
  return await PLivroAndamentoProximoNumeroData(livroNaturezaId);
}

export const PLivroAndamentoProximoNumeroService = withClientErrorHandler(
  executePLivroAndamentoProximoNumeroService,
);
