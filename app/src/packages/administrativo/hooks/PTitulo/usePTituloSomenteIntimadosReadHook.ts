import { createPTituloSomenteReadHook } from '@/packages/administrativo/hooks/PTitulo/ptituloSomenteReadHookFactory';
import { PTituloSomenteIntimadosService } from '@/packages/administrativo/services/PTitulo/PTituloSomenteIntimadosService';

export const usePTituloSomenteIntimadosReadHook = createPTituloSomenteReadHook(
  PTituloSomenteIntimadosService,
  'Títulos somente intimados listados com sucesso',
);
