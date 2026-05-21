import type { PLivroNaturezaInterface } from '@/packages/administrativo/interfaces/PLivroNatureza/PLivroNaturezaInterface';
import type { PaginationMeta } from '@/shared/components/pagination';

export type PLivroNaturezaIndexResult = {
  rows: PLivroNaturezaInterface[];
  pagination: PaginationMeta;
};
