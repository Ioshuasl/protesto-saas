'use server';

import { PTITULO_ENDPOINTS } from '@/packages/administrativo/data/PTitulo/ptituloDataConfig';
import { createPTituloSomenteIndexData } from '@/packages/administrativo/data/PTitulo/ptituloSomenteIndexDataFactory';

export const PTituloSomenteCadastradosData = createPTituloSomenteIndexData(
  PTITULO_ENDPOINTS.somenteCadastrados,
);
