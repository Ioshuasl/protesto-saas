export const PTITULOAPONTAMENTOBATCH_FAKE_ENDPOINTS = {
  index: "apontamento-lote/p_titulo_apontamento_lote/",
};

export function usePTituloApontamentoBatchMockData() {
  return process.env.NEXT_PUBLIC_USE_MOCK_P_TITULO_APONTAMENTO_BATCH !== "false";
}
