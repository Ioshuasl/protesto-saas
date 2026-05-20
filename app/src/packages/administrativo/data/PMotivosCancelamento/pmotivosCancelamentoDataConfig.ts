export const PMOTIVOS_CANCELAMENTO_FAKE_ENDPOINTS = {
  index: 'administrativo/p_motivos_cancelamento/',
  show: (id: number) => `administrativo/p_motivos_cancelamento/${id}/`,
  create: 'administrativo/p_motivos_cancelamento/',
  update: (id: number) => `administrativo/p_motivos_cancelamento/${id}/`,
  delete: (id: number) => `administrativo/p_motivos_cancelamento/${id}/`,
};

export function usePMotivosCancelamentoMockData() {
  return process.env.NEXT_PUBLIC_USE_MOCK_PMOTIVOS_CANCELAMENTO !== 'false';
}
