export const PTITULOARQUIVO_FAKE_ENDPOINTS = {
  index: "cra/p_arquivo_titulo/",
  show: (id: number) => `cra/p_arquivo_titulo/${id}/`,
};

export function usePTituloArquivoMockData() {
  return process.env.NEXT_PUBLIC_USE_MOCK_P_TITULO_ARQUIVO !== "false";
}
