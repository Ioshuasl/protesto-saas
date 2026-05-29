/** Rotas em api/packages/v1/administrativo/endpoints/p_arquivo_titulo_endpoint.py */
export const PARQUIVO_TITULO_ENDPOINTS = {
  index: "administrativo/p_arquivo_titulo/",
  show: (id: number) => `administrativo/p_arquivo_titulo/${id}/`,
  showTexto: (id: number) => `administrativo/p_arquivo_titulo/${id}/texto/`,
  showTextoImportado: (id: number) =>
    `administrativo/p_arquivo_titulo/${id}/texto_importado/`,
  download: (id: number) => `administrativo/p_arquivo_titulo/${id}/download/`,
};
