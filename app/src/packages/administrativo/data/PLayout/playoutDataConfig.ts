export const PLAYOUT_FAKE_ENDPOINTS = {
  index: "administrativo/p_layout/",
};

export function usePLayoutMockData() {
  return process.env.NEXT_PUBLIC_USE_MOCK_PLAYOUT !== "false";
}
