import type { PPessoaIndexQuery } from '@/packages/administrativo/interfaces/PPessoa/PPessoaIndexQuery';

export const PPESSOA_FILTER_ALL = 'ALL';

export type PPessoaTipoPessoaFilter = 'F' | 'J' | typeof PPESSOA_FILTER_ALL;

export type PPessoaFilterState = {
  search: string;
  tipo_pessoa: PPessoaTipoPessoaFilter;
  cidade?: string;
  uf?: string;
};

export const defaultPPessoaFilterState: PPessoaFilterState = {
  search: '',
  tipo_pessoa: PPESSOA_FILTER_ALL,
  cidade: undefined,
  uf: undefined,
};

export function buildPPessoaIndexQuery(
  state: PPessoaFilterState,
): PPessoaIndexQuery | undefined {
  const busca = state.search.trim();
  const cidade = state.cidade?.trim();
  const uf = state.uf?.trim();
  const tipoPessoa =
    state.tipo_pessoa !== PPESSOA_FILTER_ALL ? state.tipo_pessoa : undefined;

  if (!busca && !cidade && !uf && !tipoPessoa) {
    return undefined;
  }

  const query: PPessoaIndexQuery = {};

  if (busca) query.busca = busca;
  if (cidade) query.cidade = cidade;
  if (uf) query.uf = uf.toUpperCase();
  if (tipoPessoa) query.tipo_pessoa = tipoPessoa;

  return query;
}
