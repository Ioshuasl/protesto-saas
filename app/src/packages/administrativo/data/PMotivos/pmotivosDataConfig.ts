export const PMOTIVOS_FAKE_ENDPOINTS = {
  index: 'administrativo/p_motivos/',
  show: (id: number) => `administrativo/p_motivos/${id}/`,
  create: 'administrativo/p_motivos/',
  update: (id: number) => `administrativo/p_motivos/${id}/`,
  delete: (id: number) => `administrativo/p_motivos/${id}/`,
};

export function usePMotivosMockData() {
  return process.env.NEXT_PUBLIC_USE_MOCK_PMOTIVOS !== 'false';
}
