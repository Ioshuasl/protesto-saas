export type PPessoaIndexQuery = {
  /** Busca unificada em nome, CPF/CNPJ e telefone (resultados concatenados na API). */
  busca?: string;
  /** Valor exato do seletor de cidade (CIDADE). */
  cidade?: string;
  /** Valor exato do seletor de UF. */
  uf?: string;
  /** F = CPF (11 dígitos); J = CNPJ (14 dígitos). */
  tipo_pessoa?: 'F' | 'J';
  page?: number;
  per_page?: number;
  /** formato3: ex. pessoa_id.desc */
  sort?: string;
};
