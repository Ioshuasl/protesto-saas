'use server';

import { PTITULO_ENDPOINTS } from '@/packages/administrativo/data/PTitulo/ptituloDataConfig';
import { createPTituloSomenteIndexData } from '@/packages/administrativo/data/PTitulo/ptituloSomenteIndexDataFactory';

export const PTituloSomenteApontadosData = createPTituloSomenteIndexData(
  PTITULO_ENDPOINTS.somenteApontados,
);
