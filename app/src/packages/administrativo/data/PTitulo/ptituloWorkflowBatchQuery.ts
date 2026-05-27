import type { PTituloIndexQuery } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexQuery';

export type PTituloWorkflowEtapa = 'apontamento' | 'intimacao' | 'protesto';
export type PTituloWorkflowStatus = 'pendente' | 'concluido';

export function mapBatchStatusToWorkflowStatus(
  status: '' | 'P' | 'A' | 'I' | 'R',
): PTituloWorkflowStatus | undefined {
  if (status === 'P') return 'pendente';
  if (status === 'A' || status === 'I' || status === 'R') return 'concluido';
  return undefined;
}

export function buildPTituloWorkflowBatchQuery(options: {
  workflow_etapa: PTituloWorkflowEtapa;
  statusFilter: '' | 'P' | 'A' | 'I' | 'R';
  busca?: string;
}): PTituloIndexQuery {
  const busca = options.busca?.trim();
  return {
    workflow_etapa: options.workflow_etapa,
    workflow_status: mapBatchStatusToWorkflowStatus(options.statusFilter),
    busca: busca || undefined,
    busca_pessoa: busca || undefined,
  };
}
