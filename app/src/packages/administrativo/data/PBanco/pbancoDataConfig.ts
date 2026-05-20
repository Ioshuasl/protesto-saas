export const PBANCO_FAKE_ENDPOINTS = {
  index: 'administrativo/p_banco/',
  show: (id: number) => `administrativo/p_banco/${id}/`,
  create: 'administrativo/p_banco/',
  update: (id: number) => `administrativo/p_banco/${id}/`,
  delete: (id: number) => `administrativo/p_banco/${id}/`,
};

export function usePBancoMockData() {
  return process.env.NEXT_PUBLIC_USE_MOCK_PBANCO !== 'false';
}
