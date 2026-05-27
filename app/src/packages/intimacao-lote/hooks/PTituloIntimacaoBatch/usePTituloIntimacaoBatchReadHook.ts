import { usePTituloWorkflowBatchReadHook } from '@/packages/administrativo/hooks/PTitulo/usePTituloWorkflowBatchReadHook';
import type { PTituloIntimacaoBatchInterface } from '@/packages/intimacao-lote/interface/PTituloIntimacaoBatch/PTituloIntimacaoBatchInterface';

export const usePTituloIntimacaoBatchReadHook = () => {
  const { titulos, setTitulos, isLoading, fetchTitulos } = usePTituloWorkflowBatchReadHook({
    successMessage: 'Títulos para intimação em lote listados com sucesso',
  });

  return {
    titulosIntimacaoBatch: titulos as PTituloIntimacaoBatchInterface[],
    setTitulosIntimacaoBatch: setTitulos,
    isLoading,
    fetchTitulosIntimacaoBatch: fetchTitulos,
  };
};
