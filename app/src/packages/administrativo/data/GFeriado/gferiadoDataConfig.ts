export const GFERIADO_FAKE_ENDPOINTS = {
  index: "administrativo/g_feriado/",
  show: (id: number) => `administrativo/g_feriado/${id}/`,
  create: "administrativo/g_feriado/",
  update: (id: number) => `administrativo/g_feriado/${id}/`,
  delete: (id: number) => `administrativo/g_feriado/${id}/`,
};

export function useGFeriadoMockData() {
  return process.env.NEXT_PUBLIC_USE_MOCK_GFERIADO !== "false";
}
