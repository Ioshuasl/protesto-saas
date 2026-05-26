import type { PCertidaoIndexQuery } from "@/packages/certidao/interface/PCertidao/PCertidaoIndexQuery";

export const PCERTIDAO_FILTER_ALL = "__all__";

export type PCertidaoFilterState = {
  busca: string;
  tipo_certidao: string;
  status: string;
  data_inicio: string;
  data_fim: string;
};

export const defaultPCertidaoFilterState: PCertidaoFilterState = {
  busca: "",
  tipo_certidao: PCERTIDAO_FILTER_ALL,
  status: PCERTIDAO_FILTER_ALL,
  data_inicio: "",
  data_fim: "",
};

export function buildPCertidaoIndexQuery(
  state: PCertidaoFilterState,
): Omit<PCertidaoIndexQuery, "page" | "per_page"> | undefined {
  const params: Omit<PCertidaoIndexQuery, "page" | "per_page"> = {};
  const busca = state.busca.trim();

  if (busca) {
    params.busca = busca;
  }
  if (state.tipo_certidao === "P" || state.tipo_certidao === "N") {
    params.tipo_certidao = state.tipo_certidao;
  }
  if (state.status === "A" || state.status === "C") {
    params.status = state.status;
  }
  if (state.data_inicio) {
    params.data_inicio = state.data_inicio;
  }
  if (state.data_fim) {
    params.data_fim = state.data_fim;
  }

  return Object.keys(params).length > 0 ? params : undefined;
}
