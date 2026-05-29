/** Rotas em api/packages/v1/administrativo/endpoints/p_banco_endpoint.py */
export const PBANCO_ENDPOINTS = {
  index: 'administrativo/p_banco/',
  show: (id: number) => `administrativo/p_banco/${id}`,
  showByCodigo: (codigo: string) =>
    `administrativo/p_banco/codigo/${encodeURIComponent(codigo.trim())}`,
  create: 'administrativo/p_banco/',
  update: (id: number) => `administrativo/p_banco/${id}`,
  delete: (id: number) => `administrativo/p_banco/${id}`,
};
