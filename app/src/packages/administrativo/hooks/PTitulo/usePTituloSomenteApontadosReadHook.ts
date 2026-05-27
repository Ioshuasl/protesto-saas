import { createPTituloSomenteReadHook } from '@/packages/administrativo/hooks/PTitulo/ptituloSomenteReadHookFactory';
import { PTituloSomenteApontadosService } from '@/packages/administrativo/services/PTitulo/PTituloSomenteApontadosService';

export const usePTituloSomenteApontadosReadHook = createPTituloSomenteReadHook(
  PTituloSomenteApontadosService,
  'Títulos somente apontados listados com sucesso',
);
