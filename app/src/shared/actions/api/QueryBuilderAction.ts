export type Primitive = string | number | boolean;

export interface PaginationParams {
  /** Página lógica (1..N). Valores <= 0 são ignorados. */
  readonly page?: number;
  /**
   * Tamanho da página no padrão da API (per_page).
   * Valores <= 0 são ignorados.
   */
  readonly per_page?: number;
  /**
   * Alias legado para per_page. Se ambos estiverem presentes,
   * per_page tem precedência.
   */
  readonly page_size?: number;
}

export type SortDirection = 'asc' | 'desc';

export interface SortParams {
  /** Campo lógico para ordenação (ex.: "pessoa_id"). */
  readonly field?: string;
  /** Direção da ordenação. Default lógico: "asc". */
  readonly direction?: SortDirection;
}

export interface FilterCondition {
  /** Campo lógico permitido pelos allowed_fields do repositório. */
  readonly field: string;
  /** Operador de filtro (ex.: "eq", "in", "like"). */
  readonly operator: string;
  /** Valor simples ou lista de valores (para "in"). */
  readonly value: Primitive | ReadonlyArray<Primitive>;
}

export interface Formato3QueryParams {
  readonly pagination?: PaginationParams;
  readonly sort?: SortParams;
  readonly filters?: ReadonlyArray<FilterCondition>;
}

/**
 * Builder de query string no padrão "formato3", focado em baixo overhead.
 *
 * Converte um objeto de alto nível em:
 *   ?p=1&per_page=20&sort=pessoa_id.desc&f=campo:op:valor&f=...
 */
export class QueryBuilderAction {
  // Classe apenas estática
  private constructor() {}

  /**
   * Monta a query string (?p=...&pp=...&sort=...&f=...) a partir do objeto estruturado.
   */
  static build(params: Formato3QueryParams | null | undefined): string {
    if (!params) return '';

    const parts: string[] = [];

    // Paginação
    const pagination = params.pagination;
    if (pagination) {
      const { page, page_size: pageSize, per_page: perPage } = pagination;

      if (typeof page === 'number' && page > 0) {
        parts.push(`p=${encodeURIComponent(String(page))}`);
      }

      const effectivePageSize =
        typeof perPage === 'number' && perPage > 0
          ? perPage
          : typeof pageSize === 'number' && pageSize > 0
            ? pageSize
            : undefined;

      if (typeof effectivePageSize === 'number') {
        // Backend espera per_page na query string
        parts.push(`per_page=${encodeURIComponent(String(effectivePageSize))}`);
      }
    }

    // Ordenação
    const sort = params.sort;
    if (sort && sort.field) {
      const direction: SortDirection = sort.direction ?? 'asc';
      // sort=pessoa_id.desc
      const sortValue = `${sort.field}.${direction}`;
      parts.push(`sort=${encodeURIComponent(sortValue)}`);
    }

    // Filtros
    const filters = params.filters;
    if (filters && filters.length > 0) {
      for (let i = 0; i < filters.length; i++) {
        const f = filters[i];
        if (!f || !f.field || !f.operator) continue;

        // Normaliza value para string
        let valueStr: string;
        const value = f.value;

        if (Array.isArray(value)) {
          // Lista: join por vírgula (in:SP,RJ)
          const len = value.length;
          if (len === 0) continue;
          const tmp: string[] = new Array(len);
          for (let j = 0; j < len; j++) {
            tmp[j] = String(value[j]);
          }
          valueStr = tmp.join(',');
        } else {
          if (value === undefined || value === null || value === '') continue;
          valueStr = String(value);
        }

        const raw = `${f.field}:${f.operator}:${valueStr}`;
        parts.push(`f=${encodeURIComponent(raw)}`);
      }
    }

    if (parts.length === 0) {
      return '';
    }

    // Junta tudo em uma única string de query
    return `?${parts.join('&')}`;
  }
}
