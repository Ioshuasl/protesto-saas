export const PRETORNOCRA_FAKE_ENDPOINTS = {
  index: "cra/retorno/",
};

export function usePRetornoCraMockData() {
  return process.env.NEXT_PUBLIC_USE_MOCK_P_RETORNO_CRA !== "false";
}
