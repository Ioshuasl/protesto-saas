import { buildPArquivoTituloIndexEndpoint } from "@/packages/cra/data/PTituloArquivo/pArquivoTituloIndexQueryBuilder";
import type { PArquivoTituloInterface } from "@/packages/cra/interface/PArquivoTitulo/PArquivoTituloInterface";
import type { PArquivoTituloIndexQuery } from "@/packages/cra/interface/PArquivoTitulo/PArquivoTituloIndexQuery";
import type { PArquivoTituloIndexResult } from "@/packages/cra/interface/PArquivoTitulo/PArquivoTituloIndexQuery";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";
import {
  DEFAULT_PAGINATION_META,
  normalizePaginationMeta,
  type PaginationMeta,
} from "@/shared/components/pagination";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

function emptyPArquivoTituloIndexResult(
  perPage = DEFAULT_PAGINATION_META.per_page,
): PArquivoTituloIndexResult {
  return {
    rows: [],
    pagination: { ...DEFAULT_PAGINATION_META, per_page: perPage },
  };
}

async function executePTituloArquivoIndexData(
  query?: PArquivoTituloIndexQuery,
): Promise<PArquivoTituloIndexResult> {
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: buildPArquivoTituloIndexEndpoint(query),
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return emptyPArquivoTituloIndexResult(perPage);
  }

  const rows = Array.isArray(response?.data)
    ? (response.data as PArquivoTituloInterface[])
    : [];
  const pagination = normalizePaginationMeta(
    (response?.pagination as Partial<PaginationMeta> | undefined) ?? undefined,
    perPage,
  );

  return { rows, pagination };
}

export const PTituloArquivoIndexData = withClientErrorHandler(executePTituloArquivoIndexData);
