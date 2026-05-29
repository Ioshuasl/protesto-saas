import type { PArquivoTituloIndexQuery } from "@/packages/cra/interface/PArquivoTitulo/PArquivoTituloIndexQuery";
import { PARQUIVO_TITULO_ENDPOINTS } from "@/packages/cra/data/PTituloArquivo/pTituloArquivoDataConfig";
import { DEFAULT_PAGINATION_META } from "@/shared/components/pagination";

export function buildPArquivoTituloIndexEndpoint(query?: PArquivoTituloIndexQuery): string {
  const params = new URLSearchParams();
  const page = query?.page ?? DEFAULT_PAGINATION_META.page;
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  params.set("p", String(page));
  params.set("per_page", String(perPage));
  params.set("sort", query?.sort ?? "arquivo_titulo_id.desc");

  if (query?.include) params.set("include", query.include);
  if (query?.portador_codigo) params.set("portador_codigo", query.portador_codigo);
  if (query?.data_inicio) params.set("data_inicio", query.data_inicio);
  if (query?.data_fim) params.set("data_fim", query.data_fim);

  return `${PARQUIVO_TITULO_ENDPOINTS.index}?${params.toString()}`;
}
