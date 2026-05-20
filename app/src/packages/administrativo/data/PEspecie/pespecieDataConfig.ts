export const PESPECIE_FAKE_ENDPOINTS = {
  index: 'administrativo/p_especie/',
  show: (id: number) => `administrativo/p_especie/${id}/`,
  create: 'administrativo/p_especie/',
  update: (id: number) => `administrativo/p_especie/${id}/`,
  delete: (id: number) => `administrativo/p_especie/${id}/`,
};

export function usePEspecieMockData() {
  return process.env.NEXT_PUBLIC_USE_MOCK_PESPECIE !== 'false';
}
