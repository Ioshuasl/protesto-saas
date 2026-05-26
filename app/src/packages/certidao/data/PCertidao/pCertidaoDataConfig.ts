/** Rotas em api/packages/v1/administrativo/endpoints/p_certidao_endpoint.py */
export const PCERTIDAO_ENDPOINTS = {
  index: "administrativo/p_certidao/",
  show: (id: number) => `administrativo/p_certidao/${id}`,
  create: "administrativo/p_certidao/",
  update: (id: number) => `administrativo/p_certidao/${id}`,
  delete: (id: number) => `administrativo/p_certidao/${id}`,
  cancelar: (id: number) => `administrativo/p_certidao/${id}/cancelar`,
  consultaApresentante: "administrativo/p_certidao/consulta_apresentante/",
};
