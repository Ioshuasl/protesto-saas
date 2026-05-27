import { createPTituloSomenteReadHook } from '@/packages/administrativo/hooks/PTitulo/ptituloSomenteReadHookFactory';
import { PTituloSomenteCadastradosService } from '@/packages/administrativo/services/PTitulo/PTituloSomenteCadastradosService';

export const usePTituloSomenteCadastradosReadHook = createPTituloSomenteReadHook(
  PTituloSomenteCadastradosService,
  'Títulos somente cadastrados listados com sucesso',
);
