/** Rotas em api/packages/v1/administrativo/endpoints/g_emolumento_endpoint.py */
export const GEMOLUMENTO_ENDPOINTS = {
  indexBySistema: (sistemaId: number) => `administrativo/g_emolumento/sistema/${sistemaId}`,
  show: (id: number) => `administrativo/g_emolumento/${id}`,
  create: 'administrativo/g_emolumento/',
  update: (id: number) => `administrativo/g_emolumento/${id}`,
  delete: (id: number) => `administrativo/g_emolumento/${id}`,
};
