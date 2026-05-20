export const PTITULOINTIMACAOBATCH_FAKE_ENDPOINTS = {
  index: "intimacao-lote/p_titulo_intimacao_lote/",
};

export function usePTituloIntimacaoBatchMockData() {
  return process.env.NEXT_PUBLIC_USE_MOCK_P_TITULO_INTIMACAO_BATCH !== "false";
}
