export const GUSUARIO_FAKE_ENDPOINTS = {
  index: 'administrativo/g_usuario/',
  show: (id: number) => `administrativo/g_usuario/${id}/`,
  create: 'administrativo/g_usuario/',
  update: (id: number) => `administrativo/g_usuario/${id}/`,
  delete: (id: number) => `administrativo/g_usuario/${id}/`,
};

export function useGUsuarioMockData() {
  return process.env.NEXT_PUBLIC_USE_MOCK_GUSUARIO !== 'false';
}
