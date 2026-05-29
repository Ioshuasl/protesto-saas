import { PARQUIVO_TITULO_ENDPOINTS } from "@/packages/cra/data/PTituloArquivo/pTituloArquivoDataConfig";
import type { PArquivoTituloInterface } from "@/packages/cra/interface/PArquivoTitulo/PArquivoTituloInterface";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

export type PArquivoTituloShowQuery = {
  include?: string;
};

export async function PTituloArquivoShowData(
  arquivoTituloId: number,
  query?: PArquivoTituloShowQuery,
): Promise<PArquivoTituloInterface> {
  const params = new URLSearchParams();
  if (query?.include) {
    params.set("include", query.include);
  }

  const qs = params.toString();
  const endpoint = qs
    ? `${PARQUIVO_TITULO_ENDPOINTS.show(arquivoTituloId)}?${qs}`
    : PARQUIVO_TITULO_ENDPOINTS.show(arquivoTituloId);

  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PArquivoTituloInterface;
  }

  throw new Error(response?.message || "Arquivo de título não encontrado");
}
