export const CRAIMPORTACAO_FAKE_ENDPOINTS = {
  save: "cra/importacao/",
};

export function useCraImportacaoMockData() {
  return process.env.NEXT_PUBLIC_USE_MOCK_CRAIMPORTACAO !== "false";
}
