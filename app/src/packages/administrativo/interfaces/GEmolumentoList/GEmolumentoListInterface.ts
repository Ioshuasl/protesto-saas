import type { GEmolumentoItemInterface } from '@/packages/administrativo/interfaces/GEmolumentoItem/GEmolumentoItemInterface';
import type { PaginationMeta } from '@/shared/components/pagination';

export interface GEmolumentoListFilter {
  emolumento_periodo_id?: number;
  sistema_id?: number | null;
  busca?: string;
}

export interface GEmolumentoListInterface extends GEmolumentoItemInterface {
  selo_grupo?: Record<string, unknown> | null;
  emolumento?: Record<string, unknown> | null;
}

export interface GEmolumentoListQuery extends GEmolumentoListFilter {
  page?: number;
  per_page?: number;
  sort?: string;
}

export interface GEmolumentoListResult {
  rows: GEmolumentoListInterface[];
  pagination: PaginationMeta;
}
