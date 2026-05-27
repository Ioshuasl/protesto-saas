import { usePTituloWorkflowBatchReadHook } from '@/packages/administrativo/hooks/PTitulo/usePTituloWorkflowBatchReadHook';
import type { PTituloApontamentoBatchInterface } from '@/packages/apontamento-lote/interface/PTituloApontamentoBatch/PTituloApontamentoBatchInterface';

export const usePTituloApontamentoBatchReadHook = () => {
  const { titulos, setTitulos, isLoading, fetchTitulos } = usePTituloWorkflowBatchReadHook({
    successMessage: 'Títulos para apontamento em lote listados com sucesso',
  });

  return {
    titulosApontamentoBatch: titulos as PTituloApontamentoBatchInterface[],
    setTitulosApontamentoBatch: setTitulos,
    isLoading,
    fetchTitulosApontamentoBatch: fetchTitulos,
  };
};
