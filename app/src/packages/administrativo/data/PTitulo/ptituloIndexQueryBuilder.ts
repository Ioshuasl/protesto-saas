import type { PTituloIndexQuery } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexQuery';
import { DEFAULT_PAGINATION_META } from '@/shared/components/pagination';

export function buildPTituloIndexEndpoint(
  basePath: string,
  query?: PTituloIndexQuery,
): string {
  const params = new URLSearchParams();

  const page = query?.page ?? DEFAULT_PAGINATION_META.page;
  const perPage = query?.per_page ?? DEFAULT_PAGINATION_META.per_page;

  params.set('p', String(page));
  params.set('per_page', String(perPage));
  params.set('sort', query?.sort ?? 'titulo_id.desc');

  if (query?.busca) params.set('busca', query.busca);
  if (query?.busca_pessoa) params.set('busca_pessoa', query.busca_pessoa);
  if (query?.numero_apontamento != null) {
    params.set('numero_apontamento', String(query.numero_apontamento));
  }
  if (query?.nosso_numero) params.set('nosso_numero', query.nosso_numero);
  if (query?.numero_titulo) params.set('numero_titulo', query.numero_titulo);
  if (query?.numero_titulo_banco) {
    params.set('numero_titulo_banco', query.numero_titulo_banco);
  }
  if (query?.ocorrencia_id != null) params.set('ocorrencia_id', String(query.ocorrencia_id));
  if (query?.ocorrencia_andamento_id != null) {
    params.set('ocorrencia_andamento_id', String(query.ocorrencia_andamento_id));
  }
  if (query?.banco_id != null) params.set('banco_id', String(query.banco_id));
  if (query?.especie_id != null) params.set('especie_id', String(query.especie_id));
  if (query?.situacao_data) params.set('situacao_data', query.situacao_data);
  if (query?.workflow_etapa) params.set('workflow_etapa', query.workflow_etapa);
  if (query?.workflow_status) params.set('workflow_status', query.workflow_status);

  const qs = params.toString();
  return qs ? `${basePath}?${qs}` : basePath;
}
