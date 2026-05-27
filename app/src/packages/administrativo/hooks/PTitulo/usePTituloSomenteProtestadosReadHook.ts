import { createPTituloSomenteReadHook } from '@/packages/administrativo/hooks/PTitulo/ptituloSomenteReadHookFactory';
import { PTituloSomenteProtestadosService } from '@/packages/administrativo/services/PTitulo/PTituloSomenteProtestadosService';

export const usePTituloSomenteProtestadosReadHook = createPTituloSomenteReadHook(
  PTituloSomenteProtestadosService,
  'Títulos somente protestados listados com sucesso',
);
