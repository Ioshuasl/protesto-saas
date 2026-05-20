export const PTITULOPROTESTARBATCH_FAKE_ENDPOINTS = {
  index: "protesto-lote/p_titulo_protestar_lote/",
};

export function usePTituloProtestarBatchMockData() {
  return process.env.NEXT_PUBLIC_USE_MOCK_P_TITULO_PROTESTAR_BATCH !== "false";
}
