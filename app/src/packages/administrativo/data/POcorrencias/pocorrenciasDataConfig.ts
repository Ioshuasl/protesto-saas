export const POCORRENCIAS_FAKE_ENDPOINTS = {
  index: 'administrativo/p_ocorrencias/',
  show: (id: number) => `administrativo/p_ocorrencias/${id}/`,
  create: 'administrativo/p_ocorrencias/',
  update: (id: number) => `administrativo/p_ocorrencias/${id}/`,
  delete: (id: number) => `administrativo/p_ocorrencias/${id}/`,
};

export function usePOcorrenciasMockData() {
  return process.env.NEXT_PUBLIC_USE_MOCK_POCORRENCIAS !== 'false';
}
