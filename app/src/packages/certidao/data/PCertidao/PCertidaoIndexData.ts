import { PCERTIDAO_ENDPOINTS } from "@/packages/certidao/data/PCertidao/pCertidaoDataConfig";
import type { PCertidaoInterface } from "@/packages/certidao/interface/PCertidao/PCertidaoInterface";
import type { PCertidaoIndexQuery } from "@/packages/certidao/interface/PCertidao/PCertidaoIndexQuery";
import type { PCertidaoIndexResult } from "@/packages/certidao/interface/PCertidao/PCertidaoIndexResult";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";
import {
  DEFAULT_PAGINATION_META,
  normalizePaginationMeta,
  type PaginationMeta,
} from "@/shared/components/pagination";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

function buildPCertidaoIndexEndpoint(query?: PCertidaoIndexQuery): string {
  const params = new URLSearchParams();
  const page = query?.page ?? DEFAULT_PAGINATION_META.page;
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  params.set("p", String(page));
  params.set("per_page", String(perPage));
  params.set("sort", "certidao_id.desc");

  if (query?.tipo_certidao) params.set("tipo_certidao", query.tipo_certidao);
  if (query?.data_certidao) params.set("data_certidao", query.data_certidao);
  if (query?.data_inicio) params.set("data_inicio", query.data_inicio);
  if (query?.data_fim) params.set("data_fim", query.data_fim);
  if (query?.status) params.set("status", query.status);
  if (query?.busca) params.set("busca", query.busca);

  return `${PCERTIDAO_ENDPOINTS.index}?${params.toString()}`;
}

function emptyPCertidaoIndexResult(perPage = DEFAULT_PAGINATION_META.per_page): PCertidaoIndexResult {
  return {
    rows: [],
    pagination: { ...DEFAULT_PAGINATION_META, per_page: perPage },
  };
}

async function executePCertidaoIndexData(query?: PCertidaoIndexQuery): Promise<PCertidaoIndexResult> {
  const api = new API();
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  const response = await api.send({
    method: Methods.GET,
    endpoint: buildPCertidaoIndexEndpoint(query),
  });

  if (Number(response?.status) < 200 || Number(response?.status) >= 300) {
    return emptyPCertidaoIndexResult(perPage);
  }

  const rows = Array.isArray(response?.data) ? (response.data as PCertidaoInterface[]) : [];
  const pagination = normalizePaginationMeta(
    (response?.pagination as Partial<PaginationMeta> | undefined) ?? undefined,
    perPage,
  );

  return { rows, pagination };
}

export const PCertidaoIndexData = withClientErrorHandler(executePCertidaoIndexData);
