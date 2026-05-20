'use server';

import { PTituloLiquidacaoData } from '@/packages/administrativo/data/PTitulo/PTituloLiquidacaoData';
import type { PTituloLiquidacaoFormInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloLiquidacaoFormInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executePTituloLiquidacaoService(id: number, payload?: PTituloLiquidacaoFormInterface) {
  return PTituloLiquidacaoData(id, payload);
}

export const PTituloLiquidacaoService = withClientErrorHandler(
  executePTituloLiquidacaoService,
);
