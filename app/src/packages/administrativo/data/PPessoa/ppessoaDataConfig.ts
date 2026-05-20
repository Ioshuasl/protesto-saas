export const PPESSOA_FAKE_ENDPOINTS = {
  index: 'administrativo/p_pessoa/',
  show: (id: number) => `administrativo/p_pessoa/${id}/`,
  create: 'administrativo/p_pessoa/',
  update: (id: number) => `administrativo/p_pessoa/${id}/`,
  delete: (id: number) => `administrativo/p_pessoa/${id}/`,
};

export function usePPessoaMockData() {
  return process.env.NEXT_PUBLIC_USE_MOCK_PPESSOA !== 'false';
}
