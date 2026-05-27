import { usePTituloWorkflowBatchReadHook } from '@/packages/administrativo/hooks/PTitulo/usePTituloWorkflowBatchReadHook';
import type { PTituloProtestarBatchInterface } from '@/packages/protesto-lote/interface/PTituloProtestarBatch/PTituloProtestarBatchInterface';

export const usePTituloProtestarBatchReadHook = () => {
  const { titulos, setTitulos, isLoading, fetchTitulos } = usePTituloWorkflowBatchReadHook({
    successMessage: 'Títulos para protesto em lote listados com sucesso',
  });

  return {
    titulosProtestarBatch: titulos as PTituloProtestarBatchInterface[],
    setTitulosProtestarBatch: setTitulos,
    isLoading,
    fetchTitulosProtestarBatch: fetchTitulos,
  };
};
