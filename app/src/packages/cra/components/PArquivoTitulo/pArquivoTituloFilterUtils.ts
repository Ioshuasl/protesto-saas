import type { PArquivoTituloIndexQuery } from "@/packages/cra/interface/PArquivoTitulo/PArquivoTituloIndexQuery";

export type PArquivoTituloFilterState = {
  bancoId: string;
  data_inicio: string;
  data_fim: string;
};

export const defaultPArquivoTituloFilterState: PArquivoTituloFilterState = {
  bancoId: "",
  data_inicio: "",
  data_fim: "",
};

export function buildPArquivoTituloIndexQuery(
  state: PArquivoTituloFilterState,
  bancoCodigoById: Map<string, string>,
): Omit<PArquivoTituloIndexQuery, "page" | "per_page" | "sort"> | undefined {
  const params: Omit<PArquivoTituloIndexQuery, "page" | "per_page" | "sort"> = {};

  if (state.bancoId) {
    const codigo = bancoCodigoById.get(state.bancoId)?.trim();
    if (codigo) {
      params.portador_codigo = codigo.toUpperCase();
    }
  }
  if (state.data_inicio) {
    params.data_inicio = state.data_inicio;
  }
  if (state.data_fim) {
    params.data_fim = state.data_fim;
  }

  return Object.keys(params).length > 0 ? params : undefined;
}
