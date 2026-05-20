export const PCERTIDAO_FAKE_ENDPOINTS = {
  index: "certidao/p_certidao/",
  show: (id: number) => `certidao/p_certidao/${id}/`,
  create: "certidao/p_certidao/",
  update: (id: number) => `certidao/p_certidao/${id}/`,
  consultaApresentante: "certidao/p_certidao/consulta_apresentante/",
};

export function usePCertidaoMockData() {
  return process.env.NEXT_PUBLIC_USE_MOCK_P_CERTIDAO !== "false";
}
